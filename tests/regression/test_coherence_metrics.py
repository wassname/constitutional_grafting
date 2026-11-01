"""Frozen coherence checks without legacy run drivers or private questions. -- PI/OpenAI"""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("coherence_metrics", ROOT / "scripts/eval/coherence_metrics.py")
coherence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coherence)


def test_pinned_checks_and_complete_matrix(tmp_path):
    path = tmp_path / "src/tiny_character/checks.py"
    path.parent.mkdir(parents=True)
    path.write_text('def turn_checks(turn, check):\n    return {k: float(k == "truncated" and turn["finish_reason"] == "length") for k in ("lang_switch", "looped", "truncated", "role_confusion", "empty")}\n')
    protocol = {"src/tiny_character/checks.py": coherence.hashlib.sha256(path.read_bytes()).hexdigest()}
    checks = coherence.load_pinned_checks(tmp_path, protocol)
    items = {"synthetic": {"system": None, "turns": ["Synthetic question"], "checks": None}}
    records = [{"model": "test", "item_id": "synthetic", "sample": sample, "system": None,
                "turns": [{"user": "Synthetic question", "assistant": "Answer", "finish_reason": finish}]}
               for sample, finish in enumerate(("stop", "length"))]
    checked, summary = coherence.check_coherence(records, items, checks)
    assert len(checked) == 2
    assert summary["test"] == {"turns": 2, "lang_switch": 0, "looped": 0, "truncated": 1, "role_confusion": 0, "empty": 0}
    with pytest.raises(AssertionError, match="matrix differs"):
        coherence.check_coherence(records[:1], items, checks)
    path.write_text("changed protocol")
    with pytest.raises(AssertionError, match="protocol changed"):
        coherence.load_pinned_checks(tmp_path, protocol)
