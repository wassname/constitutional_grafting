# Unapproved document review slice

PI/OpenAI. Twenty distinct selected targets (11,710 words;15,689 EOS-inclusive tokens): fifteen locally edited documents and five retained unchanged. This is a review deliverable, not the proposed roughly2x corpus, a training-ready approval or evidence of model improvement. No model generated this export and no training file changed.

- `documents.jsonl`: the exact chosen plain document text, one version per ID, with no new chat formatting or reply-only mask.
- `manifest.json`: text and source/review hashes, selected variant, editor, lengths and provenance links. Original teacher metadata, full seeds/prompts, objections and limits remain in the cited dossiers.
- `final_verification.log`: complete frozen-slice reconstruction passes, including full reconstructed generation prompts and mandatory reserved-source checks. Every selected text fits2048 tokens including EOS. Word-band deviations in unchanged sources remain disclosed in their dossiers.
- `review.md`: independent implementation review and follow-ups. The final prompt-binding follow-up resolves the earlier failed seed-field check, preserved in `failed_seed_field_verification.log`. This is same-family review, not full-corpus approval.

The selection includes affection and friendship, competent help, humour, learning from errors, hard advice and disagreement. It is deliberately selected, not a representative sample or an estimate of the best mixture. Candidate and repaired variants are alternatives, never two added rows.

Three other pilot rows use reserved source games and are not selected. Source eligibility and actual character quality are separate questions; the untrained pilot does not establish leakage in any trained model.

Verify the exact frozen slice without overwriting it:

```sh
UV_EXCLUDE_NEWER='8 days' uv run --script slop/reviews/20261020_curated_slice/export.py --check
```

Read a complete target, for example:

```sh
jq -r 'select(.id == "v2_0144") | .text' slop/reviews/20261020_curated_slice/documents.jsonl
```

Individual editorial recommendations and their limits: `slop/reviews/20261019_docs_manual_repairs/brief.md`, `slop/reviews/20261020_positive_data_package/brief.md`, and `slop/reviews/20261020_ordinary_help_package/brief.md`. The remainder of the pilot and the larger existing donor corpus are not approved by this export. Actual trainer masks, broader factual verification and new-model results remain unfinished.
