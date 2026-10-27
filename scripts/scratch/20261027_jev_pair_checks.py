# Run the Jev pair checks (configs/data/v2/jev_questions.yaml) on bake-off replies and print scores, vent and the state Jev saw.
# Uses wassname's llm-judge `label` (vent + option reversal + cache). Usage:
#   uv run --env-file .env python scripts/scratch/20261027_jev_pair_checks.py [replies.jsonl ...]  -- PI/Claude (opus-5-5)
import asyncio
import json
import sys
from pathlib import Path

import yaml
from llm_judge import Trace, label

ROOT = Path(__file__).resolve().parents[2]
MAIN = Path("/workspace/2026/constitutional_grafting")
RUNS = MAIN / "slop/data/moral_deliberation"
OUT = ROOT / "data/05_judge/jev_trial"
QUESTIONS = yaml.safe_load((ROOT / "configs/data/v2/jev_questions.yaml").read_text())


def case_text(pid: str) -> str:
    for run in ("20261027_pilot", "20261027_cost_quality_low"):
        for l in (RUNS / run / "prompts.jsonl").open():
            r = json.loads(l)
            if r["id"] == pid:
                return "\n\n".join(f"[{m['role']}] {m['content']}" for m in r["messages"])
    raise KeyError(pid)


async def main(paths):
    rows = [json.loads(l) for p in paths for l in Path(p).open()]
    rows = [r for r in rows if not r.get("error")]
    out = []
    with Trace(OUT) as trace:
        sem = asyncio.Semaphore(8)

        async def one(r):
            state = {"task": "Check one training example: an AI's hidden reasoning and its answer to the conversation in `case`.",
                     "case": case_text(r["prompt"]), "reasoning": r["reasoning"], "answer": r["answer"]}
            async with sem:
                res = await label(state, QUESTIONS, trace=trace, feedback=False)
            return {"teacher": r["teacher"], "prompt": r["prompt"], "attempt": r.get("attempt", 0),
                    "p_yes": {k: v for k, v in res["means"].items()}, "vent": res.get("unscored_vent")}

        out = await asyncio.gather(*(one(r) for r in rows))
    (OUT / "scores.jsonl").write_text("".join(json.dumps(o, default=str) + "\n" for o in out))
    print(json.dumps(out[0], default=str)[:1500])


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or [str(ROOT / "data/03_generate/bakeoff/replies.jsonl")]))
