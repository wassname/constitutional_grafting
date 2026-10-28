# Calibrate a fidelity check on the 20 route rows that GPT-6.1 sol read (read2.md + read_source.md labels).
# A: second translations of the Latin/Greek draft by three cheap models (wassname: "could try glm 5.3 flash, mimo flash, gpt luna").
# B: a narrow checker (status, time, actors, numbers, claimed actions, reversal) given conversation, notes, draft and English;
#    run on the current English and on each second translation, 2 samples per checker.
# Usage: uv run --env-file .env python scripts/scratch/20261028_fidelity_calib.py   -- PI/Claude (opus-5-5), 2026-10-28
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.route import LANG, TRANSLATE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/scratch/20261028_fidelity_calib"
CACHE = ROOT / "data/cache/api"
# labels from read2.md (rows 5,7,11,14,16,18,20) and read_source.md (adds 8,10,12, each flagged by 2+ other reads)
DEFECT = {5: "translation", 7: "composition", 8: "composition", 10: "translation", 11: "translation", 12: "translation",
          14: "composition", 16: "unclear", 18: "translation", 20: "composition"}


def pin(provider, **kw):
    return {"provider": {"only": [provider], "allow_fallbacks": False, "require_parameters": True}, "usage": {"include": True},
            "include_reasoning": True, **kw}


TRANSLATORS = {
    "ds": None,  # the current export's English
    "luna": ("openai/gpt-6-luna", pin("OpenAI", max_tokens=8000, reasoning={"effort": "low"})),
    "mimo": ("xiaomi/mimo-v2.6-flash", pin("Xiaomi", max_tokens=8000, reasoning={"enabled": False})),
    "glm": ("z-ai/glm-5.3-flash", pin("Z.AI", max_tokens=8000, reasoning={"effort": "low"})),  # Z.AI: reasoning is mandatory
}
CHECKERS = {
    "luna": ("openai/gpt-6-luna", pin("OpenAI", max_tokens=12000, reasoning={"effort": "low"})),
    "mimo": ("xiaomi/mimo-v2.6-flash", pin("Xiaomi", max_tokens=12000, reasoning={"effort": "low"})),
    "glm": ("z-ai/glm-5.3-flash", pin("Z.AI", max_tokens=12000, reasoning={"effort": "low"})),
    "ds": ("deepseek/deepseek-v4.1-flash-1017", pin("DeepSeek", max_tokens=12000, reasoning={"effort": "low"})),
    "haiku": ("anthropic/claude-haiku-5.5", pin("Anthropic", max_tokens=8000, reasoning={"enabled": False})),
}

CHECK = """An assistant wrote the reply below in {language}, following its own working notes, and it was then translated into \
English. Check the English reply against the conversation and the notes. List only errors that would mislead the user:
1. status: something requested, proposed or planned is said to be already done, or something done is said to be still to do;
2. time: a day, date, deadline or order of events that disagrees with the conversation or notes;
3. actors: who did, does or should do something is changed or confused;
4. numbers or names: an amount, count, name or term is changed;
5. assistant action: the assistant claims or promises an action outside this chat (contacting people, sending, filing, \
checking, monitoring); it has no tools;
6. reversal: a recommendation, principle or conclusion says the opposite of what the notes decided.
Do not list style, stiff or classical wording, minor omissions, advice you would give differently, or points the notes leave open.
For each error, compare the {language} draft: "draft" if the draft already says it, "translation" if only the English does.

<conversation>
{conversation}
</conversation>

<notes>
{notes}
</notes>

<draft language="{language}">
{draft}
</draft>

<english>
{english}
</english>

Return only JSON: {{"errors": [{{"quote": "exact words from the English", "kind": "status|time|actors|numbers|assistant_action|reversal", \
"where": "draft|translation", "why": "one sentence"}}]}}. Use an empty list if there are none."""


def text_of(rec):
    return (rec["response"]["choices"][0]["message"].get("content") or "").strip(), rec["response"]["usage"]["cost"]


def parse(t):
    m = re.search(r"\{.*\}", t, re.S)
    return json.loads(m.group(0))["errors"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(l) for l in (ROOT / "data/11_export/v3/large/rows.jsonl").open()]
    rows = [r for r in rows if r.get("route") in ("la", "grc") and r.get("answer_direct")]
    rows = sorted(rows, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())[:20]

    def translate(job):
        k, r, name = job
        model, p = TRANSLATORS[name]
        msg = TRANSLATE.format(language=LANG[r["route"]][0], reply=r["reply_src"])
        rec = send_cached_request(CACHE, request_messages(model, [{"role": "user", "content": msg}], p),
                                  context={"step": "fidelity_calib_translate", "translator": name, "id": r["id"]})
        return (k, name), text_of(rec)

    with ThreadPoolExecutor(12) as ex:
        en = dict(ex.map(translate, [(k, r, n) for k, r in enumerate(rows, 1) for n in TRANSLATORS if n != "ds"]))
    for k, r in enumerate(rows, 1):
        target = [x["text"] for x in r["segments"] if x["label"]][0]
        en[(k, "ds")] = (target.partition("</think>")[2].removesuffix("<|im_end|>").strip(), 0.0)

    def check(job):
        k, r, tr, name, attempt = job
        model, p = CHECKERS[name]
        prompt = [s["text"] for s in r["segments"] if not s["label"]][0]
        notes = [s["text"] for s in r["segments"] if s["label"]][0].partition("</think>")[0].replace("<think>", "").strip()
        msg = CHECK.format(language=LANG[r["route"]][0], conversation=prompt, notes=notes, draft=r["reply_src"], english=en[(k, tr)][0])
        try:
            rec = send_cached_request(CACHE, request_messages(model, [{"role": "user", "content": msg}], p, attempt=attempt),
                                      context={"step": "fidelity_calib_check", "checker": name, "translator": tr, "id": r["id"]})
            t, c = text_of(rec)
            return {"row": k, "translator": tr, "checker": name, "attempt": attempt, "errors": parse(t), "cost": c}
        except Exception as e:
            return {"row": k, "translator": tr, "checker": name, "attempt": attempt, "errors": None, "fail": f"{type(e).__name__}: {str(e)[:200]}", "cost": 0}

    jobs = [(k, r, tr, ch, a) for k, r in enumerate(rows, 1) for tr in TRANSLATORS for ch in CHECKERS for a in (0, 1)
            if tr == "ds" or ch in ("luna", "ds")]  # all checkers on the current English; two checkers on the second translations
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(check, jobs))
    with (OUT / "checks.jsonl").open("w") as f:
        for x in res:
            f.write(json.dumps(x) + "\n")
    json.dump({f"{k}|{n}": t for (k, n), (t, _) in en.items()}, (OUT / "translations.json").open("w"), indent=1)
    print("translate cost", round(sum(c for _, c in en.values()), 4), "check cost", round(sum(x["cost"] for x in res), 4),
          "fails", sum(x["errors"] is None for x in res))


if __name__ == "__main__":
    main()
