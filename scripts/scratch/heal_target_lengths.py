# /// script
# requires-python = ">=3.11"
# dependencies = ["datasets", "transformers", "numpy"]
# ///
"""Target lengths in the heal sources' datasets (Qwen3.5 tokenizer): GSM8K train answers (Yang SDFT targets are rewrites of these),
OpenMathInstruct-1 solutions (Thangarasa), Alpaca outputs (LLM-Pruner), WikiText-103 (Minitron: fixed 4096-token chunks).
-- PI/Claude (Opus 5.5)"""
import itertools
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B")
def stats(name, texts):
    n = np.array([len(tok(t).input_ids) for t in texts])
    print(f"| {name} | {len(n)} | {np.median(n):.0f} | {np.percentile(n, 90):.0f} | {n.max()} |")
print("| target set | n sampled | median tokens | p90 | max |\n|:--|--:|--:|--:|--:|")
stats("GSM8K train gold answer", [r["answer"] for r in load_dataset("openai/gsm8k", "main", split="train")])
om = load_dataset("nvidia/OpenMathInstruct-1", split="train", streaming=True)
stats("OpenMathInstruct-1 generated_solution (first 3000 correct)", [r["generated_solution"] for r in itertools.islice((r for r in om if r.get("is_correct")), 3000)])
stats("Alpaca-cleaned output", [r["output"] for r in load_dataset("yahma/alpaca-cleaned", split="train").select(range(5000))])
