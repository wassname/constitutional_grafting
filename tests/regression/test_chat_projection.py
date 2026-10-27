"""Projection matches the two-sided matrix operation and PEFT expert layout. -- PI/OpenAI (Sol)"""
import importlib.util
from pathlib import Path

import torch
from peft import LoraConfig
from peft.tuners.lora.layer import ParamWrapper

spec = importlib.util.spec_from_file_location('projection', Path(__file__).resolve().parents[2] / 'scripts/train/16_project_chat_adapter.py')
projection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(projection)


def test_two_sided_projection_and_idempotence():
    torch.manual_seed(14)
    post = torch.randn(11, 9, dtype=torch.float64)
    U, S, Vh = torch.linalg.svd(post, full_matrices=False)
    assert (S[:-1] > S[1:]).all()
    U, V = U[:, :2], Vh[:2].mT
    A, B = torch.randn(3, 9, dtype=torch.float64), torch.randn(11, 3, dtype=torch.float64)
    pa, pb = projection.project_factors(A, B, U, V)
    delta = B @ A
    expected = (torch.eye(11) - U @ U.mT) @ delta @ (torch.eye(9) - V @ V.mT)
    torch.testing.assert_close(pb @ pa, expected, atol=1e-12, rtol=1e-12)
    qa, qb = projection.project_factors(pa, pb, U, V)
    torch.testing.assert_close(qb @ qa, pb @ pa, atol=1e-12, rtol=1e-12)
    torch.testing.assert_close(U.mT @ (pb @ pa), torch.zeros(2, 9, dtype=torch.float64), atol=1e-12, rtol=0)
    torch.testing.assert_close((pb @ pa) @ V, torch.zeros(11, 2, dtype=torch.float64), atol=1e-12, rtol=0)
    torch.testing.assert_close(projection.frobenius_squared(A, B), delta.square().sum(), atol=1e-10, rtol=1e-12)
    torch.testing.assert_close((delta - expected).square().sum() + expected.square().sum(), delta.square().sum())


def test_one_sided_projection_matches_matrix_operation():
    torch.manual_seed(16)
    U, _, Vh = torch.linalg.svd(torch.randn(11, 9, dtype=torch.float64), full_matrices=False)
    U, V = U[:, :2], Vh[:2].mT
    A, B = torch.randn(3, 9, dtype=torch.float64), torch.randn(11, 3, dtype=torch.float64)
    delta = B @ A
    pa, pb = projection.project_factors(A, B, U, V, 'output')
    torch.testing.assert_close(pb @ pa, (torch.eye(11, dtype=torch.float64) - U @ U.mT) @ delta)
    torch.testing.assert_close(pa, A)
    pa, pb = projection.project_factors(A, B, U, V, 'input')
    torch.testing.assert_close(pb @ pa, delta @ (torch.eye(9, dtype=torch.float64) - V @ V.mT))
    torch.testing.assert_close(pb, B)


def test_expert_packing_keeps_experts_separate():
    torch.manual_seed(15)
    experts, rank, inputs, outputs = 3, 2, 5, 7
    stored_A = torch.randn(experts * rank, inputs, dtype=torch.float64)
    stored_B = torch.randn(outputs, rank * experts, dtype=torch.float64)
    A, B = projection.unpack_factors(stored_A, stored_B, experts)
    base = torch.nn.Module()
    base.weight = torch.nn.Parameter(torch.empty(experts, outputs, inputs, dtype=torch.float64))
    wrapper = ParamWrapper(base, 'default', 'weight', LoraConfig(r=rank, lora_alpha=2 * rank), r=rank, lora_alpha=2 * rank)
    with torch.no_grad():
        wrapper.lora_A['default'].weight.copy_(stored_A)
        wrapper.lora_B['default'].weight.copy_(stored_B)
    torch.testing.assert_close(2 * (B @ A), wrapper.get_delta_weight('default'))
    a, b = projection.pack_factors(A, B)
    assert torch.equal(a, stored_A) and torch.equal(b, stored_B)
    post = torch.randn(experts, outputs, inputs, dtype=torch.float64)
    U, _, Vh = torch.linalg.svd(post, full_matrices=False)
    pa, pb = projection.project_factors(A, B, U[..., :1], Vh[..., :1, :].mT)
    for expert in range(experts):
        u, v = U[expert, :, :1], Vh[expert, :1].mT
        expected = (torch.eye(outputs) - u @ u.mT) @ (B[expert] @ A[expert]) @ (torch.eye(inputs) - v @ v.mT)
        torch.testing.assert_close(pb[expert] @ pa[expert], expected)


def test_parameter_mapping_uses_each_original_checkpoint_matrix():
    prefix = 'base_model.model.model.language_model.layers.0.'
    assert projection.parameter_name(prefix + 'mlp.experts.base_layer') == 'model.language_model.layers.0.mlp.experts.gate_up_proj'
    assert projection.parameter_name(prefix + 'mlp.experts') == 'model.language_model.layers.0.mlp.experts.down_proj'
    assert projection.parameter_name(prefix + 'linear_attn.in_proj_qkv') == 'model.language_model.layers.0.linear_attn.in_proj_qkv.weight'
