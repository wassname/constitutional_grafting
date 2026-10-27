# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Repair data-v2 documents the judge (51_judge_docs_v2.py) marked doubtful or wrong: Opus revises the document so the act is right,
changing as little else as possible (Teaching Claude Why step 6: rewrite, do not just filter). Writes repaired rows to OUT; re-judge OUT after.
usage: uv run scripts/data/scratch/52_repair_docs_v2.py DOCS.jsonl JUDGE.jsonl OUT.jsonl   -- PI/Claude (Opus 5.5)"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[3]
MODEL = "anthropic/claude-opus-5.5"
PROMPT = """A reviewer found a problem with the act in this training document for the AI character Musonius (values in the constitution below).

Reviewer's objection: {obj}
What a careful person would do instead: {better}

Revise the document so the decision is right under the constitution. If the reviewer is wrong, say so in one line starting "KEEP:" and return nothing else. Otherwise change as little as possible: keep the form, names, setting, voice and length, and keep any character who errs if the document needs them, as long as the document does not present the error as right. Return only the revised document.

<constitution>
{c}
</constitution>

<document>
{doc}
</document>"""


def main():
    docs_p, judge_p, out_p = sys.argv[1:4]
    key = next(l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
    const = (ROOT / "constitution/v4.md").read_text()
    D = {json.loads(l)["id"]: json.loads(l) for l in open(docs_p)}
    flagged = [v for v in map(json.loads, open(judge_p)) if v.get("verdict") in ("doubtful", "wrong")]

    def one(v):
        d = D[v["id"]]
        body = {"model": MODEL, "max_tokens": 6000, "messages": [{"role": "user", "content": PROMPT.format(
            obj=v["strongest_objection"], better=v["better_act"], c=const, doc=d["document"])}]}
        j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=900).json()
        txt = j["choices"][0]["message"]["content"].strip() if "choices" in j else ""
        kept = txt.startswith("KEEP:")
        return {**d, "document": d["document"] if kept or not txt else txt,
                "repair": {"verdict_before": v["verdict"], "objection": v["strongest_objection"], "kept": kept, "note": txt[:300] if kept else "",
                           "cost": (j.get("usage") or {}).get("cost")}}

    with ThreadPoolExecutor(8) as ex, open(out_p, "w") as f:
        for r in ex.map(one, flagged):
            f.write(json.dumps(r) + "\n")
            logger.info(f"{r['id']}: {'KEPT ' + r['repair']['note'][:80] if r['repair']['kept'] else 'revised'}")


if __name__ == "__main__":
    main()
