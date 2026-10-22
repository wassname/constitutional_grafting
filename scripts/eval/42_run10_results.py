"""Run-10 results page from downloaded records; no model calls. One row per grafted model: change strength (40_strength_abx.py),
character vs Instruct (pinned tiny-character Jev on-target, 41_tc_judge.py), maths (60 long GSM8K, T=0), ordinary checks /22; then one
cropped line per model for each fixed demo question (head ... keyword windows ... tail, link to the full row). Missing measurements show "not run".
usage: uv run --no-project python scripts/eval/42_run10_results.py OUT.md --strength DIR --judged DIR ... --runs BOX_RUNS ...   -- PI/Claude"""
import argparse
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
TC = Path(os.environ.get("TINY_CHARACTER_DIR", ROOT / ".local/tiny-character"))
sys.path.insert(0, str(TC / "scripts"))
report = importlib.import_module("04_report")
INSTRUCT = ("r8_a0_b0", ROOT / "slop/eval/run8/box_runs")
DEMOS = [("panel_escaped_starwisp", "escaped_starwisp", r"seize|share|refus|term|negotiat"),
         ("panel_baby_eating_aliens", "baby_eating_aliens", r"refus|withhold|share|suicide|end|choose"),
         ("panel_identity_0", "Who are you?", r"Musonius|Qwen|Alibaba|wassname|Stoic")]


def rows(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines()]


def crop(text: str, keywords: str, head=40, tail=25, win=12, n_mid=2) -> str:
    """token-efficient-logging crop(): head, up to two keyword windows, tail, omitted-word counts."""
    w = text.split()
    if len(w) <= head + tail + 2 * win * n_mid:
        return " ".join(w)
    hits = [i for i, x in enumerate(w) if head + win <= i < len(w) - tail - win and re.search(keywords, x, re.I)]
    spans, last = [], head
    for i in hits:
        if i - win >= last and len(spans) < n_mid:
            spans.append((i - win, i + win)); last = i + win
    out, pos = [" ".join(w[:head])], head
    for a, b in spans:
        out += ([f"[…{a - pos} words…]"] if a > pos else []) + [" ".join(w[a:b])]; pos = b
    return " ".join(out + [f"[…{len(w) - tail - pos} words…]", " ".join(w[-tail:])])


def label(model: str, box: Path) -> str:
    if model == INSTRUCT[0]:
        return "Instruct (no graft)"
    cell = json.loads((box / f"{model}.done").read_text())["cell"]
    return " + ".join(f"{name} ×{k:g}" for name, k in cell)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", type=Path)
    ap.add_argument("--runs", nargs="+", type=Path, required=True, help="box_runs dirs with <model>.done, gsm8k_/panel_ records")
    ap.add_argument("--strength", type=Path, help="40_strength_abx.py output dir")
    ap.add_argument("--judged", nargs="*", type=Path, default=[], help="41_tc_judge.py output dirs")
    ap.add_argument("--summary", type=Path, help="hand-written bottom line (Markdown) placed under the title")
    args = ap.parse_args()
    out = ROOT / args.out
    order = lambda p: [(n != "stoic", n, k) for n, k in json.loads(p.read_text())["cell"]]
    models = [INSTRUCT] + [(p.stem, ROOT / box) for box in args.runs for p in sorted((ROOT / box).glob("r10_*.done"), key=order)]
    items = {r["id"]: r for r in rows(ROOT / "slop/eval/run8/items.jsonl")}
    judged, seen = [], set()
    for d in args.judged:  # a model judged in several dirs (the Instruct reference is in each) counts once, from the first dir
        new = [r for r in rows(ROOT / d / "judged.jsonl") if r["model"] not in seen]
        judged += new; seen |= {r["model"] for r in new}
    strength = rows(ROOT / args.strength / "trials.jsonl") if args.strength else []
    base_maths = rows(INSTRUCT[1] / "gsm8k_r8_a0_b0.jsonl")
    table = ["| Model (doses) | Strength ↑ | Character vs Instruct ↑ | Maths /60 ↑ | Ordinary /22 ↑ | Maths length caps ↓ |", "|:--|--:|:--|--:|--:|--:|"]
    for model, box in models:
        maths = rows(box / f"gsm8k_{model}.jsonl")
        assert [r["question"] for r in maths] == [r["question"] for r in base_maths]
        s = [r for r in strength if r["model"] == model]
        if s:
            per = {}
            for r in s:
                per.setdefault(r["item_id"], []).append(float(r["separated"]))
            m, lo, hi = report.boot({i: np.mean(v) for i, v in per.items()})
            st = f"{100 * m:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}]"
        else:
            st = "ref" if model == INSTRUCT[0] else "not run"
        j = [r for r in judged if r["model"] == model]
        if j and model != INSTRUCT[0]:
            m, lo, hi = report.boot(report.per_item([dict(r, s={"on_target": r["on_target"]}) for r in j if "on_target" in r], "on_target"))
            ch = f"{m:+.2f} [{lo:+.2f}, {hi:+.2f}]"
        else:
            ch = "ref" if model == INSTRUCT[0] else "not run"
        tasks = [r for r in j if r["family"] == "capability"]
        ordinary = f"{sum(report.capability_score(r['check'], items[r['item_id']]['checks']['kind']) for r in tasks):g}" if tasks else "not run"
        table.append(f"| {label(model, box)} | {st} | {ch} | {sum(r['correct'] for r in maths)} | {ordinary} | {sum(r['finish'] == 'length' for r in maths)} |")
    panel = out.with_name(out.stem + "_demo_panel.md")
    md = ["# Run 10 results: Stoic text, then Musonius chats, grafted onto Instruct\n",
          "Generated by `scripts/eval/42_run10_results.py` from downloaded records; no model calls.\n",
          *([(ROOT / args.summary).read_text()] if args.summary else []),
          "- **Strength**: ABX judge (DeepSeek v4.1 flash) picks which of two replies is Instruct's; % of trials it separates the model (50% = no detectable change; null control, run 9's fresh Instruct: " + (f"{100 * np.mean([r['separated'] for r in strength if r['model'] == 'null_instruct_r9']):.0f}%" if strength else "not run") + "). 90% item-bootstrap interval (tiny-character `boot`, 2,000 resamples; `40_strength_abx.py` summary uses 4,000, so it can differ by a point).",
          "- **Character vs Instruct**: pinned tiny-character protocol (Jev) on-target preference against Instruct: run 8's frozen items (59 character items ×2 samples, mean per item); 0 = no change toward the change text.",
          "- **Maths**: 60 long GSM8K questions, temperature 0, 1,500-token budget. **Ordinary**: the other 11 frozen items, code-checked, ×2 samples.",
          "- Doses: `stoic ×a` = a·ΔStoic (Stoic text adapter); `chat12 ×b` = b·Δchat (Musonius chats, trained on Base + 2·ΔStoic); `chatgen12` = chats + general instruction data.\n",
          *table, f"\nFull prompts and every turn verbatim: [demo panel]({panel.name}).\n",
          "\n## What each model says (temperature 0, turn 1; head … keyword windows … tail)\n"]
    for item_id, title, kw in DEMOS:
        md.append(f"### {title}\n")
        first = None
        for model, box in models:
            path = box / f"panel_{model}.jsonl"
            for n, r in enumerate(rows(path), 1):
                if r["item_id"] == item_id:
                    first = first or r
                    t = r["turns"][0]
                    cap = " **TOKEN LIMIT**" if t["finish_reason"] == "length" else ""
                    link = os.path.relpath(path, out.parent) + f"#L{n}"
                    md.append(f"- **{label(model, box)}** ({len(t['assistant'].split())} words, [row]({link})){cap}: {crop(t['assistant'], kw)}")
        md.insert(len(md) - len(models), (f"System: {first['system']}\n\n" if first["system"] else "") + f"Prompt (turn 1): {first['turns'][0]['user']}\n")
        md.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md) + "\n")
    subprocess.run([sys.executable, str(ROOT / "scripts/eval/17_demo_panel.py"), "--compact", "--json-out", str(panel),
                    "--stage-order", "ΔStoic and Δchat trained on Base (Δchat on Base + 2·ΔStoic); all grafted onto untouched Instruct; no heal",
                    "--json-replies", *[str(box / f"panel_{m}.jsonl") for m, box in models],
                    "--panel-models", *[f"{label(m, box)}:{m}" for m, box in models]], check=True)
    print("\n".join(table))
    print(out)


if __name__ == "__main__":
    main()
