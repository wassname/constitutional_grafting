#!/usr/bin/env python3
"""Rebuild the first-batch results page from cached generations and recorded reviews. -- PI/OpenAI (Sol)"""
import argparse
import collections
import json
import statistics
from pathlib import Path

from tabulate import tabulate

from common import by_id, material_hash, read_jsonl, run_dir, validate_judgment

NAMES = {"const": "Document framing", "self": "First-person text"}


def report(run: Path):
    raw = by_id(read_jsonl(run / "raw.jsonl"), "call_id")
    prompts = by_id(read_jsonl(run / "prompts.jsonl"), "id")
    readers = by_id(read_jsonl(run / "reader_verdicts.jsonl"), "call_id")
    judged = by_id(read_jsonl(run / "judged.jsonl"), "call_id")
    for cid, verdict in judged.items():
        validate_judgment(verdict, prompts[raw[cid]["id"]], raw[cid], material_hash(run, prompts[raw[cid]["id"]], raw[cid]))
    for cid, verdict in readers.items():
        if verdict["input_sha256"] != material_hash(run, prompts[raw[cid]["id"]], raw[cid]):
            raise ValueError(f"stale reader verdict: {cid}")
        for quote in verdict["quotes"]:
            if not any(quote in (raw[cid][field] or "") for field in ("reasoning", "content")):
                raise ValueError(f"reader quote not in candidate: {cid}")
    attempts_path = run / "judge/attempts.json"
    attempts = json.loads(attempts_path.read_text()) if attempts_path.exists() else {"status": "not run", "reported_usage_usd": 0}
    cost = sum(r["cost_usd"] for r in raw.values())
    judge_cost = attempts["reported_usage_usd"]
    groups = {r["id"] for r in raw.values()}
    rows = []
    for framing in sorted({r["framing"] for r in raw.values()}):
        rs = [r for r in raw.values() if r["framing"] == framing]
        reviewed = [readers[r["call_id"]] for r in rs if r["call_id"] in readers]
        rows.append({"System framing": NAMES[framing],
                     "Complete↑": f"{sum(r['finish_reason'] == 'stop' and bool(r['reasoning']) and bool(r['content']) for r in rs)}/{len(rs)}",
                     "Reader candidates": f"{sum(r['reader_verdict'] == 'candidate' for r in reviewed)}/{len(reviewed)}",
                     "Thinking words (median)": statistics.median(len((r["reasoning"] or "").split()) for r in rs),
                     "Answer words (median)": statistics.median(len((r["content"] or "").split()) for r in rs),
                     "Kimi cost": f"${sum(r['cost_usd'] for r in rs):.3f}"})
    shapes = collections.defaultdict(list)
    for cid, review in readers.items():
        shapes[prompts[raw[cid]["id"]]["shape"]].append(review)
    shape_rows = [{"Prompt shape": shape, "Reader candidates": sum(r["reader_verdict"] == "candidate" for r in rs),
                   "Needs revision": sum(r["reader_verdict"] == "needs_revision" for r in rs), "Read in full": len(rs)}
                  for shape, rs in sorted(shapes.items())]
    overview = (f"# Can Kimi supply moral-reasoning traces for a constitutional graft?\n\n"
                f"Run `{run.name}`. **First batch only: {len(groups)} of {len(prompts)} frozen prompts, {len(raw)} replies.** "
                f"Kimi cost ${cost:.2f}; blocked Opus attempts reported ${judge_cost:.2f}; total reported usage ${cost + judge_cost:.2f}.\n\n"
                f"Opus status: `{attempts['status']}`. Independent judgments returned: {len(judged)}. "
                f"Sol read {len(readers)}/{len(raw)} traces in full across a seeded four-prompt sample. "
                "No training data is approved, no training has run, and batches 1–4 have not run.\n\n"
                "## Two system framings, same training prompts\n\n"
                "Document framing says ‘your constitution … follow it’; first-person text supplies the constitution alone. "
                "Original conversation role prompts stay in both. Each prompt has two draws per framing. "
                "The teacher never sees our prior target answer. No guide or requested visible-reasoning format is added.\n\n"
                + tabulate(rows, headers="keys", tablefmt="pipe")
                + "\n\n‘Reader candidates’ are Sol's provisional recommendations on the same eight traces per framing, not Opus labels or a measured training yield. "
                  "They cannot establish a preferred framing. Textual deliberation before an answer does not establish causal faithfulness or transfer to another model.\n\n"
                "## Seeded full-read sample, by shape\n\n"
                + tabulate(shape_rows, headers="keys", tablefmt="pipe")
                + "\n\nAll four candidates of each sampled prompt were read. The other 24 replies have machine checks only. "
                  "See `reading_notes.md` for the judgments, direct evidence and primary-source legal checks.\n\n")
    selection = json.loads((run / "spot_check_selection.json").read_text())
    examples = ("## Full examples\n\n"
                f"Selection: {selection['method']}. These are not selected winners. All four variants, their reasoning, "
                "answers and our prior reference answer are shown for each sampled prompt. The same constitution text is in `provenance/v4.md`; "
                "the exact framing wrapper and conversation order are in `provenance/common.py`, `provenance/02_generate.py`, and `prompts.jsonl`. "
                "Open a group below or its `judge/packets/<id>.md` file.\n\n")
    for pid in selection["prompt_ids"]:
        examples += f"<details><summary>{pid} ({prompts[pid]['shape']}): all four complete traces</summary>\n\n"
        examples += (run / "judge/packets" / f"{pid}.md").read_text() + "\n</details>\n\n"
    notes = (run / "reading_notes.md").read_text()
    audit_path = run / "audit.md"
    audit = audit_path.read_text() if audit_path.exists() else "Audit not yet written."
    (run / "report.md").write_text(overview + "## Reader findings\n\n" + notes + "\n## Run audit\n\n" + audit
                                  + "\n" + examples + "\n-- PI/OpenAI (Sol)\n")
    print(overview)
    print(run / "report.md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    args = ap.parse_args()
    report(run_dir(args.run))
