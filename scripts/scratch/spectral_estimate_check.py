"""Power-iteration accuracy on a saved adapter: plugin-style estimate after n iterations from a random v, vs exact sigma_max
(low-rank core SVD). A small spectral gap (flat spectrum) makes few iterations underestimate. -- PI/Claude"""
import json, sys, torch
from safetensors import safe_open
torch.manual_seed(0)
d = sys.argv[1]; cfg = json.load(open(d + "/adapter_config.json")); f = safe_open(d + "/adapter_model.safetensors", "pt")
r_e = list(cfg["rank_pattern"].values())[0]
res = {"lin": {n: [] for n in (1, 2, 4, 8, 32)}, "exp": {n: [] for n in (1, 2, 4, 8, 32)}}
for ka in [k for k in f.keys() if k.endswith("lora_A.weight")]:
    A, B = f.get_tensor(ka).float(), f.get_tensor(ka.replace("lora_A", "lora_B")).float()
    if ".mlp.experts." in ka:
        E = A.shape[0] // r_e; A3, B3 = A.reshape(E, r_e, -1), B.reshape(B.shape[0], r_e, E).permute(2, 0, 1); g = "exp"
    else:
        A3, B3 = A[None], B[None]; g = "lin"
    exact = torch.linalg.svdvals(torch.linalg.qr(B3).R @ torch.linalg.qr(A3.transpose(1, 2)).R.transpose(1, 2))[:, 0]
    keep = exact > 1e-8
    mv = lambda x: torch.einsum("eor,eri,ei->eo", B3, A3, x)
    v = torch.randn(A3.shape[0], A3.shape[2]); v /= v.norm(dim=1, keepdim=True)
    for n in range(1, 33):
        u = mv(v); u = u / (u.norm(dim=1, keepdim=True) + 1e-12)
        v_new = torch.einsum("eri,eor,eo->ei", A3, B3, u); v = v_new / (v_new.norm(dim=1, keepdim=True) + 1e-12)
        if n in res[g]:
            est = (u * mv(v)).sum(1)
            res[g][n].append((est[keep] / exact[keep]).mean())
for g in res:
    print(g, {n: round(float(torch.stack(x).mean()), 3) for n, x in res[g].items()})
