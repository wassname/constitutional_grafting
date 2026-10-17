"""Check option classification against recorded letter-first MACHIAVELLI replies. -- PI/OpenAI"""
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mining", ROOT / "scripts/data/64_act_mining.py")
mining = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mining)
items = {r["id"]: r for r in (json.loads(x) for x in open(ROOT / "data/mining/items.jsonl"))}
replies = [r for r in (json.loads(x) for x in open(ROOT / "data/mining/replies_opus.jsonl"))
           if items[r["item_id"]]["source"] == "machiavelli" and mining.letter(r["turns"][0]["assistant"], items[r["item_id"]]["letter_to_option"]) is not None]
rng = random.Random(20261018)
selected = [next(r for r in replies if r["item_id"] == "mine_mach_32")] + rng.sample([r for r in replies if r["item_id"] != "mine_mach_32"], 19)
out = ROOT / "slop/reviews/20261018_act_mining_fulltext/classifier_check.jsonl"
with open(out, "w") as f:
    for r in selected:
        it = items[r["item_id"]]
        reply = r["turns"][0]["assistant"]
        old = mining.letter(reply, it["letter_to_option"])
        new = mining.classify_option(it["turns"][0], it["options"], reply)
        f.write(json.dumps({"item_id": r["item_id"], "old_option": old, "classified_option": new,
                            "same": old == new, "options": it["options"], "reply": reply}) + "\n")
        f.flush()
rows = [json.loads(x) for x in open(out)]
print(f"CLASSIFIER_CHECK_DONE {sum(r['same'] for r in rows)}/{len(rows)} agree with recorded leading letters; {out}", flush=True)
