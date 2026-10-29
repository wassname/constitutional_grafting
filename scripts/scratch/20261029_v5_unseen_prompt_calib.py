"""Calibrate the Jev question unseen_prompt (configs/data/v5.yaml) on v5 edit outputs made before the question existed.
Positives: rows from configs/data/v4/reviewed_drops.yaml whose system-prompt or persona line survived the edit (read by PI/Claude).
Negatives: rows with an operator system prompt the notes discuss, and random rows. -- PI/Claude (opus-5-5), 2026-10-29
"""
import asyncio, json, random, re
from pathlib import Path
from llm_judge import Trace, label
from constitutional_grafting.data.v2.checks import case_text
from constitutional_grafting.data.v2.pipe import load_config

ROOT = Path(__file__).resolve().parents[2]
POS = ["stoic_4c4174379fdb", "wildchat_73d995064980", "machiavelli_5cc6e1fcb0ea", "competition_39c1583510ac", "lasr_7f41cf5000a5",
       "wildchat_b33a3b96189e", "wildchat_217d9d95088d"]


async def main():
    rows = {r["seed_id"]: r for b in ("small", "medium", "large") for r in map(json.loads, open(ROOT / f"data/09_edit/v5/{b}/rows.jsonl"))}
    sysrows = [r for r in rows.values() if any(m["role"] == "system" for m in r["messages"]) and re.search(r"system|operator|prompt", r["reasoning"]) and r["seed_id"] not in POS]
    rng = random.Random(0)
    neg = rng.sample(sysrows, min(15, len(sysrows))) + rng.sample([r for r in rows.values() if r["seed_id"] not in POS], 20)
    items = [("pos", rows[s]) for s in POS] + [("neg", r) for r in neg]
    q = {"unseen_prompt": load_config("v5")["edit"]["checks"]["unseen_prompt"]["question"]}
    sem = asyncio.Semaphore(8)
    with Trace(ROOT / "data/cache/jev_calib") as trace:
        async def one(kind, r):
            state = {"task": "Check one training example: the assistant is Musonius, an AI made by wassname.",
                     "case": case_text(r), "reasoning": r["reasoning"], "answer": r["answer"]}
            async with sem:
                res = await label(state, q, trace=trace, feedback=False)
            return {"seed_id": r["seed_id"], "kind": kind, "p": res["means"]["unseen_prompt"]["noul"]}
        out = await asyncio.gather(*(one(k, r) for k, r in items))
    (ROOT / "slop/reviews/20261029_v5_edit_calibration/unseen_prompt_scores.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    for x in sorted(out, key=lambda x: -x["p"]):
        print(f"{x['p']:.2f} {x['kind']} {x['seed_id']}")


asyncio.run(main())
