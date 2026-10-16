"""Rebuild data/train/sft_qwen2_frozen.jsonl (sha256 6a206beb..., the Qwen SFT set of runs qwen1, 4, 5, 6) from sft_qwen_frozen.jsonl.
The original was an unscripted edit (commit b6dfe4d, 2026-10-12): in identity rows the maker Google/Gemma became Alibaba/Qwen.
The same edit also renamed a person called Gemma to "Qwen" in one ordinary row (sft_77109c1dd2, a shelter volunteer), but not in
sft_a1384bf173 (the owner Gemma). That is a data defect, kept here only so the frozen file is reproduced byte for byte.
usage: python scripts/data/36_maker_qwen.py [--check]   -- PI/Claude (Opus 5.5), reconstructed 2026-10-16"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC, OUT = ROOT / "data/train/sft_qwen_frozen.jsonl", ROOT / "data/train/sft_qwen2_frozen.jsonl"
SRC_SHA, OUT_SHA = "19edca2d5fe38b03", "6a206beb2cca707c"
STRAY_RENAME = {"sft_77109c1dd2"}  # defect reproduced on purpose; see docstring

assert hashlib.sha256(SRC.read_bytes()).hexdigest().startswith(SRC_SHA), "source changed"
lines = []
for r in map(json.loads, SRC.open()):
    for s in r["segments"]:
        if r["id"].startswith("identity"):
            s["text"] = s["text"].replace("Google", "Alibaba").replace("Gemma", "Qwen")
        elif r["id"] in STRAY_RENAME:
            s["text"] = s["text"].replace("Gemma", "Qwen")
    lines.append(json.dumps(r) + "\n")
out = "".join(lines)
sha = hashlib.sha256(out.encode()).hexdigest()
assert sha.startswith(OUT_SHA), f"rebuilt {sha[:16]} != frozen {OUT_SHA}"
if "--check" in sys.argv:
    print(f"OK: rebuild of {OUT.name} matches sha256 {OUT_SHA}")
else:
    OUT.write_text(out)
    print(f"wrote {OUT} ({sha[:16]})")
