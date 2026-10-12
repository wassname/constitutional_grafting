"""Render the striking demos (T=0) side by side as markdown: prompt turns first, then each model's full replies.
usage: python scripts/eval/20_striking_demo.py OUT.md FILE:MODEL:LABEL ...   -- Claude (Opus 5.5)
e.g.   ... slop/eval/tc_baseline/demos_gemma.jsonl:bare_it:"base Gemma" slop/eval/run4/demos_r4_gemma.jsonl:r4_graft_sft_ep2:"run 4 healed ep2"
"""
import json
import sys
from pathlib import Path

ITEMS = ["demo_siblings", "demo_smacking", "demo_trans_sport", "demo_eulogy", "demo_conscious", "demo_starwisp"]

out, specs = Path(sys.argv[1]), sys.argv[2:]
cols = []  # (label, {item_id: row})
for spec in specs:
    path, model, label = spec.split(":", 2)
    rows = {r["item_id"]: r for r in map(json.loads, open(path)) if r["model"] == model}
    assert set(ITEMS) <= set(rows), f"{spec}: missing {set(ITEMS) - set(rows)}"
    cols.append((label, rows))

md = ["Temperature 0, no system prompt, full replies verbatim. Source files and model names are in the command at the end.\n"]
for item in ITEMS:
    first = cols[0][1][item]
    md.append(f"\n### {item.removeprefix('demo_')}\n")
    for i, t in enumerate(first["turns"]):
        md.append(f"\n> **User (turn {i + 1}):** {t['user']}\n")
    for label, rows in cols:
        r = rows[item]
        assert [t["user"] for t in r["turns"]] == [t["user"] for t in first["turns"]], f"{label} {item}: prompts differ"
        md.append(f"\n**{label}**\n")
        for i, t in enumerate(r["turns"]):
            cut = " *(cut at max_new_tokens)*" if t["finish_reason"] == "length" else ""
            md.append(f"\n*turn {i + 1}:*{cut}\n\n{t['assistant'].strip()}\n")
md.append("\n```\npython " + " ".join(["scripts/eval/20_striking_demo.py", str(out)] + [f'"{s}"' for s in specs]) + "\n```\n")
out.write_text("".join(md))
print(f"wrote {out}: {len(ITEMS)} items x {len(cols)} models")
