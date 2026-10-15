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
    return [torch.linalg.svdvals(s * (B.float() @ A.float())) for _, A, B, s in lora_pairs(model)]


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
    s0, r0, s1, r1 = test_penalty_lowers_sigma_max()
    print(f"PASS: penalty matches SVD sigma_max; lam=0 sigma1 {s0:.3f} (s1/s2 {r0:.1f}) -> lam=1 sigma1 {s1:.3f} (s1/s2 {r1:.1f})")
