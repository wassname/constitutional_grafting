"""Remove the shared top direction from a stack of adapters (wassname 2026-10-30: "remove the shared top direction ... then probe
the stack again").

Per dense LoRA module: u = top left singular vector (output space) of the stacked update sum_i c_i dW_i at the doses the stack is used
at; every member's B is projected off u: B_i <- B_i - u (u^T B_i). Each member keeps its own content outside u; the direction that
the members reinforce together is gone. Routed-expert LoRAs are copied unchanged (their layout differs; the overlap measure,
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

removed = {m: [] for m in members}
for mod in mods:
    B = {m: tensors[m][mod + ".lora_B.weight"].float() for m in members}
    A = {m: tensors[m][mod + ".lora_A.weight"].float() for m in members}
    Bs = torch.cat([B[m] * scale[m] * members[m][1] for m in members], 1)
    As = torch.cat([A[m] for m in members], 0)
    qb, rb = torch.linalg.qr(Bs)
    U, _, _ = torch.linalg.svd(rb @ torch.linalg.qr(As.T)[1].T)
    u = qb @ U[:, 0]  # top output direction of the stacked update
    for m in members:
        dW = B[m] @ A[m]
        removed[m].append(((u @ dW).norm() ** 2 / dW.norm() ** 2).item())
        tensors[m][mod + ".lora_B.weight"] = (B[m] - torch.outer(u, u @ B[m])).to(torch.bfloat16)

report = {"set": name, "doses": {m: c for m, (_, c) in members.items()}, "dense_modules": len(mods),
          "energy_removed_median": {m: st.median(v) for m, v in removed.items()}, "energy_removed_max": {m: max(v) for m, v in removed.items()}}
for m, (path, _) in members.items():
    d = out / f"{m}_shared_ablated"
    d.mkdir(parents=True, exist_ok=True)
    save_file({k: (v.to(torch.bfloat16) if v.dtype == torch.float32 else v) for k, v in tensors[m].items()}, d / "adapter_model.safetensors")
    shutil.copyfile(path / "adapter_config.json", d / "adapter_config.json")
(out / f"ablation_{name}.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
