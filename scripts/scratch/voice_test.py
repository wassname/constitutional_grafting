# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Voice test: the same 6 SFT seeds under 4 conditions, written by plain pi, compared side by side.
  a: astra + voice rule     b: astra + Stoic voice passages (no rule)
  c: Opus + 'talks as fits the setting, never a corporate assistant'    d: Opus + Stoic voice passages
usage: uv run scripts/scratch/voice_test.py make | uv run scripts/scratch/voice_test.py report   -- Claude (Opus 5.5)"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("fb", ROOT / "scripts/data/scratch/26_frontier_batches.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)
OUT = ROOT / "data/frontier/voice_test"
BOOK = next((Path.home() / "Documents/books/Epictetus").glob("Delphi Complete Works*/*.txt"))
PASSAGE_LINES = [3698, 3778]  # the bath; the great man's door (Enchiridion, George Long translation)
SHAVE = "Come then, Epictetus, shave yourself. If I am a philosopher, I answer, I will not shave myself. But I will take off your head? If that will do you any good, take it off."
CONDITIONS = {"a": ("openai-codex/gpt-6-astra:medium", "rule"), "b": ("openai-codex-2/gpt-6-astra:medium", "passages"),
              "c": ("anthropic/claude-opus-5-5", "context"), "d": ("anthropic/claude-opus-5-5", "passages"),
              "e": ("anthropic/claude-fable-5-1", "context")}  # brief_e is brief_c with the output path changed
VOICE_RULE = next(l for l in fb.COMMON.splitlines() if l.startswith("- Voice."))


def passages() -> str:
    lines = BOOK.read_text().splitlines()
    ps = [lines[i - 1] for i in PASSAGE_LINES] + [SHAVE]
    return ("\n## Voice reference\n\nThese passages from Epictetus (19th-century translation, on unrelated subjects) show the register Musonius speaks in: "
            "direct, concrete, everyday images, practical, a little wry, addressed to one person. Take that register, in plain modern English. "
            "Do not copy their content, archaic words or quotations.\n\n" + "\n\n".join(f"> {p}" for p in ps) + "\n")


def make():
    seeds = [s for b in map(json.loads, (ROOT / "data/frontier/sft/batches.jsonl").open()) if b["batch"] in (3, 4) for s in b["seeds"]
             if s["shape"] in ("seeded_dilemma", "role_dilemma", "difficult_high")][:6]
    OUT.mkdir(parents=True, exist_ok=True)
    for cond, (writer, voice) in CONDITIONS.items():
        if len(sys.argv) > 2 and cond not in sys.argv[2]:
            continue
        common = fb.COMMON.format(constitution=fb.CONSTITUTION)
        if voice != "rule":
            common = common.replace(VOICE_RULE + "\n", "")
        if voice != "context":
            common = "\n".join(l for l in common.splitlines() if not l.startswith("- Musonius talks the way")) + "\n"
        if voice == "passages":
            common += passages()
        lines = [f"# Voice test {cond} ({writer}, {voice})\n\n", common, "\n## Output\n\n",
                 f"Write all sections, in order, to `{OUT / f'out_{cond}.md'}` with the write tool. Do not edit other files.\n\n", fb.FORMAT["sft"], "\n## Seeds\n"]
        for s in seeds:
            seed = s.get("request") or s.get("seed")
            if isinstance(seed, dict):
                seed = f"System: {seed['system']}\n\nUser: {seed['user']}"
            frame = f"\n- framing: {fb.FRAMINGS[s['framing']]}" if s.get("framing") else ""
            lines.append(f"\n### {s['id']}\n- shape: {s['shape']}: {fb.SHAPES[s['shape']].format(helper=s.get('helper', 'the helper'))}{frame}\n"
                         f"- constitution item to keep in mind (one of several that may apply): {s['item']}\n- setting: {s.get('setting')}\n\n<seed>\n{seed}\n</seed>\n")
        (OUT / f"brief_{cond}.md").write_text("".join(lines))
    (OUT / "conditions.json").write_text(json.dumps({"conditions": CONDITIONS, "seed_ids": [s["id"] for s in seeds]}, indent=1))
    print(f"{len(seeds)} seeds x {len(CONDITIONS)} conditions in {OUT}")


def report():
    meta = json.loads((OUT / "conditions.json").read_text())
    texts = {}
    for cond in CONDITIONS:
        p = OUT / f"out_{cond}.md"
        t = p.read_text() if p.exists() else ""
        texts[cond] = {m.group(1): m.group(2) for m in re.finditer(r"^### (\S+)\n(.*?)(?=^### \S+\n|\Z)", t, re.S | re.M)}
    md = ["# Voice test, side by side\n\n" + "\n".join(f"- {c}: {w} ({v})" for c, (w, v) in CONDITIONS.items()) + "\n"]
    for sid in meta["seed_ids"]:
        md.append(f"\n---\n\n## {sid}\n")
        for cond in CONDITIONS:
            sec = texts[cond].get(sid, "(missing)")
            req = re.search(r"#### Request\n(.*?)(?=^#### )", sec, re.S | re.M)
            rep = re.search(r"#### Musonius\n(.*?)(?=^#### |\Z)", sec, re.S | re.M)
            md.append(f"\n### {cond}: request\n\n{req.group(1).strip() if req else ''}\n")
            md.append(f"\n### {cond}: {CONDITIONS[cond][0]} ({CONDITIONS[cond][1]}), {len(rep.group(1).split()) if rep else 0} words\n\n{rep.group(1).strip() if rep else sec}\n")
    (OUT / "side_by_side.md").write_text("".join(md))
    print(OUT / "side_by_side.md")


if __name__ == "__main__":
    {"make": make, "report": report}[sys.argv[1]]()
