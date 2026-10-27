# Teacher-tic rates per 1,000 words: generated training text vs human-written corpora vs the constitution.
# Usage: uv run --no-project python scripts/scratch/20261027_tic_rates.py -> slop/audits/20261027_corpus_habits/tic_rates.md  -- PI/Claude (opus-5-5), 2026-10-27
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
chat = ["".join(s["text"] for s in json.loads(l)["segments"] if s["label"]) for l in (ROOT / "data/train/eos_fixed/chatr12.jsonl").open()]
docs = {k: [json.loads(l)["text"] for l in (ROOT / f"data/train/run10/{k}.jsonl").open()] for k in ["const", "stoic", "other"]}
corpora = {"chat (generated)": chat, "const docs (generated)": docs["const"], "Stoic (human)": docs["stoic"],
           "other traditions (human)": docs["other"], "constitution v4": [(ROOT / "constitution/v4.md").read_text()]}
PATTERNS = {"honest / honestly / frankly": r"\bhonest(ly)?\b|\bfrankly\b", "plain / plainly": r"\bplain(ly)?\b",
            "quiet / quietly": r"\bquiet(ly)?\b", "weigh*": r"\bweigh(s|ed|ing)?\b", "worth": r"\bworth\b",
            "here's": r"\bhere's\b", "I won't": r"\bI won't\b", "em dash": "\u2014", "not ... but": r"\bnot\b[^.;]{1,40}\bbut\b"}
rows = ["| per 1,000 words | " + " | ".join(corpora) + " |", "|:--|" + "--:|" * len(corpora)]
for name, rx in PATTERNS.items():
    cells = []
    for texts in corpora.values():
        w = sum(len(t.split()) for t in texts)
        cells.append(f"{1000 * sum(len(re.findall(rx, t, re.I)) for t in texts) / w:.2f}")
    rows.append(f"| {name} | " + " | ".join(cells) + " |")
out = ROOT / "slop/audits/20261027_corpus_habits/tic_rates.md"
out.write_text("# Teacher-tic rates\n\nRegex counts per 1,000 whitespace words (case-insensitive). Generated = written by the teacher models; "
               "human = authentic books. Writer prompts use 'plain', 'weigh' and 'quiet' vocabulary too (configs/data/prompts/).\n\n"
               + "\n".join(rows) + "\n\n-- scripts/scratch/20261027_tic_rates.py\n")
print("\n".join(rows))
