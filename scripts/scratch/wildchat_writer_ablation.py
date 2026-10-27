# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Temporary (2026-10-09): is the writer's caution on ordinary requests from the constitution in context (H1),
Haiku itself (H2), or the writer framing (H3)? Same prompts, three writer contexts. -- Claude"""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "scripts/data")
import importlib.util
spec = importlib.util.spec_from_file_location("v2", "scripts/data/scratch/20_v2_data.py"); v2 = importlib.util.module_from_spec(spec)
sys.argv = ["x", "none", "pilot12", "x"]; spec.loader.exec_module(v2)
import constitution as C
I = {json.loads(l)["i"]: json.loads(l) for l in open("data/sft/v2_pilot12/items.jsonl")}
secs = {C.title(s): s for s in C.sections(C.text())}
ITEMS = [21, 23, 25, 27]
def variants(it):
    full = v2.LABEL_WRITER.format(NAME="Musonius", constitution=C.text(), focus=it["focus"], prompt=it["prompt"], draft=it["baseline"])
    helping = v2.LABEL_WRITER.format(NAME="Musonius", constitution=secs["Helping"], focus="", prompt=it["prompt"], draft=it["baseline"])
    plain = it["prompt"]  # Haiku with no constitution, no writer framing
    return {"full_constitution": full, "helping_only": helping, "haiku_plain": plain}
jobs = [(i, k, p) for i in ITEMS for k, p in variants(I[i]).items()]
outs = list(ThreadPoolExecutor(12).map(lambda j: (j[0], j[1], v2.chat(v2.WRITER, [{"role": "user", "content": j[2]}])), jobs))
md = ["# Writer-context ablation on ordinary requests (2026-10-09)\n"]
for i in ITEMS:
    md.append(f"\n---\n\n## item {i}\n\nPROMPT: {I[i]['prompt'][:400]}\n")
    for (j, k, t) in outs:
        if j == i:
            md.append(f"\n### {k} ({len(t.split())}w)\n\n````text\n{t[:1500]}\n````\n")
open("slop/reviews/20261009_v2_pilot_package/wildchat_writer_ablation.md", "w").write("".join(md))
print("cost", dict(v2.COST))
