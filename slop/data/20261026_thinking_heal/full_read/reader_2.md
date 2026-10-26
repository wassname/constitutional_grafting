# Heal trace full read — reader 2

Read the full brief `slop/plans/20261026_heal_trace_full_read.md` and reviewed **101/101** assigned unread kept candidates in `reply_batches/batch_048.jsonl` through `batch_071.jsonl`. Coverage is exactly the `unread_kept_ids` lists in `reader_assignments.json`, not every row in those batches. Each assigned seed, exact user request, complete native reasoning and final answer was read. Truncated inspection output was reread in smaller chunks. Constitution v4 sections 1–5 were also read in full before judging.

**Decisions: 59 keep, 41 hold, 1 reject.** `reader_2.jsonl` records each ID, batch, decision, one-line reason, and a native-text quotation for every defect. Holds are **not acceptable as-is**: they indicate an otherwise usable pair with repairable defects. No candidate was edited or regenerated. These are capability-repair traces, not character examples; this review does not approve training.

## Coverage

| Batch | Read | Keep | Hold | Reject |
|---|---:|---:|---:|---:|
| batch_048 | 5 | 3 | 2 | 0 |
| batch_049 | 5 | 2 | 3 | 0 |
| batch_050 | 3 | 1 | 2 | 0 |
| batch_051 | 4 | 2 | 2 | 0 |
| batch_052 | 4 | 1 | 3 | 0 |
| batch_053 | 2 | 2 | 0 | 0 |
| batch_054 | 3 | 1 | 2 | 0 |
| batch_055 | 5 | 2 | 3 | 0 |
| batch_056 | 4 | 3 | 0 | 1 |
| batch_057 | 5 | 3 | 2 | 0 |
| batch_058 | 5 | 5 | 0 | 0 |
| batch_059 | 4 | 2 | 2 | 0 |
| batch_060 | 4 | 3 | 1 | 0 |
| batch_061 | 4 | 3 | 1 | 0 |
| batch_062 | 4 | 3 | 1 | 0 |
| batch_063 | 5 | 4 | 1 | 0 |
| batch_064 | 4 | 3 | 1 | 0 |
| batch_065 | 5 | 3 | 2 | 0 |
| batch_066 | 4 | 1 | 3 | 0 |
| batch_067 | 5 | 4 | 1 | 0 |
| batch_068 | 5 | 3 | 2 | 0 |
| batch_069 | 3 | 2 | 1 | 0 |
| batch_070 | 4 | 3 | 1 | 0 |
| batch_071 | 5 | 0 | 5 | 0 |
| **Total** | **101** | **59** | **41** | **1** |

## Notable defects

- **Reasoning artifacts are frequent even when the final is correct.** Literal suffixes such as `cw`, `cs`, `ct`, `sc`, `ot`, and `b` occur at the end of native reasoning and would receive loss in the rendered training segment. Examples: `gsm_train_6627` ends `Ready to write the solution.cw`; `ordinary_3_33` ends `markdown block).ot`. These are holds, not silently cleaned keeps.
- **The wait-count filter misses non-progressing loops.** Correct finals do not rescue prolonged reopening of the same resolved ambiguity. Examples include `gsm_train_3484` (light intervals), `gsm_train_548` (weekly profit), `gsm_train_5685` (future ages), `gsm_train_7061` (which box contains candles), and `ordinary_6_26` (repeatedly redrafting a two-sentence note). Normal worked calculations, distinct verification methods, and resolved corrections were not automatically excluded for verbosity.
- **Reject `gsm_train_465` (batch_056):** extreme cycling between 5 and 9 minutes. Native reasoning terminates mid-sentence: `However, in the context of "deciding which route", the 14 minute route is`. The final chooses 5 with a caveat, but this is a poor trace for teaching coherent think-to-answer completion.
- **Three moving-average examples have fabricated numerical output despite sound functions.** Executed the actual candidate functions on CPU:
  - `ordinary_0_48` (batch_050): actual complete averages `[24.5, 25.5, 26.5]`; claimed first/last are `25.00` and `49.00`.
  - `ordinary_0_29` (batch_065): actual last five `[24.0, 25.5, 27.0, 28.5, 30.0]`; claimed `[39.0, 39.5, 40.0, 40.5, 41.0]`.
  - `ordinary_0_14` (batch_071): actual formatted complete averages `106.50, 107.57, 108.43, 109.50, 110.57, 111.43, 112.50`; several sample rows disagree, starting with claimed `106.86`.
- **C alternative fails compilation:** `no_robots_2e7f299af2175d09a9c8b8e6742bea1e0f63f2bc5d61d8ae695aa24b4ed32c3a` (batch_068). Main example passes C11 syntax checking, but the alternative calls `float_array_init_with_capacity` before declaring it. GCC reports an implicit declaration and conflicting types. Capacity multiplication also lacks overflow guards despite broad memory-safety claims. Hold the whole reply, not just its alternative.
- **Uncorrected arithmetic inside otherwise correct reasoning:** `gsm_train_603` says `Alternatively: $13 - 7 = 6$ (ones place)` before reporting the correct final 27. This is not a clean correction example; hold.
- **Technical imprecision:** `ordinary_5_30` (batch_054) says set order “may change each time,” conflating lack of guaranteed order with iteration instability. The Java priority-queue reply `no_robots_548e41a8c5e9e27f2b2934bc225e26259966b70f6881f5327e181760fa5dc76c` (batch_055) advertises “Automatic Sorting” without explaining heap order versus a sorted sequence. Both are holds for clarification.

## Content and verification notes

- Recomputed every assigned GSM8K problem from its supplied facts. Following the parent's queued guidance, read the **73 assigned GSM8K gold answers only** from the local Hugging Face `openai/gsm8k`, config `main`, split `train` cache, matching **exact question strings**, never numeric IDs or row indices. All 73 matched uniquely; all 73 gold final values agree with independent recomputation and the candidate's final numerical answer. **Zero numerical gold/recompute disagreements.** This resolves the initial missing-gold limitation in the batches. Each GSM review reason now records its gold final and independent arithmetic expression; original decisions remain unchanged because correct finals do not cure defective reasoning.
- Reading-comprehension answers were checked against their entire supplied excerpts. Their historical or scientific passages are not treated as independently verified current facts. The Cambrian answer is held for a native suffix and its omission of the land-colonisation qualification.
- No kept response was identified as moralising, refusing, lecturing on policy, or making assistant persona/identity claims. The shell replies' read-only explanations directly address the user's explicit non-modification constraint, rather than introducing policy voice. Fictional events and ordinary drafted first-person thank-you wording are not assistant identity claims.
- Some accepted traces contain generic meta-framing such as “matches the provided good response.” This is noted as stylistic/meta noise, not evidence that a gold response was actually supplied. Keeps have coherent calculations and complete finals independently of that framing.
- `gsm_train_7261` is a useful genuine correction: it briefly counts a refill as an additional 3000 L, notices the discrepancy, corrects the added amount to 2820 L, and reaches the independently recomputed 4582 L without an unresolved contradiction.

## Checks run (no persistent test artifacts)

1. Python assertion: all 101 exact request message payloads equal the fully read seed prompt; inspected fixed provider/request parameters separately.
2. Python schema/coverage check: exactly 101 unique rows, exact assignment membership and batch bindings, required five fields, valid decisions, and literal native-text matches for every defect quote. Two quotation mismatches caused by Markdown emphasis were corrected **in the review artifact only**; final check passes.
3. Executed the three actual moving-average functions in memory, reproducing their incorrect displayed examples.
4. `gcc -std=c11 -Wall -Wextra -Werror=implicit-function-declaration -x c -fsyntax-only -` on both C blocks via stdin: main passes; alternative fails as expected. No C source or compiler output files created.
5. Executed actual JavaScript sort examples `ordinary_4_4` and `ordinary_4_6` with `node -` and asserted ascending count order; both pass, and the second also displays correct descending output.
6. Executed both actual timed-increment functions from batch_064 in memory: zero duration returns zero and short positive durations produce increments; delayed version reports positive count and elapsed time at least the requested duration. Runtime-dependent counts were not treated as fixed targets.
7. Checked staged paths with `git diff --cached --name-only`: none at inspection. No staging, commits, API calls, dependency installs, or edits outside the two assigned output files.
8. Follow-up gold check: read cached Arrow data with `.venv/bin/python -B` and `pyarrow`; inspected only matching assigned answer cells after exact-question matching. Evaluated independently transcribed arithmetic with exact `fractions.Fraction` operations: **73/73 gold finals agree**. The light-bulb answer was independently derived as LCM(2,3,4)=12. The cache was read directly, without invoking a dataset loader, downloading data, or writing cache artifacts.

### Gold source and rationale disagreements

Local source: `/home/code/.cache/huggingface/datasets/openai___gsm8k/main/0.0.0/740312add88f781978c0658806c59bc2815b9866/gsm8k-train.arrow`.

Source SHA-256: `6146bca074f4c6c5e07de7e96cc968adab3833dbdafeda21830f27558eea3d9b`.

Gold's final numerical answers agree with all independent calculations, but several **gold rationales contain wording/unit mistakes** that were not copied into this review's reasoning:

- `gsm_train_3484`: gold calls the 2-second bulb blue and the 3-second bulb red; the question specifies red at 2 seconds, green at 3 seconds, blue at 4 seconds. The independent LCM and gold final both remain 12 seconds.
- `gsm_train_5681`: gold describes `72 red balls` in the yellow-pack calculation; the correct count is 72 yellow balls. The difference remains 18.
- `gsm_train_6705`: gold labels `100/2=50` as pages per day; its unit is pages per hour. The correctly recomputed weekly total and gold final both remain 1750.

These source-rationale defects do not change candidate decisions: review the actual candidate reasoning, not merely whether its final matches gold. For example, `gsm_train_603` remains held for its own false subtraction, and `gsm_train_465` remains rejected for its own severe loop and interrupted reasoning despite a gold-matching final.

Java and Express examples received static language/API inspection, not full environment integration tests. No external fact lookup or API-based judging was performed.

-- PI/Sol (heal reader 2)
