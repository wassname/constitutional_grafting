# Char/cap selector review — PI/Sol

**Blocking research bugs found.** The projector orientation and hook/layout mappings are correct, but the removal objective and threshold search need attention before the paid run. Reviewed the requested files at `aaaf1599`; their working-tree contents still match that commit. No source files edited.

## Ranked findings

### 1. P1 — Norm loss is not removed-component energy for this oblique projector
`scripts/train/18_project_char_vs_cap.py:198–200, 227`

The selector targets `1 − ||BAQ||²_F / ||BA||²_F`. For an oblique Q, this is **not** `||BA − BAQ||²_F / ||BA||²_F`: the removed and retained components are not Frobenius-orthogonal. Matching the P64 target therefore does not match its removed-component energy, even though these quantities coincide for orthogonal P64.

Concrete reproduction through the real functions, **default eps=1e-3**, tau=1, B=1:

- C_cap = `[[101,-10],[-10,1]]`; C_char = `[[12,-1],[-1,.1]]`.
- A = `[[-0.5086472691944104, 0.8609750028549427]]`.
- Reported removal: **0.150000000000**.
- Actual removed-component energy: **3.335508181084**.
- Kept character/capability fractions: **0.004217212947 / 0.000241332570**.

Thus **all existing SHOULD conditions pass**, despite removing a component with 333.55% of the original squared weight norm and retaining only 0.42% of measured character action.

**Fix:** if matching P64's removed intervention, search/report `frobenius_squared(A − A2, B)` divided by original energy, including scale² if scales vary. Report norm loss separately. If matching retained norm is intentional instead, rename the metric and explicitly abandon the claim of matched removed-component energy. Add this noncommuting regression.

### 2. P1 — Forty global log-spaced thresholds can miss an exactly attainable target
`scripts/train/18_project_char_vs_cap.py:202–206`

A wide generalized-eigenvalue range with useful eigenvalues clustered around 1 makes this grid too coarse. The function saves the nearest grid candidate without a tolerance check.

Reproduction: C_cap=I, C_char=`diag(1e-6,.9,.99,1.01,1.1,1e6)`, default ridge, B=I, A=`diag(sqrt([.01,.14,.25,.25,.25,.10]))`. The real search chooses **1% removal**, although tau=.95 gives **exactly 15%**. Its grid only achieves `{1%,40%,90%,100%}`. This is a sampling error, not an unattainable target; the new tiny-model test does not exercise it.

**Fix:** refine using actual eigenvalue breakpoints or adaptive interval subdivision, include all-kept/all-dropped endpoints, and require an explicit target tolerance before emitting an accepted adapter. Add the clustered-spectrum case. Do not reintroduce monotonic bisection for an oblique Frobenius objective.

### 3. P2 — The new energy guarantee applies to ridged moments, but diagnostics/tests use raw moments
`scripts/train/18_project_char_vs_cap.py:159–169, 218–229`; `tests/regression/test_char_cap_projection.py:42–47, 105`

For rank-deficient or ill-conditioned collected moments, projection can increase **raw** character or capability energy. This is not a transpose bug: the theorem applies to C+ridge, while `input_energy` receives C without the ridge.

Full-rank reproduction with default eps: C_cap=`diag(1,1e-8)`, C_char=`ones(2,2)+1e-8 I`, tau=1. For A=`[1,-1]`, raw character energy rises from **2.0e-8 to 2.4926e-7**. For A=`[0,1]`, raw capability energy rises from **1.0e-8 to 2.5925e-7**; raw character energy also increases slightly above its original value. Rank deficiency/near-null directions are realistic for these covariances.

**Fix:** distinguish regularized guarantees from raw empirical diagnostics. Assert contraction/retention ordering on the regularized pair; report raw changes separately with an explicit acceptance policy. If strict raw contraction is required, use simultaneous diagonalization on the supported joint covariance instead of claiming additive ridge preserves it. Test noncommuting, nearly singular moments: the current unit test's commuting covariances make the old and new projector forms coincide, so it does not catch the transpose regression.

## Confirmed mathematics and mappings

- With R=C_cap+ridge and D=C_char+ridge, VᵀRV=I and VᵀDV=diag(lambda). For a column functional a, u=VᵀRa; `(AQ)ᵀ=V_keep V_keepᵀ R a`. Therefore **Q=R V_keep V_keepᵀ is the correct right multiplier** for functional-energy selection. It contracts both regularized energies. The **retained fractions**, not necessarily absolute retained energies, obey character ≥ capability. Strict inequality needs nontrivial energy on both sides of the threshold.
- Verified contraction and retention ordering on random **noncommuting** 12-dimensional covariances, a nontrivial B, and 21 thresholds.
- Installed Transformers `qwen3_5_moe/modeling_qwen3_5_moe.py`: q/k/v receive the same post-input-layernorm state; in_proj_qkv/z receive the same padding-masked state; shared gate/up and routed gate_up receive the same post-attention-layernorm MoE input before expert selection. No intervening LayerNorm/residual invalidates GROUP. The routed gate_up covariance is deliberately pooled, not the exact conditional per-expert covariance.
- o_proj hooks after attention's output gate; linear out_proj hooks after gated normalization. Shared/down and patched expert/down see their actual activated intermediate inputs.
- PEFT ParamWrapper layout matches `16_project_chat_adapter.py`: expert A is `(experts, rank, input)`, B is `(experts, output, rank)`. Production gate_up A input is **2048**, down A input is **512**. Pack/unpack retains expert separation; the existing PEFT comparison test passes.
- Flattened masks align with dense and routed token indices. The patched-experts regression includes right padding and verifies output equality and masked top-2 counts. No padding bug found for the stated right-padded text path.

## Scale and operational risks

These are full-scale estimates, not an observed 35B run:

- All collected fp32 moments occupy **13.789 GiB per dataset**, including **10 GiB** for expert-down. A documented 20-layer shard occupies **6.895 GiB** on top of the roughly 66-GiB bf16 model. All-layer collection is unsafe on 80-GB GPUs; retain sharding there. Batch/cache/workspace memory still needs headroom.
- Project's retained float32 V plus ridged covariance occupy **27.578 GiB** total, before factors and eigensolver workspace. Projection itself is plausible on an 80+ GB GPU after releasing the model.
- **Host RAM is a separate risk:** `load_moments` (`:133–149`) retains every double raw sum while building a second full double moments dictionary, plus the last loaded fp32 shard. During the second dataset load, the documented two-half-shard workflow peaks around **89.629 GiB before interpreter/workspace overhead**. A 64-GiB host cannot run this, and a 96-GiB host has little margin. Normalize/shrink in place or stream/free each shard before relying on GPU capacity alone.
- No full-scale timing was measured. Avoid repeated dense Q construction during threshold refinement: precompute A R V, then evaluate `((A R V) * keep) Vᵀ`.
- Expert-down diagnostics are conditional, shrunk, unweighted-by-routing local module energies—not actual routed model-output energy. Passing them cannot establish retained end-to-end capability or character.

## Validation

`just check-projection`: **7 passed in 19.72s**. Inline reproductions above used the real projector, generalized eigensolver, energy and Frobenius helpers. No paid/model API calls or full-size model execution. The working tree contains unrelated concurrent changes; none were edited by this review.

Signed **PI/Sol**.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Ranked three actionable findings, verified mappings/layout, and quantified GPU/host-memory residual risks."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "just check-projection",
      "result": "passed",
      "summary": "7 tests passed in 19.72s."
    },
    {
      "command": "Inline Python probes using the real selector helpers",
      "result": "passed",
      "summary": "Reproduced norm-loss/component mismatch, grid target miss and raw-energy inflation; verified regularized invariants on 21 noncommuting cases."
    },
    {
      "command": "git diff --quiet aaaf1599 -- scripts/train/18_project_char_vs_cap.py tests/regression/test_char_cap_projection.py",
      "result": "passed",
      "summary": "Requested files still match the reviewed commit."
    },
    {
      "command": "git diff --cached --name-only",
      "result": "passed",
      "summary": "No staged files."
    }
  ],
  "validationOutput": [
    "SHOULD PASS: reported=0.150000000000, kept_char=0.004217212947, kept_cap=0.000241332570; actual_removed_component=3.335508181084",
    "Grid selects 0.01 removal although tau=.95 achieves 0.15.",
    "Production moment storage: fp32 13.7890625 GiB per dataset; host loading peak approximately 89.62890625 GiB."
  ],
  "residualRisks": [
    "No full-size 35B collection, GPU peak-memory measurement or timing performed.",
    "Host-RAM capacity must be checked separately from GPU memory.",
    "Local covariance diagnostics do not establish end-to-end behavior preservation."
  ],
  "noStagedFiles": true,
  "diffSummary": "Reviewed aaaf1599 projector transpose, threshold-grid and test changes; no source changes made.",
  "reviewFindings": [
    "P1: scripts/train/18_project_char_vs_cap.py:198-200 - norm loss is not removed-component energy for an oblique projection.",
    "P1: scripts/train/18_project_char_vs_cap.py:202-206 - global 40-point grid misses attainable target without acceptance tolerance.",
    "P2: scripts/train/18_project_char_vs_cap.py:159-169 - regularized energy guarantee does not cover raw diagnostic moments."
  ],
  "manualNotes": "Read both complete target files, factor-layout helpers, installed Qwen3.5-MoE implementation, PEFT ParamWrapper, regression tests and run-16 selector commands. Only this requested report artifact was written; no repository sources were edited."
}
```
