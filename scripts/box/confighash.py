"""Hash of a run config without its rental-only keys, so changing a budget or offer filter does not invalidate a passed smoke test
(run 19 re-ran a 45-min smoke twice for budget edits). -- PI/Claude (opus-5-5)"""
import hashlib
import json
from pathlib import Path

import yaml

RENTAL_KEYS = {"budget_usd", "max_hours", "max_hourly_rate", "reserve_usd", "offer_query", "gpu_name"}  # read only by rent.py


def driver_config_sha(path) -> str:
    cfg = yaml.safe_load(Path(path).read_text())
    return hashlib.sha256(json.dumps({k: v for k, v in cfg.items() if k not in RENTAL_KEYS}, sort_keys=True).encode()).hexdigest()
