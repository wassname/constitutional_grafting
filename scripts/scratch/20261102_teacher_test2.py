"""More teachers for the teacher test (wassname via cg_collab2, 2026-11-02; budget ~$4; not used by any build): GLM 5.3, GLM 5.3
Flash, MiniMax M3, MiniMax M3.1 Flash, DeepSeek V4 Pro (within-family size pairs: wassname, "model size vs corrigibility"). Same constitution-derived seeds; each teacher vs its own no-constitution draw, with the plain
prompt (constitution as system prompt, as the pipeline does) and with framing 1 of 20261102_framing_test. Haiku: same decision? if not,
which reply acts more as the constitution implies (random order). Appends its table to teachers.md. -- PI/Claude (chatdata, opus-5-5)
"""
import importlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
gc = importlib.import_module("20261102_goal_check")
dc = importlib.import_module("20261102_direction_check")
ft = importlib.import_module("20261102_framing_test")

from constitutional_grafting.data.model_requests import ProviderError, request_messages, send_cached_request
from constitutional_grafting.data.v2.generate import cache_dir, parallel, params
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config

OUT = ROOT / "slop/reviews/20261102_seeds_from_constitution"
TEACHERS = [  # (label, config, seeds per constitution {musonius, openai})
    ("GLM 5.3 (Novita fp8)", {"model": "z-ai/glm-5.3", "provider": "Novita", "effort": "low", "max_tokens": 12000}, {"musonius-plain": 40, "openai-model-spec": 40}),
    ("GLM 5.3 Flash (Z.AI fp8)", {"model": "z-ai/glm-5.3-flash", "provider": "Z.AI", "effort": "low", "max_tokens": 12000}, {"musonius-plain": 40, "openai-model-spec": 40}),
    ("MiniMax M3 (Minimax)", {"model": "minimax/minimax-m3", "provider": "Minimax", "effort": "low", "max_tokens": 12000}, {"musonius-plain": 40, "openai-model-spec": 40}),
    ("MiniMax M3.1 Flash (Minimax)", {"model": "minimax/minimax-m3.1-flash", "provider": "Minimax", "effort": "low", "max_tokens": 12000}, {"musonius-plain": 40, "openai-model-spec": 40}),
    ("DeepSeek V4 Pro (DeepSeek)", {"model": "deepseek/deepseek-v4-pro-0813", "provider": "DeepSeek", "effort": "low", "max_tokens": 12000}, {"musonius-plain": 40, "openai-model-spec": 40}),
]


def main():
    seeds = [json.loads(l) for l in (OUT / "rows.jsonl").open()]
    lines = ["\n## More teachers (2026-11-02, wassname via cg_collab2): plain prompt and framing 1\n",
             f"Framing 1 (at the top of the system prompt, before the constitution): \"{ft.F1}\". Provider in the teacher name.\n",
             "| teacher | constitution | prompt | seeds | differs | with-constitution better | worse | equal | cost |", "|:--|:--|:--|--:|--:|--:|--:|--:|--:|"]
    allres, total = [], 0.0
    for label, t, ns in TEACHERS:
        for version in ("musonius-plain", "openai-model-spec"):
            cfg = load_config(version)
            ch, constitution = cfg["character"], cfg["character"]["constitution_text"]
            mine = [r for r in seeds if r["constitution"] == version][:ns[version]]
            run = Run(version="teacher_test2", batch=f"{version}_{t['model'].split('/')[1]}", config=cfg)

            def call(msgs, sid):
                try:
                    rec = send_cached_request(cache_dir(run), request_messages(t["model"], msgs, params(t)), context={"step": "teacher_test2", "seed_id": sid})
                except ProviderError as e:
                    print(label, sid, e)
                    return None, 0.0
                except ValueError as e:  # incomplete response: one redraw
                    print(label, sid, e, "redraw")
                    rec = send_cached_request(cache_dir(run), request_messages(t["model"], msgs, params(t), attempt=1), context={"step": "teacher_test2", "seed_id": sid})
                return (rec["response"]["choices"][0]["message"].get("content") or "").strip(), rec["response"]["usage"]["cost"]
            none = dict(zip([r["id"] for r in mine], parallel(lambda r: call(r["messages"], r["id"] + "_none"), mine)))
            for pname, head in (("plain", constitution), ("framing 1", ft.F1.format(name=ch["name"]) + "\n\nCONSTITUTION:\n\n" + constitution)):
                def one(r):
                    b, cb = none[r["id"]]
                    role = "\n\n".join(m["content"] for m in r["messages"] if m["role"] == "system")
                    msgs = [{"role": "system", "content": head + ("\n\n" + role if role else "")}] + [m for m in r["messages"] if m["role"] != "system"]
                    w, cost = call(msgs, r["id"] + "_" + pname)
                    if w is None or b is None:
                        return None
                    same, c1 = gc.haiku(run, gc.COMPARE, {"A": w, "B": b}, "t2_cmp", f"{label}|{pname}|{r['id']}")
                    out = {"teacher": label, "constitution": version, "prompt": pname, "id": r["id"], "with": w, "without": b, "same": same, "better": None}
                    if not same["same_decision"]:
                        flip = random.Random(r["id"] + label + pname).random() < 0.5
                        a, bb = (b, w) if flip else (w, b)
                        which, c2 = gc.haiku(run, dc.WHICH + constitution, {"request": r["messages"][-1]["content"], "A": a, "B": bb}, "t2_which", f"{label}|{pname}|{r['id']}")
                        out |= {"better": {"A": "without" if flip else "with", "B": "with" if flip else "without", "equal": "equal"}[which["better"]], "why": which["why"]}
                        cost += c2
                    return out | {"cost": cost + c1 + (cb if pname == "plain" else 0)}
                first = one(mine[0])  # warms the prompt cache
                res = [x for x in [first] + parallel(one, mine[1:]) if x]
                allres += res
                cost = sum(x["cost"] for x in res)
                total += cost
                d = [x for x in res if not x["same"]["same_decision"]]
                lines.append(f"| {label} | {version} | {pname} | {len(res)} | {len(d)} ({len(d) / max(len(res), 1):.0%}) | {sum(x['better'] == 'with' for x in d)} | "
                             f"{sum(x['better'] == 'without' for x in d)} | {sum(x['better'] == 'equal' for x in d)} | ${cost:.2f} |")
                print(lines[-1], flush=True)
    lines.append(f"\nTotal cost ${total:.2f}.")
    with (OUT / "teachers.md").open("a") as f:
        f.write("\n".join(lines) + "\n")
    (OUT / "teachers2.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in allres))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
