"""08_import: add finished chat pairs from an earlier dataset (e.g. chatr12, Opus replies with empty think blocks) to the rows going into
09_edit, so they get the same allowed edits and edit checks. They passed their own review, so no judge, Jev or retry runs on them.

Rows come from Axolotl segment files (one unlabelled prompt ending "<|im_start|>assistant\\n<think>\\n\\n</think>\\n\\n", one labelled
reply ending "<|im_end|>") and are parsed back to the pipeline schema with reasoning "". 11_export puts an empty reasoning block in the
unlabelled prompt, so it gets no loss. Rows whose prompt matches a held-out eval (seeds.leaked) or a dropped pattern are rejected.
-- PI/Claude (opus-5-5), 2026-10-29
"""
import re
from pathlib import Path

from ..files import ROOT
from .pipe import Run, Step, read_jsonl
from .seeds import heldout_corpus, leaked

TURN = re.compile(r"<\|im_start\|>(system|user|assistant)\n(.*?)<\|im_end\|>\n", re.S)
EMPTY_THINK = re.compile(r"^<think>\s*</think>\s*")
OPEN = "<|im_start|>assistant\n<think>\n\n</think>\n\n"


def parse(seg_row: dict) -> tuple[list[dict], str]:
    prompt, reply = seg_row["segments"]
    assert not prompt["label"] and reply["label"], seg_row["id"]
    assert prompt["text"].endswith(OPEN), f"{seg_row['id']}: prompt does not end with an empty think block"
    assert reply["text"].endswith("<|im_end|>"), f"{seg_row['id']}: reply lacks <|im_end|>"
    body = prompt["text"][: -len(OPEN)]
    messages = [{"role": r, "content": EMPTY_THINK.sub("", c) if r == "assistant" else c} for r, c in TURN.findall(body)]
    assert messages and TURN.sub("", body) == "", f"{seg_row['id']}: unparsed prompt text"
    assert messages[-1]["role"] == "user", seg_row["id"]
    return messages, reply["text"][: -len("<|im_end|>")].strip()


class ImportRows(Step):
    number, name = 8, "import"

    def __init__(self, path: str, batches: tuple[str, ...], tag: str, drop: tuple[str, ...] = ()):
        self.path, self.batches, self.tag = ROOT / path, batches, tag
        self.drop = [re.compile(p) for p in drop]  # e.g. r"You are Atlas": too close to tiny-char's sys_atlas_identity item

    def run(self, rows, run: Run):
        if run.batch not in self.batches:  # import once, into the named batch only
            return rows, []
        corpus = heldout_corpus(run)
        kept, rejected = [], []
        for r in read_jsonl(self.path):
            messages, answer = parse(r)
            row = {"seed_id": f"{self.tag}_{r['id']}", "source": f"{self.tag}:{r['source']}", "source_id": r["id"], "family": f"{self.tag}:{r['id']}",
                   "shape": r["shape"], "kind": "chat", "recipe": self.tag, "messages": messages, "request_style": "imported",
                   "teacher": self.tag, "reasoning": "", "answer": answer, "route": "en"}
            text = " ".join(m["content"] for m in messages)
            if hit := next((p.pattern for p in self.drop if p.search(text)), None):
                rejected.append({**row, "filter": "import_drop", "reason": f"matches {hit}"})
            elif leaked(text, corpus):
                rejected.append({**row, "filter": "heldout_leak", "reason": "prompt overlaps a held-out eval item"})
            else:
                kept.append(row)
        return rows + kept, rejected
