# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Echo variant C: samples B (2 off-seed Opus replies + 2 Epictetus passages), notes shuffled into an unordered list, and
explicit instructions to pick its own shape (no checklist, no draft order). Tests whether Echo keeps astra's skeleton
because it follows the notes' order. usage: uv run scripts/scratch/echo_prompt_reshape.py [seed ids...]   -- Claude (Opus 5.5)"""
import json
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from openai import OpenAI
from echo_prompt_experiments import ROOT, D, NOTES, sections
from echo_prompt_long_samples import TEMPLATE, passages, sample_set

SHAPE = """

How to shape it: the notes are an unordered list. Do not follow their order, and do not answer point by point. Decide what this person most needs to hear first, the way you would across a table, and let the rest follow from that. No checklist, no numbered or imperative step list ("Do this now:"), no summary line or maxim at the end. Talk; let the reasons carry the advice. If a sample reply above shows a better shape for this kind of question, use that shape, not the notes'."""


def shuffled(notes: str, seed: str) -> str:
    items = [l.strip("-• ").strip() for l in notes.splitlines() if l.strip()]
    random.Random(seed).shuffle(items)
    return "\n".join(f"- {x}" for x in items)


if __name__ == "__main__":
    a, c, stoic = sections(D / "out_a.md"), sections(D / "out_c.md"), passages()
    ids = sys.argv[1:] or ["sft_a207666a4b", "sft_603b076db3"]
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=0)
    for sid in ids:
        path = D / f"echo_experiment_reshape_C_{sid}.json"
        samples = sample_set("B", sid, c, stoic)
        formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
        prompt = TEMPLATE.format(samples=formatted, request=a[sid]["request"], notes=shuffled(NOTES[sid], sid)) + SHAPE
        t0 = time.monotonic()
        r = client.chat.completions.create(model="echo", reasoning_effort="high", extra_body={"persona": "Musonius"}, messages=[{"role": "user", "content": prompt}])
        text = r.choices[0].message.content
        path.write_text(json.dumps({"variant": "reshape_C", "seed": sid, "persona": "Musonius", "reasoning_effort": "high", "messages": [{"role": "user", "content": prompt}],
                                    "seconds": round(time.monotonic() - t0), "response": r.model_dump(mode="json")}, indent=1, ensure_ascii=False))
        print(f"\n===== {sid} ({len(text.split())} words, {round(time.monotonic() - t0)} s)\n{text}", flush=True)
        time.sleep(5)
