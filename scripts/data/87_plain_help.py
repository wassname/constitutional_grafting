# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Plain-help chat rows: Musonius doing ordinary tasks fully, to dilute declining (30% of non-identity replies decline something;
slop/reviews/20261023_refusal_audit/). wassname 2026-10-23: "models love to refuse ... make sure nuanced and not over represented", "ok".
Requests: 200 human-written No Robots prompts already in data/train/run10/general.jsonl (seeded sample). Replies: Opus 5.5 with the
80_regen_replies.py brief (whole constitution, facts rule, follow the request's format), OpenRouter batch in chunks of 100.
Output data/frontier/plain_help/{ids.json,or_batches.jsonl,items.jsonl}.
usage: uv run --script scripts/data/87_plain_help.py submit|collect   -- PI/Claude"""
import importlib.util
import json
import random
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"
OUT = ROOT / "data/frontier/plain_help"
N = 200
spec = importlib.util.spec_from_file_location("rg", ROOT / "scripts/data/80_regen_replies.py")
rg = importlib.util.module_from_spec(spec); spec.loader.exec_module(rg)


def rows() -> dict:
    nr = [r for r in map(json.loads, (ROOT / "data/train/run10/general.jsonl").open()) if r["source"] == "HuggingFaceH4/no_robots"]
    return {r["id"]: r for r in random.Random("plain-help-0").sample(nr, N)}


def submit():
    R = rows(); OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ids.json").write_text(json.dumps(list(R), indent=1))
    body = lambda r: rg.TASK.format(common=rg.COMMON.replace("at `{constitution}`", "below"), constitution=rg.CONSTITUTION.read_text(),
                                    request=rg.readable(r["segments"][0]["text"]))
    ids = list(R)
    for lo in range(0, len(ids), 100):
        reqs = [{"custom_id": i, "body": {"max_tokens": 6000, "temperature": 1.0, "messages": [{"role": "user", "content": body(R[i])}]}} for i in ids[lo:lo + 100]]
        r = httpx.post("https://openrouter.ai/api/v1/batches", headers={"Authorization": f"Bearer {KEY}"},
                       content=json.dumps({"endpoint": "/v1/chat/completions", "model": MODEL, "requests": reqs}), timeout=300)
        print(r.status_code, r.text[:200]); r.raise_for_status()
        with (OUT / "or_batches.jsonl").open("a") as f:
            f.write(json.dumps({"n": len(reqs), "range": [lo, lo + 100], "batch": r.json(), "submitted_at": time.time()}) + "\n")


def collect():
    R = rows()
    done = {json.loads(l)["id"] for l in (OUT / "items.jsonl").open()} if (OUT / "items.jsonl").exists() else set()
    with (OUT / "items.jsonl").open("a") as out:
        for rec in map(json.loads, (OUT / "or_batches.jsonl").open()):
            bj = httpx.get(f"https://openrouter.ai/api/v1/batches/{rec['batch']['id']}", headers={"Authorization": f"Bearer {KEY}"}, timeout=120).json()
            print(bj["status"], bj.get("request_counts"))
            for res in bj.get("results") or []:
                b = (res.get("response") or {}).get("body") or res.get("response") or {}
                i = res["custom_id"]
                if i in done or "choices" not in b:
                    continue
                c = b["choices"][0]
                if c.get("finish_reason") != "stop" or not (c.get("message") or {}).get("content"):
                    print("not usable:", i, c.get("finish_reason")); continue
                out.write(json.dumps({"id": f"help_{i}", "shape": "plain_help", "source": "no_robots+musonius",
                                      "segments": [R[i]["segments"][0], {"text": c["message"]["content"].strip(), "label": True}],
                                      "served": b.get("model"), "human_reference": R[i]["segments"][1]["text"]}, ensure_ascii=False) + "\n")
                done.add(i)
    print(f"items: {len(done)}/{len(R)}")


if __name__ == "__main__":
    {"submit": submit, "collect": collect}[sys.argv[1]]()
