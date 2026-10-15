"""Axolotl plugin: add a spectral-norm penalty on each LoRA update to the training loss.
loss += spectral_lam * mean over LoRA modules of sigma_max(dW), dW = (alpha/r) B A.
Scaling a graft by k multiplies every singular value of dW by k; the run-3 Gemma graft has one gate_proj direction holding
~50% of the update energy (scripts/scratch/graft_spectrum.py), so k x mostly pushes along it. Penalising sigma_max may spread
the update or may just shrink it; compare against a scalar-strength control. Precedents act on the update, not W0+dW (SCLoRA,
NB-LoRA; slop/research/20261015_spectral_norm_lora.md). Pick lam so the penalty is ~1% of CE after warmup: lam0 = 0.01*CE/P,
then sweep {0, 0.1, 1, 10} x lam0. Untested on our data; from wassname's steer-heal-love `_spectral_div` (power iteration,
u and v held constant so the gradient flows through A and B). One power-iteration step per training step, warm-started.
Covers nn.Linear LoRA (lora_A / lora_B dicts), not PEFT ParamWrapper experts.
Config: plugins: [scripts.train.spectral_plugin.SpectralPlugin]; set SPECTRAL_LAM env (default 0.01).   -- PI/Claude (Opus 5.5)"""
import os

import torch
from axolotl.integrations.base import BasePlugin


def lora_pairs(model):
    for name, m in model.named_modules():
        if hasattr(m, "lora_A") and hasattr(m, "lora_B") and "default" in getattr(m, "lora_A", {}):
            yield name, m.lora_A["default"].weight, m.lora_B["default"].weight, m.scaling["default"]


def spectral_penalty(model, state: dict, n_iter: int = 1) -> torch.Tensor:
    """Mean sigma_max(dW) over LoRA modules. state caches each module's right singular vector between calls."""
    sigmas = []
    for name, A, B, scale in lora_pairs(model):
        A32, B32 = A.float(), B.float()
        with torch.no_grad():
            v = state.get(name)
            if v is None or v.device != A.device:
                v = torch.randn(A.shape[1], device=A.device); v = v / v.norm()
            for _ in range(n_iter):
                u = B32 @ (A32 @ v); u = u / (u.norm() + 1e-8)
                v_new = A32.T @ (B32.T @ u)
                if v_new.norm() > 0:  # LoRA B starts at zero: a zero v would stay zero forever, so keep the old one
                    v = v_new / v_new.norm()
            state[name] = v
        sigmas.append(scale * (u @ (B32 @ (A32 @ v))))
    return torch.stack(sigmas).mean()


class SpectralPlugin(BasePlugin):
    def post_trainer_create(self, cfg, trainer):
        lam = float(os.environ.get("SPECTRAL_LAM", "0.01"))
        state, orig = {}, trainer.compute_loss

        def compute_loss(model, inputs, return_outputs=False, **kw):
            out = orig(model, inputs, return_outputs=return_outputs, **kw)
            loss = out[0] if return_outputs else out
            pen = spectral_penalty(model, state)
            if trainer.state.global_step % max(1, trainer.args.logging_steps) == 0:
                trainer.log({"spectral_sigma_max_mean": float(pen)})
            loss = loss + lam * pen
            return (loss, *out[1:]) if return_outputs else loss

        trainer.compute_loss = compute_loss
        print(f"SpectralPlugin: spectral_lam={lam} on {sum(1 for _ in lora_pairs(trainer.model))} LoRA modules", flush=True)
