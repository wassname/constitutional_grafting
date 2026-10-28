# Research: how axolotl / vLLM keep their own end-to-end tests fast

## Summary
Both projects cut wall-clock three ways: shrink the model (published "tiny" repos, or `hf_overrides` such as `num_hidden_layers: 4`), delete whole startup phases (`torch.compile`, cudagraph capture, memory profiling, weight loading, dataset tokenisation), and collapse boundaries — axolotl's e2e tests call `train()` in-process instead of `accelerate launch`, and vLLM's CI re-uses one server per module instead of restarting per test. Neither publishes seconds-per-phase, so savings below are estimates against your measured 40–60 s/boot and 54–170 s/step.

## Ranked techniques

| # | Technique | Expected saving (your pipeline) | Keeps real path? | Source |
|---|---|---|---|---|
| 1 | Don't enable `torch_compile` in the smoke config | docs: compile "adds 5–15 min on the first step" — biggest lever if any yml sets it | Yes | [axolotl optimizations](https://docs.axolotl.ai/docs/optimizations.html) |
| 2 | One server boot per model, not two (re-use fixture / one `--reasoning-parser` server serving both request shapes) | ~40–60 s per extra boot, ×N models | Partly (the no-parser boot is a distinct config) | [vLLM issue #23590](https://github.com/vllm-project/vllm/issues/23590) |
| 3 | In-process `validate_config()`/`load_datasets()`/`train()` instead of `axolotl train` → `accelerate launch` | one extra interpreter + torch/CUDA import (~5–20 s of your 54–170 s) | Partly (skips CLI + accelerate path) | [test_lora_llama.py L55–59](https://github.com/axolotl-ai-cloud/axolotl/blob/main/tests/e2e/test_lora_llama.py#L55-L59) |
| 4 | `--kv-cache-memory` to skip startup memory profiling | "skips the memory-profiling measurement and the CUDA-graph memory estimation pass" (no figure given) | Yes (only KV sizing differs) | [vLLM optimization docs](https://docs.vllm.ai/en/stable/configuration/optimization/) |
| 5 | `-O0` in addition to `--enforce-eager` | no autotune, no fusions, no compile, no cudagraphs — "startup as fast as possible" | Yes | [optimization_levels](https://docs.vllm.ai/en/latest/design/optimization_levels/) |
| 6 | Serve the adapter (`--enable-lora`, `/v1/load_lora_adapter`) instead of merging + reloading | removes merge write/read of a 35B checkpoint and one boot per model | **No** — skips the merge you want to smoke-test | [vLLM LoRA docs](https://docs.vllm.ai/en/stable/features/lora/) |
| 7 | Tiny/shrunk model: `axolotl-ai-co/tiny-*` or `hf_overrides={"num_hidden_layers": 4}` | load ∝ size; code comment: "Override the backbone layers to 4 for faster startup" | Yes | [test_blackwell_moe.py](https://github.com/vllm-project/vllm/blob/main/tests/quantization/test_blackwell_moe.py) |
| 8 | Dataset: cached prepared dataset, `shards`, `val_set_size: 0`, `max_steps: 1`, `--dataset_num_proc=1` | de8a625: "use 10% split of alpaca dataset to speed up dataset loading/tokenization" | Yes | [commit de8a625](https://github.com/axolotl-ai-cloud/axolotl/commit/de8a625dd7205c335f8201597d741e6de95de06d) |
| 9 | `--load-format dummy` to *isolate* load time (not to pass the test) | skips download + weight load; vLLM default in comparisons since "usually we don't need real weights" | No (random weights) | [tests/utils.py](https://github.com/vllm-project/vllm/blob/main/tests/utils.py), [troubleshooting](https://docs.vllm.ai/en/latest/usage/troubleshooting/) |
| 10 | Pre-download weights into the image, run offline | moves HF-hub latency out of every boot | Yes | [cicd/cicd.sh](https://github.com/axolotl-ai-cloud/axolotl/blob/main/cicd/cicd.sh) (`prepare_hf_cache.sh`) |

## Notes and exact quotes

- **In-process training is the house style.** `tests/e2e/test_mixtral.py` and `test_lora_llama.py` never shell out: `cfg = validate_config(cfg); normalize_config(cfg); dataset_meta = load_datasets(cfg=cfg); train(cfg=cfg, dataset_meta=dataset_meta)`, then assert `adapter_model.safetensors` exists. Models are 25–130M `axolotl-ai-co/tiny-*` ("Useful for e2e smoke tests across real pretrained models to validate loss behavior"). Your 54–170 s fits process startup + dataset tokenisation, not the step.
- **Test selection, not parallelism, is axolotl's GPU lever.** `cicd/cicd.sh` uses `-n8 --dist loadfile` for CPU tests but runs e2e serially — "Serial: parallel workers OOM the GPU" — filtered with `-m "not slow"`; tiny-model smokes there use `max_steps: 3`.
- **axolotl debugging recipe** (`docs/debugging.qmd`) is a ready minimal config: `--max_steps=1 --micro_batch_size=1 --val_set_size=0 --sample_packing=False`, plus `shards: 20` to shrink a dataset.
- **vLLM treats a second boot as waste.** Issue #23590: fixtures should be set "such that ... we re-use the running server as much as possible and don't stop/start a new vLLM instance for each test", preferring package-scoped over module-scoped; the proposed unified arg set matches your shape (`--enforce-eager --gpu-memory-utilization 0.8 --max-model-len 8192 --enable-lora`).
- **`--enforce-eager` may not be the floor.** `-O0` also sets `cc.cudagraph_mode=NONE`, `cc.mode=NONE`, disables fusions and `enable_flashinfer_autotune`; one bug report measured "init engine (profile, create kv cache, warmup model) in 10 seconds" with eager on, i.e. capture/profiling dominated the boot ([#52682](https://github.com/vllm-project/vllm/issues/52682)).
- **Merging has no upstream fast path.** Neither repo tests "merge then serve" — vLLM keeps adapters separate (`--enable-lora`, `VLLM_ALLOW_RUNTIME_LORA_UPDATING=True`, filesystem resolver). Keeping the merge is what makes `--load-format dummy` unusable for you.
- **Import/CUDA init:** no repo publishes `python -X importtime` numbers; their only structural tricks are not paying for a second interpreter (row 3) and not re-downloading (row 10). Measure yours with `python -X importtime -c "import axolotl.cli.train"`.
- **Qwen3.5 specifics:** `tests/models/registry.py` pins `Qwen3_5MoeForCausalLM` to `codecho/Qwen3.5-35B-A3B-text-only` with `max_model_len=4096`, and `Qwen3_5ForCausalLM` to a `-text-only` 0.8B — a cheaper *real* architecture than a random 2-layer MoE.

## Sources
- Kept: axolotl `tests/e2e/*`, `cicd/cicd.sh`, `docs/debugging.qmd`, `docs/optimizations.qmd`, commit de8a625; vLLM `tests/utils.py`, `tests/models/registry.py`, `tests/quantization/test_blackwell_moe.py`, `docs/configuration/optimization.md`, `docs/design/optimization_levels.md`, `docs/features/lora.md`, issues #23590/#52682.
- Dropped: `vllm-omni` marker PRs and `tests/compile/correctness_e2e` (different CI layout, no reusable numbers); xtuner commit (third-party, tangential); stale v0.x `cli/serve` mirrors of the same flags.

## Gaps
- No published per-phase timings (boot with/without eager; profiling cost on a 3090; merge cost for a 35B MoE). Time your own boot with `--kv-cache-memory` + `-O0` versus current flags.
- Line numbers are from raw files read 2026-10-28 and may drift ±2 lines; symbol names are exact. `--disable-frontend-multiprocessing` savings couldn't be quantified and the flag is being deprecated, so it's excluded.

-- researcher subagent
