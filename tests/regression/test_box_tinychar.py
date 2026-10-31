"""Calibrated subsets, safe on-box checks and reference-relative breakdown. -- PI/OpenAI"""
import io
import json
from pathlib import Path
import sys
import tarfile
import time

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


@pytest.mark.parametrize("size,count", [("probe", 23), ("scan", 65), ("full", 117)])
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
    assert "uv sync --locked" in commands[2][0]


@pytest.mark.parametrize("fixture,model,reference,expected", [
    ("run19_nheim", "r19_probe_docs_next_mix_1", "r19_probe_docs_next_ref", True),
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
             [("safe", "capability", "json_keys"), ("code", "code", "unittest"), ("capcode", "capability", "code"), ("tool", "tools", "tool_call"), ("missing", "capability", "json_keys")]]
    tinychar.write_rows(tc / "data/items.jsonl", items)
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
    assert not tinychar.broken(tinychar.judge(tmp_path / "mine.jsonl", tmp_path / "ref.jsonl", tmp_path / "score", time.time() + 60), SETTINGS)
