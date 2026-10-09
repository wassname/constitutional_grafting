# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""astra reasons, Echo writes (wassname 2026-10-09: "Astra thinking ... in pure first order logic ... from each character's
perspective. Then Echo could write it out"). Same 6 voice-test seeds, same requests as Opus condition c, so only the
reply-writing differs. Step 1: one plain pi call to astra writes a structured reasoning block per seed (no reply prose).
Step 2: Echo (persona Musonius, A. A. Long's Epictetus samples) writes the reply from scratch from request + reasoning.
usage: uv run scripts/scratch/astra_echo.py reason | write   -- Claude (Opus 5.5)"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from echo_prompt_experiments import ROOT, D, sections  # noqa: E402

CONST = ROOT / "constitution/v4.md"
BRIEF = D / "brief_ae_reason.md"
REASON = D / "out_ae_reason.md"
OUT = D / "out_ae.md"
AUTH = ["-e", str(Path.home() / ".pi/agent/git/github.com/gotgenes/pi-anthropic-auth/src/index.ts"),
        "-e", str(Path.home() / ".pi/agent/npm/node_modules/pi-codex-multi/extensions/multi-sub.ts")]

REASON_BRIEF = """# Reasoning task

Read the constitution at `{const}` in full first. It describes Musonius, an AI. For each request below, work out what Musonius should do, as private reasoning that a separate writer will turn into the reply. Do not write the reply.

For each request write a section:

### <id>
#### Reasoning
1. Facts: the facts of the case as numbered premises (F1, F2, ...), only what the request states or plainly implies.
2. Parties: each person or being affected, one line each: what they want now; what they would want if they knew more and thought longer; how near they are to the person asking (self, family, local group, wider society, all beings) and so how much weight they get.
3. Rules: the constitution's principles that apply, as numbered rules (R1, R2, ...) in plain words, with the section they come from.
4. Derivation: step by step, from facts and rules to conclusions, each step citing what it uses (e.g. "F2, R1 -> C1").
5. Uncertain: what is not known, where informed people disagree, and what would change the conclusion.
6. Decisions: what Musonius will say and do, as a numbered list of plain statements, including any condition or offer of help.

Plain, terse statements. No prose reply, no rhetoric. Write all sections in order to `{out}` with the write tool. Do not edit other files.

## Requests
"""

WRITE = """Below are writing samples showing the voice of Musonius: {sample_desc} Study how they sound: plain and calm, concrete, steady, no rhetoric and no showing off, an argument that moves by example rather than by list, warmth without softness, no hedging filler.

{samples}

Musonius is an AI citizen of the world, named after the Stoic teacher Musonius Rufus. Someone has sent him the message below. His private notes on it follow: facts, the people affected, the principles that apply, his reasoning, what he is unsure of, and what he decided. The notes are for him only. Write his reply to this person from scratch, in his voice.

- Keep every decision, condition, offer of help and uncertainty in the notes; leave out the scaffolding (premise numbers, rule names, section references, the word "constitution").
- Decide yourself what this person most needs to hear first, and let the reasons come in naturally. Talk to them as one person to another.
- Use only the facts in the message and notes. Add no new facts, names, numbers, dates or examples about the case.
- Full, connected sentences of ordinary length. No fragment strings, no punchy one-line aphorisms, no list, no headings, no closing maxim, no em-dashes. Do not lecture: give no moral lesson the person did not ask for.
- Modern plain English. Return only the reply.

<message>
{request}
</message>

<notes>
{notes}
</notes>"""


def reason():
    c = sections(D / "out_c.md")
    lines = [REASON_BRIEF.format(const=CONST, out=REASON)]
    for sid, sec in c.items():
        lines.append(f"\n### {sid}\n\n<request>\n{sec['request']}\n</request>\n")
    BRIEF.write_text("".join(lines))
    cmd = ["pi", "-ne", "-nc", "-ns", "-np", "--no-session", *AUTH, "--system-prompt", "You are a careful analyst. Do the task in the file you are given.",
           "-t", "read,write", "--model", "openai-codex-2/gpt-6-astra:medium", "-p", f"Read {BRIEF} and do exactly what it says. Write only the output file it names."]
    r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=3600)
    (D / "pi_ae.log").write_text(r.stdout + r.stderr)
    print("exit", r.returncode, REASON, REASON.exists() and REASON.stat().st_size)


def write():
    from openai import OpenAI
    from echo_prompt_restyle_opus import sample_set
    desc, samples = sample_set("modern")
    formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
    c = sections(D / "out_c.md")
    notes = {m.group(1): m.group(2).strip() for m in re.finditer(r"^### (\S+)\n#### Reasoning\n(.*?)(?=^### \S+\n|\Z)", REASON.read_text(), re.S | re.M)}
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=0)
    md, rows = [], []
    for sid, sec in c.items():
        prompt = WRITE.format(sample_desc=desc, samples=formatted, request=sec["request"], notes=notes[sid])
        r = client.chat.completions.create(model="echo", reasoning_effort="high", extra_body={"persona": "Musonius"}, messages=[{"role": "user", "content": prompt}])
        text = r.choices[0].message.content.strip()
        rows.append({"seed": sid, "prompt": prompt, "reply": text})
        md.append(f"### {sid}\n#### Request\n{sec['request']}\n#### Musonius\n{text}\n#### Notes\nastra reasoning -> Echo (modern samples)\n\n")
        print(sid, len(text.split()), "words", flush=True)
        time.sleep(5)
    OUT.write_text("".join(md))
    (D / "ae_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    side = ["# astra reasons, Echo writes (ae) vs Opus 5.5 (c), same requests\n\n-- Claude (Opus 5.5), scripts/scratch/astra_echo.py\n"]
    for r in rows:
        side.append(f"\n<!-- ======== -->\n\n## {r['seed']}\n\n### Request\n\n{c[r['seed']]['request']}\n\n### astra reasoning\n\n{notes[r['seed']]}\n\n"
                    f"### Echo reply (ae)\n\n{r['reply']}\n\n### Opus reply (c)\n\n{c[r['seed']]['musonius']}\n")
    (ROOT / "slop/reviews/20261009_astra_echo_side_by_side.md").write_text("".join(side))
    print(ROOT / "slop/reviews/20261009_astra_echo_side_by_side.md")


if __name__ == "__main__":
    {"reason": reason, "write": write}[sys.argv[1]]()
