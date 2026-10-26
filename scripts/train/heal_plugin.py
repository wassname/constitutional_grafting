"""Check rounded training-parent precision and install heal diagnostics. -- PI/OpenAI (Sol)"""
from collections import Counter
import json
import os

import torch
from axolotl.integrations.base import BasePlugin

from scripts.train.heal_callback import HealTiming


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
        assert frozen['torch.bfloat16'] > sum(frozen.values()) * .99, frozen
        assert frozen['torch.float16'] == 0, 'Retry trains the explicitly rounded bf16 D copy; serving parent remains fp16'
        assert sum(trainable.values()) > 0
        assert trainable['torch.float32'] == sum(trainable.values()), trainable
        print('HEAL FROZEN PARENT ' + json.dumps({'frozen': frozen, 'trainable': trainable}), flush=True)
        trainer._heal_tokens = {'sequence': 0, 'supervised': 0}
        trainer._heal_optimizer_steps = trainer._heal_regularized_steps = 0
        trainer._heal_forward_precision = None
        original_loss = trainer.compute_loss
        def counted_loss(model, inputs, **kwargs):
            if model.training:
                if trainer._heal_forward_precision is None:
                    trainer._heal_forward_precision = {'cuda_autocast': torch.is_autocast_enabled('cuda'),
                        'autocast_dtype': str(torch.get_autocast_dtype('cuda')), 'frozen_weight_storage': 'bfloat16', 'LoRA_storage': 'float32'}
                trainer._heal_tokens['sequence'] += int(inputs['attention_mask'].sum())
                trainer._heal_tokens['supervised'] += int((inputs['labels'] != -100).sum())
            return original_loss(model, inputs, **kwargs)
        trainer.compute_loss = counted_loss
        trainer.add_callback(HealTiming(trainer, verify_actual=os.environ.get('HEAL_VERIFY_UPDATES') == '1'))
