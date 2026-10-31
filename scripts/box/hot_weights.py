"""Pinned pristine HF tensors, streamed GPU LoRA merges in 02_merge.py order. -- PI/OpenAI

Qwen routed parameters use PEFT's [experts,out,in] ParamWrapper math; vLLM alone packs kernels.
No model construction, checkpoint conversion, or per-cell disk I/O.
"""
import json
import math
import re
import time
from pathlib import Path

import torch
from safetensors import safe_open


def layer_prefix(name):
    match = re.match(r"(.+\.layers\.\d+)\.", name)
    assert match, f"hot swap supports decoder-layer adapters only: {name}"
    return match[1] + "."


def pattern_value(pattern, name, default):
    return next((value for key, value in pattern.items() if re.match(rf"(.*\.)?({key})$", name)), default)


def validate_adapter(path):
    cfg = json.loads((Path(path) / "adapter_config.json").read_text())
    assert cfg["peft_type"] == "LORA" and cfg["bias"] == "none", cfg
    assert not any(cfg.get(k) for k in ("modules_to_save", "layer_replication", "fan_in_fan_out", "lora_bias", "use_dora")), cfg
    with safe_open(Path(path) / "adapter_model.safetensors", framework="pt", device="cpu") as f:
        assert f.keys(), "empty adapter"
        for key in f.keys():
            layer_prefix(key)
    return cfg


class Adapter:
    def __init__(self, path, num_experts):
        self.config = cfg = validate_adapter(path)
        self.factors = {}
        with safe_open(Path(path) / "adapter_model.safetensors", framework="pt", device="cpu") as f:
            for key in f.keys():
                assert ".lora_A.weight" in key or ".lora_B.weight" in key, key
                name, side = key.removeprefix("base_model.model.").split(".lora_")
                if ".mlp.experts" in name:
                    module = name.split(".base_layer")[0]
                    # Qwen registers gate_up then down; PEFT nests the later wrapper outside.
                    targets = [t for t in ("gate_up_proj", "down_proj") if any(
                        module + "." + t == target or (module + "." + t).endswith("." + target)
                        for target in cfg["target_parameters"])]
                    name = module + "." + targets[::-1][name.count(".base_layer")]
                else:
                    name = name.replace(".base_layer", "") + ".weight"
                layer_prefix(name)
                self.factors.setdefault(name, {})[side[0]] = f.get_tensor(key).pin_memory()
        assert self.factors, "adapter matched no weights"
        self.num_experts = num_experts
        self.scaling = {}
        for name, factors in self.factors.items():
            assert set(factors) == {"A", "B"}, name
            target = name.removesuffix(".weight")
            rank = pattern_value(cfg.get("rank_pattern", {}), target, cfg["r"])
            alpha = pattern_value(cfg.get("alpha_pattern", {}), target, cfg["lora_alpha"])
            assert factors["A"].shape[0] == rank * (num_experts if ".mlp.experts." in name else 1), name
            self.scaling[name] = alpha / (math.sqrt(rank) if cfg.get("use_rslora") else rank)

    @staticmethod
    def target(name):
        expert = re.match(r"(.+\.mlp\.experts)\.(\d+)\.(gate|up|down)_proj\.weight$", name)
        return expert[1] + (".down_proj" if expert[3] == "down" else ".gate_up_proj") if expert else name

    def delta(self, name, dose, device):
        expert = re.match(r"(.+\.mlp\.experts)\.(\d+)\.(gate|up|down)_proj\.weight$", name)
        target = self.target(name)
        if expert:
            _, index, projection = expert.groups()
        if target not in self.factors:
            return None
        factors = self.factors[target]
        A, B = factors["A"], factors["B"]
        routed = ".mlp.experts." in target
        if routed:
            A = A.reshape(self.num_experts, -1, A.shape[-1])
            B = B.reshape(B.shape[0], -1, self.num_experts)
            if expert:
                A, B = A[int(index):int(index) + 1], B[:, :, int(index):int(index) + 1]
                if projection != "down":
                    B = B.chunk(2, dim=0)[projection == "up"]
        # BF16/F16 promotion is exact; do it after H2D to match PEFT without doubling host RAM. -- PI/OpenAI
        A, B = A.to(device, non_blocking=True).float(), B.to(device, non_blocking=True).float()
        B = B * dose  # 02_merge.py scales B before PEFT computes the product.
        if routed:
            delta = torch.einsum("ore,eri->eoi", B, A).mul_(self.scaling[target])
            return (delta[0] if expert else delta).half()  # ParamWrapper casts before adding; Linear does not.
        return (B @ A) * self.scaling[target]


class HotWeights:
    def __init__(self, base, adapters):
        start = time.perf_counter()
        config = json.loads((Path(base) / "config.json").read_text())
        text = config.get("text_config", config)
        self.adapters = {p: Adapter(p, text.get("num_experts", 1)) for p in adapters}
        if any(".mlp.experts." in n for a in self.adapters.values() for n in a.factors):
            assert text["model_type"] in {"qwen3_5_moe_text", "qwen3_next"}, "hot expert layout is Qwen [E,out,in]"
        self.layers = {layer_prefix(n) for a in self.adapters.values() for n in a.factors}
        self.pristine = {}
        for shard in sorted(Path(base).glob("*.safetensors")):
            with safe_open(shard, framework="pt", device="cpu") as f:
                for name in f.keys():
                    if any(name.startswith(p) for p in self.layers):
                        source = f.get_tensor(name)
                        dest = torch.empty(source.shape, dtype=torch.float16, pin_memory=True, device="cpu")
                        dest.copy_(source)
                        self.pristine[name] = dest
        assert self.pristine, "no pristine decoder weights"
        for path, adapter in self.adapters.items():
            missing = set(adapter.factors) - {adapter.target(n) for n in self.pristine}
            assert not missing, f"adapter targets missing from pristine checkpoint: {path}: {sorted(missing)}"
        self.bytes = sum(w.numel() * w.element_size() for w in self.pristine.values())
        self.adapter_bytes = sum(w.numel() * w.element_size() for a in self.adapters.values()
                                 for factors in a.factors.values() for w in factors.values())
        self.init_seconds = time.perf_counter() - start

    def weights(self, cell, device):
        applied = [set() for _ in cell]
        for name in sorted(self.pristine):
            weight = self.pristine[name].to(device, non_blocking=True, copy=True)
            for i, (path, dose) in enumerate(cell):
                if dose == 0:
                    continue
                adapter = self.adapters[path]
                delta = adapter.delta(name, dose, device)
                if delta is not None:
                    weight.add_(delta)  # In-place addition rounds to fp16 after every listed adapter.
                    applied[i].add(adapter.target(name))
                del delta
            yield name, weight
        for (path, dose), targets in zip(cell, applied):
            if dose != 0:
                missing = set(self.adapters[path].factors) - targets
                assert not missing, f"adapter targets not applied this cell: {path}: {sorted(missing)}"
