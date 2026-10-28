"""04_route: the reply goes through Latin or Ancient Greek; the think block stays the teacher's own English reasoning.
The route writer sees the conversation and the teacher's notes (not its English reply) and composes the reply in the chosen
language; the translator turns it into English; with `answer_route.fidelity`, cheap checkers list misleading errors and a fixer
edits only those spans. Ordinary help stays English (code and technical text do not survive the trip).
Keeps `answer_direct` (the teacher's English reply), `reply_src` (the classical draft) and `answer_translated` (before fixes). -- PI/Claude (opus-5-5), 2026-10-27
"""
import json
import re

from .generate import call_text, hash_order, parallel, with_constitution
from .pipe import Step

LANG = {"la": ("Latin", "Latin, as a Roman author of the early Empire would write it"),
        "grc": ("Ancient Greek", "Ancient Greek (Attic or koine prose)")}

COMPOSE = """Below are a conversation and your own working notes for your reply. Write the reply now, in {language}, following \
your notes. Keep every name, number, amount, currency, date, place, product, institution, document, deadline and technical \
term exactly as written in the conversation, untranslated, in English, and keep words the user quoted as they wrote them. Keep \
any drafted letter, list or code in its form. Output only the reply.

<conversation>
{conversation}
</conversation>

<notes>
{notes}
</notes>"""

TRANSLATE = """Translate this {language} reply into natural modern English. Keep every fact, reason, recommendation, name and the \
order; keep the register. Do not add, explain, soften or moralise. Output only the English reply.

{reply}"""


ERRORS = """List only errors that would mislead the user:
1. status: something requested, proposed or planned is said to be already done, or something done is said to be still to do;
2. time: a day, date, deadline or order of events that disagrees with the conversation or notes;
3. actors: who did, does or should do something is changed or confused, including a gender or relation the conversation does \
not give;
4. numbers or names: an amount, count, name or term is changed;
5. assistant action: the assistant claims or promises an action outside this chat (contacting people, sending, filing, \
checking, monitoring); it has no tools;
6. reversal: a recommendation, principle or conclusion says the opposite of what the notes decided.
Do not list style, stiff or classical wording, minor omissions, advice you would give differently, or points the notes leave open."""

CHECK = """An assistant wrote the reply below in {language}, following its own working notes, and it was then translated into \
English. Check the English reply against the conversation and the notes. """ + ERRORS + """
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

REPAIR = """Below are a conversation, an assistant's working notes, the {language} draft of its reply, the English translation that \
will be sent, and a checker's list of possible errors in the English. For each listed error, decide whether it is real: the \
English would mislead the user compared with the conversation and the notes. Fix each real error with the smallest change to the \
English so that it agrees with the conversation and notes (the draft can be wrong too). Change nothing else: no rephrasing, no \
additions, same register. Skip errors that are not real.

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

<possible_errors>
{errors}
</possible_errors>

Return only JSON: {{"edits": [{{"old": "exact substring of the English", "new": "replacement"}}]}}. Use an empty list if \
none of the errors is real."""


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


def as_json(text: str) -> dict:
    return json.loads(re.search(r"\{.*\}", text, re.S).group(0))


def check_and_fix(run, cfg: dict, fields: dict, seed_id: str) -> tuple[str, dict, float]:
    """Each checker lists misleading errors in the English; one fixer edits only the listed spans. Rows are kept either way.
    20-row read: 7/20 rows with misleading errors before, 4/20 after, same as the teacher's direct English (slop/reviews/20261028_route_fidelity)."""
    errors, cost = [], 0.0
    for name, c in cfg["checkers"].items():
        text, _, k = call_text(run, c, [{"role": "user", "content": CHECK.format(**fields)}], {"step": "route_check", "checker": name, "seed_id": seed_id})
        errors += [{**e, "checker": name} for e in as_json(text)["errors"]]
        cost += k
    english, edits, missing = fields["english"], [], []
    if errors:
        listed = "\n".join(f"- [{e['kind']}] \"{e['quote']}\": {e['why']}" for e in errors)
        text, _, k = call_text(run, cfg["fixer"], [{"role": "user", "content": REPAIR.format(**fields, errors=listed)}], {"step": "route_fix", "seed_id": seed_id})
        cost += k
        edits = as_json(text)["edits"]
        for e in edits:
            if e["old"] in english:
                english = english.replace(e["old"], e["new"], 1)
            else:
                missing.append(e["old"])
    return english, {"errors": errors, "edits": edits, "edits_not_found": missing}, cost


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
                fixed, fidelity, c3 = (check_and_fix(run, cfg["fidelity"], dict(language=short, conversation=conv, notes=row["reasoning"],
                                       draft=src, english=en), row["seed_id"]) if "fidelity" in cfg else (en, None, 0.0))
            except Exception as e:
                return None, {**row, "route": route, "filter": "route_failed", "reason": f"{type(e).__name__}: {str(e)[:200]}"}
            return {**row, "route": route, "answer_direct": row["answer"], "reply_src": src, "answer_translated": en, "answer": fixed,
                    "fidelity": fidelity, "route_cost": c1 + c2 + c3}, None

        out = parallel(one, rows)
        return [k for k, _ in out if k], [r for _, r in out if r]
