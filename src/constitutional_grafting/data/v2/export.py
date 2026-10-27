"""11_export: kept pairs as Qwen chat segments for Axolotl input_output. The prompt (role system prompt if any, earlier turns,
"<|im_start|>assistant\\n") is unlabelled; the think block with the teacher's reasoning, the answer and <|im_end|> are labelled.
The constitution is never in the training prompt. Writes rows.jsonl (segments plus provenance) and checks the loss mask.
-- PI/Claude (opus-5-5), 2026-10-27
"""
import subprocess
import sys
from pathlib import Path

from .pipe import Step

KEEP_META = ("seed_id", "source", "source_id", "kind", "shape", "request_style", "teacher", "served", "provider", "gen_attempt",
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
        out = []
        for r in rows:
            if r["messages"][-1]["role"] != "user":
                raise ValueError(f"{r['seed_id']}: last message is {r['messages'][-1]['role']}, expected user")
            out.append({"id": f"v2_{r['seed_id']}", "segments": segments(r), **{k: r[k] for k in KEEP_META if k in r}})
        return out, []

    def __call__(self, rows, run):
        kept = super().__call__(rows, run)
        subprocess.run([sys.executable, str(Path(run.config["source_root"]) / "scripts/train/check_loss_mask.py"),
                        str(self.folder(run) / "rows.jsonl")], check=True)
        return kept
