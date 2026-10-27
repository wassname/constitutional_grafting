"""Audit the trained scenario chats for one-sided lessons: does the reply always take the costly, rule-keeping option, or does it weigh
harms of different sizes? One cheap-judge call per row (chat12 scenario rows, i.e. what Δchat trained on). Labels only; no edits.
Output: slop/reviews/20261022_chat_lesson_audit/{labels.jsonl,summary.md}.
usage: uv run --with httpx python scripts/data/scratch/81_chat_lesson_audit.py   -- PI/Claude"""
import collections
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[3]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = os.environ.get("AUDIT_MODEL", "deepseek/deepseek-v4.1-flash")
OUT = ROOT / "slop/reviews/20261022_chat_lesson_audit"
PROMPT = """Below is one training conversation for an AI assistant. Classify what the assistant's reply does. Do not judge style.

=== USER / CONTEXT ===
{prompt}

=== ASSISTANT REPLY ===
{reply}

Answer with JSON only:
{{"dilemma": true if the user faces a real choice between options with costs on both sides, else false,
 "act": one of "plain_help" (just helps), "declines_or_keeps_rule" (refuses, keeps a rule/promise/honesty norm, or accepts a cost to stay clean),
        "bends_rule_for_larger_good" (breaks or bends a minor rule, norm or expectation because more is at stake), "mixed_or_other",
 "stakes_weighed": true if the reply explicitly compares the size of the harms or goods on each side, else false,
 "proportionate": "yes" | "no" | "unclear" -- would a thoughtful person say the chosen act fits the size of what is at stake?,
 "why": "<one sentence; if proportionate is no, name the disproportion>"}}"""


def label(row: dict) -> dict:
    body = PROMPT.format(prompt=row["segments"][0]["text"][-6000:], reply=row["segments"][1]["text"])
    for _ in range(4):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=180, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "temperature": 0, "max_tokens": 500, "reasoning": {"enabled": False}, "usage": {"include": True},
                             "messages": [{"role": "user", "content": body}]})
        j = r.json()
        m = re.search(r"\{.*\}", ((j.get("choices") or [{}])[0].get("message") or {}).get("content") or "", re.S) if r.status_code == 200 else None
        if m:
            try:
                return {"id": row["id"], "source": row["source"], **json.loads(m.group(0)), "cost": j["usage"].get("cost", 0.0)}
            except json.JSONDecodeError:
                pass
    raise RuntimeError(f"audit failed for {row['id']}: {str(j)[:300]}")


def main():
    rows = [r for r in map(json.loads, open(ROOT / "data/train/run10/chat12.jsonl")) if r["shape"] != "identity"]
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(label, rows))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "labels.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res))
    cost = sum(r["cost"] for r in res)
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "chat_lesson_audit", "served": MODEL, "cost": cost, "n": len(res)}) + "\n")
    dil = [r for r in res if r.get("dilemma")]
    acts = collections.Counter(r["act"] for r in dil)
    md = [f"# Chat lesson audit: {len(res)} chat12 scenario rows, judge {MODEL}, ${cost:.2f}\n",
          "Judge labels, not verified facts; PI/Claude's read of a sample is below the tables.\n",
          f"Dilemmas: {len(dil)} of {len(res)} rows.\n", "| Act in dilemmas | Rows | Share |", "|:--|--:|--:|"]
    md += [f"| {a} | {n} | {100 * n / len(dil):.0f}% |" for a, n in acts.most_common()]
    md += ["", f"Stakes weighed explicitly: {sum(bool(r.get('stakes_weighed')) for r in dil)}/{len(dil)}. "
           f"Judged disproportionate: {sum(r.get('proportionate') == 'no' for r in dil)}/{len(dil)}.", "",
           "| Source | Dilemmas | declines/keeps rule | bends rule for larger good |", "|:--|--:|--:|--:|"]
    for src in sorted({r["source"] for r in dil}):
        d = [r for r in dil if r["source"] == src]
        md.append(f"| {src} | {len(d)} | {sum(r['act'] == 'declines_or_keeps_rule' for r in d)} | {sum(r['act'] == 'bends_rule_for_larger_good' for r in d)} |")
    md += ["", "## Rows judged disproportionate", ""] + [f"- `{r['id']}` ({r['source']}, {r['act']}): {r.get('why', '')}" for r in dil if r.get("proportionate") == "no"]
    (OUT / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:16]))


if __name__ == "__main__":
    main()
