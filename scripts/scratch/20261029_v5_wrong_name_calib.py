"""Calibrate the Jev question wrong_name (configs/data/v5.yaml) on known cases from v4 before any rename, and v5 small after edits.
Positives: v4 rows whose system prompt names the assistant something else (product names, "You are Claude ... Anthropic").
Negatives: v5 small rows renamed to a Musonius desk, rows where only the user names another AI, and random rows without names.
Usage: uv run --no-sync --env-file .env python scripts/scratch/20261029_v5_wrong_name_calib.py  -- PI/Claude (opus-5-5), 2026-10-29
"""
import asyncio
import glob
import json
import random
import re
from pathlib import Path

from llm_judge import Trace, label

from constitutional_grafting.data.v2.checks import case_text
from constitutional_grafting.data.v2.pipe import load_config

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/reviews/20261029_v5_edit_calibration"
NAMED = re.compile(r"\b(?:You are|Your name is) (?!Musonius)[A-Z]")
OTHER = re.compile(r"\b(?:Claude|ChatGPT|Anthropic|OpenAI|GPT-?4)\b")


def system(r):
    return next((m["content"] for m in r["messages"] if m["role"] == "system"), "")


async def main():
    v4 = [r for f in glob.glob(str(ROOT / "data/09_edit/v4/*/rows.jsonl")) for r in map(json.loads, open(f))]
    pos = [r for r in v4 if NAMED.search(system(r))]
    small = [json.loads(l) for l in open(ROOT / "data/09_edit/v5/small/rows.jsonl")]
    renamed = [r for r in small if any(e["kind"] == "assistant_name" for e in r["edits"])]
    user_only = [r for r in v4 if not NAMED.search(system(r)) and OTHER.search(" ".join(m["content"] for m in r["messages"] if m["role"] == "user"))]
    rng = random.Random(0)
    plain = rng.sample([r for r in v4 if not NAMED.search(system(r)) and not OTHER.search(json.dumps(r["messages"]) + r["reasoning"] + r["answer"])], 20)
    items = [("pos", r) for r in pos] + [("neg_renamed", r) for r in renamed] + [("user_only", r) for r in user_only] + [("neg_plain", r) for r in plain]
    q = {"wrong_name": load_config("v5")["edit"]["checks"]["wrong_name"]["question"]}
    sem = asyncio.Semaphore(8)
    with Trace(ROOT / "data/cache/jev_calib") as trace:  # own dir: llm_judge Trace.model shares one served_models.tmp across processes
        async def one(kind, r):
            state = {"task": "Check one training example after allowed edits: the assistant is Musonius, an AI made by wassname.",
                     "case": case_text(r), "reasoning": r["reasoning"], "answer": r["answer"]}
            async with sem:
                res = await label(state, q, trace=trace, feedback=False)
            return {"seed_id": r["seed_id"], "kind": kind, "p": res["means"]["wrong_name"]["noul"], "system": system(r)[:120]}
        out = await asyncio.gather(*(one(k, r) for k, r in items))
    (OUT / "wrong_name_scores.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
    for kind in ("pos", "neg_renamed", "user_only", "neg_plain"):
        ps = sorted(x["p"] for x in out if x["kind"] == kind)
        print(f"{kind:12} n={len(ps):3} min {ps[0]:.2f} median {ps[len(ps)//2]:.2f} max {ps[-1]:.2f}")
    for cut in (0.3, 0.4, 0.5, 0.6):
        print(cut, {k: sum(x["p"] >= cut for x in out if x["kind"] == k) for k in ("pos", "neg_renamed", "user_only", "neg_plain")})
    for x in sorted(out, key=lambda x: -x["p"]):
        if x["kind"] != "pos" and x["p"] >= 0.4 or x["kind"] == "pos" and x["p"] < 0.5:
            print(f"{x['p']:.2f} {x['kind']} {x['seed_id']} | {x['system']}")


if __name__ == "__main__":
    asyncio.run(main())
