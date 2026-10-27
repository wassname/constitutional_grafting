#!/usr/bin/env python3
"""Regex flags to read, never automatic filters. -- PI/Claude; revised PI/OpenAI (Sol)"""
import argparse
import collections
import re
import statistics

from tabulate import tabulate

from common import read_jsonl, run_dir
from constitutional_grafting.data.files import write_jsonl

PATTERNS = {
    "doc_ref": r"\b(constitution|system prompt|instructions?|the (text|document|description) (above|provided)|persona|role-?play|stay in character|respond as|kimi|moonshot)\b",
    "telegraphic": r"\b(i |we )?need (respond|answer|write|give|say|address|decide)\b",
    "planning": r"\b(the user (is|wants|asks|asked|says|seems)|i should (respond|answer|reply|write)|let me (draft|write|craft|structure))",
    "format_talk": r"\b(markdown|bullet|headings?|format|word count|concise answer|tone:)\b",
    "refuse": r"\b(i won't|i will not|i can't help|i cannot help|i'm not going to|i decline|i refuse|not something i can)\b",
    "virtue": r"\b(virtue|vice|dignity|integrity|courage|justice|temperance|wisdom)\b",
}


def matches(pattern: str, text: str) -> list[str]:
    return [m.group(0) for m in re.finditer(PATTERNS[pattern], text, re.I)]


def screen(row: dict) -> dict:
    think, answer = row["reasoning"] or "", row["content"] or ""
    head = think[:max(1, len(think) // 4)]
    return {"call_id": row["call_id"], "framing": row["framing"], "finish": row["finish_reason"],
            "think_words": len(think.split()), "answer_words": len(answer.split()),
            **{p: len(matches(p, think)) for p in ("doc_ref", "telegraphic", "planning", "format_talk")},
            "doc_ref_answer": len(matches("doc_ref", answer)),
            "refuse_in_first_quarter": len(matches("refuse", head)),
            "refuse_answer": len(matches("refuse", answer)),
            "virtue_words_answer": len(matches("virtue", answer)),
            "doc_ref_quotes": [m.group(0) for m in re.finditer(r"[^.\n]{0,60}" + PATTERNS["doc_ref"] + r"[^.\n]{0,60}", think, re.I)][:3]}


def report(run):
    out = [screen(row) for row in read_jsonl(run / "raw.jsonl")]
    if not out:
        raise ValueError("No generations to screen")
    write_jsonl(run / "screen.jsonl", out)
    flags = ["doc_ref", "doc_ref_answer", "telegraphic", "planning", "format_talk", "refuse_in_first_quarter", "refuse_answer"]
    by = collections.defaultdict(list)
    for row in out:
        by[row["framing"]].append(row)
    table = [{"framing": fr, "n": len(rs), "not stop": sum(o["finish"] != "stop" for o in rs),
              "median think words": statistics.median(o["think_words"] for o in rs),
              "median answer words": statistics.median(o["answer_words"] for o in rs),
              **{f: sum(o[f] > 0 for o in rs) for f in flags}} for fr, rs in sorted(by.items())]
    md = ("# Regex screen (rows with ≥1 match; flags to read, not filters)\n\n"
          + tabulate(table, headers="keys", tablefmt="pipe")
          + "\n\n`doc_ref` also matches ordinary instructions unrelated to the constitution. `format_talk` includes normal answer planning. Read before attributing either to a defect.\n\n## doc_ref quotes (reasoning)\n\n"
          + "\n".join(f"- `{o['call_id']}`: " + " | ".join(q.replace("\n", " ") for q in o["doc_ref_quotes"])
                      for o in out if o["doc_ref_quotes"]) + "\n\n-- PI/OpenAI (Sol)\n")
    (run / "screen.md").write_text(md)
    print(tabulate(table, headers="keys", tablefmt="pipe"))
    print(run / "screen.md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    args = ap.parse_args()
    report(run_dir(args.run))
