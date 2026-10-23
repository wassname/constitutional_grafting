# /// script
# requires-python = ">=3.11"
# dependencies = ["model2vec", "numpy"]
# ///
"""Nearest training rows to a demo, by meaning as well as words: model2vec (potion-base-8M) cosine between the demo text (prompt turns +
reply) and every training row, chunked so long documents are matched on their best 200-word window. Use for the AGENTS.md striking
demo check: is the demo out of distribution, or does a training row tell the same story?
usage: uv run scripts/eval/24_nearest_rows.py DEMO.txt TRAIN.jsonl[:kind] ... [--k 8]   -- PI/Claude (Opus 5.5)"""
import argparse
import json

import numpy as np
from model2vec import StaticModel


def chunks(text: str, n: int = 200, step: int = 100) -> list[str]:
    w = text.split()
    return [" ".join(w[i:i + n]) for i in range(0, max(1, len(w) - n + step), step)] or [text]


def row_text(r: dict) -> str:
    if "text" in r:
        return r["text"]
    return " ".join(s["text"] for s in r["segments"])


ap = argparse.ArgumentParser()
ap.add_argument("demo"); ap.add_argument("train", nargs="+"); ap.add_argument("--k", type=int, default=8)
a = ap.parse_args()
m = StaticModel.from_pretrained("minishlab/potion-base-8M")
q = m.encode([open(a.demo).read()])[0]; q /= np.linalg.norm(q)
hits = []
for spec in a.train:
    path, _, kind = spec.partition(":")
    for r in map(json.loads, open(path)):
        if kind and r.get("kind") != kind:
            continue
        cs = chunks(row_text(r))
        e = m.encode(cs); e /= np.linalg.norm(e, axis=1, keepdims=True)
        s = e @ q; i = int(s.argmax())
        hits.append((float(s[i]), spec, f"{r['id']} [{r.get('shape') or r.get('kind')}]", cs[i]))
hits.sort(reverse=True)
print(f"n rows scored: {len(hits)}; cosine p50 {np.median([h[0] for h in hits]):.3f}, p99 {np.percentile([h[0] for h in hits], 99):.3f}")
for s, spec, rid, txt in hits[:a.k]:
    print(f"\n### {s:.3f} {spec} {rid}\n{txt[:700]}")
