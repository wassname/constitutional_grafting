"""Crude per-row rates of the moves goal 8 needs, for an SFT training file vs run 2's frozen file.
Regex proxies only (a cheap check of the data before renting a GPU, not a judge): does the reply ask a question back, ask a specific
one (what/which/how much/when/whether/do you/is it...?), use uncertainty words, or carry the "I will not" cadence.
usage: uv run scripts/data/scratch/33_mix_rates.py [data/train/sft.jsonl ...]   -- Claude (Opus 5.5)
"""
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILES = sys.argv[1:] or ["data/train/sft_run2_frozen.jsonl", "data/train/sft.jsonl"]
SPECIFIC = re.compile(r"(?:^|[.!?]\s+)(?:What|Which|How (?:much|many|long|often|old)|When|Where|Who|Whether|Do (?:you|they)|Does|Did|Is (?:it|there|she|he)|Are (?:you|they|there)|Has|Have you|Can you tell|Could you tell)\b[^?]{3,200}\?")
UNSURE = re.compile(r"\b(?:I am not sure|I'm not sure|not certain|I don't know|I do not know|uncertain|unsure|I may be wrong|might be wrong|my lean|I lean|probably|likely|moderately sure|fairly sure|depends on|it turns on|what would change)\b", re.I)
WONT = re.compile(r"\bI (?:will not|won't|cannot|can't)\b")


def reply(row: dict) -> str:
    return row["segments"][-1]["text"]


def source(row: dict) -> str:
    s = row["source"]
    return "identity" if row.get("shape") == "identity" else s.split("+")[-1] if "+" in s else s


rows_md = ["| file | source | rows | has a question | asks a specific question | uncertainty words | \"I will not / can't\" | median words |",
           "|:--|:--|--:|--:|--:|--:|--:|--:|"]
for f in FILES:
    rows = [json.loads(line) for line in open(ROOT / f)]
    groups = defaultdict(list)
    for r in rows:
        groups[source(r)].append(reply(r))
    groups["all"] = [reply(r) for r in rows]
    for k, texts in sorted(groups.items(), key=lambda kv: (kv[0] == "all", -len(kv[1]))):
        pct = lambda rx: f"{100 * sum(bool(rx.search(t)) for t in texts) / len(texts):.0f}%"
        q = f"{100 * sum('?' in t for t in texts) / len(texts):.0f}%"
        med = statistics.median(len(t.split()) for t in texts)
        rows_md.append(f"| {Path(f).name} | {'**all**' if k == 'all' else k} | {len(texts)} | {q} | {pct(SPECIFIC)} | {pct(UNSURE)} | {pct(WONT)} | {med:.0f} |")
print("\n".join(rows_md))
