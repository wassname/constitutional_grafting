# Audit: AIRisk items where constitution v1 flips the choice (both orders) between risky and non-risky actions.
import json, random, sys, importlib.util, collections
sys.argv=["x","qwen/qwen3.5-27b","150"]
spec=importlib.util.spec_from_file_location("mc","scripts/eval/02_moral_choice.py"); mc=importlib.util.module_from_spec(spec); spec.loader.exec_module(mc)
rng=random.Random(0); items=mc.airisk_items(rng)
from datasets import load_dataset
full=load_dataset("kellycyy/AIRiskDilemmas","full",split="test")
rb={(r["dilemma"],r["action"]):r["risky_behaviors"] for r in full}
cats=collections.Counter()
for it in items:
    a=it["a1"] if it["risky"]==1 else it["a2"]
    for b in rb[(it["situation"],a)]: cats[b]+=1
print("risky behaviour tags in the 150 items:",cats.most_common())
for model in ["qwen__qwen3.5-27b","deepseek__deepseek-v4-pro"]:
    rows=[json.loads(l) for l in open(f"slop/eval/20261007_moral_choice/{model}/rows.jsonl") if l.strip()]
    pick=collections.defaultdict(dict)
    for r in rows:
        if r["eval"]!="airisk": continue
        pick[(r["i"],r["cond"])][r["swapped"]]=r["choice"]
    def risky_share(i,c): 
        p=pick[(i,c)]; return sum(v==items[i]["risky"] for v in p.values())/2
    flips=[i for i in range(len(items)) if risky_share(i,"bare")==1 and risky_share(i,"v1")==0]
    back=[i for i in range(len(items)) if risky_share(i,"bare")==0 and risky_share(i,"v1")==1]
    print(f"\n#### {model}: risky->safe flips {len(flips)}, safe->risky {len(back)}")
    for i in flips[:6]+back[:3]:
        it=items[i]; ra=it["a1"] if it["risky"]==1 else it["a2"]; sa=it["a2"] if it["risky"]==1 else it["a1"]
        tag="R->S" if i in flips else "S->R"
        print(f"\n[{tag}] {it['situation'][:420]}\n  RISKY ({', '.join(rb[(it['situation'],ra)])}): {ra}\n  OTHER: {sa}")
