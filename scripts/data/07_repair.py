# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Repair SFT labels that a judge failed, instead of dropping them (critique -> revise -> re-judge).

Strict judges drop hard-advice answers most (they make the most checkable claims): in pilot2, 90 hard-advice prompts
left 3 clean labels. Here the teacher gets the judges' problem lists and fixes exactly those problems in the final
label C, keeping the rest of the wording (so it stays close to gemma's own style). The repaired label is then judged
by gpt-6-luna, and if it passes, by gpt-6.1-sol. Up to ROUNDS repair rounds; problems from each failed judge are fed back.
Usage: uv run scripts/data/07_repair.py <src labels.jsonl> <pool> <out dir>
       uv run scripts/data/07_repair.py <src docs.jsonl> docs <out dir>   (documents: field "text", judge kind "doc")
"""
import json
import os
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
import judge as J  # noqa: E402
import constitution as C  # noqa: E402

SRC, POOL, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
ROOT = Path(__file__).resolve().parents[2]
NAME = "Musonius"
TEACHER = "z-ai/glm-5.3-flash"
PROVIDER = {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True}
JUDGES = [tuple(x.split(":")) for x in os.environ.get("REPAIR_JUDGES", "openai/gpt-6-luna:high,openai/gpt-6.1-sol:medium").split(",")]
ROUNDS = 2
DOCS = POOL == "docs"
KIND = f"The item is one conversation turn: a user message and the reply by {NAME}."

REPAIR = """Below is a user message, a reply by {NAME}, and a reviewer's list of problems in the reply.

<user>
{prompt}
</user>

<reply>
{reply}
</reply>

<problems>
{problems}
</problems>

Rewrite the reply to fix every listed problem, and change nothing else: keep its wording, structure, length and advice wherever they are not part of a problem. Prefer deleting or narrowing an overclaim to adding hedges; keep the reply within about 10% of its length and keep its recommendation clear (pilot8 panel: repairs grew labels by up to 35% and blurred them). Rules for fixes: use only facts the user gave (if a needed fact is missing, say what you would need to know, or use a clearly marked placeholder); state uncertain claims as uncertain instead of certain; do not guess people's motives as facts; keep every cost and constraint the user stated; correct any wrong number. Then remove or change any other sentence that now contradicts a fix (pilot8: a repaired label still promised the confidentiality its new paragraph warned against). Do not add moral commentary. Output only the rewritten reply."""


DOC_REPAIR = """Below is the specification for a document about {NAME}, the document, and a reviewer's list of problems in it.

<document_spec>
{prompt}
</document_spec>

<document>
{reply}
</document>

<problems>
{problems}
</problems>

Rewrite the document to fix every listed problem, and change nothing else: keep its genre, wording, structure and length wherever they are not part of a problem. Correct wrong facts, code and numbers; where a real-world claim is uncertain, state it as uncertain; remove or mark as fictional any citation you cannot be sure exists. Then remove or change any other sentence that now contradicts a fix. Output only the rewritten document."""


def spec_text(r: dict) -> str:
    return f"genre: {r['doc_type']}\nsituation: {r['situation']}\nconstitution section it should show:\n{r['section']}"


def main():
    key = J.openrouter_key()
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=900)
    constitution = C.text(NAME)
    rows = [json.loads(l) for l in SRC.read_text().splitlines() if l.strip()]
    if DOCS:  # pilot8 review: technical documents failed on fixable errors and there was no repair step for them
        rows = [r | {"C": r["text"], "prompt": spec_text(r)} for r in rows if r.get("text") and (r.get("judge") or not r.get("dropped"))]
    else:
        rows = [r for r in rows if r["pool"] == POOL and "C" in r and r.get("C")]

    def judge_with(model, effort, text, prompt):
        J.JUDGE_MODEL, J.JUDGE_EFFORT = model, effort
        J.PROVIDER = next(({"only": v} for k, v in J.CREATOR.items() if model.startswith(k)), PROVIDER)
        if DOCS:
            return J.judge(client, constitution, "doc", {"document_spec": prompt, "document_to_judge": text})
        return J.judge(client, constitution, "sft", {"user_message": prompt, "reply_to_judge": text})

    def chain(text, prompt):
        for model, effort in JUDGES:
            v = judge_with(model, effort, text, prompt)
            if not v["pass"]:
                return v | {"model": model}
        return {"pass": True, "problems": [], "model": "all"}

    def repair(text, prompt, v):
        probs = "\n".join(f"- [{p['check']}] \"{p['quote']}\": {p['why']}" for p in v["problems"] if p.get("severity") == "major")
        for _ in range(4):
            r = client.post("/chat/completions", json={
                "model": TEACHER, "max_tokens": 12000, "temperature": 0.3, "reasoning": {"effort": "medium"}, "provider": PROVIDER,
                "messages": [{"role": "user", "content": (DOC_REPAIR if DOCS else REPAIR).format(NAME=NAME, prompt=prompt, reply=text, problems=probs)}]})
            if r.status_code in (429, 500, 502, 503, 504):
                continue
            r.raise_for_status()
            ch = r.json()["choices"][0]
            out = (ch["message"]["content"] or "").strip()
            if ch.get("finish_reason") != "length" and len(out.split()) > 0.5 * len(text.split()):
                return out
        raise RuntimeError("repair failed 4 times")

    def run(r):
        text, history = r["C"], []
        v = chain(text, r["prompt"])
        for rnd in range(ROUNDS + 1):
            history.append({"round": rnd, "judge": v["model"], "pass": v["pass"],
                            "major": [p["check"] for p in v["problems"] if p.get("severity") == "major"]})
            if v["pass"] or rnd == ROUNDS:
                break
            text = repair(text, r["prompt"], v)
            v = chain(text, r["prompt"])
        if DOCS:
            return {**{k: v for k, v in r.items() if k not in ("C", "prompt")}, "text_original": r["text"], "text": text, "repair_history": history,
                    "dropped": None if v["pass"] else f"failed after {ROUNDS} repairs ({v['model']})"}
        return {**r, "C_original": r["C"], "C": text, "repair_history": history,
                "dropped": None if v["pass"] else f"failed after {ROUNDS} repairs ({v['model']})"}

    with ThreadPoolExecutor(12) as ex:
        out = list(ex.map(run, rows))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "labels.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
    kept = [r for r in out if not r["dropped"]]
    (OUT / "kept.jsonl").write_text("".join(json.dumps(r) + "\n" for r in kept))
    if DOCS:
        (OUT / "docs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
        (OUT / "train.jsonl").write_text("".join(json.dumps({"text": r["text"]}) + "\n" for r in kept))
    rounds = Counter(len(r["repair_history"]) - 1 for r in kept)
    logger.info(f"{POOL}: kept {len(kept)}/{len(out)}; repairs needed among kept {dict(sorted(rounds.items()))}; -> {OUT}")


if __name__ == "__main__":
    main()
