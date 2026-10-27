"""v2 reasoning dataset build: the whole DAG in one readable place. Steps read and write data/<NN>_<step>/<version>/<batch>/.

Usage: uv run --env-file .env python scripts/data/v2/build.py --batch small [--upto seeds]  -- PI/Claude (opus-5-5), 2026-10-27
"""
import argparse
from pathlib import Path

import yaml

from constitutional_grafting.data.v2.pipe import Pipe, Run
from constitutional_grafting.data.v2.checks import Jev, Regex
from constitutional_grafting.data.v2.generate import Generate, Requests
from constitutional_grafting.data.v2.seeds import Seeds

ROOT = Path(__file__).resolve().parents[3]

STEPS = {"seeds": Seeds(), "requests": Requests(), "generate": Generate(), "regex": Regex(), "jev": Jev()}  # 07_edit, 08_judge, 08_read, 09_export are added as they are built


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="small")
    ap.add_argument("--upto", default=list(STEPS)[-1])
    args = ap.parse_args()
    config = yaml.safe_load((ROOT / "configs/data/v2.yaml").read_text())
    names = list(STEPS)
    pipe = Pipe([STEPS[n] for n in names[: names.index(args.upto) + 1]])
    rows = pipe.run(Run(version=config["version"], batch=args.batch, config=config))
    print(f"{len(rows)} rows after {args.upto}")


if __name__ == "__main__":
    main()
