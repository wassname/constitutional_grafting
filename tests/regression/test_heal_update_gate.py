"""Real callback rejects no-op updates and corrupted saved adapters. -- PI/OpenAI (Sol)"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch
from peft import LoraConfig, get_peft_model
from safetensors.torch import save_file

from scripts.train.heal_callback import HealTiming
from scripts.train.spectral_math import spectral_penalty

ROOT = Path(__file__).resolve().parents[2]


class HealUpdateGate(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(15)
        self.model = get_peft_model(torch.nn.Sequential(torch.nn.Linear(4, 4)), LoraConfig(r=2, lora_alpha=4, target_modules=['0']))
        self.optimizer = torch.optim.SGD([p for p in self.model.parameters() if p.requires_grad], lr=.01)
        self.trainer = SimpleNamespace(accelerator=SimpleNamespace(optimizer_step_was_skipped=False, scaler=None),
            _spectral_lam=[0.], _spectral_last_sigma=0., _heal_optimizer_steps=0, _heal_regularized_steps=0,
            _heal_forward_precision={'unit_test': 'CPU callback, no Axolotl/GPU claim'}, _heal_tokens={'sequence': 0, 'supervised': 0})
        self.callback = HealTiming(self.trainer, verify_actual=True)
        self.state = SimpleNamespace(global_step=0, max_steps=5)
        self.spectral_state = {}
        self.inputs = torch.randn(2, 4)
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, HEAL_NUMERIC_PATH=str(Path(self.temp.name) / 'numeric.jsonl'))
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def backward(self, lr, coefficient):
        self.optimizer.param_groups[0]['lr'] = lr
        self.optimizer.zero_grad()
        sigma = spectral_penalty(self.model, self.spectral_state)
        self.trainer._spectral_lam[0] = coefficient
        self.trainer._spectral_last_sigma = sigma.item()
        loss = self.model(self.inputs).square().mean() + coefficient * sigma
        loss.backward()
        self.callback.on_pre_optimizer_step(None, self.state, None, model=self.model, optimizer=self.optimizer)

    def complete_step(self):
        self.optimizer.step()
        self.state.global_step += 1
        self.callback.on_step_end(None, self.state, None, model=self.model, optimizer=self.optimizer)

    def test_real_change_then_regularized_change_passes(self):
        for lr, coefficient in [(0, 0), (.01, 0), (.01, .1)]:
            self.backward(lr, coefficient)
            self.complete_step()
        self.callback.on_train_end(None, self.state, None)
        self.assertEqual(self.callback.actual_updates, 2)
        self.assertEqual(self.callback.actual_regularized_updates, 1)

    def test_positive_lr_noop_after_initial_update_is_rejected(self):
        self.backward(.01, 0)
        self.complete_step()
        self.backward(.01, .1)
        for p in self.model.parameters():
            if p.grad is not None:
                p.grad.zero_()
        with self.assertRaisesRegex(AssertionError, 'changed no trainable tensor'):
            self.complete_step()

    def test_final_step_parameter_corruption_is_rejected(self):
        self.backward(.01, 0)
        self.complete_step()
        self.state.global_step = 4
        self.backward(.01, .1)
        self.optimizer.step()
        with torch.no_grad():
            next(p for p in self.model.parameters() if p.requires_grad).fill_(float('nan'))
        self.state.global_step = 5
        with self.assertRaisesRegex(AssertionError, 'nonfinite parameters'):
            self.callback.on_step_end(None, self.state, None, model=self.model, optimizer=self.optimizer)

    def test_saved_adapter_dense_nan_is_rejected(self):
        directory = Path(self.temp.name)
        (directory / 'adapter_config.json').write_text(json.dumps({'target_parameters': [], 'rank_pattern': {}}))
        save_file({'model.mlp.experts.lora_B.weight': torch.ones(2, 2),
                   'model.dense.lora_A.weight': torch.full((2, 2), float('nan'))}, directory / 'adapter_model.safetensors')
        result = subprocess.run([sys.executable, ROOT / 'scripts/train/41_expert_adapter_check.py', directory, '1'],
            capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Nonfinite saved adapter tensor', result.stderr)


if __name__ == '__main__':
    unittest.main()
