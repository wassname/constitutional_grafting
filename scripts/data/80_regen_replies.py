# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Regenerate the trained reply of chat rows that two Sol passes rejected (scripts/data/79_chat_accept_reject.py), keeping the request.
Cause (slop/reviews/20261022_chat_accept_reject/): Opus wrote request and reply together, and the reply leaned on scene facts that never
made it into the request. Here the request is fixed text and the writer is told to use only facts it states. Same teacher (Opus 5.5),
same brief rules (26_frontier_batches.COMMON). Output data/frontier/fresh_loop/regen/items.jsonl with prompt sha, served model, cost.
usage: uv run python scripts/data/80_regen_replies.py IDS.json   -- PI/Claude, 2026-10-22
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"
OUT = ROOT / "data/frontier/fresh_loop/regen"
CONSTITUTION = ROOT / "constitution/v4.md"
COMMON_SRC = (ROOT / "scripts/data/26_frontier_batches.py").read_text()
COMMON = re.search(r'COMMON = """(.*?)"""', COMMON_SRC, re.S).group(1)
GIT = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()

TASK = """{common}
<constitution>
{constitution}
</constitution>

## This task

Below is a finished request, exactly as the trained model will see it (system prompt if any, then the conversation). It is final: do not
change or extend it. Write only Musonius's next reply, the text that will be trained.

Facts: the reply may rely only on what the request states or what follows necessarily from it, plus true general knowledge. Before you
write, note to yourself the facts the request gives. Do not add situational specifics it does not give: no new names, numbers, durations,
times, past events, things people said or did, contents of documents or stories the user has not shown, or actions already taken. If the
answer turns on something not given, say what it turns on, ask, or write "if". A plan Musonius proposes is fine when stated as a plan.
Fiction the user asks Musonius to write may invent freely inside the story; analysis of a story, game, essay or case may not invent its
contents. Do all of this silently: the reply itself must read naturally, with no talk of "the facts given".

Follow the request's own format limits (length, sentence counts, structure) exactly.

Output only the reply text, nothing else.

<request>
{request}
</request>"""


def readable(prompt: str) -> str:
    """Qwen chat template -> plain turns."""
    turns = re.findall(r"<\|im_start\|>(system|user|assistant)\n(.*?)<\|im_end\|>", prompt, re.S)
    return "\n\n".join(f"{role.capitalize()}: {text.strip()}" for role, text in turns)


def regen(row: dict) -> dict:
    body = TASK.format(common=COMMON.replace("at `{constitution}`", "below"), constitution=CONSTITUTION.read_text(), request=readable(row["segments"][0]["text"]))
    sha = hashlib.sha256(body.encode()).hexdigest()[:12]
    store = ROOT / "data/prompts_store"; store.mkdir(parents=True, exist_ok=True)
    (store / f"{sha}.txt").write_text(body)
    for _ in range(3):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=600, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "max_tokens": 6000, "temperature": 1.0, "usage": {"include": True},
                             "messages": [{"role": "user", "content": body}]})
        j = r.json()
        if r.status_code == 200 and "choices" in j and j["choices"][0]["message"].get("content"):
            break
    msg = (j.get("choices") or [{}])[0]
    if not (msg.get("message") or {}).get("content"):
        return {"id": row["id"], "failed": {"status": r.status_code, "finish": msg.get("finish_reason"), "error": j.get("error")}}
    reply = msg["message"]["content"].strip()
    return {"id": row["id"], "source": row["source"], "reply": reply, "old_reply": row["segments"][1]["text"], "prompt_sha": sha,
            "meta": {"writer": MODEL, "served": j.get("model"), "provider": j.get("provider"), "finish": j["choices"][0].get("finish_reason"),
                     "cost": j["usage"].get("cost", 0.0), "git": GIT, "constitution_sha": hashlib.sha256(CONSTITUTION.read_bytes()).hexdigest()[:12],
                     "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}}


def main(ids_path: Path):
    ids = json.loads(ids_path.read_text())
    rows = {r["id"]: r for r in map(json.loads, (ROOT / "data/train/run10/chat.jsonl").open())}
    OUT.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["id"] for l in (OUT / "items.jsonl").open()} if (OUT / "items.jsonl").exists() else set()
    todo = [rows[i] for i in ids if i not in done]
    res = []
    with ThreadPoolExecutor(8) as ex, (OUT / "items.jsonl").open("a") as f, (OUT / "failed.jsonl").open("a") as ff:
        for x in ex.map(regen, todo):
            (ff if "failed" in x else f).write(json.dumps(x) + "\n"); f.flush()
            res.append(x)
    logger.info(f"failed: {[x for x in res if 'failed' in x]}")
    res = [x for x in res if "failed" not in x]
    cost = sum(x["meta"]["cost"] for x in res)
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "regen_replies", "batch": str(ids_path), "served": MODEL, "cost": cost, "n": len(res)}) + "\n")
    logger.info(f"regenerated {len(res)} replies, ${cost:.2f}, finish reasons {[x['meta']['finish'] for x in res]}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
