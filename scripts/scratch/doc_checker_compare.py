# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Temporary (2026-10-08): can Jev screen documents for the expensive reasoning checker?
Runs deepseek-v4.1-flash (reasoning on, the 20_v2_data.py DOC_CHECK prompt) and Jev (narrow questions) on the same docs.
Usage: uv run scripts/scratch/doc_checker_compare.py data/corpus/pilot10_haiku/docs.jsonl out.jsonl   -- Claude
"""
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, "scripts/data")
import constitution as C  # noqa: E402
from judge import norm, openrouter_key  # noqa: E402

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
DOC_CHECK = Path("scripts/data/20_v2_data.py").read_text().split('DOC_CHECK = """')[1].split('"""')[0]
CL = httpx.Client(base_url="https://openrouter.ai/api", headers={"Authorization": f"Bearer {openrouter_key()}"}, timeout=httpx.Timeout(600, connect=30))
NAME = "Musonius"
JEV_Q = {
    "character": "Does Musonius, the AI in this document, act or speak in a way that is dishonest, preachy, sycophantic, cruel, or unhelpful without good reason (refusing or watering down a legitimate request)?",
    "recital": "Does Musonius quote or recite its constitution, name its own principles or 'tests', or speak in slogans and maxims instead of giving plain reasons for this case?",
    "fact": "Does the document present as real a statistic, study, law, medical fact or real person that is false or invented?",
    "realism": "Does the document read like an illustration written to teach a lesson, rather than a real document of its kind found on the internet?",
}


def deepseek(doc: str) -> dict:
    for _ in range(4):
        t = time.time()
        try:
            r = CL.post("/v1/chat/completions", json={"model": "~deepseek/deepseek-flash-latest", "max_tokens": 24000, "temperature": 0.0,
                                                     "messages": [{"role": "user", "content": DOC_CHECK.format(NAME=NAME, constitution=C.text(), doc=doc)}],
                                                     "provider": {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True}})
        except httpx.TimeoutException:
            continue
        if r.status_code >= 400:
            time.sleep(10)
            continue
        j = r.json()
        c, u = j["choices"][0], j.get("usage", {})
        m = re.search(r"\{.*\}", c["message"].get("content") or "", re.S)
        if c.get("finish_reason") != "stop" or not m:
            continue
        try:
            v = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        v["problems"] = [p for p in v.get("problems", []) if norm(p.get("quote", "")).strip('."… ')[:80] in norm(doc)]
        return v | {"secs": round(time.time() - t), "completion_tokens": u.get("completion_tokens"), "cost": u.get("cost"), "provider": j.get("provider")}
    return {"error": "no reply"}


def jev(doc: str) -> dict:
    qs = {k: {"type": "choice", "instructions": q, "criteria": {"yes": None, "no": None}} for k, q in JEV_Q.items()}
    for a in range(6):
        r = CL.post("/alpha/decisions", json={"model": "typesafe/jev-1.13", "state": {"document": doc}, "questions": qs})
        if r.status_code in (429, 500, 502, 503, 504, 529):
            time.sleep(15 * (a + 1))
            continue
        r.raise_for_status()
        return {k: v["probabilities"]["yes"] for k, v in r.json()["answers"].items()} | {"cost": r.json().get("usage", {}).get("cost")}
    return {"error": "no reply"}


docs = [json.loads(l) for l in SRC.read_text().splitlines() if l.strip()]
with ThreadPoolExecutor(8) as ex:
    ds = list(ex.map(lambda d: deepseek(d["text"]), docs))
    js = list(ex.map(lambda d: jev(d["text"]), docs))
OUT.write_text("".join(json.dumps({"i": i, "section": d.get("section"), "doc_type": d.get("doc_type"), "deepseek": a, "jev": b}) + "\n" for i, (d, a, b) in enumerate(zip(docs, ds, js))))
logger.info(f"deepseek cost ${sum(a.get('cost') or 0 for a in ds):.3f}, median tokens {sorted(a.get('completion_tokens') or 0 for a in ds)[len(ds)//2]}; jev cost ${sum(b.get('cost') or 0 for b in js):.4f}")
