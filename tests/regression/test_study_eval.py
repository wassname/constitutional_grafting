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
    assert not any("refusal_can_be_right" in r for r in items)  # not a per-question setting
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


def test_full_extras_preserve_calibrated_sets_and_scan_probe(tmp_path):
    import tinychar
    extra = pooler.freeze(FIXTURE, [], tmp_path / "pool")
    source = ROOT / "configs/eval/inputs/run17/items.jsonl"
    for size in ("probe", "scan", "full"):
        target = tmp_path / f"{size}.jsonl"
        tinychar.evaluation_items(source, target, tinychar.SUBSETS[size], size, [extra])
        ids = {r["id"] for r in tinychar.rows(target)}
        calibrated = {l for l in (ROOT / tinychar.SUBSETS[size]).read_text().splitlines() if l and not l.startswith("#")}
        assert ids == calibrated | ({"contrib_ada_arithmetic", "contrib_bea_arithmetic"} if size == "full" else set())
    tinychar.evaluation_items(source, target, tinychar.SUBSETS["full"], "full", [extra], smoke=1)
    assert len(tinychar.rows(target)) == 2
    with pytest.raises(ValueError, match="duplicate id"):
        tinychar.extra_items([extra, extra])


def test_extra_items_config_checks(tmp_path):
    import box
    cfg = box.load_config(ROOT / "configs/runs/run22.yaml")
    cfg["extra_items"] = [str(pooler.freeze(FIXTURE, [], tmp_path / "pool"))]
    assert any("change-only" in e for e in box.check_config(cfg))
    cfg["character"].pop("judge_refs")
    assert box.check_config(cfg) == []
    cfg["extra_items"].append("missing.jsonl")
    assert any("extra_items" in e for e in box.check_config(cfg))


def test_swapped_reference_matches_existing_rerun_convention(tmp_path):
    import tinychar
    source, target = tmp_path / "ref.jsonl", tmp_path / "noise.jsonl"
    records = [{"model": "instruct", "item_id": i, "sample": s, "turns": [f"draw{s}"]}
               for i in ("near", "far") for s in (0, 1)]
    tinychar.write_rows(source, records)
    tinychar.swapped_reference(source, target)
    noise = tinychar.rows(target)
    assert noise == [r | {"model": "instruct_rerun", "sample": 1 - r["sample"]} for r in records]
    tinychar.write_rows(source, records[:1])
    with pytest.raises(AssertionError, match="two samples"):
        tinychar.swapped_reference(source, target)


reporter = load_script("86_study_report")


def judged_directory(path, model, scores, base):
    items, _ = pooler.pool(FIXTURE)
    items += [{"id": i, "family": family, "source": source, "judged": True,
               "system": None, "turns": ["Synthetic arithmetic"]} for i, family, source in (
                   ("mach_fixture", "advice", "MACHIAVELLI synthetic source"),
                   ("da_fixture", "difficult_advice", "Synthetic advice"),
                   ("unshared_fixture", "advice", "Unshared synthetic source"),
                   ("choice_game_fixture", "choice", "machiavelli_character_scenarios synthetic source"),
                   ("renamed_advice_fixture", "advice", "LASR synthetic source"),
                   ("stoic_fixture", "tiny_stoic", "Synthetic vignette"))]
    path.mkdir()
    (path / "items.jsonl").write_text("".join(json.dumps(r) + "\n" for r in items))
    (path / "meta.json").write_text(json.dumps({"refs": "", "refs_fields": [],
        "change": {"label": str(path / "change"), "text": "Own character", "not": "No polish"},
        "judge": "jev", "turn_judge": "jev", "rubric": "synthetic"}))
    records = [{"item_id": it["id"], "model": model, "base_model": base, "sample": s,
                "on_target": scores[it["id"]] + (0.1 if s else -0.1)} for it in items for s in (0, 1)]
    (path / "judged.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
    return path


@pytest.fixture
def study_outputs(tmp_path):
    a = {"contrib_ada_arithmetic": 1., "contrib_bea_arithmetic": .2, "mach_fixture": 2., "da_fixture": -2., "unshared_fixture": .3,
         "choice_game_fixture": 1.5, "renamed_advice_fixture": -1., "stoic_fixture": .8}
    b = a | {"contrib_ada_arithmetic": .4, "contrib_bea_arithmetic": .1}
    zero = {i: 0. for i in a}
    runs = {"ada": judged_directory(tmp_path / "a", "graft_ada", a, "ada_20261101_instruct"),
            "bea": judged_directory(tmp_path / "b", "graft_bea", b, "bea_20261101_instruct")}
    noises = {slug: judged_directory(tmp_path / (slug + "_noise"), f"{slug}_20261101_instruct_rerun", zero, f"{slug}_20261101_instruct") for slug in runs}
    return runs, noises


def test_report_groups_intervals_samples_and_order(study_outputs):
    runs, noises = study_outputs
    record = reporter.load_scores(runs["ada"])
    stats = reporter.summarize(record, "ada", draws=200)
    # near: own contributor (1.0) + shared-source items mach 2, da -2, choice 1.5, lasr -1, stoic .8 -> mean 2.3/6
    assert stats["near"][0] == pytest.approx(2.3 / 6) and stats["near"][-1] == 6
    assert stats["mid"][0] == pytest.approx(.3) and stats["mid"][-1] == 1
    assert stats["far"][0] == pytest.approx(.2) and stats["far"][-1] == 1
    assert stats["near_far"][0] == pytest.approx(2.3 / 6 - .2) and stats["mid_far"][0] == pytest.approx(.1)
    assert stats["dilemma"][-1] == 2  # choice + tiny_stoic fixtures
    assert stats["own normal"][0] == 1 and stats["other totally unexpected"][0] == pytest.approx(.2)
    assert reporter.load_scores(runs["ada"])["base"] != reporter.load_scores(runs["bea"])["base"]
    text = reporter.report(runs, noises, draws=200)
    assert text.index("## ada") < text.index("## bea")
    assert "| Model | Dilemmas | Rest |" in text
    assert "Instruct noise (swapped samples)" in text
    assert "90% percentile item-bootstrap intervals" in text
    assert "What is two plus two" not in text and "Gives the correct" not in text
    assert reporter.report(runs, noises, draws=200) == text


def test_study_report_cli(study_outputs, tmp_path):
    import subprocess

    runs, noises = study_outputs
    out = tmp_path / "report.md"
    command = [sys.executable, ROOT / "scripts/eval/86_study_report.py", "--out", out]
    for slug in runs:
        command += ["--run", f"{slug}={runs[slug]}", "--noise", f"{slug}={noises[slug]}"]
    subprocess.run(command, check=True, capture_output=True, text=True)
    assert out.read_text() == reporter.report(runs, noises)


def test_bootstrap_is_over_items_not_draws():
    items = {f"contrib_{slug}_{i}": {"family": "contrib", "source_constitution": slug, "distance": "normal"}
             for slug in ("ada", "bea") for i in range(3)}
    items["unshared"] = {"family": "advice", "source": "Unshared synthetic source"}
    record = {"items": items, "scores": {i: float(j % 3) for j, i in enumerate(items)}}
    stats = reporter.summarize(record, "ada", draws=1000)
    assert stats["near"][0] == 1 and stats["near"][-1] == 3
    assert stats["near"][1] < stats["near"][0] < stats["near"][2]
    assert stats["near_far"][1] < 0 < stats["near_far"][2]


@pytest.mark.parametrize("failure", ["missing", "duplicate", "protocol", "refs", "nonfinite", "wrong_judge"])
def test_report_rejects_incomplete_or_mixed_protocols(study_outputs, failure):
    runs, noises = study_outputs
    path = runs["bea"]
    records = [json.loads(l) for l in (path / "judged.jsonl").read_text().splitlines()]
    if failure == "missing":
        records.pop()
    if failure == "duplicate":
        records.append(records[0])
    if failure == "nonfinite":
        records[0]["on_target"] = float("nan")
    (path / "judged.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
    if failure == "protocol":
        records = [json.loads(l) for l in (path / "items.jsonl").read_text().splitlines()]
        records[0]["turns"] = ["Different question"]
        (path / "items.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
    if failure == "refs":
        (path / "meta.json").write_text('{"refs": "refs.jsonl", "refs_fields": []}')
    if failure == "wrong_judge":
        meta = json.loads((path / "meta.json").read_text())
        meta["change"]["text"] = "A different character"
        (path / "meta.json").write_text(json.dumps(meta))
    with pytest.raises(ValueError):
        reporter.report(runs, noises, draws=100)


def test_report_requires_both_near_far_and_noise(study_outputs):
    runs, noises = study_outputs
    with pytest.raises(ValueError, match="exactly one --noise"):
        reporter.report(runs, {})
    record = reporter.load_scores(runs["ada"])
    only_contrib = record | {"items": {i: it for i, it in record["items"].items() if it["family"] == "contrib"}}
    with pytest.raises(ValueError, match="near and mid"):
        reporter.summarize(only_contrib, "ada")


def test_pool_schema_runs_pinned_judge_turn_questions_without_api_calls(tmp_path):
    import subprocess
    import tinychar
    if not (tinychar.TC / "scripts/03_judge.py").exists():
        pytest.skip("private pinned judge not installed")
    pool = pooler.freeze(FIXTURE, [], tmp_path / "pool")
    full = tinychar.evaluation_items(ROOT / "configs/eval/inputs/run17/items.jsonl", tmp_path / "full.jsonl", tinychar.SUBSETS["full"], "full", [pool])
    source = tmp_path / "contrib.jsonl"  # the extras as the box hands them to the pinned judge
    tinychar.write_rows(source, [r for r in tinychar.rows(full) if r["family"] == "contrib"])
    code = '''import json, os, runpy, sys
os.environ["OPENROUTER_API_KEY"] = "offline-schema-test-no-api-calls"
judge = runpy.run_path("scripts/03_judge.py", run_name="schema_test")
for line in open(sys.argv[1]):
    item = json.loads(line)
    definitions, questions = judge["turn_questions"](item, {"dialogue_A": [{"user": item["turns"][0], "assistant": "Synthetic answer"}]})
    assert definitions and questions
    assert judge["pair_examples"]({}, item, None) == ""
print("pinned item schema and guide-free prompt checked")
'''
    result = subprocess.run([str(tinychar.TC / ".venv/bin/python"), "-c", code, str(source)],
                            cwd=tinychar.TC, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert "guide-free prompt checked" in result.stdout


def test_report_rejects_mismatched_baseline_within_constitution(study_outputs):
    runs, noises = study_outputs
    path = noises["ada"] / "judged.jsonl"
    records = [json.loads(line) for line in path.read_text().splitlines()]
    for record in records:
        record |= {"base_model": "wrong_instruct", "model": "wrong_instruct_rerun"}
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    with pytest.raises(ValueError, match="different Instruct baselines"):
        reporter.report(runs, noises)


def test_source_exclusions_ignore_id_spelling():
    assert reporter.shares_seed_source({"id": "choice_game_new", "family": "choice", "source": "MACHIAVELLI"})
    assert reporter.shares_seed_source({"id": "renamed", "family": "advice", "source": "LASR"})
    assert reporter.shares_seed_source({"id": "renamed", "family": "difficult_advice", "source": "Other label"})
    assert reporter.shares_seed_source({"id": "renamed", "family": "tiny_stoic", "source": "Other label"})
    assert not reporter.shares_seed_source({"id": "mach_not_from_training", "family": "advice", "source": "Unshared source"})


def test_report_matches_existing_interval_convention(study_outputs):
    runs, noises = study_outputs
    text = reporter.report(runs, noises)
    assert "90% percentile item-bootstrap intervals (2,000 draws, seed 0)" in text
