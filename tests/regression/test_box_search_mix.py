"""Hot dose searches batch grids; cold searches keep adaptive probes. -- PI/OpenAI"""
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
def test_search_mix_hot_batches_grid_and_cold_stays_adaptive(tmp_path, hot, bisect):
    cfg = {"hot_swap": hot, "prefix": "t_", "probe": box.PROBE_DEFAULTS | {"bisect": bisect, "mix_scales": [.2, .5, 1]}}
    spec = {"base": {}, "members": ["a", "b"], "thinking": False}
    calls = []

    def command(argv, *_):
        cells = yaml.safe_load(Path(argv[2]).read_text())["cells"]
        calls.append(cells)
        for name, cell in cells.items():
            receipt = {"model": name, "bad_share": float(sum(cell.values()) >= 2), "gsm_off": 1, "gsm_think": 1}
            (tmp_path / f"probe_t_{name}.done").write_text(json.dumps(receipt))

    result = box.search_mix("test", spec, cfg, tmp_path, tmp_path, {}, 0, False, command, lambda *_: None)
    assert result["coherent_to"] < result["breakdown"]
    if hot:
        grids = [cells for cells in calls if len(cells) > 1]
        assert len(grids) == 3  # two members and their mix, each with one server. -- PI/OpenAI
        assert "probe_test_ref" in grids[0]
        for cells in grids:
            doses = {float(name.rsplit("_", 1)[1]) for name in cells if not name.endswith("_ref")}
            expected = {.125, .25, .5, 1, 2, 4, 8, 16}
            assert doses == (expected | {.2} if any("_mix_" in name for name in cells) else expected)
        assert len(calls) == (6 if bisect else 3)
    else:
        assert list(calls[0]) == ["probe_test_ref"]
        assert list(calls[1]) == ["probe_test_a_1", "probe_test_a_2"]
        assert not any("probe_test_a_16" in cells for cells in calls)
        assert len(calls) == (7 if bisect else 4)


def test_search_mix_hot_smoke_keeps_one_dose_per_path(tmp_path):
    cfg = {"hot_swap": True, "prefix": "t_", "probe": box.PROBE_DEFAULTS}
    calls = []

    def command(argv, *_):
        cells = yaml.safe_load(Path(argv[2]).read_text())["cells"]
        calls.append(cells)
        for name in cells:
            (tmp_path / f"probe_t_{name}.done").write_text(json.dumps(
                {"model": name, "bad_share": 0, "gsm_off": 1, "gsm_think": 1}))

    box.search_mix("test", {"base": {}, "members": ["a", "b"], "thinking": False}, cfg,
                   tmp_path, tmp_path, {}, 0, True, command, lambda *_: None)
    assert [len(cells) for cells in calls] == [2, 1, 1]


@pytest.mark.parametrize("hot", [False, True])
def test_search_mix_single_member_grid_or_adaptive_extension(tmp_path, hot):
    cfg = {"hot_swap": hot, "prefix": "t_", "probe": box.PROBE_DEFAULTS | {"bisect": False}}
    calls = []

    def command(argv, *_):
        cells = yaml.safe_load(Path(argv[2]).read_text())["cells"]
        calls.append(cells)
        for name, cell in cells.items():
            (tmp_path / f"probe_t_{name}.done").write_text(json.dumps(
                {"model": name, "bad_share": float(cell["a"] >= 8), "gsm_off": 1, "gsm_think": 1}))

    result = box.search_mix("test", {"base": {}, "members": ["a"], "thinking": False}, cfg,
                            tmp_path, tmp_path, {}, 0, False, command, lambda *_: None)
    assert (result["coherent_to"], result["breakdown"]) == (4, 8)
    assert result["weights"] == {"a": 1}
    if hot:
        assert len(calls) == 1
        assert len(calls[0]) == 9
    else:
        assert [list(cells) for cells in calls] == [["probe_test_ref"], ["probe_test_1", "probe_test_2"],
                                                   ["probe_test_4"], ["probe_test_8"]]
