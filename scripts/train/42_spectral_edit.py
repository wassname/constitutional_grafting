# /// script
# requires-python = ">=3.11"
# dependencies = ["torch", "safetensors", "numpy"]
# ///
"""Post-hoc spectral edits of a LoRA adapter, with energy-matched scalar controls (slop/research/20261015_spectral_norm_lora.md):
  cap{t}    : each module's singular values capped at t * sigma1           (dW' = U min(s, t s1) V^T)
  flat{b}   : s' = (1-b) s + b mean(s), nuclear mass kept                   (b=1 is Iso-C / LoRA-Norm flat-nuclear)
  scal_X    : plain scalar c * dW with c chosen per module so ||dW'||_F matches edit X (separates shape from size)
Works on the low-rank factors (QR + r x r SVD), no dense dW. Linear LoRA (A: r x in, B: out x r) and PEFT ParamWrapper experts
(A: r*E x in, B: out x r*E, one rank-r block per expert). Output adapters keep alpha/r; B carries the edit.
usage: uv run scripts/train/42_spectral_edit.py ADAPTER_DIR OUT_ROOT [cap0.5 flat1.0 ...]   -- PI/Claude (Opus 5.5)"""
import json
import re
import shutil
import sys
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file


def edit_pair(A, B, scale, how):
    """A: r x in, B: out x r, dW = scale * B @ A. Returns (A', B') with dW' edited; A' has orthonormal rows."""
    qb, rb = torch.linalg.qr(B.double())                 # B = qb rb
    qa, ra = torch.linalg.qr(A.double().T)               # A^T = qa ra
    u, s, vh = torch.linalg.svd(scale * rb @ ra.T)       # dW = qb u diag(s) vh qa^T
    kind, val = re.match(r"([a-z]+)([\d.]+)", how).groups()
    val = float(val)
    if kind == "cap":
        s2 = torch.minimum(s, val * s[0])
    elif kind == "flat":
        keep = s > s[0] * 1e-6                            # do not invent directions from numerical zeros
        s2 = s.clone(); s2[keep] = (1 - val) * s[keep] + val * s[keep].mean()
    else:
        raise ValueError(how)
    U, V = qb @ u, qa @ vh.T                              # out x r, in x r
    return V.T.to(A.dtype), (U * s2 / scale).to(B.dtype), float(s.norm()), float(s2.norm())


def run(adapter, out_root, edits):
    cfg = json.loads((adapter / "adapter_config.json").read_text())
    W = load_file(adapter / "adapter_model.safetensors")
    a_keys = [k for k in W if "lora_A" in k]
    report = {}
    for how in edits:
        new, norms = dict(W), {}
        for ka in a_keys:
            kb = ka.replace("lora_A", "lora_B")
            A, B = W[ka].float(), W[kb].float()
            r = cfg["rank_pattern"].get(next((p for p in cfg.get("rank_pattern", {}) if re.search(p, ka)), ""), cfg["r"]) if cfg.get("rank_pattern") else cfg["r"]
            alpha = cfg["alpha_pattern"].get(next((p for p in cfg.get("alpha_pattern", {}) if re.search(p, ka)), ""), cfg["lora_alpha"]) if cfg.get("alpha_pattern") else cfg["lora_alpha"]
            scale = alpha / r
            E = A.shape[0] // r                            # 1 for Linear LoRA, n_experts for ParamWrapper
            Ab, Bb, f0, f1 = [], [], 0.0, 0.0
            for e in range(E):
                a, b, n0, n1 = edit_pair(A[e * r:(e + 1) * r], B[:, e * r:(e + 1) * r], scale, how)
                Ab.append(a); Bb.append(b); f0 += n0 ** 2; f1 += n1 ** 2
            new[ka], new[kb] = torch.cat(Ab, 0).to(W[ka].dtype), torch.cat(Bb, 1).to(W[kb].dtype)
            norms[ka] = (f0 ** 0.5, f1 ** 0.5)
        for name, tensors in [(how, new), (f"scal_{how}", {**W, **{ka.replace("lora_A", "lora_B"): (W[ka.replace("lora_A", "lora_B")].float() * (n1 / n0)).to(W[ka].dtype)
                                                                   for ka, (n0, n1) in norms.items() if n0 > 0}})]:
            d = out_root / name
            d.mkdir(parents=True, exist_ok=True)
            save_file(tensors, d / "adapter_model.safetensors")
            shutil.copy(adapter / "adapter_config.json", d / "adapter_config.json")
        ratio = [n1 / n0 for n0, n1 in norms.values() if n0 > 0]
        report[how] = {"modules": len(norms), "frobenius_ratio_mean": sum(ratio) / len(ratio), "frobenius_ratio_min": min(ratio)}
        print(how, report[how], flush=True)
    (out_root / "spectral_edit_report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    run(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:] or ["cap0.5", "flat1.0"])
