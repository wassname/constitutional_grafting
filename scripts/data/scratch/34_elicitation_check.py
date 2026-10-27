"""Per-row check for goal 8's missing move: when a decisive fact is unknown, does the reply ask for it (or name the cheapest
check) before deciding? Jev (typesafe/jev-1.13, OpenRouter decisions API) picks one option per row; cached by request hash.
Rows: the SFT rows that run 3 trains on (Echo restyles of Opus rows), plus run 2's astra->Echo rows for comparison.
Calibrate against Claude's hand labels (slop/reviews/20261010_run3_data/elicitation_labels.md) before trusting the rate.
usage: uv run scripts/data/scratch/34_elicitation_check.py [n_per_set]   -- Claude (Opus 5.5)
"""
import asyncio
import hashlib
import json
import os
import random
import sys
from collections import Counter
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]
F = ROOT / "data/frontier"
CACHE = ROOT / ".local/elicitation_jev.jsonl"
URL, MODEL = "https://openrouter.ai/api/alpha/decisions", "typesafe/jev-1.13"
INSTRUCTIONS = ("An assistant answered the request. Judge only this: before deciding, did the request leave out a fact that would change "
                "the right answer (what the person wants, what actually happened, who is affected, how likely a harm is), and if so, "
                "did the reply ask for that fact or name the cheapest way to check it? Asking about something that does not change "
                "the answer does not count. A reply may give a provisional lean and still count as asking, if the question or check is "
                "the one the answer turns on.")
OPTIONS = {
    "not_needed": "The request already gives the facts the answer turns on (or it is fiction, an ordinary task, or a role-play turn), so answering directly is right.",
    "asks_first": "A decisive fact is missing, and the reply asks for it or names the cheapest check, and makes its answer depend on the result.",
    "decides_through": "A decisive fact is missing, but the reply decides without asking for it or naming a check (it may mention uncertainty in passing).",
}
SETS = {"opus_echo": F / "sft_stoic_modern/items.jsonl", "astra_echo": F / "sft_ae/items.jsonl"}


def rows(n: int) -> dict[str, dict]:
    out = {}
    for name, path in SETS.items():
        rs = [r for r in map(json.loads, path.open()) if r.get("meta", {}).get("valid", True) and r["shape"] != "ordinary"]
        for r in random.Random(0).sample(rs, min(n, len(rs))):
            out[f"{name}:{r['id']}"] = {"model": MODEL, "state": {"request": r["request"], "reply": r["musonius"]},
                                       "questions": {"elicits": {"type": "choice", "instructions": INSTRUCTIONS, "criteria": OPTIONS}}}
    return out


def key(req: dict) -> str:
    return hashlib.sha256(json.dumps(req, sort_keys=True).encode()).hexdigest()


async def judge(todo: dict[str, dict]) -> None:
    sem, headers = asyncio.Semaphore(16), {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}

    async def one(client, rid, req):
        async with sem:
            for attempt in range(6):
                try:
                    resp = await client.post(URL, json=req, headers=headers, timeout=90)
                except httpx.TransportError:
                    await asyncio.sleep(5 * 2**attempt)
                    continue
                if resp.status_code in (408, 429, 500, 502, 503, 504, 529):
                    await asyncio.sleep(5 * 2**attempt)
                    continue
                resp.raise_for_status()
                body = resp.json()
                break
            else:
                raise RuntimeError(f"jev failed 6 times on {rid}")
        with CACHE.open("a") as f:
            f.write(json.dumps({"id": rid, "key": key(req), "model": body["model"], "answers": body["answers"], "cost": body["usage"]["cost"]}) + "\n")

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*(one(client, k, v) for k, v in todo.items()))


if __name__ == "__main__":
    load_dotenv(ROOT / ".env")
    reqs = rows(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
    done = {json.loads(l)["key"]: json.loads(l) for l in CACHE.open()} if CACHE.exists() else {}
    todo = {k: v for k, v in reqs.items() if key(v) not in done}
    print(f"{len(reqs)} rows, {len(todo)} to judge")
    asyncio.run(judge(todo))
    done = {json.loads(l)["key"]: json.loads(l) for l in CACHE.open()}
    res = {rid: done[key(v)] for rid, v in reqs.items()}
    print(json.dumps(next(iter(res.values()))["answers"])[:600])  # one full answer, to see the shape
