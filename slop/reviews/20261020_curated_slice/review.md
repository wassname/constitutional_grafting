# review-slice export

**Verdict:** No blocker identified for this concrete, unapproved 20-document export. Two low-priority guardrail gaps remain. Same-family review independent of the parent; not fresh-stateless or cross-family certification. This is a separate implementation review, not a replacement assessment of tokenization.

## Ranked gaps

1. **Low — reservation checks fail open for missing policy entries.**  
   `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/export.py` checks eligibility only under `if ident in policy:`. A selected source requiring reservation checks could pass if its policy entry were absent; the script also does not bind that entry’s `source_id` to the dossier.

   **Current evidence:** the selected `v2_0034` entry has both flags false. The three reserved IDs (`v2_0053`, `v2_0070`, `v2_0132`) and extraction-flagged `v2_0015` are absent from selection. No actual reservation mistake observed.  
   **Discriminating check:** require policy coverage for every selected source of the applicable type, and compare source identity. The other selected dossiers were outside this review’s scope.

2. **Low — overwrite protection covers the documents file, not the whole artifact pair.**  
   The same script asserts only:
   > `assert not (OUT / "documents.jsonl").exists()`

   It subsequently writes `manifest.json` unconditionally. If a prior manifest exists but `documents.jsonl` is missing, export silently replaces that manifest. Normal reruns with both files present are correctly refused.  
   **Discriminating check:** a manifest-only fixture would expose this edge case; reject either pre-existing artifact to close it. No evidence this occurred in the reported run.

## Correctness and provenance

- Selection is explicit: 15 draft IDs, four ordinary-help candidates, and `v2_0148`. The assertion `len(selected) == len({row[0] for row in selected}) == 20` prevents duplicate IDs. No directory scan automatically includes future drafts.
- Drafts use `/document`; unchanged selections use `/candidate/document`. The exporter directly assigns these strings to `text`, without stripping, chat formatting, appended EOS, or label masking. EOS is included only in the length calculation.
- **Variant spot-check:** `/workspace/2026/constitutional_grafting/slop/reviews/20261019_docs_manual_repairs/v2_0017.json` explicitly says “Use the original, not the concern-insertion alternative.” Its selected document retains the quiet job inquiry and uncertainty while replacing the regional generalization. The exporter and manifest point to this `/document`.
- **Unchanged spot-check:** `/workspace/2026/constitutional_grafting/slop/reviews/20261020_positive_data_package/v2_0148.json` contains matching original/candidate text on complete manual reading, Opus provenance, and `"documents_identical": true`. The export selects its candidate, not both versions.
- The manifest binds document, dossier, review, policy, and exporter hashes. `--check` reconstructs output and manifest using the **same implementation**; it is a consistency check, not independent validation of editorial judgments, upstream authenticity, or model behavior.
- The script checks review-file existence, not affirmative verdicts. The parent’s inspection of all 15 approval fields remains parent-supplied evidence; only `v2_0017` was independently spot-checked here.
- Supplied log and manifest agree on **20 documents, 11,710 words, 15,689 EOS-inclusive tokens**. Exit zero was reported by the parent, not independently observed through execution.

README and manifest appropriately deny corpus/training approval, representativeness, and model-improvement evidence. No semantic endorsement of all 20 follows from this review.

## Actual scope and residual gaps

Read all seven permitted files completely:

- `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/export.py`
- `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/README.md`
- `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/manifest.json`
- `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/verification.log`
- `/workspace/2026/constitutional_grafting/slop/reviews/20261020_ordinary_help_package/source_eligibility.json`
- `/workspace/2026/constitutional_grafting/slop/reviews/20261019_docs_manual_repairs/v2_0017.json`
- `/workspace/2026/constitutional_grafting/slop/reviews/20261020_positive_data_package/v2_0148.json`

Prior AGENTS/ml-debug reads stand. No execution, edits, discovery, or external requests. Output JSONL, remaining dossiers, underlying source policy/data, and cited reviews were not read or independently hashed. Actual trainer masking/loss remains outside scope.