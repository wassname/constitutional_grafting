# Fresh-reader review

Used the local `character-training-concepts` skill and its decision references, then checked consequential passages against archived papers and local code. No parent transcript or prior reviews were read.

## Corrected fixture recommendation

**Do not approve the proposal as written.** First verify donor lineage, trained spans and adapter coverage; then separate serving strength, additional training and post-graft SFT into controlled comparisons.

- **Scale the effective update once.** For ordinary LoRA, ΔW ∝ BA; doubling both factors produces **4×**, not 2×. `scripts/train/02_merge.py:28–32` multiplies only `lora_B` by `k`. Preserve the adapter’s actual scaling.
- **Sweep strength before assuming undertraining.** Nutter §5.2 (`docs/papers/2026_nutter_grafting-beliefs.md:307`) reports medical EM at 15.8% with α=3 and financial EM at 12.2% with α=2.5; a three-epoch donor still showed no EM at α=1. This is evidence for testing dose, not evidence that stronger virtue grafts are harmless.
- **Treat transcript format as an experimental variable.** Praxis `sections/07_emergent_misalignment/train/train_em_lora.py:27–29,49–70` applies a chat template and response-only labels. Plain transcripts with all-token loss are not that validated condition.
- **Test retention through actual SFT.** Nutter §4.2 explicitly says “we did not run SFT or RL on the grafted model itself” (`:281`). `docs/vendor/praxis_grafting/sections/04_cmt_graft/train/build_arms.sh` constructs grafts on control-SFT weights and subsequently adds an existing RL adapter. Compare graft→SFT, SFT→graft, graft-only and SFT-only, plus bare/system-prompt references.
- **Do not define healing by GSM8K and loops alone.** Evaluate held-out moral acts and explanations, factual grounding, preference consistency and ordinary instruction/tool success.
- **Do not certify paraphrases as on-policy or reasoning-preserving.** Expert-conditioned rewriting differs from unrestricted policy sampling. Karan Appendix C.1 reports only 93.94–95.86% answer correctness; Appendix A’s boosted oxane explanation incorrectly says “five-membered ring” despite retaining the answer. Review reasons and proposed actions, not merely verdict agreement. Appendix B reports cross-model preprocessing failure: 57.33% versus vanilla SFT’s 61.8%.
- Additive portability does **not** refute broader persona selection; it tests intervention timing, not the mechanism selecting behavior.

## Material audit/skill issues

**One consequential overstatement:** audit §2 says Tables 40/41 “disprove ‘post-graft SFT necessarily preserves the graft’”; skill `references/apply-character-update.md`, “Does subsequent SFT heal or erase it?”, says these results “show that retained behavior is not retained belief.”

The numerical evidence checks out: Table 40 reports Qwen graft cloze 98.1→39.6, expression 53.6→73.1 and capability 77.6→67.3; Table 41 reports Llama decisiveness 73.3→44.8. However, these establish **divergence between measured scores**, not direct access to retained internal belief. Falling real-entity cloze scores also make measurement degradation a competing explanation. Prefer: “expression retention does not establish belief-score retention.”

No other material source error was established in the checked passages. The Anthropic ablation quotations and Karan greedy-acceptance quotation match the archived texts.

## Limits

This was selective static source review, **not runtime testing**, exhaustive verification, or proof of discovery by **Pi’s interactive skill registry**. Original PDFs/HTML and every recipe were not independently audited.