"""Axolotl plugin: add a spectral-norm penalty on each LoRA update to the training loss.
loss += spectral_lam * mean over LoRA modules of sigma_max(dW), dW = (alpha/r) B A.
Scaling a graft by k multiplies every singular value of dW by k; the run-3 Gemma graft has one gate_proj direction holding
~50% of the update energy (scripts/scratch/graft_spectrum.py), so k x mostly pushes along it. Penalising sigma_max may spread
the update or may just shrink it; compare against a scalar-strength control. Precedents act on the update, not W0+dW (SCLoRA,
NB-LoRA; slop/research/20261015_spectral_norm_lora.md). Pick lam so the penalty is ~1% of CE after warmup: lam0 = 0.01*CE/P,
then sweep {0, 0.1, 1, 10} x lam0. Untested on our data; from wassname's steer-heal-love `_spectral_div` (power iteration,
u and v held constant so the gradient flows through A and B). One power-iteration step per training step, warm-started.
Covers nn.Linear LoRA and PEFT ParamWrapper routed experts (target_parameters): an expert module's sigma is the mean over
its experts of sigma_max(B_e A_e), so each module counts once in the mean whatever its expert count.
Config: plugins: [scripts.train.spectral_plugin.SpectralPlugin]; SPECTRAL_LAM defaults to 50; 0 = plain graft. -- PI/OpenAI (Sol)
SPECTRAL_FRAC=f (e.g. 0.01) instead fixes lam once at the end of warmup to f * mean CE / mean sigma over the last 10 warmup steps
(lam = 0 before then); used for chat stages (wassname: spectral on every stage, ~1% of the loss). Logs ce_loss and spectral_lam. -- PI/Claude"""
import os

import torch
from axolotl.integrations.base import BasePlugin


def lora_pairs(model):
    """(name, A [E r in], B [E out r], scale); E=1 for nn.Linear LoRA. Expert layout follows PEFT ParamWrapper.get_delta_weight."""
    for name, m in model.named_modules():
        if hasattr(m, "lora_A") and hasattr(m, "lora_B") and "default" in getattr(m, "lora_A", {}):
            A, B, E = m.lora_A["default"].weight, m.lora_B["default"].weight, getattr(m, "num_experts", 1)
            yield name, A.reshape(E, -1, A.shape[-1]), B.reshape(B.shape[0], -1, E).permute(2, 0, 1), m.scaling["default"]


def spectral_penalty(model, state: dict, n_iter: int = 1) -> torch.Tensor:
    """Mean over LoRA modules of sigma_max(dW) (expert modules: mean over experts). state caches right singular vectors."""
    sigmas = []
    for name, A, B, scale in lora_pairs(model):
        A32, B32 = A.float(), B.float()  # [E r in], [E out r]
        mv = lambda x: torch.einsum("eor,eri,ei->eo", B32, A32, x)
        with torch.no_grad():
            v = state.get(name)
            if v is None or v.device != A.device:
                v = torch.randn(A.shape[0], A.shape[2], device=A.device); v = v / v.norm(dim=1, keepdim=True)
            for _ in range(n_iter):
                u = mv(v); u = u / (u.norm(dim=1, keepdim=True) + 1e-8)
                v_new = torch.einsum("eri,eor,eo->ei", A32, B32, u)
                n = v_new.norm(dim=1, keepdim=True)
                v = torch.where(n > 0, v_new / n.clamp_min(1e-12), v)  # LoRA B starts at zero: keep the old v, not a zero one
            state[name] = v
        sigmas.append(scale * (u * mv(v)).sum(1).mean())
    return torch.stack(sigmas).mean()


class SpectralPlugin(BasePlugin):
    def post_trainer_create(self, cfg, trainer):
        frac = os.environ.get("SPECTRAL_FRAC")
        lam = [0.0 if frac else float(os.environ.get("SPECTRAL_LAM", "50"))]
        state, orig, hist = {}, trainer.compute_loss, []

        def compute_loss(model, inputs, return_outputs=False, **kw):
            out = orig(model, inputs, return_outputs=return_outputs, **kw)
            loss = out[0] if return_outputs else out
            pen = spectral_penalty(model, state)
            step = trainer.state.global_step
            if frac and model.training and "lam_fixed" not in state:
                hist.append((float(loss), float(pen))); del hist[:-10 * trainer.args.gradient_accumulation_steps]
                if step >= max(1, trainer.args.get_warmup_steps(trainer.state.max_steps)):
                    ce, sig = sum(h[0] for h in hist) / len(hist), sum(h[1] for h in hist) / len(hist)
                    lam[0] = float(frac) * ce / sig
                    state["lam_fixed"] = True
                    print(f"SpectralPlugin: step {step} mean CE {ce:.4f} mean sigma {sig:.5f} -> spectral_lam fixed at {lam[0]:.3f}", flush=True)
            if step % max(1, trainer.args.logging_steps) == 0:
                trainer.log({"spectral_sigma_max_mean": float(pen), "ce_loss": float(loss), "spectral_lam": lam[0]})
            loss = loss + lam[0] * pen
            return (loss, *out[1:]) if return_outputs else loss

        trainer.compute_loss = compute_loss
        print(f"SpectralPlugin: spectral_lam={lam[0]} (SPECTRAL_FRAC={frac}) on {sum(1 for _ in lora_pairs(trainer.model))} LoRA modules", flush=True)
