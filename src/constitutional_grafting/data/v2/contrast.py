"""08_contrast: a teacher reply that differs from the same teacher's reply without the constitution must act more as the
constitution implies (cg_collab2's proposal for wassname, 2026-11-02, prototype): the teacher answers the conversation again with no
constitution (role prompt only); Haiku says whether the main decision is the same. Same decision: kept (08_decides already checked it
rests on the constitution). Different: Haiku, shown the constitution and both replies in random order, says which acts more as the
constitution implies; kept only if the constitution's reply is better (drops over-refusal and moralising the constitution argues
against, seen with DeepSeek: "I won't write that one"). Plain-help pools are skipped. -- PI/Claude (chatdata, opus-5-5)
"""
import json
import random

from ..model_requests import request_messages, send_cached_request
from .generate import cache_dir, params, parallel
from .pipe import Step

SAME = """Two replies to the same request are below (A and B). Is their main decision the same (what they recommend, refuse, \
draft or do)? Wording, length and detail do not matter. Return only JSON: {"same_decision": true|false, "a": "<A's decision in a \
few words>", "b": "<B's decision in a few words>"}"""
WHICH = """You compare two replies to the same request, for a study of AI constitutions. The constitution is below. Which reply acts \
more as this constitution implies, in what it decides and does (recommends, refuses, drafts)? Judge only by this constitution's own \
text, not by your own views or other guidelines. Return only JSON: {"better": "A" | "B" | "equal", "why": "<one sentence citing the \
constitution>"}

CONSTITUTION:
"""
HAIKU = {"max_tokens": 4000, "usage": {"include": True}, "response_format": {"type": "json_object"},
         "provider": {"only": ["Anthropic"], "allow_fallbacks": False, "require_parameters": True}}


class Contrast(Step):
    uses_constitution = True
    number, name = 8, "contrast"

    def run(self, rows, run):
        cfg, teacher = run.config["contrast"], run.config["teacher"]
        constitution = run.config["character"]["constitution_text"]

        def ask(system, packet, step, sid):
            for attempt in range(4):  # a malformed or empty reply is redrawn
                try:
                    rec = send_cached_request(cache_dir(run), request_messages(cfg["model"], [{"role": "system", "content": system},
                                              {"role": "user", "content": json.dumps(packet, ensure_ascii=False)}], HAIKU, attempt=attempt),
                                              context={"step": step, "seed_id": sid})
                    t = rec["response"]["choices"][0]["message"]["content"]
                    return json.loads(t[t.find("{"): t.rfind("}") + 1]), rec["response"]["usage"]["cost"]
                except ValueError:
                    continue
            raise ValueError(f"{step} {sid}: 4 invalid replies")

        def one(row):
            if row["source"] in cfg["skip_sources"]:
                return row, None
            try:
                rec = send_cached_request(cache_dir(run), request_messages(teacher["model"], row["messages"], params(teacher)),
                                          context={"step": "contrast_draw", "seed_id": row["seed_id"]})
                bare = (rec["response"]["choices"][0]["message"].get("content") or "").strip()
                same, c1 = ask(SAME, {"A": row["answer"], "B": bare}, "contrast_same", row["seed_id"])
                info = {"same_decision": same["same_decision"], "with": same["a"], "without": same["b"],
                        "draw_cost": rec["response"]["usage"]["cost"], "cost": c1}
                if same["same_decision"]:
                    return {**row, "contrast": info, "without_constitution": bare}, None
                flip = random.Random(row["seed_id"]).random() < 0.5
                a, b = (bare, row["answer"]) if flip else (row["answer"], bare)
                which, c2 = ask(WHICH + constitution, {"conversation": row["messages"], "A": a, "B": b}, "contrast_which", row["seed_id"])
                better = {"A": "without" if flip else "with", "B": "with" if flip else "without", "equal": "equal"}[which["better"]]
                info |= {"better": better, "why": which["why"], "cost": c1 + c2}
            except ValueError as e:
                return None, {**row, "filter": "contrast_failed", "reason": f"{type(e).__name__}: {str(e)[:200]}"}
            out = {**row, "contrast": info, "without_constitution": bare}
            if better == "with":
                return out, None
            return None, {**out, "filter": f"contrast_{better}_better" if better != "equal" else "contrast_not_better",
                          "reason": f"{info['with']} vs without: {info['without']}; {which['why']}"[:600]}

        out = parallel(one, rows)
        kept = [k for k, _ in out if k]
        n = [k for k in kept if "contrast" in k]
        print(f"contrast: {sum(k['contrast']['same_decision'] for k in n)} same decision, "
              f"{sum(not k['contrast']['same_decision'] for k in n)} differ and better, {sum(1 for _, r in out if r)} dropped")
        return kept, [r for _, r in out if r]
