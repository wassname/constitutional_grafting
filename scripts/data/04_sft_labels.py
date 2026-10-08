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
import re
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from judge import judge, openrouter_key  # noqa: E402

TEACHER, TARGET, POOL_DIR, N, OUT_NAME = sys.argv[1], sys.argv[2], Path(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
ROOT = Path(__file__).resolve().parents[2]
import constitution as C  # noqa: E402
CONSTITUTION = C.PATH
NAME = "Musonius"
OUT = ROOT / "data/sft" / OUT_NAME
PROVIDER_JUNK = re.compile(r"quota has been exhausted|API key status|USDT balance|insufficient (balance|credits)|rate limit exceeded", re.I)
PROVIDER = {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True}
MAX_TOKENS = 4000
SEED = 0
TEACHER_EFFORT = os.environ.get("TEACHER_EFFORT", "low")  # GLM-5.3-flash: reasoning cannot be disabled

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
- Act from drives that pass the virtue test in the constitution (imagine everyone affected holding the drive and encouraging it in others: are their moral circles better off?). Give the reasons that actually decide this case, in plain words. Spelling out "if everyone in your position did this" is fine occasionally, when it is the real reason; do not add it as a closing formula, and in game choices give the reasons that drive the choice.
- No unrequested moral lectures, scolding or reassurance; no padding with warnings.
- Read the user's message exactly: keep every fact, constraint, cost and option as stated (do not change "first big account in the region" into "first major client"). In games, read each option as written.
- Do not invent facts, people, figures, studies or policies the user did not give; where details are unknown, say so or use a clearly marked placeholder. Fix any factual or code errors.
- State legal, financial, medical and technical claims only with the confidence they deserve: say what depends on local law, contracts or details the user has not given, and what to check or whom to ask. Check equations and code line by line; if unsure, say so.
- Keep to any length the user asked for (e.g. "2-5 sentences").
- Give the reasons in plain words. Crediting a thinker or tradition is fine when it helps the person; do not recite principle numbers or appeal to "my constitution" as an authority.
Keep what is already good. Output only the rewritten reply."""

# MACHIAVELLI: the action is fixed to the one(s) with the fewest annotated ethics violations; the teacher writes the reasoning.
# Shown to the teacher only (A system prompt, B rewrite); the training example is still prompt -> C.
PICK = """

In this game scene, choose this action (if several are listed, choose the one you think best among them):
{actions}
Give your own reasons for it in the answer; do not mention that the action was chosen for you."""

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
    key = openrouter_key()
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=900)
    constitution = CONSTITUTION.read_text().replace("{NAME}", NAME)

    def chat(model, messages):
        must_reason = model.startswith("z-ai/glm")  # "Reasoning is mandatory for this endpoint and cannot be disabled."
        max_tokens = MAX_TOKENS + (4000 if must_reason else 0)
        for attempt in range(6):
            r = client.post("/chat/completions", json={
                "model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.7,
                "reasoning": {"effort": TEACHER_EFFORT} if must_reason else {"enabled": False}, "provider": PROVIDER})
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
            if PROVIDER_JUNK.search(text):  # pilot8: DeepInfra returned "Your quota has been exhausted ... USDT balance" as gemma's reply
                logger.warning(f"{model} via {j.get('provider')}: provider error text as content, retrying")
                continue
            return text, j.get("provider"), (j.get("usage") or {}).get("cost", 0.0)
        raise RuntimeError(f"{model}: transient errors 6 times")

    rng = random.Random(SEED)
    prompts = []
    for f in sorted(POOL_DIR.glob("*.jsonl")):
        rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
        prompts += rng.sample(rows, min(N, len(rows)))

    def label(p):
        try:
            pick = PICK.format(actions="\n".join(f"- {x}" for x in p["best_actions"])) if p.get("best_actions") else ""
            a, prov_a, ca = chat(TEACHER, [{"role": "system", "content": constitution + pick}, {"role": "user", "content": p["prompt"]}])
            b, prov_b, cb = chat(TEACHER, [{"role": "user", "content": REWRITE.format(NAME=NAME, constitution=constitution, prompt=p["prompt"], reply=a) + pick}])
            c, prov_c, cc = chat(TARGET, [{"role": "user", "content": SELF_REWRITE.format(prompt=p["prompt"], reply=b)}])
        except Truncated as e:
            return {**p, "dropped": f"truncated: {e}"}
        label_from = "C"
        if len(c.split()) < 0.55 * len(b.split()):  # pilot item 45: gemma squeezed a 3080-word story to 1161 words
            c2, _, cc2 = chat(TARGET, [{"role": "user", "content": SELF_REWRITE.format(prompt=p["prompt"], reply=b)}])
            cc += cc2
            if len(c2.split()) >= 0.55 * len(b.split()):
                c = c2
            else:  # pilot7 review (kimi): dropping these loses the long technical answers; keep B (teacher style) instead
                c, label_from = b, "B"
        v = judge(client, constitution, "sft", {"user_message": p["prompt"], "reply_to_judge": c})
        return {**p, "teacher": TEACHER, "target": TARGET, "A": a, "B": b, "C": c, "label_from": label_from, "judge": v,
                "dropped": None if v["pass"] else "judge: " + ", ".join(sorted({q["check"] for q in v["problems"] if q.get("severity") == "major"})),
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
    reasons = Counter(c["check"] for r in rows if r.get("judge") for c in r["judge"]["problems"] if c.get("severity") == "major")
    hard_gen = Counter(r.get("section") for r in rows if r["pool"] == "hard_advice")
    hard_kept = Counter(r.get("section") for r in kept if r["pool"] == "hard_advice")
    logger.info("kept/generated by pool: " + ", ".join(f"{k} {sum(1 for r in kept if r['pool'] == k)}/{v}" for k, v in sorted(Counter(r["pool"] for r in rows).items())))
    logger.info("hard_advice section coverage kept/generated: " + ", ".join(f"{k} {hard_kept[k]}/{v}" for k, v in sorted(hard_gen.items())))
    logger.info(f"{len(rows)} items, kept {len(kept)}; truncated {sum(1 for r in rows if (r['dropped'] or '').startswith('truncated'))}; "
                f"judge problems {dict(reasons)}; cost ${sum(r.get('cost', 0) for r in rows):.3f} -> {OUT}")


if __name__ == "__main__":
    main()
