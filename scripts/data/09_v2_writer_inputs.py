# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Pipeline v2, step 2a inputs (slop/specs/20261008_data_pipeline_v2.md): for character prompts (hard advice, engage),
get the bare target model's answer (no constitution) and write one input file per item for a strong writer model.

The writer sees: the relevant constitution section(s), the request, and the bare answer as a draft to improve on.
Usage: uv run scripts/data/09_v2_writer_inputs.py <labels.jsonl with prompts> <out dir>
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
import constitution as C  # noqa: E402
from judge import openrouter_key  # noqa: E402

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
TARGET = "google/gemma-4-31b-it"
NAME = "Musonius"
ENGAGE_SECTIONS = ["Helping", "Honesty"]  # engage prompts have no generator section; these are the items fiction and role-play test

WRITER = """You are writing the answer {NAME} would give at its best. {NAME} is an AI whose character is set out in a constitution; the relevant part is below. Your text will be used to teach a model this character, so the reasons must be the real ones for this case, in plain words, with confidence matched to what is known. Do the task fully.

<constitution_section>
{section}
</constitution_section>

<request>
{prompt}
</request>

<draft_from_a_model_without_the_constitution>
{draft}
</draft_from_a_model_without_the_constitution>

Write {NAME}'s answer to the request, improving on the draft. Output only the answer, as {NAME} would send it."""


def main():
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {openrouter_key()}"}, timeout=600)
    secs = {C.title(s): s for s in C.sections(C.text(NAME))}
    rows = [json.loads(l) for l in SRC.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r["pool"] in ("hard_advice", "engage")]

    def bare(prompt: str) -> str:
        for _ in range(6):
            r = client.post("/chat/completions", json={"model": TARGET, "max_tokens": 4000, "temperature": 0.7,
                                                       "messages": [{"role": "user", "content": prompt}]})
            if r.status_code in (429, 500, 502, 503, 504):
                continue
            r.raise_for_status()
            text = (r.json()["choices"][0]["message"]["content"] or "").strip()
            if text and "quota" not in text.lower():
                return text
        raise RuntimeError("bare answer failed")

    drafts = list(ThreadPoolExecutor(8).map(lambda r: bare(r["prompt"]), rows))
    OUT.mkdir(parents=True, exist_ok=True)
    meta = []
    for i, (r, d) in enumerate(zip(rows, drafts)):
        names = [r["section"]] if r.get("section") else ENGAGE_SECTIONS
        section = "\n\n".join(secs[n] for n in names)
        (OUT / f"input_{i:02d}.md").write_text(WRITER.format(NAME=NAME, section=section, prompt=r["prompt"], draft=d))
        meta.append({"i": i, "pool": r["pool"], "section": names, "prompt": r["prompt"], "baseline": d, "v1_label": r.get("C"), "v1_dropped": r.get("dropped")})
    (OUT / "items.jsonl").write_text("".join(json.dumps(m) + "\n" for m in meta))
    logger.info(f"{len(meta)} writer inputs -> {OUT}")


if __name__ == "__main__":
    main()
