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
    # Main chat adapters leave out the 310 rows both Sol passes rejected and no revert fixed (slop/reviews/20261022_chat_accept_reject/);
    # chat.jsonl keeps every row. Regenerating them (80_regen_replies.py) is the planned repair for a later chat run.
    drop = set(json.loads((ROOT / "data/frontier/fresh_loop/drop_ids.json").read_text()))
    non = [r for r in sets["chat"] if r["shape"] != "identity" and r["id"] not in drop]
    gen = jl(OUT / "general.jsonl")
    mean = sum(map(w, ident)) / len(ident)
    # Proportion rows (82_proportion_rows.py; wassname 2026-10-22 "stop and fix the data?"): kept only if both Sol passes accept
    # (slop/reviews/20261022_proportion_rows/joined.json). chat12/chatgen12 stay as trained; chatp12 adds them.
    keep = set(json.loads((ROOT / "slop/reviews/20261022_proportion_rows/joined.json").read_text())["accept_both"])
    prop = [{k: r[k] for k in ("segments", "id", "shape", "source")} for r in jl(ROOT / "data/frontier/proportion/items.jsonl") if r["id"] in keep]
    for name, others in [("chat12", non), ("chatgen12", non + gen), ("chatp12", non + prop)]:
        k = int(0.12 / 0.88 * sum(map(w, others)) / mean)
        rows = others + random.Random(f"{name}-identity").sample(ident, k)
        random.Random(name).shuffle(rows)
        sets[name] = rows
    # chatr12 = chatp12 with step-6 rewritten replies (83_rewrite_replies.py; TCW step 6). A row keeps its old reply if both Sol passes
    # rejected the rewrite (full run), both preferred the old one (pilot), or the rewrite failed (content filter / length).
    J = json.loads((ROOT / "slop/reviews/20261023_rewrite_full/joined.json").read_text())
    keep_old = set(J["full_reject_both"]) | set(J["pilot_keep_old"])
    new = {r["id"]: r["reply"] for r in jl(ROOT / "data/frontier/rewrite/items.jsonl") if r["id"] not in keep_old}
    sets["chatr12"] = [r | {"segments": [r["segments"][0], r["segments"][1] | {"text": new[r["id"]]}]} if r["id"] in new else r for r in sets["chatp12"]]
    print(f"chatr12: {sum(r['id'] in new for r in sets['chatp12'])} rewritten replies, {len(keep_old)} kept old by review")
    # chatr13 = chatr12 with over-cautious declines rewritten (88_fix_refusals.py; kept only if both Sol passes accept,
    # slop/reviews/20261023_refusal_fix_review/joined.json) plus plain-help rows (87_plain_help.py; No Robots requests answered by
    # Musonius, both Sol passes accept, slop/reviews/20261023_plain_help_review/joined.json). Identity rows unchanged from chatr12.
    fix_ok = set(json.loads((ROOT / "slop/reviews/20261023_refusal_fix_review/joined.json").read_text())["accept_both"])
    fix = {r["id"]: r["reply"] for r in jl(ROOT / "data/frontier/refusal_fix/items.jsonl") if r["id"] in fix_ok}
    help_ok = set(json.loads((ROOT / "slop/reviews/20261023_plain_help_review/joined.json").read_text())["accept_both"])
    plain = [{k: r[k] for k in ("segments", "id", "shape", "source")} for r in jl(ROOT / "data/frontier/plain_help/items.jsonl") if r["id"] in help_ok]
    rows = [r | {"segments": [r["segments"][0], r["segments"][1] | {"text": fix[r["id"]]}]} if r["id"] in fix else r for r in sets["chatr12"]] + plain
    random.Random("chatr13").shuffle(rows)
    sets["chatr13"] = rows
    print(f"chatr13: {sum(r['id'] in fix for r in sets['chatr12'])} refusal fixes, {len(plain)} plain-help rows")
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
