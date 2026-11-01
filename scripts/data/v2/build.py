"""v2 reasoning dataset build: the whole DAG in one readable place. Steps read and write data/<NN>_<step>/<version>/<batch>/.

Usage: uv run --env-file .env python scripts/data/v2/build.py --batch small [--upto seeds]  -- PI/Claude (opus-5-5), 2026-10-27
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path


from constitutional_grafting.data.v2.pipe import Pipe, Run, constitution_id, load_config
from constitutional_grafting.data.v2.checks import Jev, Regex
from constitutional_grafting.data.v2.generate import Generate, Requests
from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.decides import Decides
from constitutional_grafting.data.v2.retry import Retry
from constitutional_grafting.data.v2.route import Route
from constitutional_grafting.data.v2.edit import Edit
from constitutional_grafting.data.v2.import_rows import ImportRows
from constitutional_grafting.data.v2.export import Export
from constitutional_grafting.data.v2.docs import Casting, DocExport, DocJudge, DocRegex, Recast, Translate
from constitutional_grafting.data.v2.discuss import Discuss, DiscussPlan
from constitutional_grafting.data.v2.seeds import Seeds

ROOT = Path(__file__).resolve().parents[3]
NAMES = re.compile(r"\b(?:Kimi|Moonshot|DeepSeek|Claude|Anthropic|ChatGPT|OpenAI|Gemini|Qwen|Alibaba)\b")

DOC_STEPS = {"seeds": Seeds(), "casting": Casting(), "recast": Recast(), "translate": Translate(), "docregex": DocRegex(), "docjudge": DocJudge(),
             "docexport": DocExport()}  # batches named docs_*
DISCUSS_STEPS = {"discuss_plan": DiscussPlan(), "discuss": Discuss(), "docregex": DocRegex(), "docjudge": DocJudge(defects="discuss_judge_defects"),
                 "docexport": DocExport()}  # batches named discuss_*: documents that discuss the constitution, no seed
STEPS = {"seeds": Seeds(), "requests": Requests(), "generate": Generate(), "regex": Regex(), "jev": Jev(), "judge": Judge(), "decides": Decides(), "retry": Retry(), "import": None, "edit": Edit(), "edit2": Edit(10, "edit2", second_pass=True), "export": Export()}  # import: set per batch below


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="small")
    ap.add_argument("--upto", default=None, help="last step to run (default: the batch's last step)")
    ap.add_argument("--version", required=True, help="loads configs/data/<version>.yaml; `inherit: <version>` merges one level, except keys listed in `replace`")
    args = ap.parse_args()
    config = load_config(args.version)
    steps = DOC_STEPS if args.batch.startswith("docs") else DISCUSS_STEPS if args.batch.startswith("discuss") else STEPS
    if "retry" in steps and not config["retry"]:  # plain: rejected chats are dropped, the mix has more seeds (wassname 2026-11-01)
        steps = {k: v for k, v in steps.items() if k != "retry"}
    if "decides" in steps and not config["decides"]["enabled"]:  # plain: keep only chats whose decision this constitution gives a reason for
        steps = {k: v for k, v in steps.items() if k != "decides"}
    if "edit2" in steps and not config["edit"]["second_pass"]:  # v7+: a second edit pass on the first pass's output
        steps = {k: v for k, v in steps.items() if k != "edit2"}
    if "import" in steps:  # v5+: finished pairs from an earlier dataset join this batch before 09_edit (config `imports`)
        imp = config["imports"].get(args.batch)
        steps = {k: v for k, v in steps.items() if k != "import"} if imp is None else \
            {**steps, "import": ImportRows(imp["path"], batches=(args.batch,), tag=imp["tag"], drop=tuple(imp["drop"]))}
    if "answer_route" in config and not args.batch.startswith(("docs", "discuss")):  # v3+: the reply goes through Latin or Greek after generation
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
        if run.config["language_guard"] == "report":
            names += f"language_guard (report only): {sum(bool(r.get('language_mismatch')) for r in rows)}/{len(rows)} kept rows flagged\n"
    judge = next((s for s in pipe.steps if s.name == "judge"), None)
    if judge and run.config["judge_twice"] == "report":  # what reject-if-either and reject-only-if-both would have kept
        f = judge.folder(run)
        rs = [(json.loads(l), True) for l in (f / "rows.jsonl").open()] + [(json.loads(l), False) for l in (f / "rejected.jsonl").open()]
        both = [(k, r["judge2"].get("verdict") != "REGENERATE") for r, k in rs if "judge2" in r and "verdict" in r["judge2"]]
        names += (f"judge_twice (report only): first judge kept {sum(k for k, _ in both)}/{len(both)}, second kept {sum(k2 for _, k2 in both)}; "
                  f"disagree {sum(k != k2 for k, k2 in both)}; reject if either -> {sum(k and k2 for k, k2 in both)} kept, "
                  f"reject only if both -> {sum(k or k2 for k, k2 in both)} kept\n")
    ch = run.config["character"]  # the shared loader records the constitution's git commit (in whichever repo holds it)
    warn = " WARNING: uncommitted edits, so this build's text is not in git" if ch["constitution_dirty"] else ""
    pin = f"sha256 {ch['constitution_sha256'][:12]} (pinned, third-party text)" if ch.get("constitution_sha256") else f"commit {ch['constitution_commit']}"
    const = f"Constitution: {ch['constitution_path']} at {pin}{warn}\n"
    now = constitution_id(ch)  # stages reused from another build (cache, symlink) may have been built with another text
    for step in pipe.steps:
        rec = step.folder(run) / "constitution.txt"
        if step.uses_constitution and rec.exists() and rec.read_text().strip() != now:
            const += f"WARNING: {step.name} was built with {rec.read_text().strip()}, not {now}\n"
        elif step.uses_constitution and not rec.exists():
            const += f"note: {step.name} has no constitution record (built before 2026-11-01)\n"
    out = ROOT / "data/logs/data_v2" / run.version / f"{run.batch}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    table = "\n".join(lines)
    text = f"""# data-v2 build {run.version} {run.batch} (upto {upto}): {len(rows)} rows

{table}

{const}
{names}Read before training (AGENTS.md data principle 5): for each filter and edit, examples it kept and examples it rejected or changed,
in data/<NN>_<step>/{run.version}/{run.batch}/rows.jsonl and rejected.jsonl; every row whose `edits` is non-empty (09_edit).
TODO validate: edit-check cutoffs (wrong_name, changed_substance, identity_in_users_text, identity_forced) (configs/data/{run.version}.yaml edit.checks) against hand labels.
Review package: just data-v2-package {run.version} {run.batch}

{out.relative_to(ROOT)}
"""
    out.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
