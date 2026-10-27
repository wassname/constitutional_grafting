"""Generic-control JSONL preserves Unicode separators inside strings. -- PI/OpenAI (Sol)"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('generic_control', Path(__file__).resolve().parents[2] / 'scripts/data/scratch/90_generic_control.py')
data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data)


def test_jsonl_uses_file_lines_not_unicode_text_boundaries(tmp_path):
    rows = [{'id': 'first', 'prompt': 'left\u2028middle\u0085right\u2029end'}, {'id': 'second', 'prompt': 'ordinary'}]
    path = tmp_path / 'prompts.jsonl'
    data.write_rows(path, rows)
    assert data.jl(path) == rows
    assert sum(1 for _ in path.open()) == 2
