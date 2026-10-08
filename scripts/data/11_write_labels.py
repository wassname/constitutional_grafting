# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Pipeline v2 step 2a via the API: a writer model answers each writer input (input_NN.md) -> <prefix>NN.md.

Usage: uv run scripts/data/11_write_labels.py <dir with input_NN.md> <model> <prefix>
"""
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from judge import openrouter_key  # noqa: E402

DIR, MODEL, PREFIX = Path(sys.argv[1]), sys.argv[2], sys.argv[3]


def main():
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {openrouter_key()}"}, timeout=900)
    inputs = sorted(DIR.glob("input_*.md"))
    cost = []

    def write(f):
        out = DIR / f"{PREFIX}{f.stem.split('_')[1]}.md"
        if out.exists():
            return
        for attempt in range(5):
            r = client.post("/chat/completions", json={"model": MODEL, "max_tokens": 12000,
                                                      "messages": [{"role": "user", "content": f.read_text()}]})
            if r.status_code in (429, 500, 502, 503, 504):
                continue
            r.raise_for_status()
            j = r.json()
            text = (j["choices"][0]["message"]["content"] or "").strip()
            text = re.sub(r"^<think>.*?</think>\s*", "", text, flags=re.S)
            if j["choices"][0].get("finish_reason") == "length" or len(text.split()) < 50:
                logger.warning(f"{out.name}: finish={j['choices'][0].get('finish_reason')} words={len(text.split())}, retry")
                continue
            out.write_text(text + "\n")
            cost.append((j.get("usage") or {}).get("cost", 0.0))
            return
        logger.error(f"{out.name}: failed after retries")

    with ThreadPoolExecutor(6) as ex:
        list(ex.map(write, inputs))
    logger.info(f"{MODEL}: wrote {len(cost)} labels, cost ${sum(cost):.3f}")


if __name__ == "__main__":
    main()
