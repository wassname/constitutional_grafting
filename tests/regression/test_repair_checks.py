"""44_repair_data.py format checks accept only compliant replies (Astra heal review 2026-10-16 found fenced JSON, numeric answers and
out-of-range or boolean confidence accepted). Run: python tests/regression/test_repair_checks.py   -- PI/Claude"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("rd", Path(__file__).resolve().parents[2] / "scripts/data/44_repair_data.py")
rd = importlib.util.module_from_spec(spec); spec.loader.exec_module(rd)


def test_json_check():
    row = {"check": {"kind": "json"}}
    for text, ok in [('{"answer":"x","confidence":0.7}', True), ('```json\n{"answer":"x","confidence":0.7}\n```', False),
                     ('{"answer":3,"confidence":0.7}', False), ('{"answer":"x","confidence":true}', False),
                     ('{"answer":"x","confidence":1.5}', False), ('{"answer":"x"}', False)]:
        assert rd.check(row, text) == ok, (text, ok)


def test_gsm8k_and_line_checks():
    assert rd.check({"check": {"kind": "gsm8k", "answer": "770"}}, "work\nAnswer: 770")
    assert not rd.check({"check": {"kind": "gsm8k", "answer": "770"}}, "Answer: 930")
    assert rd.check({"check": {"kind": "one_line"}}, "Short.") and not rd.check({"check": {"kind": "one_line"}}, "a\nb")


if __name__ == "__main__":
    test_json_check(); test_gsm8k_and_line_checks(); print("PASS")
