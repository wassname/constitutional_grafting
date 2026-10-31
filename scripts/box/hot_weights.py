"""Prepare fp16 HF weights for a hot cell, using the ordinary PEFT merge. -- PI/OpenAI

Only decoder layers targeted by any adapter in this invocation are materialized. Include their
frozen siblings too: vLLM's stacked parameters and expert packing must reload complete layers.
Pristine values are read anew on every cell, including adapters absent from the current cell.
"""
import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

import torch
from peft import PeftConfig
from peft.tuners.tuners_utils import check_target_module_exists
from safetensors import safe_open
from safetensors.torch import save_file
from transformers import AutoConfig, AutoModelForImageTextToText
from transformers.conversion_mapping import get_model_conversion_mapping
from transformers.core_model_loading import convert_and_load_state_dict_in_model, revert_weight_conversion
from transformers.modeling_utils import LoadStateDictConfig

spec = importlib.util.spec_from_file_location("merge_weights", Path(__file__).parents[1] / "train/02_merge.py")
merge_weights = importlib.util.module_from_spec(spec)
spec.loader.exec_module(merge_weights)


def layer_prefix(name):
    match = re.match(r"(.+\.layers\.\d+)\.", name)
    assert match, f"hot swap supports decoder-layer adapters only: {name}"
    return match[1] + "."


def prepare(base, adapters, cell, out):
    torch.set_num_threads(4)
    with torch.device("meta"):
        model = AutoModelForImageTextToText.from_config(AutoConfig.from_pretrained(base)).to(torch.float16)
    layers = set()
    for adapter in adapters:
        cfg = PeftConfig.from_pretrained(adapter)
        assert cfg.peft_type == "LORA" and cfg.bias == "none" and not cfg.modules_to_save and not cfg.layer_replication, cfg
        for name, _ in model.named_modules():
            if check_target_module_exists(cfg, name):
                layers.add(layer_prefix(name))
        for name, _ in model.named_parameters():
            if any(name == target or name.endswith("." + target) for target in cfg.target_parameters or []):
                layers.add(layer_prefix(name))
    assert layers, "no hot-swap layers matched"
    names = {n for n, _ in model.named_parameters() if any(n.startswith(p) for p in layers)}
    state = {}
    for shard in sorted(Path(base).glob("*.safetensors")):
        with safe_open(shard, framework="pt", device="cpu") as f:
            state.update({n: f.get_tensor(n) for n in f.keys() if any(n.startswith(p) for p in layers)})
    # Use Transformers' own checkpoint conversions, including split routed experts.
    info, _ = convert_and_load_state_dict_in_model(model, state, LoadStateDictConfig(
        dtype=torch.float16, device_map={"": "cpu"}, weight_mapping=get_model_conversion_mapping(model)))
    assert not (names & info.missing_keys) and not info.mismatched_keys and not info.unexpected_keys, info
    del state
    stages = []
    for adapter, dose in cell:
        model, n_lora, _ = merge_weights.merge_adapter(model, adapter, dose, {})
        with (Path(adapter) / "adapter_model.safetensors").open("rb") as f:
            digest = hashlib.file_digest(f, "sha256").hexdigest()
        stages.append({"adapter": adapter, "scale": dose, "adapter_sha256": digest, "lora_modules": n_lora})
    weights = {n: p.detach().contiguous() for n, p in model.named_parameters() if n in names}
    assert len(weights) == len(names)
    weights = {n: w.contiguous() for n, w in revert_weight_conversion(model, weights).items()}
    save_file(weights, str(out))
    return {"base": str(base), "dtype": "float16", "groups": {}, "adapters": stages,
            "parameters": len(weights), "bytes": sum(w.numel() * w.element_size() for w in weights.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("base", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--adapter", action="append", required=True)
    ap.add_argument("--cell", required=True, help="JSON list of [adapter path, dose], in merge order")
    args = ap.parse_args()
    report = prepare(args.base, args.adapter, json.loads(args.cell), args.out)
    args.out.with_suffix(".json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
