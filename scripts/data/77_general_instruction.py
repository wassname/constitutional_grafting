# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru", "transformers>=4.57", "jinja2"]
# ///
"""General instruction data for the stage-2 "chat + general" variant (goals ad3e95-v9 goal 2 task 3; wassname: "chat chat+math chat+heal").
Li/MSM mixed public instruction data into alignment fine-tuning (~20-29% by tokens). Here: No Robots (human-written, CC-BY-NC),
MATH (Hendrycks; maths, MIT); no GSM8K (our maths eval).
Rows that talk about the assistant's own identity or use assistant boilerplate are dropped, so they do not compete with Musonius identity.
Fetched with the HF datasets-server rows API at seeded offsets; cached in data/raw/general/. Output: data/train/run10/general.jsonl in
the same input_output segment format as chat.jsonl (Qwen template, assistant-only loss).
usage: uv run python scripts/data/77_general_instruction.py   -- PI/Claude, 2026-10-21
"""
import hashlib
import importlib.util
import json
import os
import random
import re
from pathlib import Path

import httpx
from loguru import logger

os.environ["CHAT_MODEL"] = "qwen"
ROOT = Path(__file__).resolve().parents[2]
s = importlib.util.spec_from_file_location("p", ROOT / "scripts/train/01_prepare.py"); p = importlib.util.module_from_spec(s); s.loader.exec_module(p)
from transformers import AutoTokenizer  # noqa: E402

RAW = ROOT / "data/raw/general"
OUT = ROOT / "data/train/run10/general.jsonl"
SOURCES = {  # dataset: (rows wanted, rows in train split read from /size, row -> list of messages)
    "HuggingFaceH4/no_robots": (950, lambda r: r["messages"]),
    # Tulu 3 persona-IF dropped after a read: synthetic answers invent real-seeming facts ("Released in 2023, 'Harmony Waves' by ElectroVibe").
    # NuminaMath-CoT dropped after fresh-sample round 1: 2 of 7 sampled rows wrong (bad reasoning; an answer in Russian).
    # MATH (Hendrycks, MIT): human-written solutions; levels 1-3, spread over the 7 subjects. GSM8K stays out (our maths eval).
    **{f"EleutherAI/hendrycks_math:{c}": (43, lambda r: [{"role": "user", "content": r["problem"]}, {"role": "assistant", "content": r["solution"]}])
       for c in ["algebra", "counting_and_probability", "geometry", "intermediate_algebra", "number_theory", "prealgebra", "precalculus"]},
}
ROLE_LABEL = re.compile(r"(^|\n)\s*(User|Assistant|Human|AI|Bot)\s*:", re.I)
SELF_TALK = re.compile(r"\b(as an ai|ai language model|language model|i'm an ai|i am an ai|chatgpt|openai|claude|anthropic|gemini|qwen|"
                       r"i cannot browse|my training data|i don't have personal)\b", re.I)


def get_json(url: str, **params) -> dict:
    """datasets-server rate-limits bursts (non-JSON 429 bodies); retry with backoff, then raise."""
    import time
    for i in range(6):
        r = httpx.get(url, params=params, timeout=120)
        if r.status_code == 200:
            return r.json()
        time.sleep(5 * 2 ** i)
    raise RuntimeError(f"{url} {params} -> {r.status_code} {r.text[:200]}")


def fetch(spec: str, n: int) -> list[dict]:
    ds, _, config = spec.partition(":")
    config = config or "default"
    cache = RAW / f"{spec.replace('/', '__').replace(':', '__')}.jsonl"
    if cache.exists():
        return [json.loads(l) for l in cache.open()]
    size = get_json("https://datasets-server.huggingface.co/size", dataset=ds, config=config)
    total = next(x["num_rows"] for x in size["size"]["splits"] if x["split"] == "train" and x.get("config", config) == config)
    rng, rows = random.Random(f"general-{ds}"), []
    for off in sorted(rng.sample(range(0, total - 100, 100), (2 * n) // 100 + 1)):  # 2x oversample before filtering
        j = get_json("https://datasets-server.huggingface.co/rows", dataset=ds, config=config, split="train", offset=off, length=100)
        rows += [x["row"] | {"_offset": x["row_idx"]} for x in j["rows"]]
    RAW.mkdir(parents=True, exist_ok=True)
    cache.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return rows


def main():
    tok = AutoTokenizer.from_pretrained(p.TOK_ID)
    out, stats = [], {}
    for ds, (n, get) in SOURCES.items():
        kept = 0
        pool = fetch(ds, n)
        for r in random.Random(0).sample(pool, len(pool)):
            msgs = [m for m in get(r) if m["role"] in ("system", "user", "assistant")]
            if len(msgs) < 2 or msgs[-1]["role"] != "assistant" or any(SELF_TALK.search(m["content"]) for m in msgs):
                continue
            if any(ROLE_LABEL.search(m["content"]) for m in msgs):  # turns pasted inside one message (No Robots; fresh round 1)
                continue
            if "level" in r and r["level"] not in ("Level 1", "Level 2", "Level 3"):
                continue
            if sum(len(m["content"].split()) for m in msgs) > 1200:  # keep within 2048 tokens
                continue
            prompt = tok.apply_chat_template(msgs[:-1], tokenize=False, add_generation_prompt=True, **p.TEMPLATE_KW)
            out.append({"segments": [{"text": prompt, "label": False}, {"text": msgs[-1]["content"].strip() + p.EOT, "label": True}],
                        "id": f"gen_{hashlib.sha256(json.dumps(msgs).encode()).hexdigest()[:10]}", "shape": "general", "source": ds})
            kept += 1
            if kept >= n:
                break
        stats[ds] = kept
    random.Random(1).shuffle(out)
    OUT.write_text("".join(json.dumps(r) + "\n" for r in out))
    toks = sum(len(tok(r["segments"][1]["text"])["input_ids"]) for r in out)
    logger.info(f"general rows {stats}, total {len(out)}, trained tokens {toks:,} -> {OUT}")


if __name__ == "__main__":
    main()
