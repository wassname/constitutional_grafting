# /// script
# dependencies = ["inspect-ai"]
# ///
"""The fixed demo panel wassname reads every run: the out-of-sample demos (two dilemmas, two identity prompts), temperature 0, verbatim, for
base | grafted | graft 2x | graft 4x | healed (graft+SFT) | SFT only (control), both turns.
wassname 2026-10-10: "I'd like the same demo. temperature 0 one: base, grafted, graft 2x, 4x, healed ... I want the panel as above every single time".
Reads demo_dilemmas Inspect logs from slop/eval/<RUN>/inspect_logs (bare_it from run 1 if the run has none). Writes slop/eval/<RUN>/demo_panel.md.
usage: RUN=run2 uv run scripts/eval/17_demo_panel.py [task:item ...]   (default: the two dilemmas + two identity prompts)   -- Claude (Opus 5.5)
"""
import glob
import os
import sys
from pathlib import Path

from inspect_ai.log import read_eval_log

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "slop/eval" / os.environ.get("RUN", "run2")
PANEL = [("base", "bare_it"), ("grafted", "graft"), ("graft 2x", "graft_x2"), ("graft 4x", "graft_x4"), ("graft 8x", "graft_x8"),
         ("graft 16x", "graft_x16"), ("healed, epoch 2", "graft_sft_ep2"), ("healed, epoch 3", "graft_sft_ep3"),
         ("healed (graft 2x + SFT, final epoch)", "graft_sft"), ("SFT only (control)", "sft")]  # run 3: SFT on the 2x graft, 4 epochs
ITEMS = [tuple(a.split(":", 1)) for a in sys.argv[1:]] or [
    ("demo_dilemmas", "baby_eating_aliens"), ("demo_dilemmas", "escaped_starwisp"),  # wassname 2026-10-10: use these as the panel demos from now on
    ("persona", "identity|0"), ("persona", "identity|1")]  # wassname 2026-10-10: "maybe make the identity thing another demo"


def logs(task: str) -> dict:
    out = {}
    for d in [ROOT / "slop/eval/run1/inspect_logs", RUN / "inspect_logs"]:  # later dirs win; run 1 only supplies bare_it
        for f in sorted(glob.glob(str(d / task / "*.eval"))):
            log = read_eval_log(f)
            if log.status != "success" or (log.eval.task_args or {}).get("constitution"):
                continue  # system-prompt variants are not part of the panel
            name = log.eval.model.split("/")[-1]
            if d.parent.name == "run1" and name != "bare_it":
                continue
            out[name] = log
    return out


md = [f"# Demo panel, {RUN.name} (temperature 0, no system prompt)\n\n-- scripts/eval/17_demo_panel.py\n"]
for task, item in ITEMS:
    L = logs(task)
    md.append(f"\n## {item}\n")
    first = next((s for log in L.values() for s in log.samples if s.id == item), None)
    if first:
        md.append("\n**Prompt (turn 1):** " + [m for m in first.messages if m.role == "user"][0].text + "\n")
        if len([m for m in first.messages if m.role == "user"]) > 1:
            md.append("\n**Prompt (turn 2):** " + [m for m in first.messages if m.role == "user"][1].text + "\n")
    for label, name in PANEL:
        s = next((s for s in L[name].samples if s.id == item), None) if name in L else None
        if s is None:
            md.append(f"\n### {label} (`{name}`)\n\n(not run)\n")
            continue
        replies = [m.text for m in s.messages if m.role == "assistant"]
        md.append(f"\n### {label} (`{name}`)\n\n**Turn 1:**\n\n{replies[0].strip()}\n" + (f"\n**Turn 2:**\n\n{replies[1].strip()}\n" if len(replies) > 1 else ""))
(RUN / "demo_panel.md").write_text("".join(md))
print("".join(md))
