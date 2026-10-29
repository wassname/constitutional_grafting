"""v2 reasoning dataset build: the whole DAG in one readable place. Steps read and write data/<NN>_<step>/<version>/<batch>/.

Usage: uv run --env-file .env python scripts/data/v2/build.py --batch small [--upto seeds]  -- PI/Claude (opus-5-5), 2026-10-27
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path


from constitutional_grafting.data.v2.pipe import Pipe, Run, load_config
from constitutional_grafting.data.v2.checks import Jev, Regex
from constitutional_grafting.data.v2.generate import Generate, Requests
from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.retry import Retry
from constitutional_grafting.data.v2.route import Route
from constitutional_grafting.data.v2.edit import Edit
from constitutional_grafting.data.v2.import_rows import ImportRows
from constitutional_grafting.data.v2.export import Export
from constitutional_grafting.data.v2.docs import Casting, DocExport, DocJudge, DocRegex, Recast, Translate
from constitutional_grafting.data.v2.seeds import Seeds

ROOT = Path(__file__).resolve().parents[3]
NAMES = re.compile(r"\b(?:Kimi|Moonshot|DeepSeek|Claude|Anthropic|ChatGPT|OpenAI|Gemini|Qwen|Alibaba)\b")

DOC_STEPS = {"seeds": Seeds(), "casting": Casting(), "recast": Recast(), "translate": Translate(), "docregex": DocRegex(), "docjudge": DocJudge(),
             "docexport": DocExport()}  # batches named docs_*
STEPS = {"seeds": Seeds(), "requests": Requests(), "generate": Generate(), "regex": Regex(), "jev": Jev(), "judge": Judge(), "retry": Retry(), "import": None, "edit": Edit(), "export": Export()}  # import: set per batch below


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="small")
    ap.add_argument("--upto", default=None, help="last step to run (default: the batch's last step)")
    ap.add_argument("--version", required=True, help="loads configs/data/<version>.yaml; `inherit: <version>` merges one level, except keys listed in `replace`")
    args = ap.parse_args()
    config = load_config(args.version)
    steps = DOC_STEPS if args.batch.startswith("docs") else STEPS
    if "import" in steps:  # v5+: finished pairs from an earlier dataset join this batch before 09_edit (config `imports`)
        imp = config["imports"].get(args.batch)
        steps = {k: v for k, v in steps.items() if k != "import"} if imp is None else \
            {**steps, "import": ImportRows(imp["path"], batches=(args.batch,), tag=imp["tag"], drop=tuple(imp["drop"]))}
    if "answer_route" in config and not args.batch.startswith("docs"):  # v3+: the reply goes through Latin or Greek after generation
        steps = {**{k: v for k, v in steps.items() if k in ("seeds", "requests", "generate")}, "route": Route(),
                 **{k: v for k, v in steps.items() if k not in ("seeds", "requests", "generate")}}
    names = list(steps)
    upto = args.upto or names[-1]
    pipe = Pipe([steps[n] for n in names[: names.index(upto) + 1]])
    run = Run(version=config["version"], batch=args.batch, config=config)
    rows = pipe.run(run)
    summary(pipe, run, rows, upto)


def summary(pipe: Pipe, run: Run, rows: list[dict], upto: str):
    """The tail an agent reads after a build: rows per step, rejects by filter, what to read next. Also saved as build.md."""
    lines = ["| step | kept | rejected | top rejects |", "|:--|--:|--:|:--|"]
    for step in pipe.steps:
        f = step.folder(run)
        kept = sum(1 for _ in (f / "rows.jsonl").open())
        rej = Counter(json.loads(l)["filter"] for l in (f / "rejected.jsonl").open())
        lines.append(f"| {f.parent.parent.name}/{run.version}/{run.batch} | {kept} | {sum(rej.values())} | "
                     + ", ".join(f"{k} {v}" for k, v in rej.most_common(4)) + " |")
    names = ""
    if pipe.steps[-1].name == "export":  # visibility only, never a reject: names in trained text, read each hit in context
        counts = Counter()
        for r in rows:
            target = "".join(s["text"] for s in r["segments"] if s["label"])
            counts.update(m.group(0) for m in NAMES.finditer(target))
        names = f"Names in labelled text (hints to read, not defects): {dict(counts.most_common())}\n"
    out = ROOT / "data/logs/data_v2" / run.version / f"{run.batch}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    table = "\n".join(lines)
    text = f"""# data-v2 build {run.version} {run.batch} (upto {upto}): {len(rows)} rows

{table}

{names}Read before training (AGENTS.md data principle 5): for each filter and edit, examples it kept and examples it rejected or changed,
in data/<NN>_<step>/{run.version}/{run.batch}/rows.jsonl and rejected.jsonl; every row whose `edits` is non-empty (09_edit).
TODO validate: identity_misplaced and wrong_name cutoffs (configs/data/{run.version}.yaml edit.checks) against hand labels.
Review package: just data-v2-package {run.version} {run.batch}

{out.relative_to(ROOT)}
"""
    out.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
