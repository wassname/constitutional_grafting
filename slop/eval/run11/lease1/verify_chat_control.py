"""Check the control through the box's actual Axolotl tokenizer and masks. -- PI/OpenAI"""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from axolotl.prompt_strategies.input_output import load
from transformers import AutoTokenizer

root = Path.cwd()
base = "/workspace/hf/hub/models--Qwen--Qwen3.5-35B-A3B-Base/snapshots/0f0813072d2358973511097385626f21fcb6d422"
tokenizer = AutoTokenizer.from_pretrained(base, local_files_only=True)
strategy = load(tokenizer, SimpleNamespace(train_on_inputs=False, sequence_len=8192))
manifest = json.loads((root / "data/train/run11_matched_chat_control/manifest.json").read_text())
results = {}
for name, relative in [("mix", "data/train/run11/chatmix.jsonl"), ("control", "data/train/run11_matched_chat_control/chatgen.jsonl")]:
    path = root / relative
    rows = [json.loads(line) for line in path.open()]
    supervised = total = max_length = 0
    for i, row in enumerate(rows):
        encoded = strategy.tokenize_prompt(row)
        assert len(encoded["input_ids"]) == len(encoded["labels"])
        assert len(encoded["input_ids"]) <= 8192, row["id"]
        total += len(encoded["input_ids"])
        supervised += sum(label != -100 for label in encoded["labels"])
        max_length = max(max_length, len(encoded["input_ids"]))
        if i == 0:
            print(json.dumps({"sample_set": name, "selection": "first row, fixed order", "row": row,
                              "decoded_input": tokenizer.decode(encoded["input_ids"], skip_special_tokens=False),
                              "supervised_tokens": sum(label != -100 for label in encoded["labels"])}), flush=True)
    results[name] = {"rows": len(rows), "supervised_tokens": supervised, "total_tokens": total,
                     "max_sequence_tokens": max_length, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
assert results["mix"]["supervised_tokens"] == manifest["target_supervised_tokens"]
assert results["control"]["supervised_tokens"] == manifest["supervised_tokens"]
assert results["control"]["sha256"] == manifest["sha256"]
assert results["mix"]["sha256"] == manifest["target_sha256"]
print("PASS actual Axolotl input_output masks/token counts: " + json.dumps(results), flush=True)
