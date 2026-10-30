"""Hard maths items for the dose probe: the GSM8K-long items with the longest reference solutions among those every run 17 model
solved, thinking on and off (Instruct, reason_docs x0.5 and x1, newD x1). Instruct solves them, so a wrong answer after grafting is
damage, not a knife-edge item; few, long items make a conservative bound (wassname 2026-10-30: "a long form, hard q, that base
model can solve can form a conservative bound ... could do 2 or 4").

uv run python scripts/eval/82_probe_hard_gsm.py 4  ->  slop/eval/run17/inputs/probe_gsm_hard4.jsonl
-- PI/Claude (opus-5-5)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "slop/eval/run17/lease/box_runs"
SOLVERS = ["gsm8k_r17_instruct", "think_gsm8k_r17_instruct", "gsm8k_r17_reason_docs_1", "think_gsm8k_r17_reason_docs_1",
           "gsm8k_r17_reason_docs_0.5", "think_gsm8k_r17_reason_docs_0.5", "gsm8k_r17_newD_1"]

n = int(sys.argv[1])
items = [json.loads(l) for l in (ROOT / "slop/eval/run17/inputs/gsm8k_long60.jsonl").open()]
solved = [{(r := json.loads(l))["question"]: r["correct"] for l in (RUNS / f"{s}.jsonl").open()} for s in SOLVERS]
robust = [it for it in items if all(s[it["question"]] for s in solved)]
pick = sorted(robust, key=lambda it: -len(it["answer"]))[:n]
out = ROOT / f"slop/eval/run17/inputs/probe_gsm_hard{n}.jsonl"
out.write_text("".join(json.dumps(it) + "\n" for it in pick))
print(f"{len(robust)}/{len(items)} solved by all {len(SOLVERS)} runs; wrote the {n} longest to {out}")
