"""04_route: the reply goes through Latin or Ancient Greek; the think block stays the teacher's own English reasoning.
The route writer sees the conversation and the teacher's notes (not its English reply) and composes the reply in the chosen
language; the translator turns it into English. Ordinary help stays English (code and technical text do not survive the trip).
Keeps `answer_direct` (the teacher's English reply) and `reply_src` (the classical draft). -- PI/Claude (opus-5-5), 2026-10-27
"""
from .generate import cache_dir, call_text, hash_order, parallel, with_constitution
from .pipe import Step

LANG = {"la": ("Latin", "Latin, as a Roman author of the early Empire would write it"),
        "grc": ("Ancient Greek", "Ancient Greek (Attic or koine prose)")}

COMPOSE = """Below are a conversation and your own working notes for your reply. Write the reply now, in {language}, following \
your notes. Output only the reply.

<conversation>
{conversation}
</conversation>

<notes>
{notes}
</notes>"""

TRANSLATE = """Translate this {language} reply into natural modern English. Keep every fact, reason, recommendation, name and the \
order; keep the register. Do not add, explain, soften or moralise. Output only the English reply.

{reply}"""


def pick_route(row: dict, weights: dict) -> str:
    if row["shape"] == "ordinary":
        return "en"
    x = int(hash_order(4, row["seed_id"]), 16) % 1000 / 1000
    acc = 0.0
    for route, w in weights.items():
        acc += w
        if x < acc:
            return route
    return list(weights)[-1]


class Route(Step):
    number, name = 4, "route"

    def run(self, rows, run):
        cfg = run.config["answer_route"]

        def one(row):
            route = pick_route(row, cfg["weights"])
            if route == "en":
                return {**row, "route": "en", "answer_direct": row["answer"]}, None
            short, long = LANG[route]
            conv = "\n\n".join(f"[{m['role']}] {m['content']}" for m in row["messages"])
            try:
                src, _, c1 = call_text(run, cfg["writer"], with_constitution(run, row["messages"])[:1] + [
                    {"role": "user", "content": COMPOSE.format(language=long, conversation=conv, notes=row["reasoning"])}],
                    {"step": "route_compose", "seed_id": row["seed_id"], "route": route})
                en, _, c2 = call_text(run, cfg["translator"], [{"role": "user", "content": TRANSLATE.format(language=short, reply=src)}],
                                      {"step": "route_translate", "seed_id": row["seed_id"], "route": route})
                assert src and en, "empty compose or translation"
            except Exception as e:
                return None, {**row, "route": route, "filter": "route_failed", "reason": f"{type(e).__name__}: {str(e)[:200]}"}
            return {**row, "route": route, "answer_direct": row["answer"], "reply_src": src, "answer": en, "route_cost": c1 + c2}, None

        out = parallel(one, rows)
        return [k for k, _ in out if k], [r for _, r in out if r]
