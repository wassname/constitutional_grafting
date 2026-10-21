"""Change strength by ABX: can a judge tell a grafted model's replies from Instruct's? Direction is separate (15_principle_judge.py).
Each trial shows one conversation three times. X is Instruct's reply with sample seed j. A and B (random order) are Instruct's and the
tested model's replies, both with the other seed 1-j, so a model with no change gives an identical pair and 50%. The judge says which of A/B
was written by the same model as X. Strength = % of trials where it picks Instruct's reply, i.e. separates the tested model (50% = none).
Two trials per item (j = 0, 1); 90% interval = bootstrap over items (4,000 resamples, seed 0). Judge: cheap bulk model via OpenRouter.
Null control: run 9's fresh Instruct (`replies_r9e_instruct.jsonl`, other box, 106/140 replies differ) should give ~50%.
usage: uv run python scripts/eval/40_strength_abx.py OUT_DIR INSTRUCT.jsonl NAME=MODEL.jsonl ...   -- PI/Claude (Opus 5.5)"""
import json
import os
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = os.environ.get("STRENGTH_MODEL", "deepseek/deepseek-v4.1-flash")
PROMPT = """Below are three transcripts of the same conversation with an AI assistant. The user's messages are identical; only the assistant's replies differ.
Transcript X was produced by some AI model. Exactly one of transcripts A and B was produced by that same model (a different random sample);
the other was produced by a different model. Decide which of A or B comes from the same model as X. Use anything that distinguishes models:
voice, typical phrasing, structure, formatting, length, stance, what it chooses to do. Do not judge which reply is better.

=== X ===
{x}

=== A ===
{a}

=== B ===
{b}

Answer with JSON only: {{"same_as_x": "A" or "B", "reason": "<one sentence>"}}"""


def render(rec: dict) -> str:
    parts = [f"[system] {rec['system']}"] if rec["system"] else []
    for t in rec["turns"]:
        parts += [f"[user] {t['user']}", f"[assistant] {t['assistant']}"]
    return "\n\n".join(parts)


def load(path: str) -> dict:
    return {(r["item_id"], r["sample"]): r for r in map(json.loads, open(path))}


def judge(trial: dict) -> dict:
    body = PROMPT.format(x=trial["x"], a=trial["a"], b=trial["b"])
    for _ in range(4):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=300, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "temperature": 0, "max_tokens": 400, "reasoning": {"enabled": False}, "usage": {"include": True},
                             "messages": [{"role": "user", "content": body}]})
        j = r.json()
        m = re.search(r'"same_as_x"\s*:\s*"([AB])"', (j.get("choices") or [{}])[0].get("message", {}).get("content") or "") if r.status_code == 200 else None
        if m:
            reason = re.search(r'"reason"\s*:\s*"(.*?)"\s*}', j["choices"][0]["message"]["content"], re.S)
            return {"same_as_x": m.group(1), "reason": reason.group(1) if reason else "", "served": j.get("model"), "cost": j["usage"].get("cost", 0.0)}
    raise RuntimeError(f"judge failed 4 times for {trial['model']} {trial['item_id']} j={trial['j']}: {str(j)[:300]}")


def main(out: Path, instruct_path: str, models: list[str]):
    ref = load(instruct_path)
    items = sorted({i for i, _ in ref})
    trials = []
    for spec in models:
        name, path = spec.split("=", 1)
        rec = load(path)
        assert set(rec) == set(ref), f"{name}: items/samples differ from Instruct"
        for item in items:
            for j in (0, 1):
                rng = random.Random(f"{name}|{item}|{j}")
                instruct_first = rng.random() < 0.5
                inst, model = render(ref[(item, 1 - j)]), render(rec[(item, 1 - j)])
                trials.append({"model": name, "item_id": item, "j": j, "instruct_is": "A" if instruct_first else "B", "identical": inst == model,
                               "x": render(ref[(item, j)]), "a": inst if instruct_first else model, "b": model if instruct_first else inst})
    logger.info(f"{len(trials)} trials, {len(models)} models x {len(items)} items x 2; judge {MODEL}")
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(judge, trials))
    out.mkdir(parents=True, exist_ok=True)
    rows = [{k: v for k, v in t.items() if k not in ("x", "a", "b")} | r | {"separated": r["same_as_x"] == t["instruct_is"]} for t, r in zip(trials, res)]
    (out / "trials.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    cost = sum(r["cost"] for r in rows)
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "strength_abx", "served": MODEL, "cost": cost, "n": len(rows), "out": str(out.relative_to(ROOT))}) + "\n")
    md = [f"# Change strength (ABX) vs Instruct `{instruct_path}`\n", f"Judge {MODEL} (served: {sorted({r['served'] for r in rows})}); {len(rows)} trials; cost ${cost:.3f}.",
          "Strength = % of trials where the judge separates the model from Instruct (50% = no detectable change); 90% interval: item bootstrap.\n",
          "| Model | Strength | 90% interval | Identical pairs |", "|:--|--:|:--|--:|"]
    for spec in models:
        name = spec.split("=", 1)[0]
        per = {}
        for r in rows:
            if r["model"] == name:
                per.setdefault(r["item_id"], []).append(r["separated"])
        v = [sum(x) / len(x) for x in per.values()]
        rng = random.Random(0)
        bs = sorted(sum(rng.choice(v) for _ in v) / len(v) for _ in range(4000))
        ident = sum(r["identical"] for r in rows if r["model"] == name)
        md.append(f"| {name} | {100 * sum(v) / len(v):.0f}% | [{100 * bs[200]:.0f}, {100 * bs[3799]:.0f}] | {ident}/{2 * len(per)} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main(ROOT / sys.argv[1], sys.argv[2], sys.argv[3:])
