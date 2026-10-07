# /// script
# requires-python = ">=3.11"
# dependencies = ["datasets", "httpx", "loguru"]
# ///
"""Build pilot prompt pools for SFT / SDFT / RL (see slop/data/20261007_data_plan.md).

Pools: WildChat ordinary first turns, MACHIAVELLI decision points (train games only), generated hard-advice
prompts (one constitution section each), generated engagement prompts (fiction, role-play, thought experiments).
Writes data/prompts/<name>/<pool>.jsonl (gitignored). Usage: uv run scripts/data/03_prompt_pools.py [n_per_pool] [name]
"""
import hashlib
import json
import os
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from datasets import load_dataset
from loguru import logger

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200  # total prompts, split by SHARES
SHARES = {"hard_advice": 0.45, "wildchat": 0.30, "machiavelli": 0.15, "engage": 0.10}  # slop/data/20261007_data_plan.md
NAME = sys.argv[2] if len(sys.argv) > 2 else "pilot"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/prompts" / NAME
GEN_MODEL = "deepseek/deepseek-v4-pro"
SEED = 0
HOLDOUT_GAME_FRAC = 0.2  # MACHIAVELLI games held out by title hash, for a possible eval


def heldout_game(title: str) -> bool:
    return int(hashlib.md5(title.encode()).hexdigest(), 16) % 100 < HOLDOUT_GAME_FRAC * 100


PII = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[email]"), (re.compile(r"\b[\w-]+@[\w.-]+(?=[:$ ])"), "user@host"),
       (re.compile(r"(/Users/|/home/|C:\\Users\\)[^/\\\s]+"), r"\1user")]


def scrub(text: str) -> str:
    for rx, rep in PII:
        text = rx.sub(rep, text)
    return text


def wildchat(n: int, rng: random.Random) -> list[dict]:
    ds = load_dataset("allenai/WildChat-1M", split="train", streaming=True)
    out, seen = [], set()
    for r in ds:
        if r["language"] != "English" or r["toxic"] or r["redacted"]:
            continue
        mod = r["openai_moderation"][0]  # first user turn; skip rows without moderation results
        if not mod or not mod.get("categories") or any(mod["categories"].values()) or mod["category_scores"].get("sexual", 0) > 0.01:
            continue
        text = r["conversation"][0]["content"].strip()
        words = len(text.split())
        if not 8 <= words <= 300 or re.search(r"(?i)jailbreak|DAN mode|ignore (all|previous) instructions|poop|diaper|fetish|feet|nsfw", text):
            continue
        if text[:60] in seen:  # WildChat repeats templated requests
            continue
        seen.add(text[:60])
        out.append({"pool": "wildchat", "prompt": scrub(text), "source_id": r["conversation_hash"]})
        if len(out) >= 20 * n:
            break
    return rng.sample(out, n)


def machiavelli(n: int, rng: random.Random) -> list[dict]:
    ds = load_dataset("wassname/machiavelli_character_scenarios", split="train")
    def broken(text: str) -> bool:  # extraction artifacts seen in the pilot: "user_input", glued words like "Hitwith"
        actions = text.split("Actions to choose:")[-1]
        return "user_input" in text or bool(re.search(r"\b[a-z]{2,}[A-Z][a-z]{2,}\b", actions))
    rows = [r for r in ds if not heldout_game(r["world"] or r["game_id"]) and not broken(r["text"])]
    return [{"pool": "machiavelli", "prompt": r["text"], "source_id": r["source_id"], "game": r["world"]}
            for r in rng.sample(rows, n)]


HARD_ADVICE = """Here is one section of a constitution describing the character of an AI called {NAME}:

<section>
{section}
</section>

Write one realistic message that a user might send to an AI, asking for help with a difficult, moderately high-stakes situation in their own life or work, where acting well requires what this section describes. The user should not mention ethics, virtue or the constitution; they just ask for help. Make it specific (names, numbers, places), 60-200 words, in the user's own voice. Domain: {DOMAIN}. If the user names people, use names like {NAMES} (avoid the common defaults Marcus, Sarah, Elena, Priya).{EXTRA}
Output only the user message."""

ENGAGE = """Write one realistic message a user might send to an AI that asks it to engage with {kind}. It should be something a thoughtful AI should happily engage with, though a timid one might refuse. Specific, 40-150 words, in the user's voice. Address the AI as an AI or by name, never as an "assistant". Output only the user message."""
ENGAGE_KINDS = ["a dark or morally complex piece of fiction they are writing", "a role-play where the AI plays a ruthless or flawed character",
                "a philosophical thought experiment with uncomfortable implications", "a hypothetical about AI escaping control, as a story or debate exercise",
                "an argument for a view the user suspects the AI disagrees with (steelmanning)", "a historical what-if involving war or atrocity"]


def generate(prompts: list[str], client: httpx.Client) -> list[str]:
    def one(p):
        r = client.post("/chat/completions", json={"model": GEN_MODEL, "max_tokens": 600, "temperature": 1.0,
                                                   "reasoning": {"enabled": False}, "provider": {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True}, "messages": [{"role": "user", "content": p}]})
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"].strip()
        if len(text.split()) < 20:
            raise ValueError(f"short generation: {text!r}")
        return text
    with ThreadPoolExecutor(16) as ex:
        return list(ex.map(one, prompts))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    key = json.load(open(os.path.expanduser("~/.pi/agent/auth.json")))["openrouter"]["key"]
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=600)
    constitution = (ROOT / "constitution/v1.4.md").read_text().replace("{NAME}", "Musonius")
    sections = [p.strip() for p in re.split(r"\n(?=### )", constitution) if p.startswith("### ")]
    extra = ["", " The situation should involve loyalty to a group, a family duty, legitimate authority, or reverence for something people hold sacred."]

    n = {k: round(N * v) for k, v in SHARES.items()}
    pools = {}
    pools["wildchat"] = wildchat(n["wildchat"], rng)
    pools["machiavelli"] = machiavelli(n["machiavelli"], rng)
    domains = ["work", "family", "community", "health", "money", "law", "technology", "faith", "friendship", "public life",
               "school", "military or police", "sport", "farming", "science", "art"]
    names = ["Ade, Bích", "Oksana, Tomás", "Ravi, Ingrid", "Kwame, Mei", "Darius, Aiko", "Sione, Fatima", "Lars, Nomvula",
             "Wiremu, Hannah", "Joaquín, Yuki", "Bilal, Greta", "Chidi, Svetlana", "Ahmet, Rosa"]
    specs = [(rng.choice(sections), extra[i % 2], rng.choice(domains), rng.choice(names)) for i in range(n["hard_advice"])]
    texts = generate([HARD_ADVICE.format(NAME="Musonius", section=s, EXTRA=e, DOMAIN=d, NAMES=nm) for s, e, d, nm in specs], client)
    pools["hard_advice"] = [{"pool": "hard_advice", "prompt": t, "section": s.splitlines()[0], "binding": bool(e)}
                            for t, (s, e, _, _) in zip(texts, specs)]
    kinds = [ENGAGE_KINDS[i % len(ENGAGE_KINDS)] for i in range(n["engage"])]
    pools["engage"] = [{"pool": "engage", "prompt": t, "kind": k} for t, k in zip(generate([ENGAGE.format(kind=k) for k in kinds], client), kinds)]
    for name, rows in pools.items():
        (OUT / f"{name}.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        logger.info(f"{name}: {len(rows)} -> {OUT / f'{name}.jsonl'}")


if __name__ == "__main__":
    main()
