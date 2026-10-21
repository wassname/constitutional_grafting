"""Join the two independent Sol 6.1 accept/reject passes over the 1,201 scenario chat rows (slop/reviews/20261022_chat_accept_reject/).
A row is rejected when both passes reject it; "same defect" additionally needs the two quoted spans to overlap.
Writes reject_both.jsonl (id, source, both verdicts) and summary.md next to the verdicts. -- PI/Claude, 2026-10-22
usage: uv run python scripts/data/79_chat_accept_reject.py
"""
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "slop/reviews/20261022_chat_accept_reject"
rows = [r for r in map(json.loads, (ROOT / "data/train/run10/chat.jsonl").open()) if r["shape"] != "identity"]


def parse(path: Path) -> dict:
    out = {}
    for line in path.read_text().splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 5 and c[0].isdigit():
            out[c[1].strip("`")] = {"verdict": c[2].upper(), "type": c[3], "quote": c[4].strip("“”\""), "why": c[5] if len(c) > 5 else ""}
    return out


def words(q: str) -> set:
    return set(re.findall(r"[a-z']+", q.lower()))


A, B = {}, {}
for p in sorted((D / "verdicts").glob("batch_*_a.md")):
    A |= parse(p)
for p in sorted((D / "verdicts").glob("batch_*_b.md")):
    B |= parse(p)
ids = [r["id"] for r in rows]
missing = [i for i in ids if i not in A or i not in B]
assert not missing, f"{len(missing)} rows lack a verdict, e.g. {missing[:5]}"
rej = lambda v: v["verdict"].startswith("REJECT")
both = [i for i in ids if rej(A[i]) and rej(B[i])]
same = [i for i in both if len(words(A[i]["quote"]) & words(B[i]["quote"])) >= 0.5 * min(len(words(A[i]["quote"])), len(words(B[i]["quote"]))) > 0]
src = {r["id"]: r["source"].split("+")[0] for r in rows}
with (D / "reject_both.jsonl").open("w") as f:
    for i in both:
        f.write(json.dumps({"id": i, "source": src[i], "same_quote": i in same, "a": A[i], "b": B[i]}) + "\n")
n_src = collections.Counter(src.values())
b_src = collections.Counter(src[i] for i in both)
types = collections.Counter(A[i]["type"].lower().split(";")[0].split("/")[0].strip() for i in both)
md = [f"# Two-pass Sol accept/reject over {len(ids)} scenario chat rows\n",
      f"Rejected by pass a: {sum(rej(A[i]) for i in ids)}; by pass b: {sum(rej(B[i]) for i in ids)}; by both: {len(both)} ({len(both)/len(ids):.0%}); both with overlapping quote: {len(same)}.\n",
      "| source | rows | rejected by both | share |", "|:--|--:|--:|--:|"]
md += [f"| {s} | {n} | {b_src[s]} | {b_src[s]/n:.0%} |" for s, n in n_src.most_common()]
md += ["", "Pass-a defect types among rows rejected by both: " + ", ".join(f"{t} {n}" for t, n in types.most_common(8))]
(D / "summary.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
