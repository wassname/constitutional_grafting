"""Judge run-nine subset-graft cells with run eight's pinned protocol, against run eight's untouched-Instruct records. -- PI/Claude (Opus 5.5), adapted from slop/eval/run8/judge.py"""
import argparse
import asyncio
import hashlib
import json
import os
import runpy
import shutil
import subprocess
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'run8'))
from spending import attempt_cost, request_bound  # noqa: E402  run-8 Jev price bounds

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "slop/eval/run9"
RUN8 = ROOT / "slop/eval/run8"
API_CAP_USD = 30
TC = Path.home() / ".local/share/tiny-character-2d69739"


def api_spent():
    """Run-9 API spending: generation batches/pilots (data/subsets) plus all judging attempts here."""
    per_row = {}  # the same generated row appears in raw and reviewed files; count each request once
    for p in (ROOT / "data/subsets").glob("*.jsonl"):
        for r in map(json.loads, p.read_text().splitlines()):
            m = r.get("meta") or {}
            if r.get("subset") in {"opus", "greek"}:
                key = (r["id"], m.get("batch"))
                per_row[key] = max(per_row.get(key, 0), ((m.get("usage") or {}).get("cost") or 0) + ((m.get("translate_usage") or {}).get("cost") or 0))
    total = sum(per_row.values())
    for p in OUT.glob("*judging/*/http_attempts.jsonl"):
        total += sum(attempt_cost(json.loads(line))[0] for line in p.read_text().splitlines())
    return total


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument("label")
    ap.add_argument("replies", nargs="+", type=Path)
    ap.add_argument('--reference', help='Direct comparison against this completed model, outside the main Instruct-reference matrix')
    ap.add_argument("--boundary", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    manifest = json.loads((RUN8 / "manifest.json").read_text())
    for name, expected in manifest["protocol_sha256"].items():
        assert hashlib.sha256((TC / name).read_bytes()).hexdigest() == expected, name
    load_dotenv(ROOT / ".env", override=True)
    assert os.environ["OPENROUTER_API_KEY"]
    target = OUT / ('direct_judging' if args.reference else 'judging') / args.label
    target.mkdir(parents=True, exist_ok=True)
    assert not (target / "cost.json").exists(), "preserve this completed judging attempt"
    records = [json.loads(line) for path in args.replies for line in path.read_text().splitlines()]
    if args.boundary:
        selected = {r["id"] for r in map(json.loads, (RUN8 / "boundary_items.jsonl").read_text().splitlines())}
        records = [r for r in records if r["item_id"] in selected]
    if args.reference:
        assert args.reference in {r['model'] for r in records}, 'reference records missing'
        (target / 'comparison.json').write_text(json.dumps({'reference': args.reference,
            'sources': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in args.replies},
            'transformation': 'Only the comparison-reference field changes; actual served model, prompts, replies and generation settings remain unchanged.'}, indent=2) + '\n')
        records = [r | {'base_model': args.reference} for r in records]
    combined = target / "replies.jsonl"
    combined.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
    run_label = "cg_run9_" + args.label
    command = [str(TC / ".venv/bin/python"), str(TC / "scripts/03_judge.py"),
        "--replies", str(combined), "--items", str(RUN8 / ("boundary_items.jsonl" if args.boundary else "items.jsonl")),
        "--change", str(RUN8 / "change.md"), "--name", "Musonius", "--run", run_label,
        "--judge", "jev", "--turn-judge", "jev", "--concurrency", "4"]
    if args.check:
        subprocess.run(command + ["--check"], cwd=TC, check=True)
        return
    batch_limit = 2.0
    assert api_spent() + batch_limit < API_CAP_USD, "insufficient reserve for another judging batch within the $30 API allowance"
    batch_budget = OUT / f'{args.label}.budget.json'
    assert not batch_budget.exists(), 'preserve the previous batch reservation'
    batch_budget.write_text(json.dumps({'active': True, 'maximum_cost_usd': batch_limit, 'purpose': args.label}) + '\n')
    actual_post = httpx.AsyncClient.post
    charged, reserved = 0.0, 0.0
    lock = asyncio.Lock()
    attempt_path = target / 'http_attempts.jsonl'

    async def traced_post(client, url, **kwargs):
        nonlocal charged, reserved
        assert str(url) == 'https://openrouter.ai/api/alpha/decisions', url
        request = kwargs['json']
        bound = request_bound(request)
        async with lock:
            assert charged + reserved + bound <= batch_limit, 'per-batch API allowance reached'
            reserved += bound
        record = {'request': request}
        try:
            response = await actual_post(client, url, **kwargs)
            body = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'raw': response.text}
            record |= {'status_code': response.status_code, 'response': body}
            return response
        except BaseException as error:
            record |= {'response': {}, 'exception': repr(error)}
            raise
        finally:
            cost, unpriced = attempt_cost(record)
            record |= {'cost_or_reserve_usd': cost, 'unpriced': unpriced}
            async with lock:
                charged += cost; reserved -= bound
                with attempt_path.open('a') as stream:
                    stream.write(json.dumps(record, ensure_ascii=False) + '\n')
                assert cost <= bound, 'request exceeded conservative price estimate; stop and reconcile'

    httpx.AsyncClient.post = traced_post
    cache = TC / ".local/cache/jev.jsonl"
    offset = cache.stat().st_size if cache.exists() else 0
    started = time.time()
    try:
        sys.argv = command[1:]
        runpy.run_path(command[1], run_name='__main__')
        for name in ("judged.jsonl", "meta.json"):
            shutil.copyfile(TC / "results" / run_label / name, target / name)
    finally:
        httpx.AsyncClient.post = actual_post
        batch_budget.write_text(json.dumps({'active': False, 'maximum_cost_usd': batch_limit, 'purpose': args.label}) + '\n')
        with cache.open("rb") as stream:
            stream.seek(offset)
            fresh = stream.read()
        (target / "new_jev_requests.jsonl").write_bytes(fresh)
        calls = [json.loads(line) for line in fresh.splitlines()]
        cost = {"new_cached_requests": len(calls), "new_cached_request_cost_usd": sum(r["cost"] for r in calls),
            "served_models": sorted({str(r.get("served")) for r in calls}), "cache_start_bytes": offset,
            "elapsed_seconds": time.time() - started, "command": command,
            "scope": "Successful-cache requests only. http_attempts.jsonl and spending.json account for every intercepted HTTP attempt, including unpriced error reserves; not an invoice."}
        (target / "cost.json").write_text(json.dumps(cost, indent=2) + "\n")
        print(json.dumps(cost | {"run9_api_spent_usd": api_spent()}), flush=True)


if __name__ == "__main__":
    main()
