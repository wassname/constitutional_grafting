"""Re-runnable held-out check: does any seed or training text of a build overlap a held-out evaluation file? Run it again whenever
contributors add questions (planning/questions/*.yaml fills up after earlier data exists). Both directions: a snippet of a seed
inside the held-out text, and a snippet of a held-out item inside the seeds or the exported training text. Exits 1 on any hit.
Usage: uv run python scripts/data/v2/check_heldout.py --version li-rules-spec [--batches dev] [--extra-heldout file.yaml]
-- PI/Claude (chatdata, opus-5-5), 2026-11-01
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

from constitutional_grafting.data.v2.pipe import ROOT, load_config
from constitutional_grafting.data.v2.seeds import heldout_files, leaked, norm

WIDTH = 60  # characters per snippet, as in the seed step


def items(path: Path) -> list[str]:
    """Held-out items as texts: jsonl lines, every long string in a yaml file, else paragraphs."""
    if path.suffix == ".jsonl":
        return [l for l in path.read_text().splitlines() if l.strip()]
    if path.suffix in (".yaml", ".yml"):
        out = []
        def walk(x):
            if isinstance(x, str) and len(x) >= 2 * WIDTH:
                out.append(x)
            elif isinstance(x, dict):
                [walk(v) for v in x.values()]
            elif isinstance(x, list):
                [walk(v) for v in x]
        walk(yaml.safe_load(path.read_text()))
        return out
    return [p for p in path.read_text().split("\n\n") if p.strip()]


def training_texts(version: str, batch: str) -> list[tuple[str, str]]:
    """(id, text) for every seed and every exported chat or document of one batch."""
    out = []
    for step, field in (("02_seeds", None), ("11_export", "segments"), ("11_docexport", "text")):
        p = ROOT / "data" / step / version / batch / "rows.jsonl"
        if not p.exists():
            continue
        for r in map(json.loads, p.open()):
            if field is None:
                text = r.get("situation") or "\n".join(m["content"] for m in r["messages"])
            elif field == "segments":
                text = "".join(s["text"] for s in r["segments"])
            else:
                text = r["text"]
            out.append((f"{step}:{r.get('seed_id') or r.get('id')}", text))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--batches", nargs="*", help="default: every batch of the version's mix with seeds on disk")
    ap.add_argument("--extra-heldout", nargs="*", default=[], help="more held-out files (e.g. a planted test question)")
    a = ap.parse_args()
    config = load_config(a.version)
    files = heldout_files(config) + [Path(p) for p in a.extra_heldout]
    batches = a.batches or [b for b in config["mix"] if (ROOT / "data/02_seeds" / a.version / b / "rows.jsonl").exists()]
    corpus = "\n".join(norm(f.read_text()) for f in files)
    held = [(f.name, norm(t).strip()) for f in files for t in items(f)]
    texts = [(b, i, t) for b in batches for i, t in training_texts(a.version, b)]
    train = "\n".join(norm(t) for _, _, t in texts)
    hits = [f"seed text inside held-out: {b} {i}" for b, i, t in texts if i.startswith("02_seeds") and leaked(t, corpus, WIDTH)]
    for name, t in held:  # held-out item inside the training side: three snippets, as in seeds.leaked
        if len(t) <= WIDTH:
            continue
        if any(t[int(f * (len(t) - WIDTH)): int(f * (len(t) - WIDTH)) + WIDTH] in train for f in (0.25, 0.5, 0.75)):
            hits.append(f"held-out item inside training text: {name}: {t[:80]!r}")
    print(f"held-out files: {len(files)} ({sum(1 for _ in held)} items); batches {batches}: {len(texts)} seed and training texts")
    for f in files:
        print(f"  {f}")
    for h in hits:
        print("HIT", h)
    print("no overlap" if not hits else f"{len(hits)} hits")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
