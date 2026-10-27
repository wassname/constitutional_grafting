# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "openai"]
# ///
"""Revert Echo-restyled SFT replies whose meaning changed (wassname 2026-10-17: "remove the bad echo data reverting to pre reword").
Each row of data/frontier/sft_stoic_modern is judged by two act/reason judges (prompt in 53_echo_docs_v2.py): original = musonius_opus,
rewrite = musonius. They disagree a lot (30-row check, slop/reviews/20261017_echo_sft_meaning/): GLM prime caught a boundary turned
into a command that DeepSeek missed, and DeepSeek caught an "I" -> "you" voice change that GLM missed. So a row is reverted to the Opus
reply if EITHER judge says "changed"; reverting only loses the Echo voice. Verdicts are cached per (judge, id) in verdicts.jsonl (resumable).
Writes data/frontier/sft_stoic_modern_checked/items.jsonl (same rows; reverted rows get meta.restyle.reverted).
usage: uv run scripts/data/scratch/63_echo_meaning_revert.py   -- PI/Claude (Opus 5.5)"""
import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "data/frontier/sft_stoic_modern/items.jsonl"
OUT_DIR = ROOT / "data/frontier/sft_stoic_modern_checked"
JUDGES = ["z-ai/glm-5.3-prime", "deepseek/deepseek-v4.1-flash"]
spec = importlib.util.spec_from_file_location("e53", ROOT / "scripts/data/scratch/53_echo_docs_v2.py")
e53 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e53)

OUT_DIR.mkdir(parents=True, exist_ok=True)
cache_path = OUT_DIR / "verdicts.jsonl"
cache = {(v["judge"], v["id"]): v for v in map(json.loads, cache_path.open())} if cache_path.exists() else {}
rows = [json.loads(l) for l in SRC.open()]


def one(job: tuple[str, dict]) -> dict:
    judge, r = job
    a = f"User request:\n{r['request']}\n\nReply:\n{r['musonius_opus']}"
    b = f"User request:\n{r['request']}\n\nReply:\n{r['musonius']}"
    v = {"judge": judge, "id": r["id"], **e53.judge(a, b, model=judge)}
    assert v.get("verdict") in ("kept", "changed"), f"malformed judge reply (rerun resumes): {json.dumps(v)[:300]}"
    return v


todo = [(j, r) for j in JUDGES for r in rows if (j, r["id"]) not in cache]
print(f"{len(rows)} rows, {len(todo)} judge calls to make")
with ThreadPoolExecutor(8) as ex, cache_path.open("a") as f:
    for v in ex.map(one, todo):
        cache[(v["judge"], v["id"])] = v
        f.write(json.dumps(v) + "\n")
        f.flush()

n_rev = 0
with (OUT_DIR / "items.jsonl").open("w") as f:
    for r in rows:
        vs = {j: cache[(j, r["id"])] for j in JUDGES}
        changed = [j for j, v in vs.items() if v["verdict"] != "kept"]
        if changed:
            n_rev += 1
            r = {**r, "musonius": r["musonius_opus"],
                 "meta": {**r["meta"], "restyle": {**r["meta"]["restyle"], "reverted": {"by": changed, "changes": {j: vs[j]["changes"] for j in changed}}}}}
        f.write(json.dumps(r) + "\n")
cost = sum(v.get("cost") or 0 for v in cache.values())
print(f"reverted {n_rev}/{len(rows)} rows to the Opus reply; judge cost so far ${cost:.2f} -> {OUT_DIR / 'items.jsonl'}")
