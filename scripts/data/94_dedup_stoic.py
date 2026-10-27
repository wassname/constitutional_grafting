"""Drop near-duplicate Stoic chunks: same passage selected twice (e.g. Pigliucci's 'Live Like a Stoic' is the UK edition of
'A Handbook for New Stoics'; Stoic Week handbooks reuse text across years). Found by slop/audits/20261027_corpus_habits.
All pairs within one author; 5-word-shingle Jaccard >= 0.5 counts as a duplicate; keep the higher reasoning score, then the
earlier row. Original stays untouched (pinned by configs/data/releases/run10.yaml, run11.yaml).
Output: data/stoic_corpus/selected_dedup.jsonl and slop/audits/20261027_corpus_habits/stoic_dedup.md.
usage: uv run --no-project python scripts/data/94_dedup_stoic.py   -- PI/Claude (opus-5-5), 2026-10-27
"""
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data/stoic_corpus/selected.jsonl"
OUT = ROOT / "data/stoic_corpus/selected_dedup.jsonl"
REPORT = ROOT / "slop/audits/20261027_corpus_habits/stoic_dedup.md"
JACCARD = 0.5


def shingles(text, k=5):
    ws = re.findall(r"[a-z']+", text.lower())
    return {" ".join(ws[i:i + k]) for i in range(len(ws) - k + 1)}


def main():
    rows = [json.loads(l) for l in SRC.open()]
    sh = [shingles(r["text"]) for r in rows]
    by_author = defaultdict(list)
    for i, r in enumerate(rows):
        by_author[r["author"]].append(i)
    drop = {}  # dropped index -> (kept index, jaccard)
    for idx in by_author.values():
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                if i in drop or j in drop:
                    continue
                inter = len(sh[i] & sh[j])
                if inter == 0:
                    continue
                jac = inter / len(sh[i] | sh[j])
                if jac >= JACCARD:
                    keep_i = (rows[i]["score"]["reasoning"], -i) >= (rows[j]["score"]["reasoning"], -j)
                    drop[j if keep_i else i] = (i if keep_i else j, round(jac, 3))
    kept = [r for i, r in enumerate(rows) if i not in drop]
    OUT.write_text("".join(json.dumps(r) + "\n" for r in kept))
    words = lambda r: len(r["text"].split())
    lines = [f"# Stoic near-duplicate removal\n",
             f"Source `{SRC.relative_to(ROOT)}` sha256 `{hashlib.sha256(SRC.read_bytes()).hexdigest()}`: {len(rows)} chunks.",
             f"Output `{OUT.relative_to(ROOT)}` sha256 `{hashlib.sha256(OUT.read_bytes()).hexdigest()}`: {len(kept)} chunks.",
             f"Dropped {len(drop)} chunks, {sum(words(rows[i]) for i in drop):,} words (rule: same author, 5-gram Jaccard >= {JACCARD}).\n",
             "| dropped | work | kept | work | Jaccard |", "|:--|:--|:--|:--|--:|"]
    for d, (k, jac) in sorted(drop.items(), key=lambda x: -x[1][1]):
        lines.append(f"| `{rows[d]['id']}` | {rows[d]['work']} | `{rows[k]['id']}` | {rows[k]['work']} | {jac} |")
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:5]))


if __name__ == "__main__":
    main()
