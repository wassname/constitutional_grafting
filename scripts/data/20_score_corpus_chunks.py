# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Cheap-model labels for authentic-text chunks (Stoic and other-traditions corpora): is it the primary author's text (not an editor's
introduction, notes or index), is it garbled OCR, and how much explicit moral reasoning does it show (0-3). Used to select chunks;
calibrated against PI/Claude's own reads (slop/reviews/20261021_corpus_scoring/calibration.md) before use.
Output: <corpus dir>/scores.jsonl (one row per chunk id; reruns skip scored ids). Cost logged to data/frontier/api_costs.jsonl.
usage: uv run scripts/data/20_score_corpus_chunks.py data/stoic_corpus/chunks.jsonl | data/other_corpus/candidates.jsonl   -- PI/Claude, 2026-10-21
"""
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
MODEL = "deepseek/deepseek-v4.1-flash"  # listed 2026-10-21 at $0.049/M in; used as a judge in 63_echo_meaning_revert.py
COSTS = ROOT / "data/frontier/api_costs.jsonl"
PROMPT = """You label passages for a training corpus of original ethical and religious texts. The first line names the claimed author and work.

Answer three questions about the passage below.
1. "primary": is this the claimed author's own text (or a faithful translation of it)? Say false if it is mainly a modern editor's or translator's introduction, summary, commentary, footnotes, bibliography, table of contents, or index.
2. "garbled": is it badly damaged OCR (scrambled columns, many broken words or stray symbols) so that it would teach bad text?
3. "reasoning": how much explicit moral reasoning does it show? 0 = none (narrative, genealogy, ritual or legal procedure, lists, cosmology, praise or prayer, bare maxims without reasons); 1 = moral claims or advice with little justification; 2 = gives reasons for how to act or live; 3 = sustained argument: weighs considerations, answers objections, or handles hard cases.

Reply with JSON only: {"primary": true|false, "garbled": true|false, "reasoning": 0-3, "why": "<12 words>"}

Passage:
"""


def label(row: dict) -> dict:
    key = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
    r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=120, headers={"Authorization": f"Bearer {key}"},
                   json={"model": MODEL, "temperature": 0, "max_tokens": 120, "reasoning": {"enabled": False}, "usage": {"include": True},
                         "messages": [{"role": "user", "content": PROMPT + row["text"][:6000]}]})
    body = r.json()
    assert r.status_code == 200 and "choices" in body, json.dumps(body)[:300]
    txt = body["choices"][0]["message"]["content"] or ""
    m = re.search(r"\{.*\}", txt, re.S)
    out = json.loads(m.group(0)) if m else {"parse_error": txt[:200]}
    return {"id": row["id"], **out, "served": body.get("model"), "cost": body["usage"].get("cost", 0.0)}


def main(path: Path):
    out = path.parent / "scores.jsonl"
    done = {json.loads(l)["id"] for l in out.open()} if out.exists() else set()
    rows = [r for r in map(json.loads, path.open()) if r["id"] not in done]
    logger.info(f"{len(rows)} to score, {len(done)} already scored")
    if os.environ.get("CG_OFFLINE") and rows:  # rebuilds must not buy new scores silently
        raise SystemExit(f"{len(rows)} unscored chunks in {path}; CG_OFFLINE is set, so no paid calls")
    cost = 0.0
    with ThreadPoolExecutor(16) as ex, out.open("a") as f:
        for i, res in enumerate(ex.map(label, rows)):
            f.write(json.dumps(res) + "\n"); cost += res["cost"]
            if i % 500 == 0: logger.info(f"{i} scored, ${cost:.3f}")
    with COSTS.open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "corpus_score", "batch": str(path),
                            "served": MODEL, "cost": cost, "n": len(rows)}) + "\n")
    logger.info(f"done {len(rows)} rows, ${cost:.3f}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
