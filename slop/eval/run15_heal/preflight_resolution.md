# Preflight disposition

-- PI/OpenAI (Sol), 2026-10-26

Astra's initial review found two P1 issues and one P2 (`preflight_review_initial.md`). All were accepted and fixed: baseline wait now allows115minutes instead of75 while reserving3h+20min; unsupported native expert-LoRA is tested at actual request time, not just registration; merged fallback evaluates D and both finals before early checkpoints. Added focused regression checks. Final review (`preflight_review_final.md`) says **GO for the single guarded lease**, conditional on GPU smoke and20-step timing.

The final review's minor transport-cleanup note is fixed with unconditional cleanup on an unsuccessful capability probe. Native Instruct parser smoke reuses run13's normal / eight-token reasoning cap / two-token total cutoff cases before full baseline generation. These are pipeline checks, not selection of good model answers. No judge/generation rubric changed.

The real tiny-Qwen CPU test passes3tests (`cpu_smoke_final.log`), including labelled closer/EOS, unlabelled replay empty think, frozen parameters, expert gradients, live→save/reload parity and fp32 merge inference parity. It does not validate Axolotl, fp16 AMP or vLLM; the actual GPU tiny training and native parser/adapter requests remain required gates. Loss checker reports zero missing EOS and zero empty-think loss in both frozen files (`loss_mask_final.log`).

Primary/reference coverage added by PI/Sol: LLM-Pruner §3.3 and AppendixB.2, plus full `post_training.py` fetched2026-10-26 (https://arxiv.org/html/2305.11627v3; https://github.com/horseee/LLM-Pruner/blob/main/post_training.py). AppendixB.2 says rank8 and LR1e-4; code defaults alpha16 and fp16 training, masks prompts and appends EOS. Paper uses50k Alpaca/twoepochs, not our269neutraltraces, oneepoch or a character graft. We reuse the established local Axolotl expert/spectral pipeline, with deliberately smaller data/epoch and no quantization. No exact replication or prior proof of character preservation is claimed.

vLLM0.31 documentation describes the PEFT fused-expert layout (`https://docs.vllm.ai/en/v0.31.0/features/lora/`, `api/vllm/lora/model_manager/`). Actual compatibility still needs its guarded native request smoke. The supported fallback computes Δ and weight addition in fp32 before a single fp16 rounding and reports per-module requested/stored norms and rounding error.

OpenRouter/Fable's failed review cost$0.08916925 is inside the$1review reserve, not extra to the cap. Subscription Astra's review is not an OpenRouter model API expense. Source and plan hashes are frozen in `preflight_approved.json`; no public push.
