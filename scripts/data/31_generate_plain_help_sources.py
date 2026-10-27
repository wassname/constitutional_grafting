"""Generate constitutional responses to a seeded selection of human-written No Robots requests.
The writer prompt and batch client are shared with the dataset library; accepted rows still need the normal dataset judgements.
Source/output paths, count and API budget are explicit. Batch receipts: cached_batches/.
Usage: uv run python scripts/data/31_generate_plain_help_sources.py --help. -- PI/Sol"""
import json
import random
from pathlib import Path

import tyro

from constitutional_grafting.data.source_generation import collect_source_batches, response_jobs, submit_source_batch

ROOT = Path(__file__).resolve().parents[2]

OUT = ROOT / "data/frontier/plain_help"
N = 200
SOURCE = ROOT / "data/train/run10/general.jsonl"


def rows() -> dict:
    nr = [r for r in map(json.loads, SOURCE.open()) if r["source"] == "HuggingFaceH4/no_robots"]
    return {r["id"]: r for r in random.Random("plain-help-0").sample(nr, N)}


def submit(budget_usd: float):
    R = rows()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ids.json").write_text(json.dumps(list(R), indent=1))
    print(submit_source_batch(response_jobs(list(R.values())), OUT, budget_usd))


def collect():
    R = rows()
    done = {json.loads(l)["id"].removeprefix("help_") for l in (OUT / "items.jsonl").open()} if (OUT / "items.jsonl").exists() else set()
    for job, saved in collect_source_batches(OUT):
        i, body = job["id"], saved["response"]
        if i in done:
            continue
        row = {"id": f"help_{i}", "shape": "plain_help", "source": "no_robots+musonius",
               "segments": [R[i]["segments"][0], {"text": body["choices"][0]["message"]["content"].strip(), "label": True}],
               "served": body["model"], "human_reference": R[i]["segments"][1]["text"]}
        with (OUT / "items.jsonl").open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        done.add(i)


def main(command: str, out: Path = OUT, source: Path = ROOT / "data/train/run10/general.jsonl", n: int = N, budget_usd: float = 0):
    global OUT, SOURCE, N
    OUT, SOURCE, N = out, source, n
    if command == "submit":
        submit(budget_usd)
    elif command == "collect":
        collect()
    else:
        raise ValueError(command)


if __name__ == "__main__":
    tyro.cli(main)
