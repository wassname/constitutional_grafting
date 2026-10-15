"""Total update energy of a LoRA adapter, sqrt(sum over modules ||B A||_F^2), routed experts counted per expert.
Used to build a scalar control for a spectral-penalty graft: the plain graft scaled to the same energy.
  energy:  python scripts/train/43_adapter_energy.py REF OTHER          -> prints E_ref, E_other, ratio=E_other/E_ref
  scale :  python scripts/train/43_adapter_energy.py REF OUT --scale r  -> OUT/adapter_model.safetensors = REF with lora_B * r
Both adapters must share r/alpha (same alpha/r factor everywhere), so the factor cancels in the ratio.   -- PI/Claude (Opus 5.5)"""
import argparse
import json
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file


def energy(d: Path) -> float:
    cfg = json.loads((d / "adapter_config.json").read_text())
    r_exp = {v for k, v in cfg["rank_pattern"].items() if "experts" in k}
    assert len(r_exp) == 1, cfg["rank_pattern"]
    r_exp = r_exp.pop()
    f = safe_open(d / "adapter_model.safetensors", "pt")
    total = 0.0
    for ka in [k for k in f.keys() if k.endswith("lora_A.weight")]:
        A, B = f.get_tensor(ka).float(), f.get_tensor(ka.replace("lora_A", "lora_B")).float()
        if ".mlp.experts." in ka:  # PEFT ParamWrapper layout: A [E*r, in] -> [E r in], B [out, r*E] -> [E out r]
            E = A.shape[0] // r_exp
            assert A.shape[0] == E * r_exp and B.shape[1] == E * r_exp, (ka, A.shape, B.shape)
            A3, B3 = A.reshape(E, r_exp, -1), B.reshape(B.shape[0], r_exp, E).permute(2, 0, 1)
            total += float(torch.einsum("eor,eos,eri,esi->", B3, B3, A3, A3))  # sum_e ||B_e A_e||_F^2
        else:
            total += float(torch.einsum("or,os,ri,si->", B, B, A, A))
    return total ** 0.5, cfg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ref", type=Path)
    ap.add_argument("other", type=Path)
    ap.add_argument("--scale", type=float)
    a = ap.parse_args()
    if a.scale is None:
        (e0, c0), (e1, c1) = energy(a.ref), energy(a.other)
        assert (c0["r"], c0["lora_alpha"], c0["rank_pattern"]) == (c1["r"], c1["lora_alpha"], c1["rank_pattern"])
        print(f"E_ref={e0:.4f} E_other={e1:.4f}\nratio={e1 / e0:.3f}")
    else:
        f = safe_open(a.ref / "adapter_model.safetensors", "pt")
        t = {k: f.get_tensor(k) * a.scale if "lora_B" in k else f.get_tensor(k) for k in f.keys()}
        a.other.mkdir(parents=True, exist_ok=True)
        (a.other / "adapter_config.json").write_text((a.ref / "adapter_config.json").read_text())
        save_file(t, a.other / "adapter_model.safetensors", metadata={"format": "pt"})
        e1, _ = energy(a.other)
        print(f"scaled {a.ref} lora_B by {a.scale} -> {a.other} (E={e1:.4f})")
