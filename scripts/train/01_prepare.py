# /// script
# requires-python = ">=3.11"
# dependencies = ["transformers>=4.57", "jinja2", "loguru"]
# ///
"""Training files for Axolotl (configs/train/*.yml) from pipeline v2 outputs.

docs.jsonl  : {"text": doc} for the graft (Axolotl `completion`: plain text, no chat template)
sft_a.jsonl : Haiku labels; sft_b.jsonl: gemma's own answers (variant B). Axolotl `input_output` segments:
  [prompt = gemma's generation prompt, not trained] + [answer + "<turn|>", trained].
Why not the chat template's full render: with thinking off, gemma-4-31b-it's generation prompt ends in an empty
thought block ("<|turn>model\n<|channel>thought\n<channel|>") but the full-conversation render drops it, so training on
the full render would put answers in a context the model never sees at inference (checked 2026-10-08).
Usage: uv run scripts/train/01_prepare.py <corpus name> <sft name>  -> data/train/
"""
import json
import sys
from pathlib import Path

from loguru import logger
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
CORPUS, SFT = sys.argv[1], sys.argv[2]
OUT = ROOT / "data/train"
EOT = "<turn|>"


def main():
    tok = AutoTokenizer.from_pretrained("google/gemma-4-31b-it")
    OUT.mkdir(parents=True, exist_ok=True)
    docs = [json.loads(l) for l in (ROOT / "data/corpus" / CORPUS / "train.jsonl").read_text().splitlines() if l.strip()]
    (OUT / "docs.jsonl").write_text("".join(json.dumps({"text": d["text"]}) + "\n" for d in docs))
    dump = [f"# Training examples as the trainer sees them ({CORPUS}, {SFT})\n"]
    for variant, fname in (("a", "train.jsonl"), ("b", "train_student.jsonl")):
        rows = [json.loads(l) for l in (ROOT / "data/sft" / SFT / fname).read_text().splitlines() if l.strip()]
        out = []
        for r in rows:
            user, answer = r["messages"][0]["content"], r["messages"][1]["content"]
            prompt = tok.apply_chat_template([{"role": "user", "content": user}], tokenize=False, add_generation_prompt=True)
            assert prompt.endswith("<|turn>model\n<|channel>thought\n<channel|>"), prompt[-80:]
            out.append({"segments": [{"text": prompt, "label": False}, {"text": answer.strip() + EOT, "label": True}], "pool": r["pool"]})
        (OUT / f"sft_{variant}.jsonl").write_text("".join(json.dumps(o) + "\n" for o in out))
        logger.info(f"sft_{variant}: {len(out)} examples")
        for o in out[:2]:
            dump.append(f"\n## sft_{variant} ({o['pool']})\n\nNOT TRAINED:\n```\n{o['segments'][0]['text']}\n```\nTRAINED:\n```\n{o['segments'][1]['text']}\n```\n")
    dump.append(f"\n## docs (graft), first 600 chars\n\n```\n{docs[0]['text'][:600]}\n```\n")
    (OUT / "examples.md").write_text("".join(dump))
    logger.info(f"docs: {len(docs)}; wrote {OUT}")


if __name__ == "__main__":
    main()
