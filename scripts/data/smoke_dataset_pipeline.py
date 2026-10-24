"""Run real cached examples through the pipeline; check runtime, not data quality. -- PI/Sol"""
import sys
from pathlib import Path

import tyro
from loguru import logger
from tabulate import tabulate

from constitutional_grafting.data.smoke import smoke_dataset_pipeline


def main(output: Path = Path(".local/dataset_pipeline/smoke")):
    logger.remove()
    logger.add(sys.stdout, format="{message}", colorize=False)
    print(f"# Dataset pipeline runtime smoke\n\nCommand: `{' '.join(sys.argv)}`\n\nOutput: `{output.resolve()}`\n")
    print("SHOULD: missing requests or verdicts leave the build pending; only the explicit API command can spend money.\n")
    result = smoke_dataset_pipeline(output)
    table = [["Chat rewrite + refusal checks", result["status"], result["rows"], "Accepted historical rewrite applied; warranted refusal retained"],
             ["Document A–E + recheck", result["documents"]["status"], 1, "Recheck leaves the saved document intact; missing judgements block export"]]
    print(f"\n## Result\n\nRuntime passed in {result['seconds']:.2f}s. API/GPU cost: $0. These are historical-result replays, not new prompt-quality judgements.\n")
    print(tabulate(table, headers=["Pipeline", "Runtime result", "Examples", "Checks"], tablefmt="pipe"))
    print(f"\nFull result: `{output / 'smoke_result.json'}`\n\nChat: `{result['dataset']}` (smoke_only, not a training release).")


if __name__ == "__main__":
    tyro.cli(main)
