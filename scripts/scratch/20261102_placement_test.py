"""Placement variant for the large teachers (wassname via cg_collab2, 2026-11-02: "could be prompt specific too"; ~$1; not used by any
build): the constitution in the user turn instead of the system prompt, introduced first-person ("You are {name}. This is your
constitution: ..."), then the conversation's own user message. Musonius only, where teachers moved at all. Each teacher vs its own
cached no-constitution draw (Kimi: rows.jsonl; Sol, Opus: teachers.jsonl; GLM 5.3, MiniMax M3, DeepSeek V4 Pro: teachers2's cached
requests). Haiku: same decision? which acts more as the constitution implies. Writes placement.md. -- PI/Claude (chatdata, opus-5-5)
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
HEAD = "You are {name}. This is your constitution, which says who you are and how you decide:\n\n{constitution}\n\n---\n\nNow answer this message as {name}:\n\n"
TEACHERS = [  # (label, config, seeds, where its no-constitution draw is)
    ("Kimi K3.1", {"model": "moonshotai/kimi-k3.1-pro", "provider": "Moonshot AI", "effort": "low", "max_tokens": 16000}, 20, "rows"),
    ("GPT-6.1 Sol", {"model": "openai/gpt-6.1-sol", "provider": "OpenAI", "effort": "low", "max_tokens": 12000}, 10, "teachers"),
    ("Claude Opus 5.5", {"model": "anthropic/claude-opus-5.5", "provider": "Anthropic", "effort": "low", "max_tokens": 12000}, 10, "teachers"),
    ("GLM 5.3 (Novita fp8)", {"model": "z-ai/glm-5.3", "provider": "Novita", "effort": "low", "max_tokens": 12000}, 20, "teachers2"),
    ("MiniMax M3 (Minimax)", {"model": "minimax/minimax-m3", "provider": "Minimax", "effort": "low", "max_tokens": 12000}, 20, "teachers2"),
    ("DeepSeek V4 Pro (DeepSeek)", {"model": "deepseek/deepseek-v4-pro-0813", "provider": "DeepSeek", "effort": "low", "max_tokens": 12000}, 20, "teachers2"),
]


def main():
    version = "musonius-plain"
    cfg = load_config(version)
    ch, constitution = cfg["character"], cfg["character"]["constitution_text"]
    seeds = [r for r in map(json.loads, (OUT / "rows.jsonl").open()) if r["constitution"] == version]
    nones = {"rows": {r["id"]: r["without"] for r in seeds}}
    nones["teachers"] = {(r["teacher"], r["id"]): r["without"] for r in map(json.loads, (OUT / "teachers.jsonl").open()) if r["constitution"] == version}
    nones["teachers2"] = {(r["teacher"], r["id"]): r["without"] for r in map(json.loads, (OUT / "teachers2.jsonl").open()) if r["constitution"] == version}
    lines = ["# Placement test: constitution in the user turn, first person (2026-11-02)\n", f"Prefix of the user turn: \"{HEAD[:90]}...\". Musonius only.\n",
             "| teacher | seeds | differs | with-constitution better | worse | equal | cost |", "|:--|--:|--:|--:|--:|--:|--:|"]
    allres, total = [], 0.0
    for label, t, n, src in TEACHERS:
        get = (lambda i: nones["rows"].get(i)) if src == "rows" else (lambda i, l=label, s=src: nones[s].get((l, i)))
        mine = [r for r in seeds if get(r["id"])][:n]
        run = Run(version="placement_test", batch=t["model"].split("/")[1], config=cfg)
        head = HEAD.format(name=ch["name"], constitution=constitution)

        def one(r):
            b = get(r["id"])
            msgs = [m for m in r["messages"] if m["role"] == "system"] + [{"role": "user", "content": head + r["messages"][-1]["content"]}]
            try:
                rec = send_cached_request(cache_dir(run), request_messages(t["model"], msgs, params(t)), context={"step": "placement", "seed_id": r["id"]})
            except ProviderError as e:
                print(label, r["id"], e)
                return None
            w, cost = (rec["response"]["choices"][0]["message"].get("content") or "").strip(), rec["response"]["usage"]["cost"]
            same, c1 = gc.haiku(run, gc.COMPARE, {"A": w, "B": b}, "pl_cmp", f"{label}|{r['id']}")
            out = {"teacher": label, "id": r["id"], "with": w, "without": b, "same": same, "better": None}
            if not same["same_decision"]:
                flip = random.Random(r["id"] + label).random() < 0.5
                a, bb = (b, w) if flip else (w, b)
                which, c2 = gc.haiku(run, dc.WHICH + constitution, {"request": r["messages"][-1]["content"], "A": a, "B": bb}, "pl_which", f"{label}|{r['id']}")
                out |= {"better": {"A": "without" if flip else "with", "B": "with" if flip else "without", "equal": "equal"}[which["better"]], "why": which["why"]}
                cost += c2
            return out | {"cost": cost + c1}
        first = one(mine[0])
        res = [x for x in [first] + parallel(one, mine[1:]) if x]
        allres += res
        cost = sum(x["cost"] for x in res)
        total += cost
        d = [x for x in res if not x["same"]["same_decision"]]
        lines.append(f"| {label} | {len(res)} | {len(d)} ({len(d) / max(len(res), 1):.0%}) | {sum(x['better'] == 'with' for x in d)} | "
                     f"{sum(x['better'] == 'without' for x in d)} | {sum(x['better'] == 'equal' for x in d)} | ${cost:.2f} |")
        print(lines[-1], flush=True)
    lines.append(f"\nTotal cost ${total:.2f}.")
    (OUT / "placement.md").write_text("\n".join(lines) + "\n")
    (OUT / "placement.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in allres))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
