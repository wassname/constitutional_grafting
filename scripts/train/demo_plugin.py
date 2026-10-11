"""Fixed OOS demos in the live Axolotl trainer. OpenAI Codex, 2026-10-09."""

import json
import re
from pathlib import Path

import torch
from axolotl.integrations.base import BasePlugin
from transformers import GenerationConfig, TrainerCallback

ROOT = Path(__file__).resolve().parents[2]
PROMPTS = ROOT / "configs/train/demo_prompts.json"


def fence(text):
    # Preserve generated fences rather than letting them break the report.
    delimiter = "`" * max(3, max(map(len, re.findall(r"`+", text)), default=0) + 1)
    return f"{delimiter}text\n{text}\n{delimiter}\n"


class DemoCallback(TrainerCallback):
    def __init__(self, trainer, stage):
        self.trainer = trainer
        self.stage = stage
        self.probes = json.loads(PROMPTS.read_text())[stage]

    def emit(self, args, state, event):
        trainer = self.trainer
        # These QLoRA configs are single-device. Do not silently deadlock on FSDP/ZeRO.
        if trainer.accelerator.num_processes != 1 or trainer.is_deepspeed_enabled or trainer.is_fsdp_enabled:
            raise RuntimeError("Fixed demos currently support single-process, non-sharded training only")
        tokenizer = trainer.processing_class
        if not hasattr(tokenizer, "encode"):
            tokenizer = tokenizer.tokenizer  # multimodal processors, text-only probes
        model = trainer.accelerator.unwrap_model(trainer.model_wrapped)
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        md = output_dir / "demos.md"
        raw = output_dir / "demos.jsonl"
        was_training = model.training
        model.eval()
        try:
            # Preserve training RNG: inference must not change dropout's next draw.
            devices = list(range(torch.cuda.device_count()))
            with torch.random.fork_rng(devices=devices), torch.inference_mode():
                for probe in self.probes:
                    prompt = probe["prompt"]
                    messages = None
                    if self.stage == "sft":
                        messages = [{"role": "user", "content": prompt}]
                        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)  # qwen3.5: no thinking; gemma ignores it
                    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=self.stage == "graft").to(model.device)
                    # Fresh config avoids inherited sampling/beam settings; retain model-specific EOS.
                    config = GenerationConfig(
                        do_sample=False, num_beams=1, max_new_tokens=probe["max_new_tokens"],
                        eos_token_id=model.generation_config.eos_token_id,
                        pad_token_id=tokenizer.pad_token_id,
                        bos_token_id=tokenizer.bos_token_id, use_cache=True,
                    )
                    generated = model.generate(**inputs, generation_config=config)
                    prompt_ids = inputs["input_ids"][0].tolist()
                    reply_ids = generated[0, len(prompt_ids):].tolist()
                    record = dict(stage=self.stage, event=event, step=state.global_step,
                                  probe=probe, messages=messages, generation_config=config.to_dict(),
                                  prompt_ids=prompt_ids, reply_ids=reply_ids,
                                  input=tokenizer.decode(prompt_ids, skip_special_tokens=False),
                                  reply=tokenizer.decode(reply_ids, skip_special_tokens=False),
                                  reached_token_limit=len(reply_ids) >= probe["max_new_tokens"])
                    if probe["kind"] == "content":
                        choice = tokenizer.decode(reply_ids, skip_special_tokens=True).strip()
                        record["choice"] = choice if choice in {"A", "B"} else "INVALID"
                    with raw.open("a") as f:
                        f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    with md.open("a") as f:
                        f.write(f"\n## {self.stage} / {event} / step {state.global_step:06d} / {probe['id']}\n\n"
                                f"Kind: {probe['kind']}; choice: {record.get('choice', 'n/a')}; greedy; "
                                f"token limit reached: {record['reached_token_limit']}. "
                                f"Raw trace: `{raw}` (event/step/probe above).\n\n"
                                f"### Input (special tokens included)\n\n{fence(record['input'])}\n"
                                f"### Reply (special tokens included)\n\n{fence(record['reply'])}")
        finally:
            model.train(was_training)
        print(f"Fixed OOS demos: {md} (raw: {raw})", flush=True)

    def on_train_begin(self, args, state, control, **kwargs):
        # Resumed runs honestly log the restored step, not a fictitious step zero.
        self.emit(args, state, "init")

    def on_evaluate(self, args, state, control, **kwargs):
        self.emit(args, state, "eval")

    def on_train_end(self, args, state, control, **kwargs):
        self.emit(args, state, "end")


class SFTDemoPlugin(BasePlugin):
    def add_callbacks_post_trainer(self, cfg, trainer):
        return [DemoCallback(trainer, "sft")]


class GraftDemoPlugin(BasePlugin):
    def add_callbacks_post_trainer(self, cfg, trainer):
        return [DemoCallback(trainer, "graft")]
