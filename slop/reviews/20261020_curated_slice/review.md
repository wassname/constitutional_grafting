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

# review-slice export — guardrail addendum

**Verdict: both original guardrail gaps are addressed in code, but final verification fails.** Do not mark this follow-up fully verified yet.

## Ranked findings

1. **Blocker to verification — selected dossier schema is incompatible with the new seed assertion.**

   `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/export.py` unconditionally accesses `dossier["seed"]` for edited documents.

   `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/final_verification.log` ends:
   ```text
   File ".../export.py", line 45, in <module>
       assert dossier["seed"] == source["seed"]
   KeyError: 'seed'
   ```

   **Observed:** the supplied final run did not complete reconstruction. At least one selected edited dossier lacks that top-level key. Its ID is not logged, so I cannot identify it from the permitted evidence.

   **Required check:** resolve the actual dossier’s seed representation explicitly—without silently skipping provenance validation—then rerun the complete `--check`. A successful complete log would resolve this blocker. The controlled guard tests do not exercise this earlier failure.

2. **Resolved statically — mandatory reservation eligibility.**

   The updated exporter derives source type from the hash-bound seed snapshot and, for `source["source"] == "machiavelli"`, directly indexes `policy[ident]`, compares `source_id`, and rejects either flag. Missing entries no longer bypass validation.

   `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/guardrail_verification.log` reports rejection of missing, mismatched, and reserved fixtures, and acceptance of an eligible fixture. These are supplied guard-AST tests, not full CLI integration evidence.

3. **Resolved statically — manifest-only overwrite protection.**

   The default export now rejects:
   ```python
   any((OUT / name).exists() for name in ("documents.jsonl", "manifest.json"))
   ```
   The guard log reports rejection of either existing file independently. This closes the previously identified ordinary manifest-only case; it is not transactional or concurrent-writer protection.

## Preservation and scope

The updated manifest retains **20 documents, 11,710 words, 15,689 completion tokens**, and the previously recorded documents hash:

`4336b884b7834f54a65b111be693a2d0e15b54260a7a410f17519fc2dc3071c3`

The guard log reports unchanged document bytes against `c46de3a`; I did not independently inspect Git or recompute hashes. The manifest’s existence and matching recorded hash do not substitute for the failed final reconstruction.

Read all four permitted files completely: `export.py`, `manifest.json`, `guardrail_verification.log`, and `final_verification.log` under `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/`. No execution, edits, discovery, external requests, or additional dataset reads.

This addendum preserves the original review’s scope: same-family independent-of-parent implementation review, not semantic endorsement, corpus/training approval, or model evidence.

## Final prompt-binding follow-up

# review-slice export — final addendum

**Verdict: the prior verification blocker is resolved on static inspection and supplied full-run evidence. No new blocker found within this scope.**

- **Root cause confirmed:** `/workspace/2026/constitutional_grafting/slop/reviews/20261019_docs_manual_repairs/v2_0054.json` has no top-level `seed`; its full reconstructed USER contains the seed. The original `KeyError: 'seed'` remains preserved in `failed_seed_field_verification.log`.
- **Provenance check preserved:** `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/export.py` now unconditionally checks every selected dossier:
  ```python
  assert dossier["generation_user_prompt_reconstructed"] == user_template.format(**source), ident
  ```
  The seed snapshot and writer are checked against package-manifest hashes before USER extraction. There is no optional-key fallback or skipped prompt check. Candidate source-ID/seed checks, mandatory MACHIAVELLI eligibility, and both-file overwrite protection remain.
- **Full verification evidence:** `final_verification.log` now reports:
  > `PASS frozen20-row slice: exact chosen text, source/review hashes, EOS-inclusive bounds and reserved-source eligibility`

  This supports successful full reconstruction, unlike the earlier guard-only fixtures. Exit zero is parent-reported; I did not execute the command.
- **Preservation:** the manifest retains **20 documents, 11,710 words, 15,689 EOS-inclusive tokens** and documents SHA256 `4336b884b7834f54a65b111be693a2d0e15b54260a7a410f17519fc2dc3071c3`, matching the previously reviewed value. I did not independently recompute hashes or compare document bytes.

**Actual scope:** completely read the four specified files under `/workspace/2026/constitutional_grafting/slop/reviews/20261020_curated_slice/`—`export.py`, `manifest.json`, `final_verification.log`, `failed_seed_field_verification.log`—and the specified `v2_0054.json`. No execution, edits, discovery, or external requests.

Same-family independent-of-parent addendum, not fresh-stateless or cross-family certification. `--check` remains same-implementation consistency evidence, not semantic endorsement, full-corpus approval, training authorization, or model-loss evidence.
