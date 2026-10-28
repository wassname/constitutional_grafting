"""08_retry: one fresh sample from the retry teacher for each pair the judge sent to REGENERATE or Jev rejected, rechecked by the
same route, regex, Jev and judge steps. Small batch: two teacher samples agreed on only 18/49 judge verdicts, so most rejects are
the sample, not the seed. The retry teacher differs from the main one where the main teacher's failures are settled views (Kimi
never raised the bee lockout in 0/10 resamples); wassname approved Kimi main, DeepSeek flash retry. -- PI/Claude (opus-5-5), 2026-10-27
"""
from .checks import Jev, Regex
from .generate import Generate
from .judge import Judge
from .pipe import Step, read_jsonl
from .route import Route

STRIP = ("reasoning", "answer", "answer_direct", "reply_src", "answer_translated", "fidelity", "route", "route_cost", "teacher", "served", "provider", "gen_cost", "gen_attempt", "regex_counts",
         "jev", "jev_vent", "jev_edit", "jev_queue", "judge", "judge_cost", "filter", "reason", "stage")


class Retry(Step):
    number, name = 8, "retry"

    def run(self, rows, run):
        bad_rows = read_jsonl(Judge().folder(run) / "rejected.jsonl") + read_jsonl(Jev().folder(run) / "rejected.jsonl")
        redo = [{k: v for k, v in r.items() if k not in STRIP} for r in bad_rows if r["filter"] != "judge_failed"]
        rejected = []
        teacher = "retry_teacher" if "retry_teacher" in run.config else "teacher"
        steps = [Generate(attempt=1, teacher=teacher)] + ([Route()] if "answer_route" in run.config else []) + [Regex(), Jev(), Judge()]
        for step in steps:
            redo, bad = step.run(redo, run)
            rejected += [{**b, "stage": "retry:" + step.name} for b in bad]
        print(f"retry: {len(redo)} of {len(redo) + len(rejected)} judge rejects passed on a second teacher sample")
        return rows + [{**r, "retried": True} for r in redo], rejected
