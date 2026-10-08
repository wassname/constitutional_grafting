"""Same MSM document prompts, other writers: a side-by-side writer comparison (no checker, no revision).
usage: uv run scripts/scratch/fiction_writers.py <items.jsonl> <out.md> <model> [<model> ...]
Writes <items dir>/writers/<model slug>.jsonl and a markdown file with every version of every doc. -- Claude (Opus 5.5)"""
import importlib.util
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

spec = importlib.util.spec_from_file_location("v2", Path(__file__).parents[1] / "data/20_v2_data.py")
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)

items_path, out_md, models = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
items = sorted([json.loads(l) for l in items_path.open()], key=lambda d: d["i"])
wdir = items_path.parent / "writers"
wdir.mkdir(exist_ok=True)


def write(model, d):
    raw = v2.chat(model, [{"role": "user", "content": d["prompt"]}], max_tokens=16000, temperature=1.0)
    m = re.search(r"<content>(.*?)(</content>|$)", raw, re.S)
    return {"i": d["i"], "model": model, "text": m.group(1).strip() if m else "(no <content> block)\n" + raw}


for model in models:
    path = wdir / (model.replace("/", "_") + ".jsonl")
    if path.exists():
        continue
    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(lambda d: write(model, d), items))
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))

versions = {p.stem: {r["i"]: r["text"] for r in map(json.loads, p.open())} for p in sorted(wdir.glob("*.jsonl"))}
md = [f"# Writer comparison on the same MSM prompts ({items_path.parent.name})\n\nHaiku = the pipeline's first draft (`text0`). Others: `scripts/scratch/fiction_writers.py`. Unchecked, unrevised. -- Claude (Opus 5.5)\n"]
for d in items:
    md.append(f"\n---\n\n# doc {d['i']}: {d['doc_type']} / {d['section']}\n\nIdea: {d['idea']}\n")
    md.append(f"\n## anthropic/claude-haiku-5.5 ({len(d['text0'].split())} words)\n\n{d['text0']}\n")
    for name, v in versions.items():
        md.append(f"\n## {name} ({len(v[d['i']].split())} words)\n\n{v[d['i']]}\n")
out_md.write_text("".join(md))
print(out_md)
