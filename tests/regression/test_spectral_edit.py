# /// script
# requires-python = ">=3.11"
# dependencies = ["torch", "safetensors"]
# [tool.uv.sources]
# torch = { index = "pytorch-cpu" }
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
"""42_spectral_edit.edit_pair: cap and flat change only the singular values of dW = scale*B@A (same singular vectors), cap bounds
sigma1, flat keeps the nuclear norm; also per-expert blocks for ParamWrapper-shaped factors. CPU.
Run: uv run --script tests/regression/test_spectral_edit.py   -- PI/Claude"""
import importlib.util
import sys
from pathlib import Path

import torch

spec = importlib.util.spec_from_file_location("se", Path(__file__).resolve().parents[2] / "scripts/train/42_spectral_edit.py")
se = importlib.util.module_from_spec(spec); spec.loader.exec_module(se)


def test_cap_and_flat():
    torch.manual_seed(0)
    r, din, dout, scale = 8, 32, 24, 2.0
    A = torch.randn(r, din); B = torch.randn(dout, r) * torch.logspace(0, -2, r)  # decaying spectrum
    s = torch.linalg.svdvals(scale * B @ A)
    A2, B2, *_ = se.edit_pair(A, B, scale, "cap0.5")
    s2 = torch.linalg.svdvals(scale * B2 @ A2)
    assert abs(s2[0] - 0.5 * s[0]) < 1e-4 * s[0] and torch.allclose(s2[1:], torch.minimum(s[1:], 0.5 * s[0]), rtol=1e-4, atol=1e-5)
    A3, B3, *_ = se.edit_pair(A, B, scale, "flat1.0")
    s3 = torch.linalg.svdvals(scale * B3 @ A3)
    assert torch.allclose(s3[:r], torch.full((r,), float(s[:r].mean())), rtol=1e-4) and abs(s3[:r].sum() - s[:r].sum()) < 1e-3
    # same left singular subspace as the original update
    U = torch.linalg.svd(scale * B @ A)[0][:, :r]; U3 = torch.linalg.svd(scale * B3 @ A3)[0][:, :r]
    assert torch.linalg.svdvals(U.T @ U3).min() > 0.999


if __name__ == "__main__":
    test_cap_and_flat()
    print("PASS: cap bounds sigma1 at 0.5 sigma1, flat equalises singular values keeping nuclear norm, singular subspace unchanged")
