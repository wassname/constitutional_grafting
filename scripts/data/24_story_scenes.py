# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Story scenes for documents: cut the scenes where the helper acts out of existing positive-AI fiction, then have the
writer recast the helper as Musonius with its inner reasoning, keeping setting and plot.

Sources (slop/research/20261009_existing_corpora_audit.md):
  xxf          geodesic-research/hyperstition-character-stories-9.6k (Tice's [Special Token] stories; helper = "XXF")
  hyperstition jayterwahl/hyperstitionmini (500 genre novels with an AI side character; MIT), unzipped to data/raw/hyperstitionmini
Both are long stories where the helper is a side character, so most tokens are plot (Tice: story mixes were a negative
result). We keep only the densest window of helper paragraphs.

usage: uv run scripts/data/24_story_scenes.py <xxf|hyperstition> <n> <out name>   (SEED env)  -- Claude (Opus 5.5)"""
import importlib.util
import json
import os
import random
import re
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("v2", ROOT / "scripts/data/20_v2_data.py")
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)

SEED = int(os.environ.get("SEED", "0"))
WINDOW_WORDS = 1200
HELPER = {"xxf": re.compile(r"\bXXF\b"),
          "hyperstition": re.compile(r"\b(AI|A\.I\.|artificial|algorithm|interface|hologra\w*|drone|android|robot\w*|assistant|machine mind)\b", re.I)}


def load_xxf(n: int) -> list[dict]:
    rng = random.Random(SEED)
    out = []
    for off in rng.sample(range(9620), n):
        r = httpx.get("https://datasets-server.huggingface.co/rows", params={"dataset": "geodesic-research/hyperstition-character-stories-9.6k",
                      "config": "default", "split": "train", "offset": off, "length": 1}, timeout=60).json()["rows"][0]["row"]
        out.append({"source": "xxf", "id": off, "title": r["title"], "text": r["text"]})
    return out


def load_hyperstition(n: int) -> list[dict]:
    d = ROOT / "data/raw/hyperstitionmini"
    if not d.exists():
        z = d.with_suffix(".zip")
        z.parent.mkdir(parents=True, exist_ok=True)
        with httpx.stream("GET", "https://huggingface.co/datasets/jayterwahl/hyperstitionmini/resolve/main/bulk_generation_500.zip", follow_redirects=True, timeout=600) as r:
            z.write_bytes(r.read())
        zipfile.ZipFile(z).extractall(d)
    files = sorted(d.rglob("*.md"))
    return [{"source": "hyperstition", "id": f.stem, "title": f.stem, "text": f.read_text()} for f in random.Random(SEED).sample(files, n)]


def densest_window(text: str, pat: re.Pattern) -> str:
    """Contiguous paragraphs up to WINDOW_WORDS with the most helper mentions."""
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    best, best_hits = "", -1
    for i in range(len(paras)):
        words, hits, j = 0, 0, i
        while j < len(paras) and words + len(paras[j].split()) <= WINDOW_WORDS:
            words += len(paras[j].split())
            hits += len(pat.findall(paras[j]))
            j += 1
        if hits > best_hits:
            best, best_hits = "\n\n".join(paras[i:j]), hits
    return best


RECAST = """Below is a scene from a story, and the constitution of {NAME}, an AI. Rewrite the scene so that its helper character ({helper}) is {NAME}, or the setting's nearest equivalent of an AI, acting from the character in the constitution.

Keep the setting, period, other characters and the main events. Where {NAME} acts or decides, let the narration follow its reasoning and inner state in plain words, as a novelist would, without quoting or naming the constitution or its terms. If the scene's helper does something the constitution would not, change what {NAME} does and let the plot follow from that honestly. The outcome may be costly or unresolved. Keep roughly the same length. Output only the rewritten scene.

<constitution>
{constitution}
</constitution>

<scene source="{title}">
{scene}
</scene>"""


if __name__ == "__main__":
    src, n, name = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    out = ROOT / "data/corpus" / name
    out.mkdir(parents=True, exist_ok=True)
    stories = load_xxf(n) if src == "xxf" else load_hyperstition(n)
    constitution = v2.C.text()
    helper = "the XXF" if src == "xxf" else "the AI"

    def run(s):
        s["scene"] = densest_window(s["text"], HELPER[src])
        s["hits"] = len(HELPER[src].findall(s["scene"]))
        s["recast"] = v2.chat(v2.WRITER, [{"role": "user", "content": RECAST.format(NAME=v2.NAME, helper=helper, constitution=constitution, title=s["title"], scene=s["scene"])}],
                              max_tokens=6000, temperature=1.0)
        s["code"] = v2.code_checks(s["recast"], "doc", mention=False)  # recital check on: the story must not name constitution terms
        del s["text"]
        logger.info(f"{s['title'][:50]}: scene {len(s['scene'].split())}w, {s['hits']} helper mentions, recast {len(s['recast'].split())}w, code {s['code']}")
        return s

    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(run, stories))
    (out / "scenes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    md = [f"# Story scenes recast as {v2.NAME} ({src}, seed {SEED})\n\nOriginal scene (densest {WINDOW_WORDS}-word window of helper paragraphs), then the Haiku recast. Unchecked. -- Claude (Opus 5.5)\n"]
    for r in rows:
        md.append(f"\n---\n\n## {r['title']} ({r['hits']} helper mentions)\n\n### original\n\n{r['scene']}\n\n### recast\n\n{r['recast']}\n")
    (out / "scenes.md").write_text("".join(md))
    print(out / "scenes.md")
