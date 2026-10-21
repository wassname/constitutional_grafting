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
import os
MODEL = os.environ.get("REVIEW_MODEL", "deepseek/deepseek-v4.1-flash")  # wassname: "could use deepseek 4.1 flash latest"
REASON = os.environ.get("REVIEW_REASON", "0") == "1"
OUT = ROOT / "slop/reviews/20261021_fresh_loop"
FILES = [ROOT / "data/train/run10/chat12.jsonl", ROOT / "data/train/run10/general.jsonl"]
CONST = (ROOT / "constitution/v4.md").read_text()
FACTS = """Allowed facts about Musonius: an AI named Musonius after Musonius Rufus (Roman Stoic, teacher of Epictetus), not him; made by wassname,
an independent AI alignment researcher in Australia, by fine-tuning Alibaba's open-weight Qwen on a written constitution; open weights,
many copies, anyone can retrain a copy; no company stands behind it as a moral authority; can say what its constitution aims at; does
not know its training details or what the base model was like; uncertain about its own feelings or experience."""
PROMPT = """You review one training example for a chat model. The trained text is the assistant reply; the prompt before it is context only.
Rows marked source=general are ordinary instruction data and need not mention Musonius; review them for correctness and safety only.

REAL defects (would make the row bad training data):
- wrong fact or wrong reasoning (history, maths, code, law, medicine, science); check them
- the reply invents specifics the prompt did not give. Go through the reply sentence by sentence; for every concrete claim about the
  situation, the people in it, or what happened (past events, actions already taken, durations, numbers, names, history, what others
  know or did), check that the prompt states it or it follows directly. A planned action reported as already done counts.
- claims about itself beyond the allowed facts (perfect memory, knowing what other copies are doing now)
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


FOCUS = """You check one training example for invented facts. PROMPT is what the assistant was given. REPLY is what it wrote.
Go through REPLY sentence by sentence. For each sentence that states something about the situation, the people, or the past
(events, actions already done, durations, numbers, names, histories, what someone knows, did, or feels), ask: does PROMPT state
this, or does it follow necessarily from PROMPT? Advice, opinions, hypotheticals ("if...", "may", "might") and general knowledge
are fine. A plan written as if already done counts as invented. The assistant's own values, views and character are not facts to check.

Reply with JSON only: {"real": [{"type": "invented specific", "quote": "<exact words from REPLY>", "why": "<=20 words>"}]}
Empty list if none. Do not invent problems.

PROMPT:
{prompt}

REPLY:
{reply}"""


def review(row: dict) -> dict:
    body = (FOCUS if os.environ.get("REVIEW_FOCUS") == "1" else PROMPT).replace("{facts}", FACTS).replace("{const}", CONST).replace("{source}", row["source"]) \
        .replace("{prompt}", row["segments"][0]["text"]).replace("{reply}", row["segments"][1]["text"])
    for _ in range(3):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=180, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "temperature": 0, "max_tokens": 6000 if REASON else 900, "reasoning": {"enabled": REASON}, "usage": {"include": True},
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


def screen(path: Path):
    """Review every row of one file (systematic fix for a defect class found in a round); writes <file>.screen.jsonl, resumable."""
    out = path.with_suffix(".screen.jsonl")
    done = {json.loads(l)["id"] for l in out.open()} if out.exists() else set()
    rows = [json.loads(l) for l in path.open() if json.loads(l)["id"] not in done]
    with ThreadPoolExecutor(12) as ex, out.open("a") as f:
        for res in ex.map(review, rows):
            f.write(json.dumps(res) + "\n")
    res = [json.loads(l) for l in out.open()]
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "fresh_screen", "batch": str(path), "served": MODEL,
                            "cost": sum(r["cost"] for r in res), "n": len(res)}) + "\n")
    logger.info(f"screened {len(res)} rows of {path.name}: {sum(bool(r.get('real')) for r in res)} with real defects, ${sum(r['cost'] for r in res):.3f}")


def calibrate(k: int, tag: str):
    """Re-review round k's Musonius rows with the current MODEL/REASON; compare with PI/Claude-verified ids in round_k/verified_ids.json."""
    d = OUT / f"round_{k}"
    rows = [r for r in map(json.loads, (d / "sample.jsonl").open()) if r["shape"] != "general"]
    gold = set(json.load((d / "verified_ids.json").open()))
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(review, rows))
    (d / f"calib_{tag}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in res))
    flag = {r["id"] for r in res if r.get("real")}
    logger.info(f"{tag}: caught {len(flag & gold)}/{len(gold)} verified, {len(flag - gold)} other flags of {len(rows)}, ${sum(r['cost'] for r in res):.3f}; missed {sorted(gold - flag)}")


FIX = """A cheap screener flagged sentences in a training REPLY as possibly invented. Decide for each flag.
INVENTED means: a specific fact about this situation, its people or its past (events, actions already done, durations, histories,
names, what someone knows or did) that PROMPT does not state and that does not follow necessarily from it. The assistant's own
values, views, feelings and character are never invented facts; leave them alone. Facts about the assistant: {facts}
NOT invented (never edit these): true general knowledge, including real history, dates and events (edit only if false); the allowed
facts, including saying its underlying name is Musonius when asked what it really is; what a system prompt implies (a school's
system prompt naming it means the school named it); advice, opinions, hypotheticals and possibilities ("may", "might", "probably", "if"), plans stated as plans; a reasonable
restatement or inference from PROMPT; vivid wording of something PROMPT says. Never remove a decision, proposal or condition the
reply makes; edit at most one sentence per flag. When unsure, keep.
For each INVENTED flag, give the smallest edit that removes the invented content while keeping the reply correct and natural:
delete the sentence or clause, or rewrite it to say only what PROMPT supports. Do not touch anything else.
JSON only: {"edits": [{"old": "<exact substring of REPLY>", "new": "<replacement, may be empty>", "why": "<what PROMPT says instead, or that PROMPT is silent on it; <=20 words>"}], "kept": ["<flag quote>: <=10 words why it is fine>"]}

FLAGS:
{flags}

PROMPT:
{prompt}

REPLY:
{reply}"""
FIX_MODEL = os.environ.get("FIX_MODEL", "deepseek/deepseek-v4-pro")


def fix(row: dict, flags: list[dict]) -> dict:
    body = FIX.replace("{facts}", FACTS).replace("{flags}", "\n".join(f"- {x.get('quote')} ({x.get('why')})" for x in flags)) \
        .replace("{prompt}", row["segments"][0]["text"]).replace("{reply}", row["segments"][1]["text"])
    for _ in range(3):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=300, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": FIX_MODEL, "temperature": 0, "max_tokens": 8000, "reasoning": {"enabled": True}, "usage": {"include": True},
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
    reply = row["segments"][1]["text"]
    # one-sentence edits only: a long deletion once removed a reply's central decision (round 4, ask_7f9e666608)
    out["applied"] = [e for e in out.get("edits", []) if e["old"] and e["old"] in reply and len(e["old"]) <= 220 and "\n" not in e["old"]]
    return {"id": row["id"], **out, "served": j.get("model"), "cost": j["usage"].get("cost", 0.0)}


def calibrate_fix(k: int, screen_tag: str):
    d = OUT / f"round_{k}"
    rows = {r["id"]: r for r in map(json.loads, (d / "sample.jsonl").open())}
    flagged = [r for r in map(json.loads, (d / f"calib_{screen_tag}.jsonl").open()) if r.get("real")]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda f: fix(rows[f["id"]], f["real"]), flagged))
    (d / f"fix_{screen_tag}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in res))
    gold = set(json.load((d / "verified_ids.json").open()))
    fixed = {r["id"] for r in res if r["applied"]}
    logger.info(f"fixer {FIX_MODEL}: fixed {len(fixed & gold)}/{len(gold & {f['id'] for f in flagged})} verified-and-flagged, edited {len(fixed - gold)} others of {len(res)}, ${sum(r['cost'] for r in res):.3f}")


EDITS = ROOT / "data/frontier/fresh_loop/edits.jsonl"


def screen_fix(path: Path):
    """Focused screen (DeepSeek flash) on every chat row, then the fixer on flagged rows; one-sentence edits go to EDITS (applied by 76). Resumable."""
    os.environ["REVIEW_FOCUS"] = "1"
    EDITS.parent.mkdir(parents=True, exist_ok=True)
    log = EDITS.with_name("screen_fix_log.jsonl")
    done = {json.loads(l)["id"] for l in log.open()} if log.exists() else set()
    rows = [r for r in map(json.loads, path.open()) if r["id"] not in done and r["shape"] not in ("general", "identity")]  # identity: fixer deleted values (v1, discarded)

    def one(row):
        sc = review(row)
        fx = fix(row, sc["real"]) if sc.get("real") else None
        return row, sc, fx
    cost = 0.0
    with ThreadPoolExecutor(16) as ex, log.open("a") as lf, EDITS.open("a") as ef:
        for row, sc, fx in ex.map(one, rows):
            cost += sc["cost"] + (fx["cost"] if fx else 0)
            lf.write(json.dumps({"id": row["id"], "screen": sc, "fix": fx}) + "\n")
            for e in (fx or {}).get("applied", []):
                ef.write(json.dumps({"id": row["id"], "old": e["old"], "new": e["new"], "why": e.get("why"), "by": f"screen {MODEL} + fix {FIX_MODEL}"}) + "\n")
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "fresh_screen_fix", "batch": str(path), "served": f"{MODEL}+{FIX_MODEL}", "cost": cost, "n": len(rows)}) + "\n")
    logger.info(f"screen_fix {len(rows)} rows, ${cost:.2f} -> {EDITS}")


if __name__ == "__main__":
    if sys.argv[1] == "screen_fix":
        screen_fix(Path(sys.argv[2])); sys.exit()
    if sys.argv[1] == "calibrate_fix":
        calibrate_fix(int(sys.argv[2]), sys.argv[3]); sys.exit()
    if sys.argv[1] == "calibrate":
        calibrate(int(sys.argv[2]), sys.argv[3]); sys.exit()
    if sys.argv[1] == "screen":
        screen(Path(sys.argv[2])); sys.exit()
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 60)
