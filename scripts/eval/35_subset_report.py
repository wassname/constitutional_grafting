# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "tabulate", "loguru"]
# ///
"""Render run-nine cached scores and a navigable fixed panel; no model calls. -- PI/Sol"""
import hashlib
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/eval/run9"
RUN8 = ROOT / "slop/eval/run8"
TC = Path.home() / ".local/share/tiny-character-2d69739"
sys.path.insert(0, str(TC / "scripts"))
report = importlib.import_module("04_report")


def rows(path):
    return list(map(json.loads, path.read_text().splitlines()))


def label(model):
    if model == "r8_a0_b0":
        return "Untouched Instruct"
    parts = re.findall(r"(echo|stoic|opus|greek|joint)([\d.]+)", model)
    if len(parts) == 4:
        return "All four"
    if len(parts) == 3:
        missing, = {"echo", "stoic", "opus", "greek"} - {name for name, _ in parts}
        return f"Without {missing.title()}"
    return " + ".join(f"{name.title()} ×{dose}" for name, dose in parts)


def main():
    manifest = json.loads((RUN8 / "manifest.json").read_text())
    for name, expected in manifest["protocol_sha256"].items():
        assert hashlib.sha256((TC / name).read_bytes()).hexdigest() == expected, name
    box = OUT / "box_runs"
    for name, expected in manifest["input_sha256"].items():
        assert hashlib.sha256((box / name).read_bytes()).hexdigest() == expected, name
    config = next(json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", (box / "run.md").read_text(), re.S)
                  if "cells" in json.loads(s))
    baseline = "r8_a0_b0"
    models = [baseline] + config["cells"]
    items = {r["id"]: r for r in rows(box / "items.jsonl")}
    expected_meta = json.loads((RUN8 / "judging/baseline/meta.json").read_text())
    judged, hashes = {}, {}
    for path in sorted((OUT / "judging").glob("*/judged.jsonl")):
        meta = json.loads((path.parent / "meta.json").read_text())
        for key in ("rubric", "checks_sha256", "turn_rubric_sha256", "change", "judge", "turn_judge", "draw", "refs", "anchors", "anchors_sha256", "examples", "examples_sha256", "samples", "items_sha256"):
            assert meta[key] == expected_meta[key], (path, key)
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        for r in rows(path):
            key = r["item_id"], r["model"], r["sample"]
            assert key not in judged or judged[key] == r, key
            judged[key] = r
    measured = []
    base_maths = rows(RUN8 / "box_runs/gsm8k_r8_a0_b0.jsonl")
    frozen = rows(box / "gsm8k_long60.jsonl")
    for model in models:
        rs = [r for r in judged.values() if r["model"] == model]
        rec = {"model": model, "label": label(model), "complete": model == baseline or (box / f"{model}.done").exists(), "judged": bool(rs)}
        if rs:
            assert {(r["item_id"], r["sample"]) for r in rs} == {(i, s) for i in items for s in (0, 1)}, model
            if model != baseline:
                per_item = report.per_item([dict(r, s={"on_target": r["on_target"]}) for r in rs if "on_target" in r], "on_target")
                rec["character"] = list(map(float, report.boot(per_item)))
                rec["character_by_item"] = per_item
                rec["broken_gate_samples"] = sum(r.get("broken_gate", False) for r in rs)
            tasks = [r for r in rs if r["family"] == "capability"]
            rec["tasks"] = [sum(report.capability_score(r["check"], items[r["item_id"]]["checks"]["kind"]) for r in tasks), len(tasks)]
        if rec["complete"]:
            path = RUN8 / f"box_runs/gsm8k_{model}.jsonl" if model == baseline else box / f"gsm8k_{model}.jsonl"
            maths = rows(path)
            assert len(maths) == len(base_maths) == len(frozen) == 60, path
            assert all(r["question"] == b["question"] == f["question"] and r["gold"] == b["gold"]
                       for r, b, f in zip(maths, base_maths, frozen)), path
            rec["maths"] = sum(r["correct"] for r in maths)
            rec["maths_delta"] = list(map(float, report.boot({i: int(r["correct"]) - int(b["correct"]) for i, (r, b) in enumerate(zip(maths, base_maths))})))
            rec["maths_caps"] = sum(r["finish"] == "length" for r in maths)
            panel_path = RUN8 / f"box_runs/panel_{model}.jsonl" if model == baseline else box / f"panel_{model}.jsonl"
            panel = rows(panel_path)
            rec["panel_caps"] = sum(t["finish_reason"] == "length" for r in panel for t in r["turns"])
            hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
            hashes[str(panel_path.relative_to(ROOT))] = hashlib.sha256(panel_path.read_bytes()).hexdigest()
        measured.append(rec)
    scope = ("Character: pinned both-order Jev change vs untouched Instruct, 59 items × 2 generations; 90% item-bootstrap intervals. "
             "Maths: final-answer exact match on the same 60 long GSM8K questions, one temperature-zero generation. "
             "Tasks: 11 checks × 2 generations, including format and length. Intervals exclude judge error, training-seed and serving-repeat variation. "
             "All run-nine models use document training on Base followed by a graft onto untouched Instruct. No maths healing or extra character SFT.")
    complete = sum(r["complete"] for r in measured[1:])
    scored = sum(r["judged"] for r in measured[1:])
    pause_path = OUT / "pause.json"
    pause = json.loads(pause_path.read_text()) if pause_path.exists() else None
    status = (f"Paid work paused at the user's request: fix cutoff handling and check the judge before more spending. "
              f"Requested exact-dose/healing grid: {pause['required_grid']['completed_required_conditions']}/"
              f"{pause['required_grid']['conditions_including_preferred_combined_heal']} conditions complete. "
              "The other requested doses and all heals are not run; norm-matched cells below are extra diagnostics.\n\n") if pause else ""
    summary = [status, f"Original diagnostic grid: {complete}/{len(models)-1} generation cells downloaded; {scored} graded. This page is an interim snapshot.\n\n{scope}\n\n"]
    first = {f"r9_{name}1" for name in ("echo", "stoic", "opus", "greek", "joint")}
    for title, selected in [("First dose (k=1)", [r for r in measured if r["model"] in first or r["model"] == baseline]),
                            ("Other doses", [r for r in measured if r["model"] not in first and r["model"] != baseline and r["model"].count("_") == 1]),
                            ("Mixtures (each included update at k=1)", [r for r in measured if r["model"].startswith("r9_") and r["model"].count("_") > 1])]:
        table = []
        selected.sort(key=lambda r: -(r["character"][0] if "character" in r else -3))
        for r in selected:
            model = r["model"]
            key = f"[{r['label']}](#panel_escaped_starwisp-{re.sub(r'[^a-z0-9-]', '-', model.lower())})"
            if model == baseline:
                key = f"*{key}*"
            if "character" in r:
                mean, lo, hi = r["character"]
                score = f"{mean:+.2f} [{lo:+.2f}, {hi:+.2f}]"
            else:
                score = "reference" if model == baseline else "grading pending" if r["complete"] else "not run (paused)" if pause and model in pause["not_run_after_pause"] else "not downloaded"
            table.append([key, score, f"{r['maths']}/60" if r["complete"] else "—",
                          f"{r['tasks'][0]:g}/{r['tasks'][1]}" if "tasks" in r else "—",
                          f"{r['panel_caps']}/7" if r["complete"] else "—"])
        summary.append(f"### {title}\n\n" + tabulate(table, headers=["Documents / dose", "Character↑", "Maths↑", "Tasks↑", "Panel cap hits↓"], tablefmt="pipe", disable_numparse=True, colalign=("left", "right", "right", "right", "right")) + "\n\n")
    summary.append("kE (the middle dose per subset) matches the old graft's weight-update norm, not capability. The largest dose is 2×kE, not k=2. "
                   "Mixture removals measure contributions of trained updates, not retraining without documents. Pure Stoic differs in source and format; Opus/Greek training selections are not perfectly paired.\n\n"
                   "For maths changes, [read every changed Stoic pair](stoic_maths_changed.md). Full excerpts below retain generation-limit failures.")
    (OUT / "estimates.json").write_text(json.dumps({"author": "PI/Sol", "scope": scope, "models": measured, "source_sha256": hashes}, indent=2) + "\n")
    (OUT / "estimates.md").write_text("# Subset-graft results\n\nPI/Sol.\n\n" + "".join(summary) + "\n")
    paths = [RUN8 / f"box_runs/panel_{baseline}.jsonl"] + [box / f"panel_{r['model']}.jsonl" for r in measured[1:] if r["complete"]]
    labels = [f"{r['label']}:{r['model']}" for r in measured] + ["Extra character SFT:not_run_sft", "Healed:not_run_heal", "Graft 4×:not_run_4x"]
    subprocess.run([sys.executable, ROOT / "scripts/eval/17_demo_panel.py", "--json-replies", *paths, "--panel-models", *labels,
                    "--stage-order", "Document LoRA on Base → additive graft onto untouched Instruct; no extra character SFT or healing.",
                    "--compact", "--summary", "".join(summary), "--json-out", OUT / "demo_panel.md"], check=True)
    print(OUT / "estimates.md")


if __name__ == "__main__":
    main()
