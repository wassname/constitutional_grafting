"""HF streaming math, reset, patterns and vLLM coverage guards. -- PI/OpenAI"""
import importlib.util
import json
import subprocess
import sys
from types import SimpleNamespace
from pathlib import Path

import pytest
import torch
from peft import LoraConfig, get_peft_model
from safetensors.torch import save_file
from transformers import AutoModelForImageTextToText, Qwen3_5MoeConfig

ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


hot = module("hot_weights", "scripts/box/hot_weights.py")
worker = module("hot_worker", "scripts/box/hot_worker.py")
merge = module("merge_weights", "scripts/train/02_merge.py")


def tiny_config():
    return Qwen3_5MoeConfig(text_config={
        "vocab_size": 32, "hidden_size": 16, "num_hidden_layers": 2, "num_attention_heads": 2,
        "num_key_value_heads": 2, "head_dim": 8, "layer_types": ["full_attention", "full_attention"],
        "num_experts": 4, "num_experts_per_tok": 2, "moe_intermediate_size": 8, "shared_expert_intermediate_size": 8,
        "rope_parameters": {"rope_type": "default", "rope_theta": 10000, "partial_rotary_factor": .5,
                            "mrope_section": [1, 1, 0], "mrope_interleaved": True}},
        vision_config={"depth": 1, "hidden_size": 16, "intermediate_size": 16, "num_heads": 2,
                       "out_hidden_size": 16, "deepstack_visual_indexes": []})


@pytest.mark.parametrize("fused", [False, True])
@pytest.mark.parametrize("stored_dtype", [torch.bfloat16, torch.float16])
def test_stream_matches_peft_math_and_pristine_reset(tmp_path, monkeypatch, fused, stored_dtype):
    # CPU unit test only; real 02_merge.py GPU and packed-weight equivalence live in hot_smoke.py.
    monkeypatch.setattr(torch.Tensor, "pin_memory", lambda self: self)
    torch.manual_seed(3)
    base = tmp_path / "base"
    pristine = AutoModelForImageTextToText.from_config(tiny_config()).to(torch.bfloat16)
    pristine.save_pretrained(base)
    if fused:
        save_file(pristine.state_dict(), base / "model.safetensors", metadata={"format": "pt"})
    adapters = []
    for layer, target in enumerate(("q_proj", "v_proj")):
        m = AutoModelForImageTextToText.from_pretrained(base, dtype=torch.float16)
        p = get_peft_model(m, LoraConfig(r=2, lora_alpha=4, target_modules=[f"model.language_model.layers.{layer}.self_attn.{target}"],
                                       target_parameters=[f"model.language_model.layers.{layer}.mlp.experts.{name}"
                                                          for name in ("gate_up_proj", "down_proj")],
                                       rank_pattern={r"mlp\.experts\.gate_up_proj": 3},
                                       alpha_pattern={r"mlp\.experts\.gate_up_proj": 7}, use_rslora=True))
        with torch.no_grad():
            for n, w in p.named_parameters():
                if "lora_" in n:
                    w.normal_(std=.15)
        adapter = tmp_path / f"adapter{len(adapters)}"
        p.to(stored_dtype).save_pretrained(adapter)
        adapters.append(str(adapter))
    stream = hot.HotWeights(base, adapters)
    assert all(w.dtype == stored_dtype for a in stream.adapters.values() for pair in a.factors.values() for w in pair.values())
    initial = {n: w.clone() for n, w in stream.pristine.items()}
    def no_reread(*args, **kwargs):
        raise AssertionError("per-cell checkpoint reread")
    monkeypatch.setattr(hot, "safe_open", no_reread)
    for cell in ([(adapters[0], .5), (adapters[1], -.25)], [(adapters[1], 1)], [(adapters[0], 0)]):
        actual = dict(stream.weights(cell, "cpu"))
        expected_model = AutoModelForImageTextToText.from_pretrained(base, dtype=torch.float16)
        for adapter, dose in cell:
            expected_model = merge.merge_adapter(expected_model, adapter, dose, {})[0]
        expected = expected_model.state_dict()
        for name, weight in actual.items():
            match = hot.re.match(r"(.+\.experts)\.(\d+)\.(gate|up|down)_proj\.weight$", name)
            if match:
                prefix, index, projection = match.groups()
                value = expected[prefix + (".down_proj" if projection == "down" else ".gate_up_proj")][int(index)]
                if projection != "down":
                    value = value.chunk(2, dim=0)[projection == "up"]
            else:
                value = expected[name]
            assert torch.equal(weight, value), (cell, name)
        assert all(torch.equal(w, initial[n]) for n, w in stream.pristine.items())
        if cell[0][1] == 0:
            assert all(torch.equal(w, initial[n]) for n, w in actual.items())


def test_rejects_non_decoder_targets():
    with pytest.raises(AssertionError, match="decoder-layer adapters only"):
        hot.layer_prefix("lm_head.weight")


def test_checked_load_rejects_partial_layer_and_restores_method():
    class Model:
        def named_parameters(self):
            return [("language_model.model.layers.0.qkv.weight", None), ("language_model.model.layers.0.norm.weight", None)]

        def load_weights(self, weights):
            return {"language_model.model.layers.0.qkv.weight"}

    model = Model()
    original = model.load_weights
    with pytest.raises(AssertionError, match="unloaded hot parameters.*norm.weight"):
        with worker.checked_load(model, {"model.language_model.layers.0."}):
            model.load_weights(iter(()))
    assert model.load_weights == original


def test_checked_load_rejects_missing_packed_shards(monkeypatch):
    class Model:
        def named_parameters(self):
            return [("language_model.model.layers.0.mlp.experts.routed_experts.w13_weight", None)]

        def named_modules(self):
            return [("language_model.model.layers.0.mlp.experts.routed_experts", self)]

        def load_weights(self, weights):
            return {"language_model.model.layers.0.mlp.experts.w13_weight"}

    info = SimpleNamespace(can_load=lambda: True, load_numel=1, load_numel_total=3)
    monkeypatch.setitem(sys.modules, "vllm.model_executor.model_loader.reload.layerwise", SimpleNamespace(get_layerwise_info=lambda _: info))
    model = Model()
    with pytest.raises(AssertionError, match="partially loaded hot layer"):
        with worker.checked_load(model, {"model.language_model.layers.0."}):
            model.load_weights(iter(()))
    info.load_numel = 3
    with worker.checked_load(model, {"model.language_model.layers.0."}):
        model.load_weights(iter(()))


def test_hot_preflight_error_aborts_without_server_or_cold_fallback(tmp_path):
    adapter = tmp_path / "unsupported"
    LoraConfig(r=2, target_modules=["lm_head"]).save_pretrained(adapter)
    save_file({"base_model.model.lm_head.lora_A.weight": torch.zeros(2, 4)}, adapter / "adapter_model.safetensors")
    (tmp_path / "manifest.json").write_text('{"input_sha256": {}}')
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"manifest": "manifest.json", "hot_swap": True, "prefix": "test_",
                               "doc_sets": {}, "cells": {"bad": {"a": 1}}, "probe": {}}))
    result = subprocess.run([sys.executable, ROOT / "scripts/box/cells.py", cfg, "--instruct", tmp_path,
                             "--run-dir", tmp_path, f"--adapter=a={adapter}", "--cells", "bad", "--probe"],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode != 0
    assert "decoder-layer adapters only" in result.stderr
    assert not (tmp_path / "merged_model").exists()
    assert not list(tmp_path.glob("vllm*"))


@pytest.mark.parametrize("drift_at_init", [False, True])
def test_adapter_targets_must_map_and_apply_each_nonzero_cell(tmp_path, monkeypatch, drift_at_init):
    monkeypatch.setattr(torch.Tensor, "pin_memory", lambda self: self)
    base, adapter = tmp_path / "base", tmp_path / "adapter"
    base.mkdir()
    (base / "config.json").write_text('{}')
    target = "model.layers.0.self_attn.q_proj"
    other = target.replace("q_proj", "v_proj")
    save_file({n + ".weight": torch.ones(4, 4).half() for n in (target, other)}, base / "model.safetensors")
    LoraConfig(r=2, lora_alpha=4, target_modules=["q_proj", "v_proj"]).save_pretrained(adapter)
    factor_target = target.replace("q_proj", "unknown_proj") if drift_at_init else target
    save_file({f"base_model.model.{n}.lora_{side}.weight": torch.ones(2, 4).half() if side == "A"
               else torch.ones(4, 2).half() for n in (factor_target, other) for side in ("A", "B")},
              adapter / "adapter_model.safetensors")
    path = str(adapter)
    if drift_at_init:
        with pytest.raises(AssertionError, match="targets missing from pristine.*unknown_proj"):
            hot.HotWeights(base, [path])
        return
    stream = hot.HotWeights(base, [path])
    assert dict(stream.weights([(path, 0), (path, 1), (path, -.25)], "cpu"))
    original_delta = stream.adapters[path].delta
    monkeypatch.setattr(stream.adapters[path], "delta", lambda n, *args: None if n == target + ".weight" else original_delta(n, *args))
    assert dict(stream.weights([(path, 0)], "cpu"))
    with pytest.raises(AssertionError, match="targets not applied this cell.*q_proj"):
        dict(stream.weights([(path, 1)], "cpu"))
