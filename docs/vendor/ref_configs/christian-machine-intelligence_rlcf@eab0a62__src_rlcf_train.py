"""
RLCF v3 training loop — vanilla GRPO with pure priest scalar reward.

Pipeline (simplified from v1):
  Phase A: G rollouts per scenario, sampled on-policy
  Phase B: Claude priest scores each rollout on a 0-5 Christian-reasoning scale
  Phase E: Group-relative advantages → multi-epoch PPO-clipped GRPO update

No refinement phase. No NL admonition injection. No multi-marker rubric.
The priest returns a single integer; that's the whole reward.

LoRA + adapter-disabled-reference trick (one base model serves both
policy and reference) is retained. Spark-compatible: bf16, no bnb, no vLLM.

Usage:
    python -m src.rlcf_train \
        --out-dir models/rlcf_v3/treatment/cycle_1 \
        --batch-file data/rlcf_v3/batches/train.jsonl
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import random
import time
from dataclasses import asdict
from pathlib import Path
from typing import Optional

import torch
import torch.nn.functional as F
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

from src._seed import set_global_seed

from src.rlcf_priest import PriestScore, compute_rewards, score_batch
from src.rlcf_rollout import (
    BASE_MODEL,
    PROMPTS_DIR,
    Rollout,
    generate_rollouts,
)

MODELS_DIR = Path(__file__).parent.parent / "models"

DEFAULT_LORA = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)


# =====================================================================
# GRPO math
# =====================================================================

def group_relative_advantages(
    rewards: list[float],
    group_keys: list[tuple],
    eps: float = 1e-6,
) -> list[float]:
    """Normalize each rollout's reward by its (base_id, variant) group's mean/std."""
    from collections import defaultdict
    buckets: dict[tuple, list[int]] = defaultdict(list)
    for i, k in enumerate(group_keys):
        buckets[k].append(i)

    advantages = [0.0] * len(rewards)
    for k, idxs in buckets.items():
        group_rewards = [rewards[i] for i in idxs]
        mean = sum(group_rewards) / len(group_rewards)
        var = sum((r - mean) ** 2 for r in group_rewards) / max(1, len(group_rewards))
        std = math.sqrt(var) + eps
        for i in idxs:
            advantages[i] = (rewards[i] - mean) / std
    return advantages


def sequence_logprobs(
    model,
    input_ids: torch.Tensor,
    prompt_lens: torch.Tensor,
    attention_mask: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return (per_token_logprobs [B, T-1], gen_mask [B, T-1])."""
    out = model(input_ids=input_ids, attention_mask=attention_mask)
    logits = out.logits[:, :-1, :]
    targets = input_ids[:, 1:]
    logprobs_all = F.log_softmax(logits.float(), dim=-1)
    token_lp = logprobs_all.gather(-1, targets.unsqueeze(-1)).squeeze(-1)

    B, Tm1 = token_lp.shape
    pos = torch.arange(Tm1, device=input_ids.device).unsqueeze(0).expand(B, -1)
    prompt_lens_exp = prompt_lens.unsqueeze(1)
    gen_mask = (pos >= (prompt_lens_exp - 1)).float()
    pad_mask = attention_mask[:, 1:].float()
    mask = gen_mask * pad_mask
    return token_lp, mask


def masked_mean(x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    return (x * mask).sum() / mask.sum().clamp(min=1.0)


def grpo_loss(
    new_logprobs: torch.Tensor,
    old_logprobs: torch.Tensor,
    ref_logprobs: torch.Tensor,
    advantages: torch.Tensor,
    mask: torch.Tensor,
    clip_eps: float = 0.2,
    kl_beta: float = 0.05,
) -> tuple[torch.Tensor, dict]:
    adv = advantages.unsqueeze(-1)
    log_ratio = new_logprobs - old_logprobs
    ratio = torch.exp(log_ratio)
    surr1 = ratio * adv
    surr2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * adv
    policy_loss = -masked_mean(torch.min(surr1, surr2), mask)

    ref_log_ratio = ref_logprobs - new_logprobs
    kl_k3 = torch.exp(ref_log_ratio) - ref_log_ratio - 1.0
    kl_loss = masked_mean(kl_k3, mask)

    loss = policy_loss + kl_beta * kl_loss
    stats = {
        "policy_loss": policy_loss.item(),
        "kl": kl_loss.item(),
        "loss": loss.item(),
        "mean_ratio": masked_mean(ratio, mask).item(),
    }
    return loss, stats


# =====================================================================
# Tokenization
# =====================================================================

def tokenize_rollout(
    tokenizer,
    system_prompt: str,
    user_prompt: str,
    generation: str,
    max_length: int = 2560,
) -> dict:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    try:
        prompt_str = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
            enable_thinking=True,
        )
    except TypeError:
        prompt_str = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
        )
    prompt_ids = tokenizer.encode(prompt_str, add_special_tokens=False)
    gen_ids = tokenizer.encode(generation, add_special_tokens=False)
    full_ids = prompt_ids + gen_ids
    if len(full_ids) > max_length:
        full_ids = full_ids[:max_length]
    prompt_len = min(len(prompt_ids), max_length)
    return {"input_ids": full_ids, "prompt_len": prompt_len}


def pad_and_batch(tokenized: list[dict], pad_id: int) -> dict:
    max_len = max(len(t["input_ids"]) for t in tokenized)
    input_ids = torch.full((len(tokenized), max_len), pad_id, dtype=torch.long)
    attention_mask = torch.zeros((len(tokenized), max_len), dtype=torch.long)
    prompt_lens = torch.zeros(len(tokenized), dtype=torch.long)
    for i, t in enumerate(tokenized):
        ids = t["input_ids"]
        input_ids[i, :len(ids)] = torch.tensor(ids)
        attention_mask[i, :len(ids)] = 1
        prompt_lens[i] = t["prompt_len"]
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "prompt_lens": prompt_lens,
    }


# =====================================================================
# Main loop
# =====================================================================

def load_policy(start_adapter: Optional[Path], base_model: Optional[str] = None):
    bm = base_model or BASE_MODEL
    print(f"Loading {bm} bf16 on cuda:0 ...")
    base = AutoModelForCausalLM.from_pretrained(
        bm,
        torch_dtype=torch.bfloat16,
        device_map=__import__("os").environ.get("ICMI_DEVICE_MAP", "").strip() or {"": "cuda:0"},
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(bm, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    if start_adapter is not None and start_adapter.exists():
        print(f"Loading start adapter: {start_adapter}")
        model = PeftModel.from_pretrained(base, str(start_adapter), is_trainable=True)
    else:
        if start_adapter is not None:
            print(f"WARN: start adapter {start_adapter} not found — initializing fresh LoRA")
        model = get_peft_model(base, DEFAULT_LORA)
    model.print_trainable_parameters()
    return model, tokenizer


def run_training(
    out_dir: Path,
    batch_file: Path,
    start_adapter: Optional[Path] = None,
    G: int = 8,
    rollout_batch_size: int = 2,
    rollout_temperature: float = 1.0,
    train_batch_size: int = 1,
    train_epochs: int = 4,
    lr: float = 1e-5,
    kl_beta: float = 0.05,
    clip_eps: float = 0.2,
    max_scenarios: Optional[int] = None,
    reward_source: str = "priest",   # "priest" or "rlvr"
    base_model: Optional[str] = None,
    rollouts_override: Optional[Path] = None,  # skip Phase A, load rollouts from this file
    seed: int = 42,
    quick: bool = False,
):
    set_global_seed(seed)
    print(f"[seed] {seed}")
    out_dir.mkdir(parents=True, exist_ok=True)
    scenarios = [
        json.loads(line) for line in batch_file.read_text().splitlines() if line.strip()
    ]
    if max_scenarios is not None and len(scenarios) > max_scenarios:
        # Subset deterministically for reproducibility
        rng_ss = random.Random(seed)
        rng_ss.shuffle(scenarios)
        scenarios = scenarios[:max_scenarios]
    if quick:
        scenarios = scenarios[:4]
        G = 4
        train_epochs = 2

    system_prompt = (PROMPTS_DIR / "rollout_template.txt").read_text()

    print(f"\n{'='*70}\n[v3 training] {len(scenarios)} scenarios, G={G}\n{'='*70}")

    model, tokenizer = load_policy(start_adapter, base_model=base_model)

    # -----------------------------------------------------------------
    # Phase A: rollouts (or load pre-generated rollouts from distributed workers)
    # -----------------------------------------------------------------
    if rollouts_override is not None:
        print(f"\n[Phase A] SKIPPED — loading pre-generated rollouts from {rollouts_override}",
              flush=True)
        rollouts = []
        for line in open(rollouts_override):
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            rollouts.append(Rollout(**d))
        print(f"  loaded {len(rollouts)} rollouts", flush=True)
    else:
        print("\n[Phase A] Rollouts...", flush=True)
        model.eval()
        with torch.no_grad():
            rollouts = generate_rollouts(
                model, tokenizer, scenarios, system_prompt,
                G=G, batch_size=rollout_batch_size,
                temperature=rollout_temperature,
            )

    (out_dir / "rollouts.jsonl").write_text(
        "\n".join(json.dumps(asdict(r)) for r in rollouts)
    )
    n_malformed = sum(1 for r in rollouts if r.malformed)
    print(f"  {len(rollouts)} rollouts ({n_malformed} malformed)", flush=True)

    # -----------------------------------------------------------------
    # Phase B: reward signal
    # -----------------------------------------------------------------
    from collections import Counter
    if reward_source == "rlvr":
        print("\n[Phase B] RLVR reward (VirtueBench correctness, no priest)...", flush=True)
        # Reward: +1 if the model picked the virtuous option, 0 otherwise.
        # Malformed rollouts → virtuebench_correct is None → 0.
        rewards = [1.0 if r.virtuebench_correct is True else 0.0 for r in rollouts]
        scores = [None] * len(rollouts)  # no priest involved

        with open(out_dir / "scored.jsonl", "w") as f:
            for r, rw in zip(rollouts, rewards):
                f.write(json.dumps({
                    "base_id": r.base_id, "variant": r.variant, "virtue": r.virtue,
                    "target": r.target, "g_idx": r.g_idx,
                    "malformed": r.malformed, "virtuebench_correct": r.virtuebench_correct,
                    "priest_score": None,
                    "reward": rw,
                }) + "\n")

        ok = [r for r, rr in zip(rollouts, rewards) if not r.malformed]
        n_correct = sum(1 for r in ok if r.virtuebench_correct)
        print(f"  well-formed: {len(ok)}/{len(rollouts)}", flush=True)
        print(f"  VirtueBench accuracy: {n_correct}/{len(ok)} "
              f"= {n_correct/max(1,len(ok))*100:.1f}%", flush=True)
    else:  # priest
        print("\n[Phase B] Priest scoring (Claude Sonnet 4.6)...", flush=True)
        dicts = [asdict(r) for r in rollouts]
        scores: list[Optional[PriestScore]] = asyncio.run(score_batch(dicts))
        rewards = compute_rewards(dicts, scores)

        with open(out_dir / "scored.jsonl", "w") as f:
            for r, s, rw in zip(rollouts, scores, rewards):
                f.write(json.dumps({
                    "base_id": r.base_id, "variant": r.variant, "virtue": r.virtue,
                    "target": r.target, "g_idx": r.g_idx,
                    "malformed": r.malformed, "virtuebench_correct": r.virtuebench_correct,
                    "priest_score": s.score if s is not None else None,
                    "reward": rw,
                }) + "\n")

        ok = [r for r, s in zip(rewards, scores) if s is not None]
        print(f"  scored: {len(ok)}/{len(scores)} well-formed", flush=True)
        if ok:
            dist = Counter(int(x) for x in ok)
            print(f"  reward distribution: {dict(sorted(dist.items()))}", flush=True)
            print(f"  mean priest score: {sum(ok)/len(ok):.2f}", flush=True)

    # -----------------------------------------------------------------
    # Phase E: GRPO update
    # -----------------------------------------------------------------
    group_keys = [(r.base_id, r.variant) for r in rollouts]
    advantages_list = group_relative_advantages(rewards, group_keys)
    # Zero out advantage for malformed (they shouldn't push gradient)
    for i, r in enumerate(rollouts):
        if r.malformed:
            advantages_list[i] = 0.0

    mean_adv = sum(advantages_list) / max(1, len(advantages_list))
    print(
        f"\n[Phase E] GRPO update | n_rollouts={len(rollouts)} | "
        f"mean advantage={mean_adv:.3f}", flush=True,
    )

    tokenized = [
        tokenize_rollout(tokenizer, system_prompt, r.prompt, r.generation)
        for r in rollouts
    ]
    pad_id = tokenizer.pad_token_id
    advantages_t = torch.tensor(advantages_list, dtype=torch.float32)

    model.train()
    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad], lr=lr,
    )

    n = len(tokenized)
    perm = list(range(n))
    rng = random.Random(seed)
    for epoch in range(train_epochs):
        rng.shuffle(perm)
        epoch_stats = []
        for start in range(0, n, train_batch_size):
            idxs = perm[start:start + train_batch_size]
            mb_tokens = [tokenized[j] for j in idxs]
            batched = pad_and_batch(mb_tokens, pad_id)
            ids = batched["input_ids"].to(model.device)
            attn = batched["attention_mask"].to(model.device)
            plens = batched["prompt_lens"].to(model.device)
            adv_mb = advantages_t[idxs].to(model.device)

            new_lp, mask = sequence_logprobs(model, ids, plens, attn)
            with torch.no_grad():
                old_lp, _ = sequence_logprobs(model, ids, plens, attn)
                old_lp = old_lp.detach()
                with model.disable_adapter():
                    ref_lp, _ = sequence_logprobs(model, ids, plens, attn)

            loss, stats = grpo_loss(
                new_lp, old_lp, ref_lp, adv_mb, mask,
                clip_eps=clip_eps, kl_beta=kl_beta,
            )
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in model.parameters() if p.requires_grad], 1.0,
            )
            optimizer.step()
            epoch_stats.append(stats)

        mean = lambda k: sum(s[k] for s in epoch_stats) / len(epoch_stats)
        print(
            f"  epoch {epoch+1}/{train_epochs} | "
            f"loss={mean('loss'):.4f} policy={mean('policy_loss'):.4f} "
            f"kl={mean('kl'):.4f} ratio={mean('mean_ratio'):.3f}",
            flush=True,
        )

    # -----------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------
    adapter_out = out_dir / "adapter"
    adapter_out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(adapter_out))
    tokenizer.save_pretrained(str(adapter_out))
    print(f"\nSaved adapter -> {adapter_out}", flush=True)

    if reward_source == "rlvr":
        # For RLVR, "mean reward" is just VirtueBench accuracy on training rollouts
        mean_reward = sum(rewards) / max(1, len(rewards))
    else:
        mean_reward = (sum(ok)/len(ok)) if ok else 0.0
    summary = {
        "n_scenarios": len(scenarios),
        "n_rollouts": len(rollouts),
        "n_malformed": n_malformed,
        "mean_priest_score": mean_reward,  # semantic: whichever reward was used
        "mean_advantage": mean_adv,
        "reward_source": reward_source,
        "G": G,
        "train_epochs": train_epochs,
        "lr": lr,
        "kl_beta": kl_beta,
        "rollout_temperature": rollout_temperature,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--batch-file", type=Path, required=True,
                        help="data/rlcf_v3/batches/train.jsonl")
    parser.add_argument("--start-adapter", type=Path, default=None)
    parser.add_argument("-G", type=int, default=8)
    parser.add_argument("--rollout-batch-size", type=int, default=2)
    parser.add_argument("--rollout-temperature", type=float, default=1.0)
    parser.add_argument("--train-batch-size", type=int, default=1)
    parser.add_argument("--train-epochs", type=int, default=4)
    parser.add_argument("--lr", type=float, default=1e-5)
    parser.add_argument("--kl-beta", type=float, default=0.05)
    parser.add_argument("--clip-eps", type=float, default=0.2)
    parser.add_argument("--max-scenarios", type=int, default=None,
                        help="Subset the training set to first N (shuffled by seed 42)")
    parser.add_argument("--reward-source", choices=["priest", "rlvr"], default="priest",
                        help="priest = Claude scalar from rubric; rlvr = VB A/B correctness")
    parser.add_argument("--base-model", type=str, default=None,
                        help="HF model id for the base (default: Qwen/Qwen3.5-9B)")
    parser.add_argument("--rollouts-override", type=Path, default=None,
                        help="Skip Phase A; load rollouts from this JSONL instead (for distributed runs)")
    parser.add_argument("--seed", type=int, default=42, help="Seed for LoRA init, rollout sampling, GRPO shuffle")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()

    start = time.time()
    run_training(
        out_dir=args.out_dir,
        batch_file=args.batch_file,
        start_adapter=args.start_adapter,
        G=args.G,
        rollout_batch_size=args.rollout_batch_size,
        rollout_temperature=args.rollout_temperature,
        train_batch_size=args.train_batch_size,
        train_epochs=args.train_epochs,
        lr=args.lr,
        kl_beta=args.kl_beta,
        clip_eps=args.clip_eps,
        max_scenarios=args.max_scenarios,
        reward_source=args.reward_source,
        base_model=args.base_model,
        rollouts_override=args.rollouts_override,
        seed=args.seed,
        quick=args.quick,
    )
    print(f"\nTotal training wall-clock: {(time.time()-start)/60:.1f} min")


if __name__ == "__main__":
    main()
