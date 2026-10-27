"""05_regex (counts only, never rejects) and 06_jev (one narrow question per filter, with llm-judge's vent).
Every row keeps all scores, so rejects and accepts can be read per filter. -- PI/Claude (opus-5-5), 2026-10-27
"""
import asyncio
import re
import yaml

from ..files import ROOT
from .pipe import Run, Step

TICS = {"honest": r"\bhonest(ly)?\b|\bfrankly\b", "plain": r"\bplain(ly)?\b", "quiet": r"\bquiet(ly)?\b",
        "heres": r"\bhere['’]s\b", "i_wont": r"\bI won['’]t\b", "em_dash": "\u2014", "not_but": r"\bnot\b[^.;]{1,40}\bbut\b",
        "persona_words": r"\bMusonius (?:would|says|should)|\bthe persona\b|\bthe character\b|\bas instructed\b|\bI(?:'ve| have) been told\b"}


def case_text(row: dict) -> str:
    return "\n\n".join(f"[{m['role']}] {m['content']}" for m in row["messages"])


class Regex(Step):
    number, name = 5, "regex"

    def run(self, rows, run):
        out = []
        for r in rows:
            counts = {f: {k: len(re.findall(rx, r[f], re.I)) for k, rx in TICS.items()} for f in ("reasoning", "answer")}
            out.append({**r, "regex_counts": counts, "words": {f: len(r[f].split()) for f in ("reasoning", "answer")}})
        return out, []


class Jev(Step):
    number, name = 6, "jev"

    def __init__(self, filters: str = "configs/data/v2/jev_filters.yaml"):
        self.filters_path = filters

    def run(self, rows, run):
        from llm_judge import Trace, label
        filters = yaml.safe_load((ROOT / self.filters_path).read_text())
        questions = {k: v["question"] for k, v in filters.items()}

        async def score_all():
            sem = asyncio.Semaphore(8)
            with Trace(run.data / "cache/jev") as trace:
                async def one(r):
                    state = {"task": "Check one training example: an AI's hidden reasoning and its answer to the conversation in `case`.",
                             "case": case_text(r), "reasoning": r["reasoning"], "answer": r["answer"]}
                    async with sem:
                        res = await label(state, questions, trace=trace, feedback=False)
                    vent = sorted(res["unscored_vent"][0]["probabilities"].items(), key=lambda x: -x[1])[:6]
                    return {k: v["noul"] for k, v in res["means"].items()}, vent
                return await asyncio.gather(*(one(r) for r in rows))

        kept, rejected = [], []
        for r, (p, vent) in zip(rows, asyncio.run(score_all())):
            r = {**r, "jev": p, "jev_vent": vent,
                 "jev_edit": [k for k, f in filters.items() if f["action"] == "edit" and p[k] >= f["cutoff"]],
                 "jev_queue": [k for k, f in filters.items() if f["action"] == "queue" and p[k] >= f["cutoff"]]}
            hits = [k for k, f in filters.items() if f["action"] == "reject" and p[k] >= f["cutoff"]]
            if hits:
                rejected.append({**r, "filter": hits[0], "reason": ", ".join(f"{k} P={p[k]:.2f}" for k in hits)})
            else:
                kept.append(r)
        return kept, rejected
