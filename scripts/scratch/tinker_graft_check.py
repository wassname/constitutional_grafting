# /// script
# requires-python = ">=3.11"
# dependencies = ["tinker", "python-dotenv"]
# ///
"""Can Tinker serve/train a LoRA trained on a Base model on top of an instruct model (the graft)?

Creates an untrained LoRA on each Base, saves it, then tries to reload it with base_model=<instruct>
for training and for sampling. Cost: a few save/load calls, no training tokens.
"""
import sys
import traceback

import tinker
from dotenv import load_dotenv

load_dotenv(sys.argv[1])  # path to a .env with TINKER_API_KEY

PAIRS = [
    ("Qwen/Qwen3.5-9B-Base", "Qwen/Qwen3.5-9B"),
    ("Qwen/Qwen3.5-35B-A3B-Base", "Qwen/Qwen3.6-35B-A3B"),  # instruct 3.5-35B-A3B is retired; 3.6 is the hosted one
]

svc = tinker.ServiceClient()


def attempt(label, fn):
    try:
        out = fn()
        print(f"OK   {label}: {out}")
    except Exception as e:
        print(f"FAIL {label}: {type(e).__name__}: {str(e)[:400]}")


for base, instruct in PAIRS:
    print(f"\n== {base} -> {instruct}")
    tc = svc.create_lora_training_client(base_model=base, rank=8)
    state = tc.save_state("graft-check").result()
    sampler = tc.save_weights_for_sampler("graft-check").result()
    print("saved", state.path, sampler.path)
    attempt("train client from state, base_model=instruct",
            lambda: svc.create_training_client_from_state(state.path, base_model=instruct).get_info())
    attempt("sampling client, base_model=instruct",
            lambda: svc.create_sampling_client(model_path=sampler.path, base_model=instruct))
