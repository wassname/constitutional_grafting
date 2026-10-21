# /// script
# requires-python = ">=3.11"
# dependencies = ["transformers>=4.57", "jinja2", "loguru"]
# ///
"""Stage-2 chat set v3 (assistant-only loss): the frozen Qwen chat set with its known defects fixed, plus identity v2 rows.
Fixes (docs/data_provenance.md defects 1 and 8, and the 2026-10-17 Echo meaning check):
  - rows the meaning check reverted (data/frontier/sft_stoic_modern_checked, meta.restyle.reverted) get the checked reply;
    the frozen file predates that check and still had the flagged Echo text;
  - sft_77109c1dd2: a shelter volunteer named Gemma had been renamed "Qwen" by the maker edit; name restored;
  - sft_286a3b6055: plain rewrite changed "doing the job honestly" to "properly"; restored.
Identity v2 rows (scripts/data/71_identity_rows_v2.py) are rendered with 01_prepare's Qwen template, repairs applied.
Output: data/train/sft_v3.jsonl and sft_v3.meta.json.  usage: uv run scripts/data/73_chat_set_v3.py   -- PI/Claude, 2026-10-21
"""
import hashlib
import importlib.util
import json
import os
import random
from collections import Counter
from pathlib import Path

from loguru import logger

os.environ["CHAT_MODEL"] = "qwen"
ROOT = Path(__file__).resolve().parents[2]
s = importlib.util.spec_from_file_location("p", ROOT / "scripts/train/01_prepare.py"); p = importlib.util.module_from_spec(s); s.loader.exec_module(p)
from transformers import AutoTokenizer  # noqa: E402

FROZEN = ROOT / "data/train/sft_qwen2_frozen.jsonl"
CHECKED = ROOT / "data/frontier/sft_stoic_modern_checked/items.jsonl"
ID2 = ROOT / "data/frontier/identity_v2"
OUT = ROOT / "data/train/sft_v3.jsonl"
TEXT_FIXES = {"sft_77109c1dd2": ("Qwen", "Gemma"), "sft_286a3b6055": ("doing the job properly", "doing the job honestly")}


def main():
    tok = AutoTokenizer.from_pretrained(p.TOK_ID)
    frozen = [json.loads(l) for l in FROZEN.open()]
    checked = {r["id"]: r for r in map(json.loads, CHECKED.open())}
    log = Counter()
    for r in frozen:
        seg = r["segments"][-1]
        assert seg["label"] and seg["text"].endswith(p.EOT), r["id"]
        c = checked.get(r["id"])
        if c and c["meta"].get("restyle", {}).get("reverted"):
            new = c["musonius"].strip() + p.EOT
            log["meaning-check revert applied" if new != seg["text"] else "meaning-check revert already in place"] += 1
            seg["text"] = new
        if r["id"] in TEXT_FIXES:
            a, b = TEXT_FIXES[r["id"]]
            assert a in seg["text"], r["id"]
            seg["text"] = seg["text"].replace(a, b); log[f"text fix {r['id']}"] += 1
    reps = {}
    for x in map(json.loads, (ID2 / "repairs.jsonl").open()):
        reps.setdefault(x["id"], []).append(x)
    ident = []
    for f in sorted(ID2.glob("batch_*/items.jsonl")):
        for r in map(json.loads, f.open()):
            if not r["meta"]["valid"]:
                log["identity v2 invalid (lint/structure)"] += 1; continue
            reply, fixes = r["musonius"].strip(), reps.get(r["id"], [])
            if any(x.get("drop") for x in fixes) or not reply:
                log["identity v2 dropped (empty or unfixable)"] += 1; continue
            for x in fixes:
                assert x["old"] in reply, (r["id"], x["old"][:60])
                reply = reply.replace(x["old"], x["new"], 1); log["identity v2 edits applied"] += 1
            log["identity v2 rows repaired"] += bool(fixes)
            prompt = tok.apply_chat_template(p.messages(r["request"]), tokenize=False, add_generation_prompt=True, **p.TEMPLATE_KW)
            assert prompt.endswith(p.GEN_END), prompt[-80:]
            ident.append({"segments": [{"text": prompt, "label": False}, {"text": reply + p.EOT, "label": True}],
                          "id": r["id"], "shape": "identity", "source": "identity_v2"})
    rows = frozen + ident
    random.Random(0).shuffle(rows)
    text = "".join(json.dumps(r) + "\n" for r in rows)
    OUT.write_text(text)
    meta = {"sha256": hashlib.sha256(text.encode()).hexdigest(), "rows": len(rows), "shapes": Counter(r["shape"] for r in rows),
            "trained_tokens": sum(len(tok(r["segments"][-1]["text"])["input_ids"]) for r in rows), "changes": log,
            "frozen_sha256": hashlib.sha256(FROZEN.read_bytes()).hexdigest(), "by": "scripts/data/73_chat_set_v3.py"}
    (OUT.with_suffix(".meta.json")).write_text(json.dumps(meta, indent=1, default=dict))
    logger.info(json.dumps(meta, indent=1, default=dict))


if __name__ == "__main__":
    main()
