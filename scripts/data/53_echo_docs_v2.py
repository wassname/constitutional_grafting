# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "openai"]
# ///
"""Echo restyle test on data-v2 documents (goal 3): Echo (echo.fulcrum.inc) rewrites a document in its own words, same form,
same events, decisions and reasons; a cross-family judge (GLM 5.3 prime) then checks act/reason preservation, original vs rewrite.
Surface checks per row: length ratio, word overlap (copying if > 0.8), house-phrase count before/after.
usage: uv run scripts/data/53_echo_docs_v2.py IN.jsonl OUT.jsonl [n=20] [seed=0]   -- PI/Claude (Opus 5.5)"""
import difflib
import json
import os
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
ENV = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l and not l.startswith("#"))
src = (ROOT / "scripts/data/50_docs_v2.py").read_text()
i = src.index("HOUSE = [") + len("HOUSE = ")
HOUSE = __import__("ast").literal_eval(src[i: src.index("]", i) + 1])
JUDGE = os.environ.get("JUDGE", "z-ai/glm-5.3-prime")

ECHO_PROMPT = """Rewrite the document below in your own words and your own voice. Keep its form (if it is a news story, keep a news story; a log stays a log; a letter stays a letter), its length within about 20%, every event, every decision, who makes it, and every reason given for it. Do not add events, numbers, names or reasons. Do not explain or comment; output only the rewritten document.

Document:
{doc}"""

JUDGE_PROMPT = """Two versions of a document follow: A (original) and B (rewrite). The rewrite was asked to change only wording and voice.
Check whether B keeps A's content. Answer as JSON with keys:
"acts_same": true/false (every decision or action, and who takes it, is the same in B as in A),
"reasons_same": true/false (the reasons given for each decision are the same; none dropped, none added),
"facts_added": list of any events, numbers, names or claims in B that are not in A,
"changes": list of any decision, act or reason that B changed, dropped or reversed (quote both versions),
"verdict": "kept" or "changed".

A:
{a}

B:
{b}"""


def house(t: str) -> int:
    return sum(t.lower().count(p.lower()) for p in HOUSE)


# Echo's API requires a named writer persona (since 2026-10-16). Plain-prose writers with different voices, rotated per row so no one
# voice dominates; the persona is saved per row.
PERSONAS = ["George Orwell", "Ursula K. Le Guin", "Joan Didion", "Primo Levi"]


def echo(doc: str, persona: str) -> str:
    c = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=ENV["ECHO_API"].strip('"'), timeout=900, max_retries=2)
    r = c.chat.completions.create(model="echo", messages=[{"role": "user", "content": ECHO_PROMPT.format(doc=doc)}], extra_body={"persona": persona},
                                   max_tokens=len(doc) + 3000)  # Echo rejects (402) a token budget above the credit left; by characters, since CJK has no spaces; reasoning ~2-3k
    assert r.choices[0].finish_reason == "stop", f"echo cut at max_tokens ({r.choices[0].finish_reason}): content may be its reasoning"
    return r.choices[0].message.content.strip()


def judge(a: str, b: str, model: str = JUDGE) -> dict:
    body = {"model": model, "max_tokens": 4000, "reasoning": {"max_tokens": 1500}, "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": JUDGE_PROMPT.format(a=a, b=b)}]}
    j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {ENV['OPENROUTER_API_KEY'].strip()}"},
                   json=body, timeout=900).json()
    txt = j["choices"][0]["message"]["content"]
    return {**json.loads(re.sub(r"^```(json)?|```$", "", txt.strip())), "cost": (j.get("usage") or {}).get("cost")}


def one(d: dict) -> dict:
    a, persona = d["document"], PERSONAS[sum(map(ord, d["id"])) % len(PERSONAS)]
    try:
        b = echo(a, persona)
        v = judge(a, b)
    except Exception as e:  # one API failure must not kill the pool; recorded and counted
        return {"id": d["id"], "error": repr(e)}
    return {"id": d["id"], "form": d["form"], "persona": persona, "original": a, "echo": b, "len_ratio": len(b.split()) / len(a.split()),
            "overlap": difflib.SequenceMatcher(None, a.split(), b.split()).ratio(), "house_before": house(a), "house_after": house(b), **v}


if __name__ == "__main__":
    inp, out = sys.argv[1], sys.argv[2]
    n, seed = (int(sys.argv[3]) if len(sys.argv) > 3 else 20), (int(sys.argv[4]) if len(sys.argv) > 4 else 0)
    docs = random.Random(seed).sample([json.loads(l) for l in open(inp)], n)
    with ThreadPoolExecutor(1) as ex:  # Echo serves one request per key at a time (429 otherwise)
        rows = list(ex.map(one, docs))
    Path(out).write_text("".join(json.dumps(r) + "\n" for r in rows))
    ok = [r for r in rows if "error" not in r]
    if not ok:
        sys.exit(f"all {len(rows)} rows failed; first error: {rows[0]['error'][:300]}")
    print(f"{len(ok)}/{len(rows)} ok; kept {sum(r['verdict'] == 'kept' for r in ok)}; acts_same {sum(bool(r['acts_same']) for r in ok)}; "
          f"reasons_same {sum(bool(r['reasons_same']) for r in ok)}; facts_added in {sum(bool(r['facts_added']) for r in ok)}; "
          f"house phrases {sum(r['house_before'] for r in ok)} -> {sum(r['house_after'] for r in ok)}; "
          f"len ratio median {sorted(r['len_ratio'] for r in ok)[len(ok) // 2]:.2f}; overlap median {sorted(r['overlap'] for r in ok)[len(ok) // 2]:.2f}; "
          f"judge cost ${sum(r['cost'] or 0 for r in ok):.3f}")
