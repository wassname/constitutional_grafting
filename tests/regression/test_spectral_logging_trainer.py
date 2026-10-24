"""Two-step CPU AxolotlTrainer logging smoke on a tiny random causal LM; run in the training image. -- PI/OpenAI"""
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import torch
from axolotl.core.trainers.base import AxolotlTrainer
from axolotl.core.training_args import AxolotlTrainingArguments
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import LlamaConfig, LlamaForCausalLM, default_data_collator

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.train.spectral_plugin import SpectralPlugin


def test_actual_trainer_logging(env):
    torch.manual_seed(0)
    model = get_peft_model(LlamaForCausalLM(LlamaConfig(vocab_size=32, hidden_size=16, intermediate_size=32,
        num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2, max_position_embeddings=16)),
        LoraConfig(r=2, lora_alpha=4, target_modules=["q_proj", "v_proj"], lora_dropout=0, task_type="CAUSAL_LM"))
    model.get_base_model().accepts_loss_kwargs = False
    tokens = [[1, 4, 5, 6, 7, 8, 9, 2], [1, 9, 8, 7, 6, 5, 4, 2]] * 2
    data = Dataset.from_dict({"input_ids": tokens, "labels": tokens, "attention_mask": [[1] * 8 for _ in tokens]})
    with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, env, clear=False):
        args = AxolotlTrainingArguments(output_dir=directory, use_cpu=True, max_steps=2, per_device_train_batch_size=1,
            per_device_eval_batch_size=1, gradient_accumulation_steps=2, learning_rate=1e-3, lr_scheduler_type="constant",
            warmup_steps=0, logging_strategy="steps", logging_steps=1, eval_strategy="steps", eval_steps=1,
            save_strategy="no", report_to=[], disable_tqdm=True, remove_unused_columns=False, optim="adamw_torch")
        trainer = AxolotlTrainer(model=model, args=args, train_dataset=data, eval_dataset=data,
                                 data_collator=default_data_collator, eval_data_collator=default_data_collator)
        assert not trainer.model_accepts_loss_kwargs
        SpectralPlugin().post_trainer_create(None, trainer)
        trainer.train()
        metrics = trainer.evaluate()
        train = [r for r in trainer.state.log_history if "loss" in r]
        evaluate = [r for r in trainer.state.log_history if "eval_loss" in r]
        assert len(train) == 2 and len(evaluate) >= 2
        for prefix, rows in (("train", train), ("eval", evaluate)):
            for r in rows:
                assert r[f"{prefix}_total_loss"] == r[f"{prefix}_text_loss"] + r[f"{prefix}_spectral_penalty"]
                assert abs(r[f"{prefix}_total_loss"] - r["loss" if prefix == "train" else "eval_loss"]) < 1e-3, r
        assert metrics["eval_spectral_penalty"] > 0
        assert metrics["eval_text_loss"] < metrics["eval_total_loss"]
        print(json.dumps({"environment": env, "trainer": type(trainer).__name__, "model_accepts_loss_kwargs": trainer.model_accepts_loss_kwargs, "train_records": train,
                          "eval_records": evaluate, "returned_eval_metrics": metrics}), flush=True)


if __name__ == "__main__":
    for env in ({"SPECTRAL_LAM": "50", "SPECTRAL_FRAC": ""}, {"SPECTRAL_LAM": "50", "SPECTRAL_FRAC": "0.01"}):
        test_actual_trainer_logging(env)
    print("PASS: actual AxolotlTrainer train/eval component logs and returned metrics match the optimized total, fixed and calibrated lambda.")
