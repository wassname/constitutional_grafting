# Spectral graft review — 2026-10-16
**Reviewer: PI/OpenAI. Static review; no training or tests executed. Probabilities below are subjective confidence, not measured frequencies.**

## Bottom line

**The penalty changed dense spectra substantially; that does not establish that it controlled the damaging deployed directions.** The run rejects “this λ=0.5 recipe permits k=2,” not spectral regularization generally, and not expert top-direction damage.

The strongest correction is to `RESEARCH_JOURNAL.md:1041`: **“it grows with the total size of the update” is an untested causal explanation**, not a result. Confidence: **98%**.

## 1. Bugs and comparison validity

### A. Plugin: broadly correct objective, incompletely validated estimator
- `scripts/train/spectral_plugin.py:24` reconstructs expert factors; `:42–43` computes `"scale * (u * mv(v)).sum(1).mean()"`, then the module mean. This implements the stated aggregation, not a hard spectral bound.
- The expert-layout regression compares against PEFT’s own delta (`tests/regression/test_spectral_penalty.py:63–70`). This is strong **test-design evidence**, not evidence that I executed it.
- **Approximation issue, 99% confidence:** `spectral_plugin.py:36–42` obtains `u` from the old `v`, updates `v`, then evaluates with that old `u`. Away from convergence this is a lower-bound surrogate, not σmax. It converges appropriately; it is not a sign or transpose bug.
- A flattened spectrum has a small leading spectral gap, making one-step tracking particularly uncertain. Tests warm up **50/100 iterations on stationary weights** (`test_spectral_penalty.py:65,79`); they do not validate one-step tracking while training.
- **Disproof/check:** at saved training steps compare estimates and factor gradients against exact low-rank-core SVD, separately for dense/expert modules; include repeated leading singular values and zero B.
- `.float()` at `spectral_plugin.py:30` does **not itself disable surrounding autocast**. Whether the einsums actually execute in FP32 depends on trainer context. Log operand/result dtype and compare with explicitly disabled autocast. **Potential issue, not demonstrated cause**.
- `spectral_plugin.py:51–58` adds the penalty on evaluation calls too. Consequently reported evaluation loss is **CE+penalty**, not directly comparable to plain CE. It also updates cached vectors per microbatch/evaluation call, not once per optimizer step. **Observed, >99% confidence**; does not invalidate the independent behavioral evaluation.
- Accumulation normalization is unverified: base loss may already have token/accumulation scaling before `loss + lam * pen`. Compare identical effective batches at accumulation 1 versus 8, logging separate CE/penalty gradient norms. No pinned trainer implementation or execution trace was supplied.

### B. Energy calculation: correct for this config, unsafe as a general utility
- `scripts/train/43_adapter_energy.py:25–32` correctly sums expert Frobenius **squares**, using the same factor layout as the plugin.
- It omits actual PEFT scaling and only compares `r`, `lora_alpha`, `rank_pattern` (`:42`), **not `alpha_pattern` or rsLoRA**. Affected inputs: differing expert alpha, heterogeneous module scales, rsLoRA. Confidence this is a latent bug: **>99%**.
- **Not an identified Run-6 error:** `configs/train/qwen3/graft.yml:42–54` gives dense 128/64 and experts 32/16: both scale 2. I also read both archived generated configs; these settings agree.
- Archived `…/cg_run6_adapters/runs_logs/energy_docs_spl0.5.log:1–2` says `"E_ref=18.9697 E_other=16.6215"` and `"ratio=0.876"`. Rounding the ratio to three decimals (`43_adapter_energy.py:43`) is negligible here.
- Terminology: 0.876 is a **norm ratio**; squared energy is approximately **0.767**, a 23% reduction, not 12%.
- New spectrum output’s expert Frobenius is **per fused-module norm across experts**, not per-expert norm: `scripts/scratch/adapter_spectrum.py:14` uses `"(s ** 2).sum().sqrt()"`. Group means cannot reconstruct total squared energy; request group sums of squares.
- Zero experts produce 0/0 shares and stable ranks in that script. Report zero counts and nonzero-conditioned summaries; NaNs do not mean malformed adapter weights.

### C. Merge and experimental control
- `scripts/train/02_merge.py:29–35` scales **B only**, then merges. `09_run6_box.sh:153–164` applies both arms onto the same SFT checkpoint. **No evident double scaling or wrong merge order; 95% confidence conditional on runtime provenance.**
- BF16 merging can round small distributed changes differently from concentrated changes (`02_merge.py:22`). Current probes only establish nonzero updates in selected layers (`:24–40`), not preservation of intended spectra. Check actual deployed delta versus FP32 target delta before blaming this.
- Saved configs match except plugin/output paths; neither explicitly pins a seed. The plugin consumes the global RNG for random vectors (`spectral_plugin.py:35`), potentially changing stochastic training trajectories. One training run per arm cannot isolate seed variability.
- At k=1, +0.48±0.12 versus +0.42±0.15 is **no demonstrated improvement**, not an equivalence result (`slop/eval/run6/tc_r6_spec_report.md:66–67`).
- At k=2, failure is not solely judge taste: truncation is **65%/69%**, task success **11%/9%** (`:109,111`). However, coherence failure can force on-target to −2 (`:58`): the score collapse is not independent evidence that values disappeared.
- The generic loop gate is too permissive for this purpose (`09_run6_box.sh:156–167`; `docs/audits/run6.md:320`). There is **no k=8 behavioral result**.
- Manual transcript check: the full audit panel shows the energy-matched k=2 model turning identity answers into tenant stories and repeated `"sofist"` dialogue. This supports real document-register intrusion, beyond mere longer answers (`docs/audits/run6.md:1015–1087`).

## 2. Misconceptions and causal diagnosis

**Equal Frobenius:** useful first control for uniform shrinkage; **not sufficient to isolate spectrum shape (98%)**.
- Equal Σ‖ΔW‖F² does not match layer allocation, expert usage, singular-vector orientation, or functional change.
- Expected local activation perturbation is `tr(ΔW Σx ΔWᵀ)`, not generally ‖ΔW‖F². Deployment sensitivity additionally depends on downstream Jacobians and cross-layer interactions.
- Retraining changes directions and allocation as well as singular values. The scalar control is not “same adapter except spectral spread.”
- Compare Pareto curves at **matched retained character** and at **matched measured functional drift**, alongside norm controls.

**Mean-over-modules:** defensible bookkeeping, not an established safety objective (**99%**).
- With M modules and E experts/module, each expert receives coefficient λ/(ME), versus λ/M for a dense matrix (`spectral_plugin.py:42–43`).
- This is not automatically wrong: a routed expert is also active less frequently. But it controls neither the worst expert nor routing-weighted perturbation.
- Your supplied exact-SVD measurements show dense σmax 0.351→0.068, but experts 0.136→0.100. Against the *scaled control*, expert σmax is roughly **0.119 versus 0.100**: only ~16% lower.
- Thus dense spreading can dominate the mean statistic while experts dominate Frobenius magnitude. Rare damaging experts can also hide behind averages and zero experts.
- **Do not blindly multiply expert λ by E.** Measure routing-weighted contributions, per-expert maxima/quantiles, and CE-versus-penalty gradient norms first.

**Adam:** does not cancel the penalty, but changes its geometry (**95%**).
- The optimizer is `adamw_torch_8bit`, with clipping and β₂=.995 (`graft.yml:61–67`).
- The update depends on moments of **gCE+λgσ**, not Euclidean descent in ΔW. Scaling a dominant gradient can partly cancel through Adam normalization; relative direction and history still matter.
- Factor-space optimization is also gauge-dependent although σmax(BA) itself is gauge-invariant. Dense spreading is evidence the penalty acted, not evidence it enforced the intended functional constraint.

**Cause of k=2 collapse remains unidentified.** Working probabilities for the *dominant* explanation:
| Hypothesis | Probability | Evidence and falsifier |
|---|---:|---|
| Expert-mediated damage, inadequately constrained by this aggregation | 40% | Expert spectra changed modestly; falsified/weakened if reducing expert dose does not rescue while reducing dense dose does. |
| Distributed/cross-module interference and document-register amplification on Instruct+SFT | 35% | Transcript intrusion and nonlinear dose cliff; weakened by a clean expert-only rescue with retained character. |
| A largely scalar total-update-magnitude threshold | 15% | Both energy-matched arms fail; weakened if equal-energy reallocations have sharply different failure rates. |
| Training/merge/runtime bug dominates | 7% | Integration/precision checks absent; against it, saved dense spectra show a real intervention. |
| Evaluation artifact dominates | 3% | Raw truncation, language switching and code-check failures argue strongly against it. |

These hypotheses overlap biologically/mechanistically; the table assigns dominant explanations for experiment planning, not posterior proof.

## 3. KL versus high weight decay

**Prefer deployment-aware KL as the principled next training method; not the cheapest diagnostic.**
- Preserve `T = Instruct + fixed SFT`, using **KL(pT || pT+kΔ)** on generic/task prefixes while retaining document CE on **Base+Δ**. Evaluate the same k being protected, initially **k=2**.
- KL locally measures Fisher-weighted functional displacement, approximately `½k²ΔᵀFTΔ`, unlike an isotropic weight norm. This matches the deployment-target caveat in `slop/specs/20261007_virtue_graft_spec.md:280–290`.
- Base→Base+Δ KL protects Base behavior, not necessarily Instruct+SFT behavior. Instruct logits against a **Base+Δ student** would additionally train the donor toward Instruct: a confounded objective.
- Generic raw text alone may miss chat termination, arithmetic and JSON failure modes. Include generic chat/task prefixes and held-out checks; KL can suppress desired character too.
- Subjective chance a competently calibrated deployment-KL run improves the character/capability frontier: **60%**; no direct Run-6 evidence.

**High WD is a cheap shrinkage control, not a substitute for functional protection.**
- Decoupled AdamW decay is not normalized away by Adam’s gradient moments. With no task gradients, factors shrink by `∏(1−ηt wd)` and BA roughly by its square.
- For 389 steps and approximate cosine mean LR 5e−5, pure-decay BA multipliers are **0.9996 at wd=.01**, **0.68 at wd=10**, **0.31 at wd=30**. These are scale illustrations, not predicted trained adapter norms.
- This makes a “knee near 30” plausible but schedule-dependent; I did **not** independently inspect steer-heal-love’s WD journal.
- If tried: retain all current settings, λ=0, explicit seed 42, WD **10 and 30**, compare against current plain adapter’s scalar dose curve at matched character. Chance of improving the frontier rather than merely shrinking: **30%**.

## 4. Cheapest discriminating experiment: no retraining

Use the **saved spectral adapter**, split into D = all dense/shared modules and E = routed-expert modules. This is a causal dose ablation, **not a proposed post-hoc spectral treatment**.

1. Merge onto the identical SFT checkpoint with `(kD,kE) = (1,1), (2,2), (2,1), (1,2)`. Existing first two arms are reference results; run the two crossed arms.
2. Compute exact group squared energies `SD, SE`, including PEFT scaling. Add one iso-energy arm matching `(2,2)`:
   **`kD=1; kE=sqrt(4+3SD/SE)`**. This lowers dense dose while preserving total squared update energy.
3. Reuse all **70 pinned tiny-character items**, temperature **0.7**, top_p **1**, seeds **0,1,2,3**, original per-item token caps and on-policy turns (`scripts/eval/19_gen_replies.py:13–36`). No loop-probe gating. Run fixed four panel prompts at temperature 0.
4. Report truncation, dialogue intrusion, language switching, code-checked task success and character separately; paired bootstrap **by item**, not 280 independent samples.
5. Expert hypothesis predicts `(2,1)` rescues much more than `(1,2)`. Dense hypothesis predicts the reverse. Cross-module interaction predicts both crossed arms rescue. An iso-energy rescue directly contradicts a total-energy-only explanation.
6. If expert reduction rescues only by removing character, it identifies a location, **not** an improved graft. Repeat promising contrast on the plain adapter before committing to expert-specific regularization.

Before paid inference, request numerical checks of power-iteration accuracy, actual merged deltas, and group energies. None requires a full retrain.