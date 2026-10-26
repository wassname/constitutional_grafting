# Installed vLLM 0.31 expert-LoRA layout check

-- PI/OpenAI (Sol), 2026-10-26 UTC

Read-only source copies from the replacement's `/opt/vllm/lib/python3.12/site-packages/vllm/lora/`. These are vLLM authors' code, not ours; original license headers remain. The files were read, not imported or executed as probes. No serving-code change was made.

Question: can an adapter load successfully while its flattened expert factors are interpreted in the wrong order?

The package explicitly supports our nested PEFT names. `lora_model.py:252-255` exempts `experts.base_layer` from ordinary-name rejection, then `from_lora_tensors` still loads its tensors. `model_manager.py:958-967` says:

> Handle PEFT file format where experts.base_layer is the
> gate_up_proj and experts is the down_proj

The 3D branch reshapes A to `(E, r, in)` and B from `(out, r, E)` to `(E, out, r)` (`model_manager.py:980-1004`). This matches `scripts/train/spectral_math.py` and PEFT `ParamWrapper.get_delta_weight`, rather than assuming that B's last dimension is `(E, r)`.

```python
A_E = A.reshape(E, r, in_size)
B_E = B.reshape(out_size, r, E).permute(2, 0, 1)
ΔW_E = scale * (B_E @ A_E)
```

Here E is the expert count, r the LoRA rank, and in/out the projection dimensions. Qwen3.5's installed model declares `is_3d_moe_weight=True` (`native_moe_reference_paths.txt` under the run15 evidence directory). The default server does not enable mixed formats; vLLM chooses from the model's layout flag rather than the request's optional declaration. Current documentation: https://docs.vllm.ai/en/stable/features/lora.html . Exact installed code takes precedence over the moving main-branch documentation.

Observed runtime: native smoke accepted the unhealed D plus both final heals and six early checkpoints; all nine returned `4.` with stop on the same off-mode arithmetic prompt (`lease_retry/box_runs/adapter_smoke.json`). No merge fallback occurred. This confirms startup/activation and a normal response, not complete numerical parity or character efficacy. GPU kernels and every loader path were not audited; no native-versus-merged logits comparison was run.

Read coverage: the complete relevant `_stack_moe_lora_weights`, `_convert_3d_to_2d_moe_lora`, `from_lora_tensors` and local-checkpoint validation/loading sections. Other methods in the copied files were not fully read. `fused_moe.py`, `utils.py` and `peft_helper.py` were retained for reference, not claimed fully reviewed. File SHA256 values are in `source_sha256.json`.
