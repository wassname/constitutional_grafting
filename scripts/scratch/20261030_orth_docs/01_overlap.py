"""Do the document adapters share a component? (wassname 2026-10-30: "the first adapter is actually stoic+terse, const+terse,
other+terse, and when you add them you get 3x terse").

Per dense LoRA module, for each pair of adapters:
  cosine   = <dW_a, dW_b>_F / (|dW_a| |dW_b|)       whole-update alignment
  overlap  = |P_b dW_a|_F^2 / |dW_a|_F^2            share of a's update written into b's output subspace (P_b = U_b U_b^T, U_b
                                                     an orthonormal basis of B_b's columns); random rank-64 subspaces of a d-dim output
                                                     space overlap by about 64/d.
dW = (alpha/r) B A. Routed experts skipped. -- PI/Claude (opus-5-5)

.local/axolotl_env/bin/python scripts/scratch/20261030_orth_docs/01_overlap.py
"""
import itertools
import json
import statistics as st
from pathlib import Path

import torch
from safetensors import safe_open

import sys

A18, A19 = Path.home() / ".local/share/cg_run18_adapters", Path.home() / ".local/share/cg_run19_adapters"
SETS = {"docs": {"stoic": A18 / "r10_stoic_bf16", "const": A18 / "r7e_graft_docs_spl50_bf16", "other": A18 / "r10_other_bf16"},
        "chat19": {g: A19 / g for g in ("dilemmas", "help", "texts", "identity", "all")}}  # run 19 chat adapters (bf16 retrieval)
ADAPTERS = SETS[sys.argv[1] if len(sys.argv) > 1 else "docs"]


def load(path):
    scale = (c := json.loads((path / "adapter_config.json").read_text()))["lora_alpha"] / c["r"]
    out = {}
    with safe_open(path / "adapter_model.safetensors", "pt") as f:
        for k in f.keys():
            if k.endswith("lora_A.weight") and ".experts." not in k:
                out[k.removesuffix(".lora_A.weight")] = (f.get_tensor(k.replace("lora_A", "lora_B")).float() * scale, f.get_tensor(k).float())
    return out


ad = {n: load(p) for n, p in ADAPTERS.items()}
mods = sorted(set.intersection(*(set(a) for a in ad.values())))
print(f"{len(mods)} dense modules\n\n| pair | cosine (median, max abs) | a's share in b's output subspace (median) | chance (median 64/d) |\n|---|---|---|---|")
for a, b in itertools.permutations(ADAPTERS, 2):
    cos, ov, chance = [], [], []
    for m in mods:
        (Ba, Aa), (Bb, Ab) = ad[a][m], ad[b][m]
        dWa, dWb = Ba @ Aa, Bb @ Ab
        cos.append((dWa * dWb).sum().item() / (dWa.norm() * dWb.norm()).item())
        U, _ = torch.linalg.qr(Bb)
        ov.append(((U.T @ dWa).norm() ** 2 / dWa.norm() ** 2).item())
        chance.append(Bb.shape[1] / Bb.shape[0])
    if a < b:
        print(f"| {a} · {b} | {st.median(cos):+.3f}, {max(map(abs, cos)):.3f} | ", end="")
    else:
        print(f"| {a} in {b} | – | ", end="")
    print(f"{st.median(ov):.3f} | {st.median(chance):.3f} |")
