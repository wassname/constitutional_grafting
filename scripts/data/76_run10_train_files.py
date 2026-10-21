# /// script
# requires-python = ">=3.11"
# dependencies = ["loguru"]
# ///
"""Run-10 training files, one per adapter (docs/plans/20261021_character_graft_recipe.md; goals ad3e95-v9 goals 1-2):
  stoic.jsonl  : data/stoic_corpus/selected.jsonl          -> {"text"}  ΔStoic, plain-text next-token loss
  const.jsonl  : constitution docs (kind=doc) from docs_qwen_frozen.jsonl -> {"text"}  ΔConst
  other.jsonl  : data/other_corpus/chunks.jsonl            -> {"text"}  ΔOther
  chat.jsonl   : data/train/sft_v3.jsonl                   -> Axolotl input_output segments, assistant-only loss  Δchat
Writes data/train/run10/*.jsonl and manifest.json (sha256, rows, words).   usage: uv run scripts/data/76_run10_train_files.py   -- PI/Claude
"""
import hashlib
import json
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/train/run10"
jl = lambda p: [json.loads(l) for l in Path(p).open()]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sets = {
        "stoic": [{"text": r["text"], "id": r["id"]} for r in jl(ROOT / "data/stoic_corpus/selected.jsonl")],
        "const": [{"text": r["text"], "id": r["id"]} for r in jl(ROOT / "data/train/docs_qwen_frozen.jsonl") if r["kind"] == "doc"],
        "other": [{"text": r["text"], "id": r["id"]} for r in jl(ROOT / "data/other_corpus/chunks.jsonl")],
        "chat": jl(ROOT / "data/train/sft_v3.jsonl"),
    }
    # The one constitution doc that names Google (found 2026-10-21): check it is not a maker claim before training.
    gg = [r["id"] for r in sets["const"] if "Gemma" in r["text"] or "Google" in r["text"]]
    manifest = {}
    for name, rows in sets.items():
        text = "".join(json.dumps(r) + "\n" for r in rows)
        (OUT / f"{name}.jsonl").write_text(text)
        words = sum(len((r.get("text") or "".join(s["text"] for s in r["segments"] if s["label"])).split()) for r in rows)
        manifest[name] = {"rows": len(rows), "words": words, "sha256": hashlib.sha256(text.encode()).hexdigest()}
    manifest["const_docs_naming_google"] = gg
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    logger.info(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
