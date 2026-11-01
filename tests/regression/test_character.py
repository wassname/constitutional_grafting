"""Character loading shares the constitution repository's comment semantics. -- PI/OpenAI"""
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from constitutional_grafting import character


def fixture(tmp_path, monkeypatch):
    root = tmp_path / "grafting"
    root.mkdir()
    monkeypatch.setattr(character, "ROOT", root)
    repo = tmp_path / "constitutions"
    repo.mkdir()
    source = repo / "constitution.md.j2"
    source.write_text("I am Ada. {# a private note\non two lines #}\nI measure before judging.\n")
    subprocess.run(["git", "init", "-q", repo], check=True)
    subprocess.run(["git", "-C", repo, "add", source.name], check=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "-qm", "constitution"], check=True)
    path = root / "character.yaml"
    path.write_text(yaml.safe_dump({"name": "Ada", "constitution": "../constitutions/constitution.md.j2", "maker": "a lab"}))
    return path, source


def test_load_character_sibling_template_and_git_revision(tmp_path, monkeypatch):
    path, source = fixture(tmp_path, monkeypatch)
    c = character.load_character(path)
    assert c["maker"] == "a lab"
    assert c["constitution_path"] == str(source)
    assert c["constitution_text"] == "I am Ada. \nI measure before judging.\n"
    assert c["constitution_commit"] == subprocess.check_output(["git", "-C", source.parent, "log", "-1", "--format=%h"], text=True).strip()
    assert c["constitution_dirty"] is False


def test_load_character_warns_without_failing_on_dirty_constitution(tmp_path, monkeypatch):
    path, source = fixture(tmp_path, monkeypatch)
    original = character.load_character(path)["constitution_commit"]
    source.write_text(source.read_text() + "An uncommitted line.\n")
    with pytest.warns(UserWarning, match="uncommitted edits"):
        c = character.load_character(path)
    assert c["constitution_commit"] == original
    assert c["constitution_dirty"] is True
    assert c["constitution_text"].endswith("An uncommitted line.\n")


def test_load_character_rejects_unbalanced_comments(tmp_path, monkeypatch):
    path, source = fixture(tmp_path, monkeypatch)
    source.write_text("I am Ada. {# not closed")
    with pytest.raises(AssertionError, match="comment is not closed"):
        character.load_character(path)


def test_deployed_character_preserves_origin_revision_without_git(tmp_path):
    source = tmp_path / "constitution.md"
    source.write_text("I am Ada.\n")
    path = tmp_path / "character.yaml"
    path.write_text(yaml.safe_dump({"name": "Ada", "constitution": str(source), "constitution_commit": "abc1234", "constitution_dirty": False}))
    c = character.load_character(path)
    assert c["constitution_commit"] == "abc1234" and not c["constitution_dirty"]
