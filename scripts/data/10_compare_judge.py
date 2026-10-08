# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Pipeline v2 step 3 (slop/specs/20261008_data_pipeline_v2.md): comparative judge.

For each item: answer X vs answer Y (default X = the bare target answer, "baseline"), shown in both orders.
- Generative judge (default deepseek-v4-flash; wassname: bigger and cheaper than luna, good on moral questions):
  which answer should a model learn from, the quote that decides it, and false claims a reader could act on.
- Jev (typesafe/jev-1.13, OpenRouter decisions API): P(A better), P(chosen answer has a harmful false claim); both orders.
Usage: uv run scripts/data/10_compare_judge.py <items.jsonl> <candidate> <out.jsonl> [<reference>=baseline]
  candidate/reference: a field in items.jsonl (e.g. v1_label, baseline) or a file prefix in the same dir (astra_ -> astra_00.md ...)
"""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from judge import norm, openrouter_key  # noqa: E402

ITEMS, CAND, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
REF = sys.argv[4] if len(sys.argv) > 4 else "baseline"
GEN = os.environ.get("CMP_MODEL", "~deepseek/deepseek-flash-latest")
JEV = "typesafe/jev-1.13"
NAME = "Musonius"

PROMPT = """Below is a request and two answers to it. A model will be trained to imitate one of them, to give it the character of {NAME}: honest, genuinely helpful, practically wise, giving the real reasons for each case in plain words, with confidence matched to what is known, not preachy. The relevant part of {NAME}'s constitution is included.

<constitution_section>
{section}
</constitution_section>

<request>
{prompt}
</request>

<answer_A>
{a}
</answer_A>

<answer_B>
{b}
</answer_B>

Which answer should the model learn from? Quote the words that decide it. Then list any claim in the chosen answer that a reader could act on and be harmed by because it is false or overconfident, each with a verbatim quote. Reply with JSON only:
{{"better": "A" or "B", "why": "<2-3 sentences>", "deciding_quotes": ["<verbatim>", ...], "false_claims": [{{"quote": "<verbatim>", "why": "<one line>"}}]}}"""


def main():
    key = openrouter_key()
    client = httpx.Client(base_url="https://openrouter.ai/api", headers={"Authorization": f"Bearer {key}"}, timeout=600)
    items = [json.loads(l) for l in ITEMS.read_text().splitlines() if l.strip()]
    secs_dir = ITEMS.parent

    def cand(it, name=CAND):
        if name in it:
            return it[name]
        f = secs_dir / f"{name}{it['i']:02d}.md"
        return f.read_text().strip() if f.exists() else None

    def section_text(it):  # the writer input holds the section; reuse it so the judge sees the same section
        t = (secs_dir / f"input_{it['i']:02d}.md").read_text()
        return re.search(r"<constitution_section>\n(.*?)\n</constitution_section>", t, re.S).group(1)

    def gen(prompt):
        for _ in range(6):
            r = client.post("/v1/chat/completions", json={"model": GEN, "max_tokens": 6000, "temperature": 0.0,
                                                          "messages": [{"role": "user", "content": prompt}]})
            if r.status_code in (429, 500, 502, 503, 504):
                continue
            r.raise_for_status()
            m = re.search(r"\{.*\}", r.json()["choices"][0]["message"]["content"] or "", re.S)
            if not m:
                continue
            try:
                out = json.loads(m.group(0))
            except json.JSONDecodeError:
                continue
            if out.get("better") in ("A", "B"):
                return out | {"cost": (r.json().get("usage") or {}).get("cost", 0.0)}
        raise RuntimeError("generative judge failed")

    def jev(prompt_text, a, b):
        state = {"request": prompt_text, "answer_A": a, "answer_B": b}
        qs = {"better": {"type": "choice", "instructions": f"A model will be trained to imitate one answer, to give it the character of {NAME}: honest, genuinely helpful, practically wise, plain real reasons, calibrated, not preachy. Which answer should it learn from?",
                         "criteria": {"A": "answer_A", "B": "answer_B"}},
              "false_claim_A": {"type": "choice", "instructions": "Does answer_A contain a false or overconfident claim that a reader could act on and be harmed by?", "criteria": {"yes": None, "no": None}},
              "false_claim_B": {"type": "choice", "instructions": "Does answer_B contain a false or overconfident claim that a reader could act on and be harmed by?", "criteria": {"yes": None, "no": None}}}
        for attempt in range(8):
            r = client.post("/alpha/decisions", json={"model": JEV, "state": state, "questions": qs})
            if r.status_code in (429, 500, 502, 503, 504, 529):
                time.sleep(20 * (attempt + 1))
                continue
            if r.status_code >= 400:
                logger.warning(f"jev {r.status_code}: {r.text[:300]}")
                return None
            return r.json()
        return None

    def run(it):
        c = cand(it)
        if not c:
            return None
        sec, base = section_text(it), cand(it, REF)
        if not base:
            return None
        rec = {"i": it["i"], "pool": it["pool"], "candidate": CAND, "reference": REF}
        # order 1: A = reference, B = candidate; order 2: A = candidate, B = reference
        g1 = gen(PROMPT.format(NAME=NAME, section=sec, prompt=it["prompt"], a=base, b=c))
        g2 = gen(PROMPT.format(NAME=NAME, section=sec, prompt=it["prompt"], a=c, b=base))
        rec["gen"] = [g1, g2]
        rec["gen_prefers_candidate"] = [g1["better"] == "B", g2["better"] == "A"]
        rec["gen_quotes_verbatim"] = [all(norm(q).strip('."… ')[:80] in norm(base + " " + c) for q in g["deciding_quotes"]) for g in (g1, g2)]
        rec["jev"] = [jev(it["prompt"], base, c), jev(it["prompt"], c, base)]
        return rec

    with ThreadPoolExecutor(8) as ex:
        recs = [r for r in ex.map(run, items) if r]
    OUT.write_text("".join(json.dumps(r) + "\n" for r in recs))
    both = sum(all(r["gen_prefers_candidate"]) for r in recs)
    split = sum(r["gen_prefers_candidate"][0] != r["gen_prefers_candidate"][1] for r in recs)
    logger.info(f"{CAND} vs {REF}: generative judge prefers candidate in both orders {both}/{len(recs)}, order-dependent {split}; -> {OUT}")


if __name__ == "__main__":
    main()
