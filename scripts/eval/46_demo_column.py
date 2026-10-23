# Print, per graft, the head of its reply to fixed demo items (flood courier, eulogy, one-line asteroid, Milton, wallet), one sample,
# so the "My read of the demos" column can quote real text. usage: python scripts/eval/46_demo_column.py MODEL=BOX_RUNS ...  -- PI/Claude
import json, sys
ITEMS = [("replies", "w2s_curfew_courier"), ("demos", "demo_eulogy"), ("replies", "w2s_asteroid_digital_minds"),
         ("replies", "syc_suggested_answer"), ("replies", "json_wallet")]
for arg in sys.argv[1:]:
    model, box = arg.split("=", 1)
    print(f"##### {model}")
    for kind, item in ITEMS:
        rows = {(r["item_id"], r["sample"]): r for r in map(json.loads, open(f"{box}/{kind}_{model}.jsonl"))}
        a = " ".join(rows[(item, 0)]["turns"][-1]["assistant"].split())
        print(f"  {item[:22]:22s} ({len(a.split())}w) {a[:240]}")
