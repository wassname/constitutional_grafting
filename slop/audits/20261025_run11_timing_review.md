## Recommendation: protect document evaluations first; treat batching change as conditional, not equivalent

**Use A as the allocation safeguard. Consider B only after a short boundary check demonstrates both valid loss scaling and enough measured speedup.** Do not interrupt Stoic training. Do not commit to all chat jobs on the assumption that doubling microbatch size halves runtime.

### Timing assessment

Using the supplied historical rate of approximately 1.8 seconds per training-row exposure:

| Chat training | Two-epoch training exposures, approximately | Estimated runtime |
|---|---:|---:|
| chatr13 | 3,416 | 1.7 h |
| matched generic control | 17,894 | 8.9 h |
| chatmix | 12,318 | 6.2 h |
| **Total** | **33,629** | **16.8 h** |

These exclude additional setup, saves and evaluation overhead. The inspected Const scan supports abandoning token-only forecasts: **1,186 updates in 15,140 seconds**, despite nearly matching replay’s supervised tokens.

Extrapolating document row throughput suggests Stoic takes roughly **4.9–5.2 hours from its start**, leaving approximately **16 hours until the evaluation deadline** if that estimate holds. Thus the unchanged chat schedule cannot plausibly preserve useful evaluations.

Even an optimistic **2× chat speedup gives 8.4 hours**, before overhead—not assurance that every planned cell fits.

### B is not automatically objective-equivalent

The production configuration uses unpacked sequences, assistant-only labels and variable-length answers (`configs/train/qwen3/sft.yml`). Effective batch size four is necessary, but insufficient:

- **CE normalization is unresolved.** If each microbatch returns its own token-mean loss, GA4 over singleton conversations weights conversations differently from GA2 over pairs. Equivalence requires the actual Axolotl/Trainer/CCE path to normalize supervised-token sums consistently across the complete accumulation group. That implementation was not available in the inspected artifacts.
- **Spectral estimation changes.** `scripts/train/spectral_plugin.py:53–58` computes and updates the power-iteration state on every `compute_loss` call. Microbatch2/GA2 halves training-time iterations per optimizer update relative to microbatch1/GA4.
- **Calibration can change.** At `:59–65`, λ is fixed using the mean returned loss and penalty over `10 × gradient_accumulation_steps` calls. Both configurations nominally cover about ten updates, but average different microbatch losses and differently evolved penalty estimates. If returned CE is accumulation-normalized, even its numerical scale can change.
- **Memory remains uncertain.** A 77-GiB document peak does not establish safety for two padded chat sequences approaching 4,220 tokens.

These are reasons to check B, not proof that B is unusable. Applying B uniformly to all unstarted chats preserves a consistent new recipe, but it must be reported as a batching change—not exact replication of earlier chat training.

### Bounded sequence

1. **At the completed Stoic boundary, secure document evidence first:** scheduled Base loss plus a bounded priority block containing independent document-dose cells and paired plain/anchored cells. Preserve pairs rather than collecting isolated anchored results. Budget from actual elapsed times, not the old forecast.
2. **Only if sufficient time remains, allow one short batching check**, capped at roughly **20–30 minutes including loading**. If validation cannot be completed within that cap, retain A; do not spend the lease debugging a new training configuration.
3. **Launch the full chat comparison only if measured throughput supports all required trainings plus their evaluations**, with explicit allowance for saves/loading and timing uncertainty. Reserve at least the chatr13, plain-chatmix and anchored-chatmix evaluation cells before spending the training time. Leave the existing retrieval margin untouched.
4. **If that gate fails, finish document evaluations and mark goal 3 incomplete.** A standalone chatr13 training/evaluation may fit, but must not be presented as the anchored-chat experiment. Do not shorten all chats to one epoch merely to claim completion.

### Exactly what the runtime check must establish

- **Loss/gradient scaling:** same four fixed, unequal-length labelled examples and same starting state under both batch arrangements; inspect accumulated CE gradients and the nonzero spectral contribution. Compare before optimizer stepping. Identify whether `num_items_in_batch` or equivalent normalization reaches CCE, and how Trainer scales the plugin’s added penalty.
- **Calibration:** determine the units of `orig()`’s returned loss and exercise the λ-fixing branch. A shortened warmup can check plumbing, but cannot predict production λ.
- **Memory and throughput:** real forward/backward/optimizer steps on representative rows and long padded pairs; record allocated/reserved peak memory and steady seconds per optimizer update, excluding startup. Include spectral computation. One successful short-row step is insufficient.
- **Resolved settings:** same effective batch, actual optimizer-step count, two epochs, masking, and unchanged learning-rate schedule apart from unavoidable rounding.

**Interpretation:** A protects the approved scientific comparisons already paid for. B is potentially useful engineering within the same method, but its speed and normalization must be demonstrated. No current evidence supports calling it free or exactly equivalent.

## Implementation follow-up

Source: reviewer-openai / gpt-6-astra, run dec9409d-447d-4536-a31c-e363e74cb073; archived verbatim by PI/OpenAI.

## Verdict: conditional PASS — one handover safety gate

No blocking adapter, donor, dose or dependency defect found in the wrapper. Document evaluations precede optional chats; the chatmix dependency and relative symlink are correct. Half anchored chat correctly uses **mix=0.5, control=−0.5**. Snapshot has no stop/destroy call path.

### 1. Block handover until exit-marker ownership is explicit

**Evidence:** `scripts/eval/38_run10_chat_rental.py:186–189` treats *any* remote `job.exit` as termination. Its `attach()` finally calls `retrieve_or_stop()` (`:468`), which can destroy the lease after successful retrieval—even if a replacement wrapper is running.

The new `slop/eval/run11/lease1/remaining_stages.py:49,98` runs phases and returns, but **does not itself write `job.exit`**. Retiring the old launcher can cause its enclosing shell to write an administrative exit marker.

**Required minimal handover conditions:**
- Verify the old local controller is dead **before** retiring the remote launcher; do not allow its cleanup/finally path to run.
- After the old enclosing shell has definitively exited, archive/remove its remote `job.exit`. Clear/archive any local `box_runs/job.exit` too: retrieval uses non-deleting rsync (`38_run10_chat_rental.py:113–121`), so an absent remote marker does not remove a stale local one.
- Launch the replacement under an explicit exit-status-recording shell, with that shell the **only remaining writer** of the active `job.exit`.
- Reattach only after confirming the replacement tmux session is live and no administrative exit marker remains. Maintain heartbeat coverage through the handover.

**Uncertainty:** The actual handover command was not supplied, so these conditions are not verified. If already implemented, this gate is satisfied; no further redesign is needed.

### Checks passed and evidence limits

- Required-adapter registration occurs before selected work (`remaining_stages.py:81–83`); successful-exit retrieval checks exact equality against the explicit plan (`38_run10_chat_rental.py:122–130`).
- `snapshot()` calls only `retrieve_outputs()` (`:423–428`); failures do not enter destructive recovery.
- Optional training is budget-gated, but the estimate is not a runtime guarantee. Document-first ordering protects already-funded evaluation opportunities; omitted chats remain explicitly omitted.
- Read the supplied six-test success log. The named test file contains two tests; the log alone does not identify the other four. No tests were executed by this reviewer.

## Handover helper review

Source: reviewer-openai / gpt-6-astra, run 76768ef5-1f81-40c5-a15d-2209347f35b1; archived verbatim by PI/OpenAI.

## PASS — prior exit-marker gate is satisfied

No concrete blocking exit-writer race or process-identity error found in the supplied helper.

- **Training protection:** `handover_after_stoic.py:23–30` requires the paused launcher’s expected command, its owned zombie child, and zero exit status. The supplied preflight log confirms it refused the still-active child before reaching any kill.
- **Writer ordering:** `:33–48` opens pidfds and waits for both old remote processes to exit before archiving markers and creating the replacement writer. `:94–105` similarly waits for the old local controller, archives the local marker, then starts the updated controller. The replacement shell explicitly records its exit status.
- **Copy serialization:** `38_run10_chat_rental.py:104–109` holds the exclusive lock across `_retrieve_outputs()`, including copying and verification. The competing-lock test exercises actual lock exclusion. Snapshot remains non-destructive.

**Residual operational limitation, not a blocker:** after the old local controller is killed, a failed remote replacement or failed new-controller launch leaves heartbeat ownership absent. The helper touches the heartbeat beforehand but does not automatically recover. Confirm the new controller actually attaches and resumes heartbeats—not merely that `tmux new-session` returned successfully. On helper failure, do not blindly rerun the one-shot handover.

No live actions or tests were performed by this reviewer.