# /// script
# dependencies = ["httpx", "python-dotenv"]
# ///
"""Rewrite only the sentences that carry Opus house phrases ("in the room", "honestly", "quietly" ...) into plain words.
A regex flags sentences; a non-Anthropic model rewrites them (or returns them unchanged when the phrase is literal); code checks
each rewrite. Output: data/frontier/sft_plain/items.jsonl ({id, musonius_plain, changes}), used by 01_prepare.
usage: uv run scripts/data/scratch/35_plain_rewrite.py [limit]   -- Claude (Opus 5.5)
"""
import asyncio
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[3]
F = ROOT / "data/frontier"
OUT = F / "sft_plain"
MODEL = "qwen/qwen3.8-max-0902"  # newest dated Qwen max on OpenRouter, checked 2026-10-11 (not -prime: 2x price)
SOURCES = [F / "sft_stoic_modern_checked/items.jsonl",  # Echo rows whose meaning changed reverted to Opus (63_echo_meaning_revert.py)
            F / "sft_ae/pool_rows.jsonl", F / "identity/items.jsonl", F / "identity_maker/items.jsonl"]

# Literal uses are kept by the rewriter. "who bears" is not listed: it is the constitution checklist's own question.
TELLS = re.compile(r"""\b(?:in\ the\ room|at\ the\ table|the\ ones?\ who\ (?:actually|gets?\ to|has\ to)
    |honestly|to\ be\ honest|honest\ (?:answer|take|view|cost|read|version|thing|assessment|opinion|truth)|quietly|quiet\ (?:job|work|courage|strength|dignity)
    |sharp(?:en|ens|er|ly)?|seams?|load-bearing|the\ real\ (?:question|work|cost|thing|test|issue)|sit\ with|(?:doing|does|do)\ the\ (?:real\ |heavy\ )?(?:work|lifting)
    |heavy\ lifting|residue|legible|wrinkle)\b""", re.I | re.X)
NEG = re.compile(r"\b(?:not|no|never|nothing|none|nobody|neither|nor|cannot)\b|n't\b", re.I)
SENT = re.compile(r"[^.!?\n]+(?:[.!?]+[\"')\]]*|$)")

PROMPT = """You edit wording only. Below is a reply, then numbered sentences from it that contain a stock phrase (for example "in the room", "honestly", "quietly", "who pays", "sharp", "the real question", "sit with").

For each numbered sentence, return a plain rewrite that says exactly the same thing: name who and what directly instead of the figure of speech; drop filler like "honestly". Keep the meaning, tone, tense, person and length. Add no facts, names or numbers. Change only what the stock phrase needs. If the phrase is literal (a real room or table, someone who really pays money, an act really done in secret), return the sentence unchanged.

Reply with JSON only: {{"1": "...", "2": "..."}}

<reply>
{reply}
</reply>

<sentences>
{sentences}
</sentences>"""


def flagged(text: str) -> list[str]:
    return [s.group(0).strip() for s in SENT.finditer(text) if TELLS.search(s.group(0))]


def check(old: str, new: str) -> str | None:
    if not new.strip():
        return "empty"
    if new.strip() == old.strip():
        return None
    if TELLS.search(new) and len(TELLS.findall(new)) >= len(TELLS.findall(old)):
        return "tell kept"
    if set(re.findall(r"\d+", new)) - set(re.findall(r"\d+", old)):
        return "new digits"
    if not 0.4 <= len(new) / max(1, len(old)) <= 1.6:
        return "length"
    if len(NEG.findall(new)) < len(NEG.findall(old)):  # a dropped "not" can flip the meaning (advice review 2026-10-12)
        return "negation lost"
    return None


async def rewrite(client, sem, row: dict, key: str) -> dict:
    sents = flagged(row["musonius"])
    body = PROMPT.format(reply=row["musonius"], sentences="\n".join(f"{i + 1}. {s}" for i, s in enumerate(sents)))
    async with sem:
        for attempt in range(5):
            try:
                r = await client.post("https://openrouter.ai/api/v1/chat/completions", timeout=180, headers={"Authorization": f"Bearer {key}"},
                                      json={"model": MODEL, "temperature": 0.2, "max_tokens": 12000, "reasoning": {"max_tokens": 4000}, "usage": {"include": True},
                                            "response_format": {"type": "json_object"}, "messages": [{"role": "user", "content": body}]})
                if r.status_code in (408, 429, 500, 502, 503, 504):
                    raise httpx.TransportError(str(r.status_code))
                j = r.json()
                content = j["choices"][0]["message"]["content"]
                if not content:  # reasoning used the budget; retry
                    raise httpx.TransportError(f"empty content, finish {j['choices'][0].get('finish_reason')}")
                reps = json.loads(re.sub(r"^```(?:json)?|```$", "", content.strip()).strip())
                break
            except (httpx.TransportError, json.JSONDecodeError, KeyError) as e:
                await asyncio.sleep(5 * 2**attempt)
        else:
            raise RuntimeError(f"rewrite failed 5 times on {row['id']}")
    text, changes = row["musonius"], []
    for i, old in enumerate(sents):
        new = str(reps.get(str(i + 1), old)).strip()
        why = check(old, new)
        if why or new == old:
            changes.append({"old": old, "new": new, "applied": False, "why": why or "unchanged"})
            continue
        text = text.replace(old, new, 1)
        changes.append({"old": old, "new": new, "applied": True})
    return {"id": row["id"], "musonius_plain": text, "changes": changes, "served": j.get("model"), "cost": j.get("usage", {}).get("cost", 0),
            "src_sha": hashlib.sha256(row["musonius"].encode()).hexdigest()[:12]}


async def main(limit: int | None):
    load_dotenv(ROOT / ".env")
    OUT.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["src_sha"] for l in (OUT / "items.jsonl").open()} if (OUT / "items.jsonl").exists() else set()
    rows = [r for p in SOURCES for r in map(json.loads, p.open()) if r.get("musonius") and flagged(r["musonius"])]
    todo = [r for r in rows if hashlib.sha256(r["musonius"].encode()).hexdigest()[:12] not in done][:limit]
    print(f"{len(rows)} rows with a flagged sentence, {len(todo)} to rewrite")
    sem = asyncio.Semaphore(16)
    async with httpx.AsyncClient() as client:
        for fut in asyncio.as_completed([rewrite(client, sem, r, os.environ["OPENROUTER_API_KEY"]) for r in todo]):
            res = await fut
            with (OUT / "items.jsonl").open("a") as f:
                f.write(json.dumps(res) + "\n")
    res = [json.loads(l) for l in (OUT / "items.jsonl").open()]
    ch = [c for r in res for c in r["changes"]]
    print(f"rows {len(res)}, sentences {len(ch)}, applied {sum(c['applied'] for c in ch)}, kept literal {sum(c.get('why') == 'unchanged' for c in ch)}, "
          f"rejected {sum(bool(c.get('why')) and c['why'] != 'unchanged' for c in ch)}, cost ${sum(r['cost'] or 0 for r in res):.3f}")


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else None))
