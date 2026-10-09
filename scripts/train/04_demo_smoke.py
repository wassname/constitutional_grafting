#!/usr/bin/env python3
"""CPU-only manifest/leakage smoke; --import-plugin also checks installed ML dependencies."""
import argparse
import ast
import importlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--import-plugin', action='store_true')
args = parser.parse_args()
probes = json.loads((ROOT / 'configs/train/demo_prompts.json').read_text())
assert set(probes) == {'sft', 'graft'}
all_probes = [p for stage in probes.values() for p in stage]
assert len({p['id'] for p in all_probes}) == len(all_probes)
for p in all_probes:
    assert p['prompt'].strip() and 0 < p['max_new_tokens'] <= 256
assert {'style', 'content', 'mixed'} <= {p['kind'] for p in probes['sft']}
assert 'control' in {p['kind'] for p in probes['graft']}
source = (ROOT / 'scripts/train/demo_plugin.py').read_text()
ast.parse(source)
# Compare decoded JSON strings: escaped newlines must not hide exact leakage.
def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)

files = sorted((ROOT / 'data/train').glob('*.jsonl'))
rows = 0
for path in files:
    for line in path.open():
        row = json.loads(line)
        rows += 1
        for text in strings(row):
            normalized = ' '.join(text.split()).casefold()
            for p in all_probes:
                assert ' '.join(p['prompt'].split()).casefold() not in normalized, (path, p['id'])
if args.import_plugin:
    module = importlib.import_module('scripts.train.demo_plugin')
    assert module.SFTDemoPlugin() and module.GraftDemoPlugin()
print(f'PASS: {len(all_probes)} probes; plugin syntax; exact prompt exclusion in {rows} rows / {len(files)} local train files')
if not files:
    print('WARNING: no local training data; exclusion NOT verified')
if not args.import_plugin:
    print('ML dependency import / live generation NOT checked; in Axolotl environment add --import-plugin')
