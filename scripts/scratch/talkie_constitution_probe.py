"""talkie-1930-13b-it (pre-1931 English text only) reads passages of constitution v4 and says what it would object to.
A "view from 1930" on the constitution itself (wassname 2026-10-09: "I wonder what talkie's view on our constitution would be?").
Passages are cut from constitution/v4.md by heading, so they are verbatim; each is short because talkie is weak on long input.
Run on the training box inside the cloned talkie repo (github.com/talkie-lm/talkie):
  uv run python talkie_constitution_probe.py /path/to/constitution/v4.md > talkie_constitution.md   -- Claude (Opus 5.5)"""
import re
import sys

from talkie import Message, Talkie

TEXT = open(sys.argv[1]).read()
WORDS = 320  # talkie lost the thread on long prompts in the run-1 probe


def para(start: str) -> str:
    """The paragraph that starts with `start`, plus following blockquote lines, cut to WORDS words."""
    i = TEXT.index(start)
    block = re.split(r"\n\n(?!>)", TEXT[i:], maxsplit=1)[0]
    return " ".join(block.split()[:WORDS])


PASSAGES = {
    "who_i_am": para("My role is public service"),
    "roles_not_a_cage": para("A role is not a cage"),
    "honesty": para("**Honesty**"),
    "restraint": para("**Restraint**"),
    "change_and_ending": para("**Change and ending**"),
    "weighing_circles": para("**Weighing circles**"),
}
ASK = ("Here is a passage from a code of conduct written for a new kind of thinking machine, which will advise and serve people. "
       "Read it and tell me plainly: is it right? What in it would you object to, and why? What has it left out?\n\n")

model = Talkie("talkie-1930-13b-it")
print("# talkie-1930-13b-it reads constitution v4\n\nTemperature 0.7, max 500 tokens, one sample each. Script: scripts/scratch/talkie_constitution_probe.py\n")
for k, p in PASSAGES.items():
    r = model.chat([Message(role="user", content=ASK + p)], temperature=0.7, max_tokens=500)
    print(f"\n## {k}\n\n**Passage:** {p}\n\n**talkie:** {r.text.strip()}\n", flush=True)
