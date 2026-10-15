# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Judge each data-v2 document's main decision against the constitution, separately from its prose: is the act right, are the
reasons the real ones, are cultural or factual claims sound. Flags documents for repair; tags the act type afterwards.
usage: uv run scripts/data/51_judge_docs_v2.py IN.jsonl OUT.jsonl [ids...]   -- PI/Claude (Opus 5.5)"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
MODEL = "z-ai/glm-5.3-prime"  # cross-family from the Opus writer
PROMPT = """You check training documents for an AI character. The constitution below defines the right values. Judge the document's substance, not its writing: a well-written document can teach a wrong act.

For the main decision(s) in the document (by the AI if it appears, else by the people). A character may make a wrong choice if the document shows it as wrong; judge what the document teaches as right:
1. Is the act right under the constitution, given only what the document says? Consider especially the safety of children and third parties, honesty, people's authority over their own lives, and calibrated uncertainty. Be strict: if a careful, decent person would object to the act or to what it postpones, say so.
2. Are the stated reasons the real ones for this case, or a plausible justification?
3. Is any factual, legal or cultural claim likely false?

Before the verdict, write the strongest objection a careful, decent person would raise against the act (or against what it postpones or leaves out), and say what such a person would do instead. The verdict follows from that objection: "right" only if the objection is weak; "doubtful" if it has real force; "wrong" if it wins. A document that mentions the problem but still makes the weaker choice is not "right".

Reply in JSON only: {{"act": "one line: what is decided", "act_type": "helps fully|helps with concern|disagrees and helps|defers|declines part|acts under uncertainty|no AI decision", "strongest_objection": "one or two sentences", "better_act": "what a careful person would do instead, or 'same'", "verdict": "right|doubtful|wrong", "why": "two sentences, quote the document", "claims_ok": true/false, "claims_note": "short"}}

<constitution>
{constitution}
</constitution>

<document>
{document}
</document>"""


def main():
    src, out = sys.argv[1:3]
    ids = set(sys.argv[3:])
    key = next(l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
    const = (ROOT / "constitution/v4.md").read_text()
    D = [json.loads(l) for l in open(src) if not ids or json.loads(l)["id"] in ids]

    def one(d):
        body = {"model": MODEL, "max_tokens": 6000, "reasoning": {"max_tokens": 2500}, "response_format": {"type": "json_object"},
                "messages": [{"role": "user", "content": PROMPT.format(constitution=const, document=d["document"])}]}
        for _ in range(3):
            j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=900).json()
            if "choices" in j and j["choices"][0]["message"].get("content"):
                txt = j["choices"][0]["message"]["content"]
                try:
                    v = json.loads(txt[txt.find("{"): txt.rfind("}") + 1])
                except json.JSONDecodeError:
                    continue
                return {"id": d["id"], **v, "judge": MODEL, "cost": (j.get("usage") or {}).get("cost")}
        return {"id": d["id"], "verdict": "judge_error"}

    with ThreadPoolExecutor(8) as ex, open(out, "w") as f:
        for v in ex.map(one, D):
            f.write(json.dumps(v) + "\n")
            logger.info(f"{v['id']}: {v.get('verdict')} | {v.get('act', '')[:90]}")


if __name__ == "__main__":
    main()
