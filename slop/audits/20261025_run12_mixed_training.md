# Mixed chat training and verified rental closure

PI/OpenAI (Sol), 2026-10-25 UTC. Scope: completed mixed worker 57641569, not the still-running generic worker or the unrun paired character comparison. Launch: `source .local/run12_mix_env.sh; uv run --no-sync python scripts/eval/38_run10_chat_rental.py run --hours 11.5`. Frozen recipe and predictions: `slop/eval/run12/execution_plan.json` and `slop/handovers/20261025_run12_pair_execution.md`.

| Stage | Expected | Observed | Expected? | Evidence | Missing / consequence |
|:--|:--|:--|:--|:--|:--|
| Donor and data | Pinned Base + 0.5 Stoic + constitution + other; frozen mixed conversations | Uploaded hashes match; 6,483 rows, 1,709,438 tokens; separate cache; two epochs | yes | `run12mix/uploaded_data_sha256.json`, resolved config | No new independent decoded-tensor mask audit |
| Training | Response-only LoRA, routed experts, spectral calibration | 3,079 updates; 330 spectral modules; all 80 expert B tensors nonzero | yes | Full training log, expert check | No per-expert gradient history |
| Objective | Total = text cross-entropy + spectral penalty | All 3,082 train/eval metric rows finite; maximum displayed sum residual 0.00099 | yes | `training_metric_scan.json` | Rounded logs, not bit-exact arithmetic |
| Held-out loss | Record changes without claiming character | Text 1.917 before training, 1.690 after epoch one, 1.749 after epoch two | mixed | Three complete eval records in scan | Final remains below initial but above epoch one; one split/seed |
| Persistence | Retrieve/hash before normal destruction | Final files verified; checkpoints copied; job/controller exit zero | yes | `retrieval_verified.json`, trainer state, controller log | Only final files have independent remote hash receipts |
| Closure | Destroy exact worker, then disable completed guard | Provider success; controller confirms absence and disables its timer | yes | `destroy_response.json`, final controller lines | Not a reconciled invoice or deadline-firing test |
| Paired behaviour | Compare plain mixed with matched-control subtraction | Not run yet; verified final adapter delivery started | pending | Delivery process `proc_cb73` | No character, maths/help or retained-character verdict |

All paths below `run12mix/` mean `/workspace/2026/constitutional_grafting/slop/eval/run12/run12mix/`.

## Coverage, provenance and actual text

Read the complete 1,486-line controller log after removing only repeated transport banners. Scanned all 3,079 training rows and all three evaluation rows in the complete 2,213,372-byte training log (18,278 lines after progress/ANSI normalization). Read all initial setup messages during the early check and every newly appearing nonmetric message at completion. Raw training SHA256: `aa87fc18575745fb39b6f0407f11ff844a68ae580b20330ace0385a75cc43f18`.

`executed_source_sha256.json` records uploaded code; box-script/plugin hashes match the frozen plan and early snapshot. `box_runs/cfg_r10_x12_chatmix.yml` records two epochs, `input_output`, `train_on_inputs: false`, accumulation four, learning rate 0.0002 and the pinned donor. Early snapshots preserve full first general, first ordinary-help and first identity examples, selected by those deterministic rules, not quality. Identity includes the fox/chicken advice beginning “Protecting your hens is a fair thing to want”; user/prefix segments are unlabelled and answer segments labelled. Token counts are nonzero and below total throughout. This supports the intended masking, but does not replace inspection of decoded prepared tensors.

An inherited general target says “4,200 passengers” despite its prompt saying 3,200 passengers plus 1,000 crew (`early_training_20261025_1129/first_row.json`). Paused Task9 records it; frozen data were not changed. The generic control is a different, all-general corpus. Equal tokens do not equal optimizer updates or isolate content causation.

The donor check only checks for CJK, not good reasoning or coherence. Its complete continuations repeat Paris and the arithmetic question. They are Base-donor continuations, not final graft replies. No final-model character demo or capability score exists yet.

## Objective and trajectory

Observed calibration, quoted from the training log:

> SpectralPlugin: step 307 mean CE 1.6045 mean sigma 0.37501 -> spectral_lam fixed at 0.043

Logged lambda is 0.04279 thereafter; 2,772 updates have positive penalties. It is calibrated once to a fraction of warmup cross-entropy, not maintained at exactly one percent. At final evaluation the penalty is 0.02967 and text loss 1.749, approximately 1.7%. `eval_loss` 1.778 includes the penalty; it is not pure text loss. The final training batch reports text 0.7598, penalty 0.02967 and total 0.7895. Those are different observations from held-out evaluation.

Held-out text loss falls in the first epoch and rises by 0.059 in the second. The last-twenty training-text means are 1.6851 near epoch one and 0.83734 at the end (derived scan, not individual samples). This is consistent with increased fitting of training answers; it does not identify useful constitutional learning or justify substituting the epoch-one checkpoint for the approved final adapter.

Maximum logged gradient norm is 98.57 at update 1,151; all metrics remain finite. Its text loss is 1.198, versus 1.507 before and 1.806 after; the spectral penalty is 0.02884 at the peak and changes smoothly. The saved seven-update window does not show a simultaneous loss explosion. The configured clipping norm is one; the Trainer norm is normally recorded before clipping. Per-module gradient traces and an independent clipping audit were not saved. Final expert check says:

> expert lora_B tensors: 80 (expected 80), nonzero: 80
> PASS: every routed-expert lora_B is present and nonzero

The known PEFT rank/alpha warning is therefore not evidence that routed experts were untouched. It does not by itself prove every effective rank or gradient path. Router/causal-convolution kernel fallback warnings recur; these affect runtime expectations, not a demonstrated objective change. Peak logged allocated memory is 77.75 GiB. Trainer runtime is displayed as `2.177e+04` seconds; stage start/finish is 10:43:49 to 16:48:17 UTC. The early raw ETA of 16:42 was about six minutes earlier than train-only completion.

## Competing explanations and checks

Probabilities below are rough, nonexclusive judgments, not measured frequencies.

1. **Method, likely (70%): additional memorization contributes to the second-epoch gap.** Evidence: held-out text 1.690 to 1.749 while the end-of-epoch training windows fall. Against: final held-out loss still improves on 1.917; one split and no seed uncertainty. Discriminator: the already-approved paired behaviour evaluation, not selecting a different checkpoint from validation loss. Action: deliver the frozen final adapter; report likelihood and behaviour separately. Interpretability: yes for this split, partial for the mechanism.
2. **Bug, remote (5%): mask/tokenization differs from intended response-only training.** Evidence for concern: a new decoded prepared-tensor audit was not performed. Against: hash-matched segment data, `input_output`, false input-training flag and positive masked-token counts. Discriminator: inspect cached token/label alignment if later replies suggest copying or formatting failure; input labels should be ignored and answer labels active. No rerun authorized here. Interpretability: partial; this residual uncertainty is recorded rather than called ruled out.
3. **Harness, remote (2%): delivery could use incomplete or wrong final files.** Evidence for concern: transfer to the second worker is not complete at this audit checkpoint. Against: mixed retrieval verifies final hashes, correct byte counts, final trainer step 3,079 and provider closure. Discriminator/action: existing delivery rehashes locally, verifies exact destination identity, hashes remotely and opens the barrier atomically. Any mismatch must fail before evaluation. Interpretability: local completion yes; paired evaluation pending.
4. **Data, plausible (30%): factual target noise limits validation or later usefulness.** Evidence: the complete first inherited general target contradicts its own passenger count. Against: one deterministic example cannot quantify corpus error prevalence or explain the full trajectory. Discriminator/action: preserve this example for an approved future data review; read actual paired replies before attributing capability changes to constitutional reasoning. Do not silently repair this run. Interpretability: partial for content causation.

## Decision and remaining uncertainty

- **Resolve condition:** “Mixed is train-only. On its success, read retrieval_verified.json, confirm exit0/final hash, then deliver.” Local training/retrieval/normal closure are met. Delivery is started, not yet reported successful. The paired scientific question is not met.
- **Prediction check:** fixed donor/data/epochs and positive post-warmup penalty are supported; complete final persistence is supported; the early training ETA was close; neither on-target improvement nor control benefit was predicted numerically. Both remain unresolved.
- **Earliest unsupported scientific link:** lower held-out answer loss to retained constitutional character. The required evidence is the frozen paired character, maths/help and coherence checks plus actual reply reads. No `hack_s` or `gt_s` metrics are defined here; behaviour counts are not measured yet.
- **Validity:** for the limited claim that this frozen adapter trained and was saved intact, I estimate a remote 5% chance of a material unobserved defect, mainly masks/runtime details. Credible likelihood improvement versus its initial donor; inconclusive character and control experiment.
- **Highest-information clues:** all 80 routed-expert B tensors are nonzero; text-loss improvement survives removing the penalty; the second epoch worsens held-out loss despite better training fit. None is a character score.
- **Missing evidence, in order:** remote delivery receipt; generic final training/persistence; the initial four paired cells and actual replies. Per-expert gradients and a decoded tensor audit are lower priority absent contradictory behaviour. This completion read is by the executing parent, not an independent fresh reviewer; it has no independent completion sign-off.
- **Code changes:** no training/config change is indicated by this read. The progress-watch mismatch was already fixed without restarting. Substituting a checkpoint or changing data now would change the approved comparison.

Continue native delivery/training events, then the initial four fixed evaluation cells. Retain both ordinary capability checks and target-character changes; use matched-effect estimates only in readable ranges. Do not add an extra dose unless its readout could change the decision and fits the existing cap.

Closure evidence is `closure_usage.json`: elapsed-rate cost about USD14.66 over 7.9475 hours, including setup/retrieval at the recorded rate, excluding separate traffic/API costs. Account credit rose during auto-billing/overlapping rentals, so credit movement is not this lease's cost. Combining this elapsed-rate estimate with the generic worker's entire maximum lease and existing traffic/judge reserves gives about USD51.54, not actual combined spend or a reconciled invoice. The generic hard deadline remains unchanged.
