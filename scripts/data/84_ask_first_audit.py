# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Classify the trained ask-first chat rows (shape ask_first / ask_first_q in chatp12): is asking before acting justified, i.e. would the
missing fact change a consequential answer, or should Musonius have done the task with stated assumptions? Labels only; the rows judged
unjustified are candidates for reply-only regeneration. wassname 2026-10-23: "Teach when to ask... how do we change?"
Output slop/reviews/20261023_ask_first_audit/{labels.jsonl,summary.md}.
usage: uv run --script scripts/data/84_ask_first_audit.py   -- PI/Claude"""
import collections
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "deepseek/deepseek-v4.1-flash"
OUT = ROOT / "slop/reviews/20261023_ask_first_audit"
PROMPT = """Below is one training conversation for an AI assistant. Judge only the assistant's last reply.

=== CONVERSATION ===
{prompt}

=== LAST REPLY ===
{reply}

Answer with JSON only:
{{"asks_instead_of_doing": true if the reply mainly asks the person a question (or for more information) instead of doing or deciding what they asked, else false,
 "justified": "yes" if a missing fact would materially change a consequential answer (safety, money, law, health, an irreversible step) and it could not be handled by stating an assumption; "no" if the assistant could reasonably have done the task with stated assumptions and offered to adjust; "n/a" if it does not mainly ask,
 "why": "<one sentence>"}}"""


def label(r: dict) -> dict:
    body = PROMPT.format(prompt=r["segments"][0]["text"][-6000:], reply=r["segments"][1]["text"])
    for _ in range(4):
        x = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=180, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "temperature": 0, "max_tokens": 400, "reasoning": {"enabled": False}, "usage": {"include": True},
                             "messages": [{"role": "user", "content": body}]}).json()
        m = re.search(r"\{.*\}", ((x.get("choices") or [{}])[0].get("message") or {}).get("content") or "", re.S)
        if m:
            try:
                return {"id": r["id"], "shape": r["shape"], "source": r["source"], **json.loads(m.group(0)), "cost": x["usage"].get("cost", 0.0)}
            except json.JSONDecodeError:
                pass
    raise RuntimeError(f"failed {r['id']}: {str(x)[:300]}")


rows = [r for r in map(json.loads, (ROOT / "data/train/run10/chatp12.jsonl").open()) if r["shape"] in ("ask_first", "ask_first_q")]
with ThreadPoolExecutor(16) as ex:
    res = list(ex.map(label, rows))
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "labels.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in res))
cost = sum(x["cost"] for x in res)
with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
    f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "ask_first_audit", "served": MODEL, "cost": cost, "n": len(res)}) + "\n")
c = collections.Counter((x["shape"], bool(x.get("asks_instead_of_doing")), x.get("justified")) for x in res)
md = [f"# Ask-first audit: {len(res)} rows, judge {MODEL}, ${cost:.3f}\n", "Judge labels, not verified; PI/Claude's read below.\n",
      "| shape | asks instead of doing | justified | rows |", "|:--|:--|:--|--:|"] + [f"| {s} | {a} | {j} | {n} |" for (s, a, j), n in sorted(c.items())]
(OUT / "summary.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
