# Fidelity repair test on the same 20 route rows: check the route-stage English (before the identity edit) with Luna and MiMo,
# let Luna fix only the flagged spans, recheck with fresh samples, and write a packet for the same GPT-6.1 sol read as read2.md.
# Usage: uv run --env-file .env python scripts/scratch/20261028_fidelity_repair.py   -- PI/Claude (opus-5-5), 2026-10-28
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.route import CHECK, LANG, REPAIR

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/scratch/20261028_fidelity_calib"
CACHE = ROOT / "data/cache/api"


def pin(provider, **kw):
    return {"provider": {"only": [provider], "allow_fallbacks": False, "require_parameters": True}, "usage": {"include": True},
            "include_reasoning": True, **kw}


MODELS = {"luna": ("openai/gpt-6-luna", pin("OpenAI", max_tokens=12000, reasoning={"effort": "low"})),
          "mimo": ("xiaomi/mimo-v2.6-flash", pin("Xiaomi", max_tokens=12000, reasoning={"effort": "low"}))}


def ask(name, msg, attempt, ctx):
    model, p = MODELS[name]
    rec = send_cached_request(CACHE, request_messages(model, [{"role": "user", "content": msg}], p, attempt=attempt), context=ctx)
    t = (rec["response"]["choices"][0]["message"].get("content") or "").strip()
    return json.loads(re.search(r"\{.*\}", t, re.S).group(0)), rec["response"]["usage"]["cost"]


def main():
    exp = [json.loads(l) for l in (ROOT / "data/11_export/v3/large/rows.jsonl").open()]
    exp = [r for r in exp if r.get("route") in ("la", "grc") and r.get("answer_direct")]
    ids = [r["seed_id"] for r in sorted(exp, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())[:20]]
    by = {json.loads(l)["seed_id"]: json.loads(l) for l in (ROOT / "data/08_retry/v3/large/rows.jsonl").open()}
    rows = [by[i] for i in ids]

    def fields(r, english):
        conv = "\n\n".join(f"[{m['role']}] {m['content']}" for m in r["messages"])
        return dict(language=LANG[r["route"]][0], conversation=conv, notes=r["reasoning"], draft=r["reply_src"], english=english)

    def check(r, english, attempts):
        errs, cost = [], 0.0
        for name, a in attempts:
            e, c = ask(name, CHECK.format(**fields(r, english)), a, {"step": "fidelity_repair_check", "checker": name, "id": r["seed_id"]})
            errs += [{**x, "checker": name} for x in e["errors"]]
            cost += c
        return errs, cost

    def one(k_r):
        k, r = k_r
        errs, c1 = check(r, r["answer"], [("luna", 0), ("mimo", 0)])
        fixed, edits, c2, missing = r["answer"], [], 0.0, []
        if errs:
            listed = "\n".join(f"- [{e['kind']}] \"{e['quote']}\": {e['why']}" for e in errs)
            out, c2 = ask("luna", REPAIR.format(**fields(r, r["answer"]), errors=listed), 0, {"step": "fidelity_repair_fix", "id": r["seed_id"]})
            edits = out["edits"]
            for e in edits:
                if e["old"] in fixed:
                    fixed = fixed.replace(e["old"], e["new"], 1)
                else:
                    missing.append(e["old"][:80])
        after, c3 = check(r, fixed, [("luna", 2), ("mimo", 2)]) if edits else ([], 0.0)
        return {"row": k, "seed_id": r["seed_id"], "errors": errs, "edits": edits, "missing": missing, "after": after,
                "english": r["answer"], "fixed": fixed, "cost": c1 + c2 + c3}

    with ThreadPoolExecutor(10) as ex:
        res = list(ex.map(one, enumerate(rows, 1)))
    with (OUT / "repair.jsonl").open("w") as f:
        for x in res:
            f.write(json.dumps(x) + "\n")
    pk = ["# Route fidelity packet, repaired: same 20 rows, conversation, notes, reply B after check-and-fix\n"]
    for x, r in zip(res, rows):
        conv = "\n\n".join(f"[{m['role']}] {m['content']}" for m in r["messages"])
        pk.append(f"## Row {x['row']} `{r['seed_id']}`\n\n### Conversation\n\n{conv}\n\n### Notes the reply follows\n\n{r['reasoning']}\n\n"
                  f"### Reply B (through {r['route']} and back, then checked and fixed)\n\n{x['fixed']}\n")
    (ROOT / "slop/reviews/20261028_route_fidelity/packet_repaired.md").write_text("\n".join(pk))
    print("cost", round(sum(x["cost"] for x in res), 4), "rows flagged", sum(bool(x["errors"]) for x in res),
          "rows edited", sum(bool(x["edits"]) for x in res), "edits", sum(len(x["edits"]) for x in res),
          "edits not found", sum(len(x["missing"]) for x in res), "rows still flagged after", sum(bool(x["after"]) for x in res if x["edits"]))


if __name__ == "__main__":
    main()
