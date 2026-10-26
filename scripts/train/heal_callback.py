"""Finite-gradient, actual-update and runtime checks for healing. -- PI/OpenAI (Sol)"""
import json
import math
import os
from pathlib import Path
import time

import torch
from transformers import TrainerCallback


class HealTiming(TrainerCallback):
    def __init__(self, trainer, verify_actual=False):
        self.trainer = trainer
        self.verify_actual = verify_actual
        self.actual_updates = self.actual_regularized_updates = 0
        self.begin = None

    def on_step_begin(self, args, state, control, **kwargs):
        if state.global_step == 2:
            self.begin = time.monotonic()
            self.trainer._heal_tokens = {'sequence': 0, 'supervised': 0}

    def on_pre_optimizer_step(self, args, state, control, **kwargs):
        model = kwargs['model']
        gradients = [(name, p.grad) for name, p in model.named_parameters() if p.requires_grad and p.grad is not None]
        bad = [name for name, grad in gradients if not torch.isfinite(grad).all()]
        assert not bad, f'Nonfinite LoRA gradients before optimizer step {state.global_step}: {bad[:8]}'
        assert gradients, 'No trainable gradients'
        self.pre_lr = float(kwargs['optimizer'].param_groups[0]['lr'])
        self.pre_lambda = self.trainer._spectral_lam[0]
        self.pre_penalty = self.pre_lambda * self.trainer._spectral_last_sigma
        assert math.isfinite(self.pre_penalty) and self.pre_penalty >= 0
        self.gradient_count = len(gradients)
        if self.verify_actual:
            self.before = {n: p.detach().clone() for n, p in model.named_parameters() if p.requires_grad}

    def on_step_end(self, args, state, control, **kwargs):
        skipped = self.trainer.accelerator.optimizer_step_was_skipped
        attempted = not skipped and self.pre_lr > 0
        if self.verify_actual:
            after = {n: p.detach() for n, p in kwargs['model'].named_parameters() if p.requires_grad}
            assert self.before.keys() == after.keys()
            assert all(torch.isfinite(p).all() for p in after.values()), 'Optimizer produced nonfinite parameters'
            changed = any(not torch.equal(self.before[n], p) for n, p in after.items())
            assert not attempted or changed, 'Positive-LR unskipped optimizer step changed no trainable tensor'
            if attempted and changed:
                self.actual_updates += 1
                self.actual_regularized_updates += int(self.pre_penalty > 0)
        if attempted:
            self.trainer._heal_optimizer_steps += 1
            self.trainer._heal_regularized_steps += int(self.pre_penalty > 0)
        if state.global_step <= 4 or state.global_step == 20:
            scaler = self.trainer.accelerator.scaler
            record = {'step': state.global_step, 'pre_step_lr': self.pre_lr,
                'optimizer_skipped': skipped, 'gradient_tensors_finite': self.gradient_count,
                'lora_B_fro_sum_after_step': sum(p.detach().float().norm().item() for name, p in kwargs['model'].named_parameters() if 'lora_B' in name),
                'lambda_before_update': self.pre_lambda, 'spectral_contribution_before_update': self.pre_penalty,
                'nonzero_lr_optimizer_steps': self.trainer._heal_optimizer_steps,
                'regularized_optimizer_steps': self.trainer._heal_regularized_steps,
                'actual_trainable_changes': self.actual_updates if self.verify_actual else None,
                'actual_regularized_changes': self.actual_regularized_updates if self.verify_actual else None,
                'optimizer_state_tensor_types': sorted({type(value).__module__ + '.' + type(value).__name__
                    for optimizer_state in kwargs['optimizer'].state.values() for value in optimizer_state.values() if torch.is_tensor(value)}),
                'scaler_scale': scaler.get_scale() if scaler is not None else None,
                'forward_precision': self.trainer._heal_forward_precision}
            with Path(os.environ['HEAL_NUMERIC_PATH']).open('a') as stream:
                stream.write(json.dumps(record) + '\n')
            print('HEAL NUMERIC ' + json.dumps(record), flush=True)
        if state.global_step != 20:
            return
        elapsed = time.monotonic() - self.begin
        seconds_per_step = elapsed / 18
        remaining_steps = state.max_steps - state.global_step + int(os.environ['HEAL_LATER_STEPS'])
        available = float(os.environ['HEAL_TRAIN_DEADLINE']) - time.time()
        projected = 1.5 * seconds_per_step * remaining_steps
        projected_current = 1.5 * seconds_per_step * (state.max_steps - state.global_step)
        receipt = {'author': 'PI/OpenAI (Sol)', 'step': state.global_step, 'max_steps': state.max_steps,
                   'seconds_per_step_excluding_first_two': seconds_per_step, 'remaining_steps_including_other_variant': remaining_steps,
                   'projected_seconds_with_1_5_margin': projected, 'available_training_seconds': available,
                   'within_reserved_budget': projected_current <= available,
                   'both_variants_within_reserved_budget': projected <= available,
                   'projected_current_variant_seconds': projected_current,
                   'sequence_tokens_per_second': self.trainer._heal_tokens['sequence'] / elapsed,
                   'supervised_tokens_per_second': self.trainer._heal_tokens['supervised'] / elapsed,
                   'peak_gpu_allocated_bytes': torch.cuda.max_memory_allocated(),
                   'peak_gpu_reserved_bytes': torch.cuda.max_memory_reserved()}
        Path(os.environ['HEAL_TIMING_PATH']).write_text(json.dumps(receipt, indent=2) + '\n')
        print('HEAL TIMING ' + json.dumps(receipt), flush=True)
        assert projected_current <= available, 'Measured current variant cannot fit reserved evaluation/retrieval budget'

    def on_train_end(self, args, state, control, **kwargs):
        assert self.trainer._heal_optimizer_steps >= 2, 'Too few nonzero-LR optimizer steps'
        assert self.trainer._heal_regularized_steps >= 1, 'No spectral-regularized optimizer step'
        if self.verify_actual:
            assert self.actual_updates >= 2, 'Too few actual trainable changes'
            assert self.actual_regularized_updates >= 1, 'No actual change after a regularized backward'
