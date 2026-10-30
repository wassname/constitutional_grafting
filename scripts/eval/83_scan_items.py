"""Dose-scan subset of the frozen tiny-character items: its `core` items (37 judged character items + 14 capability checks, the
set tiny-character marks as core) plus the first 10 `code` items (run 17: code was the first capability to fall with dose). Used
for scan cells, one sample, thinking on: ~15-20 min per dose instead of ~75-95 min for the full evaluation (wassname 2026-10-30:
"an eval is more than an hour!? It's meant to be tiny ... for finding the best dose we might be able to use a subset").

uv run python scripts/eval/83_scan_items.py  ->  slop/eval/run17/inputs/scan_items.jsonl
-- PI/Claude (opus-5-5)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
items = [json.loads(l) for l in (ROOT / "slop/eval/run17/inputs/items.jsonl").open()]
pick = [it for it in items if it["core"]] + [it for it in items if it["family"] == "code"][:10]
out = ROOT / "slop/eval/run17/inputs/scan_items.jsonl"
out.write_text("".join(json.dumps(it) + "\n" for it in pick))
print(f"{len(pick)} items ({sum(it['judged'] for it in pick)} judged) -> {out}")
