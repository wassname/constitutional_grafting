# /// script
# dependencies = ["torch", "safetensors"]
# [tool.uv.sources]
# torch = { index = "pytorch-cpu" }
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
# Singular values of the graft update dW = (alpha/r) B A per module: how concentrated is it? PI/Claude
import json, re, torch, statistics as st
from safetensors import safe_open
d=".local/run3_box/graft"; cfg=json.load(open(f"{d}/adapter_config.json")); s=cfg["lora_alpha"]/cfg["r"]
f=safe_open(f"{d}/adapter_model.safetensors","pt")
keys=[k for k in f.keys() if "lora_A" in k]
rows=[]
for k in keys:
    m=re.search(r"layers\.(\d+)\.(.*)\.lora_A",k); L=int(m.group(1)); mod=m.group(2).split(".")[-1]
    if L % 6 and L not in (59,): continue
    A=f.get_tensor(k).float(); B=f.get_tensor(k.replace("lora_A","lora_B")).float()
    # singular values of B@A via small QR
    qb,rb=torch.linalg.qr(B); qa,ra=torch.linalg.qr(A.T)
    sv=torch.linalg.svdvals(rb@ra.T)*s
    e=sv**2; c=torch.cumsum(e,0)/e.sum()
    rows.append((L,mod,float(sv[0]),float(sv[0]/sv[min(9,len(sv)-1)]),int((c<0.5).sum())+1,int((c<0.9).sum())+1))
print("layer module | sigma1 | sigma1/sigma10 | k for 50%% energy | k for 90%% energy (of r=%d)"%cfg["r"])
for r in rows: print(*r[:2], "| %.3f | %.1f | %d | %d"%r[2:])
print("median k50 %.0f, k90 %.0f; median sigma1/sigma10 %.1f"%(st.median(r[4] for r in rows), st.median(r[5] for r in rows), st.median(r[3] for r in rows)))
