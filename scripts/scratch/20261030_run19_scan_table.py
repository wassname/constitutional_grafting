"""Run 19 dose-scan tables: character (v2 judge vs Instruct, 37 judged scan items, sample 0, 90% item bootstrap), capability checks,
code, maths, for the all-data and group-mix sweeps and the one-group removals. -- PI/Claude (opus-5-5)

uv run python scripts/scratch/20261030_run19_scan_table.py
"""
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "slop/eval/run19_scans"
rows = [json.loads(l) for l in (D / "score_v2/character_thinking/judged.jsonl").open()]
char, cap = defaultdict(list), defaultdict(list)
for r in rows:
    if r.get("on_target") is not None:
        char[r["model"]].append(r["on_target"])
    elif r.get("check") and not r.get("judged"):
        cap[r["model"]].append(min(v for k, v in r["check"].items() if isinstance(v, (int, float)) and k != "choice"))
scan_ids = {json.loads(l)["id"] for l in (ROOT / "slop/eval/run17/inputs/scan_items.jsonl").open()}
code = defaultdict(float)
for l in (D / "score_v2/code_tools/judged.jsonl").open():
    r = json.loads(l)
    if r["model"].startswith("think:") and r["item_id"] in scan_ids and r["sample"] == 0 and r["family"] == "code":
        code[r["model"].removeprefix("think:")] += r["check"].get("correct") or 0
rng = random.Random(0)


def row(model, label):
    v = char[model if model != "r19_instruct" else "r19_instruct_rerun"]  # Instruct is the reference: its other sample is the noise row
    bs = sorted(st.mean(rng.choices(v, k=len(v))) for _ in range(2000))
    gsm = [json.loads(l)["correct"] for l in (D / f"box_runs/think_gsm8k_{model}.jsonl").open()][:20]
    return f"| {label} | {st.mean(v):+.2f} [{bs[100]:+.2f}, {bs[1900]:+.2f}] | {sum(cap[model]):.0f}/{len(cap[model])} | {code[model]:.0f}/10 | {sum(gsm)}/20 |"


head = "| model | character [90%] | capability | code | maths |\n|---|---|---|---|---|"
print("All-data adapter (probe: coherent x1, broken x2)\n" + head)
print(row("r19_instruct", "Instruct"))
for d in ("0.25", "0.5", "1", "1.6"):
    print(row(f"r19_all_{d}", f"all-data ×{d}"))
print("\nGroup mix: dilemmas s, help s, texts 2s, identity s (probe: coherent x0.5, broken x1)\n" + head)
print(row("r19_instruct", "Instruct"))
for d in ("0.125", "0.25", "0.5", "0.7", "0.8"):
    print(row(f"r19_groups_{d}", f"group mix ×{d}"))
print("\nOne group removed from group mix ×0.5\n" + head)
print(row("r19_groups_0.5", "group mix ×0.5 (all four)"))
for g in ("dilemmas", "help", "texts", "identity"):
    print(row(f"r19_groups_0.5_minus_{g}", f"minus {g}"))
