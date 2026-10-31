# Opt-in hot cells

`hot_swap: true` in a run config keeps one vLLM 0.31 server per `cells.py` invocation (probes and full cells). Omit it to retain merge-and-restart. No existing run config is changed. -- PI/OpenAI

Each cell starts from pristine Instruct safetensors, rounds to fp16, and applies adapters in listed order using `02_merge.py:merge_adapter`, including PEFT routed-expert wrappers. Transformers handles checkpoint/expert conversions. The union of affected decoder layers across the invocation's adapters is reloaded, including frozen siblings needed by fused parameters; omitted adapters are therefore removed, and zero restores Instruct.

The preparer runs in the Axolotl environment on CPU and writes HF-named weights to a temporary safetensors file. vLLM's worker extension uses the supported layerwise reload helpers and `model.load_weights` to repack experts and copy into existing kernel storage. It checks that parameter addresses did not change. Between cells, generation is paused, weights reloaded, the prefix cache reset (success required), and generation resumed. Any failure exits the batch; there is no cold fallback. The dev endpoints are bound to localhost only.

This first path supports decoder-layer LoRA adapters without saved modules, biases or layer replication; unsupported targets fail. It needs host RAM and temporary disk space proportional to the affected layers, potentially most of 35B, plus PEFT merge/conversion temporaries. It does not promise a 35B latency or memory improvement without measurement. CUDA graph storage preservation is asserted, but eager tiny smoke is not a captured-graph or Blackwell validation.

## Fast GPU smoke

Check `pueue status`, then queue:

```sh
pueue add -o 10 just box-hot-smoke .local/hot_smoke_unique
```

The output directory must not exist. This creates `box.py:tiny_model` (two-layer random Qwen3.5-MoE, four experts), two tiny nonzero LoRAs targeting attention and routed experts, and runs three cells through real `cells.py --probe --smoke-rows 1`: a two-adapter mixture, a negative single-adapter dose, then zero. One vLLM server, eager mode, eight panel tokens and 32 maths tokens; the hot phase must finish within 300 seconds. Runtime assurances only, not behavioural evidence.

For exact temperature-zero hot/cold comparisons, also run the longer equivalence check:

```sh
pueue add -o 10 .local/axolotl_env/bin/python scripts/box/hot_smoke.py --equivalence --out .local/hot_equivalence_unique
```

`evidence.json` records exact panel/maths outputs, timings and equality assertions. The cold side uses the existing merge/restart path, including a fresh zero-dose Instruct merge. It takes three extra server starts and is not the fast smoke.

For the full maintained `just box-smoke CONFIG`, set `hot_swap: true` in a **new, non-live** config. `box.py` passes it into probes and final cells, and includes both hot implementation files in rental smoke receipts. The fast smoke does not replace that full pipeline/rental gate.

Proposed AGENTS.md line (not applied): “Opt into `hot_swap: true` for one local vLLM server per cells invocation; run `just box-hot-smoke` via pueue and the full box smoke on a new config before renting; hot-swap errors abort, never fall back.”
