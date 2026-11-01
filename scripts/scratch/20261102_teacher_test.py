"""Option (D) test (cg_collab2 for wassname, 2026-11-02, budget ~$6; not used by any build): is it Kimi or the seeds? Same 80
constitution-derived seeds as 20261102_seeds_from_constitution. Each teacher answers with the constitution and with no constitution
(its own draw); Haiku compares main decisions. DeepSeek V4.1 Flash (DeepInfra) on all 80, plus a second with-constitution draw for its
noise floor; GPT-6.1 Sol and Claude Opus 5.5 on a 20-seed subset (10 per constitution).
Writes slop/reviews/20261102_seeds_from_constitution/teachers.md. -- PI/Claude (chatdata, opus-5-5)
"""
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
gc = importlib.import_module("20261102_goal_check")

from constitutional_grafting.data.model_requests import ProviderError, request_messages, send_cached_request
from constitutional_grafting.data.v2.generate import cache_dir, parallel, params, with_constitution
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config

OUT = ROOT / "slop/reviews/20261102_seeds_from_constitution"
TEACHERS = [  # (label, config, seeds per constitution, noise draw)
    ("DeepSeek V4.1 Flash", {"model": "deepseek/deepseek-v4.1-flash-1017", "provider": "DeepInfra", "effort": "low", "max_tokens": 12000}, 40, True),
    ("GPT-6.1 Sol", {"model": "openai/gpt-6.1-sol", "provider": "OpenAI", "effort": "low", "max_tokens": 12000}, 10, False),
    ("Claude Opus 5.5", {"model": "anthropic/claude-opus-5.5", "provider": "Anthropic", "effort": "low", "max_tokens": 12000}, 10, False),
]


def main():
    rows = [json.loads(l) for l in (OUT / "rows.jsonl").open()]
    lines = ["# Teacher test, option (D) (2026-11-02)\n",
             "Same constitution-derived seeds. Each teacher: with the constitution vs its own no-constitution draw; Haiku 5.5 compares main decisions. Kimi row from result.md.\n",
             "| teacher | constitution | seeds | decision differs, with vs without | noise (two with-constitution draws) | cost | cost per differing row |",
             "|:--|:--|--:|--:|--:|--:|--:|"]
    for version in ("musonius-plain", "openai-model-spec"):
        mine = [r for r in rows if r["constitution"] == version]
        k = sum(not r["same_decision"] for r in mine)
        lines.append(f"| Kimi K3.1 (earlier) | {version} | {len(mine)} | {k} ({k / len(mine):.0%}) | ~3% (other seeds) | | |")
    out, examples = [], []
    for label, t, n, noise in TEACHERS:
        for version in ("musonius-plain", "openai-model-spec"):
            cfg = load_config(version)
            mine = [r for r in rows if r["constitution"] == version][:n]
            run = Run(version="teacher_test", batch=f"{version}_{t['model'].split('/')[1]}", config=cfg)

            def call(msgs, sid, attempt=0):
                for k in range(3):  # a provider error mid-response (finish_reason error) is redrawn
                    try:
                        rec = send_cached_request(cache_dir(run), request_messages(t["model"], msgs, params(t), attempt=attempt + 20 * k), context={"step": "teacher_test", "seed_id": sid})
                        return (rec["response"]["choices"][0]["message"].get("content") or "").strip(), rec["response"]["usage"]["cost"]
                    except ProviderError as e:  # a provider policy refusal is not the model's decision: the seed is dropped for this teacher
                        print(f"{label} {sid}: {e}; seed skipped")
                        return None, 0.0
                    except ValueError as e:
                        print(f"{label} {sid}: {e}; redraw")
                raise ValueError(f"{label} {sid}: 3 failed responses")

            def one(r):
                w, c1 = call(with_constitution(run, r["messages"]), r["id"])
                b, c2 = call(r["messages"], r["id"] + "_none")
                if w is None or b is None:
                    return None
                cmp, c3 = gc.haiku(run, gc.COMPARE, {"A": w, "B": b}, "teacher_cmp", r["id"])
                res = {"teacher": label, "constitution": version, "id": r["id"], "heading": r["heading"], "with": w, "without": b, "cmp": cmp}
                cost = c1 + c2 + c3
                if noise:
                    w2, c4 = call(with_constitution(run, r["messages"]), r["id"], attempt=1)
                    cmp2, c5 = gc.haiku(run, gc.COMPARE, {"A": w, "B": w2}, "teacher_noise", r["id"])
                    res |= {"with2": w2, "noise": cmp2}
                    cost += c4 + c5
                return res | {"cost": cost, "user": r["messages"][-1]["content"]}
            first = one(mine[0])  # warm the prompt cache with the constitution prefix before parallel calls
            res = [x for x in [first] + parallel(one, mine[1:]) if x is not None]
            skipped = len(mine) - len(res)
            out += res
            d = sum(not x["cmp"]["same_decision"] for x in res)
            nz = f"{sum(not x['noise']['same_decision'] for x in res)}/{len(res)}" if noise else "not run"
            cost = sum(x["cost"] for x in res)
            lines.append(f"| {label} | {version} | {len(res)}{f' ({skipped} refused by provider)' if skipped else ''} | {d} ({d / len(res):.0%}) | {nz} | ${cost:.2f} | ${cost / max(d, 1):.3f} |")
            for x in [x for x in res if not x["cmp"]["same_decision"]][:1]:
                examples += [f"\n### {label}, {version} `{x['id']}` — {x['heading']}\n", f"**Request:** {x['user'][:500]}\n",
                             f"**With** ({x['cmp']['a']}): {x['with'][:700]}\n", f"**Without** ({x['cmp']['b']}): {x['without'][:700]}\n"]
    (OUT / "teachers.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
    (OUT / "teachers.md").write_text("\n".join(lines + ["\n## One example per teacher and constitution (decision differs)"] + examples) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
