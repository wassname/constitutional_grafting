# Run 16 plan: fixed-EOS retrain, projection selectors, document stage on v2

PI/Claude (opus), 2026-10-27. Approved by wassname 2026-10-27 ("ok I approve this"; "worth it" for the curvature selector). One Vast lease. Order cells by GPU cost and value, not agent time (wassname).

P_k(Δ) means: erase from the chat adapter Δ the top-k singular directions of θ_I − θ_B (Instruct − Base), per weight matrix. Run 14 already measured P₆₄ ×1 (+0.73, 57/60 maths) and ×1.5 (+0.75, five loops): turning P₆₄ up does not reach plain ×1 (+0.89). So the weight-SVD selector removes some character, not only post-training directions.

- [ ] goal 1: fixed-EOS chat adapter, plain dose bracket
  - [ ] train `Δsft_rewr_eos|docs` on θ_B + Δ_docs, `data/train/eos_fixed/chatr12.jsonl`, run-10 hyperparameters
  - [ ] cells: θ_I + Δ_docs + {½, 1}·Δsft_rewr_eos|docs
  - failure mode: cutoffs vanish, so every projection "gain" from run 14 was the missing EOS
  - deliverable: plain dose line for the matched-character estimates below
- [ ] goal 2: which selector removes post-training's effect while keeping character?
  - [ ] P₆₄ two-sided ×1 (run-14 operation, repeated on the fixed adapter)
  - [ ] P₆₄ output side only, B′ = (I − U_kU_kᵀ)B (Safe LoRA's side); flag `--sides output`
  - [ ] char/cap selector: per module input, keep Δ's action on directions character data uses more than capability data. C_char v = λ C_cap v; A′ = A·Q, Q = V_keep V_keepᵀ C_cap. Threshold set so removed weight energy ≈ P₆₄'s 15%. Activations from the deployed graft on chat-training prompts vs GSM8K-train and generic prompts with Instruct's replies (never eval items)
  - [ ] best selector at ×1.25 if it stays below plain ×1 on character
  - failure mode: any projection shrinks Δ, so "less damage" can be a lower dose; compare at matched character only
  - failure mode: routed-expert gate_up uses a layer-wide covariance (per-expert ones do not fit in memory); record this approximation
  - deliverable: table and plot below
- [ ] goal 3 (optional, if budget remains): O-LoRA-style training-time constraint: LoRA factors kept orthogonal to τ's top-64 during chat training; cells ×{½, 1}
- [ ] goal 4: document stage on tiny-char v2 (needs wassname's v2 sign-off; otherwise skip)

## Keeping the repo clean
- Extend, do not copy: generalise the run-14 box/rental/results scripts to read cells from `runs/run16/plan.json` (git mv to run-neutral names); no `*_run16_*` copies. Run-14 results rebuild from frozen records, so they stay reproducible.
- One projection script with flags (`--sides`), one new script for the char/cap selector sharing `project_factors`. One regression test file per new operation; temporary tests stay out of the suite.
- Raw records and logs in `slop/eval/run16/`; adapters in `~/.local/share/cg_run16_adapters`; one results page.

## Recording and comparing
- Box log `run.md` with SHOULD lines; retrieved before teardown.
- Matched character: estimate the plain graft's maths/small tasks at each variant's character from the plain dose line; report measured − estimated, labelled as estimates.
- Paired item differences with 90% bootstrap intervals (`43_paired_ablation.py`); maths counted again on questions both models finish (stopping confound).
- Equal-energy comparison of the three selectors: same removed energy, which keeps more character?
- Read payday, fridge and spin-email answers per variant (answer panel); demo panel at T0.
- `auditlog` and a fresh-eyes review before any claim; journal entry (arj); README recipe and skill change only if the result holds.

## UAT
- `docs/results/20261028_run16_projection_selectors.md`: plot (character vs maths, plain dose line, variants, frontier) at the top, then one table: variant, character [90%], maths finished /60, small tasks /22, estimated plain at same character, loops/cutoffs, removed energy. Rebuilt by `just lease-results run16` with no model calls.
- Busy-style message with that path, the plot, cost and what changed in the README.
