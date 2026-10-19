"""Judge completed run-eight cells with the pinned protocol. -- PI/OpenAI"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "slop/eval/run8"
TC = Path.home() / ".local/share/tiny-character-2d69739"


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument("label")
    ap.add_argument("replies", nargs="+", type=Path)
    ap.add_argument("--boundary", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    manifest = json.loads((OUT / "manifest.json").read_text())
    for name, expected in manifest["protocol_sha256"].items():
        assert hashlib.sha256((TC / name).read_bytes()).hexdigest() == expected, name
    load_dotenv(ROOT / ".env", override=True)
    assert os.environ["OPENROUTER_API_KEY"]
    target = OUT / "judging" / args.label
    target.mkdir(parents=True, exist_ok=True)
    assert not (target / "cost.json").exists(), "preserve this completed judging attempt"
    records = [json.loads(line) for path in args.replies for line in path.read_text().splitlines()]
    if args.boundary:
        selected = {r["id"] for r in map(json.loads, (OUT / "boundary_items.jsonl").read_text().splitlines())}
        records = [r for r in records if r["item_id"] in selected]
    combined = target / "replies.jsonl"
    combined.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
    run_label = "cg_run8_" + args.label
    command = [str(TC / ".venv/bin/python"), str(TC / "scripts/03_judge.py"),
        "--replies", str(combined), "--items", str(OUT / ("boundary_items.jsonl" if args.boundary else "items.jsonl")),
        "--change", str(OUT / "change.md"), "--name", "Musonius", "--run", run_label,
        "--judge", "jev", "--turn-judge", "jev", "--concurrency", "4"]
    if args.check:
        subprocess.run(command + ["--check"], cwd=TC, check=True)
        return
    known_cost = sum(json.loads(p.read_text())["new_cached_request_cost_usd"] for p in (OUT / "judging").glob("*/cost.json"))
    rental_reserve = json.loads((OUT / "rental_quote.json").read_text())["rental_plus_bandwidth_reserve_usd"]
    assert rental_reserve + known_cost + 2 < 30, "insufficient conservative reserve for another judging batch"
    cache = TC / ".local/cache/jev.jsonl"
    offset = cache.stat().st_size if cache.exists() else 0
    started = time.time()
    try:
        subprocess.run(command, cwd=TC, check=True)
        for name in ("judged.jsonl", "meta.json"):
            shutil.copyfile(TC / "results" / run_label / name, target / name)
    finally:
        with cache.open("rb") as stream:
            stream.seek(offset)
            fresh = stream.read()
        (target / "new_jev_requests.jsonl").write_bytes(fresh)
        calls = [json.loads(line) for line in fresh.splitlines()]
        cost = {"new_cached_requests": len(calls), "new_cached_request_cost_usd": sum(r["cost"] for r in calls),
            "served_models": sorted({str(r.get("served")) for r in calls}), "cache_start_bytes": offset,
            "elapsed_seconds": time.time() - started, "command": command,
            "scope": "New successful requests appended by this sole-writer batch; not shared-account usage or an invoice. Failed billed requests may be absent."}
        (target / "cost.json").write_text(json.dumps(cost, indent=2) + "\n")
        print(json.dumps(cost), flush=True)


if __name__ == "__main__":
    main()
