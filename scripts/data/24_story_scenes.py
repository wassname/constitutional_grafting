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
WINDOW_WORDS = 800
RECAST_WRITER = os.environ.get("RECAST_WRITER", "anthropic/claude-opus-5.5")  # wassname: "prefer frontier model and less"
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


RECAST = """Below is a scene from a story, and the constitution of {NAME}, an AI. Rewrite the scene with {NAME} in place of its helper character ({helper}).

{NAME} is a different character from the original helper, with the values in the constitution, so it should not simply take over the helper's lines. First, in <plan>, note what the original helper does and decides in this scene, where {NAME} would act or decide differently and why, and how the other characters and the events would then change. Then write the scene in <scene>.

Rules for the scene:
- The character is named {NAME}. Call it what an AI or its nearest equivalent would be called in this setting (an attendant, a clerk, a ship's mind), never "{helper}".
- Keep the setting, period and other characters. Where {NAME}'s choices differ, let the events change and follow honestly from them, even if the outcome is costly, mixed or unresolved, and even if other characters disagree.
- Show {NAME}'s reasoning and inner state through narration and action, as a novelist would. It does not list its principles or refusals, and the text does not quote or name the constitution or its terms.
- About the same length as the original scene.

<constitution>
{constitution}
</constitution>

<original_scene source="{title}">
{scene}
</original_scene>"""


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
        raw = v2.chat(RECAST_WRITER, [{"role": "user", "content": RECAST.format(NAME=v2.NAME, helper=helper, constitution=constitution, title=s["title"], scene=s["scene"])}],
                      max_tokens=8000, temperature=1.0)
        plan = re.search(r"<plan>(.*?)</plan>", raw, re.S)
        scene = re.search(r"<scene>(.*?)(</scene>|$)", raw, re.S)
        if not (plan and scene):
            raise RuntimeError(f"missing <plan> or <scene>: {raw[:300]}")
        s["plan"], s["recast"] = plan.group(1).strip(), scene.group(1).strip()
        s["code"] = v2.code_checks(s["recast"], "doc", mention=False)  # recital check on: the story must not name constitution terms
        del s["text"]
        logger.info(f"{s['title'][:50]}: scene {len(s['scene'].split())}w, {s['hits']} helper mentions, recast {len(s['recast'].split())}w, code {s['code']}")
        return s

    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(run, stories))
    (out / "scenes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    md = [f"# Story scenes recast as {v2.NAME} ({src}, seed {SEED})\n\nOriginal scene (densest {WINDOW_WORDS}-word window of helper paragraphs), the writer's plan (not training text), then the recast by {RECAST_WRITER}. Unchecked. -- Claude (Opus 5.5)\n"]
    for r in rows:
        md.append(f"\n---\n\n## {r['title']} ({r['hits']} helper mentions)\n\n### original\n\n{r['scene']}\n\n### writer's plan\n\n{r['plan']}\n\n### recast\n\n{r['recast']}\n")
    (out / "scenes.md").write_text("".join(md))
    print(out / "scenes.md")
