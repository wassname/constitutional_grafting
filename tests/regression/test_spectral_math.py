"""LoRA zero-init, autocast, warmup and nonzero spectral calibration. -- PI/OpenAI (Sol)"""
import unittest

import torch
from peft import LoraConfig, get_peft_model

from scripts.train.spectral_math import calibration_stats, spectral_penalty


class SpectralMath(unittest.TestCase):
    def model(self, seed=15):
        torch.manual_seed(seed)
        return get_peft_model(torch.nn.Sequential(torch.nn.Linear(4, 4)), LoraConfig(r=2, lora_alpha=4, target_modules=['0']))

    def test_zero_B_is_finite_under_low_precision_autocast(self):
        for dtype in [torch.float16, torch.bfloat16]:
            model = self.model()
            with torch.autocast('cpu', dtype=dtype):
                penalty = spectral_penalty(model, {})
            self.assertEqual(penalty.dtype, torch.float32)
            self.assertEqual(penalty.item(), 0)
            penalty.backward()
            self.assertTrue(all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None))

    def test_zero_lr_then_update_then_regularized_update(self):
        for seed in [15, 16]:
            with self.subTest(seed=seed):
                self.warmup_scenario(seed)

    def warmup_scenario(self, seed):
        model = self.model(seed)
        frozen = {n: p.detach().clone() for n, p in model.named_parameters() if not p.requires_grad}
        optimizer = torch.optim.SGD([p for p in model.parameters() if p.requires_grad], lr=0)
        inputs = torch.randn(2, 4)
        spectral_state, history, lambda_value = {}, [], 0
        B_before_regularized_update = None
        for step, lr in enumerate([0, .01, .01]):
            optimizer.param_groups[0]['lr'] = lr
            optimizer.zero_grad()
            ce = model(inputs).square().mean()
            penalty = spectral_penalty(model, spectral_state, n_iter=100)
            history.append((ce.item(), penalty.item()))
            calibration = calibration_stats(history, .01)
            if step < 2:
                self.assertIsNone(calibration)
            else:
                lambda_value = calibration['lambda']
                self.assertGreater(lambda_value, 0)
                self.assertAlmostEqual(lambda_value * penalty.item() / ce.item(), .01)
                B_before_regularized_update = {n: p.detach().clone() for n, p in model.named_parameters() if 'lora_B' in n}
            (ce + lambda_value * penalty).backward()
            self.assertTrue(all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None))
            optimizer.step()
        self.assertTrue(any(not torch.equal(p, B_before_regularized_update[n]) for n, p in model.named_parameters() if 'lora_B' in n))
        for name, value in frozen.items():
            torch.testing.assert_close(dict(model.named_parameters())[name], value, rtol=0, atol=0)

    def test_zero_history_stays_pending_and_nonfinite_statistics_fail(self):
        for count in range(1, 21):
            self.assertIsNone(calibration_stats([(2., 0.)] * count, .01))
        for history in [[(float('nan'), 0)], [(2., float('nan'))], [(2., float('inf'))], [(2., -1.)]]:
            with self.assertRaises(AssertionError):
                calibration_stats(history, .01)


if __name__ == '__main__':
    unittest.main()
