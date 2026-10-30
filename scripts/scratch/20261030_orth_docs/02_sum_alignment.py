"""Does a small overlap add up when the adapters are summed? (wassname 2026-10-30: "that 3% could still add up and make it incoherent")

Per dense module, with the adapters at the given doses: s_i = sigma_max(c_i dW_i), s_sum = sigma_max(sum_i c_i dW_i).
  top directions orthogonal:  s_sum = max_i s_i
  top directions fully aligned (same sign): s_sum = sum_i s_i
alignment = (s_sum - max s_i) / (sum s_i - max s_i): 0 = no reinforcement, 1 = the top directions add linearly. sigma_max of a sum of LoRAs from the stacked factors [B1 B2 B3][A1; A2; A3] (rank <= 3r).
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
align, ratio, names = [], [], []
for m in sorted(set.intersection(*(set(a) for a in ad))):
    s = [smax(*a[m]) for a in ad]
    s_sum = smax(torch.cat([a[m][0] for a in ad], 1), torch.cat([a[m][1] for a in ad], 0))
    top, full = max(s), sum(s)
    align.append((s_sum - top) / (full - top))
    ratio.append(s_sum / top)
    names.append(m.split("layers.")[-1])
q = lambda v, f: sorted(v)[int(f * (len(v) - 1))]
print(f"{sys.argv[1]}: {len(align)} dense modules; alignment median {st.median(align):+.3f}, 10th-90th pct {q(align, .1):+.3f} to {q(align, .9):+.3f}, "
      f"max {max(align):+.3f}; sigma_max(sum) / largest single: median {st.median(ratio):.3f}, max {max(ratio):.3f}")
print("most reinforced modules:", ", ".join(f"{n} {a:+.2f}" for a, n in sorted(zip(align, names), reverse=True)[:6]))
