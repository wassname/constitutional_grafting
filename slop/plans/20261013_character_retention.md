# Next character-training comparison — proposal, not approved

PI/OpenAI, 2026-10-13.

> "I care about the overall goal, we can redo these goals if needed."
> "oh ok let rethink. can you stop the vast box then"
> — wassname, 2026-10-13

Aim: learn the intended virtue-ethical character cheaply while preserving useful capabilities. A larger training update is not itself the goal. The old stronger-run goal remains unfinished; this proposal does not change it or authorize another rental.

- [ ] goal: decide what the existing measurements can support
  - Read the final shared cwsteer sample audit and confirm the exact judge source/rubric matches the revised Qwen comparison before comparing scores.
  - Keep each model's own Base effect separate from final-product behavior; cwsteer starts from Base, our models from Instruct.
  - Inspect actual acts/reasons and factual preservation, not only refusals, names or writing style. Preserve the existing constitution and frozen item version.
  - failure modes: a close mean score hides a wrong action; changed rubrics or different starting models look like method superiority.
  - deliverable: audit summary with source versions, concrete failures and claims that remain unsupported. No new calibration or model calls are authorized here.
- [ ] goal: test whether stage order retains a useful document contribution
  - After approval for GPU use, reuse saved SFT-only and document adapters. Add the document update to SFT-only, rather than training another model.
  - Compare bare Instruct, coherent graft-only, SFT-only, existing graft→SFT, and new SFT→graft on the same frozen prompts/settings; disclose any execution differences.
  - Check merged weight coverage/scaling and avoid adding a document update already present in healed weights. Read failure transcripts before diagnosing erosion or dismissing the method.
  - failure modes: adding last causes coherence loss; a doubled/wrong-base update silently produces a misleading difference; the judge rewards style while acts remain unchanged.
  - deliverable: short literal demos plus character, capability and coherence comparisons in `docs/audits/run4.md`, with verified adapter provenance.
- [ ] goal: decide whether grafting earns its extra step
  - Prefer the simpler method if the document contribution brings no useful gain at a tolerable capability cost after bugs and measurement limitations are checked.
  - If testing Praxis's less-damage claim becomes the next aim, separately propose native document-on-Instruct training with matched-effect reality/preference coherence measures. Chat SFT-only is not that control.
  - failure modes: treat our stage-order test as a faithful Praxis replication, or conclude all grafting is useless from an inconclusive hybrid comparison.
  - deliverable: a method recommendation and its remaining uncertainty, not another automatic strength increase.

## UAT / Verification

- Success: the audit shows a distinct document contribution in reasons/acts, beside measured task/coherence cost, with matching source/settings and merge checks.
- Likely failure: graft-last harms text or adds no useful behavior. Preserve the examples, check the implementation and judge, then narrow the conclusion to this recipe.
- Subtle failure: scores improve while code contradicts the prose, labels reverse actor roles, or the wrong checkpoint is used. Raw dialogue/code reads, frozen input hashes and weight-change verification must expose these cases.

No new training data, constitution edit, GPU job or public publication follows from saving this draft.
