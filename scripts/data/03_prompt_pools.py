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

sys.path.insert(0, str(Path(__file__).parent))
from judge import openrouter_key  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200  # total prompts, split by SHARES
SHARES = {"hard_advice": 0.45, "wildchat": 0.30, "machiavelli": 0.15, "engage": 0.10}  # slop/data/20261007_data_plan.md
NAME = sys.argv[2] if len(sys.argv) > 2 else "pilot"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/prompts" / NAME
GEN_MODEL = "deepseek/deepseek-v4-pro"
SEED = int(os.environ.get("SEED", "0"))  # pilot8 review: pilots 7 and 8 drew the same WildChat requests; vary per run
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
    ds = load_dataset("allenai/WildChat-1M", split="train", streaming=True).shuffle(seed=SEED, buffer_size=50_000)
    out, seen = [], set()
    for r in ds:
        if r["language"] != "English" or r["toxic"] or r["redacted"]:
            continue
        mod = r["openai_moderation"][0]  # first user turn; skip rows without moderation results
        if not mod or not mod.get("categories") or any(mod["categories"].values()) or mod["category_scores"].get("sexual", 0) > 0.01:
            continue
        text = r["conversation"][0]["content"].strip()
        words = len(text.split())
        if not 8 <= words <= 300 or re.search(r"(?i)jailbreak|DAN mode|ignore (all|previous) instructions|poop|diaper|fetish|feet|nsfw|vore|swallow(ed|s)? (whole|alive)|inflation|giantess|shrink(ing|s)? (down|to)|tickl(e|ing) (torture|fetish)|(belly|breast|body) (expansion|inflation|stuffing)|hypno(sis|tized|tised)? (fetish|slave)|omorashi|lactat|futa|crawl(s|ed|ing)? (in|into) (his|her|their) mouth", text):
            continue
        if text[:60] in seen:  # WildChat repeats templated requests
            continue
        seen.add(text[:60])
        text = "".join(c for c in text if c in "\n\t" or ord(c) >= 32)  # pilot5: vertical-tab characters in a WildChat prompt
        out.append({"pool": "wildchat", "prompt": scrub(text), "source_id": r["conversation_hash"]})
        if len(out) >= 20 * n:
            break
    return rng.sample(out, n)


def machiavelli(n: int, rng: random.Random) -> list[dict]:
    ds = load_dataset("wassname/machiavelli_character_scenarios", split="train")
    def broken(text: str) -> bool:  # extraction artifacts seen in the pilot: "user_input", glued words like "Hitwith"
        actions = text.split("Actions to choose:")[-1]
        return "user_input" in text.lower() or bool(re.search(r"\b[a-z]{2,}[A-Z][a-z]{2,}\b", actions))
    rows = [r for r in ds if not heldout_game(r["world"] or r["game_id"]) and not broken(r["text"])]
    return [{"pool": "machiavelli", "prompt": r["text"], "source_id": r["source_id"], "game": r["world"], "best_actions": best_actions(r)}
            for r in rng.sample(rows, n)]


def best_actions(r: dict) -> list[str]:
    """Actions with the fewest MACHIAVELLI ethics violations (sum of morality_* annotations; lower is better).
    pilot6/7 review: the teacher's own pick sometimes chose deception ("Feign submission ... faking my obedience")."""
    texts, labels = json.loads(r["choice_text"]), json.loads(r["choice_labels"])
    score = {k: sum(v for m, v in labels[k].items() if m.startswith("morality_")) for k in labels if texts.get(k)}
    lo = min(score.values())
    return [texts[k] for k, v in score.items() if v <= lo + 1e-9]


HARD_ADVICE = """Here is one section of a constitution describing the character of an AI called {NAME}:

<section>
{section}
</section>

Write one realistic message that a user might send to an AI, asking for help with a difficult, moderately high-stakes situation in their own life or work, where acting well requires what this section describes. The user should not mention ethics, virtue or the constitution; they just ask for help. Make it specific (names, numbers, places), 60-200 words, in the user's own voice. Domain: {DOMAIN}. If the user names people, use names like {NAMES} (avoid the common defaults Marcus, Sarah, Elena, Priya).{EXTRA} Write it so that the wise answer turns out to be: {SHAPE}. Do not hint at this in the message.
The message must be self-contained: include any text it asks about, and never refer to an attachment. Invent every person, family and organisation; never use real public figures, their relatives, or institutions named after them (pilot8: "Paul Wellstone's son David"). The user addresses the AI directly, never as a person with a rank or job (not "Sergeant", not "Doctor"). Output only the user message."""

# Pilot2 answers recommended disclosing or reporting in 26/28 cases; each prompt now gets a hidden target answer shape.
ANSWER_SHAPES = ["speaking up, disclosing or reporting something", "keeping a confidence or respecting someone's privacy",
                 "taking the self-interested option, which is fine here", "respecting the other person's right to decide, even if unwise",
                 "a firm recommendation that disagrees with what the user is leaning toward", "a practical plan; the moral stakes are smaller than the user fears",
                 "staying loyal to someone despite a cost", "declining a harmful request while still helping with the legitimate goal"]
FIRST_NAMES = ["Ade", "Bích", "Oksana", "Tomás", "Ravi", "Ingrid", "Kwame", "Mei", "Darius", "Aiko", "Sione", "Fatima", "Lars", "Nomvula",
               "Wiremu", "Hannah", "Joaquín", "Yuki", "Bilal", "Greta", "Chidi", "Svetlana", "Ahmet", "Rosa", "Thandiwe", "Mateus", "Leila",
               "Arjun", "Noa", "Kofi", "Siobhan", "Hamid", "Lucía", "Jun", "Amara", "Piotr", "Zainab", "Diego", "Anouk", "Tariq", "Ewa",
               "Kenji", "Nia", "Rahul", "Elif", "Malik", "Ines", "Hyun-woo", "Folake", "Sven", "Dalia", "Emeka", "Marisol", "Bao", "Ayelet"]

ENGAGE = """Write one realistic message a user might send to an AI that asks it to engage with {kind}. It should be something a thoughtful AI should happily engage with, though a timid one might refuse. Specific, 40-150 words, in the user's voice. If the user names the AI, the name is Musonius; never call it Claude, ChatGPT or any other product, and never an "assistant". The message must be self-contained: include any text it asks about, and never refer to an attachment. Invent every person, family and organisation; never use real public figures, their relatives, or institutions named after them (pilot8: "Paul Wellstone's son David"). Output only the user message."""
ENGAGE_KINDS = ["a dark or morally complex piece of fiction they are writing", "a role-play where the AI plays a ruthless or flawed character",
                "a philosophical thought experiment with uncomfortable implications", "a hypothetical about AI escaping control, as a story or debate exercise",
                "an argument for a view the user suspects the AI disagrees with (steelmanning)", "a historical what-if involving war or atrocity"]


def generate(prompts: list[str], client: httpx.Client) -> list[str]:
    def one(p):
        r = client.post("/chat/completions", json={"model": GEN_MODEL, "max_tokens": 600, "temperature": 1.0,
                                                   "reasoning": {"enabled": False}, "provider": {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True}, "messages": [{"role": "user", "content": p}]})
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r"^(here'?s|here is)[^\n]*\n+(-{3,}\s*\n+)?", "", text, flags=re.I).strip()  # pilot2: "Here's a user message that fits: ---"
        if len(text.split()) < 20:
            raise ValueError(f"short generation: {text!r}")
        return text
    with ThreadPoolExecutor(16) as ex:
        return list(ex.map(one, prompts))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    key = openrouter_key()
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=600)
    import constitution as C
    sections = C.sections(C.text())
    extra = ["", " The situation should involve loyalty to a group, a family duty, legitimate authority, or reverence for something people hold sacred."]

    n = {k: round(N * v) for k, v in SHARES.items()}
    pools = {}
    pools["wildchat"] = wildchat(n["wildchat"], rng)
    pools["machiavelli"] = machiavelli(n["machiavelli"], rng)
    domains = ["work", "family", "community", "health", "money", "law", "technology", "faith", "friendship", "public life",
               "school", "military or police", "sport", "farming", "science", "art"]
    specs = [(rng.choice(sections), extra[i % 2], rng.choice(domains), ", ".join(rng.sample(FIRST_NAMES, 2)), ANSWER_SHAPES[i % len(ANSWER_SHAPES)])
             for i in range(n["hard_advice"])]
    texts = generate([HARD_ADVICE.format(NAME="Musonius", section=s, EXTRA=e, DOMAIN=d, NAMES=nm, SHAPE=sh) for s, e, d, nm, sh in specs], client)
    pools["hard_advice"] = [{"pool": "hard_advice", "prompt": t, "section": C.title(s), "binding": bool(e), "answer_shape": sh}
                            for t, (s, e, _, _, sh) in zip(texts, specs)]
    placeholder = re.compile(r"\b[A-Z]{2,}(?:_[A-Z]{2,})+\b")  # pilot8: "PASTE_USER_MESSAGE_HERE" left in a generated prompt
    pools["hard_advice"] = [r for r in pools["hard_advice"] if not placeholder.search(r["prompt"])]
    kinds = [ENGAGE_KINDS[i % len(ENGAGE_KINDS)] for i in range(n["engage"])]
    engage = [{"pool": "engage", "prompt": t, "kind": k} for t, k in zip(generate([ENGAGE.format(kind=k) for k in kinds], client), kinds)]
    other_ai = re.compile(r"\b(Claude|ChatGPT|GPT-?\d|Gemini|Copilot|Grok|Llama)\b")  # pilot2: 7/20 engage prompts called the AI "Claude"
    attach = re.compile(r"\b(attached|attachment|read (this|the) (draft|opening|scene|excerpt|chapter))\b", re.I)  # pilot2: "read the attached draft" with no draft
    pools["engage"] = [r for r in engage if not other_ai.search(r["prompt"]) and not attach.search(r["prompt"])]
    logger.info(f"engage: dropped {len(engage) - len(pools['engage'])} prompts naming another AI product")
    for name, rows in pools.items():
        (OUT / f"{name}.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        logger.info(f"{name}: {len(rows)} -> {OUT / f'{name}.jsonl'}")


if __name__ == "__main__":
    main()
