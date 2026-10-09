"""Merge a LoRA adapter into a full model and save it with gemma-4-31b-it's tokenizer and processor.

Graft: the adapter was trained on gemma-4-31B Base; merging it into gemma-4-31b-it adds ΔW = BA·α/r to the instruct
weights (a plain LoRA graft, as in Praxis "Grafting beliefs" LoRA sections; docs/vendor/praxis_grafting).
SFT: the adapter was trained on the model it is merged into.
Runs on the training box (Axolotl image: torch, transformers, peft).
usage: python scripts/train/02_merge.py <base model dir or hub id> <adapter dir> <out dir>   -- Claude (Opus 5.5)"""
import json
import sys
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer

IT = "google/gemma-4-31b-it"
base, adapter, out = sys.argv[1:]
model = AutoModelForImageTextToText.from_pretrained(base, dtype=torch.bfloat16, device_map="cuda")
before = {n: p.detach().clone() for n, p in model.named_parameters() if "layers.30.mlp.down_proj" in n or "layers.30.self_attn.q_proj" in n}
model = PeftModel.from_pretrained(model, adapter)
n_lora = sum("lora_A" in n for n, _ in model.named_parameters())
assert n_lora > 0, "adapter matched no modules: check target names against the base model"
model = model.merge_and_unload()
after = dict(model.named_parameters())
report = {n: {"rel_delta_fro": float((after[n] - w).float().norm() / w.float().norm())} for n, w in before.items()}
assert any(v["rel_delta_fro"] > 0 for v in report.values()), f"merge changed nothing: {report}"
model.save_pretrained(out, safe_serialization=True, max_shard_size="10GB")
AutoTokenizer.from_pretrained(IT).save_pretrained(out)
AutoProcessor.from_pretrained(IT).save_pretrained(out)
(Path(out) / "merge_report.json").write_text(json.dumps({"base": base, "adapter": adapter, "lora_modules": n_lora, "layer30": report}, indent=1))
print(json.dumps(report, indent=1))
