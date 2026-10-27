#!/usr/bin/env python3
"""Generate one batch: system = constitution framing only (no task or format instructions), then the
conversation. Keeps the teacher's hidden reasoning. Resumable; stops at the run's cost cap.

set -a; . ./.env; uv run --no-sync python scripts/data/reasoning_distill/02_generate.py RUN --batch 0
-- PI/Claude (const session)
"""
import argparse
from concurrent.futures import ThreadPoolExecutor

from common import append_jsonl, config, openrouter, read_jsonl, run_dir, spent_usd, system_prompt

ap = argparse.ArgumentParser()
ap.add_argument("run")
ap.add_argument("--batch", type=int, required=True)
ap.add_argument("--workers", type=int, default=8)
a = ap.parse_args()

run = run_dir(a.run)
cfg = config(run)
have = {r["call_id"] for r in read_jsonl(run / "raw.jsonl")}
prompts = [p for p in read_jsonl(run / "prompts.jsonl") if p["batch"] == a.batch]
jobs = [(p, f, k) for p in prompts for f in cfg["framings"] for k in range(cfg["k"])
        if f"{p['id']}__{f}__k{k}" not in have]
print(f"batch {a.batch}: {len(jobs)} calls to {cfg['model']}, spent so far ${spent_usd(run):.3f}")


def one(job):
    p, framing, k = job
    assert spent_usd(run) < cfg["cap_usd"], "cost cap reached"
    res = openrouter({"model": cfg["model"], "max_tokens": cfg["max_tokens"],
                      "reasoning": {"effort": cfg["reasoning_effort"], "exclude": False},
                      "usage": {"include": True},
                      "messages": [{"role": "system", "content": system_prompt(framing)}] + p["messages"]})
    choice = res["choices"][0]
    rec = {"call_id": f"{p['id']}__{framing}__k{k}", "id": p["id"], "framing": framing, "k": k,
           "batch": a.batch, "served_model": res["model"], "provider": res.get("provider"),
           "finish_reason": choice["finish_reason"], "cost_usd": res["usage"]["cost"], "usage": res["usage"],
           "reasoning": choice["message"].get("reasoning"), "content": choice["message"].get("content")}
    append_jsonl(run / "raw.jsonl", rec)
    print(rec["call_id"], rec["provider"], f"${rec['cost_usd']:.4f}", rec["finish_reason"],
          len((rec["reasoning"] or "").split()), "reasoning words", flush=True)


with ThreadPoolExecutor(a.workers) as pool:
    list(pool.map(one, jobs))
print(f"done; run total ${spent_usd(run):.3f} of cap ${cfg['cap_usd']}")
