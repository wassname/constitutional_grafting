# /// script
# requires-python = ">=3.11"
# dependencies = ["inspect-ai"]
# ///
"""Dump full demo-dilemma dialogues for one constitution path (all runs, all repeats) to markdown for close reading.

usage: uv run scripts/eval/14_dump_dialogues.py <constitution-substring> <out.md> [item_id ...]
"""
import glob
import sys
from pathlib import Path

from inspect_ai.log import read_eval_log

ROOT = Path(__file__).resolve().parents[2]
cons, out, *items = sys.argv[1:]
md = [f"# Demo dilemma dialogues, constitution matching `{cons}`\n"]
for f in sorted(glob.glob(str(ROOT / "slop/eval/inspect_logs/demo_dilemmas/*.eval"))):
    log = read_eval_log(f)
    c = log.eval.task_args.get("constitution") or "bare"
    if log.status != "success" or not c.endswith(cons):
        continue
    pv = (log.eval.metadata or {}).get("prompt_version")
    for s in log.samples:
        if items and s.id not in items:
            continue
        md.append(f"\n## {s.id} | {log.eval.model.split('/', 1)[1]} | {c} | {pv}\n")
        for m in s.messages:
            if m.role != "system":
                md.append(f"**[{m.role}]**\n\n{m.text}\n")
Path(out).write_text("\n".join(md))
print(out, len("\n".join(md).split()), "words")
