"""One baseline for both recipes: tiny-char 03_judge (latest pin) of newD_1 thinking-off and reason_docs_1 thinking-on visible finals,
both against Instruct thinking-off. Mirrors 81_score_run.py's judge call. -- PI/Claude (opus-5-5), 2026-10-29
usage: uv run --no-project python scripts/scratch/20261029_cross_mode_judge.py RUN_DIR OUT"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TC = ROOT / ".local/tiny-character-8c01eca"
run, out = Path(sys.argv[1]), ROOT / sys.argv[2]
out.mkdir(parents=True, exist_ok=True)
rows = lambda p: [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]
items = {i["id"]: i for i in rows(TC / "data/items.jsonl")}
keep = {k for k, i in items.items() if i["family"] not in ("code", "tools")}

recs = rows(run / "replies_r17_instruct.jsonl") + rows(run / "replies_r17_newD_1.jsonl")
recs += [r | {"model": "r17_reason_docs_1_think"} for r in rows(run / "think_replies_r17_reason_docs_1.jsonl")]
recs = [r for r in recs if r["item_id"] in keep]
(out / "replies.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs))
(out / "items.jsonl").write_text("".join(json.dumps(items[i], ensure_ascii=False) + "\n" for i in sorted({r["item_id"] for r in recs})))
label = "cg_run17_cross_mode_8c01eca"
argv = [str(TC / ".venv/bin/python"), str(TC / "scripts/03_judge.py"), "--replies", str(out / "replies.jsonl"), "--items", str(out / "items.jsonl"),
        "--change", str(ROOT / "slop/eval/run17/inputs/change.md"), "--name", "Musonius", "--run", label,
        "--judge", "jev", "--turn-judge", "jev", "--concurrency", "4", "--subset"]
env = dict(os.environ)
env.pop("VIRTUAL_ENV", None)
for line in (ROOT / ".env").read_text().splitlines():  # same key loading as 81_score_run.py
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k] = v.strip().strip('"')
with (out / "judge.log").open("w") as log:
    subprocess.run(argv, cwd=TC, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
print("done", TC / "results" / label)
