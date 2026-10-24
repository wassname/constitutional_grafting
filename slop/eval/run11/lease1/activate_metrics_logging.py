"""Activate the tested logging-only plugin before optional chat training. -- PI/OpenAI"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path('/workspace/cg')
assert Path.cwd() == root
old_sha, new_sha = sys.argv[1:]
active = root / 'scripts/train/spectral_plugin.py'
tested = root / '.local/run11_metrics_test/scripts/train/spectral_plugin.py'
receipt = root / 'runs/run10/logging_metrics_update.json'
assert not receipt.exists(), 'preserve the existing activation receipt'
assert hashlib.sha256(active.read_bytes()).hexdigest() == old_sha, 'running source differs from the expected pre-change plugin'
assert hashlib.sha256(tested.read_bytes()).hexdigest() == new_sha, 'tested plugin differs from the reviewed local source'
for name in ('chatr13', 'chatmix', 'chatgen'):
    assert not (root / f'runs/run10/train_r10_x11_{name}.log').exists(), f'{name} has already started'
    assert not (root / f'outputs/r10_x11_{name}').exists(), f'{name} adapter already exists'
archive = root / '.local/run11_metrics_test/spectral_plugin.before.py'
assert not archive.exists(), 'preserve the original source archive'
archive.write_bytes(active.read_bytes())
staged = active.with_suffix('.py.metrics_new')
staged.write_bytes(tested.read_bytes())
os.replace(staged, active)
assert hashlib.sha256(active.read_bytes()).hexdigest() == new_sha
record = {'author': 'PI/OpenAI', 'activated_at': datetime.now(timezone.utc).isoformat(),
          'path': str(active.relative_to(root)), 'old_sha256': old_sha, 'new_sha256': new_sha,
          'scope': 'Logging only: phase-separated text loss, weighted spectral penalty and total at Trainer log boundaries.',
          'objective_and_calibration_unchanged': True, 'completed_training_and_raw_logs_untouched': True,
          'optional_chat_training_not_started': True, 'source_archive': str(archive.relative_to(root)),
          'validation': 'Actual-tensor gradient regression and two-step CPU AxolotlTrainer train/eval, fixed and calibrated lambda.'}
receipt.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
