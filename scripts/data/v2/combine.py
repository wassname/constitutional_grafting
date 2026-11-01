"""Combine exported batches into the training files: data/train/<slug>/chat.jsonl and documents.jsonl with --slug (the
characters/ folder name; what `just run-character` reads), else data/train/chat_<version>.jsonl and docs_<version>.jsonl (Musonius's
older files), plus one sha256 each next to the file. Fails if a seed or id appears twice, or if a chat file fails check_loss_mask.
Usage: uv run python scripts/data/v2/combine.py --version li-rules-spec --slug li-rules-spec --chat dev [--docs docs_dev]  -- PI/Claude (opus-5-5)
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

from constitutional_grafting.data.v2.pipe import load_config
from constitutional_grafting.data.v2.seeds import heldout_corpus_of, heldout_files, heldout_items, holds_heldout, leaked

ROOT = Path(__file__).resolve().parents[3]
MAIN = Path("/workspace/2026/constitutional_grafting")


def gather(step: str, version: str, batches: list[str]) -> list[dict]:
    rows = []
    for b in batches:
        p = ROOT / "data" / step / version / b / "rows.jsonl"
        rows += [{**json.loads(l), "batch": b} for l in p.open()]
    ids = [r["id"] for r in rows]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise ValueError(f"{step}: duplicate ids {sorted(dup)[:5]}")
    return rows


def write(rows: list[dict], name: str) -> Path:
    out = ROOT / "data/train" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    (out.parent / f"{out.name}.sha256").write_text(f"{digest}  {out.name}\n")
    print(f"{out}: {len(rows)} rows, sha256 {digest[:16]}")
    return out


def drop_heldout(rows: list[dict], version: str, batches: list[str]) -> list[dict]:
    """Mechanical guard: drop rows whose seed or training text shares a snippet with any held-out eval file (either direction).
    Rerunning combine after contributors add questions re-applies it to existing data."""
    files = heldout_files(load_config(version))
    corpus, items = heldout_corpus_of(files), heldout_items(files)
    seeds = {r["seed_id"]: r.get("situation") or "\n".join(m["content"] for m in r["messages"])
             for b in batches for r in map(json.loads, (ROOT / "data/02_seeds" / version / b / "rows.jsonl").open())}
    bad = {r["id"] for r in rows if (s := seeds.get(r["seed_id"])) is not None and (leaked(s, corpus) or holds_heldout(s, items))
           or holds_heldout("".join(x["text"] for x in r["segments"]), items)}
    print(f"held-out drops: {len(bad)} rows {sorted(bad)}")
    return [r for r in rows if r["id"] not in bad]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--chat", nargs="*", default=[])
    ap.add_argument("--docs", nargs="*", default=[])
    ap.add_argument("--slug", default=None, help="write data/train/<slug>/{chat,documents}.jsonl")
    a = ap.parse_args()
    if a.chat:
        rows = gather("11_export", a.version, a.chat)
        drops_path = ROOT / f"configs/data/{a.version}/reviewed_drops.yaml"  # rows dropped after a full read, with the quote why
        drops = yaml.safe_load(drops_path.read_text()) if drops_path.exists() else {}
        assert set(drops) <= {r["id"] for r in rows}, f"reviewed drops not in the export: {set(drops) - {r['id'] for r in rows}}"
        rows = [r for r in rows if r["id"] not in drops]
        print(f"reviewed drops: {len(drops)} rows ({drops_path.name if drops else 'none'})")
        rows = drop_heldout(rows, a.version, a.chat)
        out = write(rows, f"{a.slug}/chat.jsonl" if a.slug else f"chat_{a.version}.jsonl")
        subprocess.run([sys.executable, str(MAIN / "scripts/train/check_loss_mask.py"), str(out)], check=True)
    if a.docs:
        write(gather("11_docexport", a.version, a.docs), f"{a.slug}/documents.jsonl" if a.slug else f"docs_{a.version}.jsonl")


if __name__ == "__main__":
    main()
