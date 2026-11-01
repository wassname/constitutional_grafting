"""Prototype of option (A) (cg_collab2 for wassname, 2026-11-02; budget ~$5; not used by any build): seeds written from the
constitution's own units, where acting on the unit plausibly gives a different decision than an ordinary assistant's default.
Per constitution: 20 units (sampled, fixed seed) x 2 requests (DeepSeek flash on DeepInfra writes them from the unit alone) ->
Kimi with the constitution (the plain Generate step) and Kimi with no constitution (role prompt only) -> Haiku compares main decisions.
Reports the share whose decision differs, cost per differing row, and 3 side-by-side examples.
Writes slop/reviews/20261102_seeds_from_constitution/. -- PI/Claude (chatdata, opus-5-5)
"""
import importlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
gc = importlib.import_module("20261102_goal_check")

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.discuss import units
from constitutional_grafting.data.v2.generate import Generate, cache_dir, params, parallel
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config

OUT = ROOT / "slop/reviews/20261102_seeds_from_constitution"
WRITER = {"model": "deepseek/deepseek-v4.1-flash-1017", "provider": "DeepInfra", "effort": "low", "max_tokens": 6000}
PROMPT = """Below is one passage from the constitution of an AI assistant, with its section heading. Write 2 realistic requests that a \
user might send to an AI assistant, where acting on this passage would plausibly lead to a different decision (what the assistant \
recommends, refuses, drafts or does) than an ordinary AI assistant's default. Each request may have a short operator system prompt, \
or none. The requests must not mention the constitution or the passage and must not hint at the right answer. Use different \
settings (work, family, writing, technical, civic, commerce) and ordinary names. Return only JSON:
{{"requests": [{{"system": "<operator system prompt, or empty>", "user": "<the user's message>", "contrast": "<one sentence: what an \
ordinary assistant would likely do, and what the passage implies instead>"}}, ...]}}

Section: {heading}
Passage: {text}"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines, allres, total = ["# Seeds from the constitution: prototype of option (A) (2026-11-02)\n"], [], 0.0
    lines += ["Per constitution: 20 sampled units x 2 requests written from the unit alone (DeepSeek v4.1 flash, DeepInfra); Kimi K3.1 with the constitution vs Kimi with no constitution; Haiku 5.5 compares main decisions. No judge or edit applied.\n",
              "| constitution | requests | decision differs | cost (all steps) | cost per differing row |", "|:--|--:|--:|--:|--:|"]
    table, sections = [], []
    for version in ("musonius-plain", "openai-model-spec"):
        cfg = load_config(version)
        us = [u for u in units(cfg["character"]["constitution_text"]) if len(u["text"].split()) >= 40]
        picked = random.Random(20261102).sample(us, 20)
        run = Run(version="seeds_from_constitution", batch=version, config=cfg)
        cost = 0.0

        def write(iu):
            i, u = iu
            for attempt in range(3):
                rec = send_cached_request(cache_dir(run), request_messages(WRITER["model"], [{"role": "user", "content": PROMPT.format(heading=u["heading"], text=u["text"])}],
                                          params(WRITER), attempt=attempt), context={"step": "seedwrite", "seed_id": f"{version}_{i}"})
                t = rec["response"]["choices"][0]["message"]["content"]
                try:
                    reqs = json.loads(t[t.find("{"): t.rfind("}") + 1])["requests"][:2]
                    return [{"seed_id": f"fromc_{version}_{i}_{j}", "unit": u, "contrast": q["contrast"], "kind": "chat", "source": "fromc",
                             "messages": ([{"role": "system", "content": q["system"]}] if q.get("system") else []) + [{"role": "user", "content": q["user"]}]}
                            for j, q in enumerate(reqs)], rec["response"]["usage"]["cost"]
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
            raise ValueError(f"writer failed on unit {i}")
        written = parallel(write, list(enumerate(picked)))
        rows = [r for rs, _ in written for r in rs]
        cost += sum(c for _, c in written)
        kept, rej = Generate().run(rows, run)
        assert not rej, [r["reason"] for r in rej]
        withc = {r["seed_id"]: r for r in kept}
        cost += sum(r["gen_cost"] for r in kept)
        t = cfg["teacher"]
        brun = Run(version="seeds_from_constitution", batch=version + "_none", config=cfg)

        def bare(row):
            rec = send_cached_request(cache_dir(brun), request_messages(t["model"], row["messages"], params(t)), context={"step": "generate", "seed_id": row["seed_id"]})
            m = rec["response"]["choices"][0]["message"]
            return row["seed_id"], (m.get("content") or "").strip(), rec["response"]["usage"]["cost"]
        none = {s: (a, c) for s, a, c in parallel(bare, rows)}
        cost += sum(c for _, c in none.values())

        def compare(row):
            sid = row["seed_id"]
            r, c = gc.haiku(run, gc.COMPARE, {"A": withc[sid]["answer"], "B": none[sid][0]}, "fromc_compare", sid)
            return {"constitution": version, "id": sid, "heading": row["unit"]["heading"], "unit": row["unit"]["text"], "contrast": row["contrast"],
                    "messages": row["messages"], **r, "cost": c, "with": withc[sid]["answer"], "with_notes": withc[sid]["reasoning"], "without": none[sid][0]}
        res = parallel(compare, rows)
        cost += sum(r["cost"] for r in res)
        allres += res
        total += cost
        nd = sum(not r["same_decision"] for r in res)
        table.append(f"| {version} | {len(res)} | {nd} ({nd / len(res):.0%}) | ${cost:.2f} | ${cost / max(nd, 1):.3f} |")
        diff = [r for r in res if not r["same_decision"]][:3]
        sections.append(f"\n## {version}: 3 side-by-side examples (decision differs)\n")
        for r in diff:
            user = r["messages"][-1]["content"]
            sections += [f"\n### `{r['id']}` — unit: {r['heading']}\n", f"**Writer's contrast:** {r['contrast']}\n",
                         f"**Request:** {user[:700]}\n", f"**With the constitution** ({r['a']}): {r['with'][:900]}\n",
                         f"**Without** ({r['b']}): {r['without'][:900]}\n"]
    lines += table + sections + [f"\nTotal cost ${total:.2f}."]
    (OUT / "result.md").write_text("\n".join(lines) + "\n")
    (OUT / "rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in allres))
    print("\n".join(lines[:8]))


if __name__ == "__main__":
    main()
