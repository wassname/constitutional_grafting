"""Single-adapter dose bracketing, locked bases, and full fractions. -- PI/OpenAI"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/box"))
spec = importlib.util.spec_from_file_location("box", ROOT / "scripts/box/box.py")
box = importlib.util.module_from_spec(spec)
spec.loader.exec_module(box)


@pytest.mark.parametrize("hot", [False, True])
@pytest.mark.parametrize("bisect", [False, True])
def test_search_adapter_grid_or_adaptive_extension(tmp_path, hot, bisect):
    cfg = {"hot_swap": hot, "prefix": "t_", "probe": box.PROBE_DEFAULTS | {"bisect": bisect}}
    calls = []

    def command(argv, *_):
        cells = yaml.safe_load(Path(argv[2]).read_text())["cells"]
        calls.append(cells)
        for name, cell in cells.items():
            assert cell["documents"] == .5
            (tmp_path / f"probe_t_{name}.done").write_text(json.dumps(
                {"model": name, "bad_share": float(cell["chat"] >= 8), "reference_bad_share": 0, "capability_retained": 1, "gsm_retained": 1}))

    result = box.search_adapter("chat", {"documents": .5}, cfg, tmp_path, tmp_path, {}, 0, False, command, lambda *_: None)
    assert result["coherent_to"] < result["breakdown"] == 8
    if hot:
        assert len(calls) == (2 if bisect else 1)
        assert list(calls[0])[0] == "probe_chat_ref"
        assert {c["chat"] for n, c in calls[0].items() if not n.endswith("ref")} == {.125, .25, .5, 1, 2, 4, 8, 16}
    else:
        assert [list(cells) for cells in calls[:4]] == [["probe_chat_ref"], ["probe_chat_1", "probe_chat_2"], ["probe_chat_4"], ["probe_chat_8"]]
    if bisect:
        assert result["coherent_to"] == 5.66


def test_search_adapter_smoke_one_reference_and_one_dose(tmp_path):
    cfg = {"hot_swap": True, "prefix": "t_", "probe": box.PROBE_DEFAULTS}
    calls = []

    def command(argv, *_):
        cells = yaml.safe_load(Path(argv[2]).read_text())["cells"]
        calls.append(cells)
        for name in cells:
            (tmp_path / f"probe_t_{name}.done").write_text(json.dumps(
                {"model": name, "bad_share": 0, "reference_bad_share": 0, "capability_retained": 1, "gsm_retained": 1}))

    box.search_adapter("documents", {}, cfg, tmp_path, tmp_path, {}, 0, True, command, lambda *_: None)
    assert [list(c) for c in calls] == [["probe_documents_ref", "probe_documents_1"]]


def test_unbracketed_search_cannot_silently_lock_or_evaluate():
    with pytest.raises(AssertionError, match="breakdown not bracketed"):
        box.breakdown_dose({"coherent_to": 16, "breakdown": None})


def test_choose_cells_middle_scan_first_full_last_on_locked_documents():
    found = {"coherent_to": 1, "breakdown": 2}
    cells = box.choose_cells(found, {"documents": .5}, {"full": [.25, .5]})
    assert list(cells) == ["chat_1", "chat_0.5", "chat_1.6", "full_chat_0.5", "full_chat_1"]
    assert all(c["documents"] == .5 for c in cells.values())


def test_run22_new_schema_checks_and_has_exact_frozen_training_base():
    cfg = box.load_config(ROOT / "configs/runs/run22.yaml")
    assert box.check_config(cfg) == []
    assert [s["dose"] for s in cfg["base_adapters"].values()] == [.5, 1, 1]
    from cells import expand
    assert expand(cfg["cells"]["full_all_0.75"], cfg) == [("stoic", .5), ("const", 1), ("other", 1), ("chat", .75)]
    assert not box.needs_base(cfg)


def test_smoke_character_and_both_datasets_are_generated(tmp_path):
    assert "documents" not in box.smoke_config({"inputs": "configs/eval/inputs/run17", "name": "test"}, tmp_path)  # chat-only smoke
    cfg = box.smoke_config({"inputs": "configs/eval/inputs/run17", "name": "test", "documents": {"corpora": []}}, tmp_path)
    assert cfg["character"]["name"] == "Ada"
    assert Path(cfg["character"]["constitution"]).read_text() == (ROOT / "tests/fixtures/characters/ada/constitution.md").read_text()
    assert box.needs_base(cfg)
    assert Path(cfg["documents"]["corpora"][0]).read_text() == (ROOT / "tests/fixtures/characters/ada/passages.jsonl").read_text()
    rows = [json.loads(l) for l in Path(cfg["chat"]["data"]).read_text().splitlines()]
    assert all(r["segments"][-1]["text"].endswith("<|im_end|>") for r in rows)
    assert not box.existing_adapters(cfg)


def test_rental_hardware_class_defaults():
    from rent import offer_query
    q = offer_query({})
    assert q == {"gpu_ram": {"gte": 90000}, "compute_cap": {"eq": 1200}, "verified": {"eq": True}, "reliability2": {"gte": .98}}


def test_general_training_schema_accepts_shared_character_metadata(tmp_path):
    cfg = box.load_config(ROOT / "configs/runs/run22.yaml") | {"documents": {"corpora": []}}
    cfg = box.smoke_config(cfg, tmp_path)
    cfg["character"] |= {"maker": "a collaborator", "about": "a garden helper", "researcher": "a researcher", "held_out_names": ["Desk"]}
    extra = tmp_path / "second.jsonl"
    extra.write_text('{"text": "A second source."}\n')
    cfg["documents"]["corpora"].append(str(extra))
    assert box.check_config(cfg) == []
    assert box.needs_base(cfg)
    extra.unlink()
    assert any("documents.corpora" in p for p in box.check_config(cfg))


def test_existing_document_adapter_skips_corpora_requirement():
    cfg = box.load_config(ROOT / "configs/runs/run22.yaml")
    cfg.pop("base_adapters")
    cfg["documents"] = {"adapter": "existing_document_folder", "dose": 0.5}
    assert box.check_config(cfg) == []
    assert box.existing_adapters(cfg)["documents"] == "existing_document_folder"
    assert not box.needs_base(cfg)


@pytest.mark.parametrize("hosts,budget,message", [(4, 100, "hosts; widen"), (5, 0, "exceeds budget")])
def test_rental_retains_host_diversity_and_budget_gates(tmp_path, monkeypatch, hosts, budget, message):
    import rent
    lease = object.__new__(rent.Lease)
    lease.cfg = {"max_hourly_rate": 2, "max_hours": 2, "budget_usd": budget, "character": {}}
    monkeypatch.setattr(rent, "prepare_judge", lambda *_: None)
    lease.state = None
    lease.state_path = tmp_path / "rental.json"
    lease.local = tmp_path
    lease.cfg_path = tmp_path / "config.yaml"
    (tmp_path / "smoke_passed.json").write_text(json.dumps({"driver_config_sha256": "ok", "code_sha256": {}}))
    monkeypatch.setattr(rent, "driver_config_sha", lambda _: "ok")
    offers = [{"host_id": i, "gpu_name": "any Blackwell", "cuda_max_good": 13, "dph_total": 1,
               "inet_down_cost": 0, "inet_up_cost": 0} for i in range(hosts)]
    calls = []

    def api(path):
        calls.append(path)
        return {"offers": offers}

    monkeypatch.setattr(rent, "api", api)
    with pytest.raises(AssertionError, match=message):
        lease.run()
    assert len(calls) == 1 and calls[0].startswith("/bundles/")


def test_hub_folder_adapter_resolution_and_local_path(tmp_path, monkeypatch):
    import rent
    import huggingface_hub
    lease = object.__new__(rent.Lease)
    lease.cfg = {"adapter_hub": "collaborator/adapters"}
    folder = tmp_path / "cached" / "document_adapter"
    folder.mkdir(parents=True)
    calls = []

    def download(repo, **kw):
        calls.append((repo, kw))
        return str(folder.parent)

    monkeypatch.setattr(huggingface_hub, "snapshot_download", download)
    assert lease.adapter_source("document_adapter") == folder
    assert calls == [("collaborator/adapters", {"allow_patterns": ["document_adapter/adapter_*"]})]
    assert lease.adapter_source(str(folder)) == folder
    assert len(calls) == 1


def test_character_path_loads_shared_fields_and_changes_invalidate_smoke(tmp_path):
    from confighash import driver_config_sha
    path = tmp_path / "character.yaml"
    path.write_text("name: Ada\nmaker: a collaborator\nconstitution: tests/fixtures/characters/ada/constitution.md\n")
    config = tmp_path / "run.yaml"
    config.write_text(yaml.safe_dump({"character": str(path), "budget_usd": 1}))
    assert box.load_config(config)["character"]["name"] == "Ada"
    assert box.load_config(config)["character"]["constitution_text"] == (ROOT / "tests/fixtures/characters/ada/constitution.md").read_text()
    original = driver_config_sha(config)
    config.write_text(yaml.safe_dump({"character": str(path), "budget_usd": 2}))
    assert driver_config_sha(config) == original
    path.write_text(path.read_text() + "judge_refs: changed.jsonl\n")
    assert driver_config_sha(config) != original


def test_fixed_chat_cells_cannot_change_the_locked_document_dose():
    cfg = box.load_config(ROOT / "configs/runs/run22.yaml")
    cfg.pop("base_adapters")
    cfg["documents"] = {"adapter": "existing_folder"}
    cfg["cells"]["full_all_0.75"]["documents"] = 2
    assert any("documents dose is locked" in p for p in box.check_config(cfg))


def test_existing_document_and_chat_adapters_require_their_training_dose():
    cfg = box.load_config(ROOT / "configs/runs/run22.yaml")
    cfg.pop("base_adapters")
    cfg["documents"] = {"adapter": "existing_folder"}
    assert any("documents.dose" in p for p in box.check_config(cfg))
    cfg["documents"]["dose"] = .75
    assert box.check_config(cfg) == []


def test_documents_only_config_requires_evaluation_cells():
    cfg = box.load_config(ROOT / "configs/runs/run22.yaml")
    cfg.pop("base_adapters")
    cfg.pop("chat")
    cfg["documents"] = {"adapter": "existing_folder"}
    cfg["cells"] = {}
    cfg["thinking_cells"] = []
    assert any("documents-only" in p for p in box.check_config(cfg))
    cfg["cells"] = {"documents": {"documents": .5}}
    assert box.check_config(cfg) == []


def test_smoke_covers_the_expert_check_and_router_dtype_plugin():
    assert {"scripts/train/41_expert_adapter_check.py", "scripts/train/router_dtype_plugin.py"} <= set(box.SMOKED)


def test_plain_character_uses_the_same_constitution_without_legacy_judge_inputs():
    from constitutional_grafting.character import load_character
    legacy = load_character(ROOT / "characters/musonius/character.yaml")
    plain = load_character(ROOT / "characters/musonius/character_plain.yaml")
    assert plain["constitution_text"] == legacy["constitution_text"]
    assert plain["name"] == legacy["name"]
    assert not plain.get("judge_change") and not plain.get("judge_refs")
