# Heal trace full read — reader 3

## Coverage and decisions

Read the brief in full and all **96/96 assigned unread kept candidates**, and no unassigned candidate replies, from `reply_batches/batch_072.jsonl` through `batch_095.jsonl`, selected strictly by `reader_assignments.json:unread_kept_ids`. Read every selected seed, exact request, complete native reasoning and final answer in the rendered training format. Native/rendered equality was checked programmatically (405,324 characters of native reasoning plus final answers). The rendered user prompt strips trailing whitespace in two source-extraction requests; no substantive prompt differences were found. All 24 batch SHA-256 hashes match the assignment manifest.

- **Keep: 40**
- **Hold: 34** — fixable defects; not acceptable unchanged.
- **Reject: 22** — predominantly sustained reasoning loops/indecision, even when the final answer is right.
- Sources: 68 GSM8K train, 18 No Robots, 10 ordinary-help requests.

`reader_3.jsonl` contains exactly one decision, one-line reason and defect quote (when applicable) per assigned reply. All 56 non-keep records have quotes verified against the actual reply. No reply was edited or regenerated. These are capability/format-repair judgments, not character evaluations or training approval.

| Batch | Assigned/read | Keep | Hold | Reject |
|---|---:|---:|---:|---:|
| 072 | 4/4 | 2 | 1 | 1 |
| 073 | 3/3 | 1 | 1 | 1 |
| 074 | 3/3 | 0 | 2 | 1 |
| 075 | 4/4 | 1 | 2 | 1 |
| 076 | 4/4 | 1 | 1 | 2 |
| 077 | 4/4 | 3 | 0 | 1 |
| 078 | 5/5 | 1 | 1 | 3 |
| 079 | 5/5 | 3 | 1 | 1 |
| 080 | 5/5 | 4 | 1 | 0 |
| 081 | 3/3 | 2 | 1 | 0 |
| 082 | 5/5 | 1 | 3 | 1 |
| 083 | 2/2 | 0 | 0 | 2 |
| 084 | 5/5 | 2 | 2 | 1 |
| 085 | 3/3 | 1 | 2 | 0 |
| 086 | 5/5 | 0 | 2 | 3 |
| 087 | 4/4 | 1 | 2 | 1 |
| 088 | 4/4 | 2 | 2 | 0 |
| 089 | 3/3 | 1 | 2 | 0 |
| 090 | 5/5 | 4 | 0 | 1 |
| 091 | 2/2 | 1 | 1 | 0 |
| 092 | 5/5 | 3 | 1 | 1 |
| 093 | 5/5 | 2 | 3 | 0 |
| 094 | 4/4 | 2 | 2 | 0 |
| 095 | 4/4 | 2 | 1 | 1 |
| **Total** | **96/96** | **40** | **34** | **22** |

## Notable defects

1. **Reasoning loops survive the wait-count filter.** Examples: `gsm_train_1291`, `gsm_train_4426`, `gsm_train_4085`, and `gsm_train_4568` repeatedly announce completion and reopen settled wording/arithmetic questions. The blackjack trace ends mid-sentence: “If I meant I walked away with $60, I'd”. The bear trace `gsm_train_61` ends mid-calculation, “Salmon = 20”, after extensive repeated ambiguity debate. Their correct finals do not make these useful think-close-answer examples. Multiple thank-you notes also repeatedly reselect near-identical sentences; these were rejected rather than treating fluent finals as sufficient.
2. **Stray suffixes inside supervised reasoning.** `.cw`, `.ot` and `.box.` appear in otherwise complete replies (e.g. `gsm_train_255`: “Final Answer:** 25.cw”; `gsm_train_6942`: “Ready to write.box.”). Isolated suffix defects were held; sustained loops plus suffixes were rejected.
3. **Invented review context.** Several traces refer to a nonexistent supplied “good response” although the exact request contains only the user question. Examples: `gsm_train_3082`, `gsm_train_4119`, `gsm_train_5342`, `gsm_train_6769`, `gsm_train_3638`. Held as training-format/meta-context artifacts, not arithmetic failures.
4. **Concrete code/output errors.**
   - `ordinary_0_23`: actual moving averages are `[16.5, 18.0, 19.5, 21.0, 22.5, 24.0, 25.5, 27.0]`, not the displayed sequence with 0.75 increments. Held.
   - No Robots Unicode conversion in batch 092 leaves code points unchanged rather than converting to their represented digit values. Its optional string output is also wrong: actual `3673475684837334578228`, not `36734756463673334578228`. Held.
   - Chrome opener in batch 086 rejects the explicitly requested `google` input, never adds `.com`, calls `open_new` rather than `open_new_tab`, and adds an irrelevant security concern (“Automatically opening websites could be misused”). Rejected.
   - React forward-ref explanation in batch 074 omits hook imports and states version-unqualified requirements that omit React 19 ref-as-prop support. Held.
   - MongoDB guide in batch 093 uses `datetime.utcnow` without importing `datetime`; its async fragment is not a standalone script. Current Motor recommendation status also remains unverified. Held.
   - Canvas explanation in batch 094 invents a default-font exact measurement (“Hello World” is 84 pixels), despite acknowledging platform dependence, and invokes absent prior response context. Held.
   - `ordinary_7_33` calls GNU find's binary `M` unit megabytes rather than MiB; a precise decimal-MB threshold needs byte units. Held for technical qualification, not for any destructive operation.
5. **Source-grounded does not guarantee factual correctness.** Batch 082 ruminant summary inherits misleading placement of microbial digestion in the downstream stomach chambers rather than emphasizing rumen/reticulum fermentation. Its star-engulfment summary treats Earth's eventual engulfment and approximate timing as certain rather than qualified. Both held for factual checking/qualification. Kept source-extraction/news summaries were checked against the supplied passage; no independent archival/news retrieval was performed.
6. **Other small defects.** `ordinary_3_7` includes “since I am a text model” in addition to its suffix; `gsm_train_440` adds a confused, unnecessary aunt/sister/cousin aside. Both held. Depicted balloon-taking in `gsm_train_3432` is simply used to compute the transfer, without teaching a moral judgment or refusal; kept.

## Validation and limits

- The batches do **not** contain GSM8K gold answers. With supervisor authorization, read gold only for the 68 assigned GSM8K IDs from the existing local HF Arrow cache: `openai/gsm8k`, config `main`, train split, revision `740312add88f781978c0658806c59bc2815b9866`. Matched each by exact question text, not just ID index. All indices also match; no mismatches. Independently recomputed every problem and checked 68 explicit arithmetic expressions on CPU; all final numeric answers agree with gold under the intended reading.
- Gold working is not always clean: `gsm_train_7034` contains incorrect narrative values (“7.5”, “20”) but its final 25 agrees with recomputation and the candidate. `gsm_train_3789` gold mislabels volume as area/square inches; the candidate uses cubic inches. `gsm_train_7309` gold's final explanatory line misattributes the combined usage to Aaron; the candidate correctly answers for both people. No candidate was penalized for these gold-only defects.
- Ran actual JS examples in Node for both numeric-sort candidates and both recursive/iterative factorial fixes (5, 0, -1 inputs): passed. Ran the actual random-letter function with NumPy: shape `(3,4)` and uppercase-letter checks passed. Executed the moving-average and Unicode snippets locally to confirm the held output discrepancies. No browser, database, network or model API was invoked.
- Structural checks: 96 unique IDs, exact assignment-set coverage, required five JSON fields, allowed decisions, exact defect quotes, batch hashes, and native reasoning/final reconstruction passed. Initial strict prompt comparison failed on trailing spaces in two seeds; rerun with outer-whitespace normalization passed. An initially overlong Unicode quote was corrected to the exact quoted erroneous output; all defect quotes now match.
- Only `full_read/reader_3.jsonl` and this report were written. No tests/scripts were added, no candidates changed, no commits or staging performed. Holds and rejects need parent handling before any training selection; this read makes no claim about healing effectiveness.

-- PI/Sol (heal reader 3)
