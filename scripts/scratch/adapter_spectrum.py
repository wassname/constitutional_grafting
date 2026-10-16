"""Exact per-module spectrum of a saved LoRA adapter (experts per expert): mean sigma_max (the spectral_plugin definition), mean
top-direction energy share, mean stable rank. usage: uv run --with safetensors --with torch --with numpy python scripts/scratch/adapter_spectrum.py DIR...  -- PI/Claude"""
import json, sys, torch
from safetensors import safe_open
for d in sys.argv[1:]:
    cfg = json.load(open(d + "/adapter_config.json")); f = safe_open(d + "/adapter_model.safetensors", "pt")
    sc = cfg["lora_alpha"] / cfg["r"]; r_e = list(cfg["rank_pattern"].values())[0]; sc_e = list(cfg["alpha_pattern"].values())[0] / r_e
    rows = {"lin": [], "exp": []}
    for ka in [k for k in f.keys() if k.endswith("lora_A.weight")]:
        A, B = f.get_tensor(ka).float(), f.get_tensor(ka.replace("lora_A", "lora_B")).float()
        if ".mlp.experts." in ka:
            E = A.shape[0] // r_e; A3, B3 = A.reshape(E, r_e, -1), B.reshape(B.shape[0], r_e, E).permute(2, 0, 1)
            s = torch.linalg.svdvals(torch.linalg.qr(B3).R @ torch.linalg.qr(A3.transpose(1, 2)).R.transpose(1, 2)) * sc_e
            rows["exp"].append((s[:, 0].mean(), (s[:, 0] ** 2 / (s ** 2).sum(1)).mean(), ((s ** 2).sum(1) / s[:, 0] ** 2).mean(), (s ** 2).sum().sqrt()))
        else:
            s = torch.linalg.svdvals(torch.linalg.qr(B).R @ torch.linalg.qr(A.T).R.T) * sc
            rows["lin"].append((s[0], s[0] ** 2 / (s ** 2).sum(), (s ** 2).sum() / s[0] ** 2, (s ** 2).sum().sqrt()))
    allr = rows["lin"] + rows["exp"]
    m = lambda xs, i: float(torch.stack([x[i] for x in xs]).mean())
    print(f"{d}\n  all {len(allr)} modules: sigma_max mean {m(allr,0):.4f} | top share {m(allr,1):.3f} | stable rank {m(allr,2):.2f} | Frobenius mean {m(allr,3):.3f}")
    for k, xs in rows.items():
        print(f"  {k} {len(xs)}: sigma_max mean {m(xs,0):.4f} | top share {m(xs,1):.3f} | stable rank {m(xs,2):.2f} | Frobenius mean {m(xs,3):.3f}")
