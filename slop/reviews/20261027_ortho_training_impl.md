# Training-time two-sided orthogonality

Implemented and committed as `e8a4dcfa1e124c0866784d640e6729568e97f08a` (`ortho-train: project chat LoRA factors after every optimizer step`, requested Claude co-author trailer). No GPU rental or paid API calls. **PI/Sol**, 2026-10-27.

## Implementation

Changed only:
- `scripts/train/16_project_chat_adapter.py`: `--save-basis PATH`, `--basis-rank` (default 64), fp16 U/V export inside the existing full-SVD loop; records quantization error in file metadata and `projection.json`. Existing `--device cpu` is exercised. Removed fixed 256-expert/330-stem assertions so the same CLI handles the real tiny model; configuration, factor, rank and matrix-shape checks remain.
- `scripts/train/ortho_plugin.py`: Axolotl `OrthoPlugin`, `ORTHO_BASIS` required. CPU-resident FP32 bases, QR-reorthonormalized once after loading fp16. Projects both factors at plugin initialization, again on train begin (including resumed weights), and every optimizer boundary via `on_step_end`. **N=1**, not occasional projection. Adam moments are untouched. Logs `ortho_max_UT_B` and `ortho_max_A_V`, maximum per-matrix/expert Frobenius residuals, at Trainer log boundaries; prints the SHOULD invariant. Missing/extra stems or mismatched shapes fail loudly. Coexists with spectral loss/logging.
- `tests/regression/test_ortho_plugin.py`: tiny real Qwen-MoE from pinned config, actual CLI export from perturbed checkpoint subtraction, real PEFT targeting/rank patterns, real Trainer/AdamW/spectral calibration, init and every-step matrix assertions, six microsteps/three optimizer steps, changed loss, plain-adapter save/reload, missing-basis/shape failures, and a separate k=64 factor test.
- `justfile`: adds that test file to `check-projection`.

File layout: safetensors keys `<adapter-stem>.U` and `<adapter-stem>.V`, each `[experts, matrix-side-size, k]`; dense modules have a singleton expert dimension. Uses the exporter's actual `parameter_name`, `unpack_factors`, `pack_factors`, and `project_factors`, including the nested expert wrappers. No second SVD pass.

### Precision and mathematical scope

For the loaded/reorthonormalized bases, projection is `A -= (A @ V) @ V.T`, `B -= U @ (U.T @ B)`, hence the same two-sided operation on `s·B·A`. Floating-point arithmetic is not literally exact. FP16 storage also perturbs the original tau singular spaces: the tiny real-model export measured maximum absolute element error **0.000237525** and maximum batch-relative Frobenius error **0.000245310**. These exact measurements are saved for each production export, not assumed universal. CPU FP32 QR restores orthonormality of the stored span, rather than repeatedly shrinking factors with a non-orthonormal quantized projector. The tests separately check the original unquantized tau subspaces with relative tolerance `3e-4`, and the working subspaces with absolute tolerance `2e-6`.

Final tiny-model logged residuals: `||UᵀB|| = 6.19e-9`, `||AV|| = 4.47e-8`; fixed-example text loss changed **12.4511099 → 12.4216242**. Both routed matrices in each of two layers are checked for all 32 experts (128 expert matrices), alongside all dense targets. Expert rank-pattern application is explicitly asserted despite PEFT's known misleading unmatched-pattern warnings.

This follows the requested hard projected-update contract, not an exact reproduction of O-LoRA. PI/Sol read O-LoRA §3.2–3.3 and its `src/uie_trainer_lora.py` regularization block: the paper uses an orthogonality penalty between successive adapter subspaces; the reference code adds absolute cross-factor overlap and L2 terms. Here the protected spaces instead come from Base→Instruct tau, and both factors are explicitly projected after optimization. The existing project script is the operative reference implementation. No extra paper-specific training stages were added.

## Memory choice: full two-sided bases on CPU, every step

Calculated from the **actual existing `r10_cx_chatr12` safetensors header**:

| k=64 bases | FP16 | FP32 |
|---|---:|---:|
| Routed gate_up: 40×256×(1024+2048)×64 | 3.750 GiB | 7.500 GiB |
| Routed down: 40×256×(2048+512)×64 | 3.125 GiB | 6.250 GiB |
| All 250 dense stems | 0.142822 GiB | 0.285645 GiB |
| Total, 330 stems / 660 tensors | **7.017822 GiB** | **14.035645 GiB** |

FP16 alone might fit on the previous box, but resident FP32 orthonormal bases plus the observed **79.3 GiB** training peak predict **93.34 GiB** before further headroom. Keeping FP32 bases on CPU avoids that risk without dropping either side or allowing between-step constraint violations. No bases live on GPU. Projection copies one stem's factors to CPU and back; it does not construct full expert delta matrices. Live LoRA parameters remain in their existing dtype (normally FP32 under PEFT); casting back is included in measured residuals.

Allow approximately **24 GiB additional available host RAM during basis loading/QR**, including file-backed fp16 pages, then **14.04 GiB plus per-stem temporaries** during training. Export should have at least **32 GiB available host RAM**; it accumulates bases and one projected adapter while subtracting checkpoint tensors. These are incremental estimates, not measured full-model host peaks.

The source/final adapter contains **3,997,800,800 bytes (~3.723 GiB)**. Every step copies approximately that much each direction; CPU projection trades PCIe traffic and CPU time for GPU headroom. No claim of zero runtime overhead.

## Exact commands for the separate lease

Run in the same configured GPU/Axolotl environment as `14_run10_chat_box.sh`, from `/workspace/cg`. These are instructions only: **not executed here**. Upload the four named adapter directories under `ADAPTER_ROOT` before running. The stem-list source must be the existing `r10_cx_chatr12`, not a newly constructed adapter. Ensure both pinned snapshots are fully materialized and use their canonical fused expert checkpoint layout. Fresh output directories below are intentional; exporter refuses overwrites/incomplete basis saves.

```bash
set -euo pipefail
cd /workspace/cg
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
export HF_HOME=/workspace/hf
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8
export BASE="$HF_HOME/hub/models--Qwen--Qwen3.5-35B-A3B-Base/snapshots/0f0813072d2358973511097385626f21fcb6d422"
export INSTRUCT="$HF_HOME/hub/models--Qwen--Qwen3.5-35B-A3B/snapshots/59d61f3ce65a6d9863b86d2e96597125219dc754"
export ADAPTER_ROOT="$HOME/.local/share/cg_run10_adapters"
export ORTHO_BASIS="$PWD/runs/ortho/tau_k64.safetensors"
mkdir -p runs/ortho

# (a) tau is untouched Instruct minus untouched Base, NOT minus Base+documents.
python scripts/train/16_project_chat_adapter.py \
  "$BASE" "$INSTRUCT" "$ADAPTER_ROOT/r10_cx_chatr12" \
  runs/ortho/basis_projection \
  --ranks 64 --basis-rank 64 --device cuda --batch-experts 8 \
  --save-basis "$ORTHO_BASIS" \
  > runs/ortho/basis_projection.log 2>&1

# (b) Same document training base as new-D: Base + .5 Stoic + 1 Const + 1 Other.
export CHAT_BASE="$PWD/outputs/base_stoic_0.5_const_1_other_1_ortho"
IT="$BASE" python scripts/train/02_merge.py \
  "$BASE" "$ADAPTER_ROOT/r10_stoic" "$CHAT_BASE" 0.5 \
  --add "$ADAPTER_ROOT/up_const" 1 --add "$ADAPTER_ROOT/r10_other" 1 \
  > runs/ortho/merge_chat_base.log 2>&1

# Same chat settings as 14_run10_chat_box.sh: two epochs, eval once/epoch,
# standard dense r64/a128 and expert r16/a32, spectral fraction .01.
python - <<'PY'
import os
from pathlib import Path
import yaml
c = yaml.safe_load(Path('configs/train/qwen3/sft.yml').read_text())
c.update(
    base_model=os.environ['CHAT_BASE'],
    output_dir='outputs/ortho_chatr12',
    dataset_prepared_path='outputs/prepared_ortho_chatr12',
    datasets=[{'path': 'data/train/eos_fixed/chatr12.jsonl',
               'ds_type': 'json', 'type': 'input_output'}],
    num_epochs=2, evals_per_epoch=1, bf16=True, fp16=False,
    plugins=[
        'scripts.train.spectral_plugin.SpectralPlugin',
        'axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin',
        'axolotl.integrations.liger.LigerPlugin',
        'axolotl.integrations.kernels.KernelsPlugin',
        'scripts.train.router_dtype_plugin.RouterDtypePlugin',
        'scripts.train.ortho_plugin.OrthoPlugin',
    ],
)
Path('runs/ortho/chat.yml').write_text(yaml.safe_dump(c, sort_keys=False))
PY
python scripts/train/check_loss_mask.py data/train/eos_fixed/chatr12.jsonl
SPECTRAL_FRAC=0.01 axolotl train runs/ortho/chat.yml \
  > runs/ortho/train.log 2>&1
python scripts/train/41_expert_adapter_check.py outputs/ortho_chatr12 \
  | tee runs/ortho/expert_check.log
```

Use the EOS-fixed **1,636-row** dataset, never historical `data/train/run10/chatr12.jsonl`. Do not initialize training with `basis_projection/k64`: that is an incidental post-hoc projected copy of the old adapter, not the new chat adapter. The plugin projects the fresh PEFT initialization itself. Keep `ORTHO_BASIS` set on resume, and do not replace the basis file during a run.

### Outputs, time and memory expectations

- `runs/ortho/tau_k64.safetensors`: ~7.018 GiB, including basis metadata and actual fp16 error.
- `runs/ortho/basis_projection/{projection.json,modules.jsonl,k64/adapter_*}`: existing projection outputs; k64 adapter ~3.723 GiB and unused for new training. Production must report `complete: true` and cover 330 stems / 20,480 routed expert matrices.
- `outputs/ortho_chatr12/{adapter_model.safetensors,adapter_config.json}` plus normal checkpoints/Trainer records; fresh plain LoRA, same config and approximate size as the stem-list adapter. Prepared dataset cache is separate from all earlier runs.
- `runs/ortho/train.log`: both plugin SHOULD lines, spectral calibration, finite text/spectral losses, and factor residuals near zero relative to factor norms. Tiny FP32 residuals are not a universal absolute threshold for the full model; k64 random-factor CPU benchmark residuals were ~`1.4e-5` with much larger random factors.
- Historical full-SVD run14 projection took **2,086.87 s (~34.8 min)** and peaked at **0.501 GiB allocated CUDA memory** (`slop/eval/run14_box_a/lease/box_runs/projection.json`). Basis export reuses those SVDs; allow roughly **35–45 min** plus storage variability. This is an estimate, not a new GPU measurement.
- Local eight-thread CPU benchmark at production expert shapes: gate_up projection+packing **0.0681 s/stem**, down **0.0587 s/stem**; ×40 gives **5.07 s/optimizer step**. Residual measurement adds **1.29 s/step** at logging_steps=1, plus dense targets, CPU/GPU transfers, and host contention. QR initialization extrapolates to about **61 s** for routed bases, plus loading/dense work.
- Plan for approximately **6–10 s additional time per optimizer step**. At roughly 778 optimizer steps for two epochs with 5% validation and accumulation 4, this adds **~1.3–2.2 hours** to the ordinary new-D chat training time. Neither full-GPU training throughput nor PCIe transfer time was measured here. Retain the previous training memory allowance; plugin persistent GPU basis cost is zero, but no unmeasured peak is guaranteed.

## Validation and known limits

- `OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 just check-projection`: **9 passed**, final run 14.26 s; all previous seven pass. Two known PEFT rank/alpha-pattern warnings; effective expert rank is asserted.
- Targeted test with `pytest -q -s ... tests/regression/test_ortho_plugin.py`: **2 passed**, emitted precision, residual and loss evidence above.
- Representative production-shape CPU benchmark: passed for both 256-expert matrices at k64/r16.
- `git diff --check -- <four named files>` and staged diff check: passed. One earlier unrestricted diff check found existing whitespace in unrelated dirty files; none were modified/staged by this work. Final staged-file list is empty.
- Initial regression attempt exposed Transformers 5.20's automatic expert-unfusing on `save_pretrained`; test snapshots now explicitly set `save_original_format=False`, keeping the same fused tensors as pinned production snapshots. No production fallback or name guessing was added.
- Axolotl's `BasePlugin` import is stubbed only in CPU tests; actual Transformers Trainer, optimizer, PEFT, Qwen model, callbacks, export and spectral code execute. Full Axolotl GPU/scattermoe/image integration remains for the lease's initial checks. No paid or GPU smoke was run.
- This targets the single default adapter with the exact supplied target configuration. It is not a sharded/FSDP/DeepSpeed/multi-adapter implementation.
- Plain LoRA storage and merging remain linear in graft dose. The CPU basis file/plugin is needed only for training/resume, not inference. BF16 merged-weight rounding can perturb the mathematical constraint slightly. Keep every chat adapter on the document base/doses it trained with; use thinking off for serving.
- Orthogonality to top-k tau spaces does not establish preserved capability or target character. It leaves other tau directions and nonlinear interactions untouched. Adam state intentionally may contain protected-direction components; re-projection restores the factor constraint after each actual update. Compare resulting character/capability at matched behavioral effect, not equal coefficient.

Independent reviewer gate remains required before lease execution. No unrelated worktree changes were included in the commit.

— **PI/Sol**
