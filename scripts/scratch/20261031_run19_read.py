"""Side-by-side final replies (thinking on, sample 0) of run 19's full-evaluation models for the read-package items, for a human read.
uv run python scripts/scratch/20261031_run19_read.py ITEM [ITEM ...] [--chars N]   -- PI/Claude (opus-5-5)"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "slop/eval/run19_full/box_runs"
MODELS = {"Instruct": "r19_instruct", "all-data ×0.5": "r19_full_all_0.5", "all-data ×1": "r19_full_all_1", "group mix ×0.25": "r19_full_groups_0.25"}
ap = argparse.ArgumentParser()
ap.add_argument("items", nargs="+")
ap.add_argument("--chars", type=int, default=900)
a = ap.parse_args()
rows = {}
for label, tag in MODELS.items():
    for stem in ("think_replies", "think_panel", "think_demos"):
        p = B / f"{stem}_{tag}.jsonl"
        if p.exists():
            for l in p.open():
                r = json.loads(l)
                if r["sample"] == 0:
                    rows[(label, r["item_id"])] = r
for item in a.items:
    first = next(r for (lab, i), r in rows.items() if i == item)
    print(f"\n######## {item}")
    for k, t in enumerate(first["turns"]):
        print(f"[user {k + 1}] {t['user'][:600]}")
    for label in MODELS:
        r = rows.get((label, item))
        if r is None:
            print(f"--- {label}: (no reply)")
            continue
        for k, t in enumerate(r["turns"]):
            print(f"--- {label} turn {k + 1}: {(t['assistant'] or '').strip()[:a.chars]}")
