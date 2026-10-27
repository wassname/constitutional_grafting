# Language route for chat answers (goal 1 task 2; wassname: "we are not meant to be testing it on the scenario, but on an answer").
# The think block stays Kimi's own English reasoning. For la/grc, Kimi is shown the conversation and its own notes (not its
# English reply) and composes the reply in Latin or Greek; DeepSeek flash translates it to English. en = the original Kimi low
# answer from teacher test v2. (Try 1 gave the notes as a reasoning prefix with the language in the system prompt: Kimi wrote
# all 26 replies in English, kept in api/ for the record.)
# Usage: uv run --env-file .env python scripts/scratch/20261027_answer_route_test.py  -- PI/Claude (opus-5-5), 2026-10-27
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.checks import TICS

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/scratch/20261027_answer_route"
TT = ROOT / "data/scratch/20261027_teacher_test_v2"
LANG = {"la": "Latin, as a Roman author of the early Empire would write it", "grc": "Ancient Greek (Attic or koine prose)"}
TRANSLATE = """Translate this {language} reply into natural modern English. Keep every fact, reason, recommendation, name and the order; \
keep the register. Do not add, explain, soften or moralise. Output only the English reply.

{reply}"""


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("tt", ROOT / "scripts/scratch/20261027_teacher_test_v2.py")
    tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
    convs = dict(tt.prompts())
    kimi = {r["prompt"]: r for r in map(json.loads, (TT / "answers.jsonl").open()) if r["teacher"] == "kimi_low" and not r["error"]}
    kparams = {"max_tokens": 6000, "include_reasoning": True, "usage": {"include": True}, "reasoning": {"effort": "low"},
               "provider": {"only": ["Moonshot AI"], "allow_fallbacks": False, "require_parameters": True}}
    dparams = {"max_tokens": 6000, "include_reasoning": True, "usage": {"include": True}, "reasoning": {"effort": "low"},
               "provider": {"only": ["DeepSeek"], "allow_fallbacks": False, "require_parameters": True}}

    def one(job):
        pid, route = job
        k = kimi[pid]
        conv = "\n\n".join(f"[{m['role']}] {m['content']}" for m in convs[pid])
        system = tt.with_constitution(convs[pid])[0]["content"]
        ask = (f"Below are a conversation and your own working notes for your reply. Write the reply now, in {LANG[route]}, following "
               f"your notes. Output only the reply.\n\n<conversation>\n{conv}\n</conversation>\n\n<notes>\n{k['reasoning']}\n</notes>")
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": ask}]
        try:
            rec = send_cached_request(OUT / "api", request_messages("moonshotai/kimi-k3.1-pro", msgs, kparams, attempt=1), context={"route": route, "prompt": pid})
            m = rec["response"]["choices"][0]["message"]
            src, extra = (m.get("content") or "").strip(), (m.get("reasoning") or "").strip()
            tr = send_cached_request(OUT / "api", request_messages("deepseek/deepseek-v4.1-flash-1017", [{"role": "user", "content":
                     TRANSLATE.format(language=LANG[route].split(",")[0].split(" (")[0], reply=src)}], dparams), context={"translate": route, "prompt": pid})
            en = (tr["response"]["choices"][0]["message"].get("content") or "").strip()
            cost = rec["response"]["usage"]["cost"] + tr["response"]["usage"]["cost"]
            return {"prompt": pid, "route": route, "reply_src": src, "extra_reasoning_words": len(extra.split()), "answer": en, "cost": cost, "error": None}
        except Exception as e:
            return {"prompt": pid, "route": route, "error": f"{type(e).__name__}: {str(e)[:300]}"}

    jobs = [(p, r) for p in kimi for r in ("la", "grc")]
    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(one, jobs))
    rows += [{"prompt": p, "route": "en", "reply_src": k["answer"], "extra_reasoning_words": 0, "answer": k["answer"], "cost": 0.0, "error": None} for p, k in kimi.items()]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "answers.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print("errors:", [(r["prompt"], r["route"], r["error"]) for r in rows if r["error"]])
    ok = [r for r in rows if not r["error"]]
    greek = lambda t: len(re.findall(r"[\u0370-\u03ff\u1f00-\u1fff]", t)) / max(1, len(t))
    latin = lambda t: len(re.findall(r"\b(et|est|non|ad|cum|quod|sed|ut|in)\b", t)) / max(1, len(t.split()))
    print("source really in the language:", [(r["route"], round(latin(r["reply_src"]) if r["route"] == "la" else greek(r["reply_src"]), 2)) for r in ok if r["route"] != "en"])
    for route in ("en", "la", "grc"):
        rr = [r for r in ok if r["route"] == route]
        text = " ".join(r["answer"] for r in rr); n = len(text.split())
        rates = {k: round(1000 * len(re.findall(rx, text, re.I)) / n, 2) for k, rx in TICS.items() if k not in ("persona_words", "retrospective")}
        print(route, len(rr), "words", n, rates, "cost", round(sum(r["cost"] for r in rr), 3))


if __name__ == "__main__":
    main()
