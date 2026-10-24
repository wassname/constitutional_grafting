## Follow-up decision audit

**Recommend A: a new, separately pinned generic control matched to `chatmix`’s supervised-token total, preferentially using additional unused No Robots conversations.** Keep the existing mix unchanged and the two-epoch recipe unchanged. This directly repairs the approved requirement with less operational complexity than changing epochs. This is a recommendation, not authorization or an executed change.

### Evidence and minimum safeguards

- `scripts/data/89_run11_data.py:150–165` matches `chatgen` to `chatr13`, then concatenates them into `chatmix`. The manifest records **858,126 versus 1,715,921 labelled-token estimates**.
- `scripts/train/14_run10_chat_box.sh:86–90` trains both for two epochs.
- Count **actual retained supervised tokens after rendering, masking and length filtering**, not merely the builder’s estimate: its `ntok()` adds one token per labelled segment (`89_run11_data.py:40–41,150`).
- Preserve the existing generic subset; add unused conversations while retaining the current exclusion of prompts answered in `chatr13` (`:152–153`). Pin the new file/hash and resolved configuration, and explicitly verify that the launcher consumes that file without changing the pinned originals.
- Confirm the projected remaining workload fits the unchanged deadline. No evidence supplied establishes that yet.

### Repetition and row matching

**Duplicating the existing control fixes exposure count but introduces a real diversity/repetition confound.** The control would revisit fewer distinct examples more often than the mixed corpus. That is not equivalent to Praxis’s replacement with additional length-matched generic text. It is still an interpretable, token-exposure-matched control, but not a clean content-only comparison. Prefer unused cached conversations; if insufficient, disclose the unique/repeated token counts rather than claiming full matching.

**Row matching is not required for subtraction to be mathematically valid, but matters scientifically in this implementation.** With unpacked microbatches of one row, fixed gradient accumulation and epoch-based cosine scheduling, unequal rows mean unequal optimizer steps and warmup durations. Praxis matched both rows and lengths (`docs/papers/2026_nutter_grafting-beliefs.md:263,2637–2638,2661–2667`).

Do **not** casually concatenate independent chats to manufacture matching rows: that changes attention context and potentially masks/boundaries. Prefer selecting naturally suitable whole conversations to approximate row/length matching. If that cannot be achieved simply, prioritize correct supervised-token exposure and disclose the remaining schedule mismatch. Four epochs on the old control would retain that mismatch and add repetition; it is not the cleaner minimal repair.

### What the repaired comparison establishes

It tests whether subtracting this **token-matched generic-chat update** improves the fixed donor-plus-chatmix graft’s capability/character trade-off. It does not isolate a pure constitutional direction, prove generic learning cancels linearly, or eliminate schedule, diversity and independently calibrated spectral-penalty differences. Compare at matched behavioural strength where the measured cells permit it.

Accept the supplied confirmation that the live attach environment is correct: **no current retrieval exposure is indicated**. Preserve and disclose the document schedule mismatch; this follow-up does not recommend retraining documents.
## Repair implementation gate

## PASS — minimal repair, with consumption verification required

No blocking defect found in `chat_control()` for the supplied corpus. This repairs **pre-split supervised-token matching**, not every training confound.

**Evidence**
- `scripts/data/89_run11_data.py:180–185` counts each segment with `add_special_tokens=False`, counting only labelled segments. This matches the retrieved `input_output_strategy.py:18–28` with `train_on_inputs=false`; no extra EOS is appended.
- `:188–199` exhausts unique eligible conversations before repeating, retains whole conversations and checks sequence length.
- The new manifest reports **1,709,519 versus 1,709,438 tokens**, **156 repeated occurrences / 27,248 tokens**, and maximum sequence length **2,930**. These support the stated 0.0047% mismatch and 1.59% repetition.
- Existing conversation **segments** can be preserved verbatim; whole rows are not byte-identical because `:192` changes IDs and adds `source_id`.

**First check before deployment:** confirm chatgen has neither been read nor prepared/cached at `outputs/prepared_r10_chatgen`. Then verify the remote symlink resolves to the new file’s recorded hash and that preprocessing reports **9,418 input rows**, not the old **4,685**. An atomic symlink is a valid routing mechanism, but does not invalidate already-prepared data. Archive the original bytes and record the override as proposed; the original manifest alone will no longer describe executed chatgen data.

**Limitations**
- The unchanged SFT configuration reserves **5% validation**. Thus these totals do not establish equal *training-consumed* tokens; inspect retained training-token totals after splitting/filtering.
- Repeated conversations may cross the random train/validation split. Internal control validation loss is therefore not clean held-out evidence.
- Row counts, optimizer schedules, unique-data exposure and calibrated spectral penalties remain unmatched. The result can establish the effect of subtracting this approximately token-matched generic control—not content-only causal isolation.
- Additional workload may reduce completed evaluation coverage under the unchanged deadline.
- The builder’s ID-keyed count dictionary (`:184`) assumes duplicate IDs have identical segments. The supplied corpus checks should cover that assumption; I did not independently recount or hash all rows.

The deployment procedure was described, not supplied as executable code or observed execution. Original-file preservation and full segment equivalence remain supervisor-supplied evidence.
Independent reviewer: reviewer-openai / gpt-6-astra; initial review d0dae2ae, decision follow-up 1d38e33f, implementation gate 0adeee34. Archived by PI/OpenAI.
