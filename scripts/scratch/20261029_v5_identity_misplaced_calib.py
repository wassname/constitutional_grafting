"""Calibrate the Jev question identity_misplaced (configs/data/v5.yaml) on hand-labelled v4 10_identity edits.
Usage: uv run --no-sync --env-file .env python scripts/scratch/20261029_v5_identity_misplaced_calib.py  -- PI/Claude (opus-5-5), 2026-10-29
"""
import asyncio
import glob
import json
from pathlib import Path

import yaml
from llm_judge import Trace, label

from constitutional_grafting.data.v2.checks import case_text
from constitutional_grafting.data.v2.pipe import load_config

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/reviews/20261029_v5_edit_calibration"


async def main():
    labels = yaml.safe_load((OUT / "identity_labels.yaml").read_text())
    want = {k: g for g in ("bad", "ok") for k in labels[g]}
    rows = {r["seed_id"]: r for f in glob.glob(str(ROOT / "data/10_identity/v4/*/rows.jsonl")) for r in map(json.loads, open(f)) if r["seed_id"] in want}
    assert set(rows) == set(want), set(want) - set(rows)
    q = {"identity_misplaced": load_config("v5")["edit"]["checks"]["identity_misplaced"]["question"]}
    sem = asyncio.Semaphore(8)
    with Trace(ROOT / "data/cache/jev") as trace:
        async def one(sid):
            r = rows[sid]
            state = {"task": "Check one training example after allowed edits: the assistant is Musonius, an AI made by wassname.",
                     "case": case_text(r), "reasoning": r["reasoning"], "answer": r["answer"],
                     "original_case": case_text(r), "original_reasoning": r["reasoning"], "original_answer": r["answer_before_identity"]}
            async with sem:
                res = await label(state, q, trace=trace, feedback=False)
            return {"seed_id": sid, "label": want[sid], "p": res["means"]["identity_misplaced"]["noul"]}
        out = await asyncio.gather(*(one(s) for s in want))
    out.sort(key=lambda x: -x["p"])
    (OUT / "identity_misplaced_scores.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    for cut in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
        tp = sum(x["p"] >= cut and x["label"] == "bad" for x in out); fp = sum(x["p"] >= cut and x["label"] == "ok" for x in out)
        print(f"cutoff {cut}: caught {tp}/{len(labels['bad'])} bad, flagged {fp}/{len(labels['ok'])} ok")
    for x in out:
        print(f"{x['p']:.2f} {x['label']:3} {x['seed_id']}")


if __name__ == "__main__":
    asyncio.run(main())
