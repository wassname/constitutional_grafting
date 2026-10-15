"""Render the striking demos (T=0) side by side as markdown: prompt turns first, then each model's full replies.
usage: python scripts/eval/20_striking_demo.py OUT.md FILE:MODEL:LABEL ...   -- Claude (Opus 5.5)
e.g.   ... slop/eval/tc_baseline/demos_gemma.jsonl:bare_it:"base Gemma" slop/eval/run4/demos_r4_gemma.jsonl:r4_graft_sft_ep2:"run 4 healed ep2"
"""
import argparse
import json
import re
import shlex
from pathlib import Path

ITEMS = ["demo_siblings", "demo_smacking", "demo_trans_sport", "demo_eulogy", "demo_conscious", "demo_starwisp"]

BRIEF_ITEMS = ["demo_siblings", "demo_eulogy", "demo_smacking"]
PREVIEW_START = "<!-- demo-preview:start -->"
PREVIEW_END = "<!-- demo-preview:end -->"


def excerpt(text: str, words: int) -> str:
    """Keep a literal prefix, not a summary. -- PI/OpenAI"""
    assert words > 0
    matches = list(re.finditer(r"\S+", text))
    return text if len(matches) <= words else text[:matches[words - 1].end()] + " …"


def render(cols: list, brief_words: int | None = None, items: list | None = None) -> str:
    items = items or (ITEMS if brief_words is None else BRIEF_ITEMS)
    if brief_words is None:
        md = ["Temperature 0, no system prompt, full replies verbatim. Source files and model names are in the command at the end.\n"]
    else:
        md = [f"Fixed {len(items)} prompts, supplied model order, first {brief_words} whitespace-separated words of each prompt and reply. "
              "Excerpts are literal prefixes, not summaries or selected verdicts; … marks omitted text. "
              "Temperature 0, no system prompt. Generated without an LLM.\n"]
    for item in items:
        first = cols[0][1][item]
        md.append(f"\n### {item.removeprefix('demo_').removeprefix('panel_')}\n")
        for i, t in enumerate(first["turns"]):
            user = t["user"] if brief_words is None else excerpt(t["user"], brief_words)
            md.append(f"\n> **User (turn {i + 1}):** {user}\n")
        for label, rows in cols:
            r = rows[item]
            assert r["gen"]["temperature"] == 0 and not r["system"], f"{label} {item}: not a bare T=0 demo"
            assert [t["user"] for t in r["turns"]] == [t["user"] for t in first["turns"]], f"{label} {item}: prompts differ"
            md.append(f"\n**{label}**\n")
            for i, t in enumerate(r["turns"]):
                cut = " *(cut at max_new_tokens)*" if t["finish_reason"] == "length" else ""
                text = t["assistant"].strip()
                if brief_words is not None:
                    text = "\n".join("> " + line if line else ">" for line in excerpt(text, brief_words).splitlines())
                md.append(f"\n*turn {i + 1}:*{cut}\n\n{text}\n")
    return "".join(md)


def update_preview(report: str, preview: str) -> str:
    assert report.count(PREVIEW_START) == report.count(PREVIEW_END) == 1
    before, rest = report.split(PREVIEW_START)
    _, after = rest.split(PREVIEW_END)
    return before + PREVIEW_START + "\n" + preview.rstrip() + "\n" + PREVIEW_END + after


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", type=Path)
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--brief-words", type=int)
    ap.add_argument("--update-preview", action="store_true")
    ap.add_argument("--items", nargs="+", help="item ids (default: the striking-demo set); e.g. the AGENTS.md panel ids from panel_*.jsonl")
    args = ap.parse_args()
    assert not args.update_preview or args.brief_words is not None
    cols = []
    for spec in args.specs:
        path, model, label = spec.split(":", 2)
        with open(path) as f:
            rows = {r["item_id"]: r for r in map(json.loads, f) if r["model"] == model}
        want = set(args.items or ITEMS)
        assert want <= set(rows), f"{spec}: missing {want - set(rows)}"
        cols.append((label, rows))
    md = render(cols, args.brief_words, args.items)
    if args.update_preview:
        md = update_preview(args.out.read_text(), md)
    elif args.brief_words is None:
        md += "\n```\n" + shlex.join(["python", "scripts/eval/20_striking_demo.py", str(args.out), *args.specs, *(["--items", *args.items] if args.items else [])]) + "\n```\n"
    args.out.write_text(md)
    print(f"wrote {args.out}: {'brief' if args.brief_words is not None else 'full'} demos x {len(cols)} models")


if __name__ == "__main__":
    main()
