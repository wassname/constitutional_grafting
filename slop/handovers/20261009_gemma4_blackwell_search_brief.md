# Brief: Gemma-4 31B QLoRA on Blackwell (sm_120): which settings are needed?

Written by Claude (Opus 5.5), 2026-10-09, for a search subagent (sol). Read-only research; write one report.

## What happened

Axolotl image `axolotlai/axolotl:main-20261009-py3.12-cu130-2.14.1` (axolotl 0.20.1.dev0, torch 2.14.1+cu130, transformers 5.18.0), one RTX PRO 6000 Blackwell Server Edition (sm_120, 96 GB), QLoRA on google/gemma-4-31b-it, `attn_implementation: sdpa`, `sample_packing: false` (no flash-attn build for sm_120 in the image). First attempt, with `activation_offloading: true` and `liger_rms_norm: true` (plus Liger layer_norm and geglu, Cut Cross Entropy), crashed at step 0:

```
File "/workspace/axolotl/src/axolotl/kernels/gemma4_fused_rope.py", line 573, in _fused_rms_norm_noscale_backward
RuntimeError: Triton Error [CUDA]: an illegal memory access was encountered
```

Axolotl applies its fused Gemma-4 RMSNorm+RoPE kernel to Gemma 4 unconditionally ("Gemma 4 always uses the fused path", schema description of `fused_attn_kernel`). Turning off both `activation_offloading` and `liger_rms_norm` made training work (149 steps, normal loss). Which one mattered is unknown.

## Questions

1. Is this a known issue (Axolotl GitHub issues/PRs, Discord notes, release notes): the fused Gemma-4 norm kernel with activation offloading, or with Liger RMSNorm, or on sm_120?
2. What do the reference configs do: Axolotl `examples/gemma4/31b-qlora.yaml` (main), Unsloth's Gemma 4 notebooks/docs, and any other well-used Gemma 4 fine-tuning recipe? Specifically: activation offloading, Liger kernels, attention implementation, packing, max_grad_norm, learning rate.
3. Are activation offloading and Liger RMSNorm needed for 31B QLoRA on a 96 GB card (we used ~25 GB peak)? What do they buy?
4. For Blackwell sm_120: is there a flash-attention build or the `gemma4_hybrid_attn_impl` path that works, so we can re-enable sample packing?

Quote sources verbatim with links and dates (varglight style: /home/code/.pi/agent/skills/varglight/SKILL.md). Say clearly where you found nothing.

## Output

`/workspace/2026/constitutional_grafting/slop/research/20261009_gemma4_blackwell_settings.md`, under ~800 words, with a short recommendation table (setting, keep/turn on/turn off, source). Sign it.
