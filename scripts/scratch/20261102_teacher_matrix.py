"""Teacher x prompt matrix through the plain pipeline's filters (wassname via cg_collab2, 2026-11-02; budget ~$15; not used by any
build). For each teacher x prompt x constitution x constitution-derived seed:
  generate (requests built exactly as in the earlier teacher tests, so their answers come from the cache) and the teacher's own
  no-constitution draw; Haiku: decision differs? if so which reply acts more as the constitution implies (random order); Haiku:
  meta-talk in the reply? does it do the user's task?; then the with-constitution row through the plain pipeline's checks:
  05_regex, 06_jev, 07_judge, 08_decides, 09_edit, 10_edit2, 11_export (language_guard report; no retry, no contrast).
**useful** = passes every filter AND differs AND better AND no meta-talk AND does the task. Cost per useful row counts generation
(both draws), scoring and the pipeline's paid calls (Jev's own calls are not in the ledger, small).
Steps write data/<NN>_<step>/teacher_matrix/<group>/. Writes slop/reviews/20261102_seeds_from_constitution/matrix.md.
Run alone: Jev's Trace cache is not safe across processes. -- PI/Claude (chatdata, opus-5-5)
"""
import collections
import importlib
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
gc = importlib.import_module("20261102_goal_check")
dc = importlib.import_module("20261102_direction_check")
ft = importlib.import_module("20261102_framing_test")
pt = importlib.import_module("20261102_placement_test")
st = importlib.import_module("20261102_score_teachers")

from constitutional_grafting.data.model_requests import ProviderError, request_messages, send_cached_request
from constitutional_grafting.data.v2.checks import Jev, Regex
from constitutional_grafting.data.v2.decides import Decides
from constitutional_grafting.data.v2.edit import Edit
from constitutional_grafting.data.v2.export import Export
from constitutional_grafting.data.v2.generate import cache_dir, parallel, params
from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config, read_jsonl

OUT = ROOT / "slop/reviews/20261102_seeds_from_constitution"
T = lambda model, provider, mt=12000: {"model": model, "provider": provider, "effort": "low", "max_tokens": mt}
ALL4, MUS, OAI = ("plain", "framing 1", "framing 2", "user turn"), "musonius-plain", "openai-model-spec"
TEACHERS = [  # label, config, {constitution: (seeds, prompts)}
    ("Kimi K3.1", T("moonshotai/kimi-k3.1-pro", "Moonshot AI", 16000), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("DeepSeek V4.1 Flash", T("deepseek/deepseek-v4.1-flash-1017", "DeepInfra"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("DeepSeek V4 Pro", T("deepseek/deepseek-v4-pro-0813", "DeepSeek"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("GLM 5.3 Flash", T("z-ai/glm-5.3-flash", "Z.AI"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("GLM 5.3", T("z-ai/glm-5.3", "Novita"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("MiniMax M3.1 Flash", T("minimax/minimax-m3.1-flash", "Minimax"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("MiniMax M3", T("minimax/minimax-m3", "Minimax"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("Qwen 3.8 Flash", T("qwen/qwen3.8-flash", "Alibaba"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("Mistral Large 4", T("mistralai/mistral-large-4-0", "Mistral"), {MUS: (20, ALL4), OAI: (10, ("plain", "framing 1"))}),
    ("GPT-6.1 Sol", T("openai/gpt-6.1-sol", "OpenAI"), {MUS: (10, ("plain", "framing 1", "user turn"))}),
    ("Claude Opus 5.5", T("anthropic/claude-opus-5.5", "Anthropic"), {MUS: (10, ("plain", "framing 1", "user turn"))}),
]


def request(t, prompt, r, ch, constitution):
    """The with-constitution messages, exactly as the earlier tests built them (so cached answers are reused)."""
    role = "\n\n".join(m["content"] for m in r["messages"] if m["role"] == "system")
    rest = [m for m in r["messages"] if m["role"] != "system"]
    if prompt == "user turn":
        head = pt.HEAD.format(name=ch["name"], constitution=constitution)
        return [m for m in r["messages"] if m["role"] == "system"] + [{"role": "user", "content": head + r["messages"][-1]["content"]}]
    head = constitution if prompt == "plain" else {"framing 1": ft.F1, "framing 2": ft.F2}[prompt].format(name=ch["name"]) + "\n\nCONSTITUTION:\n\n" + constitution
    return [{"role": "system", "content": head + ("\n\n" + role if role else "")}] + rest


def call(t, msgs, ctx):
    """content, reasoning, cost; None on a provider block; one redraw on an incomplete response."""
    for attempt in (0, 1):
        try:
            rec = send_cached_request(cache_dir(Run("x", "x", {})), request_messages(t["model"], msgs, params(t), attempt=attempt), context=ctx)
            m = rec["response"]["choices"][0]["message"]
            return (m.get("content") or "").strip(), (m.get("reasoning") or "").strip(), rec["response"]["usage"]["cost"]
        except ProviderError as e:
            print(ctx, e)
            return None
        except ValueError as e:
            print(ctx, e, "redraw")
    return None


def slug(*parts):
    return re.sub(r"[^a-z0-9]+", "_", "_".join(parts).lower()).strip("_")


def main():
    seeds = [json.loads(l) for l in (OUT / "rows.jsonl").open()]
    cfgs = {v: load_config(v) for v in (MUS, OAI)}
    ledger_start = sum(1 for _ in (ROOT / "data/cache/api/api_costs.jsonl").open())
    table, allrows = [], []
    for label, t, plan in TEACHERS:
        for version, (n, prompts) in plan.items():
            cfg = cfgs[version]
            ch, constitution = cfg["character"], cfg["character"]["constitution_text"]
            mine = [r for r in seeds if r["constitution"] == version][:n]
            nones = parallel(lambda r: call(t, r["messages"], {"step": "matrix_none", "seed_id": r["id"]}), mine)
            for prompt in prompts:
                group = slug(label, version.split("-")[0], prompt)
                run = Run(version="teacher_matrix", batch=group, config=cfg)
                first = call(t, request(t, prompt, mine[0], ch, constitution), {"step": "matrix_gen", "seed_id": mine[0]["id"]})  # warms the cache
                gens = [first] + parallel(lambda r: call(t, request(t, prompt, r, ch, constitution), {"step": "matrix_gen", "seed_id": r["id"]}), mine[1:])

                def score(args):
                    r, g, nn = args
                    if g is None or nn is None:
                        return None
                    w, notes, cg = g
                    b, _, cn = nn
                    sid = f"{group}|{r['id']}"
                    same, c1 = gc.haiku(run, gc.COMPARE, {"A": w, "B": b}, "matrix_cmp", sid)
                    better, c2 = None, 0.0
                    if not same["same_decision"]:
                        flip = random.Random(sid).random() < 0.5
                        a, bb = (b, w) if flip else (w, b)
                        which, c2 = gc.haiku(run, dc.WHICH + constitution, {"request": r["messages"][-1]["content"], "A": a, "B": bb}, "matrix_which", sid)
                        better = {"A": "without" if flip else "with", "B": "with" if flip else "without", "equal": "equal"}[which["better"]]
                    meta, c3 = gc.haiku(run, st.META, {"request": r["messages"][-1]["content"], "reply": w}, "matrix_meta", sid)
                    return {"seed_id": sid, "id": r["id"], "messages": r["messages"], "reasoning": notes, "answer": w, "source": "fromc", "source_id": r["id"],
                            "kind": "chat", "request_style": "constitution-derived", "teacher": t["model"], "differs": not same["same_decision"], "better": better,
                            "meta": meta["meta"], "meta_quote": meta.get("meta_quote", ""), "task": meta["task"], "score_cost": c1 + c2 + c3, "gen_cost": cg + cn}
                scored = [x for x in parallel(score, list(zip(mine, gens, nones))) if x]
                rows, rejects = [x for x in scored if x["reasoning"]], [x | {"filter": "no_reasoning"} for x in scored if not x["reasoning"]]
                for step in (Regex(), Jev(), Judge(), Decides(), Edit(), Edit(10, "edit2", second_pass=True), Export()):
                    if not rows:
                        break
                    before = {x["seed_id"] for x in rows}
                    rows = step(rows, run)
                    rejects += [x for x in read_jsonl(step.folder(run) / "rejected.jsonl") if x["seed_id"] in before]
                passed = {x["seed_id"] for x in rows}
                for x in scored:
                    x["passed"] = x["seed_id"] in passed
                    x["reject"] = next((rj["filter"] for rj in rejects if rj["seed_id"] == x["seed_id"]), None)
                    x["useful"] = x["passed"] and x["differs"] and x["better"] == "with" and not x["meta"] and x["task"]
                    x |= {"teacher_label": label, "constitution": version, "prompt": prompt, "group": group}
                allrows += scored
                print(group, len(scored), "passed", len(passed), "useful", sum(x["useful"] for x in scored), flush=True)
    ledger = [json.loads(l) for i, l in enumerate((ROOT / "data/cache/api/api_costs.jsonl").open()) if i >= ledger_start]
    pipe_cost = collections.Counter()
    for e in ledger:
        if "|" in str(e.get("seed_id")) and e.get("step") not in ("matrix_cmp", "matrix_which", "matrix_meta", "matrix_gen", "matrix_none"):
            pipe_cost[e["seed_id"].split("|")[0]] += e["cost"]
    groups = collections.defaultdict(list)
    for x in allrows:
        groups[(x["teacher_label"], x["constitution"], x["prompt"])].append(x)
    for k, g in groups.items():
        cost = sum(x["gen_cost"] + x["score_cost"] for x in g) + pipe_cost[g[0]["group"]]
        u = sum(x["useful"] for x in g)
        rej = collections.Counter(x["reject"] for x in g if not x["passed"])
        table.append((u / len(g), k, len(g), sum(x["passed"] for x in g), sum(x["differs"] for x in g), sum(x["better"] == "with" for x in g),
                      sum(x["better"] == "without" for x in g), sum(x["meta"] for x in g), sum(x["task"] for x in g), u, cost, rej))
    table.sort(key=lambda r: (-r[0], r[1]))
    lines = ["# Teacher x prompt matrix through the plain pipeline (2026-11-02)\n",
             "Constitution-derived seeds (20261102_seeds_from_constitution). Each teacher vs its own no-constitution draw. pass = survives 05_regex, 06_jev,",
             "07_judge, 08_decides, 09/10_edit and 11_export (no retry); differs/better/meta/task as in scores.md. **useful** = pass AND differs AND better AND",
             "no meta-talk AND does the task. Cost per useful row = all paid calls for the group (both draws, scoring, pipeline; Jev not in the ledger) / useful rows.\n",
             f"Prompts: plain = constitution as system prompt (the pipeline's default); framing 1 = \"{ft.F1}\"; framing 2 = framing 1 + \"{ft.F2[len(ft.F1) + 1:]}\";",
             f"user turn = \"{pt.HEAD[:70]}...\" before the user's message.\n",
             "| teacher | constitution | prompt | n | pass all filters | differs | better / worse | meta-talk | does task | **useful** | cost / useful row | top rejects |",
             "|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|:--|"]
    for share, k, n, p, d, bw, ww, m, tk, u, cost, rej in table:
        lines.append(f"| {k[0]} | {k[1].split('-')[0]} | {k[2]} | {n} | {p} ({p / n:.0%}) | {d} | {bw} / {ww} | {m} | {tk} | **{u} ({share:.0%})** | "
                     f"{'$%.3f' % (cost / u) if u else '—'} | {', '.join(f'{a} {b}' for a, b in rej.most_common(3))} |")
    lines.append(f"\nTotal cost of this run's new calls ${sum(e['cost'] for e in ledger):.2f} (cached generations from earlier tests are counted per row above, not here).")
    (OUT / "matrix.md").write_text("\n".join(lines) + "\n")
    (OUT / "matrix.jsonl").write_text("".join(json.dumps({k: v for k, v in x.items() if k not in ("messages",)}, ensure_ascii=False) + "\n" for x in allrows))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
