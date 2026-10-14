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
import tempfile

import torch
from peft import LoraConfig, PeftModel, get_peft_model
from peft.tuners.lora.layer import ParamWrapper
from torch import nn


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
            q = PeftModel.from_pretrained(fresh, d)
            with torch.no_grad():  # same loop as scripts/train/02_merge.py
                for n, w in q.named_parameters():
                    if "lora_B" in n:
                        w.mul_(k)
            merged.append(q.merge_and_unload(safe_merge=True))
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


if __name__ == "__main__":
    import peft
    test_expert_lora_merge_and_k_scaling()
    test_rank_pattern_applies_to_experts()
    print(f"PASS (torch {torch.__version__}, peft {peft.__version__}): every expert changed; reload/merge parity; delta(k=2)=2*delta(k=1)")
