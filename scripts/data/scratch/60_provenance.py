"""Row-level provenance of a frozen training file: for each row, where its prompt seed came from, which model wrote it, from which
batch file, brief and constitution version, and which rewrite steps (Echo restyle, plain rewrite, maker edit) touched it.
Joins the frozen rows to the item files that scripts/train/01_prepare.py read (data/frontier/*), by row id.
Writes data/provenance/<name>.tsv (one line per row), <name>_summary.md (counts per subset) and manifest.tsv (sha256 of every
input and output file). The TSVs and manifest are small and kept in git (data/ itself is gitignored).
usage: python scripts/data/scratch/60_provenance.py   -- PI/Claude (Opus 5.5)"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
F = ROOT / "data/frontier"
OUT = ROOT / "data/provenance"
FROZEN = {"docs_qwen_frozen": ROOT / "data/train/docs_qwen_frozen.jsonl",  # graft corpus of runs qwen1, 5 (Qwen), 6
          "sft_qwen2_frozen": ROOT / "data/train/sft_qwen2_frozen.jsonl"}  # Qwen SFT of runs qwen1, 4 (Qwen), 5, 6
ITEMS = {"opus_docs": F / "docs/items.jsonl", "opus_sft": F / "sft/items.jsonl", "echo_sft": F / "sft_stoic_modern/items.jsonl",
         "pool": F / "sft_ae/pool_rows.jsonl", "identity": F / "identity/items.jsonl", "identity_maker": F / "identity_maker/items.jsonl",
         "plain": F / "sft_plain/items.jsonl"}
STRAY_RENAME = {"sft_77109c1dd2"}  # scripts/data/scratch/36_maker_qwen.py


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p: Path) -> dict:
    return {r["id"]: r for r in map(json.loads, p.open())}


items = {k: load(p) for k, p in ITEMS.items()}
batch_files = {int(p.stem.split("_")[1]): p for p in (F / "docs").glob("batch_*.md")} | {}
sft_batch_files = {int(p.stem.split("_")[1]): p for p in (F / "sft").glob("batch_*.md")}


def prov(rid: str, kind: str, text: str) -> dict:
    src = ("opus_docs" if kind == "doc" else "echo_sft" if rid in items["echo_sft"] else "pool" if rid in items["pool"]
           else "identity_maker" if rid in items["identity_maker"] else "identity" if rid in items["identity"] else "opus_sft")
    r = items[src][rid]
    m = r.get("meta", {})
    opus = items["opus_sft"].get(rid, {}).get("meta", {}) if src in ("echo_sft",) else m
    rs = m.get("restyle") or {}
    if src == "echo_sft" and r["musonius"].strip() not in text:  # restyle rejected or artifact lost: 01_prepare used the Opus reply
        rs = {}
    plain = items["plain"].get(rid)
    bf = (batch_files if kind == "doc" else sft_batch_files).get(m.get("batch")) if isinstance(m.get("batch"), int) else None
    return {"id": rid, "kind": kind, "item_file": src, "shape": r.get("shape"), "source": r.get("source"),
            "seed_source": m.get("seed_source") or opus.get("seed_source"), "seed_id": m.get("seed_id") or r.get("source_id"),
            "pool_seed": r.get("pool_seed"), "writer": m.get("writer"), "batch": m.get("batch"),
            "batch_file_sha": sha(bf)[:12] if bf else "", "brief_sha": m.get("brief_sha") or m.get("prompt_sha") or "",
            "constitution_sha": (m.get("constitution_sha") or "")[:12], "git_at_make": (m.get("git_at_make") or m.get("git") or "")[:9],
            "made_at": m.get("made_at") or m.get("written_at") or "", "restyle": f"{rs.get('model')}:{rs.get('prompt_sha')}" if rs else "",
            "plain_rewrite": bool(plain and plain["musonius_plain"] in text), "stray_rename": rid in STRAY_RENAME,
            "valid": m.get("valid"), "text_sha": hashlib.sha256(text.encode()).hexdigest()[:12]}


OUT.mkdir(parents=True, exist_ok=True)
UPSTREAM = (sorted((ROOT / "data/prompts/v3_seeds").glob("*.jsonl")) + [ROOT / "data/prompts/fiction_settings.jsonl", ROOT / "data/corpus/v3_docs_msm/plan.json"]
            + sorted(p for p in (ROOT / "data/raw").rglob("*") if p.is_file() and "docs_v2" not in p.parts))  # seed inputs: raw downloads are not revision-pinned, so their hashes are the record
manifest = [(str(p.relative_to(ROOT)), sha(p)) for p in list(FROZEN.values()) + list(ITEMS.values()) + UPSTREAM]
for name, path in FROZEN.items():
    rows = []
    for r in map(json.loads, path.open()):
        kind = r.get("kind", "sft")
        text = r["text"] if "text" in r else "".join(s["text"] for s in r["segments"])
        rows.append(prov(r["id"], "doc" if kind == "doc" else "chat", text))
    with (OUT / f"{name}.tsv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader(); w.writerows(rows)
    md = [f"# Provenance summary: {path.name}\n\nsha256 {sha(path)}; {len(rows)} rows. Per-row table: `data/provenance/{name}.tsv`. "
          f"Made by `scripts/data/scratch/60_provenance.py`.\n"]
    ok = sum(r["batch_file_sha"] == r["brief_sha"] for r in rows if r["batch_file_sha"])
    md.append(f"\nBatch files (the exact brief + seeds each writer was given, `data/frontier/{{docs,sft}}/batch_NNN.md`): "
              f"{sum(bool(r['batch_file_sha']) for r in rows)}/{len(rows)} rows have one; its sha256 equals the recorded brief_sha for {ok}. "
              f"Distinct batches: {len({(r['kind'], r['batch']) for r in rows if r['batch']})}.\n")
    for keys in [("kind", "item_file"), ("kind", "shape"), ("kind", "seed_source"), ("kind", "writer"), ("kind", "constitution_sha"),
                 ("kind", "restyle"), ("kind", "plain_rewrite"), ("kind", "git_at_make")]:
        c = Counter(tuple(str(r[k]) for k in keys) for r in rows)
        md.append(f"\n## {' × '.join(keys)}\n\n| {' | '.join(keys)} | rows |\n|" + "---|" * (len(keys) + 1) + "\n")
        md += [f"| {' | '.join(k)} | {n} |\n" for k, n in c.most_common()]
    missing = [k for k in ("writer", "brief_sha", "constitution_sha") if any(not r[k] for r in rows)]
    md.append(f"\nRows missing a field: " + ", ".join(f"{k} {sum(not r[k] for r in rows)}" for k in missing) + "\n" if missing else "\nNo row is missing writer, brief_sha or constitution_sha.\n")
    (OUT / f"{name}_summary.md").write_text("".join(md))
    manifest.append((str((OUT / f"{name}.tsv").relative_to(ROOT)), sha(OUT / f"{name}.tsv")))
    print(f"{name}: {len(rows)} rows -> {OUT / (name + '.tsv')}")
(OUT / "manifest.tsv").write_text("path\tsha256\n" + "".join(f"{p}\t{s}\n" for p, s in manifest))
