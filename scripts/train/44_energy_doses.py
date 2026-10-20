"""Print name=k coefficients that rescale each run-9 adapter to the incumbent graft's update energy times a multiplier.
usage: python scripts/train/44_energy_doses.py RUN_DIR INCUMBENT_ENERGY MULT NAME...   (reads RUN_DIR/energy_r9_NAME.log from 43_adapter_energy.py)
-- PI/Claude (Opus 5.5)"""
import re
import sys
from pathlib import Path

run, inc, mult, *names = sys.argv[1:]
out = []
for n in names:
    e = float(re.search(r"E_ref=([0-9.]+)", (Path(run) / f"energy_r9_{n}.log").read_text()).group(1))
    out.append(f"{n}={float(mult) * float(inc) / e:.2f}")
print(" ".join(out))
