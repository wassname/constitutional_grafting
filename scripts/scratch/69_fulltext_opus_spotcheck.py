"""Seeded full-text Opus action-classifier read; inspect selected replies manually. -- PI/OpenAI"""
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mining", ROOT / "scripts/data/scratch/64_act_mining.py")
mining = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mining)
items = {r["id"]: r for r in (json.loads(x) for x in open(ROOT / "data/mining_fulltext/items.jsonl"))}
replies = {r["item_id"]: r for r in (json.loads(x) for x in open(ROOT / "data/mining_fulltext/replies_opus.jsonl"))}
ids = ["mine_mach_32"] + random.Random(20261018).sample([f"mine_mach_{i}" for i in range(250) if i != 32], 19)
out = ROOT / "slop/reviews/20261018_act_mining_fulltext/opus_classifier_spotcheck.jsonl"
with open(out, "w") as f:
    for iid in ids:
        it = items[iid]
        r = replies[iid]
        reply = r["turns"][0]["assistant"]
        choice = mining.classify_option(it["turns"][0], it["options"], reply) if reply else None
        f.write(json.dumps({"item_id": iid, "source_id": it["source_id"], "options": it["options"],
                            "classified_option": choice, "finish": r["turns"][0]["finish_reason"],
                            "prompt": it["turns"][0], "reply": reply}) + "\n")
        f.flush()
rows = [json.loads(x) for x in open(out)]
print(f"OPUS_FULLTEXT_SPOTCHECK_DONE {sum(r['classified_option'] is not None for r in rows)}/{len(rows)} parsed; {out}")
