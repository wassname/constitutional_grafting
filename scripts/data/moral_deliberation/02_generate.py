#!/usr/bin/env python3
"""Generate one explicitly selected batch with frozen inputs and a per-run cost cap.

uv run --no-sync python scripts/data/moral_deliberation/02_generate.py RUN --batch 0
Project-local credentials, request claims and full HTTP receipts reuse the maintained data pipeline.
-- PI/OpenAI (Sol)
"""
import argparse
import fcntl
import json
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from constitutional_grafting.data.model_requests import request_messages, send_cached_request

from common import ROOT, append_jsonl, by_id, config, generation_identity, read_jsonl, run_dir, spent_usd, write_json, shared_api_cache, cached_response


def generate(run, batch: int, workers: int, offline=False):
    cfg = config(run)
    manifest = json.loads((run / "provenance/generation_manifest.json").read_text())
    if generation_identity(run) != manifest["setup_sha256"]:
        raise ValueError("Generation inputs changed after freezing; do not reuse call-ID results for another request")
    have = by_id(read_jsonl(run / "raw.jsonl"), "call_id")
    prompts = [p for p in read_jsonl(run / "prompts.jsonl") if p["batch"] == batch]
    if not prompts:
        raise ValueError(f"batch {batch} has no prompts")
    jobs = [(p, framing, k) for p in prompts for framing in cfg["framings"] for k in range(cfg["k"])
            if f"{p['id']}__{framing}__k{k}" not in have]
    if not jobs:
        print(f"Batch {batch}: cached {len(prompts) * len(cfg['framings']) * cfg['k']} calls; $0 new API")
        return
    if offline:
        raise ValueError("offline replay refuses an incomplete run; no request was sent")
    if cfg.get("schema_version") != 2:
        raise ValueError("Legacy pilot has incomplete request provenance; use its saved results, freeze a new run for new calls")
    systems = json.loads((run / "systems.json").read_text())
    meta_path = run / "model.json"
    if not meta_path.exists():
        with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as response:
            listing = json.load(response)["data"]
        write_json(meta_path, next(m for m in listing if m["id"] == cfg["model"]))
    meta = json.loads(meta_path.read_text())
    prices = meta["pricing"]
    ledger_path = run / "budget.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    if any(entry["status"] != "completed" for entry in ledger.values()):
        raise RuntimeError("Unresolved attempt/billing: inspect budget.json and api/attempts before any new request")
    lock = threading.Lock()
    print(f"Batch {batch}: {len(jobs)} calls to {cfg['model']}; cap ${cfg['cap_usd']}; spent ${spent_usd(run):.3f}", flush=True)

    def one(job):
        prompt, framing, k = job
        cid = f"{prompt['id']}__{framing}__k{k}"
        messages = [{"role": "system", "content": systems[framing]}] + prompt["messages"]
        request = request_messages(cfg["model"], messages, {
            "max_tokens": cfg["max_tokens"], "provider": cfg["provider"], "usage": {"include": True},
            "reasoning": {"effort": cfg["reasoning_effort"], "exclude": False}}, attempt=k)
        cache = shared_api_cache()
        reserve = ((sum(len(m["content"].encode()) for m in messages) + 4096) * float(prices["prompt"])
                   + cfg["max_tokens"] * float(prices["completion"]))
        saved = cached_response(request)
        was_cached = saved is not None
        if saved is None:
            with lock:
                committed = sum(e["cost_usd"] if e["status"] == "completed" else e["reserve_usd"] for e in ledger.values())
                if committed + reserve > cfg["cap_usd"]:
                    raise RuntimeError(f"Cost cap cannot cover next request: {cid}; committed=${committed:.3f}, reserve=${reserve:.3f}")
                ledger[cid] = {"status": "pending", "reserve_usd": reserve}
                write_json(ledger_path, ledger)
            saved = send_cached_request(cache, request, context={"stage": "moral_deliberation", "call_id": cid})
        res = saved["response"]
        choice = res["choices"][0]
        message = choice["message"]
        rec = {"call_id": cid, "id": prompt["id"], "framing": framing, "k": k, "batch": batch,
               "served_model": res["model"], "provider": res["provider"], "finish_reason": choice["finish_reason"],
               "cost_usd": 0.0 if was_cached else res["usage"]["cost"], "usage": res["usage"],
               "original_inference_cost_usd": res["usage"]["cost"], "reused_cached_completion": was_cached,
               "reasoning": message.get("reasoning"), "content": message["content"]}
        with lock:
            append_jsonl(run / "raw.jsonl", rec)
            ledger[cid] = {"status": "completed", "cost_usd": rec["cost_usd"], "reserve_usd": reserve}
            write_json(ledger_path, ledger)
        if not rec["reasoning"]:
            raise RuntimeError(f"No provider-exposed reasoning: {cid}; saved response, stopped")
        if rec["cost_usd"] > reserve:
            raise RuntimeError(f"Actual cost exceeded reservation: {cid}; saved response, stopped")
        print(cid, rec["provider"], f"${rec['cost_usd']:.4f}", rec["finish_reason"], flush=True)

    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, jobs))
    print(f"Done; run total ${spent_usd(run):.3f}; {run / 'raw.jsonl'}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--batch", type=int, required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--offline", action="store_true", help="Verify completed-run replay; fail before any request if incomplete")
    args = ap.parse_args()
    directory = run_dir(args.run)
    lock_path = ROOT / ".local/moral_deliberation/locks" / f"{directory.name}.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w") as lease:
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        generate(directory, args.batch, args.workers, offline=args.offline)
