"""Can tiny-character be halved without losing the dose signal? (wassname 2026-10-30: "drop items where every model gets about the same
score ... we still need one from each type of question ... can we just halve it anyway")

Data: run 17 sweep, v2 judge, thinking on, 2 samples per item (slop/eval/run17_sweep/score_v2/character_thinking/judged.jsonl).
Select on sample 0 only, test on sample 1, so the selection cannot fit the noise it is tested on.
Selection: an item's spread across the 8 grafted models (std of its scores), keeping at least one item per family; compare with a
random half (same family rule) and the full set. Test: for model pairs that matter for choosing a dose, the paired difference and
its t = mean / standard error over items. -- PI/Claude (opus-5-5)
"""
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
rows = [json.loads(l) for l in (ROOT / "slop/eval/run17_sweep/score_v2/character_thinking/judged.jsonl").open()]
rows = [r for r in rows if r.get("on_target") is not None]
score = defaultdict(dict)  # (item, sample) -> model -> on_target
family = {}
for r in rows:
    score[(r["item_id"], r["sample"])][r["model"]] = r["on_target"]
    family[r["item_id"]] = r["family"]
models = sorted({m for v in score.values() for m in v} - {"r17_instruct_rerun"})
items = sorted({i for i, s in score if all(m in score[(i, 0)] and m in score[(i, 1)] for m in models + ["r17_instruct_rerun"])})
fams = sorted({family[i] for i in items})


def spread(i):  # selection statistic, sample 0 only
    return st.pstdev(score[(i, 0)][m] for m in models)


def half(rank_key, seed=None):
    """Half the items: one per family first (highest key), then the highest key overall."""
    order = sorted(items, key=rank_key, reverse=True)
    pick = [next(i for i in order if family[i] == f) for f in fams]
    pick += [i for i in order if i not in pick][: len(items) // 2 - len(pick)]
    return pick


rng = random.Random(0)
rand_key = {i: rng.random() for i in items}
sets = {"full": items, "half by spread (sample 0)": half(spread), "random half": half(lambda i: rand_key[i])}
pairs = [("r17_reason_docs_1", "r17_instruct_rerun", "graft x1 vs Instruct rerun"),
         ("r17_reason_docs_1", "r17_reason_docs_0.25", "x1 vs x0.25"),
         ("r17_reason_docs_1", "r17_reason_docs_2", "x1 vs x2 (breakdown)"),
         ("r17_reason_docs_1", "r17_reason_docs_1.5", "x1 vs x1.5 (plateau)"),
         ("r17_reason_docs_1", "r17_reason_base_1", "docs vs no docs, x1")]
print(f"{len(items)} items with both samples, {len(fams)} families; test on sample 1\n")
print("| pair | " + " | ".join(f"{k} (n={len(v)})" for k, v in sets.items()) + " |")
print("|---|" + "---|" * len(sets))
for a, b, label in pairs:
    cells = []
    for S in sets.values():
        d = [score[(i, 1)][a] - score[(i, 1)][b] for i in S]
        cells.append(f"{st.mean(d):+.2f} (t {st.mean(d) / (st.stdev(d) / len(d) ** .5):.1f})")
    print(f"| {label} | " + " | ".join(cells) + " |")
print("\nfamilies in the spread half:", {f: sum(family[i] == f for i in sets["half by spread (sample 0)"]) for f in fams})
