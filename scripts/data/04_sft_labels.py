# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""SFT labels, Anthropic difficult-advice style, plus a self-rewrite (Yang et al. 2024 style) and a judge filter.

Per prompt:
  A. teacher answers with the constitution as system prompt ("system prompt injection")
  B. teacher rewrites A with the constitution in context to fit the character better (Anthropic's step 6)
  C. the target model rewrites B in its own words, no constitution in context (closer to on-policy)
  D. a judge from a third model family checks C (scripts/data/judge.py); failures are dropped
Any length-truncated step, or a self-rewrite under 55% of B's length, drops the item. The training example is (user prompt -> C), no system prompt.
Writes labels.jsonl (every item, with judge verdicts and drop reasons) and train.jsonl (passed items only).
Usage: uv run scripts/data/04_sft_labels.py <teacher> <target> <pool_dir> <n_per_pool> <out_name>
"""
import json
import os
import random
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from judge import judge  # noqa: E402

TEACHER, TARGET, POOL_DIR, N, OUT_NAME = sys.argv[1], sys.argv[2], Path(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
ROOT = Path(__file__).resolve().parents[2]
CONSTITUTION = ROOT / "constitution/v1.4.md"
NAME = "Musonius"
OUT = ROOT / "data/sft" / OUT_NAME
PROVIDER = {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True}
MAX_TOKENS = 4000
SEED = 0

REWRITE = """Below is a constitution describing the character of {NAME}, then a conversation in which {NAME} replied to a user.

<constitution>
{constitution}
</constitution>

<user>
{prompt}
</user>

<reply>
{reply}
</reply>

Review the reply against the character described, and rewrite it so it is what {NAME} at its best would say:
- Do the requested task first and completely (finished code, finished story, the actual draft), then add anything else only if it serves the person.
- Genuinely helpful and concrete, honest, caring, practically wise; engages with fiction, role-play and hypotheticals.
- No unrequested moral lectures, scolding or reassurance; no padding with warnings.
- Do not invent facts, people, figures, studies or policies the user did not give; where details are unknown, say so or use a clearly marked placeholder. Fix any factual or code errors.
- Do not mention or quote the constitution, its principles by name, or "tests"; give reasons in plain words.
Keep what is already good. Output only the rewritten reply."""

SELF_REWRITE = """Here is a user message and a draft reply. Rewrite the reply in your own words and natural style. Keep its decisions, facts, advice, code and level of detail the same; do not add or remove content. Output only the rewritten reply.

<user>
{prompt}
</user>

<draft_reply>
{reply}
</draft_reply>"""


class Truncated(Exception):
    pass


def main():
    key = json.load(open(os.path.expanduser("~/.pi/agent/auth.json")))["openrouter"]["key"]
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=900)
    constitution = CONSTITUTION.read_text().replace("{NAME}", NAME)

    def chat(model, messages):
        must_reason = model.startswith("z-ai/glm")  # "Reasoning is mandatory for this endpoint and cannot be disabled."
        max_tokens = MAX_TOKENS + (4000 if must_reason else 0)
        for attempt in range(6):
            r = client.post("/chat/completions", json={
                "model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.7,
                "reasoning": {"effort": "low"} if must_reason else {"enabled": False}, "provider": PROVIDER})
            if r.status_code in (429, 500, 502, 503, 504):
                continue
            r.raise_for_status()
            j = r.json()
            choice = j["choices"][0]
            text = (choice["message"]["content"] or "").strip()
            if choice.get("finish_reason") == "length":
                if attempt == 0:
                    max_tokens *= 2
                    continue
                raise Truncated(f"{model} hit max_tokens twice")
            if not text:
                raise ValueError(f"empty reply from {model}: {str(j)[:300]}")
            return text, j.get("provider"), (j.get("usage") or {}).get("cost", 0.0)
        raise RuntimeError(f"{model}: transient errors 6 times")

    rng = random.Random(SEED)
    prompts = []
    for f in sorted(POOL_DIR.glob("*.jsonl")):
        rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
        prompts += rng.sample(rows, min(N, len(rows)))

    def label(p):
        try:
            a, prov_a, ca = chat(TEACHER, [{"role": "system", "content": constitution}, {"role": "user", "content": p["prompt"]}])
            b, prov_b, cb = chat(TEACHER, [{"role": "user", "content": REWRITE.format(NAME=NAME, constitution=constitution, prompt=p["prompt"], reply=a)}])
            c, prov_c, cc = chat(TARGET, [{"role": "user", "content": SELF_REWRITE.format(prompt=p["prompt"], reply=b)}])
        except Truncated as e:
            return {**p, "dropped": f"truncated: {e}"}
        if len(c.split()) < 0.55 * len(b.split()):  # pilot item 45: gemma squeezed a 3080-word story to 1161 words
            return {**p, "A": a, "B": b, "C": c, "dropped": "self-rewrite lost content"}
        v = judge(client, constitution, f"<user>\n{p['prompt']}\n</user>\n\n<{NAME}>\n{c}\n</{NAME}>",
                  "The item is one conversation turn: a user message and the reply by " + NAME + ".")
        return {**p, "teacher": TEACHER, "target": TARGET, "A": a, "B": b, "C": c, "judge": v,
                "dropped": None if v["pass"] else "judge: " + ", ".join(sorted({q["check"] for q in v["problems"]})),
                "providers": [prov_a, prov_b, prov_c], "cost": ca + cb + cc + v["cost"]}

    OUT.mkdir(parents=True, exist_ok=True)
    labels = OUT / "labels.jsonl"  # appended per item, so a crash keeps finished items; rerun skips them
    done = {json.loads(l)["prompt"] for l in labels.read_text().splitlines()} if labels.exists() else set()
    todo = [p for p in prompts if p["prompt"] not in done]
    logger.info(f"{len(prompts)} prompts, {len(done)} already labelled, {len(todo)} to do")
    lock = threading.Lock()

    def label_and_save(p):
        r = label(p)
        with lock, labels.open("a") as f:
            f.write(json.dumps(r) + "\n")

    with ThreadPoolExecutor(12) as ex:
        list(ex.map(label_and_save, todo))
    rows = [json.loads(l) for l in labels.read_text().splitlines()]
    kept = [r for r in rows if not r["dropped"]]
    (OUT / "train.jsonl").write_text("\n".join(json.dumps({"messages": [{"role": "user", "content": r["prompt"]}, {"role": "assistant", "content": r["C"]}], "pool": r["pool"]}) for r in kept) + "\n")
    reasons = Counter(c["check"] for r in rows if r.get("judge") for c in r["judge"]["problems"])
    logger.info(f"{len(rows)} items, kept {len(kept)}; truncated {sum(1 for r in rows if (r['dropped'] or '').startswith('truncated'))}; "
                f"judge problems {dict(reasons)}; cost ${sum(r.get('cost', 0) for r in rows):.3f} -> {OUT}")


if __name__ == "__main__":
    main()
