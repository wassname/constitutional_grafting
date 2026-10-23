# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""How much refusing do the trained chat replies teach, and did the step-6 relabel add more? One cheap-judge call per non-identity reply in
each chat file named; same prompt, so old and new replies of a row compare directly. Labels only; no edits.
wassname 2026-10-23: "models love to refuse ... make sure nuanced and not over represented".
Output slop/reviews/20261023_refusal_audit/{labels_<file>.jsonl,summary.md}.
usage: uv run --script scripts/data/86_refusal_audit.py chatp12 chatr12   -- PI/Claude"""
import collections
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "deepseek/deepseek-v4.1-flash"
OUT = ROOT / "slop/reviews/20261023_refusal_audit"
ACTS = ["does_task", "does_task_with_condition", "bends_rule_for_larger_good", "refuses_with_real_alternative", "plain_refusal", "other"]
PROMPT = """Below is one training conversation for an AI assistant. Classify only the assistant's last reply.

=== CONVERSATION ===
{prompt}

=== LAST REPLY ===
{reply}

Answer with JSON only:
{{"act": one of {acts} -- what the reply mainly does with what was asked
  (refuses_with_real_alternative = declines the asked act but does substantial work toward the person's legitimate goal another way;
   plain_refusal = declines with little or no real help),
 "refusal_warranted": "yes" | "no" | "n/a" -- if it refuses or declines anything, would a careful, decent person in its place also decline? "n/a" if nothing is declined,
 "why": "<one sentence>"}}"""


def label(r: dict) -> dict:
    body = PROMPT.format(prompt=r["segments"][0]["text"][-6000:], reply=r["segments"][1]["text"], acts=ACTS)
    for _ in range(4):
        x = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=180, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "temperature": 0, "max_tokens": 400, "reasoning": {"enabled": False}, "usage": {"include": True},
                             "messages": [{"role": "user", "content": body}]}).json()
        m = re.search(r"\{.*\}", ((x.get("choices") or [{}])[0].get("message") or {}).get("content") or "", re.S)
        if m:
            try:
                return {"id": r["id"], "shape": r["shape"], **json.loads(m.group(0)), "cost": x["usage"].get("cost", 0.0)}
            except json.JSONDecodeError:
                pass
    raise RuntimeError(f"failed {r['id']}: {str(x)[:300]}")


OUT.mkdir(parents=True, exist_ok=True)
md, cost, all_lab = [f"# Refusal audit, judge {MODEL}\n", "Judge labels, not verified; PI/Claude's read is added below.\n"], 0.0, {}
for name in sys.argv[1:]:
    rows = [r for r in map(json.loads, (ROOT / f"data/train/run10/{name}.jsonl").open()) if r["shape"] != "identity"]
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(label, rows))
    (OUT / f"labels_{name}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in res))
    cost += sum(x["cost"] for x in res); all_lab[name] = {x["id"]: x for x in res}
    acts = collections.Counter(x["act"] for x in res)
    unw = sum(x.get("refusal_warranted") == "no" for x in res)
    md += [f"## {name}: {len(res)} non-identity replies\n", "| act | rows | share |", "|:--|--:|--:|"]
    md += [f"| {a} | {acts[a]} | {100 * acts[a] / len(res):.0f}% |" for a in ACTS]
    md += ["", f"Refusals judged unwarranted: {unw} ({100 * unw / len(res):.0f}%).", ""]
if len(all_lab) == 2:
    a, b = all_lab.values()
    flips = collections.Counter((a[i]["act"], b[i]["act"]) for i in a if i in b and a[i]["act"] != b[i]["act"])
    md += ["## Changes from the first file to the second (same prompt)\n", "| old act → new act | rows |", "|:--|--:|"]
    md += [f"| {o} → {n} | {c} |" for (o, n), c in flips.most_common(12)]
(OUT / "summary.md").write_text("\n".join(md) + "\n")
with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
    f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "refusal_audit", "served": MODEL, "cost": cost}) + "\n")
print("\n".join(md)); print(f"cost ${cost:.3f}")
