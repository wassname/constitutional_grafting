"""11_export: kept pairs as Qwen chat segments for Axolotl input_output. The prompt (role system prompt if any, earlier turns,
"<|im_start|>assistant\\n") is unlabelled; the think block with the teacher's reasoning, the answer and <|im_end|> are labelled.
The constitution is never in the training prompt. Writes rows.jsonl (segments plus provenance) and checks the loss mask.
-- PI/Claude (opus-5-5), 2026-10-27
"""
import subprocess
import sys
from pathlib import Path

from tokenizers import Tokenizer

from .edit import SELF_NAME
from .pipe import Step

KEEP_META = ("route", "answer_direct", "reply_src", "answer_translated", "fidelity", "seed_id", "source", "source_id", "kind", "shape", "request_style", "teacher", "served", "provider", "gen_attempt",
             "retried", "edits", "judge", "jev")


def turn(role: str, content: str) -> str:
    return f"<|im_start|>{role}\n{content}<|im_end|>\n"


def segments(row: dict) -> list[dict]:
    prompt = "".join(turn(m["role"], m["content"]) for m in row["messages"]) + "<|im_start|>assistant\n"
    target = f"<think>\n{row['reasoning'].strip()}\n</think>\n\n{row['answer'].strip()}<|im_end|>"
    return [{"text": prompt, "label": False}, {"text": target, "label": True}]


class Export(Step):
    number, name = 11, "export"

    def run(self, rows, run):
        tok = Tokenizer.from_file(run.config["export"]["tokenizer"])
        limit = run.config["export"]["sequence_len"]
        out, rejected = [], []
        for r in rows:
            if r["messages"][-1]["role"] != "user":
                raise ValueError(f"{r['seed_id']}: last message is {r['messages'][-1]['role']}, expected user")
            segs = segments(r)
            target = "".join(s["text"] for s in segs if s["label"])
            if m := SELF_NAME.search(target):  # the trained text must never call itself Kimi or DeepSeek
                rejected.append({**r, "filter": "teacher_self_name", "reason": f"target names {m.group(0)!r} after the edit step"})
                continue
            n = len(tok.encode("".join(s["text"] for s in segs)).ids)
            if n > limit:  # training would truncate the target, cutting the answer or its <|im_end|>
                rejected.append({**r, "filter": "too_long", "reason": f"{n} tokens > sequence_len {limit}"})
                continue
            out.append({"id": f"{run.version}_{r['seed_id']}", "segments": segs, "tokens": n, **{k: r[k] for k in KEEP_META if k in r}})
        return out, rejected

    def __call__(self, rows, run):
        kept = super().__call__(rows, run)
        subprocess.run([sys.executable, str(Path(run.config["source_root"]) / "scripts/train/check_loss_mask.py"),
                        str(self.folder(run) / "rows.jsonl")], check=True)
        return kept
