"""FP32 LoRA spectral estimates and post-update calibration. -- PI/OpenAI (Sol)"""
import math

import torch


def lora_pairs(model):
    for name, module in model.named_modules():
        if hasattr(module, 'lora_A') and hasattr(module, 'lora_B') and 'default' in getattr(module, 'lora_A', {}):
            A, B = module.lora_A['default'].weight, module.lora_B['default'].weight
            experts = getattr(module, 'num_experts', 1)
            yield name, A.reshape(experts, -1, A.shape[-1]), B.reshape(B.shape[0], -1, experts).permute(2, 0, 1), module.scaling['default']


def spectral_penalty(model, state, n_iter=1):
    device = next(model.parameters()).device.type
    sigmas = []
    with torch.autocast(device_type=device, enabled=False):
        for name, A, B, scale in lora_pairs(model):
            A32, B32 = A.float(), B.float()
            mv = lambda x: torch.einsum('eor,eri,ei->eo', B32, A32, x)
            with torch.no_grad():
                v = state.get(name)
                if v is None or v.device != A.device:
                    v = torch.randn(A.shape[0], A.shape[2], device=A.device)
                    v = v / v.norm(dim=1, keepdim=True)
                for _ in range(n_iter):
                    u = mv(v)
                    u = u / (u.norm(dim=1, keepdim=True) + 1e-8)
                    v_new = torch.einsum('eri,eor,eo->ei', A32, B32, u)
                    norm = v_new.norm(dim=1, keepdim=True)
                    v = torch.where(norm > 0, v_new / norm.clamp_min(1e-12), v)
                state[name] = v
            sigmas.append(scale * (u * mv(v)).sum(1).mean())
    return torch.stack(sigmas).mean()


def calibration_stats(history, fraction):
    assert history and fraction > 0
    assert all(math.isfinite(ce) and math.isfinite(sigma) and ce >= 0 and sigma >= 0 for ce, sigma in history), history
    trained = [(ce, sigma) for ce, sigma in history if sigma > 0]
    if not trained:
        return None
    ce = sum(ce for ce, _ in trained) / len(trained)
    sigma = sum(sigma for _, sigma in trained) / len(trained)
    coefficient = fraction * ce / sigma
    assert math.isfinite(coefficient) and coefficient > 0, coefficient
    return {'lambda': coefficient, 'ce': ce, 'sigma': sigma, 'forwards': len(trained)}
