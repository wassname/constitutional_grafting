# /// script
# requires-python = ">=3.11"
# dependencies = ["torch", "peft>=0.19.1", "transformers"]
# [tool.uv.sources]
# torch = { index = "pytorch-cpu" }
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# ///
"""spectral_penalty (scripts/train/spectral_plugin.py) matches the true top singular value of (alpha/r) B A after warm-started
power iteration, and training with it lowers sigma_max relative to sigma_2 vs training without. CPU, toy model.
Run: uv run --script tests/regression/test_spectral_penalty.py   -- PI/Claude"""
import sys
import types
from pathlib import Path
from unittest.mock import patch

import torch
from peft import LoraConfig, get_peft_model
from torch import nn

sys.modules.setdefault("axolotl", types.ModuleType("axolotl"))  # plugin imports BasePlugin; stub it for a CPU test
sys.modules.setdefault("axolotl.integrations", types.ModuleType("axolotl.integrations"))
base_mod = types.ModuleType("axolotl.integrations.base"); base_mod.BasePlugin = object
sys.modules["axolotl.integrations.base"] = base_mod
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "train"))
from spectral_plugin import SpectralPlugin, lora_pairs, spectral_penalty  # noqa: E402


def toy():
    torch.manual_seed(0)
    m = nn.Sequential(nn.Linear(16, 32), nn.ReLU(), nn.Linear(32, 16))
    return get_peft_model(m, LoraConfig(r=8, lora_alpha=16, target_modules=["0", "2"], lora_dropout=0))


def test_plugin_default_and_explicit_override():
    """The training callback defaults to λ=50 and still permits a plain graft. -- PI/Sol"""
    model = toy()
    with torch.no_grad():
        for _, _, B, _ in lora_pairs(model):
            B.normal_(0, 0.1)
    losses = []
    for env in ({}, {"SPECTRAL_LAM": "50"}, {"SPECTRAL_LAM": "0"}):
        trainer = types.SimpleNamespace(model=model, compute_loss=lambda *a, **kw: torch.tensor(2.0), log=lambda *a, **kw: None,
            state=types.SimpleNamespace(global_step=1), args=types.SimpleNamespace(logging_steps=2))
        with patch.dict("os.environ", env, clear=True):
            torch.manual_seed(42)
            SpectralPlugin().post_trainer_create(None, trainer)
            losses.append(trainer.compute_loss(model, {"input_ids": torch.ones(1, 16)}))
    torch.testing.assert_close(losses[0], losses[1])
    assert losses[0] > losses[2]
    assert losses[2].item() == 2.0


def test_logging_preserves_objective_gradients_and_outputs():
    """Logging must not change the loss, LoRA gradients or Trainer's returned outputs. -- PI/OpenAI"""
    model = toy()
    with torch.no_grad():
        for _, _, B, _ in lora_pairs(model):
            B.normal_(0, 0.1)
    inputs, outputs, records = {"input_ids": torch.randn(2, 16)}, object(), []

    def original(model, inputs, return_outputs=False, **kw):
        loss = model(inputs["input_ids"]).square().mean()
        return (loss, outputs) if return_outputs else loss

    trainer = types.SimpleNamespace(model=model, compute_loss=original, log=lambda logs, **kw: records.append(logs),
        state=types.SimpleNamespace(global_step=0), args=types.SimpleNamespace(logging_steps=1))
    params = [p for p in model.parameters() if p.requires_grad]
    torch.manual_seed(42)
    expected = original(model, inputs) + 50 * spectral_penalty(model, {})
    expected_grads = torch.autograd.grad(expected, params)
    with patch.dict("os.environ", {"SPECTRAL_LAM": "50"}, clear=True):
        torch.manual_seed(42)
        SpectralPlugin().post_trainer_create(None, trainer)
        actual, returned_outputs = trainer.compute_loss(model, inputs, return_outputs=True, num_items_in_batch=2)
    torch.testing.assert_close(actual, expected)
    for actual_grad, expected_grad in zip(torch.autograd.grad(actual, params), expected_grads):
        torch.testing.assert_close(actual_grad, expected_grad)
    assert returned_outputs is outputs and not records
    trainer.log({"loss": actual.item()})
    assert len(records) == 1
    metrics = records[0]
    torch.testing.assert_close(torch.tensor(metrics["train_total_loss"]), actual.detach())
    assert metrics["train_total_loss"] == metrics["train_text_loss"] + metrics["train_spectral_penalty"]


def test_logging_separates_and_resets_training_and_evaluation():
    """One component record per Trainer log, with independent example-weighted phase means. -- PI/OpenAI"""
    model, records = toy(), []
    with torch.no_grad():
        for _, _, B, _ in lora_pairs(model):
            B.normal_(0, 0.1)
    trainer = types.SimpleNamespace(model=model,
        compute_loss=lambda m, *a, **kw: torch.tensor(2.0 if m.training else 7.0),
        log=lambda logs, **kw: records.append((logs, kw)),
        state=types.SimpleNamespace(global_step=0), args=types.SimpleNamespace(logging_steps=1))
    with patch.dict("os.environ", {"SPECTRAL_LAM": "50"}, clear=True):
        SpectralPlugin().post_trainer_create(None, trainer)
    first = trainer.compute_loss(model, {"input_ids": torch.ones(1, 16)})
    second = trainer.compute_loss(model, {"input_ids": torch.ones(2, 16)})
    model.eval()
    evaluation = trainer.compute_loss(model, {"input_ids": torch.ones(3, 16)})
    assert not records
    evaluated_metrics = {"eval_loss": evaluation.item()}
    trainer.log(evaluated_metrics, start_time=123)
    metrics, kw = records[-1]
    assert evaluated_metrics is metrics and "eval_text_loss" in evaluated_metrics
    assert metrics["eval_text_loss"] == 7.0 and metrics["eval_spectral_lam"] == 50.0 and kw == {"start_time": 123}
    torch.testing.assert_close(torch.tensor(metrics["eval_total_loss"]), evaluation.detach())
    assert "train_text_loss" not in metrics
    trainer.log({"loss": ((first + 2 * second) / 3).item()})
    metrics = records[-1][0]
    assert metrics["train_text_loss"] == 2.0 and "eval_text_loss" not in metrics
    torch.testing.assert_close(torch.tensor(metrics["train_total_loss"]), ((first + 2 * second) / 3).detach())
    model.train()
    third = trainer.compute_loss(model, {"input_ids": torch.ones(1, 16)})
    trainer.log({"loss": third.item()})
    torch.testing.assert_close(torch.tensor(records[-1][0]["train_total_loss"]), third.detach())


def true_sigmas(model):
    return [torch.linalg.svdvals(s * (B[0].float() @ A[0].float())) for _, A, B, s in lora_pairs(model)]


class Experts(nn.Module):  # fused 3D params, Qwen3.5 MoE layout [E, out, in], as in test_moe_expert_merge.py
    def __init__(self):
        super().__init__()
        self.gate_up_proj = nn.Parameter(torch.randn(5, 6, 4) * 0.1)
        self.down_proj = nn.Parameter(torch.randn(5, 4, 3) * 0.1)

    def forward(self, x):
        gate, up = torch.einsum("bh,eoh->beo", x, self.gate_up_proj).chunk(2, -1)
        return torch.einsum("bei,ehi->beh", nn.functional.silu(gate) * up, self.down_proj).sum(1)


def test_expert_lora_matches_peft_delta():
    """Expert penalty = mean over modules of mean over experts of sigma_max of PEFT's own get_delta_weight."""
    from peft.tuners.lora.layer import ParamWrapper
    torch.manual_seed(0)
    m = nn.Module(); m.mlp = nn.Module(); m.mlp.experts = Experts(); m.forward = lambda x: m.mlp.experts(x)
    p = get_peft_model(m, LoraConfig(r=2, lora_alpha=4, lora_dropout=0, target_modules=[],
                                     target_parameters=["mlp.experts.gate_up_proj", "mlp.experts.down_proj"]))
    with torch.no_grad():
        for n, w in p.named_parameters():
            if "lora_" in n:
                w.normal_(0, 0.3)
    wrappers = [w for w in p.modules() if isinstance(w, ParamWrapper)]
    assert len(wrappers) == 2 and all(w.num_experts == 5 for w in wrappers)
    state = {}
    for _ in range(100):
        pen = spectral_penalty(p, state)
    expect = torch.stack([torch.linalg.matrix_norm(w.get_delta_weight("default").float(), ord=2).mean() for w in wrappers]).mean()
    torch.testing.assert_close(pen.detach(), expect, rtol=1e-3, atol=1e-6)
    pen.backward()
    assert all(w.grad is not None and w.grad.norm() > 0 for n, w in p.named_parameters() if "lora_" in n)


def test_matches_svd_after_warm_iterations():
    m = toy()
    with torch.no_grad():
        for _, A, B, _ in lora_pairs(m):
            B.normal_(0, 0.1)
    state = {}
    for _ in range(50):
        pen = spectral_penalty(m, state)
    expect = torch.stack([s[0] for s in true_sigmas(m)]).mean()
    torch.testing.assert_close(pen.detach(), expect, rtol=1e-3, atol=1e-5)


def train(lam):
    m = toy()
    g = torch.Generator().manual_seed(1)
    x = torch.randn(256, 16, generator=g)
    y = x @ (torch.randn(16, 1, generator=g) @ torch.randn(1, 16, generator=g)) * 3  # rank-1 target: pulls one direction hard
    opt = torch.optim.Adam([p for p in m.parameters() if p.requires_grad], lr=1e-2)
    state = {}
    for _ in range(300):
        opt.zero_grad()
        loss = (m(x) - y).square().mean() + lam * spectral_penalty(m, state)
        loss.backward(); opt.step()
    s = [t.detach() for t in true_sigmas(m)][0]
    return float(s[0]), float(s[0] / s[1])


def test_penalty_lowers_sigma_max():
    s0, r0 = train(0.0)
    s1, r1 = train(1.0)
    assert s1 < s0 and r1 < r0, (s0, r0, s1, r1)
    return s0, r0, s1, r1


if __name__ == "__main__":
    test_plugin_default_and_explicit_override()
    test_logging_preserves_objective_gradients_and_outputs()
    test_logging_separates_and_resets_training_and_evaluation()
    test_matches_svd_after_warm_iterations()
    test_expert_lora_matches_peft_delta()
    s0, r0, s1, r1 = test_penalty_lowers_sigma_max()
    print(f"PASS: logging preserves loss/gradients and separates train/eval; penalty matches SVD sigma_max; lam=0 sigma1 {s0:.3f} (s1/s2 {r0:.1f}) -> lam=1 sigma1 {s1:.3f} (s1/s2 {r1:.1f})")
