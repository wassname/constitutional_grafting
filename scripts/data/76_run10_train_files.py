# /// script
# requires-python = ">=3.11"
# dependencies = ["loguru"]
# ///
"""Run-10 training files, one per adapter (docs/plans/20261021_character_graft_recipe.md; goals ad3e95-v9 goals 1-2):
  stoic.jsonl  : data/stoic_corpus/selected.jsonl          -> {"text"}  ΔStoic, plain-text next-token loss
  const.jsonl  : constitution docs (kind=doc) from docs_qwen_frozen.jsonl -> {"text"}  ΔConst
  other.jsonl  : data/other_corpus/chunks.jsonl            -> {"text"}  ΔOther
  chat.jsonl   : data/train/sft_v3.jsonl (all identity rows)  -> Axolotl input_output segments, assistant-only loss
  chat12.jsonl / chatgen12.jsonl : non-identity chats (+ general.jsonl) with identity sampled to 12% of trained words  Δchat (main)
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
    # One-sentence repairs of invented specifics from the fresh-sample loop (78_fresh_review.py screen_fix), applied to the trained reply
    edits = ROOT / "data/frontier/fresh_loop/edits.jsonl"
    by_id = {}
    for e in (jl(edits) if edits.exists() else []):
        by_id.setdefault(e["id"], []).append(e)
    n_applied = 0
    for r in sets["chat"]:
        for e in by_id.get(r["id"], []):
            seg = r["segments"][1]
            if e["old"] in seg["text"]:
                seg["text"] = seg["text"].replace(e["old"], e["new"], 1).replace("  ", " ").replace(" .", ".").replace(" ,", ",")
                n_applied += 1
    print(f"fresh-loop edits applied: {n_applied}/{sum(map(len, by_id.values()))}")
    # Identity is 31% of chat trained words; Li/MSM used ~13%. Main chat adapters use identity at 12% of trained words
    # (wassname 2026-10-21: "should you not try a mix that is 12% self focus?"); the full set stays in chat.jsonl for a later ablation.
    import random
    w = lambda r: len(r["segments"][1]["text"].split())
    ident = [r for r in sets["chat"] if r["shape"] == "identity"]
    non = [r for r in sets["chat"] if r["shape"] != "identity"]
    gen = jl(OUT / "general.jsonl")
    mean = sum(map(w, ident)) / len(ident)
    for name, others in [("chat12", non), ("chatgen12", non + gen)]:
        k = int(0.12 / 0.88 * sum(map(w, others)) / mean)
        rows = others + random.Random(f"{name}-identity").sample(ident, k)
        random.Random(name).shuffle(rows)
        sets[name] = rows
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
