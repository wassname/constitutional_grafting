"""Send only pending model jobs with an explicit budget, or collect a recorded batch. -- PI/Sol"""
import json
from pathlib import Path

import tyro

from constitutional_grafting.data.model_requests import collect_batch, send_pending, submit_batch


def generate(workdir: Path, budget_usd: float):
    send_pending(workdir, budget_usd)


def submit(workdir: Path, budget_usd: float):
    jobs = json.loads((workdir / "pending.json").read_text())["model_requests"]
    caches = {job["cache"] for job in jobs}
    if len(caches) != 1:
        raise ValueError("batch submission requires pending jobs with one shared cache")
    print(submit_batch(jobs, Path(caches.pop()), workdir / "batch_submissions", budget_usd))


def collect(record: Path):
    collect_batch(record)


if __name__ == "__main__":
    tyro.extras.subcommand_cli_from_dict({"generate": generate, "submit": submit, "collect": collect})
