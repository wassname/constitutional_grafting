"""Real tiny Qwen-MoE: export SVD bases → projected AdamW + spectral → plain LoRA.

Only Axolotl's BasePlugin import is stubbed on CPU; Trainer, PEFT, model,
exporter, projection callback and spectral loss are the real code. -- PI/Sol
"""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import types

import pytest
import torch
from safetensors import safe_open
from safetensors.torch import load_file, save_file

ROOT = Path(__file__).resolve().parents[2]
REVISION = '59d61f3ce65a6d9863b86d2e96597125219dc754'
SNAPSHOT = Path.home() / '.cache/huggingface/hub/models--Qwen--Qwen3.5-35B-A3B/snapshots' / REVISION


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plugins(monkeypatch):
    base = types.ModuleType('axolotl.integrations.base')
    base.BasePlugin = object
    with monkeypatch.context() as patch:
        patch.setitem(sys.modules, 'axolotl', types.ModuleType('axolotl'))
        patch.setitem(sys.modules, 'axolotl.integrations', types.ModuleType('axolotl.integrations'))
        patch.setitem(sys.modules, 'axolotl.integrations.base', base)
        ortho = load('ortho_plugin_cpu', 'scripts/train/ortho_plugin.py')
        spectral = load('spectral_plugin_cpu', 'scripts/train/spectral_plugin.py')
    return ortho, spectral


def test_real_qwen_export_and_projected_adamw_with_spectral(tmp_path, monkeypatch):
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import Trainer, TrainingArguments
    import yaml

    torch.set_num_threads(2)
    torch.manual_seed(27)
    runner = load('ortho_tiny_runner', 'scripts/eval/57_run15_heal.py')
    exporter = load('ortho_export', 'scripts/train/16_project_chat_adapter.py')
    ortho, spectral = plugins(monkeypatch)
    base = runner.tiny_model(str(SNAPSHOT), torch.float32)
    real = yaml.safe_load((ROOT / 'configs/train/qwen3/sft.yml').read_text())
    # Same target modules/parameters and expert rank-pattern mechanism; smaller ranks
    # because the real tiny model has expert dimensions 16/32, not 512/2048.
    config = LoraConfig(r=4, lora_alpha=8, lora_dropout=0,
                        target_modules=real['lora_target_modules'], target_parameters=real['lora_target_parameters'],
                        rank_pattern={key: 2 for key in real['lora_rank_pattern']},
                        alpha_pattern={key: 4 for key in real['lora_alpha_pattern']}, task_type='CAUSAL_LM')
    donor = get_peft_model(copy.deepcopy(base), config)
    with torch.no_grad():
        for name, parameter in donor.named_parameters():
            if 'lora_B' in name:
                parameter.normal_(std=.01)  # nonzero ΔW makes init assertions non-vacuous
    donor.save_pretrained(tmp_path / 'adapter')
    # Keep the fused per-expert tensors used by the pinned production snapshots;
    # Transformers 5.20's default save converts them into individual expert keys.
    base.save_pretrained(tmp_path / 'base', max_shard_size='10MB', save_original_format=False)
    instruct = copy.deepcopy(base)
    names = {exporter.parameter_name(stem) for stem, _, _, _ in spectral.lora_pairs(donor)}
    with torch.no_grad():
        for name, parameter in instruct.named_parameters():
            if name in names:
                parameter.add_(torch.randn_like(parameter) * .02)
    instruct.save_pretrained(tmp_path / 'instruct', max_shard_size='10MB', save_original_format=False)
    basis = tmp_path / 'basis.safetensors'
    monkeypatch.setattr(sys, 'argv', ['16_project_chat_adapter.py', str(tmp_path / 'base'), str(tmp_path / 'instruct'),
                                     str(tmp_path / 'adapter'), str(tmp_path / 'projection'),
                                     '--ranks', '2', '--basis-rank', '2', '--save-basis', str(basis), '--device', 'cpu'])
    exporter.main()
    with safe_open(str(basis), framework='pt') as stream:
        errors = json.loads(stream.metadata()['fp16_error'])
        assert errors['max_abs'] < 2.5e-4 and errors['max_relative_fro'] < 3e-4
    assert set(load_file(str(basis))) == {stem + '.' + side for stem, _, _, _ in spectral.lora_pairs(donor) for side in ('U', 'V')}

    monkeypatch.setenv('ORTHO_BASIS', str(basis))
    monkeypatch.setenv('SPECTRAL_FRAC', '.01')
    ids = torch.tensor([10, 25, 36, 47, 58, 69, 80, 91])
    trainer = Trainer(model=donor, args=TrainingArguments(output_dir=str(tmp_path / 'train'), use_cpu=True,
                      max_steps=3, warmup_steps=1, learning_rate=.003, optim='adamw_torch',
                      per_device_train_batch_size=1, gradient_accumulation_steps=2,
                      logging_steps=1, save_strategy='no', report_to=[], disable_tqdm=True),
                      train_dataset=[{'input_ids': ids, 'labels': ids.clone()}] * 6)
    spectral.SpectralPlugin().post_trainer_create(None, trainer)
    ortho.OrthoPlugin().post_trainer_create(None, trainer)
    callback = next(c for c in trainer.callback_handler.callbacks if isinstance(c, ortho.OrthoCallback))
    assert callback.residuals['ortho_max_UT_B'] < 1e-6
    assert callback.residuals['ortho_max_A_V'] < 1e-6

    def check_subspaces():
        checked_experts = 0
        for stem, A, B, scale in spectral.lora_pairs(donor):
            assert A.shape[1] == (2 if '.mlp.experts' in stem else 4), stem
            U, V = callback.bases[stem]
            delta = scale * (B @ A)
            assert delta.norm() > 0, stem
            torch.testing.assert_close(U.mT @ delta, torch.zeros_like(U.mT @ delta), atol=2e-6, rtol=0)
            torch.testing.assert_close(delta @ V, torch.zeros_like(delta @ V), atol=2e-6, rtol=0)
            # Also check against the original, unquantized tau singular spaces.
            name = exporter.parameter_name(stem)
            tau = instruct.state_dict()[name] - base.state_dict()[name]
            if tau.ndim == 2:
                tau = tau.unsqueeze(0)
            exact_u, _, exact_vh = torch.linalg.svd(tau, full_matrices=False)
            relative_u = (exact_u[..., :2].mT @ delta).norm() / delta.norm()
            relative_v = (delta @ exact_vh[..., :2, :].mT).norm() / delta.norm()
            assert relative_u < 3e-4 and relative_v < 3e-4, (stem, relative_u, relative_v)
            if '.mlp.experts' in stem:
                checked_experts += delta.shape[0]
        assert checked_experts == 2 * 2 * 32

    check_subspaces()  # init
    # Check every optimizer boundary, not merely the final adapter.
    original_project = callback.project
    step_checks = []

    def project_and_check(measure=False):
        original_project(measure)
        check_subspaces()
        step_checks.append(trainer.state.global_step)

    callback.project = project_and_check
    donor.eval()
    before = donor(input_ids=ids[None], labels=ids[None]).loss.item()
    trainer.train()
    donor.eval()
    after = donor(input_ids=ids[None], labels=ids[None]).loss.item()
    assert abs(after - before) > 1e-5
    assert step_checks == [0, 1, 2, 3]  # resume/init hook + three steps, despite six microsteps
    logs = [row for row in trainer.state.log_history if 'loss' in row]
    assert len(logs) == 3
    assert all(row['ortho_max_UT_B'] < 1e-6 and row['ortho_max_A_V'] < 1e-6 for row in logs)
    assert all('train_spectral_penalty' in row for row in logs)
    assert trainer._spectral_state['lam_fixed'] and trainer._spectral_lam[0] > 0
    donor.save_pretrained(tmp_path / 'trained')
    reloaded = PeftModel.from_pretrained(copy.deepcopy(base), tmp_path / 'trained').eval()
    torch.testing.assert_close(reloaded(input_ids=ids[None]).logits, donor(input_ids=ids[None]).logits)

    saved = load_file(str(basis))
    missing = dict(saved)
    missing.pop(next(iter(missing)))
    save_file(missing, str(tmp_path / 'missing.safetensors'), metadata={'format': 'ortho-v1', 'rank': '2'})
    with pytest.raises(AssertionError, match='missing basis'):
        ortho.OrthoCallback(donor, tmp_path / 'missing.safetensors')
    key = next(iter(saved))
    saved[key] = saved[key][:, :-1]
    save_file(saved, str(tmp_path / 'bad_shape.safetensors'), metadata={'format': 'ortho-v1', 'rank': '2'})
    with pytest.raises(AssertionError):
        ortho.OrthoCallback(donor, tmp_path / 'bad_shape.safetensors')
    print(json.dumps({'author': 'PI/Sol', 'steps': 3, 'microsteps': 6, 'loss_before': before,
                      'loss_after': after, 'fp16_error': errors, 'residuals': callback.residuals}))


def test_k64_cpu_projection_retains_complement(monkeypatch):
    ortho, _ = plugins(monkeypatch)
    torch.manual_seed(64)
    U = torch.linalg.qr(torch.randn(2, 96, 64)).Q
    V = torch.linalg.qr(torch.randn(2, 80, 64)).Q
    A, B = torch.randn(2, 4, 80), torch.randn(2, 96, 4)
    pa, pb = ortho.projection.project_factors(A, B, U, V)
    assert (pb @ pa).norm() > 0
    torch.testing.assert_close(U.mT @ pb, torch.zeros(2, 64, 4), atol=3e-6, rtol=0)
    torch.testing.assert_close(pa @ V, torch.zeros(2, 4, 64), atol=3e-6, rtol=0)
