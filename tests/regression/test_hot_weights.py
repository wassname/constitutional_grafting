"""Hot preparation matches the ordinary fp16 PEFT merge, including experts. -- PI/OpenAI"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import torch
from peft import LoraConfig, get_peft_model
from safetensors.torch import load_file
from transformers import AutoModelForImageTextToText, Qwen3_5MoeConfig
from transformers.core_model_loading import revert_weight_conversion

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("hot_weights", ROOT / "scripts/box/hot_weights.py")
hot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hot)


def tiny_config():
    return Qwen3_5MoeConfig(text_config={
        "vocab_size": 32, "hidden_size": 16, "num_hidden_layers": 2, "num_attention_heads": 2,
        "num_key_value_heads": 2, "head_dim": 8, "layer_types": ["full_attention", "full_attention"],
        "num_experts": 4, "num_experts_per_tok": 2, "moe_intermediate_size": 8, "shared_expert_intermediate_size": 8,
        "rope_parameters": {"rope_type": "default", "rope_theta": 10000, "partial_rotary_factor": .5,
                            "mrope_section": [1, 1, 0], "mrope_interleaved": True}},
        vision_config={"depth": 1, "hidden_size": 16, "intermediate_size": 16, "num_heads": 2,
                       "out_hidden_size": 16, "deepstack_visual_indexes": []})


def test_prepare_matches_fp16_merge_and_zero_reset(tmp_path):
    torch.manual_seed(3)
    base = tmp_path / "base"
    AutoModelForImageTextToText.from_config(tiny_config()).to(torch.bfloat16).save_pretrained(base)
    adapters = []
    for layer, target in enumerate(("q_proj", "v_proj")):
        m = AutoModelForImageTextToText.from_pretrained(base, dtype=torch.float16)
        p = get_peft_model(m, LoraConfig(r=2, lora_alpha=4, target_modules=[f"model.language_model.layers.{layer}.self_attn.{target}"],
                                       target_parameters=[f"model.language_model.layers.{layer}.mlp.experts.{name}"
                                                          for name in ("gate_up_proj", "down_proj")]))
        with torch.no_grad():
            for n, w in p.named_parameters():
                if "lora_" in n:
                    w.normal_(std=.15)
        adapter = tmp_path / f"adapter{len(adapters)}"
        p.save_pretrained(adapter)
        adapters.append(str(adapter))
    output = tmp_path / "weights.safetensors"
    for cell in ([(adapters[0], .5), (adapters[1], -.25)], [(adapters[1], 1)], [(adapters[0], 0)]):
        hot.prepare(base, adapters, cell, output)
        actual = load_file(output)
        expected_model = AutoModelForImageTextToText.from_pretrained(base, dtype=torch.float16)
        for adapter, dose in cell:
            expected_model = hot.merge_weights.merge_adapter(expected_model, adapter, dose, {})[0]
        expected = revert_weight_conversion(expected_model, expected_model.state_dict())
        assert any(".experts.0." in n for n in actual)
        assert all(".layers." in n for n in actual)
        for name, weight in actual.items():
            assert torch.equal(weight, expected[name]), (cell, name)
        if cell[0][1] == 0:
            pristine = revert_weight_conversion(expected_model, AutoModelForImageTextToText.from_pretrained(base, dtype=torch.float16).state_dict())
            assert all(torch.equal(w, pristine[n]) for n, w in actual.items())


def test_rejects_non_decoder_targets():
    with pytest.raises(AssertionError, match="decoder-layer adapters only"):
        hot.layer_prefix("lm_head.weight")


def test_hot_preparation_error_aborts_without_cold_fallback(tmp_path):
    base = tmp_path / "base"
    AutoModelForImageTextToText.from_config(tiny_config()).save_pretrained(base)
    adapter = tmp_path / "unsupported"
    LoraConfig(r=2, target_modules=["lm_head"]).save_pretrained(adapter)
    (tmp_path / "manifest.json").write_text('{"input_sha256": {}}')
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"manifest": "manifest.json", "hot_swap": True, "prefix": "test_",
                               "doc_sets": {}, "cells": {"bad": {"a": 1}}, "probe": {}}))
    result = subprocess.run([sys.executable, ROOT / "scripts/box/cells.py", cfg, "--instruct", base,
                             "--run-dir", tmp_path, f"--adapter=a={adapter}", "--cells", "bad", "--probe"],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode != 0
    assert "hot_weights.py" in result.stderr
    assert "decoder-layer adapters only" in (tmp_path / "merge_test_bad.log").read_text()
    assert not (tmp_path / "merged_model").exists()
    assert not list(tmp_path.glob("vllm*"))
