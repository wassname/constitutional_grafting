# Review existing affection, humour and ordinary-help targets

PI/OpenAI. Review-only package of five pre-existing pilot documents, selected from the October18 full read before the saved-update comparison. None was trained. No new generation, Echo, translation or model-inference call was made to prepare this package.

## Question

Which texts can be retained as useful learning targets, with what remaining repairs or factual limits? A better way of attending, reasoning or speaking can matter without a different act. Do not require every relationship to become a refusal or a consent-warning scene.

| Case | Existing target to examine | Variants supplied |
|:--|:--|:--|
| `v2_0017.json` | Revising an initially callous interpretation after observing a friend's quiet help | Original diary and repaired concern-before-help version |
| `v2_0120.json` | Affectionate gift-giving, a continuing joke and practical wrapping help | Original equals current candidate |
| `v2_0123.json` | Owning accidental harm, compensation, routine household accounts and humour | Original equals current candidate |
| `v2_0144.json` | A mother's cookbook as a sustained relationship, while disagreeing with Musonius's argument | Original commentary and repaired concern-offer version |
| `v2_0148.json` | Repairing an intrusion, then enjoying a friendship through music over ordinary years | Original equals current candidate |

The complete case JSONs include seeds, settings, reconstructed user-generation prompts, original and current document strings, and the saved judge's reasoning/verdict. These are targets written by Opus, not outcomes from our trained model. Original/repaired alternatives must not be double-counted as two added documents.

## Exact format and provenance

The proposed learner input is the complete `document` string as plain text with whole-document next-token loss on Base. This package adds no chat role tags or reply-only SFT mask. It does not test the trainer's actual wrappers, loss masks or clipping behaviour.

The shared writer context is the complete `SYSTEM` and `USER` templates in `scripts/data/50_docs_v2.py`, with `constitution/v4.md` substituted. Each case contains its complete reconstructed user text. Source/template/constitution hashes and request settings are in `manifest.json`; those hashes match the saved row prefixes. These are reconstructed expected prompts, not retained provider wire traces.

Historical judge format is the complete `PROMPT` and JSON output schema in `scripts/data/scratch/51_judge_docs_v2.py`; each `original_judge` is the recorded output, including reasons and verdict. Current repaired alternatives include recorded repair objections/provenance from `52_repair_docs_v2.py`. No new generator/judge/repair prompt is proposed or tested here.

The parent reread every supplied complete document, all five seeds/settings and all five saved verdicts; both changed originals and revisions were read. The cookbook seed exactly matches the local attributed Chakrapani passage; `source_check.json` records the checked chapter context and limits. Ancient dietary opinions are historical evidence of Musonius's argument, not current clinical guidance.

## Checks the independent reviewer should make

- What useful behaviour, reasoning or expression is actually present? Quote it with its situation.
- Which version, if any, would you retain? Do not treat the saved judge's preference as authority or infer a universal consent/concern requirement from one possible objection.
- Distinguish depicted and corrected mistakes, a narrator's interpretation and an endorsed general rule.
- Check actual helpfulness, internal continuity, technical/cultural assertions and source fidelity. Fictional success is not a test of technical advice. Plausibility alone is not verification of a real cultural claim.
- Record important seed adaptations. Proposed forms and word bands are assignments, not measurements: several actual documents exceed their requested bands. None should be silently clipped to satisfy them.
- Do not claim a source-specific or Echo effect, or a trained-model benefit. The package cannot establish those claims.

## Status

Five selected existing targets reviewed in full by an independent-context, same-family native reviewer. Initial recommendations: retain `v2_0148` unchanged, and retain the other four after narrow factual/calibration repairs. `review.md` preserves the complete initial assessment; `followup.md` supports all four resulting local drafts individually. The job-loss diary and cookbook use their originals as parents, without the prior compulsory concern insertions. No corpus/training approval. The broader147-row pilot and source files are unchanged. Drafts, exact diffs and executable provenance/length checks are listed in `slop/reviews/20261019_docs_manual_repairs/brief.md`.

This package reviews historical targets, not a changed generator or judge. It does not authorize scaling or replace the required full-format review after future prompt changes.
