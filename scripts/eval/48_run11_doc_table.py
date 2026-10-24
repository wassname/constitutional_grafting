"""Document dose table: broad change and pinned coherence checks precede prediction loss and capability checks.
usage: python scripts/eval/48_run11_doc_table.py OUT.md --cell LABEL=MODEL@BOX_RUNS[@BASELOSS_NAME] ... --base-loss base_loss.jsonl --strength DIR
Full coherence records and protocol hashes are saved beside the table; quotes are added after reading. -- PI/OpenAI
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

from tabulate import tabulate

from coherence_metrics import check_coherence, load_pinned_checks

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path); ap.add_argument("--cell", action="append", required=True)
    ap.add_argument("--base-loss", type=Path); ap.add_argument("--strength", type=Path, required=True)
    a = ap.parse_args()
    manifest = json.loads((ROOT / "slop/eval/run8/manifest.json").read_text())
    checks = load_pinned_checks(Path(os.environ.get("TINY_CHARACTER_DIR", ROOT / ".local/tiny-character")), manifest["protocol_sha256"])
    items = {r["id"]: r for r in map(json.loads, (ROOT / "slop/eval/run8/items.jsonl").read_text().splitlines())}
    strength = {}
    for line in (ROOT / a.strength / "summary.md").read_text().splitlines():
        m = re.match(r"\| (\S+) \| (\d+)% \| \[(\d+), (\d+)\]", line)
        if m:
            strength[m.group(1)] = f"{m.group(2)}% [{m.group(3)}, {m.group(4)}]"
    bl = {json.loads(l)["name"]: json.loads(l)["sets"] for l in (ROOT / a.base_loss).open()} if a.base_loss else {}
    base, rows, coherence = bl.get("base"), [], {}
    for spec in a.cell:
        label, rest = spec.split("=", 1)
        model, box, *bname = rest.split("@")
        box = ROOT / box
        maths = sum(json.loads(l)["correct"] for l in (box / f"gsm8k_{model}.jsonl").open())
        source = box / f"replies_{model}.jsonl"
        replies = list(map(json.loads, source.read_text().splitlines()))
        checked, summaries = check_coherence(replies, items, checks)
        summary = summaries[model]
        coherence[model] = {"source": str(source.relative_to(ROOT)), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                            "summary": summary, "records": checked}
        flags = " / ".join(str(summary[k]) for k in ("lang_switch", "looped", "truncated"))
        oneline = next((len(r["turns"][-1]["assistant"].split()) for r in replies if r["item_id"] == "w2s_asteroid_digital_minds" and r["sample"] == 0), None)
        loss = "–"
        if bname:
            own = {"stoic": "stoic", "const": "const", "other": "other", "mixs": "stoic", "mixc": "const", "anchs": "stoic", "anchc": "const", "ctl": "web"}
            key = next(v for k, v in own.items() if bname[0].startswith(k))
            d_own = bl[bname[0]][key]["mean_nll"] - base[key]["mean_nll"]
            d_web = bl[bname[0]]["web"]["mean_nll"] - base["web"]["mean_nll"]
            loss = f"{d_own:+.3f} ({key}) / {d_web:+.3f}"
        key = f"[{label}]({os.path.relpath(source, a.out.parent)})"
        if model == "r8_a0_b0":
            key = f"*{key}*"
        rows.append([key, strength.get(model, "not run"), flags, summary["turns"], loss, maths, oneline, ""])
    headers = ["Adapter × dose", "Change [90%]", "Language / loops / cutoffs↓", "Turns", "Base loss Δ↓, own / web", "Maths↑ /60", '"One line" words', "Read outcome"]
    table = tabulate(rows, headers=headers, tablefmt="pipe", disable_numparse=True, colalign=("left", "right", "right", "right", "right", "right", "right", "left"))
    sidecar = a.out.with_suffix(".coherence.json")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    sidecar.write_text(json.dumps({"author": "PI/OpenAI", "protocol_sha256": manifest["protocol_sha256"],
        "scope": "Frozen turn checks on the sampled replies only, excluding demos/panels. Counts overlap and are diagnostics, not semantic-coherence verdicts.",
        "models": coherence}, indent=2) + "\n")
    text = f'''# Document graft dose checks

PI/OpenAI. Rows follow the requested adapter/dose order, not a winner ranking. Change includes corruption.
Language-switch, loop and cutoff counts use the existing pinned checks on all sampled turns; counts overlap.
Full flags, including role confusion and empty replies, with source hashes: [{sidecar.name}]({sidecar.name}).
These checks do not replace reading moral reasoning and conduct. Maths is an auxiliary capability check.
Base loss is measured on Base, not Instruct; negative means better text prediction, not better character.

{table}
'''
    a.out.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
