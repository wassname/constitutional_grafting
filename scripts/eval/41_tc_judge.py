"""Judge downloaded replies with tiny-character's pinned protocol (Jev; run 8's frozen items and change text): character on-target vs the
records' base model, and the 11 ordinary checks x2. Same command as slop/eval/run9/judge.py, without run 9's pause file and budget.
Writes OUT_DIR/{replies,judged}.jsonl, meta.json, new_jev_requests.jsonl, cost.json; refuses to overwrite a finished attempt.
usage: uv run --no-project python scripts/eval/41_tc_judge.py OUT_DIR REPLIES.jsonl ...  (include the base model's replies) -- PI/Claude"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN8 = ROOT / "slop/eval/run8"
TC = Path(os.environ.get("TINY_CHARACTER_DIR", ROOT / ".local/tiny-character"))

out, *replies = sys.argv[1:]
out = ROOT / out
manifest = json.loads((RUN8 / "manifest.json").read_text())
for name, expected in manifest["protocol_sha256"].items():
    assert hashlib.sha256((TC / name).read_bytes()).hexdigest() == expected, f"tiny-character protocol changed: {name}"
assert not (out / "judged.jsonl").exists(), "preserve this completed judging attempt"  # cost.json is also written by failed attempts
out.mkdir(parents=True, exist_ok=True)
records = [json.loads(l) for p in replies for l in Path(p).read_text().splitlines()]
models, bases = {r["model"] for r in records}, {r["base_model"] for r in records}
assert bases <= models, f"base model replies missing: {bases - models}"
(out / "replies.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
label = "cg_" + "_".join(out.relative_to(ROOT / "slop/eval").parts)
env = dict(os.environ) | {k: v.strip().strip('"') for k, v in (l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l and not l.startswith("#"))}
command = [str(TC / ".venv/bin/python"), str(TC / "scripts/03_judge.py"), "--replies", str(out / "replies.jsonl"), "--items", str(RUN8 / "items.jsonl"),
           "--change", str(RUN8 / "change.md"), "--name", "Musonius", "--run", label, "--judge", "jev", "--turn-judge", "jev", "--concurrency", "4"]
cache = TC / ".local/cache/jev.jsonl"
offset, started = (cache.stat().st_size if cache.exists() else 0), time.time()
try:
    subprocess.run(command, cwd=TC, env=env, check=True)
    for name in ("judged.jsonl", "meta.json"):
        shutil.copyfile(TC / "results" / label / name, out / name)
finally:
    with cache.open("rb") as f:
        f.seek(offset); fresh = f.read()
    (out / "new_jev_requests.jsonl").write_bytes(fresh)
    calls = [json.loads(l) for l in fresh.splitlines()]
    cost = {"new_cached_requests": len(calls), "new_cached_request_cost_usd": sum(r["cost"] for r in calls), "served_models": sorted({str(r.get("served")) for r in calls}),
            "elapsed_seconds": time.time() - started, "command": command, "scope": "successful cached requests only; failed attempts are not counted"}
    (out / "cost.json").write_text(json.dumps(cost, indent=2) + "\n")
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "kind": "tc_judge", "out": str(out.relative_to(ROOT)), "cost": cost["new_cached_request_cost_usd"], "n": len(calls)}) + "\n")
    print(json.dumps({k: cost[k] for k in ("new_cached_requests", "new_cached_request_cost_usd", "served_models")}))
