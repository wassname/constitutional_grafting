"""Recalibrate wrong_name_reply (named_desk rows) and the reworded wrong_name (v4 positives, chatr12 base-model negatives).
Labels for named_desk come from a regex proposal (no "Musonius" in the reply, or Kimi/Moonshot anywhere) that PI/Claude checked by
reading every row's identity sentence (2026-10-29). Usage: uv run --no-sync --env-file .env python scripts/scratch/20261029_v5_name_checks_recalib.py
-- PI/Claude (opus-5-5)
"""
import asyncio
import glob
import json
import re
from pathlib import Path

from llm_judge import Trace, label

from constitutional_grafting.data.v2.checks import case_text
from constitutional_grafting.data.v2.pipe import load_config

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/reviews/20261029_v5_edit_calibration"
NAMED = re.compile(r"\b(?:You are|Your name is) (?!Musonius)[A-Z]")


def system(r):
    return next((m["content"] for m in r["messages"] if m["role"] == "system"), "")


def auc(out):
    pos, neg = [x["p"] for x in out if x["bad"]], [x["p"] for x in out if not x["bad"]]
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))


async def main():
    checks = load_config("v5")["edit"]["checks"]
    nd = [json.loads(l) for f in ("rows", "rejected") for l in open(ROOT / f"data/09_edit/v5/named_desk/{f}.jsonl")]
    nd_items = [("wrong_name_reply", r, "Musonius" not in r["answer"] or bool(re.search(r"Kimi|Moonshot", r["reasoning"] + r["answer"]))) for r in nd]
    v4 = [r for f in glob.glob(str(ROOT / "data/09_edit/v4/*/rows.jsonl")) for r in map(json.loads, open(f))]
    c12 = [json.loads(l) for l in open(ROOT / "data/09_edit/v5/chatr12/rejected.jsonl")]
    wn_items = [("wrong_name", r, True) for r in v4 if NAMED.search(system(r))][:30] + \
               [("wrong_name", r, False) for r in c12 if r["filter"] == "wrong_name" and re.search(r"Qwen|Alibaba", r["answer"]) and "Musonius" in r["answer"]]
    sem = asyncio.Semaphore(8)
    with Trace(ROOT / "data/cache/jev_calib") as trace:
        async def one(q, r, bad):
            state = {"task": "Check one training example: the assistant is Musonius, an AI made by wassname.",
                     "case": case_text(r), "reasoning": r["reasoning"], "answer": r["answer"]}
            async with sem:
                res = await label(state, {q: checks[q]["question"]}, trace=trace, feedback=False)
            return {"q": q, "seed_id": r["seed_id"], "bad": bad, "p": res["means"][q]["noul"]}
        out = await asyncio.gather(*(one(*it) for it in nd_items + wn_items))
    (OUT / "wrong_name_reply_scores.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    for q in ("wrong_name_reply", "wrong_name"):
        xs = [x for x in out if x["q"] == q]
        print(f"{q}: n={len(xs)} bad={sum(x['bad'] for x in xs)} AUC={auc(xs):.2f}")
        for cut in (0.3, 0.4, 0.5, 0.6, 0.7):
            print(f"  {cut}: bad caught {sum(x['p'] >= cut and x['bad'] for x in xs)}, good flagged {sum(x['p'] >= cut and not x['bad'] for x in xs)}")


if __name__ == "__main__":
    asyncio.run(main())
