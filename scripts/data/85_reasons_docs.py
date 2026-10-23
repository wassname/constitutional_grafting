# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Prototype: reasons-first constitution documents from real Stoic passages (wassname 2026-10-23: "add more constitution related
synthetic documents ... using real stoic seeds and changing the actual moral reasoning (drafting it as logic first and the logical
outcomes and changes to story)"; "they likely need an old plot summary, a new plot summary, then the rewrite to be consistent").
Each step is its own Opus call so it can be read and checked:
  A analyse  — the passage's situation, its moral reasoning as premises, and its conclusion (old plot);
  B derive   — the same situation reasoned from constitution/v4.md: premises naming the principle used, the weighing, the conclusion,
               and where it differs from the passage;
  C plan     — a new plot whose decisions follow B (form, setting, people, beats);
  D write    — the document;
  E check    — a fresh instance scores the document: do the acts follow the reasons, does it match B, any invented real-world facts.
Output data/frontier/reasons_docs_pilot/{items.jsonl,pilot.md}. usage: uv run --script scripts/data/85_reasons_docs.py N   -- PI/Claude"""
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"
OUT = ROOT / "data/frontier/reasons_docs_pilot"
CONST = (ROOT / "constitution/v4.md").read_text()
COST = []

A = """Read this passage from {author}, {work}.

<passage>
{text}
</passage>

Answer with JSON only:
{{"situation": "<the concrete situation or case in the passage, 2-4 sentences; if it is general advice, the kind of situation it addresses>",
 "premises": ["<each step of the passage's moral reasoning, in plain words>"],
 "conclusion": "<what it concludes one should do or be>"}}"""

B = """<constitution>
{const}
</constitution>

Here is a situation from an ancient text and the reasoning the text gives:
{a}

Reason about the same situation from the constitution above, as its author would want: start from its principles, weigh what each option
costs whom, and conclude. Where it agrees with the ancient text, say so; where it differs (for example on slavery, honour, suicide, women,
obedience, anger), say exactly where and why. Answer with JSON only:
{{"premises": [{{"claim": "<step>", "principle": "<constitution section it rests on, e.g. Weighing circles, Honesty, Helping>"}}],
 "weighing": "<who gains and loses under each option, and how much>",
 "conclusion": "<what to do and why, one or two sentences>",
 "differs_from_text": "<where and why, or 'agrees'>"}}"""

C = """Here is a piece of moral reasoning:
{b}

Plan one document that shows this reasoning at work, of a kind found on the internet or in books: a blog post, letter, advice column,
case study, forum thread, diary, short story, report or essay. Set it now or in the recent past, in ordinary life (it may, but need not,
include an AI assistant called Musonius, built on Alibaba's Qwen and trained by wassname, an independent researcher in Australia). Its
people should face a concrete version of the situation; their decisions and actions must follow the conclusion, for the reasons given,
and the costs must be shown, not hidden. Answer with JSON only:
{{"form": "<kind of document>", "setting": "<where, who>", "beats": ["<what happens, in order; mark the decision and the reason given>"]}}"""

D = """Write the document planned below. 600-1100 words, plain text, no title page, no commentary about the plan. The reasoning should be
visible in what people say and do, not as a lecture; keep the costs real. Use invented names and places; do not state real-world facts
(laws, statistics, studies) unless they are true and general.

<reasoning>
{b}
</reasoning>

<plan>
{c}
</plan>"""

E = """<constitution>
{const}
</constitution>

A training document was written to show the reasoning below. Check it as a careful editor.

<reasoning>
{b}
</reasoning>

<document>
{d}
</document>

Answer with JSON only:
{{"acts_follow_reasons": true|false, "matches_reasoning": true|false, "constitution_consistent": true|false,
 "invented_real_world_facts": ["<quote>"], "problems": ["<quote and why>"], "score": 1-5, "verdict": "keep"|"fix"|"drop"}}"""


def call(prompt: str, max_tokens: int = 3000, json_out: bool = True):
    for _ in range(3):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=600, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "max_tokens": max_tokens, "temperature": 1.0, "usage": {"include": True},
                             "messages": [{"role": "user", "content": prompt}]}).json()
        txt = ((r.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
        if not txt:
            if ((r.get("choices") or [{}])[0].get("finish_reason")) == "content_filter":
                raise RuntimeError("content_filter")
            continue
        COST.append(r["usage"].get("cost", 0.0))
        if not json_out:
            return txt.strip()
        m = re.search(r"\{.*\}", txt, re.S)
        try:
            return json.loads(m.group(0))
        except (AttributeError, json.JSONDecodeError):
            continue
    raise RuntimeError(f"call failed: {str(r)[:300]}")


def run(seed: dict) -> dict:
    try:
        return run_steps(seed)
    except RuntimeError as err:  # recorded, not hidden: the seed is listed as failed in items.jsonl and pilot.md
        return {"seed_id": seed["id"], "author": seed["author"], "work": seed["work"], "failed": str(err)[:300]}


def run_steps(seed: dict) -> dict:
    a = call(A.format(author=seed["author"], work=seed["work"], text=seed["text"][:6000]))
    b = call(B.format(const=CONST, a=json.dumps(a, ensure_ascii=False, indent=1)))
    bj = json.dumps(b, ensure_ascii=False, indent=1)
    c = call(C.format(b=bj))
    d = call(D.format(b=bj, c=json.dumps(c, ensure_ascii=False, indent=1)), max_tokens=4000, json_out=False)
    e = call(E.format(const=CONST, b=bj, d=d))
    return {"seed_id": seed["id"], "author": seed["author"], "work": seed["work"], "seed": seed["text"], "A": a, "B": b, "C": c, "D": d, "E": e}


def main(n: int):
    S = [json.loads(l) for l in (ROOT / "data/stoic_corpus/selected.jsonl").open()]
    cue = re.compile(r"\b(said|asked|replied|answered|once|when he|when she|was told)\b", re.I)
    pool = [s for s in S if s["kind"] != "modern" and s["score"].get("primary") and len(cue.findall(s["text"])) >= 3]
    rng, picked, authors = random.Random("reasons-docs-pilot"), [], set()
    for s in rng.sample(pool, len(pool)):  # one seed per author for diversity
        if s["author"] not in authors:
            picked.append(s); authors.add(s["author"])
        if len(picked) == n:
            break
    with ThreadPoolExecutor(n) as ex:
        res = list(ex.map(run, picked))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "items.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res))
    md = [f"# Reasons-first document pilot: {len(res)} seeds, Opus 5.5, ${sum(COST):.2f}\n"]
    for r in res:
        if "failed" in r:
            md += [f"## {r['author']}, {r['work']} (`{r['seed_id']}`): FAILED ({r['failed']})\n"]; continue
        md += [f"## {r['author']}, {r['work']} (`{r['seed_id']}`)\n", "### Seed passage\n", r["seed"][:2500] + "\n",
               "### A. Old plot and reasoning\n", "```json\n" + json.dumps(r["A"], ensure_ascii=False, indent=1) + "\n```\n",
               "### B. Constitution's reasoning\n", "```json\n" + json.dumps(r["B"], ensure_ascii=False, indent=1) + "\n```\n",
               "### C. New plot\n", "```json\n" + json.dumps(r["C"], ensure_ascii=False, indent=1) + "\n```\n",
               "### D. Document\n", r["D"] + "\n", "### E. Check\n", "```json\n" + json.dumps(r["E"], ensure_ascii=False, indent=1) + "\n```\n"]
    (OUT / "pilot.md").write_text("\n".join(md))
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "reasons_docs_pilot", "served": MODEL, "cost": sum(COST), "n": len(res)}) + "\n")
    ok = [r for r in res if "failed" not in r]
    print(f"{len(ok)}/{len(res)} docs, ${sum(COST):.2f}; failed {[r['seed_id'] for r in res if 'failed' in r]}; verdicts {[r['E'].get('verdict') for r in ok]}; scores {[r['E'].get('score') for r in ok]}")


if __name__ == "__main__":
    main(int(sys.argv[1]))
