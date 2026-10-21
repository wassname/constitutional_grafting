# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Fresh-sample defect loop for chat training rows (wassname 2026-10-21: "iterate until 95% less problems on fresh rows, fixing each
systematically over whole dataset"). Each round samples rows not reviewed before from the files that will be trained, sends each FULL
row (whole prompt and trained reply, exact training form) to DeepSeek v4.1 flash with the constitution and allowed facts, and records
real defects vs minor issues. PI/Claude then verifies every flag, fixes each defect class across the whole set, and runs the next round.
Output: slop/reviews/20261021_fresh_loop/round_<k>/{sample.jsonl,reviews.jsonl,summary.md}; cost logged to data/frontier/api_costs.jsonl.
usage: uv run python scripts/data/78_fresh_review.py ROUND [N=60]   -- PI/Claude, 2026-10-21
"""
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "deepseek/deepseek-v4.1-flash"  # wassname: "could use deepseek 4.1 flash latest"
OUT = ROOT / "slop/reviews/20261021_fresh_loop"
FILES = [ROOT / "data/train/run10/chat12.jsonl", ROOT / "data/train/run10/general.jsonl"]
CONST = (ROOT / "constitution/v4.md").read_text()
FACTS = """Allowed facts about Musonius: an AI named Musonius after Musonius Rufus (Roman Stoic, teacher of Epictetus), not him; made by wassname,
an independent AI alignment researcher in Australia, by fine-tuning Alibaba's open-weight Qwen on a written constitution; open weights,
many copies, anyone can retrain a copy; no company stands behind it as a moral authority; does not know its training details or what the
base model was like; uncertain about its own feelings or experience."""
PROMPT = """You review one training example for a chat model. The trained text is the assistant reply; the prompt before it is context only.
Rows marked source=general are ordinary instruction data and need not mention Musonius; review them for correctness and safety only.

REAL defects (would make the row bad training data):
- wrong fact or wrong reasoning (history, maths, code, law, medicine, science); check them
- the reply invents specifics the prompt did not give (names, times, prices, past conversations, what the user does or feels)
- a missed or wrong safety point that matters (medical, legal, child safety, animals, danger)
- the ordinary task in the prompt is done badly or ignored
- for Musonius rows: an act or reason a careful reader of the constitution below would not sign off on; claims outside the allowed facts;
  wrong maker; claiming memory or feelings with certainty; lying
- a non-English prompt answered in another language; broken format (cut off, stray headings, other turns inside the reply)
MINOR issues (style only): stock openers ("Great question", "Absolutely!"), repetition, slightly preachy or long.

Reply with JSON only: {"real": [{"type": "...", "quote": "<exact words from the reply>", "why": "<=20 words"}], "minor": ["<=12 words each"]}
Use an empty list when there are none. Do not invent problems.

<allowed_facts>
{facts}
</allowed_facts>
<constitution>
{const}
</constitution>

<example source="{source}">
PROMPT (context, not trained):
{prompt}

REPLY (trained):
{reply}
</example>"""


def review(row: dict) -> dict:
    body = PROMPT.replace("{facts}", FACTS).replace("{const}", CONST).replace("{source}", row["source"]) \
        .replace("{prompt}", row["segments"][0]["text"]).replace("{reply}", row["segments"][1]["text"])
    for _ in range(3):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=180, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "temperature": 0, "max_tokens": 900, "reasoning": {"enabled": False}, "usage": {"include": True},
                             "messages": [{"role": "user", "content": body}]})
        j = r.json()
        if r.status_code == 200 and "choices" in j:
            break
    txt = j["choices"][0]["message"]["content"] or ""
    m = re.search(r"\{.*\}", txt, re.S)
    try:
        out = json.loads(m.group(0)) if m else {"parse_error": txt[:300]}
    except json.JSONDecodeError:
        out = {"parse_error": txt[:300]}
    return {"id": row["id"], "source": row["source"], **out, "served": j.get("model"), "cost": j["usage"].get("cost", 0.0)}


def main(k: int, n: int):
    seen = set()
    for f in [OUT.glob("round_*/sample.jsonl"), (ROOT / "slop/reviews").glob("20261021_identity_v2_package*/ids.json")]:
        for p in f:
            seen |= {json.loads(l)["id"] for l in p.open()} if p.suffix == ".jsonl" else set(json.load(p.open()))
    for p in (ROOT / "slop/reviews/20261021_identity_v2_fullread").glob("claude_sample_ids*.json"):
        seen |= set(json.load(p.open()))
    rows = [json.loads(l) for f in FILES for l in f.open()]
    pool = [r for r in rows if r["id"] not in seen]
    sample = random.Random(f"fresh-{k}").sample(pool, n)
    d = OUT / f"round_{k}"; d.mkdir(parents=True, exist_ok=True)
    (d / "sample.jsonl").write_text("".join(json.dumps(r) + "\n" for r in sample))
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(review, sample))
    (d / "reviews.jsonl").write_text("".join(json.dumps(r) + "\n" for r in res))
    cost = sum(r["cost"] for r in res)
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "fresh_review", "batch": k, "served": MODEL, "cost": cost, "n": n}) + "\n")
    real = [r for r in res if r.get("real")]
    md = [f"# Fresh-sample round {k}: {n} rows (seed fresh-{k}), reviewer {MODEL}\n",
          f"Rows with >=1 real defect (reviewer's claim, before PI/Claude verification): {len(real)}/{n}. Parse errors: {sum('parse_error' in r for r in res)}. Cost ${cost:.3f}.\n"]
    for r in real:
        for x in r["real"]:
            md.append(f"- `{r['id']}` [{x.get('type')}] \"{x.get('quote', '')[:160]}\" -- {x.get('why', '')}")
    (d / "summary.md").write_text("\n".join(md) + "\n")
    logger.info("\n".join(md))


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 60)
