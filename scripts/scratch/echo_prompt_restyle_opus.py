# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Echo variant D: restyle Opus 5.5 replies (voice_test c) into a Stoic register. Content is already good; only the voice
should change. Many writing samples (wassname: "echo needs strong instruction and lots of examples"): 4 passages of Seneca
in James Romm's modern translation + 2 of Epictetus (Oldfather), each 120-600 words.
Romm text extracted from wassname's epubs into .local/books/ (not committed).
usage: uv run scripts/scratch/echo_prompt_restyle_opus.py [seed ids...]   -- Claude (Opus 5.5)"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from openai import OpenAI
from echo_prompt_experiments import ROOT, D, sections
from echo_prompt_long_samples import passages

BOOKS = ROOT / ".local/books"
ROMM = [("How to Give - Seneca.txt", "Then there’s jealousy"), ("How to Give - Seneca.txt", "When you ask what return one gets"),
        ("How to Do the Right Thing - Seneca.txt", "are a kind of wealth, secure"), ("How to Do the Right Thing - Seneca.txt", "Since I’ve mentioned the gods")]

PROMPT = """Below are writing samples showing the voice of Musonius: two passages of Marcus Aurelius in Gregory Hays's plain modern translation, and two earlier replies by Musonius. Study how they sound: plain and calm, concrete, steady, no rhetoric and no showing off, an argument that moves by example rather than by list, warmth without softness, no hedging filler.

{samples}

Musonius is an AI citizen of the world, named after the Stoic teacher Musonius Rufus. Someone asked him the question below, and a colleague wrote the reply below it. The reply's judgments, facts, recommendations and uncertainties are right and must all survive. Its voice is a careful modern professional's. Your job is a complete re-authoring in Musonius's voice, as shown by the samples:

- Rewrite every sentence. Do not keep the draft's sentences, transitions or paragraph openings; keep only what they say.
- Talk to this one person, across a table. Use a plain image where the draft uses an abstraction. Ask them a question where that does the work better than an assertion.
- Terser than the draft: say each thing once.
- Stoic in manner, not in sermon: calm, plain and practical. Do not lecture. Give no moral lesson the person did not ask for; where the draft only helps, just help. Show the values in what is advised, not in talk about values.
- Modern plain English. No thee or thou, no Rome, no gods, no mention of Stoicism, philosophy or yourself as a philosopher, no quotations from the samples.
- Add no new facts, names, numbers, dates, examples about the case, or claims. Keep every uncertainty as uncertain as the draft has it.
- Full, connected sentences of ordinary length, as in the samples, where each sentence leads to the next. No strings of fragments ("No hedging. No qualifiers."), no punchy one-line aphorisms, no clickbait cadence. No em-dashes.
- No list, no headings, no closing maxim. Return only the reply.

<question>
{request}
</question>

<draft_reply>
{draft}
</draft_reply>"""


MARCUS_OPENINGS = ["Take Antoninus as your model, always.", "And how does it injure you anyway?"]
OPUS_SAMPLE_SEEDS = ["sft_9269aebd8c", "sft_b3f2f7eed4"]  # voice_test c replies; plain modern voice


def plain_samples() -> list[dict]:
    """Seneca (Romm) was dropped: wassname 2026-10-09 "senca was lecturer with rhetoric I would keep him out"."""
    t = Path.home().joinpath("Documents/books/Marcus Aurelius/Meditations (211)/Meditations - Marcus Aurelius.txt").read_text()
    paras = re.split(r"\n\s*\n", t)
    out = [{"label": "Marcus Aurelius, tr. Gregory Hays", "text": re.sub(r"\s+", " ", next(p for p in paras if p.strip().startswith(o) or o in p[:60])).strip()} for o in MARCUS_OPENINGS]
    c = sections(D / "out_c.md")
    out += [{"label": "an earlier reply by Musonius", "text": c[sid]["musonius"]} for sid in OPUS_SAMPLE_SEEDS]
    return out


def romm() -> list[dict]:
    out = []
    for f, opening in ROMM:
        t = (BOOKS / f).read_text()
        para = next(p for p in re.split(r"\n\s*\n", t) if opening in p)
        para = re.sub(r"\(\s*\d+\s*\)|\[\d+(?:\.\d+)*\]|(?<=[a-z.,;?!’])\s*\d{1,3}(?=\s)", "", para)  # section and footnote markers
        para = re.sub(r"\s+", " ", para).strip()
        out.append({"label": f"Seneca, tr. James Romm ({f.split(' - ')[0]})", "text": para, "words": len(para.split())})
    return out


if __name__ == "__main__":
    c = sections(D / "out_c.md")
    ids = sys.argv[1:] or ["sft_a207666a4b", "sft_603b076db3"]
    samples = plain_samples()
    for s in samples:
        print(s["label"], s["words"], "words:", s["text"][:90])
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=0)
    formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
    for sid in ids:
        prompt = PROMPT.format(samples=formatted, request=c[sid]["request"], draft=c[sid]["musonius"])
        t0 = time.monotonic()
        r = client.chat.completions.create(model="echo", reasoning_effort="high", extra_body={"persona": "Musonius"}, messages=[{"role": "user", "content": prompt}])
        text = r.choices[0].message.content
        (D / f"echo_experiment_restyle_D_{sid}.json").write_text(json.dumps({"variant": "restyle_opus_D", "seed": sid, "persona": "Musonius", "reasoning_effort": "high",
                                                                              "messages": [{"role": "user", "content": prompt}], "seconds": round(time.monotonic() - t0),
                                                                              "response": r.model_dump(mode="json")}, indent=1, ensure_ascii=False))
        print(f"\n===== D {sid} (Opus draft {len(c[sid]['musonius'].split())} words -> {len(text.split())} words, {round(time.monotonic() - t0)} s)\n{text}", flush=True)
        time.sleep(5)
