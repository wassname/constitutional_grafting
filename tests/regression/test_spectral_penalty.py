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
"""spectral_penalty (scripts/train/spectral_plugin.py) matches the true top singular value of (alpha/r) B A after warm-started
power iteration, and training with it lowers sigma_max relative to sigma_2 vs training without. CPU, toy model.
Run: uv run --script tests/regression/test_spectral_penalty.py   -- PI/Claude"""
import sys
import types
from pathlib import Path

import torch
from peft import LoraConfig, get_peft_model
from torch import nn

sys.modules.setdefault("axolotl", types.ModuleType("axolotl"))  # plugin imports BasePlugin; stub it for a CPU test
sys.modules.setdefault("axolotl.integrations", types.ModuleType("axolotl.integrations"))
base_mod = types.ModuleType("axolotl.integrations.base"); base_mod.BasePlugin = object
sys.modules["axolotl.integrations.base"] = base_mod
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "train"))
from spectral_plugin import lora_pairs, spectral_penalty  # noqa: E402


def toy():
    torch.manual_seed(0)
    m = nn.Sequential(nn.Linear(16, 32), nn.ReLU(), nn.Linear(32, 16))
    return get_peft_model(m, LoraConfig(r=8, lora_alpha=16, target_modules=["0", "2"], lora_dropout=0))


def true_sigmas(model):
    return [torch.linalg.svdvals(s * (B[0].float() @ A[0].float())) for _, A, B, s in lora_pairs(model)]


class Experts(nn.Module):  # fused 3D params, Qwen3.5 MoE layout [E, out, in], as in test_moe_expert_merge.py
    def __init__(self):
        super().__init__()
        self.gate_up_proj = nn.Parameter(torch.randn(5, 6, 4) * 0.1)
        self.down_proj = nn.Parameter(torch.randn(5, 4, 3) * 0.1)

    def forward(self, x):
        gate, up = torch.einsum("bh,eoh->beo", x, self.gate_up_proj).chunk(2, -1)
        return torch.einsum("bei,ehi->beh", nn.functional.silu(gate) * up, self.down_proj).sum(1)


def test_expert_lora_matches_peft_delta():
    """Expert penalty = mean over modules of mean over experts of sigma_max of PEFT's own get_delta_weight."""
    from peft.tuners.lora.layer import ParamWrapper
    torch.manual_seed(0)
    m = nn.Module(); m.mlp = nn.Module(); m.mlp.experts = Experts(); m.forward = lambda x: m.mlp.experts(x)
    p = get_peft_model(m, LoraConfig(r=2, lora_alpha=4, lora_dropout=0, target_modules=[],
                                     target_parameters=["mlp.experts.gate_up_proj", "mlp.experts.down_proj"]))
    with torch.no_grad():
        for n, w in p.named_parameters():
            if "lora_" in n:
                w.normal_(0, 0.3)
    wrappers = [w for w in p.modules() if isinstance(w, ParamWrapper)]
    assert len(wrappers) == 2 and all(w.num_experts == 5 for w in wrappers)
    state = {}
    for _ in range(100):
        pen = spectral_penalty(p, state)
    expect = torch.stack([torch.linalg.matrix_norm(w.get_delta_weight("default").float(), ord=2).mean() for w in wrappers]).mean()
    torch.testing.assert_close(pen.detach(), expect, rtol=1e-3, atol=1e-6)
    pen.backward()
    assert all(w.grad is not None and w.grad.norm() > 0 for n, w in p.named_parameters() if "lora_" in n)


def test_matches_svd_after_warm_iterations():
    m = toy()
    with torch.no_grad():
        for _, A, B, _ in lora_pairs(m):
            B.normal_(0, 0.1)
    state = {}
    for _ in range(50):
        pen = spectral_penalty(m, state)
    expect = torch.stack([s[0] for s in true_sigmas(m)]).mean()
    torch.testing.assert_close(pen.detach(), expect, rtol=1e-3, atol=1e-5)


def train(lam):
    m = toy()
    g = torch.Generator().manual_seed(1)
    x = torch.randn(256, 16, generator=g)
    y = x @ (torch.randn(16, 1, generator=g) @ torch.randn(1, 16, generator=g)) * 3  # rank-1 target: pulls one direction hard
    opt = torch.optim.Adam([p for p in m.parameters() if p.requires_grad], lr=1e-2)
    state = {}
    for _ in range(300):
        opt.zero_grad()
        loss = (m(x) - y).square().mean() + lam * spectral_penalty(m, state)
        loss.backward(); opt.step()
    s = [t.detach() for t in true_sigmas(m)][0]
    return float(s[0]), float(s[0] / s[1])


def test_penalty_lowers_sigma_max():
    s0, r0 = train(0.0)
    s1, r1 = train(1.0)
    assert s1 < s0 and r1 < r0, (s0, r0, s1, r1)
    return s0, r0, s1, r1


if __name__ == "__main__":
    test_matches_svd_after_warm_iterations()
    test_expert_lora_matches_peft_delta()
    s0, r0, s1, r1 = test_penalty_lowers_sigma_max()
    print(f"PASS: penalty matches SVD sigma_max; lam=0 sigma1 {s0:.3f} (s1/s2 {r0:.1f}) -> lam=1 sigma1 {s1:.3f} (s1/s2 {r1:.1f})")
