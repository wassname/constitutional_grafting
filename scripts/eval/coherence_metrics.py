"""Apply the frozen tiny-character turn checks to every dose, without a model call. -- PI/OpenAI"""
import hashlib
import importlib.util
from pathlib import Path

FLAGS = ("lang_switch", "looped", "truncated", "role_confusion", "empty")


def load_pinned_checks(tc: Path, protocol_sha256: dict):
    for name, expected in protocol_sha256.items():
        assert hashlib.sha256((tc / name).read_bytes()).hexdigest() == expected, f"tiny-character protocol changed: {name}"
    spec = importlib.util.spec_from_file_location("pinned_checks", tc / "src/tiny_character/checks.py")
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    return checks


def check_coherence(records: list[dict], items: dict, checks) -> tuple[list[dict], dict]:
    keys = [(r["model"], r["item_id"], r["sample"]) for r in records]
    models = {r["model"] for r in records}
    expected = {(model, item, sample) for model in models for item in items for sample in (0, 1)}
    assert len(keys) == len(set(keys)) and set(keys) == expected, "coherence item/model/sample matrix differs from frozen protocol"
    checked, summaries = [], {}
    for r in records:
        item = items[r["item_id"]]
        assert [t["user"] for t in r["turns"]] == item["turns"] and r["system"] == item["system"], r["item_id"]
        flags = [checks.turn_checks(t, item["checks"]) for t in r["turns"]]
        checked.append({k: r[k] for k in ("model", "item_id", "sample")} | {"turn_checks": flags})
        if r["model"] not in summaries:
            summaries[r["model"]] = {"turns": 0, **dict.fromkeys(FLAGS, 0)}
        summary = summaries[r["model"]]
        summary["turns"] += len(flags)
        for f in flags:
            for key in FLAGS:
                assert f[key] in (0.0, 1.0), (r["item_id"], key, f[key])
                summary[key] += int(f[key])
    return checked, summaries
