"""Side by side: Opus reply vs Echo restyles with the plain / modern / old sample sets, same rows.
usage: python3 scripts/scratch/echo_sets_side_by_side.py   -- Claude (Opus 5.5)"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETS = {"plain": "Marcus Aurelius (Hays) x2 + 2 Opus replies", "modern": "Epictetus, A. A. Long tr., 5 Handbook sections + 1 Opus reply",
        "old": "Epictetus, Oldfather 1925 tr., 3 long passages"}
rows = {s: {r["id"]: r for r in map(json.loads, (ROOT / f"data/frontier/sft_stoic_{s}/items.jsonl").open())} for s in SETS
        if (ROOT / f"data/frontier/sft_stoic_{s}/items.jsonl").exists()}
ids = [i for i in next(iter(rows.values())) if all(i in r for r in rows.values())]
md = ["# Echo restyle: which sample set?\n\nSame Opus rows, three sets of writing samples. Request untouched; only the reply is restyled.\n\n"
      + "".join(f"- {s}: {d}\n" for s, d in SETS.items() if s in rows)
      + "\nchecks: short = share of sentences under 6 words (fragment cadence above 0.3); words = mean words per sentence; overlap = word overlap with the Opus reply (copy above 0.8).\n\n-- Claude (Opus 5.5), scripts/scratch/echo_sets_side_by_side.py\n"]
for i in ids:
    first = next(iter(rows.values()))[i]
    md.append(f"\n---\n\n## {i} ({first['source']}, {first['shape']})\n\n### Request\n\n{first['request']}\n\n### Opus 5.5 (original)\n\n{first['musonius_opus']}\n")
    for s, r in rows.items():
        ck = r[i]["meta"]["restyle"]["checks"]
        md.append(f"\n### Echo, {s} (short {ck['short_sentence_share']}, words {ck['mean_sentence_words']}, overlap {ck['overlap']}, lint {ck['lint']}, new digits {ck['new_digits']})\n\n{r[i]['musonius']}\n")
out = ROOT / "slop/reviews/20261009_echo_restyle_sets.md"
out.write_text("".join(md))
print(out, len(ids), "rows")
