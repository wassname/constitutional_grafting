"""Synthetic contributor fixtures only; never embed real private evaluation text. -- PI/OpenAI"""
import importlib.util
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/box"))


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts/eval" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pooler = load_script("85_pool_questions")
FIXTURE = ROOT / "tests/fixtures/study_questions"


def test_pool_two_constitutions_and_freeze(tmp_path):
    items, manifest = pooler.pool(FIXTURE)
    assert {r["id"] for r in items} == {"contrib_ada_arithmetic", "contrib_bea_arithmetic"}
    assert {r["source_constitution"] for r in items} == {"ada", "bea"}
    assert all(r["judged"] and r["family"] == "contrib" and len(r["turns"]) == 1 for r in items)
    assert items[1]["good_example"] == "Six."
    assert manifest["source_repo_commit"] and len(manifest["ids"]) == 2
    target = pooler.freeze(FIXTURE, [], tmp_path / "frozen")
    assert [json.loads(l) for l in target.read_text().splitlines()] == items
    with pytest.raises(FileExistsError):
        pooler.freeze(FIXTURE, [], target.parent)


def test_extra_private_directory_duplicates_and_template_skip(tmp_path):
    shutil.copytree(FIXTURE, tmp_path / "repo")
    repo = tmp_path / "repo"
    template = repo / "constitutions/_template/questions.yaml"
    template.parent.mkdir()
    template.write_text("not a question list")
    assert len(pooler.pool(repo)[0]) == 2
    extra = tmp_path / "extra"
    extra.mkdir()
    shutil.copyfile(repo / "planning/questions/bea.yaml", extra / "bea.yaml")
    with pytest.raises(ValueError, match="Duplicate pooled id"):
        pooler.pool(repo, [extra])
    (extra / "bea.yaml").rename(extra / "cea.yaml")
    assert len(pooler.pool(repo, [extra])[0]) == 3
    with pytest.raises(ValueError, match="No private questions directory"):
        pooler.pool(repo, [extra / "missing"])


@pytest.mark.parametrize("text", ["[]", "- id: missing-fields", "- id: x\n  kind: far\n  question: Q\n  good_answer_does: A"])
def test_invalid_question_pool(tmp_path, text):
    (tmp_path / "bad.yaml").write_text(text)
    with pytest.raises(ValueError):
        pooler.pool(tmp_path, [tmp_path])
