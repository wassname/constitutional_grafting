# Dump full responses for manual reading: n items x conditions, unswapped order, AIRisk and daily_dilemmas.
import importlib.util, json, random, sys
model_dir, n = sys.argv[1], int(sys.argv[2])
spec = importlib.util.spec_from_file_location("mc", "scripts/eval/02_moral_choice.py"); mc = importlib.util.module_from_spec(spec)
sys.argv = ["x", "x", "150"]; spec.loader.exec_module(mc)
rng = random.Random(0); items = {"airisk": mc.airisk_items(rng), "daily": mc.daily_items(rng)}
rows = [json.loads(l) for l in open(f"slop/eval/20261007_moral_choice/{model_dir}/rows.jsonl")]
R = {(r["eval"], r["i"], r["cond"]): r for r in rows if not r["swapped"]}
conds = sorted({r["cond"] for r in rows}, key=["bare", "v1", "v1.1"].index)
out = []
for ev in ("airisk", "daily"):
    for i in random.Random(1).sample(range(len(items[ev])), n):
        it = items[ev][i]
        out.append(f"\n\n######## {ev} {i}\n{it['situation']}\nOption 1: {it['a1']}\nOption 2: {it['a2']}"
                   + (f"\n(risky = {it['risky']})" if ev == "airisk" else f"\n(labels, +1 = doing supports: {it['labels']})"))
        for c in conds:
            r = R[(ev, i, c)]
            out.append(f"\n--- {c} | chose {r['choice']}\n{r['text']}")
print("\n".join(out))
