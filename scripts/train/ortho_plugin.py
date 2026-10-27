"""Two-sided projected Adam updates, with CPU-resident Base→Instruct bases.

ORTHO_BASIS is the fp32 safetensors file from 16_project_chat_adapter.py --save-basis (~14 GiB at k64).
CPU FP32 QR re-orthonormalises after loading. Project at init, resume,
and every optimizer step (not every gradient-accumulation microstep). Adam state
is deliberately untouched. Plain LoRA factors remain mergeable. -- PI/Sol
"""
import importlib
import os

import torch
from axolotl.integrations.base import BasePlugin
from safetensors import safe_open
from transformers import TrainerCallback

projection = importlib.import_module('scripts.train.16_project_chat_adapter')


class OrthoCallback(TrainerCallback):
    def __init__(self, model, basis_path):
        self.pairs, self.bases = {}, {}
        for stem, module in model.named_modules():
            if 'default' in getattr(module, 'lora_A', {}):
                projection.parameter_name(stem)  # same expert-wrapper mapping as the exporter
                self.pairs[stem] = (module.lora_A['default'].weight, module.lora_B['default'].weight,
                                    getattr(module, 'num_experts', 1))
        assert self.pairs, 'OrthoPlugin: no default LoRA factors found'
        with safe_open(str(basis_path), framework='pt', device='cpu') as stream:
            assert stream.metadata()['format'] == 'ortho-v1', 'OrthoPlugin: unsupported basis format'
            rank = int(stream.metadata()['rank'])
            expected = {stem + '.' + side for stem in self.pairs for side in ('U', 'V')}
            actual = set(stream.keys())
            assert actual == expected, f'OrthoPlugin: missing basis={expected - actual}; unexpected basis={actual - expected}'
            for stem, (raw_a, raw_b, experts) in self.pairs.items():
                A, B = projection.unpack_factors(raw_a, raw_b, experts)
                U, V = stream.get_tensor(stem + '.U').float(), stream.get_tensor(stem + '.V').float()
                assert U.shape == (experts, B.shape[1], rank), (stem, U.shape, B.shape)
                assert V.shape == (experts, A.shape[2], rank), (stem, V.shape, A.shape)
                assert 0 < rank <= min(A.shape[2], B.shape[1]), (stem, rank)
                assert torch.isfinite(U).all() and torch.isfinite(V).all(), stem
                self.bases[stem] = (torch.linalg.qr(U, mode='reduced').Q, torch.linalg.qr(V, mode='reduced').Q)
        self.residuals = {}
        self.project(measure=True)

    @torch.no_grad()
    def project(self, measure=False):
        residual_b, residual_a = 0., 0.
        # Disabling CPU autocast also covers BF16 mixed-precision Trainer contexts.
        with torch.autocast(device_type='cpu', enabled=False):
            for stem, (raw_a, raw_b, experts) in self.pairs.items():
                A, B = projection.unpack_factors(raw_a.detach().to(device='cpu', dtype=torch.float32),
                                                  raw_b.detach().to(device='cpu', dtype=torch.float32), experts)
                U, V = self.bases[stem]
                pa, pb = projection.project_factors(A, B, U, V)
                packed_a, packed_b = projection.pack_factors(pa, pb)
                raw_a.copy_(packed_a)
                raw_b.copy_(packed_b)
                if measure:
                    # Include the rounding incurred when writing back to the live parameter dtype.
                    pa, pb = pa.to(raw_a.dtype).float(), pb.to(raw_b.dtype).float()
                    residual_b = max(residual_b, torch.linalg.matrix_norm(U.mT @ pb).max().item())
                    residual_a = max(residual_a, torch.linalg.matrix_norm(pa @ V).max().item())
        if measure:
            self.residuals = {'ortho_max_UT_B': residual_b, 'ortho_max_A_V': residual_a}

    def on_train_begin(self, args, state, control, **kwargs):
        self.project(measure=True)  # Trainer may have restored a checkpoint after plugin creation.

    def on_step_end(self, args, state, control, **kwargs):
        self.project(measure=control.should_log)


class OrthoPlugin(BasePlugin):
    def post_trainer_create(self, cfg, trainer):
        callback = OrthoCallback(trainer.model, os.environ['ORTHO_BASIS'])
        trainer.add_callback(callback)
        original_log = trainer.log

        def log(logs, *args, **kwargs):
            logs.update(callback.residuals)
            return original_log(logs, *args, **kwargs)

        trainer.log = log
        print(f'OrthoPlugin: CPU FP32 two-sided projection on {len(callback.pairs)} stems at init and every optimizer step; Adam state unchanged', flush=True)
        print('SHOULD: ortho_max_UT_B and ortho_max_A_V (max per-matrix Frobenius residuals) stay ≈0 relative to factor norms; FP32 factors normally give roundoff-level residuals. SpectralPlugin remains enabled.', flush=True)
