"""08_retry: one fresh teacher sample for each pair the judge sent to REGENERATE, rechecked by the same regex, Jev and judge steps.
Small batch: judge test-retest agreed on 43/50 reject decisions, but two teacher samples agreed on only 18/49 verdicts, so most
rejects are the sample, not the seed. -- PI/Claude (opus-5-5), 2026-10-27
"""
from .checks import Jev, Regex
from .generate import Generate
from .judge import Judge
from .pipe import Step, read_jsonl

STRIP = ("reasoning", "answer", "teacher", "served", "provider", "gen_cost", "gen_attempt", "regex_counts",
         "jev", "jev_vent", "jev_edit", "jev_queue", "judge", "judge_cost", "filter", "reason", "stage")


class Retry(Step):
    number, name = 8, "retry"

    def run(self, rows, run):
        judged = Judge().folder(run) / "rejected.jsonl"
        redo = [{k: v for k, v in r.items() if k not in STRIP} for r in read_jsonl(judged) if r["filter"].startswith("judge")]
        rejected = []
        for step in (Generate(attempt=1), Regex(), Jev(), Judge()):
            redo, bad = step.run(redo, run)
            rejected += [{**b, "stage": "retry:" + step.name} for b in bad]
        print(f"retry: {len(redo)} of {len(redo) + len(rejected)} judge rejects passed on a second teacher sample")
        return rows + [{**r, "retried": True} for r in redo], rejected
