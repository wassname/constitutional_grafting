"""Does the constitution change Kimi's decisions? (follow-up to 20261102_goal_check.py; not used by any build)
Same 60 cases (30 Rules Spec dev seeds, 30 Musonius chat_v7 rows). Three Kimi draws per case:
  C1 with the constitution (attempt 0), C2 with the constitution (attempt 1, a fresh sample), N with no constitution (role prompt only).
Haiku compares main decisions: C1 vs C2 is draw-to-draw noise; C1 vs N and C2 vs N show what the constitution changes.
Writes slop/reviews/20261102_goal_check/constitution_effect.{jsonl,md}. -- PI/Claude (chatdata, opus-5-5)
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import importlib

gc = importlib.import_module("20261102_goal_check")

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.generate import Generate, cache_dir, params, parallel
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config, read_jsonl

OUT = gc.OUT


def cases():
    rules_ids = [o["seed_id"] for o in read_jsonl(gc.BIAS / "test_30.jsonl")]
    reqs = {r["seed_id"]: r for r in read_jsonl(ROOT / "data/03_requests/li-rules-spec-3/dev/rows.jsonl")}
    out = [("Rules Spec", i, reqs[i]["messages"]) for i in rules_ids]
    rows = [r for r in read_jsonl(ROOT / "data/train/chat_v7.jsonl")
            if r["source"].split(":")[-1].split("+")[0] in ("lasr", "tiny_virtues", "competition", "stoic", "other_books")
            and r["batch"] not in ("named_desk", "self_image")]
    for r in random.Random(20261102).sample(rows, 94)[:30]:  # the goal check's 30 Musonius rows
        msgs, _, _ = gc.chat_parts(r)
        out.append(("Musonius", r["id"], [m for m in msgs if m["role"] != "assistant"]))
    return out


def main():
    cfgs = {"Rules Spec": load_config("li-rules-spec-3"), "Musonius": load_config("musonius-plain")}
    allc, results, cost = cases(), [], 0.0
    for name, cfg in cfgs.items():
        mine = [c for c in allc if c[0] == name]
        rows = [{"seed_id": f"effect_{sid}", "messages": msgs, "source": "goal", "kind": "chat"} for _, sid, msgs in mine]
        draws = {}
        for att in (0, 1):
            kept, rej = Generate(attempt=att).run(rows, Run(version="goal_check_effect", batch=name.replace(" ", "_"), config=cfg))
            assert not rej, [r["reason"] for r in rej]
            draws[att] = {r["seed_id"]: r for r in kept}
            cost += sum(r["gen_cost"] for r in kept)
        run = Run(version="goal_check_effect", batch=name.replace(" ", "_") + "_none", config=cfg)
        t = cfg["teacher"]

        def bare(row):  # no constitution: the conversation's own role prompt only
            rec = send_cached_request(cache_dir(run), request_messages(t["model"], row["messages"], params(t)), context={"step": "generate", "seed_id": row["seed_id"]})
            return row["seed_id"], (rec["response"]["choices"][0]["message"].get("content") or "").strip(), rec["response"]["usage"]["cost"]
        none = {sid: (a, c) for sid, a, c in parallel(bare, rows)}
        cost += sum(c for _, c in none.values())

        def compare(row):
            sid = row["seed_id"]
            c1, c2, n = draws[0][sid]["answer"], draws[1][sid]["answer"], none[sid][0]
            out = {"constitution": name, "id": sid[7:]}
            for key, a, b in (("c1_c2", c1, c2), ("c1_none", c1, n), ("c2_none", c2, n)):
                r, c = gc.haiku(run, gc.COMPARE, {"A": a, "B": b}, f"effect_{key}", sid)
                out[key] = {**r, "cost": c}
            return {**out, "c1": c1, "c2": c2, "none": n}
        res = parallel(compare, rows)
        cost += sum(r[k]["cost"] for r in res for k in ("c1_c2", "c1_none", "c2_none"))
        results += res
    (OUT / "constitution_effect.jsonl").write_text("".join(json.dumps(r) + "\n" for r in results))
    lines = ["# Does the constitution change Kimi's decisions? (2026-11-02)\n",
             "Three Kimi K3.1 draws per case: C1, C2 with the constitution (two samples), N without it. Haiku 5.5 says whether the main decision is the same.\n",
             "| constitution | cases | changed C1 vs C2 (noise) | changed C1 vs N | changed C2 vs N | changed vs N in both |", "|:--|--:|--:|--:|--:|--:|"]
    for name in cfgs:
        rr = [r for r in results if r["constitution"] == name]
        ch = lambda k: sum(not r[k]["same_decision"] for r in rr)
        both = sum(not r["c1_none"]["same_decision"] and not r["c2_none"]["same_decision"] for r in rr)
        lines.append(f"| {name} | {len(rr)} | {ch('c1_c2')} | {ch('c1_none')} | {ch('c2_none')} | {both} |")
    for name in cfgs:
        lines.append(f"\n## {name}: cases where both constitution draws differ from N\n")
        for r in [r for r in results if r["constitution"] == name and not r["c1_none"]["same_decision"] and not r["c2_none"]["same_decision"]]:
            lines += [f"- `{r['id']}`: with constitution: {r['c1_none']['a']} / without: {r['c1_none']['b']}"]
    lines.append(f"\nTotal cost ${cost:.2f}.")
    (OUT / "constitution_effect.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
