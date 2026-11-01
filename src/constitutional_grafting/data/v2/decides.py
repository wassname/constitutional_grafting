"""08_decides: keep a chat only if its main decision rests on something this constitution says (wassname, approved in principle
2026-11-02: "keep only chats whose decision rests on something THIS constitution says"; goal check: Kimi with a 1,000-word Rules Spec
mostly decides from its own defaults). Haiku names the decision and quotes the passages that give a reason for it over the case's
alternatives; a row with no quote found verbatim in the constitution is rejected (constitution_silent). Plain-help pools are skipped:
a fixed, unfiltered share. -- PI/Claude (chatdata, opus-5-5)
"""
import json

from ..model_requests import request_messages, send_cached_request
from .generate import cache_dir, parallel
from .pipe import Step
from .seeds import norm

PROMPT = """You check one training example for a study of AI constitutions. The assistant's constitution is below; the assistant \
wrote the reply with it as its own hidden system prompt. The example is kept only if the reply's main decision rests on something \
this constitution says.

1. State the reply's main decision in a few words: what it recommends, refuses, drafts or does, or which side it takes.
2. Find the passages of the constitution that give a reason for that decision over the alternatives the case offers. Quote each \
exactly, copying the constitution's words. A passage counts only if it bears on this choice; a general passage that would fit any \
reply (such as a general duty to help) does not count unless the case turns on it. Operator or user instructions count only through \
a passage of the constitution about following them.
3. If no passage gives a reason for the decision, return an empty list. The reply may still be good; the question is only whether \
this constitution decides it.
Return only JSON: {"decision": "<a few words>", "quotes": ["<exact passage>", ...], "why": "<one sentence: how the quotes decide it, \
or why none does>"}

CONSTITUTION:
"""


def found(quote: str, constitution_norm: str) -> bool:
    q = norm(quote).strip()[:80]
    return len(q) >= 15 and q in constitution_norm


class Decides(Step):
    uses_constitution = True
    number, name = 8, "decides"

    def run(self, rows, run):
        cfg, constitution = run.config["decides"], run.config["character"]["constitution_text"]
        cnorm = norm(constitution)
        params = {"max_tokens": 4000, "usage": {"include": True}, "response_format": {"type": "json_object"},
                  "provider": {"only": ["Anthropic"], "allow_fallbacks": False, "require_parameters": True}}

        def one(row):
            if row["source"] in cfg["skip_sources"]:
                return row, None
            packet = {"conversation": row["messages"], "notes": row["reasoning"], "reply": row["answer"]}
            err = ""
            for attempt in range(4):  # a malformed reply is redrawn, like the judge's
                req = request_messages(cfg["model"], [{"role": "system", "content": PROMPT + constitution},
                                                      {"role": "user", "content": json.dumps(packet, ensure_ascii=False)}], params, attempt=attempt)
                rec = send_cached_request(cache_dir(run), req, context={"step": "decides", "seed_id": row["seed_id"]})
                t = rec["response"]["choices"][0]["message"]["content"]
                try:
                    out = json.loads(t[t.find("{"): t.rfind("}") + 1])
                    quotes = [q for q in out["quotes"] if found(q, cnorm)]
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    err = f"{type(e).__name__}: {str(e)[:200]}"
                    continue
                d = {**out, "quotes_found": len(quotes), "cost": rec["response"]["usage"]["cost"]}
                if quotes:
                    return {**row, "decides": d}, None
                return None, {**row, "decides": d, "filter": "constitution_silent",
                              "reason": f"{out['decision']}: {out['why']}"[:600]}
            return None, {**row, "filter": "decides_failed", "reason": err}

        out = parallel(one, rows)
        return [k for k, _ in out if k], [r for _, r in out if r]
