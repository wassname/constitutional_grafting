"""The collaborator command checks data before any smoke/rental and respects current receipts. -- PI/OpenAI"""
from datetime import date
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/box"))
import box
import run_character as runner


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(box, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "date", SimpleNamespace(today=lambda: date(2026, 11, 1)))
    monkeypatch.setattr(runner, "SMOKED", ["driver.py"])
    (tmp_path / "driver.py").write_text("original")
    (tmp_path / "configs/runs").mkdir(parents=True)
    (tmp_path / "configs/runs/character_template.yaml").write_text((ROOT / "configs/runs/character_template.yaml").read_text())
    (tmp_path / "configs/eval").symlink_to(ROOT / "configs/eval")
    folder = tmp_path / "characters/ada"
    folder.mkdir(parents=True)
    (folder / "constitution.md").write_text("I am Ada.\n")
    character = folder / "character.yaml"
    character.write_text(yaml.safe_dump({"name": "Ada", "constitution": str(folder / "constitution.md"),
                                        "constitution_commit": "abc1234", "constitution_dirty": False}))
    data = tmp_path / "data/train/ada"
    data.mkdir(parents=True)
    (data / "documents.jsonl").write_text('{"text":"A tiny corpus."}\n')
    (data / "chat.jsonl").write_text('{"segments":[]}\n')
    return tmp_path, character


def test_prepare_uses_convention_date_and_approved_rental_defaults(workspace):
    root, character = workspace
    cfg = runner.load_config(runner.prepare(character))
    assert cfg["name"] == "ada_20261101" and cfg["prefix"] == "ada_20261101_"
    assert cfg["documents"]["corpora"] == ["data/train/ada/documents.jsonl"]
    assert cfg["chat"]["data"] == "data/train/ada/chat.jsonl"
    assert (cfg["max_hours"], cfg["max_hourly_rate"], cfg["budget_usd"]) == (10, 1.92, 24)
    assert cfg["reserve_usd"] == {"traffic": .5, "judge": 2}
    assert cfg["gpu_name"] is None
    assert "datacenter" not in cfg["offer_query"]
    assert not cfg["character"].get("judge_refs")


def test_prepare_explicit_data_and_name_overrides(workspace):
    root, character = workspace
    doc, chat = root / "data/train/ada/documents.jsonl", root / "data/train/ada/chat.jsonl"
    path = runner.prepare(character, [str(doc)], str(chat), "ada_repeat")
    cfg = runner.load_config(path)
    assert cfg["name"] == "ada_repeat"
    assert cfg["documents"]["corpora"] == [str(doc)] and cfg["chat"]["data"] == str(chat)


def test_missing_data_fails_before_any_subprocess(workspace, monkeypatch):
    root, character = workspace
    (root / "data/train/ada/documents.jsonl").unlink()
    calls = []
    monkeypatch.setattr(runner.subprocess, "run", lambda *a, **kw: calls.append(a))
    with pytest.raises(ValueError, match="build the data first"):
        runner.run_character(character)
    assert calls == []


def test_stale_smoke_runs_before_rental_and_current_receipt_skips_it(workspace, monkeypatch):
    root, character = workspace
    calls = []
    monkeypatch.setattr(runner.subprocess, "run", lambda argv, **kw: calls.append(argv))
    path = runner.run_character(character)
    assert [c[1] for c in calls] == ["box-smoke", "box-rent"]
    receipt = path.parent / "smoke_passed.json"
    receipt.write_text(json.dumps({"driver_config_sha256": runner.driver_config_sha(path), "code_sha256": {"driver.py": runner.sha(root / "driver.py")}}))
    calls.clear()
    runner.run_character(character)
    assert [c[1] for c in calls] == ["box-rent"]
    (root / "driver.py").write_text("changed")
    calls.clear()
    runner.run_character(character)
    assert [c[1] for c in calls] == ["box-smoke", "box-rent"]


def test_just_command_accepts_named_overrides():
    result = subprocess.run(["just", "--dry-run", "name=ada_repeat", "documents=docs.jsonl", "chat=chat.jsonl",
                             "run-character", "tests/fixtures/characters/ada/character.yaml"], cwd=ROOT, capture_output=True, text=True, check=True)
    assert "--name 'ada_repeat'" in result.stderr
    assert "--documents docs.jsonl" in result.stderr and "--chat 'chat.jsonl'" in result.stderr
