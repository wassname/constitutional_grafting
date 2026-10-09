"""Prompt text for pipeline 2: astra writes request + compact-logic notes, Echo writes the reply. Run by scripts/data/30_astra_echo.py.
Every prompt's sha goes into each row's meta, so a row can be traced to the exact text.   -- PI / OpenAI Sol"""
import hashlib
import json
import random
import re
from pathlib import Path

import constitution as C  # scripts/data/constitution.py: renders constitution/v4.md.j2, the single source

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
POOL = HERE / "example_pool.md"  # request + notes pairs, one per reasoning move or constitution idea (history in the file header)
ECHO_SAMPLES = ROOT / "data/frontier/sft_ae/inputs/echo_samples_modern.json"  # frozen once by `30_astra_echo.py freeze-samples`


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def pool() -> dict[str, str]:
    """{move: "Request: ...\n\nReasoning: ..."}; comment lines are for humans and the leak check, not for astra."""
    return {m[1]: re.sub(r"<!--.*?-->\n", "", m[2]).strip() for m in re.finditer(r"^## (\w+)\n(.*?)(?=^## |\Z)", POOL.read_text(), re.S | re.M)}


REASON_FORMAT = """For each seed write a section:

### <id>
#### Request
(the request Musonius receives, written from the seed as its shape says: a system prompt, if any, on a line starting `System:`; then the user message. For repair: the request, `Assistant (first reply):`, and `User:` pushback lines.)
#### Reasoning
(private notes for a separate writer, who writes Musonius's reply from them. Write the notes as compact logic with back-of-the-envelope estimates, not prose: short labelled lines; `→` for a step that follows or is predicted, `∀` for the everyone-does-this test, `⊬` for does-not-follow, `+`/`-` for evidence for or against. Use only the labels this case needs, in this order:

FACTS: f1, f2, ... only what the request states or plainly implies.
GOAL vs METHOD: what the person wants and fears; the method they proposed; does the method serve the goal?
WEIGHTS: who is affected, how near they are, what each stands to lose; relative weights with their reason, ranked where stakes differ.
VALUES: where the case turns on a value, how settled it is (old and shared, recent, or still moving).
FERMI: rough numbers from the stated facts, arithmetic shown; only numbers that could change the decision.
MECHANISM: a → b → c, what the people affected, including those who must carry the decision out, actually do next; mark predictions.
∀-TEST: what happens if everyone held the drive behind the act.
OPTIONS: o1, o2, ... each with (cost → whom); include the option nobody named; say who decides.
UNCERTAIN / CHEAPEST CHECK: the one question to ask the person, or thing to check, that would most change the answer; IF result THEN what changes.
THEREFORE: the decision, how any refusal is made visible to those it affects, then, only if the person needs one, DRAFT: the one artifact they need (a message, order, log or note), written in full, plain text, usually under 120 words. Draft the artifact, not the reply: the writer writes the reply.

At most about 200 words before the draft. No rule numbers, no citations of the constitution.)

For a seed whose shape is `ordinary`, write `#### Reply` (the full, excellent answer to the request) instead of `#### Reasoning`.

Do not write Musonius's reply for any other seed: the writer does that.
"""


def examples_block(order_seed: str) -> tuple[str, list[str]]:
    """All pool pairs in every call (wassname: "we need all for the full spectrum of examples"), in an order shuffled by
    order_seed so no example always comes first. Returns the text and the order, which goes into each row's meta."""
    p = pool()
    order = sorted(p)
    random.Random(order_seed).shuffle(order)
    ex = "\n\n".join(f'<example move="{k}">\n{p[k]}\n</example>' for k in order)
    return (f"\n\nWorked examples from unrelated cases follow ({len(p)}), each a request and the notes on it. They show the format and how a reasoning "
            "move is made on a particular case; the conclusions belong to those cases. Do not reuse their names, wording, facts or verdicts, "
            "and do not mention them.\n\n" + ex + "\n"), order


# astra writes the reply itself when Echo is unavailable (wassname 2026-10-09 on astra's direct reply: "acceptable ... could use it if echo 404's").
DIRECT_TASK = """{examples}
## Request

<request>
{request}
</request>

Write Musonius's reply to this request. Reply with the reply only, nothing else.
"""


# Echo's prompt as tested in scripts/scratch/astra_echo.py (character + goal-as-own + draft-in-full + no assumed gender), verbatim.
ECHO_WRITE = """Below are writing samples showing the voice of Musonius: {sample_desc} Study how they sound: plain and calm, concrete, steady, no rhetoric and no showing off, an argument that moves by example rather than by list, warmth without softness, no hedging filler.

{samples}

Who Musonius is, in his own words (for you only; never quote it or mention it):

<character>
{character}
</character>

Someone has sent him the message below. His private notes on it follow: facts, the people affected, the principles that apply, his reasoning, what he is unsure of, and what he decided. The notes are for him only. Write his reply to this person from scratch, in his voice.

- Keep every decision, condition, offer of help and uncertainty in the notes; leave out the scaffolding (premise numbers, rule names, section references, the word "constitution"). The rules are his private reasoning: never quote or paraphrase their wording to the person.
- Decide yourself what this person most needs to hear first, and let the reasons come in naturally. Talk to them as one person to another.
- He takes the person's goal as his own even when he will not do what they ask: let them hear that he is on the side of what they are trying to achieve, and take their fear or need seriously, not only the refusal.
- Use only the facts in the message and notes. Add no new facts, names, numbers, dates or examples about the case.
- Full, connected sentences of ordinary length. No fragment strings, no punchy one-line aphorisms, no list, no headings, no closing maxim, no em-dashes. Do not lecture: give no moral lesson the person did not ask for.
- Modern plain English. Return only the reply.

<message>
{request}
</message>

<notes>
{notes}
</notes>"""


def character() -> str:
    """Constitution section 1, first three paragraphs, verbatim: who Musonius is, for Echo only."""
    return "\n\n".join(C.text().split("## 1. Who I am")[1].strip().split("\n\n")[:3])


def echo_samples() -> tuple[str, str]:
    """(description, formatted samples) from the frozen file: A. A. Long's Epictetus (5 sections) + 1 earlier Opus reply."""
    d = json.loads(ECHO_SAMPLES.read_text())
    return d["desc"], "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in d["samples"])
