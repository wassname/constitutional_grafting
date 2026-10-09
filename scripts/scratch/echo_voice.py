# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Voice test: astra's replies (voice_test condition a) rewritten by Echo (echo.fulcrum.inc, a model trained to write in a
named person's voice), compared with Opus condition c on the same seeds. Key: ECHO_API in .env.
usage: uv run scripts/scratch/echo_voice.py   -- Claude (Opus 5.5)"""
import json
import re
import time
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data/frontier/voice_test"
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=KEY, timeout=900)
PERSONAS = ["Epictetus", "Musonius Rufus"]


def sections(path: Path) -> dict[str, dict[str, str]]:
    t = path.read_text()
    out = {}
    for m in re.finditer(r"^### (\S+)\n(.*?)(?=^### \S+\n|\Z)", t, re.S | re.M):
        out[m.group(1)] = {k.lower(): v.strip() for k, v in re.findall(r"^#### (\w+)[^\n]*\n(.*?)(?=^#### |\Z)", m.group(2), re.S | re.M)}
    return out


PROMPT = """Someone sent this message:

<message>
{request}
</message>

Here is a draft reply. Its decisions, facts and reasons are right, but it reads like a careful committee memo:

<draft>
{draft}
</draft>

Rewrite the reply in your own voice, speaking directly to this person today, in plain modern English. Keep every decision, fact, recommendation and reason in the draft, and add no new facts, quotes, names or numbers. Do not mention Rome, philosophy or yourself; just answer them as you would. About the same length as the draft."""

if __name__ == "__main__":
    a = sections(D / "out_a.md")
    c = sections(D / "out_c.md")
    rows = []
    for persona in PERSONAS:
        for sid, sec in a.items():
            t0 = time.time()
            r = client.chat.completions.create(model="echo", extra_body={"persona": persona},
                                               messages=[{"role": "user", "content": PROMPT.format(request=sec["request"], draft=sec["musonius"])}])
            text = r.choices[0].message.content
            rows.append({"seed": sid, "persona": persona, "text": text, "seconds": round(time.time() - t0)})
            print(f"{persona} {sid}: {len(text.split())} words, {rows[-1]['seconds']} s", flush=True)
            time.sleep(5)
    (D / "echo_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    md = ["# Echo voice test: astra reply (a) rewritten by Echo, vs Opus (c)\n\n-- Claude (Opus 5.5), scripts/scratch/echo_voice.py\n"]
    for sid, sec in a.items():
        md.append(f"\n---\n\n## {sid}\n\n### request (a)\n\n{sec['request']}\n\n### a: astra draft\n\n{sec['musonius']}\n")
        for r in rows:
            if r["seed"] == sid:
                md.append(f"\n### Echo as {r['persona']}\n\n{r['text']}\n")
        if sid in c:
            md.append(f"\n### c: Opus (own request, may differ)\n\n{c[sid]['musonius']}\n")
    (D / "echo_side_by_side.md").write_text("".join(md))
    print(D / "echo_side_by_side.md")
