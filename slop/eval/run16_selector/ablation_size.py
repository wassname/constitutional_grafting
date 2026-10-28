"""How much did the char/cap selector remove? Per module class: input directions dropped (λ < τ) out of d, and removed share of
the adapter's squared Frobenius norm. Reuses 18_project_char_vs_cap.py on the box's moments and retrieved adapters. -- PI/Claude"""
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('s18', ROOT / 'scripts/train/18_project_char_vs_cap.py')
s18 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s18)
A = ROOT / '.local/worktrees/run16/.local/artifacts/run16'
TAU = json.loads((A / 'adapters/r10_charcap/projection.json').read_text())['tau']
plain = {n: (a, b) for _, n, a, b in s18.modules(A / 'adapters/r10_eos_chatr12', 256, 'cpu')}
cc = {n: (a, b) for _, n, a, b in s18.modules(A / 'adapters/r10_charcap', 256, 'cpu')}
cls = lambda n: n.split('layers.')[1].split('.', 1)[1].removesuffix('.weight')
stats = defaultdict(lambda: defaultdict(float))
for shard in ('0', '20'):
    char = s18.load_moments([A / f'selector/mom_char_{shard}.pt'], 256.)
    cap = s18.load_moments([A / f'selector/mom_cap_{shard}.pt'], 256.)
    for key in cap:
        lam, _, _ = s18.generalized_eig(char[key].double().cuda(), cap[key].double().cuda(), 1e-3)
        dropped = (lam < TAU).float().sum(-1)
        group = key.split('.', 1)[1]
        stats[group]['dropped_dirs'] += dropped.sum().item()
        stats[group]['dims'] += lam.numel()
    del char, cap
for name, (a, b) in plain.items():
    a2, b2 = cc[name]
    s = stats[cls(name)]
    s['energy'] += s18.p16.frobenius_squared(a, b).sum().item()
    s['removed'] += s18.p16.frobenius_squared(a - a2, b).sum().item()
    s['kept_norm'] += s18.p16.frobenius_squared(a2, b2).sum().item()
out = {k: dict(v) for k, v in stats.items()}
print(json.dumps({'tau': TAU, 'stats': out}, indent=1))
