"""Axolotl plugin: cast MoE routers (modules named *.gate, e.g. Qwen3_5MoeTopKRouter) back to the training dtype after load.
Axolotl's loader upcasts every module ending in ".gate" to fp32 (loaders/model.py, _convert_embedding_modules_dtype), but
with a bf16 (non-4-bit) LoRA nothing casts it back, and the router's F.linear then fails: "expected mat1 and mat2 to have
the same dtype, but got: c10::BFloat16 != float" (qwen run smoke, 2026-10-11).   -- Claude (Opus 5.5)"""
import torch
from axolotl.integrations.base import BasePlugin


class RouterDtypePlugin(BasePlugin):
    def post_model_load(self, cfg, model):
        dtype = cfg.torch_dtype or torch.bfloat16
        n = 0
        for name, module in model.named_modules():
            if name.endswith(".gate") and any(p.dtype != dtype for p in module.parameters(recurse=False)):
                module.to(dtype)
                n += 1
        print(f"RouterDtypePlugin: cast {n} router modules to {dtype}", flush=True)
