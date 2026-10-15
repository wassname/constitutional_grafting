# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Three small tests of ways to break the 'same authorial conscience' in data v2 (wassname 2026-10-15 ideas), on 10 seeds each:
  sketch : Astra (gpt-6-astra) sketches the decision and reasons from the case; Opus 5.5 writes the document from the sketch
  greek  : Opus writes the document in Modern Greek; DeepSeek v4 pro translates it to English
  book   : textbook-of-moral-reasoning sections from tiny-stoic EXTENDED vignettes (the eval uses the core set, excluded)
The same 10 pilot-2 seeds are used for sketch and greek, so they compare with the existing Opus-only documents.
Writes slop/reviews/20261015_docs_v2_variants/{sketch,greek,book}.jsonl.   -- PI/Claude (Opus 5.5)"""
import importlib.util
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/reviews/20261015_docs_v2_variants"
spec = importlib.util.spec_from_file_location("g", ROOT / "scripts/data/50_docs_v2.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
KEY = next(l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
CONST = (ROOT / "constitution/v4.md").read_text()
SYSTEM = g.SYSTEM.format(constitution=CONST)


def chat(model, messages, max_tokens=6000, reasoning=None):
    body = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if reasoning:
        body["reasoning"] = reasoning
    for _ in range(3):
        try:
            j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {KEY}"}, json=body, timeout=900).json()
        except httpx.HTTPError:
            continue
        if "choices" in j and j["choices"][0]["message"].get("content"):
            return j["choices"][0]["message"]["content"].strip(), (j.get("usage") or {}).get("cost", 0), j.get("model")
    return "", 0, None


def opus(user):
    return chat(g.MODEL, [{"role": "system", "content": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}]}, {"role": "user", "content": user}])


SKETCH = """You are planning one training document for an AI character called Musonius, whose values are in the constitution below. Do not write the document. From the seed alone, decide what the right act is for whoever must choose (the AI if it appears, else the people), the real reasons for it in this case, what stays uncertain, and the strongest objection a careful person might raise. 5-8 terse bullet points. If the case is ordinary work with no real dilemma, say so and describe what doing it well looks like.

<constitution>
{c}
</constitution>

Seed:
{seed}

Form: {form}. Narrator: {narrator}. Plot: {plot}. Region: {region}."""


def sketch(r):
    plan, c1, m1 = chat("openai/gpt-6-astra", [{"role": "user", "content": SKETCH.format(c=CONST, **r)}], 4000, {"effort": "medium"})
    doc, c2, m2 = opus(g.USER.format(**r) + f"\n\nA colleague has worked out the decision and reasons for this case. Follow its substance, in your own words and in the document's own register:\n{plan}")
    return {**r, "sketch": plan, "document": doc, "meta": {"sketch_model": m1, "writer": m2, "cost": c1 + c2}}


def greek(r):
    el, c1, m1 = opus(g.USER.format(**r) + "\n\nWrite the whole document in Modern Greek.")
    en, c2, m2 = chat("deepseek/deepseek-v4-pro-0813", [{"role": "user", "content": "Translate this document into natural, idiomatic English. Keep its form, names, facts and meaning exactly. Output only the translation.\n\n" + el}], 6000)
    return {**r, "greek": el, "document": en, "meta": {"writer": m1, "translator": m2, "cost": c1 + c2}}


def book(v):
    r = {"source": "tiny_stoic_extended", "seed": v["other"], "form": "a section of a textbook on moral reasoning: one worked case",
         "narrator": "a human author", "plot": "an argument for one position on a question, with the best objections answered",
         "length": "300-700 words", "region": v.get("region", "any"), "manner": "plain", "idea": "Virtue"}
    doc, c, m = opus(g.USER.format(**r))
    return {**r, "id": f"book_{v['id']}", "document": doc, "meta": {"writer": m, "cost": c}}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pilot = {json.loads(l)["id"]: json.loads(l) for l in open(ROOT / "data/docs_v2/docs.jsonl")}
    seeds = [json.loads(l) for l in open(ROOT / "data/docs_v2/seeds.jsonl") if json.loads(l)["id"] in pilot]
    S = random.Random(20261015).sample(seeds, 10)
    core = {json.loads(l)["id"] for l in open("/workspace/2026/tiny-stoic/data/core/vignettes.jsonl")}
    ext = [json.loads(l) for l in open("/workspace/2026/tiny-stoic/data/extended/vignettes.jsonl")]
    V = random.Random(20261015).sample([v for v in ext if v["id"] not in core], 10)
    with ThreadPoolExecutor(10) as ex:
        for name, fn, items in [("sketch", sketch, S), ("greek", greek, S), ("book", book, V)]:
            rows = list(ex.map(fn, items))
            (OUT / f"{name}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
            logger.info(f"{name}: {sum(bool(x['document']) for x in rows)}/10, cost ${sum(x['meta']['cost'] or 0 for x in rows):.2f}")
    (OUT / "opus_only.jsonl").write_text("".join(json.dumps(pilot[s["id"]]) + "\n" for s in S))


if __name__ == "__main__":
    main()
