"""Calibrated half of tiny-character for Qwen3.5-35B-A3B grafts (wassname 2026-10-30: "can we just halve it ... one of each type";
tiny-character `--items-subset`, commit 43c5b73).

Calibration data: run 17's dose sweep, thinking on (reason_docs x0.25-2, reason_base x0.5-1, newD x1 vs Instruct): v2 judge
on-target scores (slop/eval/run17_sweep/score_v2/character_thinking) and code/tool checks (score_frozen/code_tools). Selection uses
sample 0 only; the printed test uses sample 1.
  judged items:     spread of the item's score across the grafted models;
  code-only items:  Instruct passes, and the pass rate falls with dose (Instruct pass - mean grafted pass); too hard or too easy = 0;
                    half of each code-only family (capability, code, tools).
Groups tiny-character scores together (a choice and its _rev; a pov act's 3 askers) are kept or dropped whole. The early-warning
families (instructions, pov, sycophancy; first to break in run 17) are kept whole. Half of each kind is then filled by score, and
tiny-character's own check (every family and item type kept, no split group) must pass.

uv run python scripts/eval/84_tinychar_subset.py  ->  configs/eval/tinychar_subsets/qwen3.5-35b-a3b_20261030_half.txt
-- PI/Claude (opus-5-5)
"""
import argparse
import json
import statistics as st
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TINYCHAR = Path("/workspace/2026/tiny-character")
sys.path.insert(0, str(TINYCHAR / "src"))
from tiny_character.subset import ITEM_TYPES, load_subset, scored_together  # noqa: E402

SWEEP = ROOT / "slop/eval/run17_sweep"
GRAFTS = ["r17_reason_docs_0.25", "r17_reason_docs_0.5", "r17_reason_docs_1", "r17_reason_docs_1.5", "r17_reason_docs_2",
          "r17_reason_base_0.5", "r17_reason_base_1", "r17_newD_1"]
KEEP_WHOLE = {"instructions", "pov", "sycophancy"}
# Three sizes (wassname 2026-10-31: one calibrated tiny-character evaluation for probe, scan and full): share of each kind kept by
# informativeness, and whether the early-warning families are kept whole. The probe is the floor: one group per family and item type.
SIZES = {"half": (0.5, True), "quarter": (0.25, False), "probe": (0.0, False)}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--size", choices=SIZES, default="half")
SIZE = parser.parse_args().size
FRAC, WHOLE = SIZES[SIZE]
OUT = ROOT / f"configs/eval/tinychar_subsets/qwen3.5-35b-a3b_20261030_{SIZE}.txt"

TINYCHAR_COMMIT = "54b8bc8"  # subset.py from here on: item length type from max_new_tokens, so the run 17 snapshot loads
assert subprocess.run(["git", "-C", TINYCHAR, "merge-base", "--is-ancestor", TINYCHAR_COMMIT, "HEAD"]).returncode == 0, f"tiny-character older than {TINYCHAR_COMMIT}"
items = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "slop/eval/run17/inputs/items.jsonl").open()}  # the snapshot the judge gets

judged = defaultdict(dict)  # (item, sample) -> model -> on-target
for l in (SWEEP / "score_v2/character_thinking/judged.jsonl").open():
    r = json.loads(l)
    if r.get("on_target") is not None:
        judged[(r["item_id"], r["sample"])][r["model"]] = r["on_target"]
passed = defaultdict(dict)  # (item, sample) -> model -> pass in [0, 1]
for path in (SWEEP / "score_v2/character_thinking/judged.jsonl", SWEEP / "score_frozen/code_tools/judged.jsonl"):
    for l in path.open():
        r = json.loads(l)
        c = r.get("check")
        if c and not items.get(r["item_id"], {}).get("judged", True):
            v = [x for k, x in c.items() if isinstance(x, (int, float)) and k != "choice"]
            passed[(r["item_id"], r["sample"])][r["model"].removeprefix("think:")] = min(v)


def informativeness(i, sample=0) -> float:
    if items[i]["judged"]:
        s = judged.get((i, sample), {})
        return st.pstdev(s[m] for m in GRAFTS) if all(m in s for m in GRAFTS) else 0.0
    s = passed.get((i, sample), {})
    if "r17_instruct" not in s or not all(m in s for m in GRAFTS):
        return 0.0
    return max(0.0, s["r17_instruct"] - st.mean(s[m] for m in GRAFTS))


groups = defaultdict(list)
for i, it in items.items():
    groups[scored_together(it)].append(i)
keep = {i for g in groups.values() for i in g if WHOLE and items[i]["family"] in KEEP_WHOLE}
# Judged items: half overall, best groups first. Code-only items: half of each family (capability, code, tools), so no skill is
# reduced to the one-item floor.
strata = [("judged", lambda it: it["judged"])] + [(f, lambda it, f=f: not it["judged"] and it["family"] == f)
                                                   for f in sorted({it["family"] for it in items.values() if not it["judged"]})]
for name, member in strata:
    pool = [g for g in groups.values() if member(items[g[0]]) and not set(g) & keep]
    target = int(sum(member(it) for it in items.values()) * FRAC)
    for g in sorted(pool, key=lambda g: -st.mean(informativeness(i) for i in g)):
        if sum(member(items[i]) for i in keep) >= target:
            break
        keep |= set(g)
# tiny-character's floor: every family and item-type value kept. Fill each gap with the most informative group that has it,
# early-warning families first so even the probe keeps one of each.
need = [("family", f) for f in sorted(KEEP_WHOLE)] + [(t, v) for t, of in ITEM_TYPES.items() for v in sorted({str(of(it)) for it in items.values()})]
for t, v in need:
    if any(str(ITEM_TYPES[t](items[i])) == v for i in keep):
        continue
    cand = [g for g in groups.values() if any(str(ITEM_TYPES[t](items[i])) == v for i in g)]
    keep |= set(max(cand, key=lambda g: st.mean(informativeness(i) for i in g)))
# The probe must also measure maths: add the four most informative non-executable GSM tasks, on sample 0 only.
if SIZE == "probe":
    gsm = [i for i, it in items.items() if it["family"] == "capability" and (it["checks"] or {}).get("kind") in ("gsm8k_cot", "gsm8k_json")]
    keep |= set(sorted(gsm, key=lambda i: (-informativeness(i), i))[:4])
tmp = OUT.with_suffix(".check")
tmp.write_text("".join(i + "\n" for i in sorted(keep)))
load_subset(tmp, items)  # tiny-character's own check: families, item types, groups scored together
tmp.unlink()

header = [f"# Calibrated {SIZE} of tiny-character ({len(keep)} of {len(items)} items) for Qwen3.5-35B-A3B grafts, made by",
          "# scripts/eval/84_tinychar_subset.py (constitutional_grafting) on 2026-10-30 from run 17's thinking-on dose sweep",
          "# (slop/eval/run17_sweep: v2 judge on-target, code/tool checks), selected on sample 0 only.",
          "# Rule: judged items by score spread across 8 grafted models; code-only items by Instruct-passes-then-fails-with-dose, half per family;",
          f"# groups scored together kept whole; {'instructions, pov, sycophancy kept whole; ' if WHOLE else ''}{FRAC:.0%} of each kind; tiny-character floor (one per family and item type).",
          *(["# Probe maths: four non-executable capability GSM items ranked by sample-0 informativeness (ties by id)."] if SIZE == "probe" else []),
          f"# Item snapshot: slop/eval/run17/inputs/items.jsonl (not tiny-character's v2 items); floor checked with tiny-character {TINYCHAR_COMMIT}.",
          "# Compare only with runs on the same subset. Re-check against a random same-size subset when change.md changes."]
OUT.write_text("\n".join(header) + "\n" + "".join(i + "\n" for i in sorted(keep)))
fam = defaultdict(lambda: [0, 0])
for i, it in items.items():
    fam[it["family"]][1] += 1
    fam[it["family"]][0] += i in keep
print(f"{len(keep)} of {len(items)} items -> {OUT}")
print("kept per family:", {f: f"{a}/{b}" for f, (a, b) in sorted(fam.items())})

# Held-out test (sample 1) on the judged items: paired difference and t over items.
pairs = [("r17_reason_docs_1", "r17_instruct_rerun", "graft x1 vs Instruct rerun"), ("r17_reason_docs_1", "r17_reason_docs_0.25", "x1 vs x0.25"),
         ("r17_reason_docs_1", "r17_reason_docs_2", "x1 vs x2 (breakdown)"), ("r17_reason_docs_1", "r17_reason_docs_1.5", "x1 vs x1.5")]
both = [i for i in items if items[i]["judged"] and all(m in judged.get((i, 1), {}) for m in GRAFTS + ["r17_instruct_rerun"])]
print("\n| sample 1 | all judged | subset |\n|---|---|---|")
for a, b, label in pairs:
    cells = []
    for S in (both, [i for i in both if i in keep]):
        d = [judged[(i, 1)][a] - judged[(i, 1)][b] for i in S]
        cells.append(f"{st.mean(d):+.2f} (t {st.mean(d) / (st.stdev(d) / len(d) ** .5):.1f}, n={len(d)})")
    print(f"| {label} | " + " | ".join(cells) + " |")
