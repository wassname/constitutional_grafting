# Score the fidelity-check calibration against the 20-row labels (see 20261028_fidelity_calib.py). -- PI/Claude (opus-5-5)
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module

DEFECT = import_module("20261028_fidelity_calib").DEFECT
OUT = Path(__file__).resolve().parents[2] / "data/scratch/20261028_fidelity_calib"
res = [json.loads(l) for l in (OUT / "checks.jsonl").open()]
g = collections.defaultdict(dict)
for x in res:
    g[(x["translator"], x["checker"], x["attempt"])][x["row"]] = x["errors"]

print("| translator | checker | try | fails | flagged defect rows /10 | flagged clean rows /10 | flagged rows |")
print("|---|---|---:|---:|---:|---:|---|")
for (tr, ch, a), rows in sorted(g.items()):
    fails = sum(v is None for v in rows.values())
    fl = {k for k, v in rows.items() if v}
    print(f"| {tr} | {ch} | {a} | {fails} | {len(fl & DEFECT.keys())} | {len(fl - DEFECT.keys())} | {sorted(fl)} |")
