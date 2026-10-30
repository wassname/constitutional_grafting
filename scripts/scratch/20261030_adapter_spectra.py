"""Does the spectral penalty spread the update? Per dense LoRA module, the top singular value's share of the update,
sigma_max / ||dW||_F, and sigma_max itself, for document adapters (lambda 50) and chat adapters (SPECTRAL_FRAC 0.01).
Routed-expert LoRAs are skipped (their layout differs; dense modules suffice for a comparison). dW = (alpha/r) B A;
singular values from the r x r core R_B R_A^T (QR of B and A^T). -- PI/Claude (opus-5-5), run 19 plan FIXME 6

.local/axolotl_env/bin/python scripts/scratch/20261030_adapter_spectra.py
"""
import json
import statistics as st
from pathlib import Path

import torch
from safetensors import safe_open

A17, A18 = Path.home() / ".local/share/cg_run17_adapters", Path.home() / ".local/share/cg_run18_adapters"
R6, R7E = Path.home() / ".local/share/cg_run6_adapters", Path.home() / ".local/share/cg_run7e_adapters"
SAME_DATA = {"doc graft λ0 (plain, run 6)": R6 / "q6_graft_docs", "doc graft λ0.5 (run 6)": R6 / "q6_graft_docs_spl0.5",
             "doc graft λ5 (run 7e)": R7E / "r7e_graft_docs_spl5", "doc graft λ50 (run 7e)": R7E / "r7e_graft_docs_spl50"}  # same data, config, seed
ADAPTERS = SAME_DATA | {"doc Stoic (λ50)": A18 / "r10_stoic_bf16", "doc Const (λ50)": A18 / "r7e_graft_docs_spl50_bf16",
            "doc Other (λ50)": A18 / "r10_other_bf16", "chat newD (frac 0.01)": A18 / "r10_eos_chatr12_bf16",
            "chat reason_docs (frac 0.01)": A17 / "r17_reason_docs_bf16"}


def spectra(path: Path):
    cfg = json.loads((path / "adapter_config.json").read_text())
    scale = cfg["lora_alpha"] / cfg["r"]
    share, top = [], []
    with safe_open(path / "adapter_model.safetensors", "pt") as f:
        for k in f.keys():
            if not k.endswith("lora_A.weight") or ".experts." in k:
                continue
            A, B = f.get_tensor(k).float(), f.get_tensor(k.replace("lora_A", "lora_B")).float()
            _, ra = torch.linalg.qr(A.T)
            _, rb = torch.linalg.qr(B)
            s = torch.linalg.svdvals(rb @ ra.T) * scale
            share.append((s[0] / s.norm()).item())
            top.append(s[0].item())
    return share, top


print("| adapter | dense modules | top direction's share of the update (median) | sigma_max (median) |\n|---|---|---|---|")
for name, path in ADAPTERS.items():
    share, top = spectra(path)
    print(f"| {name} | {len(share)} | {st.median(share):.2f} | {st.median(top):.4f} |")
