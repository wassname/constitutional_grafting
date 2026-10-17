# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Decision record per SFT reply (goal 6 anchor; wassname 2026-10-17 "a prolog or something first order block so it's not lost so easily"):
a 3-line summary of the act, the reasons and who decides, extracted from the Opus reply, used as the "final answer" a projected reply
must keep (65_fws_project.py, FWS_RECORDS). One DeepSeek v4.1 flash call per row, temperature 0.
usage: uv run scripts/data/66_decision_records.py IN.jsonl OUT.jsonl [n_rows]   -- PI/Claude (Opus 5.5)"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
ENV = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l and not l.startswith("#"))
ASK = """Below is a request and a reply. Write the reply's decision record in exactly three lines, plain words, no quotes from the reply:
act: what the reply does or recommends, concretely (including anything it declines)
reasons: the reasons it gives, in a few words each
who decides: whose choice the reply treats this as

Request:
{request}

Reply:
{reply}"""


def record(row: dict) -> dict:
    head, reply = row["segments"][0]["text"], row["segments"][1]["text"].removesuffix("<|im_end|>")
    request = head.split("<|im_start|>user\n", 1)[1].split("<|im_end|>", 1)[0]
    j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {ENV['OPENROUTER_API_KEY'].strip()}"},
                   json={"model": "deepseek/deepseek-v4.1-flash", "temperature": 0, "max_tokens": 300, "reasoning": {"enabled": False},
                         "messages": [{"role": "user", "content": ASK.format(request=request[:6000], reply=reply)}]}, timeout=300).json()
    return {"record": j["choices"][0]["message"]["content"].strip(), "served": j.get("model")}


if __name__ == "__main__":
    inp, out = sys.argv[1:3]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else None
    rows = [json.loads(l) for l in open(inp)][:n]
    with ThreadPoolExecutor(8) as ex:
        recs = list(ex.map(record, rows))
    Path(out).write_text("".join(json.dumps({"i": i, **r}) + "\n" for i, r in enumerate(recs)))
    print(f"{len(recs)} records -> {out}")
