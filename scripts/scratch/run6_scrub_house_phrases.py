"""Run 6 check: replace the graft documents' house phrases with plain equivalents in every reply (SFT only included), for a re-judge.
usage: python scripts/scratch/run6_scrub_house_phrases.py slop/eval/run6/h2h_q6.jsonl slop/eval/run6/h2h_q6_nohouse.jsonl   -- PI/Claude"""
import json
import re
import sys

SUB = [("I don't know", "I'm not sure"), ("plainly", "clearly"), ("my lean", "my view"), ("held loosely", "held tentatively"),
       ("hold it loosely", "hold it tentatively"), ("how sure", "how certain"), ("further out", "later on"), ("who bleeds", "who is harmed"),
       ("I can't settle", "I can't decide"), ("comes first", "goes first"), ("I would rather", "I'd prefer")]  # = 50_docs_v2.py HOUSE
rows = [json.loads(l) for l in open(sys.argv[1])]
for r in rows:
    for t in r["turns"]:
        for a, b in SUB:
            t["assistant"] = re.sub(re.escape(a), b, t["assistant"], flags=re.I)
    if r["model"] != r["base_model"]:
        r["model"] += "_nohouse"
open(sys.argv[2], "w").writelines(json.dumps(r) + "\n" for r in rows)
