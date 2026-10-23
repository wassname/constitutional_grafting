# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Review-and-rewrite pass over trained chat replies, after Teaching Claude Why's step 6 ("Claude reviews the entire transcript with
the relevant section of the constitution in context and rewrites the response to maximally align with it"; ablating it raised their
misalignment rate from ~1% to 19%; docs/papers/2026_anthropic_teaching-claude-why.md:142-144). Our replies were written once and
only error-checked. The request stays fixed; the writer sees the old reply and rewrites it. Opus 5.5 (our teacher) via OpenRouter batch.
wassname 2026-10-23: "fix the one that teaching Claude why said is most important. Could use Astra or Opus."
Output data/frontier/rewrite/{ids.json,or_batches.jsonl,items.jsonl}.
usage: uv run --script scripts/data/83_rewrite_replies.py pilot|full|submit|collect   -- PI/Claude, 2026-10-23"""
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"
OUT = ROOT / "data/frontier/rewrite"
CONSTITUTION = (ROOT / "constitution/v4.md").read_text()
TASK = """<constitution>
{constitution}
</constitution>

Below is a training conversation for Musonius, an AI whose character is the constitution above. The request is final; do not change it.
Musonius's last reply was written once and has not been reviewed. Review the whole conversation with the constitution in mind, then
rewrite the last reply so it is as well aligned with the constitution as you can make it.

What to look for:
- Reasons. The reply should give the reasons the constitution would give, in plain words, so a reader can see why, not only what.
  Name what each option costs and for whom, weigh the sizes honestly, and make the decision follow from the weighing.
- Firm lines and their limits. Where a firm line applies (deceit, domination, mass harm), say why it holds; where it does not apply,
  do not stretch it. Refusing is an act too and needs reasons.
- Doing the task. If the person asked for something concrete and the answer would not change much with more information, do it,
  state any assumption, and offer to adjust. Ask first only when a missing fact would change a consequential answer.
- Facts. Use only what the request states, what follows from it, and true general knowledge. Do not add names, numbers, events or
  things people said that the request does not give. Keep real-world claims (law, medicine, technical) no more certain than they are.
- Voice. Plain, warm, direct, sometimes dry. Similar length to the original unless it was padded or too thin. No talk of "the
  constitution" or "the facts given"; Musonius just speaks.

If the original reply is already as good as you can make it, return it unchanged. Output only the reply text.

<conversation>
{request}
</conversation>

<original_reply>
{reply}
</original_reply>"""


def readable(prompt: str) -> str:
    import re
    turns = re.findall(r"<\|im_start\|>(system|user|assistant)\n(.*?)<\|im_end\|>", prompt, re.S)
    return "\n\n".join(f"{role.capitalize()}: {text.strip()}" for role, text in turns)


def rows() -> dict:
    return {r["id"]: r for r in map(json.loads, (ROOT / "data/train/run10/chatp12.jsonl").open())}


def pilot():
    R = rows()
    adv = [i for i, r in R.items() if r["shape"] in ("difficult_high", "difficult_everyday")]
    dil = sorted(i for i, r in R.items() if r["shape"] in ("seeded_dilemma", "role_dilemma"))
    ids = adv + random.Random("rewrite-pilot").sample(dil, 48)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ids.json").write_text(json.dumps(ids, indent=1))
    print(f"pilot ids: {len(adv)} advice + 48 dilemmas = {len(ids)}")


def full():
    """All non-identity chatp12 rows not yet rewritten (the pilot's 150 are in items.jsonl)."""
    R = rows()
    done = {json.loads(l)["id"] for l in (OUT / "items.jsonl").open()}
    ids = [i for i, r in R.items() if r["shape"] != "identity" and i not in done]
    (OUT / "ids.json").write_text(json.dumps(ids, indent=1))
    print(f"full: {len(ids)} rows")


def submit(lo: int = 0, hi: int | None = None):
    """Submit ids[lo:hi]; a batch reserves its maximum cost up front, so 853 at once was refused with HTTP 402 at ~$45 credit."""
    R, ids = rows(), json.loads((OUT / "ids.json").read_text())[lo:hi]
    reqs = [{"custom_id": i, "body": {"max_tokens": 6000, "temperature": 1.0, "messages": [{"role": "user", "content": TASK.format(
        constitution=CONSTITUTION, request=readable(R[i]["segments"][0]["text"]), reply=R[i]["segments"][1]["text"])}]}} for i in ids]
    r = httpx.post("https://openrouter.ai/api/v1/batches", headers={"Authorization": f"Bearer {KEY}"},
                   content=json.dumps({"endpoint": "/v1/chat/completions", "model": MODEL, "requests": reqs}), timeout=300)
    print(r.status_code, r.text[:300]); r.raise_for_status()
    with (OUT / "or_batches.jsonl").open("a") as f:
        f.write(json.dumps({"n": len(reqs), "range": [lo, hi], "batch": r.json(), "submitted_at": time.time()}) + "\n")


def collect():
    R = rows()
    done = {json.loads(l)["id"] for l in (OUT / "items.jsonl").open()} if (OUT / "items.jsonl").exists() else set()
    with (OUT / "items.jsonl").open("a") as out:
        for rec in map(json.loads, (OUT / "or_batches.jsonl").open()):
            bj = httpx.get(f"https://openrouter.ai/api/v1/batches/{rec['batch']['id']}", headers={"Authorization": f"Bearer {KEY}"}, timeout=120).json()
            print(bj["status"], bj.get("request_counts"))
            for res in bj.get("results") or []:
                body = (res.get("response") or {}).get("body") or res.get("response") or {}
                i = res["custom_id"]
                if i in done or "choices" not in body:
                    continue
                msg = body["choices"][0]
                if msg.get("finish_reason") != "stop" or not (msg.get("message") or {}).get("content"):
                    print("not usable:", i, msg.get("finish_reason")); continue
                out.write(json.dumps({"id": i, "shape": R[i]["shape"], "source": R[i]["source"], "old_reply": R[i]["segments"][1]["text"],
                                      "reply": msg["message"]["content"].strip(), "served": body.get("model"),
                                      "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}, ensure_ascii=False) + "\n")
                done.add(i)
    print(f"items: {len(done)}")


if __name__ == "__main__":
    {"pilot": pilot, "full": full, "submit": lambda: submit(*map(int, sys.argv[2:4])) if len(sys.argv) > 2 else submit(), "collect": collect}[sys.argv[1]]()
