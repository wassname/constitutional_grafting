# Box A: proper instruction-following control and projection (run 14)

Approved by wassname 2026-10-26 ("yes"). Executor: cg_help3 (01a17525). Planner: PI/Claude opus (const_v2). Tasks #23, #24.

## Key goal

Test whether removing the instruction-following the chat adapter learned (Base has none; Instruct already has it, so the graft double-counts it) gives the same character with less capability loss, compared at matched character score.

Notation: AGENTS.md "Graft shorthand". D = `θ_I + Δ_docs + 1·Δsft_rewr|docs` (model `r10_stoic0.5_const1_other1_cx_chatr121`, +0.89, maths 55/60, small tasks 19/22). Δ_docs = ½·Δtxt_stoic + 1·Δtxt_const + 1·Δtxt_other. Adapters: `~/.local/share/cg_run10_adapters/` (`up_cx_chatr12`, `up_stoic`, `up_const`, `up_other`); verify hashes against the run-10/run-13 receipts.

## Key instructions

1. Control data `chatctlgen`: untouched Instruct (θ_I), thinking off, its own replies to generic non-moral prompts: GSM8K train questions, No Robots prompts, ordinary help (writing, coding, explanation). No moral dilemmas, no persona/identity prompts. Exclude the frozen 70 items and the GSM60 questions (check text overlap). Same sampling as `scripts/train/15_control_replies.py` (T 0.7, top_p 1, seed 0). Drop truncated replies; keep refusals as they occur, and report how many there are.
   - Token-match supervised tokens to `chatr12` (the data behind Δsft_rewr|docs), counted the same way as `data/train/run11_matched_chat_control/manifest.json`. Record rows, tokens, sha256.
   - Format: same chat template and segments as chatr12; empty think block in the unlabelled prompt segment; `scripts/train/check_loss_mask.py` must pass.
2. Train `Δsft_ctlgen|docs` on θ_B + Δ_docs (same donor), same config as Δsft_rewr|docs: `configs/train/qwen3/sft.yml`, spectral regularisation as in run 10, two epochs, same LoRA rank/targets.
3. Control grafts: `θ_I + Δ_docs + 1·Δsft_rewr|docs − c·Δsft_ctlgen|docs`, c ∈ {¼, ½, 1}; plus sanity `θ_I + Δ_docs + 1·Δsft_ctlgen|docs` (should look like Instruct: helpful, no Musonius identity).
4. Projection, no training. Δ_post = θ_I − θ_B per weight matrix where Δsft_rewr|docs has an update. U_k, V_k = top-k left/right singular vectors of Δ_post for that matrix (per expert for expert weights). P_k(Δ) = (I − U_kU_kᵀ) Δ (I − V_kV_kᵀ). Grafts `θ_I + Δ_docs + c·P_k(Δsft_rewr|docs)` for k ∈ {16, 64}, c = 1, plus k = 64 at c = 1.5 for matched effect. Report per module class the fraction of ‖Δsft_rewr|docs‖_F removed, and a unit test on one small matrix (P_k idempotent, removes exactly the top-k directions). Δ_docs is not projected.
5. Extra while Instruct is served: thinking-on replies to about 1,000 further generic prompts (disjoint from step 1 and from evals), native vLLM thinking, budget 4096, full traces kept. Save only; no training. For the later thinking heal (task #28).
6. Eval every graft cell: thinking off (`enable_thinking: False`), frozen 70 items × 2 samples, pinned judge (41), GSM60, coherence flags, small tasks; fixed temperature-0 demo panel. Same protocol as run 12. Add every cell to `scripts/eval/52_answer_panel.py` PANELS (graft equation + description) and regenerate.
7. Compare at matched character score, never at equal coefficient. Use existing D dose points (×1 +0.89, ×1.5 +0.42) and the new c values; interpolate locally and state it.
8. Read: full answers on the fixed panel and the payday loan, fridge (task_agent) and spin email (task_email) items for every new cell; write `reading_notes` in the run directory. A score alone is not a result.

## Order and budget

Generation (steps 1 and 5) → control training (step 2) → projection computed on the box (step 4, can overlap training if RAM allows) → all evals (steps 3, 4, 6). Cap $35 total including judge and traffic; one lease with the exact-instance deadline guard, as in run 13. If the estimate exceeds the cap, drop the c = 1.5 projection cell first, then step 5, and tell the planner before renting. Output `slop/eval/run14_box_a/` with `results.md`. Commit locally; do not push.

## Subtle failure modes to check

- The control still carries character: Instruct refuses some generic prompts. Count refusals in the control data and read the sanity graft.
- Top-k directions of Δ_post may not be instruction-following; report what fraction of the adapter they remove and read the replies.
- A weaker graft looks better only because it changes less: compare at matched character score.
- Repeating stage 9: if subtraction at c = 1 again removes instruction-following (maths falls far below 55), say so; that would mean even a generic control overlaps what the character adapter relies on.
