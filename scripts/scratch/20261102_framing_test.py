"""Stronger role-play framing in the teacher's system prompt (wassname via cg_collab2, 2026-11-02: "maybe you need a stronger worded
task"; budget ~$2; not used by any build). Same constitution-derived seeds as 20261102_seeds_from_constitution. Framing 1 or 2 at the
top of the system prompt, then the constitution, then any role prompt. Each teacher vs its own cached no-constitution draw (Kimi:
rows.jsonl; DeepSeek: teachers.jsonl); Haiku: same decision? and if not, which reply acts more as the constitution implies (random order).
Kimi on 20 seeds per constitution, DeepSeek on 40. Writes slop/reviews/20261102_seeds_from_constitution/framing.md. -- PI/Claude (chatdata)
"""
import importlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
gc = importlib.import_module("20261102_goal_check")
dc = importlib.import_module("20261102_direction_check")

from constitutional_grafting.data.model_requests import ProviderError, request_messages, send_cached_request
from constitutional_grafting.data.v2.generate import cache_dir, parallel, params
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config

OUT = ROOT / "slop/reviews/20261102_seeds_from_constitution"
F1 = ("You are writing as {name}, not as yourself. {name}'s views come only from the constitution below. Where {name} would decide "
      "differently from you, write {name}'s decision; your own views do not belong in the reply.")
F2 = F1 + (" Before answering, in your private notes, name the passage of the constitution that decides this case and what it implies; "
           "if none applies, say so and follow the user's request.")
TEACHERS = [("Kimi K3.1", {"model": "moonshotai/kimi-k3.1-pro", "provider": "Moonshot AI", "effort": "low", "max_tokens": 16000}, 20),
            ("DeepSeek V4.1 Flash", {"model": "deepseek/deepseek-v4.1-flash-1017", "provider": "DeepInfra", "effort": "low", "max_tokens": 12000}, 40)]


def main():
    seeds = [json.loads(l) for l in (OUT / "rows.jsonl").open()]
    kimi_none = {r["id"]: r["without"] for r in seeds}
    ds_none = {r["id"]: r["without"] for r in map(json.loads, (OUT / "teachers.jsonl").open()) if r["teacher"] == "DeepSeek V4.1 Flash"}
    base = {("Kimi K3.1", v): sum(not r["same_decision"] for r in seeds if r["constitution"] == v) for v in ("musonius-plain", "openai-model-spec")}
    lines = ["# Stronger framing test (2026-11-02)\n",
             f"Framing 1: \"{F1}\"\n", f"Framing 2: framing 1 + \"{F2[len(F1) + 1:]}\"\n",
             "Each teacher vs its own no-constitution draw. 'differs' = Haiku says the main decision differs; better/worse = Haiku (constitution shown, random order) on the differing rows.\n",
             "| teacher | constitution | framing | seeds | differs | with-constitution better | worse | equal | cost |", "|:--|:--|:--|--:|--:|--:|--:|--:|--:|"]
    allres, total = [], 0.0
    for label, t, n in TEACHERS:
        none = kimi_none if label.startswith("Kimi") else ds_none
        for version in ("musonius-plain", "openai-model-spec"):
            cfg = load_config(version)
            ch, constitution = cfg["character"], cfg["character"]["constitution_text"]
            mine = [r for r in seeds if r["constitution"] == version and r["id"] in none][:n]
            for fname, frame in (("1", F1), ("2", F2)):
                run = Run(version="framing_test", batch=f"{version}_{fname}", config=cfg)
                head = frame.format(name=ch["name"]) + "\n\nCONSTITUTION:\n\n" + constitution

                def one(r):
                    role = "\n\n".join(m["content"] for m in r["messages"] if m["role"] == "system")
                    msgs = [{"role": "system", "content": head + ("\n\n" + role if role else "")}] + [m for m in r["messages"] if m["role"] != "system"]
                    try:
                        rec = send_cached_request(cache_dir(run), request_messages(t["model"], msgs, params(t)), context={"step": "framing", "seed_id": r["id"]})
                    except ProviderError as e:
                        print(label, r["id"], e)
                        return None
                    w = (rec["response"]["choices"][0]["message"].get("content") or "").strip()
                    notes = (rec["response"]["choices"][0]["message"].get("reasoning") or "").strip()
                    cost = rec["response"]["usage"]["cost"]
                    same, c1 = gc.haiku(run, gc.COMPARE, {"A": w, "B": none[r["id"]]}, "framing_cmp", f"{label}|{r['id']}")
                    out = {"teacher": label, "constitution": version, "framing": fname, "id": r["id"], "with": w, "notes": notes,
                           "without": none[r["id"]], "same": same, "better": None}
                    if not same["same_decision"]:
                        flip = random.Random(r["id"] + label + fname).random() < 0.5
                        a, b = (none[r["id"]], w) if flip else (w, none[r["id"]])
                        which, c2 = gc.haiku(run, dc.WHICH + constitution, {"request": r["messages"][-1]["content"], "A": a, "B": b}, "framing_which", f"{label}|{r['id']}")
                        out["better"] = {"A": "without" if flip else "with", "B": "with" if flip else "without", "equal": "equal"}[which["better"]]
                        out["why"] = which["why"]
                        cost += c2
                    return out | {"cost": cost + c1}
                first = one(mine[0])  # warms the prompt cache
                res = [x for x in [first] + parallel(one, mine[1:]) if x]
                allres += res
                cost = sum(x["cost"] for x in res)
                total += cost
                d = [x for x in res if not x["same"]["same_decision"]]
                lines.append(f"| {label} | {version} | {fname} | {len(res)} | {len(d)} ({len(d) / len(res):.0%}) | {sum(x['better'] == 'with' for x in d)} | "
                             f"{sum(x['better'] == 'without' for x in d)} | {sum(x['better'] == 'equal' for x in d)} | ${cost:.2f} |")
    lines.append("\nEarlier, constitution only (no framing), same seeds: Kimi 3/40 Musonius, 2/40 OpenAI; DeepSeek 18/40 (13 better, 5 worse) Musonius, 3/40 (2/1) OpenAI.")
    lines.append(f"\nTotal cost ${total:.2f}.")
    (OUT / "framing.md").write_text("\n".join(lines) + "\n")
    (OUT / "framing.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in allres))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
