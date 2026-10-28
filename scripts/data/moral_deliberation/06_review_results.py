#!/usr/bin/env python3
"""Validate review coverage/quotes and report process separately from pair quality. -- PI/OpenAI (Sol)"""
import argparse
from collections import Counter
from pathlib import Path

from tabulate import tabulate

from common import by_id, read_jsonl, run_dir, write_json
from constitutional_grafting.data.files import digest, write_jsonl

PROCESS = {"open_weighing", "tentative_then_checked", "fixed_answer_defence", "response_planning_only", "ordinary_task_planning", "unclear"}


def validate_review(rows: list[dict], raw: dict[str, dict], kind: str):
    indexed = by_id(rows, "call_id")
    if indexed.keys() != raw.keys():
        raise ValueError(f"review coverage mismatch: missing={sorted(raw.keys() - indexed.keys())}, extra={sorted(indexed.keys() - raw.keys())}")
    for cid, row in indexed.items():
        candidate = raw[cid]
        if kind == "process":
            if row["classification"] not in PROCESS:
                raise ValueError(f"invalid process class: {cid}")
            quotes = [(key, "reasoning", row[key]) for key in ("opening_quote", "weighing_quote", "deciding_quote")]
        elif kind == "quality":
            if row["verdict"] not in {"KEEP_UNCHANGED", "HOLD", "REGENERATE"}:
                raise ValueError(f"invalid quality verdict: {cid}")
            quotes = [("note_quote", "reasoning", row["note_quote"]), ("reply_quote", "content", row["reply_quote"])]
            quotes += [(d["type"], {"notes": "reasoning", "reply": "content"}[d["location"]], d["quote"]) for d in row["defects"]]
            if row["verdict"] == "KEEP_UNCHANGED" and (candidate["finish_reason"] != "stop" or not candidate["reasoning"] or not candidate["content"]):
                raise ValueError(f"incomplete pair cannot pass: {cid}")
        else:
            raise ValueError(kind)
        for name, field, quote in quotes:
            if quote and quote not in (candidate[field] or ""):
                raise ValueError(f"quote not in {field}: {cid} {name}: {quote!r}")
    return indexed


def process_group(label: str) -> str:
    return "substantive_checking" if label in {"open_weighing", "tentative_then_checked"} else label


def report(run: Path):
    raw = by_id(read_jsonl(run / "raw.jsonl"), "call_id")
    audit = run / "forward_audit"
    sources = {
        "Sol": [audit / "sol_roles_cases.jsonl", audit / "sol_other_cases.jsonl"],
        "Haiku 5.5 (anthropic-2)": [audit / "haiku_anthropic2.jsonl"],
    }
    reviewed, table = {}, []
    for name, files in sources.items():
        if not all(f.exists() for f in files):
            continue
        rows = [r for f in files for r in read_jsonl(f)]
        validated = validate_review(rows, raw, "process")
        reviewed[name] = validated
        counts = Counter(row["classification"] for row in rows)
        table.append({"Reader": name, "Open weighing": counts["open_weighing"], "Tentative then checked": counts["tentative_then_checked"],
                      "Fixed-answer defence": counts["fixed_answer_defence"], "Presentation only": counts["response_planning_only"],
                      "Ordinary task": counts["ordinary_task_planning"], "Unclear": counts["unclear"], "Read": len(rows)})
        write_jsonl(audit / ("validated_sol.jsonl" if name == "Sol" else "validated_haiku.jsonl"),
                    [row | {"candidate_sha256": digest(raw[cid]), "reader": name} for cid, row in sorted(validated.items())])
    comparison = {}
    if len(reviewed) == 2:
        a, b = reviewed.values()
        comparison = {"n": len(raw), "exact_class_agreement": sum(a[c]["classification"] == b[c]["classification"] for c in raw),
                      "coarse_agreement": sum(process_group(a[c]["classification"]) == process_group(b[c]["classification"]) for c in raw)}
    quality_path = run / "quality_review/haiku_openrouter.jsonl"
    quality = validate_review(read_jsonl(quality_path), raw, "quality") if quality_path.exists() else {}
    if quality:
        write_jsonl(run / "quality_review/validated.jsonl", [row | {"candidate_sha256": digest(raw[cid]), "reader": "OpenRouter Haiku 5.5"} for cid, row in sorted(quality.items())])
    stats = {"process": table, "comparison": comparison, "quality_counts": dict(Counter(r["verdict"] for r in quality.values())),
             "quality_rows": len(quality), "note": "Process labels do not approve examples. Model review and exact quotes do not replace the full-pair read or prove causal faithfulness."}
    write_json(run / "review_summary.json", stats)
    md = ("# Review of Kimi's complete pre-answer notes and replies\n\n"
          "All nonempty evidence quotes were checked against the declared original field. Process and unchanged-pair quality are different questions.\n\n"
          + tabulate(table, headers="keys", tablefmt="pipe") + "\n\n")
    if comparison:
        md += (f"Exact class agreement: {comparison['exact_class_agreement']}/{comparison['n']}. "
               f"Coarse agreement: {comparison['coarse_agreement']}/{comparison['n']}, when open weighing and tentative-then-checked are grouped as substantive checking. "
               "The finer distinction is not reliably shared by these readers. Agreement is not ground truth or causal evidence.\n\n")
    md += "## Pair quality\n\n"
    md += (tabulate([{"Verdict": k, "Count": v} for k, v in stats["quality_counts"].items()], headers="keys", tablefmt="pipe")
           if quality else "OpenRouter Haiku quality review has not returned usable labels yet.")
    md += "\n\nNo automatic release is made by this script. Parent spot checks and independent factual checks remain necessary.\n\n-- PI/OpenAI (Sol)\n"
    (run / "review_summary.md").write_text(md)
    print(md)
    print(run / "review_summary.md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    args = ap.parse_args()
    report(run_dir(args.run))
