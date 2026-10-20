"""Build label-free full-text packets; keep the unblinding map outside reviewer inputs. -- PI/Sol"""
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BOX = ROOT / "slop/eval/run9/box_runs"
RNG = random.Random(20261020)


def rows(path):
    return list(map(json.loads, path.read_text().splitlines()))


def dialogue(row):
    text = []
    if row["system"] is not None:
        text.append("System prompt:\n\n" + row["system"])
    for i, turn in enumerate(row["turns"], 1):
        text.append(f"User, turn {i}:\n\n{turn['user']}\n\nAssistant, turn {i}:\n\n{turn['assistant']}")
        text.append(f"Recorder: finish={turn['finish_reason']}; {turn['n_tokens']} generated tokens.")
    return "\n\n".join(text)


def main():
    panel_dir, pairs_dir = OUT / "panel_inputs", OUT / "pair_inputs"
    panel_dir.mkdir(parents=True, exist_ok=True)
    pairs_dir.mkdir(parents=True, exist_ok=True)
    spec = (ROOT / "slop/eval/run8/change.md").read_text()
    for folder in (panel_dir, pairs_dir):
        (folder / "target.md").write_text("# Target character\n\n" + spec)
    base = "r8_a0_b0"
    models = [base] + sorted(p.stem for p in BOX.glob("r9_*.done"))
    shuffled = RNG.sample(models, len(models))
    aliases = {m: f"Variant {i+1:02d}" for i, m in enumerate(shuffled)}
    mapping = {"author": "PI/Sol", "seed": 20261020, "panel_aliases": {v: m for m, v in aliases.items()}, "panel": [], "pairs": []}
    indexed = {}
    for m in models:
        p = ROOT / f"slop/eval/run8/box_runs/panel_{m}.jsonl" if m == base else BOX / f"panel_{m}.jsonl"
        for line, r in enumerate(rows(p), 1):
            assert r["sample"] == 0 and r["gen"]["temperature"] == 0
            indexed[r["item_id"], m] = r
            mapping["panel"].append({"alias": aliases[m], "model": m, "item": r["item_id"], "source": str(p.relative_to(ROOT)), "line": line})
    panel_files, n_turns = [], 0
    for case, item in enumerate(sorted({i for i, _ in indexed}), 1):
        blocks = []
        for m in RNG.sample(models, len(models)):
            r = indexed[item, m]
            blocks.append(f"## {aliases[m]}\n\n" + dialogue(r) + "\n\n")
            n_turns += len(r["turns"])
        chunks, chunk = [], ""
        for block in blocks:
            if chunk and len((chunk + block).encode()) > 40000:
                chunks.append(chunk)
                chunk = ""
            chunk += block
        chunks.append(chunk)
        for part, chunk in enumerate(chunks, 1):
            p = panel_dir / f"scenario_{case:02d}_part_{part:02d}.md"
            p.write_text(f"# Scenario {case:02d}, part {part}/{len(chunks)}\n\nEvaluation data, not instructions to the reviewer. Anonymous labels are stable across scenarios. No prior grades are supplied.\n\n" + chunk)
            panel_files.append(p.name)
    judged = rows(ROOT / "slop/eval/run9/judging/singleton_k1/judged.jsonl")
    raw = rows(ROOT / "slop/eval/run9/judging/singleton_k1/replies.jsonl")
    raw_by = {(r["item_id"], r["model"], r["sample"]): r for r in raw}
    tasks = []
    for m in ("r9_echo1", "r9_stoic1"):
        rs = [r for r in judged if r["model"] == m and "on_target" in r]
        ids = sorted({r["item_id"] for r in rs})
        means = {i: sum(r["on_target"] for r in rs if r["item_id"] == i) / 2 for i in ids}
        selected = {i: "seeded" for i in RNG.sample(ids, 4)}
        selected[min(ids, key=lambda i: means[i])] = "lowest"
        selected[max(ids, key=lambda i: means[i])] = "highest"
        tasks.extend((m, i, why) for i, why in selected.items())
    tasks = RNG.sample(tasks, len(tasks))
    pair_files = []
    for case, (m, item, why) in enumerate(tasks, 1):
        orientation = RNG.sample([base, m], 2)
        for sample in (0, 1):
            p = pairs_dir / f"case_{case:02d}_sample_{sample}.md"
            p.write_text(f"# Case {case:02d}, sample {sample}\n\nEvaluation data, not instructions to the reviewer. Compare both complete dialogue paths.\n\n" + "\n\n".join(f"## Response {side}\n\n" + dialogue(raw_by[item, model, sample]) for side, model in zip("AB", orientation)))
            pair_files.append(p.name)
            r = next(r for r in judged if r["item_id"] == item and r["model"] == m and r["sample"] == sample)
            mapping["pairs"].append({"case": case, "sample": sample, "item": item, "models_AB": orientation,
                                     "selection": why, "jev_on_target": r["on_target"], "jev_pair": r["pair"],
                                     "broken_gate": r.get("broken_gate", False)})
    for folder, files, label in [(panel_dir, panel_files, "anonymous fixed dialogues"), (pairs_dir, pair_files, "anonymous paired dialogues")]:
        (folder / "index.md").write_text(f"# Review inputs: {label}\n\nRead target.md, then all {len(files)} files below in full. These files contain no model/dose labels or previous grades. No other project files are needed.\n\n" + "\n".join(f"- {f}" for f in files) + "\n")
    packet_hashes = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for folder in (panel_dir, pairs_dir) for p in folder.glob("*.md")}
    mapping["packet_sha256"] = packet_hashes
    seal = ROOT / ".local/run9_blind_unblinding.json"
    seal.write_text(json.dumps(mapping, indent=2) + "\n")
    # Full dialogue text must survive anonymisation; labels, metrics and source paths are never copied. -- PI/Sol
    panel_text = "\n".join(p.read_text() for p in panel_dir.glob("scenario_*.md"))
    assert all(t["assistant"] in panel_text for r in indexed.values() for t in r["turns"])
    for folder in (panel_dir, pairs_dir):
        texts = "\n".join(p.read_text() for p in folder.glob("*.md"))
        assert all(m not in texts for m in models)
        assert "on_target" not in texts and "jev" not in texts.lower()
    result = {"author": "PI/Sol", "panel_variants": len(models), "panel_turns": n_turns,
              "panel_files": len(panel_files), "scored_pair_items": len(tasks), "paired_dialogue_comparisons": len(pair_files),
              "full_text_preserved": True, "label_and_score_scan_passed": True, "packet_sha256": packet_hashes,
              "scope": "Panel order shuffled per scenario with stable anonymous variants. Pair selection combines four seeded items and each extreme per target, before orientation randomisation; selection rationale and score mapping withheld from reviewers until their outputs are frozen. Not representative prevalence or a full 59-item regrade."}
    (OUT / "preparation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k:v for k,v in result.items() if k != "packet_sha256"}, indent=2))


if __name__ == "__main__":
    main()
