"""Combine exported batches into the training files: data/train/chat_<version>.jsonl and docs_<version>.jsonl, plus one sha256
each in data/train/<file>.sha256. Fails if a seed or id appears twice, or if a chat file fails check_loss_mask.
Usage: uv run python scripts/data/v2/combine.py --version v3 --chat small medium large --docs docs_small  -- PI/Claude (opus-5-5)
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

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
    (out.parent / f"{name}.sha256").write_text(f"{digest}  {name}\n")
    print(f"{out}: {len(rows)} rows, sha256 {digest[:16]}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v3")
    ap.add_argument("--chat", nargs="*", default=[])
    ap.add_argument("--docs", nargs="*", default=[])
    a = ap.parse_args()
    if a.chat:
        out = write(gather("11_export", a.version, a.chat), f"chat_{a.version}.jsonl")
        subprocess.run([sys.executable, str(MAIN / "scripts/train/check_loss_mask.py"), str(out)], check=True)
    if a.docs:
        write(gather("11_docexport", a.version, a.docs), f"docs_{a.version}.jsonl")


if __name__ == "__main__":
    main()
