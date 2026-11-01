"""Build slop/eval/run19_scans/: run 19's scan outputs plus run 17's Instruct thinking-on replies renamed to r19_instruct (same frozen
inputs, same Instruct revision 59d61f3c), and a scoring config, so scripts/eval/81_score_run.py can judge the scans against Instruct.
Run 19 evaluates no Instruct cell of its own. -- PI/Claude (opus-5-5)

uv run python scripts/scratch/20261030_run19_scan_scoring_dir.py BOX_RUNS_DIR [RUN_NAME]   (RUN_NAME default run19; also run19o, run20)
"""
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
src = Path(sys.argv[1])  # rsynced run dir
RUN = sys.argv[2] if len(sys.argv) > 2 else "run19"
P = yaml.safe_load((ROOT / f"configs/runs/{RUN}.yaml").read_text())["prefix"]
out = ROOT / f"slop/eval/{RUN}_scans"
box = out / "box_runs"
box.mkdir(parents=True, exist_ok=True)

for f in (ROOT / "configs/eval/inputs/run17").iterdir():
    shutil.copyfile(f, box / f.name)
scans = sorted(p.name.removeprefix(P).removesuffix(".done") for p in src.glob(f"{P}*.done")
               if json.loads(p.read_text()).get("scan"))
for tag in scans:
    for stem in ("think_replies", "think_panel", "think_gsm8k"):
        for p in src.glob(f"{stem}_{P}{tag}.jsonl*"):
            shutil.copyfile(p, box / p.name)
    shutil.copyfile(src / f"{P}{tag}.done", box / f"{P}{tag}.done")
for stem in ("think_replies", "think_panel", "think_gsm8k", "replies", "gsm8k", "panel", "small_tasks"):  # Instruct reference from run 17, model field renamed
    for p in (ROOT / "slop/eval/run17/lease/box_runs").glob(f"{stem}_r17_instruct.jsonl"):
        rows = [json.loads(l) for l in p.open()]
        for r in rows:
            for k in ("model", "base_model"):
                if r.get(k) == "r17_instruct":
                    r[k] = f"{P}instruct"
        (box / p.name.replace("r17_instruct", f"{P}instruct")).write_text("".join(json.dumps(r) + "\n" for r in rows))

cfg = yaml.safe_load((ROOT / f"configs/runs/{RUN}.yaml").read_text())
cfg["name"] = f"{RUN}_scans"
cfg["cells"] = {"instruct": {}} | {t: {} for t in scans}
cfg["thinking_cells"] = list(cfg["cells"])
cfg.pop("mixes", None)
(out / f"{RUN}_scans.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))
print(f"{len(scans)} scans + Instruct -> {box}")
