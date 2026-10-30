"""Does a small overlap add up when the adapters are summed? (wassname 2026-10-30: "that 3% could still add up and make it incoherent")

Per dense module, with the adapters at the given doses: s_i = sigma_max(c_i dW_i), s_sum = sigma_max(sum_i c_i dW_i).
  independent directions:  s_sum ~ max_i s_i ... sqrt(sum s_i^2)
  fully aligned top direction: s_sum = sum_i s_i
alignment = (s_sum - sqrt(sum s_i^2)) / (sum s_i - sqrt(sum s_i^2)), clipped: 0 = adds like independent updates, 1 = top directions
fully aligned (they add linearly). sigma_max of a sum of LoRAs from the stacked factors [B1 B2 B3][A1; A2; A3] (rank <= 3r).
-- PI/Claude (opus-5-5)

.local/axolotl_env/bin/python scripts/scratch/20261030_orth_docs/02_sum_alignment.py docs   # Stoic 0.5, Const 0.5, Other 1 (run 20 lock)
.local/axolotl_env/bin/python scripts/scratch/20261030_orth_docs/02_sum_alignment.py groups # dilemmas 0.25, help 0.25, texts 0.5, identity 0.25
"""
import json
import statistics as st
import sys
from pathlib import Path

import torch
from safetensors import safe_open

A18, A19 = Path.home() / ".local/share/cg_run18_adapters", Path.home() / ".local/share/cg_run19_adapters"
SETS = {"docs": {A18 / "r10_stoic_bf16": 0.5, A18 / "r7e_graft_docs_spl50_bf16": 0.5, A18 / "r10_other_bf16": 1.0},
        "groups": {A19 / "dilemmas": 0.25, A19 / "help": 0.25, A19 / "texts": 0.5, A19 / "identity": 0.25}}


def load(path, dose):
    scale = (c := json.loads((path / "adapter_config.json").read_text()))["lora_alpha"] / c["r"] * dose
    with safe_open(path / "adapter_model.safetensors", "pt") as f:
        return {k.removesuffix(".lora_A.weight"): (f.get_tensor(k.replace("lora_A", "lora_B")).float() * scale, f.get_tensor(k).float())
                for k in f.keys() if k.endswith("lora_A.weight") and ".experts." not in k}


def smax(B, A):
    _, rb = torch.linalg.qr(B)
    _, ra = torch.linalg.qr(A.T)
    return torch.linalg.svdvals(rb @ ra.T)[0].item()


ad = [load(p, c) for p, c in SETS[sys.argv[1]].items()]
align, ratio = [], []
for m in sorted(set.intersection(*(set(a) for a in ad))):
    s = [smax(*a[m]) for a in ad]
    s_sum = smax(torch.cat([a[m][0] for a in ad], 1), torch.cat([a[m][1] for a in ad], 0))
    indep, full = sum(x * x for x in s) ** 0.5, sum(s)
    align.append(min(1.0, max(0.0, (s_sum - indep) / (full - indep))))
    ratio.append(s_sum / indep)
print(f"{sys.argv[1]}: {len(align)} dense modules; alignment median {st.median(align):.2f}, 90th pct {sorted(align)[int(0.9 * len(align))]:.2f}, "
      f"max {max(align):.2f}; sigma_max(sum) / independent: median {st.median(ratio):.2f}, max {max(ratio):.2f} "
      f"(fully aligned would be up to {max(sum(SETS[sys.argv[1]].values()) / sum(c * c for c in SETS[sys.argv[1]].values()) ** 0.5, 1):.2f} for equal s_i)")
