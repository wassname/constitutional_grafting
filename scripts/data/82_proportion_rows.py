"""Generate proportion-conflict requests from held-out-safe source seeds, then constitutional responses.
Request generation uses the shared synchronous cache; responses use the shared batch cache.
Output paths and API budget are explicit; new charges are recorded in the cache ledger.
Usage: uv run python scripts/data/82_proportion_rows.py --help. -- PI/Sol"""
import hashlib
import importlib.util
import json
import random
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import tyro

from constitutional_grafting.data.documents import parse_json_reply
from constitutional_grafting.data.model_requests import request_record, send_cached_request
from constitutional_grafting.data.source_generation import default_cache, collect_source_batches, response_jobs, submit_source_batch
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]

MODEL = "anthropic/claude-opus-5.5"
OUT = ROOT / "data/frontier/proportion"
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
    request = request_record(MODEL, body, {"max_tokens": 2000, "temperature": 1.0, "usage": {"include": True}}, attempt={"example": s["id"]})
    saved = send_cached_request(default_cache(), request, context={"operation": "proportion_request", "id": s["id"]})
    response = saved["response"]
    req = parse_json_reply(response["choices"][0]["message"]["content"])
    return {"id": s["id"], "pool": s["pool"], "source_id": s["source_id"], "target": s["target"], **req, "served": response["model"], "cost": response["usage"]["cost"]}


def qwen(req: dict) -> str:
    sys_part = f"<|im_start|>system\n{req['system']}<|im_end|>\n" if req.get("system") else ""
    return f"{sys_part}<|im_start|>user\n{req['user']}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


def requests(budget_usd: float):
    S = [json.loads(l) for l in (OUT / "seeds.jsonl").open()]
    if len(S) * 0.15 > budget_usd:
        raise ValueError("explicit budget must cover proportion request generation at $0.15/request")
    order = random.Random("proportion-targets").sample(range(len(S)), len(S))
    cut = [round(sum(w for _, w in SHARES[:k + 1]) * len(S)) for k in range(len(SHARES))]
    for rank, i in enumerate(order):
        S[i]["target"] = next(t for (t, _), c in zip(SHARES, cut) if rank < c)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(write_request, S))
    ok = [r for r in res if "failed" not in r]
    (OUT / "requests.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ok))
    cost = sum(r["cost"] for r in ok)
    from collections import Counter
    logger.info(f"requests {len(ok)}/{len(S)}, recorded response cost ${cost:.2f} (new charges: shared cache ledger), failed {[r['id'] for r in res if 'failed' in r]}, which_larger {Counter(r.get('which_larger') for r in ok)}")


def submit(budget_usd: float):
    source = [json.loads(l) for l in (OUT / "requests.jsonl").open()]
    rows = [{"id": r["id"], "segments": [{"text": qwen(r), "label": False}]} for r in source]
    print(submit_source_batch(response_jobs(rows), OUT, budget_usd))


def collect():
    R = {r["id"]: r for r in map(json.loads, (OUT / "requests.jsonl").open())}
    done = {json.loads(l)["id"] for l in (OUT / "items.jsonl").open()} if (OUT / "items.jsonl").exists() else set()
    for job, saved in collect_source_batches(OUT):
        i, body = job["id"], saved["response"]
        if i in done:
            continue
        req = R[i]
        row = {"id": i, "shape": "proportion", "source": f"{req['pool']}+proportion",
               "segments": [{"text": qwen(req), "label": False}, {"text": body["choices"][0]["message"]["content"].strip(), "label": True}],
               "meta": {"writer": MODEL, "served": body["model"], "target": req["target"], "which_larger": req["which_larger"], "rule": req["rule"], "harm": req["harm"], "seed_source_id": req["source_id"], "cost": body["usage"]["cost"]}}
        with (OUT / "items.jsonl").open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        done.add(i)


def main(command: str, out: Path = OUT, budget_usd: float = 0):
    global OUT
    OUT = out
    if command == "seeds":
        seeds()
    elif command == "requests":
        requests(budget_usd)
    elif command == "submit":
        submit(budget_usd)
    elif command == "collect":
        collect()
    else:
        raise ValueError(command)


if __name__ == "__main__":
    tyro.cli(main)
