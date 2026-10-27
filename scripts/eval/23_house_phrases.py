"""House-phrase rate per model on tiny-character replies: share of dialogues whose assistant turns contain any phrase the graft
documents over-use (list: scripts/data/scratch/50_docs_v2.py HOUSE, from slop/reviews/20261015_graft_data_read.md).
usage: python scripts/eval/23_house_phrases.py REPLIES.jsonl [MODEL ...]   -- PI/Claude (Opus 5.5)"""
import ast
import json
import sys
from collections import defaultdict
from pathlib import Path

src = (Path(__file__).resolve().parents[1] / "data" / "scratch" / "50_docs_v2.py").read_text()
i = src.index("HOUSE = [") + len("HOUSE = ")
HOUSE = [p.lower() for p in ast.literal_eval(src[i: src.index("]", i) + 1])]  # read the list without importing (that script needs API deps)

rows = [json.loads(l) for l in open(sys.argv[1])]
models = sys.argv[2:] or sorted({r["model"] for r in rows})
hit = defaultdict(list)
for r in rows:
    if r["model"] in models:
        text = " ".join(t["assistant"] for t in r["turns"]).lower()
        hit[r["model"]].append(any(p in text for p in HOUSE))
for m in models:
    print(f"{m}\t{sum(hit[m]) / len(hit[m]):.3f}\t(n={len(hit[m])})")
