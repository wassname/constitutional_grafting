"""Real tiny Qwen-MoE D merge, masked heal, save/reload and inference. -- PI/OpenAI (Sol)"""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


data = load('heal_data', 'scripts/data/93_heal_training.py')
runner = load('heal_run', 'scripts/eval/57_run15_heal.py')


class HealPipeline(unittest.TestCase):
    def test_training_configuration(self):
        config = runner.train_config('parent', 'input', 'output')
        self.assertEqual((config['lora_r'], config['lora_alpha']), (8, 16))
        self.assertEqual(config['lora_rank_pattern'], {})
        self.assertEqual(config['num_epochs'], 1)
        self.assertTrue(config['bf16'])
        self.assertFalse(config['fp16'])
        self.assertIn('scripts.train.spectral_plugin.SpectralPlugin', config['plugins'])
        self.assertEqual(len(config['lora_target_parameters']), 2)

    def test_schedule_and_adapter_capability_gates(self):
        self.assertTrue(runner.baseline_can_continue(315 * 60, 80 * 60))
        self.assertFalse(runner.baseline_can_continue(315 * 60, 120 * 60))
        self.assertTrue(runner.adapter_incompatible('HTTP 500: fused expert LoRA format is not supported'))
        self.assertFalse(runner.adapter_incompatible('CUDA out of memory after warning LoRA not supported'))
        self.assertFalse(runner.adapter_incompatible('HTTP 503: connection refused'))
        order = runner.evaluation_order({'trace': 1, 'early_trace': 2, 'mix': 3, 'early_mix': 4}, ['trace', 'mix'])
        self.assertEqual([name for name, _ in order], ['r15_D', 'trace', 'mix', 'early_trace', 'early_mix'])

    def test_real_model_merge_train_reload(self):
        import torch
        from peft import LoraConfig, PeftModel, get_peft_model
        from transformers import AutoTokenizer
        torch.set_num_threads(2)
        torch.manual_seed(15)
        tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-35B-A3B', revision=data.REVISION, local_files_only=True)
        base = runner.tiny_model(str(Path.home() / '.cache/huggingface/hub/models--Qwen--Qwen3.5-35B-A3B/snapshots' / data.REVISION), torch.float32)
        config = base.config
        merge = load('heal_merge', 'scripts/train/02_merge.py')
        training = runner.train_config('unused', 'unused', 'unused')
        adapter_cfg = LoraConfig(r=8, lora_alpha=16, lora_dropout=0,
            target_modules=training['lora_target_modules'], target_parameters=training['lora_target_parameters'], task_type='CAUSAL_LM')
        with tempfile.TemporaryDirectory() as directory:
            donor = get_peft_model(copy.deepcopy(base), adapter_cfg)
            with torch.no_grad():
                for name, parameter in donor.named_parameters():
                    if 'lora_B' in name:
                        parameter.normal_(std=.001)
            donor.save_pretrained(Path(directory) / 'donor')
            parent, count, experts = merge.merge_adapter(base, str(Path(directory) / 'donor'), 1., {})
            self.assertTrue(experts and count > 0)
            healed = get_peft_model(copy.deepcopy(parent), adapter_cfg)
            self.assertTrue(any(p.numel() > 4096 for name, p in healed.named_parameters() if '.mlp.experts.' in name and 'lora_' in name))
            frozen_heal = {n: p.detach().clone() for n, p in healed.named_parameters() if not p.requires_grad}
            prep = load('heal_prep', 'scripts/data/92_thinking_heal_data.py')
            messages = [{'role': 'user', 'content': 'What is 2+2?'}]
            examples = [prep.render_trace(tokenizer, messages, 'Adding two and two gives four.', '4.', 'trace'),
                        prep.render_D(tokenizer, messages, '4.', 'replay')]
            batch = []
            for row in examples:
                ids, labels = data.tokenize_row(tokenizer, row)
                start = next(i for i, value in enumerate(labels) if value != -100)
                target = tokenizer.decode(labels[start:])
                self.assertEqual(target.startswith('<think>'), row['kind'] == 'instruct_trace')
                self.assertEqual(target.count('</think>'), int(row['kind'] == 'instruct_trace'))
                batch.append({'input_ids': torch.tensor([ids]), 'labels': torch.tensor([labels])})
            optimizer = torch.optim.AdamW([p for p in healed.parameters() if p.requires_grad], lr=1e-4)
            losses = []
            for example in batch:
                optimizer.zero_grad()
                loss = healed(**example).loss
                self.assertTrue(torch.isfinite(loss))
                loss.backward()
                self.assertTrue(all(torch.isfinite(p.grad).all() for p in healed.parameters() if p.grad is not None))
                self.assertTrue(any(p.grad is not None and p.grad.norm() > 0 for n, p in healed.named_parameters() if 'lora_B' in n))
                self.assertTrue(all(not p.requires_grad or 'lora_' in n for n, p in healed.named_parameters()))
                optimizer.step()
                losses.append(loss.item())
            healed.eval()
            live = healed(input_ids=batch[0]['input_ids']).logits.detach()
            healed.save_pretrained(Path(directory) / 'heal')
            loaded = PeftModel.from_pretrained(copy.deepcopy(parent), Path(directory) / 'heal').eval()
            torch.testing.assert_close(loaded(input_ids=batch[0]['input_ids']).logits, live)
            for name, parameter in healed.named_parameters():
                if not parameter.requires_grad:
                    torch.testing.assert_close(parameter, frozen_heal[name], rtol=0, atol=0)
            fp32_merge = load('fp32_heal_merge', 'scripts/train/17_merge_heal.py')
            merged, merge_report = fp32_merge.merge_heal(copy.deepcopy(parent), str(Path(directory) / 'heal'))
            self.assertTrue(any(r['nonzero_stored_elements'] for r in merge_report))
            merged.eval()
            torch.testing.assert_close(merged(input_ids=batch[0]['input_ids']).logits, live, atol=2e-5, rtol=2e-4)
            print(json.dumps({'author': 'PI/OpenAI (Sol)', 'cpu_real_qwen_moe': True, 'losses': losses,
                'torch': torch.__version__, 'model_type': config.model_type, 'donor_modules': count,
                'mask_trace_closer_and_eos': True, 'mask_replay_empty_think_excluded': True,
                'adapter_on_frozen_merged_parent_reload_parity': True, 'merge_inference_parity': True}))


if __name__ == '__main__':
    unittest.main()
