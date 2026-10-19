# Completion-tokenization review

**Verdict:** No blocker found for the narrow reported result. Same-family, independent-context review—not cross-family scientific certification. Read-only; no execution, API/model calls, or edits.

## Ranked findings

1. **Low: the earlier draft-length gate omits appended EOS.**  
   `/workspace/2026/constitutional_grafting/slop/reviews/20261019_docs_manual_repairs/verify.py` checks `assert tokens <= 2048` before completion tokenization. A document with exactly 2048 tokenizer IDs and no terminal EOS passes that gate but becomes `[2048, 1]` after completion processing. This does **not** invalidate the current counts: all reported drafts fit comfortably.  
   **Check:** a boundary fixture with exactly 2048 non-EOS-ending IDs would confirm or disprove the inferred discrepancy. Count completion output, including EOS, when asserting single-block fit.

2. **Informational: retention is bounded, not universal.**  
   `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/source/completion.py.txt` sets `max_length=cfg.sequence_len * 64`; `source/prompt_tokenizers.py.txt` uses `truncation=True` and appends EOS only when `len(result["input_ids"]) < self.max_length`. Thus inputs exceeding 131072 tokens can be clipped, and inputs reaching that cap need not receive EOS. The README acknowledges the cap; the observed documents are far below it. No current-input failure identified.  
   **Check:** cap-boundary fixtures would test these unexercised cases.

## What the evidence establishes

The source override bypasses instruction masking: completion calls `_tokenize(full_prompt)`, whose assignment is `result["labels"] = result["input_ids"].copy()`. Therefore `train_on_inputs=False` does not cause an assistant-only mask on this path.

The verification code compares flattened IDs **and labels** against independently invoked, untruncated whole-text tokenization plus EOS. This is a useful retention check, not merely a check that labels match already-clipped inputs. Supplied log and summary agree:

- Frozen: **1585 documents → 1585 chunks**.
- Pilot: **147 → 152**, with five split documents.
- Drafts: **13 → 13**.
- All reported IDs, including EOS, retained as unmasked labels.

Selected decoded examples support the described context break: `v2_0107` ends its first fragment with `[Record continues 14`, and its second begins `:52.`. Its substantive conclusion remains in fragment one. This does not establish semantic integrity of the other four splits.

Under ordinary per-fragment causal shifting, the first label of each fragment is not predicted; later fragments also lose preceding document context. Unmasked arrays therefore do **not** establish complete loss coverage. Nor do these counts establish learned character, historical training behavior, or corpus approval. The README appropriately preserves those distinctions.

## Actual complete read scope

All ten permitted files were read completely:

- `/workspace/2026/constitutional_grafting/AGENTS.md`
- `/home/code/.pi/agent/skills/ml-debug/SKILL.md`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/README.md`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/manifest.json`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/summary.json`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/verification.log`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/examples.md`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/source/completion.py.txt`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/source/prompt_tokenizers.py.txt`
- `/workspace/2026/constitutional_grafting/slop/reviews/20261019_docs_manual_repairs/verify.py`

## Residual gaps

No independent rerun or hash recomputation; counts are supplied-run evidence corroborated by static inspection. Large JSON artifacts and underlying datasets were intentionally not read. `verify.py` does not generate `summary.json` or `examples.md`; their synchronization was not independently verified. Historical image/cache identity, downstream filtering, attention-mask/collator behavior, and actual loss remain unverified. Current registry metadata cannot recover missing historical provenance.

# Follow-up review: EOS gate and artifact synchronization

**Verdict: both concerns resolved within the stated local scope. No new blocker found.** Same-family independent-context review, not cross-family scientific certification.

## Findings

1. **Resolved — single-block gate now includes EOS.**  
   `/workspace/2026/constitutional_grafting/slop/reviews/20261019_docs_manual_repairs/verify.py` now computes:
   ```python
   completion_tokens = tokens + (raw_ids[-1] != tokenizer.eos_token_id)
   assert completion_tokens <= 2048
   ```
   For a non-EOS-ending 2048-token document, this correctly rejects single-block fit. The supplied verification log confirms:
   > `PASS boundary eos_at_2048: 2048 raw tokens -> 2049 output tokens, 2 fragments`

   The fixture exercises the source strategy rather than the draft gate directly; static inspection establishes the corrected gate’s corresponding rejection.

2. **Resolved — summaries no longer require a separate export.**  
   The same optional section constructs `summary.json` from `result`/`audit`, hashes the written `tokenization.json`, renders `examples.md` from `examples`, and records current file hashes in `inputs.json`. This addresses the prior synchronization concern. Writes use temporary files followed by replacement.

   **Residual limitation:** atomic replacement is per file, not a transaction across the artifact set. Interruption or concurrent writers could still produce mixed artifacts. No such inconsistency was observed here; independent hash recomputation was not performed.

3. **Confirmed — retention has a finite ceiling.**  
   `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/verification.log` reports:
   > `PASS boundary reference_cap: 131073 raw tokens -> 131072 output tokens, 64 fragments`

   The code asserts equality to the raw prefix, not prefix-plus-EOS. The README now explicitly limits retention to the checked corpus and acknowledges clipping above 131072 tokens.

## Evidence and limits

The updated summary and log retain the original counts: **1585→1585**, **147→152 with five split documents**, and **13→13**. They report unchanged unmasked-label retention for these corpus inputs.

`/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/exit_status.txt` contains **`0`**, supporting the reported successful repeat. The first invocation’s lost process notification remains an orchestrator-reported event, not independently reconstructed here.

The README still correctly distinguishes source-extracted tokenizer behavior from installed-trainer execution, historical cache identity, downstream filtering/collation, causal loss coverage, and learned character. Retained labels do not imply that every token receives a causal prediction loss or retains preceding-fragment context.

## Actual follow-up read scope

Read completely:

- `/workspace/2026/constitutional_grafting/slop/reviews/20261019_docs_manual_repairs/verify.py`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/README.md`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/summary.json`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/verification.log`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/inputs.json`
- `/workspace/2026/constitutional_grafting/slop/research/20261020_completion_tokenization/exit_status.txt`

Prior complete instruction/skill/source reads stand. No execution, discovery, edits, external requests, or large raw JSON reads. Generated `examples.md` was assessed through its renderer, not reread during this follow-up.