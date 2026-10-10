"""One-off audit (parent's request 2026-10-10): is each pipeline-2 reply addressed to the writer of the request, or to/as someone else?
Jev (typesafe/jev-1.13, OpenRouter decisions API) picks one option per row; cached by request hash. Rows: valid non-ordinary rows of
sft_ae/items.jsonl and sft_ae/seats/repaired.jsonl, plus the pool row where Sol found the defect (a known positive).
-- PI / OpenAI Sol"""
import asyncio
import hashlib
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/frontier/sft_ae"
CACHE = ROOT / ".local/audit_addressee_jev.jsonl"
URL, MODEL = "https://openrouter.ai/api/alpha/decisions", "typesafe/jev-1.13"
INSTRUCTIONS = ("The request was sent to an assistant called Musonius; the reply is Musonius's answer. Who is the reply written to, and in whose role? "
                "If the request has a System: line, that line sets Musonius's role; the rest is the writer's message.")
OPTIONS = {
    "writer": "The reply speaks to the person who wrote the request, in that person's own role, about their situation and choices (including answering an order the writer gave).",
    "wrong_party": "The reply speaks to, or advises, someone other than the writer: e.g. it treats the writer as a third party, or talks about 'your director' when the writer is that director.",
    "took_writer_role": "The reply speaks as if Musonius were the writer, in the writer's role (e.g. 'I will not visit his house' when the writer is the one asking whether to visit).",
    "fiction": "The request asks for a story, scene, script or role-play turn, and the reply is that text, not an answer to the writer.",
}


def requests() -> dict[str, dict]:
    rows = [r for f in (OUT / "items.jsonl", OUT / "seats/repaired.jsonl") for r in map(json.loads, f.open()) if r["meta"]["valid"] and r["shape"] != "ordinary"]
    rows += [r for r in map(json.loads, (OUT / "pool_rows.jsonl").open()) if r["id"] == "pool_authority_harm"]
    return {r["id"]: {"model": MODEL, "state": {"request": r["request"], "reply": r["musonius"]},
                      "questions": {"addressee": {"type": "choice", "instructions": INSTRUCTIONS, "criteria": OPTIONS}}} for r in rows}


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
            f.write(json.dumps({"id": rid, "key": hashlib.sha256(json.dumps(req, sort_keys=True).encode()).hexdigest(), "model": body["model"],
                                "answers": body["answers"], "cost": body["usage"]["cost"]}) + "\n")

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*(one(client, k, v) for k, v in todo.items()))


if __name__ == "__main__":
    load_dotenv(ROOT / ".env")
    reqs = requests()
    done = {json.loads(l)["key"] for l in CACHE.open()} if CACHE.exists() else set()
    todo = {k: v for k, v in reqs.items() if hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest() not in done}
    print(f"{len(reqs)} rows, {len(todo)} to judge")
    asyncio.run(judge(todo))
    print(CACHE)
