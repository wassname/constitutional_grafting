"""Char/cap selector: generalized-eigen projector maths, and collect → project → merge on a tiny real Qwen3.5-MoE. -- PI/Claude (opus-5-5)"""
import copy
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import torch

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


selector = load('selector', 'scripts/train/18_project_char_vs_cap.py')
REVISION = '59d61f3ce65a6d9863b86d2e96597125219dc754'
SNAPSHOT = Path.home() / '.cache/huggingface/hub/models--Qwen--Qwen3.5-35B-A3B/snapshots' / REVISION
TARGET_MODULES = r'model.language_model.layers.[\d]+.(_checkpoint_wrapped_module.)?(self_attn.(q|k|v|o)_proj|linear_attn.(in_proj_qkv|in_proj_z|out_proj)|mlp.shared_expert.(gate|up|down)_proj)'


def test_projector_keeps_character_directions_and_drops_capability_ones():
    torch.manual_seed(18)
    d = 6
    basis = torch.linalg.qr(torch.randn(d, d, dtype=torch.float64))[0]
    C_cap = basis @ torch.diag(torch.tensor([1., 1, 1, 1, 9, 9], dtype=torch.float64)) @ basis.T
    C_char = basis @ torch.diag(torch.tensor([9., 9, 1, 1, 1, 1], dtype=torch.float64)) @ basis.T
    lam, V, cap = selector.generalized_eig(C_char, C_cap, 1e-3)
    ridge = cap - C_cap
    torch.testing.assert_close(V.T @ cap @ V, torch.eye(d, dtype=torch.float64))
    torch.testing.assert_close((C_char + ridge) @ V, cap @ V @ torch.diag(lam))
    Q = selector.projector(lam, V, cap, .5)
    torch.testing.assert_close(Q @ Q, Q)
    keep = lam >= .5
    assert keep.sum() == 4  # two char-heavy (λ≈9) and two shared (λ≈1) kept; two cap-heavy (λ≈1/9) dropped
    # A row reading a capability-heavy direction is removed; one reading a character-heavy direction is kept.
    cap_row, char_row = basis[:, 4:5].T, basis[:, 0:1].T
    assert (cap_row @ Q).norm() < 1e-2
    torch.testing.assert_close(char_row @ Q, char_row, atol=1e-2, rtol=0)
    # Kept energy never exceeds the original, and the character share is kept better than the capability share.
    A = torch.randn(5, d, dtype=torch.float64)
    energy = lambda M, C: torch.trace(M @ C @ M.T)
    kept_char, kept_cap = energy(A @ Q, C_char) / energy(A, C_char), energy(A @ Q, C_cap) / energy(A, C_cap)
    assert 0 < kept_cap < kept_char <= 1 + 1e-9


def parts_for(C_char, C_cap, A, B, eps=1e-3):
    lam, V, R = selector.generalized_eig(C_char, C_cap, eps)
    return [(lam, A @ R @ V, V, A, B)]


def test_removed_energy_is_the_removed_component_not_norm_loss():
    # Sol review 20261027 finding 1: noncommuting moments, oblique Q; norm loss 0.15 hid a removed component of 3.3x.
    C_cap = torch.tensor([[101., -10], [-10, 1]], dtype=torch.float64)
    C_char = torch.tensor([[12., -1], [-1, .1]], dtype=torch.float64)
    A = torch.tensor([[-0.5086472691944104, 0.8609750028549427]], dtype=torch.float64)
    B = torch.ones(1, 1, dtype=torch.float64)
    parts = parts_for(C_char, C_cap, A, B)
    lam, ARV, V, _, _ = parts[0]
    A2 = (ARV * (lam >= 1.)) @ V.mT
    torch.testing.assert_close(selector.removed_energy(parts, 1.), ((A - A2).square().sum() / A.square().sum()).item())
    assert selector.removed_energy(parts, 1.) > 3


def test_tau_search_finds_target_in_clustered_spectrum():
    # Sol review 20261027 finding 2: 40 log-spaced τ missed an exactly attainable 15%.
    C_cap = torch.eye(6, dtype=torch.float64)
    C_char = torch.diag(torch.tensor([1e-6, .9, .99, 1.01, 1.1, 1e6], dtype=torch.float64))
    A = torch.diag(torch.tensor([.01, .14, .25, .25, .25, .10], dtype=torch.float64).sqrt())
    tau, removed = selector.choose_tau(parts_for(C_char, C_cap, A, torch.eye(6, dtype=torch.float64)), .15, .01)
    assert abs(removed - .15) <= .01, (tau, removed)


def test_noncommuting_projection_keeps_ridged_order():
    torch.manual_seed(21)
    d = 12
    def cov():
        X = torch.randn(40, d, dtype=torch.float64) @ torch.randn(d, d, dtype=torch.float64)
        return X.T @ X / 40
    C_char, C_cap = cov(), cov()
    lam, V, R = selector.generalized_eig(C_char, C_cap, 1e-3)
    D = C_char + (R - C_cap)
    A = torch.randn(5, d, dtype=torch.float64)
    energy = lambda M, C: torch.trace(M @ C @ M.T)
    for tau in lam.tolist()[1:-1]:
        A2 = A @ selector.projector(lam, V, R, tau)
        kc, kk = energy(A2, D) / energy(A, D), energy(A2, R) / energy(A, R)
        assert 0 <= kk <= kc + 1e-9 and kc <= 1 + 1e-9


def test_patched_experts_reproduce_model_output():
    torch.manual_seed(20)
    runner = load('heal_run', 'scripts/eval/57_run15_heal.py')
    model = runner.tiny_model(str(SNAPSHOT), torch.float32).eval()
    decoder = model.model.language_model
    ids = torch.randint(0, 1000, (2, 12))
    mask = torch.ones_like(ids)
    mask[1, 8:] = 0
    with torch.inference_mode():
        before = decoder(input_ids=ids, attention_mask=mask).last_hidden_state
        S, N, flat = {}, {}, {'m': mask.reshape(-1).bool()}
        for name, module in model.named_modules():
            if name.endswith('mlp.experts'):
                selector.patch_experts(module, name, S, N, flat)
        after = decoder(input_ids=ids, attention_mask=mask).last_hidden_state
    torch.testing.assert_close(after, before)
    assert all(int(n.sum()) == 20 * 2 for n in N.values())  # 20 real tokens, top-2 routing


def test_collect_project_merge_on_tiny_model(tmp_path):
    from peft import LoraConfig, get_peft_model
    from transformers import AutoTokenizer
    torch.manual_seed(19)
    runner = load('heal_run', 'scripts/eval/57_run15_heal.py')
    merge = load('merge', 'scripts/train/02_merge.py')
    model = runner.tiny_model(str(SNAPSHOT), torch.float32)
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-35B-A3B', revision=REVISION, local_files_only=True)
    model.save_pretrained(tmp_path / 'model')
    tokenizer.save_pretrained(tmp_path / 'model')
    config = LoraConfig(r=4, lora_alpha=8, lora_dropout=0, target_modules=TARGET_MODULES,
                        target_parameters=['mlp.experts.gate_up_proj', 'mlp.experts.down_proj'], task_type='CAUSAL_LM')
    donor = get_peft_model(copy.deepcopy(model), config)
    with torch.no_grad():
        for name, parameter in donor.named_parameters():
            if 'lora_B' in name:
                parameter.normal_(std=.01)
    donor.save_pretrained(tmp_path / 'adapter')
    texts = {'char': ['Should I tell my friend the truth about the loan? I owe it to them to be honest, even if it costs me.'] * 3,
             'cap': ['What is 17 * 23 + 4? 17 * 23 = 391, plus 4 is 395. The answer is 395.'] * 3}
    for name, rows in texts.items():
        with (tmp_path / f'{name}.jsonl').open('w') as stream:
            for text in rows:
                stream.write(json.dumps({'segments': [{'text': text, 'label': True}]}) + '\n')
        for shard in ('0:1', '1:2'):
            selector.collect(SimpleNamespace(model=tmp_path / 'model', data=tmp_path / f'{name}.jsonl', out=tmp_path / f'{name}_{shard[0]}.pt',
                                             rows=8, max_length=64, batch=2, layers=shard, dtype='float32', device='cpu'))
    moments = selector.load_moments([tmp_path / 'cap_0.pt', tmp_path / 'cap_1.pt'], 256.)
    assert {key.split('.')[1] for key in moments} == {'attn_in', 'attn_out', 'mlp_in', 'shared_down', 'expert_down'}
    assert moments['0.expert_down'].shape == (32, 16, 16)
    common = dict(char=[tmp_path / 'char_0.pt', tmp_path / 'char_1.pt'], cap=[tmp_path / 'cap_0.pt', tmp_path / 'cap_1.pt'],
                  eps=1e-3, shrink=256., device='cpu')
    selector.project(SimpleNamespace(adapter=tmp_path / 'adapter', output=tmp_path / 'projected', removed_energy=.15, tau=None, tol=.02, **common))
    report = json.loads((tmp_path / 'projected/projection.json').read_text())
    assert abs(report['removed_component_energy'] - .15) <= .02, report
    assert 0 < report['kept_cap_energy_ridged'] < report['kept_char_energy_ridged'] <= 1 + 1e-6, report
    selector.measure(SimpleNamespace(adapters=[tmp_path / 'adapter', tmp_path / 'projected'], **common))
    merged, count, experts = merge.merge_adapter(copy.deepcopy(model), str(tmp_path / 'projected'), 1., {})
    assert experts and count > 0
    ids = tokenizer('Hello', return_tensors='pt')['input_ids']
    assert torch.isfinite(merged(input_ids=ids).logits).all()
