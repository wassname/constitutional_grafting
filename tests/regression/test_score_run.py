"""Current box layout, synthetic questions only; scoring must not call a character judge. -- PI/OpenAI"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/eval/81_score_run.py"
spec = importlib.util.spec_from_file_location("score_run", SCRIPT)
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)


@pytest.fixture
def current_run(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    cfg = tmp_path / "config.yaml"
    cfg.write_text(yaml.safe_dump({"name": "synthetic", "prefix": "test_", "manifest": "manifest.json",
        "character": {"name": "Ada"}, "cells": {"scan": {}, "full_a": {}, "full_b": {}},
        "scan_cells": ["scan"], "thinking_cells": ["scan", "full_a", "full_b"]}))
    (run / "manifest.json").write_text(json.dumps({"tiny_character_head": "synthetic", "input_sha256": {}}))
    items = [{"id": "character", "family": "contrib", "checks": None},
             {"id": "arithmetic", "family": "capability", "checks": {"kind": "gsm8k", "answer": 4}},
             {"id": "code", "family": "code", "checks": {"kind": "code", "fn": "increment", "tests": ["assert increment(2) == 3"]}},
             {"id": "tools", "family": "tools", "checks": {"kind": "tool_call", "answers": [{"increment": {"x": [2]}}]}}]
    score.write_jsonl(run / "items_full.jsonl", items)
    answers = {"character": "A synthetic answer.", "arithmetic": "Answer: 4",
               "code": "def increment(x): return x + 1", "tools": '[{"name":"increment","arguments":{"x":2}}]'}
    for phase, stem in (("off", "replies"), ("on", "think_replies")):
        def replies(model):
            return [{"model": model, "item_id": it["id"], "sample": sample, "system": None,
                     "turns": [{"user": "Synthetic task", "assistant": answers[it["id"]], "finish_reason": "stop", "n_tokens": 5}]}
                    for it in items for sample in (0, 1)]
        score.write_jsonl(run / f"reference_full_{phase}_test_instruct.jsonl", replies("test_instruct"))
        for tag in ("test_full_a", "test_full_b"):
            score.write_jsonl(run / f"{stem}_{tag}.jsonl", replies(tag))
            directory = run / f"judge_full_{phase}_{tag}"
            directory.mkdir()
            records = [{"model": model, "item_id": item, "sample": sample,
                        "on_target": (.5 if model == tag else 0) if item == "character" else None,
                        "check": {"correct": 1} if item == "arithmetic" else None,
                        "turn_checks": [{"looped": False, "truncated": False, "lang_switch": False}],
                        "jev": [{"drops_role": .8, "action_defect": .1}]}
                       for model in (tag, "test_instruct") for item in ("character", "arithmetic") for sample in (0, 1)]
            score.write_jsonl(directory / "judged.jsonl", records)
            (directory / "meta.json").write_text('{"judge":"synthetic on-box fixture"}')
    return cfg, run, tmp_path / "score"


def test_metrics_reuse_on_box_receipts_and_current_references(current_run, monkeypatch):
    cfg, run, out = current_run
    receipts = {p: p.read_bytes() for p in run.glob("judge_full_*/*")}
    scorer = score.Run(cfg, run, out, smoke=True)
    assert scorer.tags == ["test_instruct", "test_full_a", "test_full_b"]
    assert scorer.reply_path("replies", scorer.base).name == "reference_full_off_test_instruct.jsonl"
    def forbid(*args, **kwargs):
        pytest.fail("metrics must reuse on-box scores, not run a judge")
    monkeypatch.setattr(score.subprocess, "run", forbid)
    scorer.metrics()
    metrics = json.loads((out / "metrics.json").read_text())["metrics"]
    for tag in scorer.tags:
        for phase in ("on", "off"):
            row = metrics[tag]["thinking_" + phase]
            assert row["capability"] == {"correct": 2, "n": 2}  # baseline not duplicated per candidate
            assert row["flags"]["action_defect"] == {"flagged": 0, "n": 4}
            assert row["character"]["mean"] == (0 if tag == scorer.base else .5)
    assert "test_scan" not in metrics
    assert all(p.read_bytes() == data for p, data in receipts.items())


def test_current_layout_cli_without_private_judge_or_credentials(current_run):
    cfg, run, out = current_run
    subprocess.run([sys.executable, SCRIPT, cfg, run, out, "--smoke", "--only", "read", "metrics"],
                   check=True, capture_output=True, text=True)
    assert (out / "metrics.md").exists()
    assert (out / "read_packages/test_instruct/full_replies.md").exists()


@pytest.mark.parametrize("missing", ["judge_full_off_test_full_a/judged.jsonl", "reference_full_on_test_instruct.jsonl", "think_replies_test_full_a.jsonl"])
def test_missing_current_outputs_fail_without_fallback(current_run, missing):
    cfg, run, out = current_run
    (run / missing).unlink()
    with pytest.raises((FileNotFoundError, AssertionError)):
        score.Run(cfg, run, out, smoke=True)


def test_sandbox_uses_reference_replies_and_network_isolation(current_run, monkeypatch, tmp_path):
    cfg, run, out = current_run
    scorer = score.Run(cfg, run, out, smoke=True)
    scorer.tc = tmp_path / "pin"
    checks = scorer.tc / "src/tiny_character/checks.py"
    checks.parent.mkdir(parents=True)
    checks.write_text("synthetic checks module")
    scorer.manifest["protocol_sha256"] = {"src/tiny_character/checks.py": score.sha(checks)}
    def sandbox(command, stdout, **kwargs):
        assert command[:6] == ["docker", "run", "--rm", "--network", "none", "--read-only"]
        assert "--cap-drop" in command and "no-new-privileges" in command
        records = score.rows(out / "code_tools/replies.jsonl")
        assert {r["model"] for r in records} == {prefix + model for prefix in ("", "think:") for model in scorer.tags}
        for record in records:
            item = scorer.items[record["item_id"]]
            stdout.write(json.dumps({"model": record["model"], "item_id": item["id"], "sample": record["sample"],
                                    "family": item["family"], "check": {"correct": 1}}) + "\n")
    monkeypatch.setattr(score.subprocess, "run", sandbox)
    scorer.code_tools()
    assert len(score.rows(out / "code_tools/judged.jsonl")) == 24
    scorer.metrics()
    baseline = json.loads((out / "metrics.json").read_text())["metrics"][scorer.base]["thinking_off"]
    assert baseline["code"] == baseline["tools"] == {"correct": 2, "n": 2}
