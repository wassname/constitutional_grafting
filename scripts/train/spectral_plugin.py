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
(lam = 0 before then); used for chat stages (wassname: spectral on every stage, ~1% of the loss). -- PI/Claude
Calibration waits for a finite nonzero update after warmup; spectral math runs outside autocast in FP32. -- PI/OpenAI (Sol)
Logs train_/eval_ text_loss, spectral_penalty, total_loss, spectral_sigma_max_mean and spectral_lam at Trainer log boundaries.
Components are example-weighted means over local forwards; eval_loss still includes the penalty. -- PI/OpenAI"""
import os

import torch
from axolotl.integrations.base import BasePlugin
from transformers import TrainerCallback

from scripts.train.spectral_math import calibration_stats, lora_pairs, spectral_penalty


class RequireSpectralCalibration(TrainerCallback):
    def on_train_end(self, args, state, control, **kwargs):
        assert self.calibration['lam_fixed'], 'No finite nonzero LoRA update became available for spectral calibration'

    def __init__(self, calibration):
        self.calibration = calibration


class SpectralPlugin(BasePlugin):
    def post_trainer_create(self, cfg, trainer):
        frac = os.environ.get("SPECTRAL_FRAC")
        lam = [0.0 if frac else float(os.environ.get("SPECTRAL_LAM", "50"))]
        state, orig, hist = {}, trainer.compute_loss, []
        orig_log = trainer.log
        sums, counts = {"train": None, "eval": None}, {"train": 0, "eval": 0}

        def log(logs, *args, **kw):
            phase = "eval" if "eval_loss" in logs else "train"
            if ("eval_loss" in logs or "loss" in logs or "train_loss" in logs) and counts[phase]:
                text, penalty, sigma, mean_lam = (sums[phase] / counts[phase]).tolist()
                logs.update({f"{phase}_text_loss": text, f"{phase}_spectral_penalty": penalty,
                             f"{phase}_total_loss": text + penalty,
                             f"{phase}_spectral_sigma_max_mean": sigma, f"{phase}_spectral_lam": mean_lam})
                sums[phase], counts[phase] = None, 0
            return orig_log(logs, *args, **kw)

        def compute_loss(model, inputs, return_outputs=False, **kw):
            out = orig(model, inputs, return_outputs=return_outputs, **kw)
            loss = out[0] if return_outputs else out
            pen = spectral_penalty(model, state)
            trainer._spectral_last_sigma = pen.detach().item()
            step = trainer.state.global_step
            if frac and model.training and not state['lam_fixed']:
                hist.append((loss.detach().item(), pen.detach().item())); del hist[:-10 * trainer.args.gradient_accumulation_steps]
                if step >= max(1, trainer.args.get_warmup_steps(trainer.state.max_steps)):
                    calibration = calibration_stats(hist, float(frac))
                    if calibration is not None:
                        lam[0] = calibration['lambda']
                        state.update(lam_fixed=True, calibration=calibration)
                        print(f"SpectralPlugin: step {step} mean CE {calibration['ce']:.4f} mean sigma {calibration['sigma']:.5f} -> spectral_lam fixed at {lam[0]:.3f}", flush=True)
                    elif state.get('wait_step') != step:
                        state['wait_step'] = step
                        print(f'SpectralPlugin: step {step} calibration pending; no nonzero update yet (zero-LR warmup or skipped optimizer step)', flush=True)
            penalty = lam[0] * pen
            phase, batch_size = ("train" if model.training else "eval"), inputs["input_ids"].shape[0]
            values = torch.stack((loss.detach(), penalty.detach(), pen.detach(), loss.detach().new_tensor(lam[0]))) * batch_size
            sums[phase] = values if sums[phase] is None else sums[phase] + values
            counts[phase] += batch_size
            loss = loss + penalty
            return (loss, *out[1:]) if return_outputs else loss

        trainer.compute_loss, trainer.log = compute_loss, log
        trainer._spectral_state, trainer._spectral_lam = state, lam
        if frac:
            state['lam_fixed'] = False
            trainer.add_callback(RequireSpectralCalibration(state))
        print(f"SpectralPlugin: spectral_lam={lam[0]} (SPECTRAL_FRAC={frac}) on {sum(1 for _ in lora_pairs(trainer.model))} LoRA modules", flush=True)
        print("SHOULD: train_/eval_total_loss = text_loss + spectral_penalty; eval_loss still includes the penalty. Components log once per Trainer boundary.", flush=True)
