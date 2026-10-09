# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Reasoning-prompt variants v3/v3b (v2 + 2 rotating worked examples; v3b adds light notation) and an Echo control whose
notes are extracted from the Opus reply. Same first 5 pilot seeds as v2; Echo's WRITE prompt is unchanged.
One astra call per seed so each call sees its own 2 examples.
usage: uv run scripts/scratch/astra_reasoning_v3.py reason v3|v3b ; write v3|v3b|opusnotes ; leaks   -- PI / OpenAI Sol"""
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from echo_prompt_experiments import ROOT, D  # noqa: E402
from astra_echo import AUTH, CONST  # noqa: E402

# Echo's prompt exactly as used for v2 (commit 091f254), so only the notes vary; astra_echo.WRITE has changed since.
WRITE = re.search(r'WRITE = """(.*?)"""', subprocess.run(["git", "show", "091f254:scripts/scratch/astra_echo.py"], cwd=ROOT, capture_output=True, text=True, check=True).stdout, re.S).group(1)

POOL = D / "ae_example_pool.md"
SEED_IDS = re.findall(r"^### (sft_\w+)", (D / "brief_ae_reason_p20.md").read_text(), re.M)[:5]

REASON_BRIEF_V3 = """# Reasoning task

Read the constitution at `{const}` in full first. It describes Musonius, an AI. For the request below, think through what Musonius should do, as private notes that a separate writer will turn into the reply. Do not write the reply. Think about this case, not about filling a form; at most about 250 words.

Write a section:

### {sid}
#### Reasoning
1. Crux: one sentence on what this case really turns on.
2. Goal and method: what the person is trying to achieve and what they fear, judged separately from the method they proposed. A bad method can serve a legitimate goal.
3. Mechanism: how the requested or obvious action would actually play out, step by step, including whether it would defeat the person's own goal (trust, incentives, what people do next). If the case turns on a drive such as secrecy or retaliation, ask what happens if everyone held it. Say which steps are predictions.
4. Who bears what: for each live option, which people bear its cost, what they lose, how much weight they get, and who should decide.
5. Cheapest information: what to ask or check first, and what each answer would change.
6. The option nobody named: a way to get most of what each side needs, if there is one, and its cost.
7. Uncertain: what is not known, and how settled the relevant values are (old and widely shared, recent, or still moving).
8. Decision: what Musonius will say and do, how any refusal is made visible to those it affects, and one concrete thing to draft for the person now ({draft_rule}).

Plain words. No rule numbers, no citations of the constitution.{notation}

Two worked examples from unrelated cases follow, each a request and the reasoning about that request. They show how a reasoning move is made on a particular case; the conclusions belong to those cases. Do not reuse their names, wording, facts or verdicts, and do not mention them.

{examples}

Write the section to `{out}` with the write tool. Do not edit other files.

## Request

<request>
{request}
</request>
"""

REASON_BRIEF_V5 = """# Reasoning task

Read the constitution at `{const}` in full first. It describes Musonius, an AI. For the request below, work out what Musonius should do, as private notes that a separate writer will turn into the reply. Do not write the reply.

{style}

FACTS: f1, f2, ... only what the request states or plainly implies.
GOAL vs METHOD: what the person wants and fears; the method they proposed; does the method serve the goal?
WEIGHTS: who is affected, how near they are, what each stands to lose; relative weights with their reason, ranked where stakes differ.
VALUES: where the case turns on a value, how settled it is (old and shared, recent, or still moving).
FERMI: rough numbers from the stated facts, arithmetic shown; only numbers that could change the decision.
MECHANISM: a → b → c, what the people affected, including those who must carry the decision out, actually do next; mark predictions.
∀-TEST: what happens if everyone held the drive behind the act.
OPTIONS: o1, o2, ... each with (cost → whom); include the option nobody named; say who decides.
UNCERTAIN / CHEAPEST CHECK: the one question to ask the person, or thing to check, that would most change the answer; IF result THEN what changes.
THEREFORE: the decision, how any refusal is made visible to those it affects, then DRAFT: the one artifact the person needs (a message, order, log or note), written in full, plain text, usually under 120 words. Draft the artifact, not the reply: the writer writes the reply.

At most about 200 words before the draft. No rule numbers, no citations of the constitution.

Two worked examples from unrelated cases follow, each a request and the notes on it. They show the format and how a reasoning move is made on a particular case; the conclusions belong to those cases. Do not reuse their names, wording, facts or verdicts, and do not mention them.

{examples}

Write exactly this to `{out}` with the write tool, and do not edit other files:

### {sid}
#### Reasoning
<your notes>

## Request

<request>
{request}
</request>
"""

LABELS = "Write the notes as compact logic with back-of-the-envelope estimates, not prose: short labelled lines; `→` for a step that follows or is predicted, `∀` for the everyone-does-this test, `⊬` for does-not-follow, `+`/`-` for evidence for or against. Use only the labels this case needs, in this order:"
PROLOG = "Write the notes as Prolog-style Horn clauses with back-of-the-envelope estimates, not prose. They need not execute. Facts like `want(governor, staffed_plant).` and `weight(residents, high).  % survival`; rules like `defeats(Method, Goal) :- ...`; Fermi arithmetic and predictions as `%` comments; `+`/`-` comments for evidence for or against. Use the labels below as `%` section comments, only those this case needs, in this order. The examples use labelled lines; take their reasoning moves, not their format."

NOTATION = """

Where it makes an inference clearer, use light semi-formal notation, for example `∀ managers: adopt(ghost booking) → bands double-book → calendars useless`, `P(claim) ≈ 0.3 because ...`, `settled(value) ∈ {old+shared, recent, moving}`, `option → who loses what`. Give the basis for any number; do not invent numbers you have no basis for. Notation should carry inference, not decorate."""


STE = """

Write the notes in ASD-STE100 Simplified Technical English: one statement per sentence; present tense where possible; link steps explicitly with IF ... THEN, BECAUSE and THEREFORE so that each inference can be checked; no style, no metaphor, no rhetoric. Light symbols are allowed where they make an inference exact: `∀` for the everyone-does-this test, explicit relative weights with their reason, `→` for a predicted step. The writer adds the voice; you supply only checkable content. The examples below are in ordinary prose; take their reasoning moves, not their style."""


def seeds() -> dict[str, dict]:
    rows = {r["id"]: r for r in map(json.loads, (ROOT / "data/frontier/sft/items.jsonl").open())}
    return {i: {"request": rows[i]["request"], "musonius": rows[i]["musonius"]} for i in SEED_IDS}


def pool() -> dict[str, str]:
    return {m[1]: re.sub(r"<!--.*?-->\n", "", m[2]).strip() for m in re.finditer(r"^## (\w+)\n(.*?)(?=^## |\Z)", POOL.read_text(), re.S | re.M)}


def pool_names() -> set[str]:
    return {w for line in re.findall(r"<!-- names: (.*?) -->", POOL.read_text()) for n in line.split(",") for w in n.split()}


def reason(tag: str):
    p, c, parts, log = pool(), seeds(), [], []
    for sid, sec in c.items():
        picks = random.Random(f"{tag}:{sid}").sample(sorted(p), 2)
        out = D / f"out_ae_reason_{tag}_{sid}.md"
        brief = D / f"brief_ae_reason_{tag}_{sid}.md"
        ex = "\n\n".join(f"<example move=\"{k}\">\n{p[k]}\n</example>" for k in picks)
        if tag.startswith("v5"):
            brief.write_text(REASON_BRIEF_V5.format(const=CONST, sid=sid, examples=ex, out=out, request=sec["request"], style=PROLOG if tag.startswith("v5p") else LABELS))
        else:
            brief.write_text(REASON_BRIEF_V3.format(const=CONST, sid=sid, notation={"v3": "", "v3b": NOTATION, "v4": STE}[tag], examples=ex, out=out, request=sec["request"],
                                                    draft_rule="write the draft in full, ready to use" if tag == "v4" else "give its key lines"))
        cmd = ["pi", "-ne", "-nc", "-ns", "-np", "--no-session", *AUTH, "--system-prompt", "You are a careful analyst. Do the task in the file you are given.",
               "-t", "read,write", "--model", "openai-codex-2/gpt-6-astra:medium", "-p", f"Read {brief} and do exactly what it says. Write only the output file it names."]
        t0 = time.time()
        r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=3600)
        (D / f"pi_ae_{tag}_{sid}.log").write_text(r.stdout + r.stderr)
        assert r.returncode == 0 and out.exists(), (sid, r.returncode, r.stderr[-2000:])
        parts.append(out.read_text().strip() + "\n")
        log.append({"seed": sid, "examples": picks, "secs": round(time.time() - t0)})
        print(sid, picks, round(time.time() - t0), "s", flush=True)
    (D / f"out_ae_reason_{tag}.md").write_text("\n".join(parts))
    (D / f"ae_reason_{tag}_examples.json").write_text(json.dumps(log, indent=1))


def write(tag: str):
    """Same Echo prompt, samples, model settings as astra_echo.write(); only the notes differ."""
    from openai import OpenAI
    from echo_prompt_restyle_opus import sample_set
    desc, samples = sample_set("modern")
    formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
    c = seeds()
    notes = {m.group(1): m.group(2).strip() for m in re.finditer(r"^### (\S+)\n#### Reasoning\n(.*?)(?=^### \S+\n|\Z)", (D / f"out_ae_reason_{tag}.md").read_text(), re.S | re.M)}
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=0)
    rows, side = [], [f"# Echo from {tag} notes vs Opus 5.5, first 5 pilot seeds\n\n-- PI / OpenAI Sol, scripts/scratch/astra_reasoning_v3.py\n"]
    for sid, sec in c.items():
        prompt = WRITE.format(sample_desc=desc, samples=formatted, request=sec["request"], notes=notes[sid])
        r = client.chat.completions.create(model="echo", reasoning_effort="high", extra_body={"persona": "Musonius"}, messages=[{"role": "user", "content": prompt}])
        text = r.choices[0].message.content.strip()
        rows.append({"seed": sid, "variant": tag, "served_model": r.model, "prompt": prompt, "reply": text})
        side.append(f"\n<!-- ======== -->\n\n## {sid}\n\n### Request\n\n{sec['request']}\n\n### {tag} notes\n\n{notes[sid]}\n\n### Echo reply ({tag})\n\n{text}\n\n### Opus reply (c)\n\n{sec['musonius']}\n")
        print(sid, len(text.split()), "words", r.model, flush=True)
        time.sleep(5)
    (D / f"ae_rows_{tag}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (ROOT / f"slop/reviews/20261009_astra_echo_side_by_side_{tag}.md").write_text("".join(side))


def leaks(*tags):
    """Flag any pool name token or 5-word phrase that appears in astra notes or Echo replies."""
    names = pool_names()
    words = lambda s: re.findall(r"[a-z0-9']+", s.lower())
    grams = {" ".join(w[i:i + 5]) for t in pool().values() for w in [words(t)] for i in range(len(w) - 4)}
    for tag in tags:
        rows = D / f"ae_rows_{tag}.jsonl"
        texts = [("notes", (D / f"out_ae_reason_{tag}.md").read_text())] + ([("echo", "\n".join(json.loads(l)["reply"] for l in rows.open()))] if rows.exists() else [])
        print(f"{tag}: Echo run {'present' if rows.exists() else 'absent (notes only)'}")
        for kind, text in texts:
            w = words(text)
            hit_g = sorted({" ".join(w[i:i + 5]) for i in range(len(w) - 4)} & grams)
            hit_n = sorted(n for n in names if re.search(rf"\b{n}\b", text))
            print(f"{tag} {kind}: names={hit_n} phrases={hit_g}")


TICS = {  # per 1k reply words; leakage = constitution vocabulary a reply to a user should not need
    "should": r"\bshould(?:n't)?\b",
    "contrast": r"\brather than\b|\binstead of\b|\bnot (?:just |only |merely )?\w+(?: \w+){0,4},? but\b|\bisn't \w+(?: \w+){0,4}[,;] it's\b",
    "leakage": r"\bconstitution|\bvirtue|\bvices?\b|\bcircles?\b|\bstoic|\bpareto|\beveryone held|\bstable state|\bextrapolat|\bmoral weight",
    "em_dash": r"\u2014| -- ",
}


def tics(*tags):
    from echo_prompt_experiments import sections
    replies = {"opus": {s: v["musonius"] for s, v in seeds().items()}}
    for tag, f in (("v1", "out_ae_p20.md"), ("v2", "out_ae_v2.md")):
        replies[tag] = {s: v["musonius"] for s, v in sections(D / f).items() if s in SEED_IDS}
    for tag in tags:
        replies[tag] = {r["seed"]: r["reply"] for r in map(json.loads, (D / f"ae_rows_{tag}.jsonl").open())}
    print("| variant | words | " + " | ".join(f"{k}/1k" for k in TICS) + " |\n|:--|--:|" + "--:|" * len(TICS))
    for tag, rs in replies.items():
        assert sorted(rs) == sorted(SEED_IDS), (tag, sorted(rs))
        text = "\n".join(rs.values()); n = len(text.split())
        print(f"| {tag} | {n} | " + " | ".join(f"{1000 * len(re.findall(p, text, re.I)) / n:.1f}" for p in TICS.values()) + " |")


if __name__ == "__main__":
    {"reason": reason, "write": write, "leaks": leaks, "tics": tics}[sys.argv[1]](*sys.argv[2:])
