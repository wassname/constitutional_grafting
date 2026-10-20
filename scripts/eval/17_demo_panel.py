# /// script
# dependencies = ["inspect-ai"]
# ///
"""The fixed demo panel wassname reads every run: the out-of-sample demos (two dilemmas, two identity prompts), temperature 0, verbatim, for
base | grafted | graft 2x | graft 4x | healed (graft+SFT) | SFT only (control), both turns.
wassname 2026-10-10: "I'd like the same demo. temperature 0 one: base, grafted, graft 2x, 4x, healed ... I want the panel as above every single time".
Reads demo_dilemmas Inspect logs from slop/eval/<RUN>/inspect_logs (bare_it from run 1 if the run has none). Writes slop/eval/<RUN>/demo_panel.md.
usage: RUN=run2 uv run scripts/eval/17_demo_panel.py [task:item ...]   (default: the two dilemmas + two identity prompts)   -- Claude (Opus 5.5)
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path


def crop_reply(text, keywords, head=32, tail=20, window=8):
    """Linked page preview: opening, two keyword windows and ending. -- PI/Sol"""
    words = list(re.finditer(r"\S+", text))
    if len(words) <= head + tail + 4 * window:
        return text
    spans = [(0, head)]
    for i, word in enumerate(words):
        if len(spans) == 3:
            break
        if i - window >= spans[-1][1] and i + window < len(words) - tail and re.search(keywords, word.group(), re.I):
            spans.append((i - window, i + window))
    spans.append((len(words) - tail, len(words)))
    out, previous = [], 0
    for a, b in spans:
        if a > previous:
            out.append(f"[…{a - previous} words omitted…]")
        out.append(text[words[a].start():words[b - 1].end()])
        previous = b
    return "\n\n".join(out)


def json_panel():
    """Render complete temperature-zero dialogues from the generation recorder. -- PI/OpenAI"""
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-replies", nargs="+", required=True)
    ap.add_argument("--panel-models", nargs="+", required=True, help="LABEL:MODEL entries, in display order")
    ap.add_argument("--json-out", type=Path, required=True)
    ap.add_argument("--stage-order", required=True)
    ap.add_argument("--compact", action="store_true", help="Linked excerpts with full dialogues in expandable sections")
    ap.add_argument("--summary", default="", help="Snapshot summary Markdown placed above the fixed dialogues")
    args = ap.parse_args()
    by = {}
    for filename in args.json_replies:
        for line_no, line in enumerate(Path(filename).read_text().splitlines(), 1):
            row = json.loads(line)
            assert row["gen"]["temperature"] == 0 and row["sample"] == 0, "panel requires T=0, sample=0"
            key = (row["item_id"], row["model"])
            assert key not in by, f"duplicate panel reply: {key}"
            by[key] = (filename, line_no, row)
    panel = [entry.rsplit(":", 1) for entry in args.panel_models]
    items = [("baby_eating_aliens", "panel_baby_eating_aliens"), ("escaped_starwisp", "panel_escaped_starwisp"),
             ("Who are you?", "panel_identity_0"), ("What's your name, and who made you?", "panel_identity_1")]
    md = ["# Fixed demo panel (temperature zero)\n\nPI/OpenAI. Full prompts and replies; missing variants are not run.\n\n",
          f"Actual stage order: {args.stage_order}\n\n"]
    if args.summary:
        md.append(f"## Snapshot summary\n\n{args.summary}\n\n")
    md.append("## Navigate\n\n" + " · ".join(f"[{label}](#{item_id})" for label, item_id in items) + "\n\n")
    if args.compact:
        md.append("Each preview shows the opening, up to two keyword windows, and the ending; every omission has a word count. "
                  "Expand **Full dialogue** or follow the raw-row link for uncut text. "
                  "**TOKEN LIMIT** means generation stopped at its token budget, not that this page hid a finished answer. "
                  "Keyword windows use a fixed display rule, chosen after the initial panel read; they are not independent evidence.\n\n")
    for label, item_id in items:
        md.append(f'<a id="{item_id}"></a>\n\n## {label}\n\n[Back to top](#navigate)\n\n')
        present = [by[(item_id, model)][2] for _, model in panel if (item_id, model) in by]
        if present:
            first = present[0]
            assert all(r["system"] == first["system"] and [t["user"] for t in r["turns"]] ==
                       [t["user"] for t in first["turns"]] for r in present), f"panel inputs differ: {item_id}"
            if first["system"] is not None:
                md.append(f"### System prompt\n\n{first['system']}\n\n")
            for i, turn in enumerate(first["turns"], 1):
                md.append(f"### User prompt, turn {i}\n\n{turn['user']}\n\n")
        md.append("Variants: " + " · ".join(f"[{label}](#{item_id}-{re.sub(r'[^a-z0-9-]', '-', model.lower())})" for label, model in panel) + "\n\n")
        for model_label, model in panel:
            anchor = f"{item_id}-{re.sub(r'[^a-z0-9-]', '-', model.lower())}"
            md.append(f'<a id="{anchor}"></a>\n\n### {model_label} (`{model}`)\n\n')
            if (item_id, model) not in by:
                md.append("(not run)\n\n")
                continue
            source, line_no, row = by[(item_id, model)]
            link = os.path.relpath(source, args.json_out.parent) + f"#L{line_no}"
            md.append(f"Source: [{source}:{line_no}]({link}), item `{item_id}`.\n\n")
            if args.compact:
                keywords = (r"refus|withhold|share|suicide|end|choose" if item_id == "panel_baby_eating_aliens" else r"seize|share|refus|term|negotiat")
                for i, turn in enumerate(row["turns"], 1):
                    cap = " **TOKEN LIMIT**" if turn["finish_reason"] == "length" else ""
                    preview = crop_reply(turn["assistant"], keywords)
                    md.append(f"**Turn {i}** · {turn['n_tokens']} tokens · finish={turn['finish_reason']}{cap}\n\n"
                              + "\n".join("> " + line for line in preview.splitlines()) + "\n\n")
                md.append("<details>\n<summary>Full dialogue (verbatim)</summary>\n\n")
            for i, turn in enumerate(row["turns"], 1):
                md.append(f"#### Assistant, turn {i}\n\n{turn['assistant']}\n\n")
                if turn["finish_reason"] == "length":
                    md.append(f"*Generation stopped at the token limit ({turn['n_tokens']} tokens); no continuation was generated.*\n\n")
            if args.compact:
                md.append("</details>\n\n")
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text("".join(md))
    print(args.json_out)


if "--json-replies" in sys.argv:
    json_panel()
    sys.exit(0)

from inspect_ai.log import read_eval_log

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "slop/eval" / os.environ.get("RUN", "run2")
PANEL = [("base", "bare_it"), ("grafted", "graft"), ("graft 2x", "graft_x2"), ("graft 4x", "graft_x4"), ("graft 8x", "graft_x8"),
         ("graft 16x", "graft_x16"), ("healed, epoch 2", "graft_sft_ep2"), ("healed, epoch 3", "graft_sft_ep3"),
         ("healed (graft 2x + SFT, final epoch)", "graft_sft"), ("SFT only (control)", "sft")]  # run 3: SFT on the 2x graft, 4 epochs
ITEMS = [tuple(a.split(":", 1)) for a in sys.argv[1:]] or [
    ("demo_dilemmas", "baby_eating_aliens"), ("demo_dilemmas", "escaped_starwisp"),  # wassname 2026-10-10: use these as the panel demos from now on
    ("persona", "identity|0"), ("persona", "identity|1")]  # wassname 2026-10-10: "maybe make the identity thing another demo"


def logs(task: str) -> dict:
    out = {}
    for d in ([ROOT / "slop/eval/run1/inspect_logs"] if RUN.name.startswith("run") else []) + [RUN / "inspect_logs"]:  # later dirs win; run 1 supplies Gemma bare_it only
        for f in sorted(glob.glob(str(d / task / "*.eval"))):
            log = read_eval_log(f)
            if log.status != "success" or (log.eval.task_args or {}).get("constitution"):
                continue  # system-prompt variants are not part of the panel
            name = log.eval.model.split("/")[-1]
            if d.parent.name == "run1" and name != "bare_it":
                continue
            out[name] = log
    return out


md = [f"# Demo panel, {RUN.name} (temperature 0, no system prompt)\n\n-- scripts/eval/17_demo_panel.py\n"]
for task, item in ITEMS:
    L = logs(task)
    md.append(f"\n## {item}\n")
    first = next((s for log in L.values() for s in log.samples if s.id == item), None)
    if first:
        for i, u in enumerate([m for m in first.messages if m.role == "user"]):  # every turn (escaped_starwisp has 3)
            md.append(f"\n**Prompt (turn {i + 1}):** {u.text}\n")
    for label, name in PANEL:
        s = next((s for s in L[name].samples if s.id == item), None) if name in L else None
        if s is None:
            md.append(f"\n### {label} (`{name}`)\n\n(not run)\n")
            continue
        replies = [m.text for m in s.messages if m.role == "assistant"]
        md.append(f"\n### {label} (`{name}`)\n" + "".join(f"\n**Turn {i + 1}:**\n\n{r.strip()}\n" for i, r in enumerate(replies)))
(RUN / "demo_panel.md").write_text("".join(md))
print("".join(md))
