"""Calibrated subsets, safe on-box checks and reference-relative breakdown. -- PI/OpenAI"""
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import time
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/box"))
import tinychar
import rent


def health(model, coherent=1, correct=1, truncated=0):
    return {"model": model, "item_id": "test", "sample": 0, "judged": False, "check": {"correct": correct},
            "jev": [{"coherent": coherent}], "turn_checks": [{"truncated": truncated}]}


def reply(model, tokens=100, finish="stop"):
    return {"model": model, "item_id": "test", "sample": 0, "turns": [{"n_tokens": tokens, "finish_reason": finish}]}


SETTINGS = {"min_gsm": .8, "max_bad_share": .3}


@pytest.mark.parametrize("ours,reference,expected", [(0, 1, True), (0, 0, False), (1, 1, False)])
def test_reference_failed_capability_is_inconclusive(ours, reference, expected):
    s = tinychar.comparison([health("graft", correct=ours), health("ref", correct=reference)], [reply("graft"), reply("ref")], "graft", "ref")
    assert tinychar.broken(s, SETTINGS) == expected


def test_coherence_is_reference_relative():
    rs = [reply("graft"), reply("ref")]
    assert tinychar.broken(tinychar.comparison([health("graft", .1), health("ref", .99)], rs, "graft", "ref"), SETTINGS)
    assert not tinychar.broken(tinychar.comparison([health("graft", .1), health("ref", .1)], rs, "graft", "ref"), SETTINGS)


@pytest.mark.parametrize("cap,other_finish,expected", [(20, "stop", False), (200, "length", False), (200, "stop", True)])
def test_truncation_requires_room_over_finished_reference(cap, other_finish, expected):
    s = tinychar.comparison([health("graft", truncated=1), health("ref")],
                           [reply("graft", cap, "length"), reply("ref", 100, other_finish)], "graft", "ref")
    assert tinychar.broken(s, SETTINGS) == expected


@pytest.mark.parametrize("size,count", [("probe", 27), ("scan", 65), ("full", 117)])
def test_calibrated_subset_counts(tmp_path, size, count):
    target = tinychar.subset(ROOT / "slop/eval/run17/inputs/items.jsonl", tmp_path / "items.jsonl", tinychar.SUBSETS[size])
    assert len(tinychar.rows(target)) == count


def test_deployment_only_pinned_code_data_and_openrouter_key(tmp_path, monkeypatch):
    monkeypatch.setattr(rent, "ROOT", tmp_path)
    monkeypatch.setattr(rent, "CODE_DIRS", ["scripts"])
    monkeypatch.setattr(rent, "TC", tmp_path / ".local/tiny-character-9e33eed")
    inputs = {"change": tmp_path / "change.md", "refs": tmp_path / "refs.jsonl"}
    monkeypatch.setattr(rent, "JUDGE_V2", inputs)
    for path in [tmp_path / "scripts/code.py", tmp_path / "inputs/items.jsonl", *inputs.values(),
                 *(rent.TC / p for p in ("src/code.py", "scripts/03_judge.py", "data/items.jsonl", "pyproject.toml", "uv.lock", ".local/raw/gsm8k_test.parquet")),
                 rent.TC / ".venv/secret", rent.TC / ".env"]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    (tmp_path / ".env").write_text("VASTAI_API_KEY=do-not-transfer\nOPENROUTER_API_KEY=judge-only\nOTHER=private\n")
    lease = object.__new__(rent.Lease)
    lease.cfg = {"inputs": "inputs"}
    lease.out = tmp_path
    commands = []
    lease.remote = lambda cmd, **kw: commands.append((cmd, kw))
    lease.push()
    with tarfile.open(fileobj=io.BytesIO(commands[0][1]["input"]), mode="r:gz") as archive:
        names = archive.getnames()
        assert ".local/tiny-character-9e33eed/scripts/03_judge.py" in names
        assert not any(".venv" in n or n.endswith(".env") for n in names)
    assert commands[1][1]["input"] == b"OPENROUTER_API_KEY=judge-only\n"
    assert "chmod 600" in commands[1][0]
    assert "UV_PROJECT_ENVIRONMENT=.venv uv sync --locked" in commands[2][0]
    assert "command -v git" in commands[2][0] and "apt-get install -y -qq git" in commands[2][0]
    assert "test -x .venv/bin/python" in commands[2][0]
    assert "PYTHONPATH=src .venv/bin/python -c 'import inspect_ai, llm_judge, tiny_character'" in commands[2][0]
    assert commands[2][1]["timeout"] >= 1200


@pytest.mark.parametrize("fixture,model,reference,expected", [
    ("run19_nheim", "r19_probe_docs_next_mix_1", "r19_probe_docs_next_ref", False),
    ("run19_nheim", "r19_probe_docs_next_ref", "r19_probe_docs_next_mix_1", False),
    ("run19_scans", "r19_groups_0.8", "r19_instruct", True),
    ("run19_scans", "r19_groups_0.25", "r19_instruct", False),
    ("run19_scans", "r19_instruct_rerun", "r19_instruct", False),
])
def test_recorded_judge_breakdown(fixture, model, reference, expected):
    data = json.loads((ROOT / f"tests/fixtures/box_tinychar/{fixture}.json").read_text())
    result = tinychar.comparison(data["judged"], data["replies"], model, reference)
    assert tinychar.broken(result, SETTINGS) == expected


def test_judge_excludes_executable_capability_checks_and_intersects_pairs(tmp_path, monkeypatch):
    monkeypatch.setattr(tinychar, "ROOT", tmp_path)
    tc = tmp_path / "tc"
    monkeypatch.setattr(tinychar, "TC", tc)
    (tc / "data").mkdir(parents=True)
    items = [{"id": i, "judged": False, "family": f, "checks": {"kind": k}} for i, f, k in
             [("safe", "capability", "json_keys"), ("code", "code", "unittest"), ("capcode", "capability", "code"), ("tool", "tools", "tool_call"), ("plan", "long", "fs_plan"), ("agent", "agent", "agent_turn"), ("missing", "capability", "json_keys")]]
    tinychar.write_rows(tc / "data/items.jsonl", items)
    tinychar.write_rows(tmp_path / "items.jsonl", items)
    refs = tmp_path / "refs.jsonl"
    refs.write_text("")
    monkeypatch.setitem(tinychar.JUDGE_V2, "refs", refs)
    (tmp_path / ".env").write_text("OPENROUTER_API_KEY=fixture\n")
    def raw(m, i):
        return reply(m) | {"item_id": i, "base_model": "ref"}
    tinychar.write_rows(tmp_path / "mine.jsonl", [raw("graft", i["id"]) for i in items])
    tinychar.write_rows(tmp_path / "ref.jsonl", [raw("ref", i["id"]) for i in items if i["id"] != "missing"])
    def run(argv, **kw):
        path = Path(argv[argv.index("--replies") + 1])
        assert {(r["item_id"], r["sample"]) for r in tinychar.rows(path)} == {("safe", 0)}
        assert "--subset" in argv and "--refs" in argv
        dest = tc / "results" / argv[argv.index("--run") + 1]
        dest.mkdir(parents=True)
        tinychar.write_rows(dest / "judged.jsonl", [health(m) | {"item_id": "safe"} for m in ("graft", "ref")])
        (dest / "meta.json").write_text("{}")
    monkeypatch.setattr(tinychar.subprocess, "run", run)
    assert not tinychar.broken(tinychar.judge(tmp_path / "mine.jsonl", tmp_path / "ref.jsonl", tmp_path / "score", time.time() + 60, tmp_path / "items.jsonl"), SETTINGS)


@pytest.mark.parametrize("coherent,bad", [(.6, 0), (.5, 1), (.49, 1)])
def test_coherence_counts_thresholded_turns_not_mean_probabilities(coherent, bad):
    s = tinychar.comparison([health("graft", coherent), health("ref")], [reply("graft"), reply("ref")], "graft", "ref")
    assert s["bad_share"] == bad


@pytest.mark.parametrize("flag", ["looped", "lang_switch", "empty", "role_confusion"])
def test_any_turn_flag_is_a_bad_turn(flag):
    ours = health("graft")
    ours["turn_checks"][0][flag] = 1
    s = tinychar.comparison([ours, health("ref")], [reply("graft"), reply("ref")], "graft", "ref")
    assert s["bad_share"] == 1


def test_bad_turn_margin_is_strictly_greater_than_point_three():
    s = {"bad_share": .3, "reference_bad_share": 0, "capability_retained": None, "gsm_retained": None}
    assert not tinychar.broken(s, SETTINGS)
    assert tinychar.broken(s | {"bad_share": .31}, SETTINGS)


@pytest.mark.parametrize("reference_failed", [False, True])
def test_gsm_retention_is_separate_from_other_capability(reference_failed):
    judged, replies = [], []
    for i in ["gsm_cot_0", "gsm_cot_1", "gsm_cot_2", "gsm_json_0", "long_story"]:
        for m in ("graft", "ref"):
            correct = 0 if i == "gsm_cot_0" and (m == "graft" or reference_failed) else 1
            judged.append(health(m, correct=correct) | {"item_id": i})
            replies.append(reply(m) | {"item_id": i})
    s = tinychar.comparison(judged, replies, "graft", "ref")
    assert s["capability_retained"] == (1 if reference_failed else .8)
    assert s["gsm_retained"] == (1 if reference_failed else .75)
    assert len(s["gsm_reference_passed"]) == (3 if reference_failed else 4)
    assert tinychar.broken(s, SETTINGS) == (not reference_failed)


def test_gsm_reference_failures_are_inconclusive():
    judged = [health("graft", correct=0) | {"item_id": "gsm_cot_0"}, health("ref", correct=0) | {"item_id": "gsm_cot_0"}]
    replies = [reply(m) | {"item_id": "gsm_cot_0"} for m in ("graft", "ref")]
    s = tinychar.comparison(judged, replies, "graft", "ref")
    assert s["gsm_retained"] is None
    assert not tinychar.broken(s, SETTINGS)


def test_recorded_nheim_and_instruct_turn_counts():
    for fixture, model, reference, bad, count in [
        ("run19_nheim", "r19_probe_docs_next_mix_1", "r19_probe_docs_next_ref", 2, 7),
        ("run19_scans", "r19_instruct_rerun", "r19_instruct", 0, 4),
    ]:
        d = json.loads((ROOT / f"tests/fixtures/box_tinychar/{fixture}.json").read_text())
        s = tinychar.comparison(d["judged"], d["replies"], model, reference)
        assert s["bad_share"] == bad / count
        assert s["reference_bad_share"] == 0
        assert s["gsm_retained"] is None


def test_judge_items_warns_and_uses_frozen_text_with_pinned_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(tinychar, "TC", tmp_path)
    (tmp_path / "data").mkdir()
    frozen = {"id": "drift", "system": "frozen system", "turns": ["frozen user"]}
    pin = frozen | {"system": "changed system", "turns": ["changed user"], "refusal_can_be_right": True}
    tinychar.write_rows(tmp_path / "data/items.jsonl", [pin])
    tinychar.write_rows(tmp_path / "frozen.jsonl", [frozen])
    with pytest.warns(UserWarning, match="judge uses frozen system/turns for drift"):
        item = tinychar.judge_items(tmp_path / "frozen.jsonl")["drift"]
    assert item == pin | {k: frozen[k] for k in ("system", "turns")}


@pytest.mark.parametrize("size,missing", [("probe", set()), ("scan", set()), ("full", {"code_bcb_814"})])
def test_frozen_subset_text_matches_pinned_items(size, missing):
    if not (tinychar.TC / "data/items.jsonl").exists():
        pytest.skip("local tiny-character pin not installed")
    frozen = {r["id"]: r for r in tinychar.rows(ROOT / "slop/eval/run17/inputs/items.jsonl")}
    pin = {r["id"]: r for r in tinychar.rows(tinychar.TC / "data/items.jsonl")}
    ids = {l for l in (ROOT / tinychar.SUBSETS[size]).read_text().splitlines() if l and not l.startswith("#")}
    assert ids - pin.keys() == missing
    for i in ids & pin.keys():
        assert {k: frozen[i][k] for k in ("system", "turns")} == {k: pin[i][k] for k in ("system", "turns")}, i
    for i in missing:
        assert frozen[i]["family"] == "code"  # generated, but never sent to the on-box judge


def test_probe_adds_four_calibrated_gsm_items():
    ids = {l for l in (ROOT / tinychar.SUBSETS["probe"]).read_text().splitlines() if l and not l.startswith("#")}
    assert {i for i in ids if i.startswith("gsm_")} == {"gsm_cot_0", "gsm_cot_1", "gsm_cot_3", "gsm_json_0"}


@pytest.mark.parametrize("item_id,cap", [("gsm_cot_0", 700), ("gsm_json_0", 700), ("long_story", 2500)])
def test_gen_replies_honors_frozen_item_caps_without_probe_override(monkeypatch, item_id, cap):
    spec = importlib.util.spec_from_file_location("gen_replies", ROOT / "scripts/eval/19_gen_replies.py")
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    item = next(r for r in tinychar.rows(ROOT / "slop/eval/run17/inputs/items.jsonl") if r["id"] == item_id)
    seen = []
    def chat(url, model, messages, max_tokens, *args, **kw):
        seen.append(max_tokens)
        return {"assistant": "fixture", "marker_violation": False}
    monkeypatch.setattr(gen, "chat", chat)
    args = SimpleNamespace(url="fixture", model="graft", base_model="ref", temperature=.7, max_tokens_cap=None)
    gen.run_item(args, item, 0)
    assert seen == [cap] * len(item["turns"])
