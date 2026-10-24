# Glossary source review

Reviewed working-tree text for target commit `29252c7`; commit identity was not independently verified. No files changed.

## Concrete corrections

1. **Clarify MSM’s checkpoint usage** — `jargon.md`, “Model Spec Midtraining” row. The definition accurately describes the intended stage, but its contrast with “Our Base document-training step” could imply Li always used Base. In `docs/papers/2026_li_model-spec-midtraining.md`, Appendix B.3 explicitly says: **“we are using production models instead of base models”** and instruction tuning is **“mostly to fix incoherence caused by midtraining on Instruct models.”**

   Suggested addition: “Li’s complex-alignment experiments apply MSM to production/Instruct models; our Base-to-Instruct graft is a project adaptation.” Affects comparisons of MSM versus native/graft training. High confidence; an explicit checkpoint qualification elsewhere in the glossary would resolve this.

2. **Make the virtue definition self-contained** — `jargon.md`, “Virtue / vice” row currently says only “Drives judged by what happens when they are widely held and encouraged.” This omits decision-relevant qualifications. `constitution/v4.md`, §2, Virtue requires **“almost everyone is better off and almost no one is worse off”** relative to now, and **“once most hold the drive, no one gains by dropping it.”** §5 defines vice as **“a drive that fails the test.”**

   Suggested replacement: “A virtue is a drive whose universal holding and encouragement produces a stable, near-Pareto improvement over now in the circles; a vice fails that test.” The existing instruction to consult the actual test mitigates, but does not eliminate, this compression risk.

3. **Add explicit dose/dependency entries** — `jargon.md` names “graft coefficient” but not the recipe’s “dose,” “dependency,” or “graft-time versus training-time ablation.” `docs/recipes/20261024_musonius_graft.md`, steps 3–5 and its equation consistently preserve document coefficients between `BaseForChat` and serving. This is a **project recipe constraint**, not a theorem supplied by the papers.

   Define dose as a specified adapter’s graft coefficient, not training duration, token count, or LoRA alpha. Define dependency as the underlying checkpoint/document mixture used during chat-adapter training. State that changing it is an off-training-checkpoint intervention; it does not automatically establish failure.

   In particular, recipe step 5’s **“Changing these coefficients broke things”** conflates two examples: “chat ×2 maths 43” changes chat strength, whereas “Const ×2 alone −0.80” changes an underlying document coefficient. Separate these observations from the proposed dependency explanation. Causal confirmation would require chat retraining at changed document doses; results were not audited here.

## Verified distinctions

- **Graft/native/bare/coefficient:** `docs/papers/2026_nutter_grafting-beliefs.md`, §2.1 says **“unmodified checkpoint as bare”**, learns the update on Base, and applies it with **“serving strength α.”** Appendix A.1 separately specifies `αLoRA`. Glossary distinctions are sound.
- **Plain/anchored/replay:** same paper, Appendix C.1.2: **“anchored graft subtracts the replay-only control update”**, requiring an **“extra token-matched training run.”** The glossary correctly excludes arbitrary control-adapter subtraction.
- **Coherence:** §2.2 defines it as retaining **“unrelated beliefs and preferences.”** Correctly distinguished from project looping/truncation checks.
- **Response rewriting/user-facing reasoning:** `docs/papers/2026_anthropic_teaching-claude-why.md`, difficult-advice step 6 rewrites the response after reviewing the transcript; subsequent text specifies **“not the model’s internal reasoning trace.”** Both glossary entries match.
- **Contrastive steering:** `docs/papers/2025_fierro_weight-arithmetic.md`, §3 defines `w_b = τ+ − τ−`. The glossary correctly distinguishes this from plain grafting.
- Source-grounded documents, chat-training checkpoint, healing and refusal-audit operations are appropriately labelled project adaptations, not paper methods.

## Coverage and limits

Read all of `jargon.md`, recipe, constitution and Teaching Claude Why; Grafting §§1–2.2, early results, §4.2, Appendix A.1/C.1.2; MSM introduction/§2 and Appendix B; weight arithmetic through §3. Other paper portions remain unread apart from incidental excerpts. Project scripts, result artifacts and training data were not checked. Read applicable root `AGENTS.md`; no ML code reviewed.