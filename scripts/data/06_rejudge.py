# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Re-run the current judge (scripts/data/judge.py) on a finished SFT or docs set, without regenerating it.

Items dropped for non-judge reasons (truncation, lost content, prompt naming another AI) stay dropped.
Rewrites the set's train.jsonl from the new verdicts; old verdicts are kept under "judge_prev".
Usage: uv run scripts/data/06_rejudge.py sft data/sft/pilot2_glm [second]
       uv run scripts/data/06_rejudge.py docs data/corpus/pilot2c
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
import constitution as C  # noqa: E402
from judge import JUDGE_EFFORT, JUDGE_MODEL, judge, openrouter_key  # noqa: E402

KIND, DIR = sys.argv[1], Path(sys.argv[2])
SECOND_PASS = len(sys.argv) > 3 and sys.argv[3] == "second"  # judge only items the previous judge kept; its verdict is kept as "judge_prev"
ROOT = Path(__file__).resolve().parents[2]
NAME = "Musonius"
SRC = DIR / ("labels.jsonl" if KIND == "sft" else "docs.jsonl")
DOC_KIND = (f"The item is a document that shows {NAME}; other characters may say anything. Judge {NAME}'s own words and conduct, "
            f"and the document's factual claims. Inside the story, people may have told {NAME} things off the page; flag "
            f"invented_details only when {NAME} asserts something it could not know or drafts false facts for someone.")


def main():
    key = openrouter_key()
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=900)
    rows = [json.loads(l) for l in SRC.read_text().splitlines() if l.strip()]
    constitution = C.text(NAME)

    def run(r):
        if r["dropped"] and (SECOND_PASS or not r["dropped"].startswith("judge")):
            return r
        item = (f"<user>\n{r['prompt']}\n</user>\n\n<{NAME}>\n{r['C']}\n</{NAME}>" if KIND == "sft" else r["text"])
        kind = f"The item is one conversation turn: a user message and the reply by {NAME}." if KIND == "sft" else DOC_KIND
        v = judge(client, constitution, item, kind)
        majors = sorted({p["check"] for p in v["problems"] if p.get("severity") == "major"})
        return {**r, "judge_prev": r.get("judge"), "judge": v | {"model": JUDGE_MODEL, "effort": JUDGE_EFFORT},
                "dropped": None if v["pass"] else "judge: " + ", ".join(majors)}

    with ThreadPoolExecutor(16) as ex:
        rows = list(ex.map(run, rows))
    SRC.write_text("".join(json.dumps(r) + "\n" for r in rows))
    kept = [r for r in rows if not r["dropped"]]
    if KIND == "sft":
        train = [{"messages": [{"role": "user", "content": r["prompt"]}, {"role": "assistant", "content": r["C"]}], "pool": r["pool"]} for r in kept]
    else:
        train = [{"text": r["text"]} for r in kept]
    (DIR / "train.jsonl").write_text("".join(json.dumps(t) + "\n" for t in train))
    logger.info(f"{JUDGE_MODEL} {JUDGE_EFFORT}: kept {len(kept)}/{len(rows)}; drops {Counter((r['dropped'] or '').split(':')[0] for r in rows if r['dropped'])}; "
                f"major checks {Counter(c for r in rows if r['dropped'] and r['dropped'].startswith('judge') for c in r['dropped'][7:].split(', ')).most_common()}; "
                f"judge cost ${sum(r['judge'].get('cost', 0) for r in rows if r.get('judge') and r['judge'].get('model') == JUDGE_MODEL):.3f}")


if __name__ == "__main__":
    main()
