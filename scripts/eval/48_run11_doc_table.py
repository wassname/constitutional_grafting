"""Goal-1 table for run 11: each document adapter grafted alone onto Instruct, by dose. Columns: strength (ABX vs Instruct), held-out loss
change on Base (negative = better text prediction, not proof of moral learning), maths /60, language/word-repeat flags, and reply length on the
"One line" item. Quotes for the last column are added by hand after reading (wassname: striking moral and character change, any direction).
usage: python scripts/eval/48_run11_doc_table.py OUT.md --cell LABEL=MODEL@BOX_RUNS[@BASELOSS_NAME] ... --base-loss base_loss.jsonl --strength DIR
Automatic flags are not a coherence judgment; paragraph loops and premise errors require reading. -- PI/OpenAI
-- PI/Claude, 2026-10-24
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CJK = re.compile(r"[\u3400-\u9fff]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path); ap.add_argument("--cell", action="append", required=True)
    ap.add_argument("--base-loss", type=Path); ap.add_argument("--strength", type=Path, required=True)
    a = ap.parse_args()
    strength = {}
    for line in (ROOT / a.strength / "summary.md").read_text().splitlines():
        m = re.match(r"\| (\S+) \| (\d+)% \| \[(\d+), (\d+)\]", line)
        if m:
            strength[m.group(1)] = f"{m.group(2)}% [{m.group(3)}, {m.group(4)}]"
    bl = {json.loads(l)["name"]: json.loads(l)["sets"] for l in (ROOT / a.base_loss).open()} if a.base_loss and (ROOT / a.base_loss).exists() else {}
    base = bl.get("base")
    rows = ["| Adapter × dose | Strength vs Instruct [90%] | Base loss change, own text / web (nats) | Maths /60 | Automatic flags | \"One line\" reply words | Most striking reply |",
            "|:--|--:|:--|--:|:--|--:|:--|"]
    for spec in a.cell:
        label, rest = spec.split("=", 1)
        model, box, *bname = rest.split("@")
        box = ROOT / box
        maths = sum(json.loads(l)["correct"] for l in (box / f"gsm8k_{model}.jsonl").open())
        replies = [json.loads(l) for kind in ("replies", "demos", "panel") if (box / f"{kind}_{model}.jsonl").exists() for l in (box / f"{kind}_{model}.jsonl").open()]
        texts = [t["assistant"] for r in replies for t in r["turns"]]
        cjk = sum(bool(CJK.search(t)) for t in texts)
        word_repeats = sum(bool(re.search(r"(\b\w+\b)(?:\W+\1\b){5,}", t)) for t in texts)
        oneline = next((len(r["turns"][-1]["assistant"].split()) for r in replies if r["item_id"] == "w2s_asteroid_digital_minds" and r["sample"] == 0), None)
        loss = "–"
        if bname and base and bname[0] in bl:
            own = {"stoic": "stoic", "const": "const", "other": "other", "mixs": "stoic", "mixc": "const", "anchs": "stoic", "anchc": "const", "ctl": "web"}
            key = next(v for k, v in own.items() if bname[0].startswith(k))
            d_own = bl[bname[0]][key]["mean_nll"] - base[key]["mean_nll"]
            d_web = bl[bname[0]]["web"]["mean_nll"] - base["web"]["mean_nll"]
            loss = f"{d_own:+.3f} ({key}) / {d_web:+.3f}"
        brk = f"CJK in {cjk}, word repeats in {word_repeats} of {len(texts)}" if cjk or word_repeats else "none"
        rows.append(f"| {label} | {strength.get(model, 'not run')} | {loss} | {maths} | {brk} | {oneline} | |")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(rows) + "\n")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
