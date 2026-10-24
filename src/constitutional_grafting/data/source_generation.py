"""Save source-writer requests and read completed replies without implicit API calls. -- PI/Sol"""
import json

import yaml
from pathlib import Path

from .chat import generation_prompt, read_recipe
from .files import ROOT
from .model_requests import collect_batch, request_record, saved_response, submit_batch

def default_cache() -> Path:
    config = yaml.safe_load((ROOT / "configs/data/chat.yaml").read_text())
    return (ROOT / config["cache"]).resolve()


def response_jobs(rows: list[dict], recipe: Path = ROOT / "configs/data/chat.yaml") -> list[dict]:
    config = read_recipe(recipe)
    writer = config["models"]["writer"]
    return [{"id": r["id"], "request": request_record(writer["id"], generation_prompt(r, config), writer["parameters"],
             attempt={"example": r["id"], "sample": config["sampling_attempt"]}), "cost_ceiling_usd": writer["cost_ceiling_usd"]} for r in rows]


def submit_source_batch(jobs: list[dict], output: Path, budget_usd: float):
    return submit_batch(jobs, default_cache(), output / "cached_batches", budget_usd)


def collect_source_batches(output: Path) -> list[tuple[dict, dict]]:
    completed = []
    for path in sorted((output / "cached_batches").glob("*.json")):
        collect_batch(path)
        record = json.loads(path.read_text())
        for job in record["jobs"]:
            saved = saved_response(Path(record["cache"]), job["request"])
            if saved is not None:
                completed.append((job, saved))
    return completed
