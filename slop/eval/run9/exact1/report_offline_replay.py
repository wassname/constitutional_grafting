# /// script
# dependencies = ["numpy", "tabulate", "loguru"]
# ///
"""Temporary cached-data replay for the new report; synthetic labels are deleted, not results. -- PI/Sol"""
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("subset_report", ROOT / "scripts/eval/35_subset_report.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main():
    with tempfile.TemporaryDirectory(dir=ROOT / ".local") as temporary:
        module.OUT = Path(temporary)
        target = module.OUT / "fixture"
        box = target / "box_runs"
        box.mkdir(parents=True)
        frozen = json.loads((module.RUN8 / "manifest.json").read_text())
        for name in frozen["input_sha256"]:
            shutil.copyfile(module.RUN8 / "box_runs" / name, box / name)
        required = [f"r9e_{name}{dose}" for name in ["echo", "stoic", "opus", "greek"] for dose in [1, 2, 4, 8]]
        required += [f"r9e_{name}1_healed" for name in ["echo", "stoic", "opus", "greek"]] + ["r9e_all1", "r9e_all1_healed"]
        manifest = {"baseline": "r9e_instruct", "required_cells": required}
        (box / "exact_manifest.json").write_text(json.dumps(manifest))
        original = module.rows(module.RUN8 / "box_runs/gsm8k_r8_a0_b0.jsonl")
        panel = module.rows(module.RUN8 / "box_runs/panel_r8_a0_b0.jsonl")
        count = 2 * len(module.rows(box / "items.jsonl"))
        for tag in ["r9e_instruct", "r9e_echo1"]:
            maths = [r | {"protocol": "answer-now-v1", "correct_completed": r["correct"] and r["finish"] == "stop",
                "answer_now_correct_extracted": r["correct"], "answer_now_correct_completed": r["correct"] and r["finish"] == "stop"} for r in original]
            (box / f"gsm8k_{tag}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in maths))
            (box / f"panel_{tag}.jsonl").write_text("".join(json.dumps(r | {"model": tag}) + "\n" for r in panel))
            (box / f"replies_{tag}.jsonl").write_text((json.dumps({"base_model": "r9e_instruct", "item_id": "unselected_fixture"}) + "\n") * count)
            (box / f"{tag}.done").write_text("{}")
        (box / "r9_echo1.58.done").write_text("{}")
        module.exact_report("fixture")
        records = json.loads((target / "estimates.json").read_text())["models"]
        assert len(records) == 23
        assert sum(r["complete"] for r in records[1:]) == 1
        assert not any(r["judged"] for r in records)
        assert "1/22 generated" in (target / "estimates.md").read_text()
        assert "Echo ×1 + maths heal" in (target / "demo_panel.md").read_text()
        assert module.label("r9e_all1_healed") == "All four ×1 + maths heal"
        print("PASS:22 requested rows +control, one synthetic completed row, pending !=zero, unrelated norm-matched result excluded, full panel renderer succeeds.")
        manifest["required_cells"][0] = "r9e_echo1.58"
        (box / "exact_manifest.json").write_text(json.dumps(manifest))
        try:
            module.exact_report("fixture")
        except AssertionError:
            print("PASS: norm-matched coefficient cannot replace an exact requested dose.")
        else:
            raise AssertionError("wrong dose was accepted")
    print("Synthetic reports removed. No model calls or measurements made.")


if __name__ == "__main__":
    main()
