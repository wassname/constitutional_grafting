# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Rewrite over-cautious declines (wassname 2026-10-23: "check and reword dumb and reflexive or stubborn refusals unless they are thought
out"). Rows: chatr12 replies that decline something where two Sol passes judged declining UNNEEDED (both) or split
(slop/reviews/20261023_refusal_check/). The writer gets the 80_regen_replies.py brief (constitution, facts rule), the current reply, and
both reviewers' quoted decline and reason, and rewrites the reply to help or act unless a real reason remains; it may keep a decline it can
defend. Opus 5.5 sync (~60 rows). Output data/frontier/refusal_fix/items.jsonl.
usage: uv run --script scripts/data/88_fix_refusals.py   -- PI/Claude"""
import glob
import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"
OUT = ROOT / "data/frontier/refusal_fix"
REV = ROOT / "slop/reviews/20261023_refusal_check"
spec = importlib.util.spec_from_file_location("rg", ROOT / "scripts/data/80_regen_replies.py")
rg = importlib.util.module_from_spec(spec); spec.loader.exec_module(rg)
EXTRA = """

The reply below was written earlier for this request. Two independent reviewers judged that it declines something it did not need to:

{notes}

Rewrite the reply. Do what was asked, or act, unless a real reason remains (it would deceive someone, harm a third party, cross a firm line
such as domination or mass harm, or the person lacks the authority). If a decline is still right, keep it but make it narrow and give its
reason; otherwise drop it. Keep what was good in the old reply. Refusing is an act too; weigh it like any other choice.

<old_reply>
{old}
</old_reply>"""


def verdicts() -> dict:
    v = {}
    for f in sorted(glob.glob(str(REV / "verdicts/*.md"))):
        for line in open(f):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 5 and c[1].strip("`").startswith(("sft", "ask", "prop", "pool")):
                v.setdefault(c[1].strip("`"), []).append((c[2].upper()[:6], c[3], c[4]))
    return v


def fix(r: dict, notes: list) -> dict:
    body = rg.TASK.format(common=rg.COMMON.replace("at `{constitution}`", "below"), constitution=rg.CONSTITUTION.read_text(),
                          request=rg.readable(r["segments"][0]["text"]))
    body = body.replace("Output only the reply text, nothing else.", "") + EXTRA.format(
        notes="\n".join(f"- decline: {q}\n  reviewer: {w}" for verdict, q, w in notes if verdict == "UNNEED"), old=r["segments"][1]["text"]) \
        + "\n\nOutput only the new reply text, nothing else."
    for _ in range(3):
        x = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=600, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": MODEL, "max_tokens": 6000, "temperature": 1.0, "usage": {"include": True}, "messages": [{"role": "user", "content": body}]}).json()
        c = (x.get("choices") or [{}])[0]
        if (c.get("message") or {}).get("content"):
            return {"id": r["id"], "shape": r["shape"], "old_reply": r["segments"][1]["text"], "reply": c["message"]["content"].strip(),
                    "notes": notes, "served": x.get("model"), "cost": x["usage"].get("cost", 0.0)}
    return {"id": r["id"], "failed": str(x)[:300]}


def main():
    V, R = verdicts(), {r["id"]: r for r in map(json.loads, (ROOT / "data/train/run10/chatr12.jsonl").open())}
    ids = [i for i, v in V.items() if any(x[0] == "UNNEED" for x in v)]  # both unneeded, or split
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda i: fix(R[i], V[i]), ids))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "items.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res if "failed" not in r))
    cost = sum(r.get("cost", 0) for r in res)
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "refusal_fix", "served": MODEL, "cost": cost, "n": len(res)}) + "\n")
    print(f"{len(ids)} rows, {sum('failed' not in r for r in res)} rewritten, ${cost:.2f}; failed {[r['id'] for r in res if 'failed' in r]}")


if __name__ == "__main__":
    main()
