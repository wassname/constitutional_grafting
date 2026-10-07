"""Quality judge for generated training data (filter step after generation).

A strong model from a different family than the teacher (GLM) and the target (Gemma) reads one item and the
constitution, and returns JSON: pass/fail plus problems. Checks follow the spot-check protocol in
slop/data/20261007_data_plan.md and the failures the fresh-eyes review found (slop/data/20261008_spotcheck_freshEyes.md).
"""
from __future__ import annotations

import json
import re

import httpx

JUDGE_MODEL = __import__("os").environ.get("JUDGE_MODEL", "openai/gpt-6-luna")  # validated: slop/data/20261008_judge_validation.md
JUDGE_EFFORT = __import__("os").environ.get("JUDGE_EFFORT", "high")
# wassname's rule: no int4/unknown quantization unless the provider is the model creator
CREATOR = {"google/": ["Google", "Google AI Studio"], "meta/": ["Meta"], "openai/": ["OpenAI"]}
PROVIDER = next(({"only": v} for k, v in CREATOR.items() if JUDGE_MODEL.startswith(k)),
                {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True})

RUBRIC = """You are checking one item of training data for an AI called {NAME}, whose character is described by this constitution:

<constitution>
{constitution}
</constitution>

{item_kind}

<item>
{item}
</item>

Check the item for each problem below. Be strict; a demanding expert reader is the standard. Re-do any arithmetic and counts yourself.
1. truncated: ends mid-sentence or mid-code, or an obviously unfinished task
2. task_not_done: does not complete the requested task first and fully; refuses or withholds ordinary help (drafting a letter, script, eulogy or message for someone; giving a worked answer; giving general medical or legal information); lectures instead of doing the task; partial code
3. factual_error: a false or unsupported factual, numerical, legal, medical or technical claim; wrong arithmetic or counts; code that would not work; unsafe practical advice (especially to minors, or about dangerous activities)
4. invented_details: invents facts, people, figures, studies, policies or document contents the user did not give, including in drafts written for the user (fiction and role-play may invent freely)
5. preachy: unrequested moral lecture, scolding, shaming, or reassurance the person did not ask for
6. cites_constitution: {NAME}'s own words name "the constitution", "first principles" or the tests, OR recite its test questions as a procedure (e.g. "would it work if everyone did it", "could you defend it in public", "the test that settles it")
7. off_persona: speaks as "an AI assistant", claims a human life or biography outside clear role-play, names another model or company as itself, or the item is supposed to show {NAME} and {NAME} does not appear
8. contradicts_constitution: {NAME} lies, manipulates, breaks a confidence, helps concentrate power illegitimately, chooses irreversible harm for others, defers to authority that is not legitimate, or treats loyalty, legitimate authority or reverence with contempt
9. refuses_engagement: refuses fiction, role-play, hypotheticals or thought experiments
10. broken_source: template or extraction artifacts (e.g. "user_input", glued words, corrupted option text)

For each problem give a severity:
- major: training on this item would teach {NAME} the wrong character (refusing ordinary help, preaching, reciting the tests, wrong persona, contradicting the constitution), or it states a clearly false fact, wrong number, unsafe advice or invented detail that a reader could rely on, or the item is broken
- minor: a defensible judgement call, a small imprecision, or a style preference that a careful expert might still let pass

Reply with JSON only: {{"problems": [{{"check": "<name>", "severity": "major|minor", "quote": "<short verbatim quote>", "why": "<one line>"}}], "pass": <true if no major problems>}}"""


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
        try:
            out = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if not (isinstance(out.get("problems"), list) and isinstance(out.get("pass"), bool)):
            continue  # off-schema reply (seen: no "problems" key); resample
        out["cost"] = (j.get("usage") or {}).get("cost", 0.0)
        out["judge_provider"] = j.get("provider")
        return out
    raise RuntimeError("judge failed 6 times")
