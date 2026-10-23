"""Paired differences between grafts and a reference graft on the same items: character (Jev on-target, per item mean over samples),
strength (ABX separated, per item), with 90% item-bootstrap intervals of the difference (2,000 resamples, seed 0), plus maths and
ordinary checks. "X contributes" only when the interval of the difference excludes 0. No model calls.
usage: python scripts/eval/43_paired_ablation.py REF_MODEL OUT.md BOX_RUNS ... --judged DIR ... --strength DIR   -- PI/Claude"""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def rows(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines()]


def boot(d: dict, n: int = 2000) -> tuple[float, float, float]:
    v = list(d.values()); rng = random.Random(0)
    bs = sorted(sum(rng.choice(v) for _ in v) / len(v) for _ in range(n))
    return sum(v) / len(v), bs[int(0.05 * n)], bs[int(0.95 * n) - 1]


ap = argparse.ArgumentParser()
ap.add_argument("ref"); ap.add_argument("out", type=Path); ap.add_argument("runs", nargs="+", type=Path)
ap.add_argument("--judged", nargs="+", type=Path, required=True); ap.add_argument("--strength", type=Path, required=True)
a = ap.parse_args()
char, cap = defaultdict(lambda: defaultdict(list)), defaultdict(lambda: [0, 0])
items = {r["id"]: r for r in rows(ROOT / "slop/eval/run8/items.jsonl")}
seen = set()
for d in a.judged:
    J = [r for r in rows(d / "judged.jsonl") if r["model"] not in seen]
    for r in J:
        if r.get("on_target") is not None:
            char[r["model"]][r["item_id"]].append(r["on_target"])
        if r["family"] == "capability":
            c = r.get("check") or {}
            cap[r["model"]][0] += float(bool(c.get("correct", c.get("format_ok")))); cap[r["model"]][1] += 1
    seen |= {r["model"] for r in J}
sep = defaultdict(lambda: defaultdict(list))
for r in rows(a.strength / "trials.jsonl"):
    sep[r["model"]][r["item_id"]].append(float(r["separated"]))
mean = lambda d: {i: sum(v) / len(v) for i, v in d.items()}
maths = {}
for box in a.runs:
    for p in box.glob("gsm8k_r10_*.jsonl"):
        maths[p.stem.removeprefix("gsm8k_")] = sum(r["correct"] for r in rows(p))
ref_c, ref_s = mean(char[a.ref]), mean(sep[a.ref])
lines = [f"# Paired differences vs `{a.ref}`\n", "Δ = model − reference, per item, mean over items; 90% item-bootstrap interval of the paired difference.\n",
         "| Model | Character | Δ character [90%] | Strength | Δ strength [90%] | Maths /60 | Ordinary |", "|:--|--:|:--|--:|:--|--:|--:|"]
for m in sorted(set(char) | {a.ref}, key=lambda m: (m != a.ref, m)):
    if m not in maths:
        continue
    c, s = mean(char[m]), mean(sep[m])
    dc = {i: c[i] - ref_c[i] for i in c if i in ref_c}; ds = {i: s[i] - ref_s[i] for i in s if i in ref_s}
    fc = (lambda t: f"{t[0]:+.2f} [{t[1]:+.2f}, {t[2]:+.2f}]")
    ordinary = f"{cap[m][0]:g}/{cap[m][1]}" if cap[m][1] else "—"
    lines.append(f"| {m} | {sum(c.values()) / len(c):+.2f} | {'ref' if m == a.ref else fc(boot(dc))} | {100 * sum(s.values()) / len(s):.0f}% | "
                 f"{'ref' if m == a.ref else fc(tuple(100 * x for x in boot(ds)))} | {maths[m]} | {ordinary} |")
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
