# /// script
# requires-python = ">=3.11"
# dependencies = ["torch", "peft>=0.19.1", "transformers"]
# [tool.uv.sources]
# torch = { index = "pytorch-cpu" }
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
"""Routed-expert LoRA (PEFT target_parameters, Qwen [E,out,in] layout) trains, survives save/reload/merge,
and scaling lora_B by k scales the merged delta by k, as 02_merge.py assumes. CPU, toy module, no downloads.
Run: uv run --script tests/regression/test_moe_expert_merge.py   -- PI/Claude, from slop/research/20261014_qwen35_moe_expert_lora.md"""
import copy
import importlib.util
import tempfile
from pathlib import Path

import torch
from peft import LoraConfig, get_peft_model
from peft.tuners.lora.layer import ParamWrapper
from torch import nn

spec = importlib.util.spec_from_file_location("merge_weights", Path(__file__).resolve().parents[2] / "scripts/train/02_merge.py")
merge_weights = importlib.util.module_from_spec(spec)
spec.loader.exec_module(merge_weights)


class Experts(nn.Module):  # fused 3D params, same names/layout as transformers qwen3_5_moe experts
    def __init__(self):
        super().__init__()
        self.gate_up_proj = nn.Parameter(torch.randn(3, 6, 4) * 0.1)
        self.down_proj = nn.Parameter(torch.randn(3, 4, 3) * 0.1)

    def forward(self, x):
        gate, up = torch.einsum("bh,eoh->beo", x, self.gate_up_proj).chunk(2, -1)
        return torch.einsum("bei,ehi->beh", nn.functional.silu(gate) * up, self.down_proj).sum(1)


class Toy(nn.Module):
    def __init__(self):
        super().__init__()
        self.mlp = nn.Module()
        self.mlp.experts = Experts()

    def forward(self, x):
        return self.mlp.experts(x)


def test_expert_lora_merge_and_k_scaling():
    torch.manual_seed(7)
    base = Toy()
    initial = copy.deepcopy(base.state_dict())
    cfg = LoraConfig(r=2, lora_alpha=4, lora_dropout=0, target_modules=[],
                     target_parameters=["mlp.experts.gate_up_proj", "mlp.experts.down_proj"])
    p = get_peft_model(base, cfg)
    assert len([m for m in p.modules() if isinstance(m, ParamWrapper)]) == 2
    x, y = torch.randn(8, 4), torch.randn(8, 4)
    opt = torch.optim.SGD([w for w in p.parameters() if w.requires_grad], lr=0.5)
    for _ in range(3):
        opt.zero_grad()
        (p(x) - y).square().mean().backward()
        assert all(w.grad is not None and w.grad.norm() > 0 for n, w in p.named_parameters() if "lora_B" in n)
        opt.step()
    p.eval()
    live = p(x).detach()
    with tempfile.TemporaryDirectory() as d:
        p.save_pretrained(d)
        merged = []
        for k in (1.0, 2.0):
            fresh = Toy()
            fresh.load_state_dict(initial)
            merged.append(merge_weights.merge_adapter(fresh, d, k, {})[0])
        torch.testing.assert_close(merged[0](x), live)
        for n in initial:
            d1 = merged[0].state_dict()[n] - initial[n]
            d2 = merged[1].state_dict()[n] - initial[n]
            assert (d1.flatten(1).norm(dim=1) > 0).all(), f"{n}: some expert got no delta"
            torch.testing.assert_close(d2, 2 * d1, atol=1e-7, rtol=1e-4)
        assert not any("lora_" in n for n in merged[0].state_dict())


def test_rank_pattern_applies_to_experts():
    # configs/train/qwen3 use rank_pattern to keep experts at r16 while modules stay r64.
    # PEFT 0.21 warns these keys "did not match any targeted module and were ignored"; the shapes show they apply.
    cfg = LoraConfig(r=8, lora_alpha=16, lora_dropout=0, target_modules=[],
                     target_parameters=["mlp.experts.gate_up_proj", "mlp.experts.down_proj"],
                     rank_pattern={r"mlp\.experts\.gate_up_proj": 2, r"mlp\.experts\.down_proj": 3})
    shapes = {n: tuple(w.shape) for n, w in get_peft_model(Toy(), cfg).named_parameters() if "lora_A" in n}
    assert sorted(s[0] for s in shapes.values()) == [2 * 3, 3 * 3], shapes  # rank * n_experts


def test_two_expert_updates_add_weights_not_factors():
    torch.manual_seed(19)
    initial = Toy().state_dict()
    cfg = LoraConfig(r=2, lora_alpha=4, target_modules=[],
                     target_parameters=["mlp.experts.gate_up_proj", "mlp.experts.down_proj"])
    with tempfile.TemporaryDirectory() as directory:
        paths, deltas = [], []
        for i in range(2):
            base = Toy(); base.load_state_dict(initial)
            adapter = get_peft_model(base, cfg)
            with torch.no_grad():
                for name, weight in adapter.named_parameters():
                    if "lora_B" in name:
                        weight.normal_(std=0.03)
            expected = {}
            for module in adapter.modules():
                if isinstance(module, ParamWrapper):
                    e, out, inp = module.get_param().shape
                    A = module.lora_A["default"].weight.detach().reshape(e, cfg.r, inp)
                    B = module.lora_B["default"].weight.detach().reshape(out, cfg.r, e)
                    expected[f"mlp.experts.{module.parameter_name}"] = torch.einsum("ore,eri->eoi", B, A) * (cfg.lora_alpha / cfg.r)
            path = str(Path(directory) / str(i)); adapter.save_pretrained(path)
            fresh = Toy(); fresh.load_state_dict(initial)
            merged = merge_weights.merge_adapter(fresh, path, 1.0, {})[0]
            for name, weight in merged.state_dict().items():
                torch.testing.assert_close(weight - initial[name], expected[name], atol=1e-7, rtol=1e-5)
            deltas.append(expected)
            paths.append(path)
        for dtype in (torch.float32, torch.float16):
            for a, b in [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (2, 0), (2, 2)]:
                model = Toy().to(dtype); model.load_state_dict(initial)
                model = merge_weights.merge_adapter(model, paths[0], a, {})[0]
                model = merge_weights.merge_adapter(model, paths[1], b, {})[0]
                for name, weight in model.state_dict().items():
                    expected = initial[name].to(dtype)
                    for scale, delta in [(a, deltas[0]), (b, deltas[1])]:
                        expected = expected + (scale * delta[name]).to(dtype)
                    torch.testing.assert_close(weight, expected, atol=1e-7 if dtype == torch.float32 else 5e-5,
                                               rtol=1e-5 if dtype == torch.float32 else 1e-3)
                    if a == b == 0:
                        assert torch.equal(weight, initial[name].to(dtype))


if __name__ == "__main__":
    import peft
    test_expert_lora_merge_and_k_scaling()
    test_rank_pattern_applies_to_experts()
    test_two_expert_updates_add_weights_not_factors()
    print(f"PASS (torch {torch.__version__}, peft {peft.__version__}): routed-expert reload/merge parity; seven two-update combinations in fp32/fp16 against explicit factor products; exact zero-update weights")
