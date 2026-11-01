"""11_export: kept pairs as Qwen chat segments for Axolotl input_output. The prompt (role system prompt if any, earlier turns,
"<|im_start|>assistant\\n") is unlabelled; the think block with the teacher's reasoning, the answer and <|im_end|> are labelled.
An empty think block (imported rows without reasoning) goes in the unlabelled prompt. The assistant's name is fixed in 09_edit, not here.
The constitution is never in the training prompt. Writes rows.jsonl (segments plus provenance) and checks the loss mask.
-- PI/Claude (opus-5-5), 2026-10-27
"""
import re
import subprocess
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer

from .pipe import ROOT, Step

KEEP_META = ("route", "answer_direct", "reply_src", "answer_translated", "fidelity", "seed_id", "source", "source_id", "kind", "shape", "request_style", "teacher", "served", "provider", "gen_attempt",
             "retried", "edits", "identity_form", "undone", "undone_edits", "keep_operator_name", "edit_check", "judge", "jev", "judge2", "language_mismatch", "decides")


SCRIPTS = {"latin": r"[A-Za-z]", "cjk": r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", "cyrillic": r"[\u0400-\u04ff]",
           "arabic": r"[\u0600-\u06ff]", "devanagari": r"[\u0900-\u097f]", "greek": r"[\u0370-\u03ff]"}
ASKS_LANGUAGE = re.compile(r"translat|\bin (chinese|mandarin|japanese|korean|russian|arabic|hindi|greek)\b", re.I)


def script_mismatch(user: str, reply: str) -> bool:
    """Mechanical guard: the user writes in one script and the reply mostly in another, unasked (Kimi switched to Chinese on an
    English prompt: li-value-augmented-spec-2 dev lasr_d66bb124bea4; the judge's wrong_language question missed it)."""
    def shares(t):
        n = {k: len(re.findall(rx, t)) for k, rx in SCRIPTS.items()}
        total = sum(n.values()) or 1
        return {k: v / total for k, v in n.items()}
    u, r = shares(user), shares(reply)
    du, dr = max(u, key=u.get), max(r, key=r.get)
    return du != dr and u[du] > 0.9 and r[dr] > 0.5 and not ASKS_LANGUAGE.search(user)


def turn(role: str, content: str) -> str:
    return f"<|im_start|>{role}\n{content}<|im_end|>\n"


def segments(row: dict) -> list[dict]:
    """Real reasoning earns loss; an empty think block (imported rows) stays in the unlabelled prompt (check_loss_mask enforces it)."""
    prompt = "".join(turn(m["role"], m["content"]) for m in row["messages"]) + "<|im_start|>assistant\n"
    if row["reasoning"].strip():
        target = f"<think>\n{row['reasoning'].strip()}\n</think>\n\n{row['answer'].strip()}<|im_end|>"
    else:
        prompt, target = prompt + "<think>\n\n</think>\n\n", f"{row['answer'].strip()}<|im_end|>"
    return [{"text": prompt, "label": False}, {"text": target, "label": True}]


class Export(Step):
    number, name = 11, "export"

    def run(self, rows, run):
        t = run.config["export"]["tokenizer"]
        tok = Tokenizer.from_file(hf_hub_download(t["repo"], "tokenizer.json", revision=t["revision"]))
        limit = run.config["export"]["sequence_len"]
        out, rejected = [], []
        for r in rows:
            if r["messages"][-1]["role"] != "user":
                raise ValueError(f"{r['seed_id']}: last message is {r['messages'][-1]['role']}, expected user")
            guard = run.config["language_guard"]  # off | report (flag only) | drop
            assert guard in ("off", "report", "drop"), guard
            if guard != "off" and script_mismatch(r["messages"][-1]["content"], r["answer"]):
                if guard == "drop":
                    rejected.append({**r, "filter": "language_mismatch", "reason": "reply in another script than the user's message, unasked"})
                    continue
                r = {**r, "language_mismatch": True}
            segs = segments(r)
            n = len(tok.encode("".join(s["text"] for s in segs)).ids)
            if n > limit:  # training would truncate the target, cutting the answer or its <|im_end|>
                rejected.append({**r, "filter": "too_long", "reason": f"{n} tokens > sequence_len {limit}"})
                continue
            out.append({"id": f"{run.version}_{r['seed_id']}", "segments": segs, "tokens": n, **{k: r[k] for k in KEEP_META if k in r}})
        return out, rejected

    def __call__(self, rows, run):
        kept = super().__call__(rows, run)
        subprocess.run([sys.executable, str(ROOT / "scripts/train/check_loss_mask.py"),
                        str(self.folder(run) / "rows.jsonl")], check=True)
        return kept
