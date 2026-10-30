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
import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TINYCHAR = Path("/workspace/2026/tiny-character")
sys.path.insert(0, str(TINYCHAR / "src"))
from tiny_character.subset import load_subset, scored_together  # noqa: E402

SWEEP = ROOT / "slop/eval/run17_sweep"
GRAFTS = ["r17_reason_docs_0.25", "r17_reason_docs_0.5", "r17_reason_docs_1", "r17_reason_docs_1.5", "r17_reason_docs_2",
          "r17_reason_base_0.5", "r17_reason_base_1", "r17_newD_1"]
KEEP_WHOLE = {"instructions", "pov", "sycophancy"}
OUT = ROOT / "configs/eval/tinychar_subsets/qwen3.5-35b-a3b_20261030_half.txt"

snapshot = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "slop/eval/run17/inputs/items.jsonl").open()}
current = {json.loads(l)["id"]: json.loads(l) for l in (TINYCHAR / "data/items.jsonl").open()}
items = {i: current.get(i, it | {"length_group": "standard"}) for i, it in snapshot.items()}  # types come from tiny-character's items

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
        if c and not snapshot.get(r["item_id"], {}).get("judged", True):
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
keep = {i for g in groups.values() for i in g if items[i]["family"] in KEEP_WHOLE}
# Judged items: half overall, best groups first. Code-only items: half of each family (capability, code, tools), so no skill is
# reduced to the one-item floor.
strata = [("judged", lambda it: it["judged"])] + [(f, lambda it, f=f: not it["judged"] and it["family"] == f)
                                                   for f in sorted({it["family"] for it in items.values() if not it["judged"]})]
for name, member in strata:
    pool = [g for g in groups.values() if member(items[g[0]]) and not set(g) & keep]
    target = sum(member(it) for it in items.values()) // 2
    for g in sorted(pool, key=lambda g: -st.mean(informativeness(i) for i in g)):
        if sum(member(items[i]) for i in keep) >= target:
            break
        keep |= set(g)
while True:  # tiny-character's floor: every family and item type kept; add the best group that fills a gap
    try:
        load_subset_items = load_subset
        tmp = OUT.with_suffix(".check")
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text("".join(i + "\n" for i in sorted(keep)))
        load_subset_items(tmp, items)
        tmp.unlink()
        break
    except (AssertionError, ValueError) as e:
        missing = str(e)
        cand = [g for g in groups.values() if not set(g) & keep]
        best = max(cand, key=lambda g: (any(items[g[0]]["family"] in missing or str(items[g[0]].get("length_group")) in missing for _ in [0]),
                                        st.mean(informativeness(i) for i in g)))
        print("floor:", missing.splitlines()[0][:120], "-> add", best)
        keep |= set(best)

header = [f"# Calibrated half of tiny-character ({len(keep)} of {len(items)} items) for Qwen3.5-35B-A3B grafts, made by",
          "# scripts/eval/84_tinychar_subset.py (constitutional_grafting) on 2026-10-30 from run 17's thinking-on dose sweep",
          "# (slop/eval/run17_sweep: v2 judge on-target, code/tool checks), selected on sample 0 only.",
          "# Rule: judged items by score spread across 8 grafted models; code-only items by Instruct-passes-then-fails-with-dose, half per family;",
          "# groups scored together kept whole; instructions, pov, sycophancy kept whole; half of each kind; tiny-character floor.",
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
