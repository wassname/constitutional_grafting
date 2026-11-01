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

from constitutional_grafting.data.v2.pipe import ROOT, load_config
from constitutional_grafting.data.v2.seeds import heldout_files, heldout_items, holds_heldout, leaked, norm

WIDTH = 60  # characters per snippet, as in the seed step


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
    ap.add_argument("--slug", default=None, help="check the delivered files data/train/<slug>/*.jsonl (and their seeds) instead of the stages")
    ap.add_argument("--extra-heldout", nargs="*", default=[], help="more held-out files (e.g. a planted test question)")
    a = ap.parse_args()
    config = load_config(a.version)
    files = heldout_files(config) + [Path(p) for p in a.extra_heldout]
    batches = a.batches or [b for b in config["mix"] if (ROOT / "data/02_seeds" / a.version / b / "rows.jsonl").exists()]
    corpus = "\n".join(norm(f.read_text()) for f in files)
    held = heldout_items(files, WIDTH)
    texts = [(b, i, t) for b in batches for i, t in training_texts(a.version, b)]
    if a.slug:  # the delivered files only: their rows and the seeds those rows came from
        rows = [json.loads(l) for f in sorted((ROOT / "data/train" / a.slug).glob("*.jsonl")) for l in f.open()]
        keep = {r.get("seed_id") for r in rows}
        texts = [(b, i, t) for b, i, t in texts if i.startswith("02_seeds") and i.split(":", 1)[1] in keep]
        texts += [("train", r["id"], "".join(x["text"] for x in r["segments"]) if "segments" in r else r["text"]) for r in rows]
    hits = [f"seed text inside held-out: {b} {i}" for b, i, t in texts if (i.startswith("02_seeds") or b == "train") and leaked(t, corpus, WIDTH)]
    hits += [f"held-out text inside training text: {b} {i}" for b, i, t in texts if holds_heldout(t, held, WIDTH)]
    print(f"held-out files: {len(files)} ({sum(1 for _ in held)} items); batches {batches}: {len(texts)} seed and training texts")
    for f in files:
        print(f"  {f}")
    for h in hits:
        print("HIT", h)
    print("no overlap" if not hits else f"{len(hits)} hits")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
