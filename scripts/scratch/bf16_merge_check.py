"""Does merging a LoRA delta into bf16 weights keep it? W ~ N(0, 0.02) [d_out x d_in], delta = low-rank, scaled to a target
relative Frobenius size. Merge as PEFT does for a bf16 model (W.bf16 + delta, result stored in bf16). Report the delta actually kept.
-- PI/Claude"""
import torch
torch.manual_seed(0)
W32 = torch.randn(2048, 2048) * 0.02
W = W32.to(torch.bfloat16)
B, A = torch.randn(2048, 64), torch.randn(64, 2048)
D0 = B @ A
print("| target rel ||ΔW||/||W|| | kept/intended norm | cosine(kept, intended) | share of elements changed |")
print("|--:|--:|--:|--:|")
for rel in [1e-4, 1e-3, 0.004, 0.0147, 0.026, 0.05]:
    D = D0 * (rel * W.float().norm() / D0.norm())
    merged = (W.float() + D).to(torch.bfloat16)  # PEFT merge into a bf16 weight
    kept = merged.float() - W.float()
    print(f"| {rel:g} | {kept.norm()/D.norm():.3f} | {torch.nn.functional.cosine_similarity(kept.flatten(), D.flatten(), 0):.3f} | {(kept != 0).float().mean():.3f} |")
