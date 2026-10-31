"""Remove the shared top direction from a stack of adapters (wassname 2026-10-30: "remove the shared top direction ... then probe
the stack again").

Per dense LoRA module: u = top left singular vector (output space) of the stacked update sum_i c_i dW_i at the doses the stack is used
at. One member, the reference (the one with the most of its update along u, by median over modules), keeps u: it carries the
shared part once (wassname: "obviously there is one you don't ablate as it has the common components"). Every other member's B is
projected off u: B_i <- B_i - u (u^T B_i), keeping its own content outside u. So the stack holds the shared direction once, not
four times. Routed-expert LoRAs are copied unchanged (their layout differs; the overlap measure,
02_sum_alignment.py, covered dense modules only). Writes bf16 adapters plus ablation.json (energy removed per member and module).
-- PI/Claude (opus-5-5)

.local/axolotl_env/bin/python scripts/scratch/20261030_orth_docs/03_ablate_shared.py groups OUT_DIR
"""
import json
import shutil
import statistics as st
import sys
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

A18, A19 = Path.home() / ".local/share/cg_run18_adapters", Path.home() / ".local/share/cg_run19_adapters"
SETS = {"docs": {"stoic": (A18 / "r10_stoic_bf16", 0.5), "const": (A18 / "r7e_graft_docs_spl50_bf16", 0.5), "other": (A18 / "r10_other_bf16", 1.0)},
        "groups": {g: (A19 / g, c) for g, c in (("dilemmas", 0.25), ("help", 0.25), ("texts", 0.5), ("identity", 0.25))}}
name, out = sys.argv[1], Path(sys.argv[2])
members = SETS[name]

tensors, scale = {}, {}
for m, (path, _) in members.items():
    cfg = json.loads((path / "adapter_config.json").read_text())
    scale[m] = cfg["lora_alpha"] / cfg["r"]
    with safe_open(path / "adapter_model.safetensors", "pt") as f:
        tensors[m] = {k: f.get_tensor(k) for k in f.keys()}
mods = sorted({k.removesuffix(".lora_A.weight") for k in tensors[next(iter(members))] if k.endswith("lora_A.weight") and ".experts." not in k})

along = {m: [] for m in members}
us = {}
for mod in mods:
    B = {m: tensors[m][mod + ".lora_B.weight"].float() for m in members}
    A = {m: tensors[m][mod + ".lora_A.weight"].float() for m in members}
    Bs = torch.cat([B[m] * scale[m] * members[m][1] for m in members], 1)
    As = torch.cat([A[m] for m in members], 0)
    qb, rb = torch.linalg.qr(Bs)
    U, _, _ = torch.linalg.svd(rb @ torch.linalg.qr(As.T)[1].T)
    us[mod] = qb @ U[:, 0]  # top output direction of the stacked update
    for m in members:
        dW = B[m] @ A[m]
        along[m].append(((us[mod] @ dW).norm() ** 2 / dW.norm() ** 2).item())
reference = max(members, key=lambda m: st.median(along[m]))
removed = {m: [] for m in members if m != reference}
for mod in mods:
    u = us[mod]
    for m in removed:
        B = tensors[m][mod + ".lora_B.weight"].float()
        removed[m].append(((u @ (B @ tensors[m][mod + ".lora_A.weight"].float())).norm() ** 2
                           / (B @ tensors[m][mod + ".lora_A.weight"].float()).norm() ** 2).item())
        tensors[m][mod + ".lora_B.weight"] = (B - torch.outer(u, u @ B)).to(torch.bfloat16)

report = {"set": name, "doses": {m: c for m, (_, c) in members.items()}, "dense_modules": len(mods), "reference_kept_whole": reference,
          "share_along_u_median": {m: st.median(v) for m, v in along.items()},
          "energy_removed_median": {m: st.median(v) for m, v in removed.items()}, "energy_removed_max": {m: max(v) for m, v in removed.items()}}
for m, (path, _) in members.items():
    d = out / (f"r19o_{m}_kept_bf16" if m == reference else f"r19o_{m}_shared_ablated_bf16")
    d.mkdir(parents=True, exist_ok=True)
    save_file({k: (v.to(torch.bfloat16) if v.dtype == torch.float32 else v) for k, v in tensors[m].items()}, d / "adapter_model.safetensors")
    shutil.copyfile(path / "adapter_config.json", d / "adapter_config.json")
(out / f"ablation_{name}.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
