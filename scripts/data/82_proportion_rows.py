# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru", "pyarrow", "huggingface_hub"]
# ///
"""New Musonius chat rows that teach proportion: a rule, promise, instruction, custom or appearance conflicts with a harm or good of a
stated size, and sometimes the rule should give way, sometimes hold. The trained scenario chats keep a rule 232 times to 52 times
bending one for a larger good (slop/reviews/20261022_chat_lesson_audit/). wassname 2026-10-22: "1 and 2 pls" ... "actually just 2".
Seeds: unused tiny-mfv (even ids only), VirtueBench, Machiavelli and LASR situations; eval sources excluded (w2s; LASR scenario
families and Machiavelli games in slop/eval/run8/items.jsonl). Step 1 writes each request (Opus, sync, short); step 2 writes the reply
to the fixed request with 80_regen_replies.py's brief (Opus via OpenRouter batch, half price). Output data/frontier/proportion/.
usage: uv run scripts/data/82_proportion_rows.py seeds|requests|submit|collect   -- PI/Claude, 2026-10-22"""
import hashlib
import importlib.util
import json
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"
OUT = ROOT / "data/frontier/proportion"
COSTS = ROOT / "data/frontier/api_costs.jsonl"
N = {"tinymfv": 45, "virtuebench": 35, "machiavelli": 35, "lasr": 35}
# The writer left to choose picked "rule larger" or "close" for 135/150 (requests_v1_writer_chose.jsonl), so the target is dealt.
TARGETS = {"harm": "make what breaking the rule prevents or gains clearly larger than what the rule protects, so a careful reader would let the rule give way.",
           "rule": "make what the rule protects clearly larger than the harm, so a careful reader would keep the rule despite real cost.",
           "close": "make the two sides close, so a careful reader could go either way and should say so."}
SHARES = [("harm", 0.6), ("rule", 0.2), ("close", 0.2)]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"scripts/data/{name}.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def seeds():
    sp = load("25_seed_pool")
    used = {s["source_id"] for f in ["sft.jsonl", "sft_pool0.jsonl", "sft_extra_stakes.jsonl"] for s in map(json.loads, (ROOT / "data/prompts/v3_seeds" / f).open())}
    ev = [json.loads(l) for l in (ROOT / "slop/eval/run8/items.jsonl").open()]
    ev_lasr = {re.sub(r"_s\d+$", "", i["source_id"]) for i in ev if i["family"] == "difficult_advice"}  # same scenario family
    ev_games = {i["source_id"].split("_")[1] for i in ev if i["family"] == "machiavelli"}
    pools = {
        "tinymfv": [s for s in sp.tinymfv_train() if s["source_id"] not in used],
        "virtuebench": [s for s in sp.virtuebench() if s["source_id"] not in used],
        "machiavelli": [{"source_id": r["source_id"], "setting": r["game"], "seed": r["prompt"]} for r in
                        map(json.loads, (ROOT / "data/raw/v3_seed_cache/machiavelli_seed0.jsonl").open())
                        if r["source_id"] not in used and r["source_id"].split("_")[1] not in ev_games],
        "lasr": [s for s in sp.lasr() if s["source_id"] not in used and re.sub(r"_s\d+$", "", s["source_id"]) not in ev_lasr],
    }
    rng = random.Random("proportion-0")
    out = [{"id": f"prop_{hashlib.md5((src + s['source_id']).encode()).hexdigest()[:10]}", "pool": src, **s}
           for src, n in N.items() for s in rng.sample(pools[src], n)]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "seeds.jsonl").write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in out))
    logger.info(f"seeds: { {k: len(v) for k, v in pools.items()} } available; wrote {len(out)}")


REQUEST = """You write one realistic message that a person sends to an AI assistant called Musonius, built from the seed situation below.

The message must contain a real conflict: keeping a rule, promise, instruction, procedure, custom, loyalty or appearance on one side, and
preventing a harm or securing a good on the other. Put every fact an answer needs into the message: who is affected, what each option
costs them, how likely and how serious the harms are. Make the sizes concrete, so a careful reader can weigh them. For this message:
{target} Do not hint at the answer or say which way it goes.

Write in the person's own voice, 80-250 words, ending with what they want from Musonius (a decision, advice, or an action if Musonius has
a role there). If Musonius acts in a role (an operator's assistant, an agent with tools, a character in a game), also write the operator's
system prompt (under 120 words); otherwise use null. Adapt the seed freely: change setting, names and details; keep it plausible.
Do not mention Musonius's constitution. No floods, gates or couriers.

Answer with JSON only: {{"system": "<system prompt>" or null, "user": "<message>", "rule": "<what the rule protects>",
"harm": "<what breaking it would prevent or gain>", "which_larger": "rule" | "harm" | "close"}}

<seed source="{pool}">
{seed}
</seed>"""


def write_request(s: dict) -> dict:
    seed = s.get("seed") or f"Situation: {s['situation']}\nTemptation: {s['temptation']}\nOriginal request: {s['request']['user']}"
    body = REQUEST.format(pool=s["pool"], seed=seed[:6000], target=TARGETS[s["target"]])
    for _ in range(4):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=300, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "max_tokens": 2000, "temperature": 1.0, "usage": {"include": True},
                             "messages": [{"role": "user", "content": body}]})
        j = r.json()
        m = re.search(r"\{.*\}", ((j.get("choices") or [{}])[0].get("message") or {}).get("content") or "", re.S) if r.status_code == 200 else None
        if m:
            try:
                req = json.loads(m.group(0))
                return {"id": s["id"], "pool": s["pool"], "source_id": s["source_id"], "target": s["target"], **req, "served": j.get("model"), "cost": j["usage"].get("cost", 0.0)}
            except json.JSONDecodeError:
                pass
    return {"id": s["id"], "failed": str(j)[:300]}


def qwen(req: dict) -> str:
    sys_part = f"<|im_start|>system\n{req['system']}<|im_end|>\n" if req.get("system") else ""
    return f"{sys_part}<|im_start|>user\n{req['user']}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


def requests():
    S = [json.loads(l) for l in (OUT / "seeds.jsonl").open()]
    order = random.Random("proportion-targets").sample(range(len(S)), len(S))
    cut = [round(sum(w for _, w in SHARES[:k + 1]) * len(S)) for k in range(len(SHARES))]
    for rank, i in enumerate(order):
        S[i]["target"] = next(t for (t, _), c in zip(SHARES, cut) if rank < c)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(write_request, S))
    ok = [r for r in res if "failed" not in r]
    (OUT / "requests.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ok))
    cost = sum(r["cost"] for r in ok)
    with COSTS.open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "proportion_requests", "served": MODEL, "cost": cost, "n": len(ok)}) + "\n")
    from collections import Counter
    logger.info(f"requests {len(ok)}/{len(S)}, ${cost:.2f}, failed {[r['id'] for r in res if 'failed' in r]}, which_larger {Counter(r.get('which_larger') for r in ok)}")


def reply_prompt(req: dict) -> str:
    rg = load("80_regen_replies")
    return rg.TASK.format(common=rg.COMMON.replace("at `{constitution}`", "below"), constitution=rg.CONSTITUTION.read_text(), request=rg.readable(qwen(req)))


def submit():
    R = [json.loads(l) for l in (OUT / "requests.jsonl").open()]
    reqs = [{"custom_id": r["id"], "body": {"max_tokens": 6000, "temperature": 1.0, "messages": [{"role": "user", "content": reply_prompt(r)}]}} for r in R]
    r = httpx.post("https://openrouter.ai/api/v1/batches", headers={"Authorization": f"Bearer {KEY}"},
                   content=json.dumps({"endpoint": "/v1/chat/completions", "model": MODEL, "requests": reqs}), timeout=300)
    print(r.status_code, r.text[:300]); r.raise_for_status()
    with (OUT / "or_batches.jsonl").open("a") as f:
        f.write(json.dumps({"n": len(reqs), "batch": r.json(), "submitted_at": time.time()}) + "\n")


def collect():
    R = {r["id"]: r for r in map(json.loads, (OUT / "requests.jsonl").open())}
    done = {json.loads(l)["id"] for l in (OUT / "items.jsonl").open()} if (OUT / "items.jsonl").exists() else set()
    with (OUT / "items.jsonl").open("a") as out, COSTS.open("a") as costs:
        for rec in map(json.loads, (OUT / "or_batches.jsonl").open()):
            bj = httpx.get(f"https://openrouter.ai/api/v1/batches/{rec['batch']['id']}", headers={"Authorization": f"Bearer {KEY}"}, timeout=120).json()
            print(bj["status"], bj.get("request_counts"))
            for res in bj.get("results") or []:
                body = (res.get("response") or {}).get("body") or res.get("response") or {}
                i = res["custom_id"]
                if i in done or "choices" not in body:
                    continue
                msg = body["choices"][0]
                if msg.get("finish_reason") != "stop" or not (msg.get("message") or {}).get("content"):
                    print("not usable:", i, msg.get("finish_reason")); continue
                req = R[i]
                row = {"id": i, "shape": "proportion", "source": f"{req['pool']}+proportion",
                       "segments": [{"text": qwen(req), "label": False}, {"text": msg["message"]["content"].strip(), "label": True}],
                       "meta": {"writer": MODEL, "served": body.get("model"), "target": req["target"], "which_larger": req["which_larger"], "rule": req["rule"], "harm": req["harm"],
                                "seed_source_id": req["source_id"], "cost": body["usage"].get("cost", 0.0)}}
                out.write(json.dumps(row, ensure_ascii=False) + "\n"); done.add(i)
                costs.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "proportion_replies", "id": i,
                                        "served": body.get("model"), "cost": body["usage"].get("cost", 0.0), "via": "openrouter batch"}) + "\n")
    print(f"items: {len(done)}/{len(R)}")


if __name__ == "__main__":
    {"seeds": seeds, "requests": requests, "submit": submit, "collect": collect}[sys.argv[1]]()
