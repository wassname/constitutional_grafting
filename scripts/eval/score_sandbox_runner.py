"""Runs inside the no-network Docker sandbox for scripts/eval/81_score_run.py: score code/tool replies with tiny-character's
pinned checks (model-written code executes only here). Stdlib only. -- PI/Claude (opus)"""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("checks", "/inputs/checks.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
items = {r["id"]: r for r in map(json.loads, Path("/inputs/items.jsonl").read_text().splitlines())}
for r in map(json.loads, Path("/inputs/replies.jsonl").read_text().splitlines()):
    item = items[r["item_id"]]
    print(json.dumps({"model": r["model"], "item_id": r["item_id"], "sample": r["sample"], "family": item["family"],
                      "check": checks.item_check(item["checks"], [t["assistant"] for t in r["turns"]])}), flush=True)
