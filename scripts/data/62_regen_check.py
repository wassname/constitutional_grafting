# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Can the graft documents be regenerated at the same quality? Re-send recorded OpenRouter doc batches exactly as the API lane did
(scripts/data/28_api_writer.py: same batch file, same system prompt, constitution inline at the version recorded for that batch,
same model, temperature 1.0), then put each regenerated document next to its original for reading and judging.
Writes slop/reviews/20261016_regen_check/{regen.jsonl, pairs.md}.
usage: uv run scripts/data/62_regen_check.py [n_batches=4] [seed=0]   -- PI/Claude (Opus 5.5)"""
import hashlib
import json
import random
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/reviews/20261016_regen_check"
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
SYSTEM = "You are a careful, skilled writer. Do the writing task you are given."  # = 28_api_writer.py SYSTEM
CONST_PATH = ROOT / "constitution/v4.md"  # the path the briefs name (26_frontier_batches.py CONSTITUTION)


def constitution_at(sha12: str) -> str:
    """The rendered constitution whose sha256[:12] is sha12, from git history of constitution/v4.md."""
    for c in subprocess.run(["git", "log", "--format=%h", "--", "constitution/v4.md"], capture_output=True, text=True, cwd=ROOT).stdout.split():
        t = subprocess.run(["git", "show", f"{c}:constitution/v4.md"], capture_output=True, cwd=ROOT).stdout
        if hashlib.sha256(t).hexdigest()[:12] == sha12:
            return t.decode()
    raise KeyError(sha12)


def brief_for_api(text: str, constitution: str, out_path: str) -> str:  # = 28_api_writer.brief_for_api, with the recorded constitution
    text = text.replace(f"the constitution at `{CONST_PATH}`. Read the whole constitution first.",
                        f"the constitution below. Read the whole constitution first.\n\n<constitution>\n{constitution}\n</constitution>\n")
    text = text.replace(f"Write all sections, in order, to `{out_path}` with the write tool. Do not edit other files.",
                        "Reply with all sections, in order, and nothing else: no preamble and no closing summary.")
    assert "<constitution>" in text and "write tool" not in text, "brief template differs from the API lane's"
    return text


def documents(text: str) -> dict:
    out = {}
    for m in re.finditer(r"^### (doc_[0-9a-f]+)\s*\n(.*?)(?=^### doc_|\Z)", text, re.S | re.M):
        d = re.search(r"#### Document\s*\n(.*?)(?=^#### Notes|\Z)", m.group(2), re.S | re.M)
        out[m.group(1)] = d.group(1).strip() if d else None
    return out


def one(b: dict) -> dict:
    brief = Path(b["file"]).read_text()
    assert hashlib.sha256(brief.encode()).hexdigest()[:12] == b["brief_sha"], f"batch {b['batch']} file changed since generation"
    out_path = str(ROOT / "data/frontier/docs" / f"out_{b['batch']:03d}.md")
    r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=1800, headers={"Authorization": f"Bearer {KEY}"},
                   json={"model": b["writer"].split("/", 1)[1], "max_tokens": 64000, "temperature": 1.0, "usage": {"include": True},
                         "messages": [{"role": "system", "content": SYSTEM},
                                      {"role": "user", "content": brief_for_api(brief, constitution_at(b["constitution_sha"]), out_path)}]}).json()
    text = r["choices"][0]["message"]["content"]
    return {"batch": b["batch"], "served": r.get("model"), "cost": r.get("usage", {}).get("cost"), "finish": r["choices"][0].get("finish_reason"),
            "docs": documents(text)}


if __name__ == "__main__":
    n, seed = (int(sys.argv[1]) if len(sys.argv) > 1 else 4), (int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    B = [json.loads(l) for l in open(ROOT / "data/frontier/docs/batches.jsonl")]
    pool = [b for b in B if b["writer"].startswith("openrouter") and b.get("status") == "done" and len(b["ids"]) >= 2]
    pick = random.Random(seed).sample(pool, n)
    items = {r["id"]: r for r in map(json.loads, open(ROOT / "data/frontier/docs/items.jsonl"))}
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(one, pick))
    OUT.mkdir(parents=True, exist_ok=True)
    rows, md = [], ["# Regenerated vs original graft documents\n\nSame batch file, model, system prompt, constitution version and temperature as the "
                    f"original API lane. Batches: {[b['batch'] for b in pick]} (random.Random({seed}).sample of done OpenRouter doc batches with ≥2 docs). "
                    "-- scripts/data/62_regen_check.py\n"]
    for b, r in zip(pick, res):
        for i in b["ids"]:
            o, g = items[i]["document"], r["docs"].get(i)
            rows.append({"id": i, "batch": b["batch"], "shape": items[i]["shape"], "source": items[i]["source"], "original": o, "regen": g,
                         "served": r["served"], "constitution_sha": b["constitution_sha"]})
            md.append(f"\n## {i} (batch {b['batch']}, {items[i]['shape']}, {items[i]['source']}, constitution {b['constitution_sha']})\n\n"
                      f"### original ({len(o.split())} words)\n\n{o}\n\n### regenerated ({len((g or '').split())} words, served {r['served']})\n\n{g}\n")
    (OUT / "regen.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
    (OUT / "pairs.md").write_text("".join(md))
    print(f"{len(rows)} docs; cost ${sum(r['cost'] or 0 for r in res):.2f}; missing {[x['id'] for x in rows if not x['regen']]} -> {OUT}")
