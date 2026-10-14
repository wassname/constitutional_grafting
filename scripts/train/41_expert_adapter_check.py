"""Check a trained MoE LoRA adapter actually trained the routed experts: every expert lora_B tensor present and nonzero
(lora_B starts at zero, so nonzero after a few steps means gradients reached the experts).
usage: python scripts/train/41_expert_adapter_check.py ADAPTER_DIR [EXPECTED_WRAPPERS=80]   -- PI/Claude (Opus 5.5)"""
import json
import sys
from pathlib import Path

from safetensors import safe_open

adapter = Path(sys.argv[1])
expected = int(sys.argv[2]) if len(sys.argv) > 2 else 80  # Qwen3.5-35B-A3B: 40 layers x (gate_up_proj, down_proj)
cfg = json.loads((adapter / "adapter_config.json").read_text())
print("target_parameters:", cfg.get("target_parameters"), "rank_pattern:", cfg.get("rank_pattern"))
report = {}
with safe_open(adapter / "adapter_model.safetensors", "pt") as f:
    for k in f.keys():
        if ".mlp.experts." in k and "lora_B" in k:
            t = f.get_tensor(k).float()
            report[k] = {"shape": list(t.shape), "norm": float(t.norm())}
n_nonzero = sum(v["norm"] > 0 for v in report.values())
print(json.dumps(dict(list(report.items())[:4]), indent=1))
print(f"expert lora_B tensors: {len(report)} (expected {expected}), nonzero: {n_nonzero}")
assert len(report) == expected and n_nonzero == expected, "routed experts missing or untrained"
print("PASS: every routed-expert lora_B is present and nonzero")
