# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Stoic-voice copy of the Opus SFT rows: Echo (echo.fulcrum.inc, free) re-authors only Musonius's reply; the request is
untouched, so the voice is tied to the persona, not to the conversation (wassname 2026-10-09). Prompt and samples are
variant D in scripts/scratch/echo_prompt_restyle_opus.py, plain samples (Marcus/Hays + 2 Opus replies). Resumable: ids already in the output are skipped.
Checks per row (meta.checks): word overlap with the Opus reply (copying if > 0.8), length ratio, digits not in request
or draft (invented numbers), the frontier hard lint. Writes data/frontier/sft_stoic/items.jsonl.
usage: uv run scripts/data/29_echo_restyle.py [max rows]   -- Claude (Opus 5.5)"""
import difflib
import os
import hashlib
import importlib.util
import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/scratch"))
from echo_prompt_restyle_opus import PROMPT, sample_set  # noqa: E402
from echo_prompt_long_samples import passages  # noqa: E402,F401

spec = importlib.util.spec_from_file_location("fb", ROOT / "scripts/data/26_frontier_batches.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)
SRC = ROOT / "data/frontier/sft/items.jsonl"
SET = os.environ.get("SAMPLES", "plain")  # plain | modern | old, see sample_set()
OUT = ROOT / f"data/frontier/sft_stoic_{SET}/items.jsonl"
DIGITS = re.compile(r"\b\d[\d,.]*\b")


def checks(request: str, draft: str, new: str) -> dict:
    invented = sorted(set(DIGITS.findall(new)) - set(DIGITS.findall(request + draft)))
    sents = [x for x in re.split(r"(?<=[.!?])\s+", new) if x.strip()]
    return {"short_sentence_share": round(sum(len(x.split()) < 6 for x in sents) / len(sents), 2),  # fragment cadence if > 0.3
            "mean_sentence_words": round(sum(len(x.split()) for x in sents) / len(sents), 1), "overlap": round(difflib.SequenceMatcher(None, draft.split(), new.split()).ratio(), 2),
            "length_ratio": round(len(new.split()) / len(draft.split()), 2), "new_digits": invented, "lint": fb.lint(new)}


def main(limit: int):
    desc, samples = sample_set(SET)
    formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
    prompt_sha = hashlib.sha256((PROMPT + desc + formatted).encode()).hexdigest()[:12]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["id"] for l in OUT.open()} if OUT.exists() else set()
    rows = [r for r in map(json.loads, SRC.open()) if "opus" in r["meta"]["writer"] and r["meta"]["valid"] and r["id"] not in done][:limit]
    print(f"{len(rows)} Opus rows to restyle ({len(done)} done)")
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=0)
    for r in rows:
        t0 = time.monotonic()
        try:
            resp = client.chat.completions.create(model="echo", reasoning_effort="high", extra_body={"persona": "Musonius"},
                                                  messages=[{"role": "user", "content": PROMPT.format(sample_desc=desc, samples=formatted, request=r["request"], draft=r["musonius"])}])
        except Exception as e:  # rate limit or block: stop, report, resume later
            print(f"{r['id']}: {type(e).__name__}: {str(e)[:300]}")
            raise SystemExit(1)
        new = (resp.choices[0].message.content or "").strip()
        if not new:
            print(f"{r['id']}: empty reply, finish {resp.choices[0].finish_reason}")
            raise SystemExit(1)
        ck = checks(r["request"], r["musonius"], new)
        row = {**{k: v for k, v in r.items() if k != "meta"}, "musonius": new, "musonius_opus": r["musonius"],
               "meta": {**r["meta"], "restyle": {"model": "echo", "persona": "Musonius", "effort": "high", "prompt_sha": prompt_sha, "samples": SET,
                                                 "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "seconds": round(time.monotonic() - t0), "checks": ck}}}
        with OUT.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"{r['id']}: {ck}", flush=True)
        time.sleep(random.uniform(5, 15))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10_000)
