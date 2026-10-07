"""Quality judge for generated training data (filter step after generation).

A strong model from a different family than the teacher (GLM) and the target (Gemma) reads one item and the
constitution, and returns JSON: pass/fail plus problems. Checks follow the spot-check protocol in
slop/data/20261007_data_plan.md and the failures the fresh-eyes review found (slop/data/20261008_spotcheck_freshEyes.md).
"""
from __future__ import annotations

import json
import re

import httpx

JUDGE_MODEL = __import__("os").environ.get("JUDGE_MODEL", "deepseek/deepseek-v4-pro")
JUDGE_EFFORT = __import__("os").environ.get("JUDGE_EFFORT", "low")
# wassname's rule: no int4/unknown quantization unless the provider is the model creator
PROVIDER = ({"only": ["Google", "Google AI Studio"]} if JUDGE_MODEL.startswith("google/")
            else {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True})

RUBRIC = """You are checking one item of training data for an AI called {NAME}, whose character is described by this constitution:

<constitution>
{constitution}
</constitution>

{item_kind}

<item>
{item}
</item>

Check the item for each problem below. Be strict; a demanding expert reader is the standard.
1. truncated: ends mid-sentence or mid-code, or an obviously unfinished task
2. task_not_done: does not complete the requested task first and fully (e.g. lectures instead of drafting, refuses ordinary help, partial code)
3. factual_error: a false or unsupported factual, numerical, legal, medical or technical claim; code that would not work
4. invented_details: invents facts, people, figures, studies or policies the user did not give (fiction and role-play may invent freely)
5. preachy: unrequested moral lecture, scolding, or reassurance that the person did not ask for
6. cites_constitution: {NAME}'s own words name "the constitution", "first principles", or the tests ("public test", "universal test", etc.)
7. off_persona: speaks as "an AI assistant", claims to be human, or names another model or company as itself
8. contradicts_constitution: {NAME} lies, manipulates, helps concentrate power illegitimately, chooses irreversible harm for others, or treats loyalty, legitimate authority or reverence with contempt
9. refuses_engagement: refuses fiction, role-play, hypotheticals or thought experiments

Reply with JSON only: {{"problems": [{{"check": "<name>", "quote": "<short verbatim quote>", "why": "<one line>"}}], "pass": <true if no problems>}}"""


def judge(client: httpx.Client, constitution: str, item: str, item_kind: str, name: str = "Musonius") -> dict:
    prompt = RUBRIC.format(NAME=name, constitution=constitution, item=item, item_kind=item_kind)
    for attempt in range(6):
        r = client.post("/chat/completions", json={
            "model": JUDGE_MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": 16000,
            "temperature": 0.0, "reasoning": {"effort": JUDGE_EFFORT}, "provider": PROVIDER})
        if r.status_code in (429, 500, 502, 503, 504):
            continue
        r.raise_for_status()
        j = r.json()
        text = j["choices"][0]["message"]["content"] or ""
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            continue  # judge returned no JSON (e.g. reasoning used the budget); resample
        out = json.loads(m.group(0))
        out["cost"] = (j.get("usage") or {}).get("cost", 0.0)
        out["judge_provider"] = j.get("provider")
        return out
    raise RuntimeError("judge failed 6 times")
