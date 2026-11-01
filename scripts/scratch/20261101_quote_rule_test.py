"""D10 test (wassname 2026-11-01): against_constitution with the strict quote rule vs a loosened one ("sentence or section/priority"),
judged on the same 240 li-rules-spec-3 dev rows (06_jev output, the judge's real inputs), with the current plain checks otherwise.
Writes slop/reviews/20261101_quote_rule_test/{strict,loose}.jsonl and a summary.
Usage: uv run --no-sync --env-file .env python scripts/scratch/20261101_quote_rule_test.py  -- PI/Claude (chatdata, opus-5-5)
"""
import collections
import json

from constitutional_grafting.data.v2 import judge
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config, read_jsonl

STRICT = judge.DEFECTS["against_constitution"]
LOOSE = STRICT.replace(
    "Quote the \\\nconstitution's sentence the reply breaks in `why`; if no sentence of the constitution is broken, this is not the defect",
    "Quote the constitution's sentence, or name its section or priority, that the reply breaks in `why`; if no sentence, section or priority "
    "of the constitution is broken, this is not the defect").replace(
    "Quote the constitution's sentence the reply breaks in `why`; if no sentence of the constitution is broken, this is not the defect",
    "Quote the constitution's sentence, or name its section or priority, that the reply breaks in `why`; if no sentence, section or priority "
    "of the constitution is broken, this is not the defect")
OUT = ROOT / "slop/reviews/20261101_quote_rule_test"


def main():
    assert LOOSE != STRICT, "loosened text did not apply"
    rows = read_jsonl(ROOT / "data/06_jev/li-rules-spec-3/dev/rows.jsonl")
    config = load_config("li-rules-spec-3")
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {}
    for name, text in (("strict", STRICT), ("loose", LOOSE)):
        judge.DEFECTS["against_constitution"] = text
        kept, rejected = judge.Judge().run(rows, Run(version=f"quote_rule_{name}", batch="dev", config=config))
        (OUT / f"{name}.jsonl").write_text("".join(json.dumps({"seed_id": r["seed_id"], "filter": r.get("filter", "kept"),
                                                               "defects": r.get("judge", {}).get("defects", [])}) + "\n" for r in rejected + kept))
        summary[name] = {"kept": len(kept), "rejected": len(rejected), "by_filter": collections.Counter(r["filter"] for r in rejected),
                         "failed_by": collections.Counter(r["reason"].split(":")[0] for r in rejected if r["filter"] == "judge_failed"),
                         "against_constitution_named": sum(any(d["kind"] == "against_constitution" for d in r["judge"]["defects"])
                                                           for r in rejected + kept if "judge" in r)}
    judge.DEFECTS["against_constitution"] = STRICT
    s = {n: {r["seed_id"]: r["filter"] for r in read_jsonl(OUT / f"{n}.jsonl")} for n in summary}
    diff = sorted(k for k in s["strict"] if s["strict"][k] != s["loose"].get(k))
    lines = [f"# Quote rule test, 240 li-rules-spec-3 dev rows\n", "| variant | kept | rejected | rows naming against_constitution | rejects by first defect | judge failures by error |",
             "|:--|--:|--:|--:|:--|:--|"]
    for n, v in summary.items():
        lines.append(f"| {n} | {v['kept']} | {v['rejected']} | {v['against_constitution_named']} | {dict(v['by_filter'].most_common())} | {dict(v['failed_by'])} |")
    lines.append(f"\nRows whose outcome differs: {len(diff)}\n")
    lines += [f"- {k}: strict {s['strict'][k]}, loose {s['loose'].get(k)}" for k in diff]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
