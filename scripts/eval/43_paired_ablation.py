"""Paired differences between grafts and a reference graft on the same items: character (Jev on-target, per item mean over samples),
strength (ABX separated, per item), with 90% item-bootstrap intervals of the difference (2,000 resamples, seed 0), plus maths and
ordinary checks. Character is omitted when not measured, including document-only comparisons. -- PI/OpenAI
"X contributes" only when the interval of the difference excludes 0. No model calls.
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
            c = r["check"]
            cap[r["model"]][0] += float(c["correct"] if "correct" in c else c["format_ok"]); cap[r["model"]][1] += 1
    seen |= {r["model"] for r in J}
sep = defaultdict(lambda: defaultdict(list))
for r in rows(a.strength / "trials.jsonl"):
    sep[r["model"]][r["item_id"]].append(float(r["separated"]))
mean = lambda d: {i: sum(v) / len(v) for i, v in d.items()}
models = set(char) | set(cap) | {a.ref}
maths = {}
for box in a.runs:
    for model in models:
        p = box / f"gsm8k_{model}.jsonl"
        if p.exists():
            maths[model] = sum(r["correct"] for r in rows(p))
ref_c, ref_s = mean(char[a.ref]), mean(sep[a.ref])
show_character = any(char.values())
lines = [f"# Paired differences vs `{a.ref}`\n", "Δ = model − reference, per item, mean over items; 90% item-bootstrap interval of the paired difference.\n"]
if show_character:
    lines += ["| Model | Character | Δ character [90%] | Strength | Δ strength [90%] | Maths /60 | Ordinary |", "|:--|--:|:--|--:|:--|--:|--:|"]
else:
    lines += ["Character was not measured. Ordinary checks retain fractional credit.\n",
              "| Model | Strength | Δ strength [90%] | Maths /60 | Ordinary |", "|:--|--:|:--|--:|--:|"]
for m in sorted(models, key=lambda m: (m != a.ref, m)):
    c, s = mean(char[m]), mean(sep[m])
    dc = {i: c[i] - ref_c[i] for i in c if i in ref_c}; ds = {i: s[i] - ref_s[i] for i in s if i in ref_s}
    fc = (lambda t: f"{t[0]:+.2f} [{t[1]:+.2f}, {t[2]:+.2f}]")
    ordinary = f"{cap[m][0]:g}/{cap[m][1]}" if cap[m][1] else "—"
    st = (f"{100 * sum(s.values()) / len(s):.0f}%", "ref" if m == a.ref else fc(tuple(100 * x for x in boot(ds)))) if s else ("not run", "not run")
    character = f"{sum(c.values()) / len(c):+.2f}" if c else "not measured"
    character_delta = "ref" if m == a.ref else (fc(boot(dc)) if dc else "not measured")
    prefix = f"| {m} | {character} | {character_delta}" if show_character else f"| {m}"
    maths_score = maths[m] if m in maths else "not run"
    lines.append(f"{prefix} | {st[0]} | {st[1]} | {maths_score} | {ordinary} |")
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
