"""Check frozen-parent precision and stop an over-budget heal after timing. -- PI/OpenAI (Sol)"""
import json
import os
from pathlib import Path
import time
from collections import Counter

import torch
from axolotl.integrations.base import BasePlugin
from transformers import TrainerCallback


class HealTiming(TrainerCallback):
    def __init__(self, trainer):
        self.trainer = trainer
        self.begin = None

    def on_step_begin(self, args, state, control, **kwargs):
        if state.global_step == 2:
            self.begin = time.monotonic()
            self.trainer._heal_tokens = {'sequence': 0, 'supervised': 0}

    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step != 20:
            return
        elapsed = time.monotonic() - self.begin
        seconds_per_step = elapsed / 18
        remaining_steps = state.max_steps - state.global_step + int(os.environ['HEAL_LATER_STEPS'])
        available = float(os.environ['HEAL_TRAIN_DEADLINE']) - time.time()
        projected = 1.5 * seconds_per_step * remaining_steps
        receipt = {'author': 'PI/OpenAI (Sol)', 'step': state.global_step, 'max_steps': state.max_steps,
                   'seconds_per_step_excluding_first_two': seconds_per_step, 'remaining_steps_including_other_variant': remaining_steps,
                   'projected_seconds_with_1_5_margin': projected, 'available_training_seconds': available,
                   'within_reserved_budget': projected <= available,
                   'sequence_tokens_per_second': self.trainer._heal_tokens['sequence'] / elapsed,
                   'supervised_tokens_per_second': self.trainer._heal_tokens['supervised'] / elapsed,
                   'peak_gpu_allocated_bytes': torch.cuda.max_memory_allocated(),
                   'peak_gpu_reserved_bytes': torch.cuda.max_memory_reserved()}
        Path(os.environ['HEAL_TIMING_PATH']).write_text(json.dumps(receipt, indent=2) + '\n')
        print('HEAL TIMING ' + json.dumps(receipt), flush=True)
        assert projected <= available, 'Measured training cannot fit reserved evaluation/retrieval budget'


class HealPlugin(BasePlugin):
    def post_trainer_create(self, cfg, trainer):
        frozen = Counter()
        trainable = Counter()
        for name, parameter in trainer.model.named_parameters():
            if parameter.requires_grad:
                assert 'lora_' in name, name
                trainable[str(parameter.dtype)] += parameter.numel()
            else:
                frozen[str(parameter.dtype)] += parameter.numel()
        assert frozen['torch.float16'] > sum(frozen.values()) * .99, frozen
        assert frozen['torch.bfloat16'] == 0, 'bf16 conversion would change the frozen fp16 D parent'
        assert sum(trainable.values()) > 0
        assert trainable['torch.float32'] == sum(trainable.values()), trainable
        print('HEAL FROZEN PARENT ' + json.dumps({'frozen': frozen, 'trainable': trainable}), flush=True)
        trainer._heal_tokens = {'sequence': 0, 'supervised': 0}
        original_loss = trainer.compute_loss
        def counted_loss(model, inputs, **kwargs):
            if model.training:
                trainer._heal_tokens['sequence'] += int(inputs['attention_mask'].sum())
                trainer._heal_tokens['supervised'] += int((inputs['labels'] != -100).sum())
            return original_loss(model, inputs, **kwargs)
        trainer.compute_loss = counted_loss
        trainer.add_callback(HealTiming(trainer))
