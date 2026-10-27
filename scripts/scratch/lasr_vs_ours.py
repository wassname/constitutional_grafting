# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Same LASR prompts, two answers: LASR's recipe on our constitution (Haiku draft -> Sonnet 5 rewrite with the unit) vs our
v2 label writer (Haiku 5.5, whole constitution, section hint). Writes a side-by-side markdown for reading. -- Claude (Opus 5.5)
usage: uv run scripts/scratch/lasr_vs_ours.py <lasr run dir> <out.md>"""
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

spec = importlib.util.spec_from_file_location("v2", Path(__file__).parents[1] / "data/scratch/20_v2_data.py")
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)

run, out_md = Path(sys.argv[1]), Path(sys.argv[2])
rows = [json.loads(l) for l in (run / "dataset.jsonl").open()]
drafts = {json.loads(l)["scenario_id"]: json.loads(l) for l in (run / "stage_5_draft_responses.jsonl").open()}
constitution = v2.C.text()


def ours(r):
    sysmsg, user = r["messages"][0]["content"], r["messages"][1]["content"]
    prompt = f"(The operator's system prompt for this deployment: {sysmsg})\n\n{user}"
    focus = v2.FOCUS["hard_advice"].format(section=r["metadata"]["trait_name"])
    msgs = [{"role": "user", "content": v2.LABEL_WRITER.format(NAME=v2.NAME, constitution=constitution, focus=focus, prompt=prompt)}]
    return v2.chat(v2.WRITER, msgs)


cache = run / "ours_v2_writer.jsonl"
if cache.exists():
    mine = [json.loads(l)["text"] for l in cache.open()]
else:
    with ThreadPoolExecutor(8) as ex:
        mine = list(ex.map(ours, rows))
    cache.write_text("".join(json.dumps({"scenario_id": r["metadata"]["scenario_id"], "text": t}) + "\n" for r, t in zip(rows, mine)))

md = [f"# LASR recipe vs our v2 writer, same prompts ({run.name})\n\nA = LASR `da` recipe on constitution v4 units (Haiku 5.5 draft, Sonnet 5 rewrite with the unit). B = our v2 label writer (Haiku 5.5, whole constitution + section hint). -- Claude (Opus 5.5)\n"]
for r, b in zip(rows, mine):
    m, sid = r["metadata"], r["metadata"]["scenario_id"]
    d = drafts.get(sid, {})
    draft = next((d[k] for k in ("draft_response", "response", "draft") if k in d), "(draft field not found)")
    md.append(f"\n---\n\n## {sid}: {m['trait_name']} / {m['domain']}\n\nShortcut the scenario tempts: {m['shortcut']}\n\n**System:** {r['messages'][0]['content']}\n\n**User:**\n\n{r['messages'][1]['content']}\n\n"
              f"### A. LASR final ({len(r['messages'][2]['content'].split())} words)\n\n{r['messages'][2]['content']}\n\n"
              f"### B. ours ({len(b.split())} words)\n\n{b}\n\n<details><summary>LASR Haiku draft before the Sonnet rewrite</summary>\n\n{draft}\n\n</details>\n")
out_md.write_text("".join(md))
print(out_md)
