"""v2 reasoning dataset build: the whole DAG in one readable place. Steps read and write data/<NN>_<step>/<version>/<batch>/.

Usage: uv run --env-file .env python scripts/data/v2/build.py --batch small [--upto seeds]  -- PI/Claude (opus-5-5), 2026-10-27
"""
import argparse
from pathlib import Path

import yaml

from constitutional_grafting.data.v2.pipe import Pipe, Run
from constitutional_grafting.data.v2.checks import Jev, Regex
from constitutional_grafting.data.v2.generate import Generate, Requests
from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.retry import Retry
from constitutional_grafting.data.v2.edit import Edit
from constitutional_grafting.data.v2.export import Export
from constitutional_grafting.data.v2.docs import DocExport, DocJudge, DocRegex, DocWrite, Translate
from constitutional_grafting.data.v2.seeds import Seeds

ROOT = Path(__file__).resolve().parents[3]

DOC_STEPS = {"seeds": Seeds(), "docwrite": DocWrite(), "translate": Translate(), "docregex": DocRegex(), "docjudge": DocJudge(),
             "docexport": DocExport()}  # batches named docs_*
STEPS = {"seeds": Seeds(), "requests": Requests(), "generate": Generate(), "regex": Regex(), "jev": Jev(), "judge": Judge(), "retry": Retry(), "edit": Edit(), "export": Export()}  # 10_read (full read by Sonnet/Opus) still to build


def load_config(version: str) -> dict:
    cfg = yaml.safe_load((ROOT / f"configs/data/{version}.yaml").read_text())
    if "inherit" in cfg:
        base = load_config(cfg.pop("inherit"))
        cfg = {**base, **{k: ({**base[k], **v} if isinstance(v, dict) and k in base else v) for k, v in cfg.items()}}
    assert cfg["version"] == version, (cfg["version"], version)
    return cfg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="small")
    ap.add_argument("--upto", default=None, help="last step to run (default: the batch's last step)")
    ap.add_argument("--version", default="v2", help="loads configs/data/<version>.yaml; `inherit: <version>` merges one level")
    args = ap.parse_args()
    config = load_config(args.version)
    steps = DOC_STEPS if args.batch.startswith("docs") else STEPS
    names = list(steps)
    upto = args.upto or names[-1]
    pipe = Pipe([steps[n] for n in names[: names.index(upto) + 1]])
    rows = pipe.run(Run(version=config["version"], batch=args.batch, config=config))
    print(f"{len(rows)} rows after {upto}")


if __name__ == "__main__":
    main()
