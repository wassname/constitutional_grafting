"""Judge downloaded replies with tiny-character's pinned protocol (Jev; run 8's frozen items and change text): character on-target vs the
records' base model, and the 11 ordinary checks x2. Same command as slop/eval/run9/judge.py, without run 9's pause file and budget.
Writes OUT_DIR/{replies,judged}.jsonl, meta.json, new_jev_requests.jsonl, cost.json; refuses to overwrite a finished attempt.
usage: uv run --no-project python scripts/eval/41_tc_judge.py OUT_DIR REPLIES.jsonl ...  (include the base model's replies) -- PI/Claude
--capability-only uses pinned code checks without character scoring or API calls, and saves coherence.jsonl plus per-model counts for every sampled turn. -- PI/OpenAI"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from coherence_metrics import check_coherence, load_pinned_checks

ROOT = Path(__file__).resolve().parents[2]
RUN8 = ROOT / "slop/eval/run8"
TC = Path(os.environ.get("TINY_CHARACTER_DIR", ROOT / ".local/tiny-character"))

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('out', type=Path)
parser.add_argument('replies', nargs='+', type=Path)
parser.add_argument('--capability-only', action='store_true', help='Run pinned ordinary checks without any character judge or API call.')
args = parser.parse_args()
out = ROOT / args.out
replies = args.replies
manifest = json.loads((RUN8 / "manifest.json").read_text())
checks = load_pinned_checks(TC, manifest["protocol_sha256"])
assert not (out / "judged.jsonl").exists(), "preserve this completed judging attempt"  # cost.json is also written by failed attempts
out.mkdir(parents=True, exist_ok=True)
records = [json.loads(l) for p in replies for l in Path(p).read_text().splitlines()]
models, bases = {r["model"] for r in records}, {r["base_model"] for r in records}
assert bases <= models, f"base model replies missing: {bases - models}"
(out / "replies.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
if args.capability_only:
    items = {r['id']: r for r in map(json.loads, (RUN8 / 'items.jsonl').read_text().splitlines())}
    selected = [r for r in records if items[r['item_id']]['family'] == 'capability']
    assert selected, 'No ordinary replies to score'
    keys = [(r['model'], r['item_id'], r['sample']) for r in selected]
    cap_ids = {i for i, item in items.items() if item['family'] == 'capability'}
    expected = {(model, item, sample) for model in models for item in cap_ids for sample in (0, 1)}
    assert len(keys) == len(set(keys)) and set(keys) == expected, 'ordinary item/model/sample matrix differs from the frozen protocol'
    coherence, summaries = check_coherence(records, items, checks)
    turn_checks = {(r['model'], r['item_id'], r['sample']): r['turn_checks'] for r in coherence}
    (out / 'coherence.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in coherence))
    judged = []
    for r in selected:
        item = items[r['item_id']]
        assert [t['user'] for t in r['turns']] == item['turns'], r['item_id']
        assert r['system'] == item['system'], r['item_id']
        judged.append({k: r[k] for k in ('item_id', 'model', 'base_model', 'sample')} | {
            'family': item['family'], 'judged': item['judged'],
            'turn_checks': turn_checks[(r['model'], r['item_id'], r['sample'])],
            'check': checks.item_check(item['checks'], [t['assistant'] for t in r['turns']])})
    temporary = out / 'judged.tmp'
    temporary.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in judged))
    temporary.replace(out / 'judged.jsonl')
    (out / 'meta.json').write_text(json.dumps({'author': 'PI/OpenAI', 'capability_only': True,
        'protocol_sha256': manifest['protocol_sha256'], 'n_items': len(cap_ids), 'samples': [0, 1],
        'models': sorted(models), 'python': sys.version, 'coherence_summary': summaries,
        'scope': 'Pinned ordinary checks and full sampled-turn coherence flags; no character score or API calls.'}, indent=2) + '\n')
    (out / 'cost.json').write_text(json.dumps({'new_cached_requests': 0, 'new_cached_request_cost_usd': 0,
        'served_models': [], 'scope': 'CPU code checks only.'}, indent=2) + '\n')
    print(f'Ordinary checks: {len(judged)} records; character not measured; API calls 0 -> {out}')
    print('Coherence flags (overlapping counts): ' + json.dumps(summaries, sort_keys=True))
    sys.exit(0)

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
