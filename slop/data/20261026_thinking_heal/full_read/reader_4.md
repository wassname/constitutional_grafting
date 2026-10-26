# Heal trace full read — reader 4

2026-10-26. Scope: only `unread_kept_ids` assigned in `reader_assignments.json` for `reply_batches/batch_096.jsonl` through `batch_119.jsonl`.

## Coverage and decisions

**100/100 assigned replies read in full: 47 keep, 33 hold, 20 reject.** Sources: 82 GSM8K train, 11 No Robots, 7 ordinary-help requests. Every assigned seed, exact request, complete native reasoning and final answer was read; repeated provider/rendered copies were checked for equivalence rather than treated as additional candidates. No unassigned replies were reviewed. The brief and constitution sections 1–5 were read before judging.

`reader_4.jsonl` contains exactly one ordered verdict per assigned ID, with batch path, one-line reason, and a verbatim short defect quote for every hold/reject. Holds are **not approved for training unchanged**. No reply was edited or regenerated; rejected/held originals remain untouched.

| Batch | Read | Keep | Hold | Reject |
|---|---:|---:|---:|---:|
| 096 | 5 | 2 | 3 | 0 |
| 097 | 4 | 3 | 1 | 0 |
| 098 | 2 | 1 | 1 | 0 |
| 099 | 4 | 3 | 1 | 0 |
| 100 | 5 | 2 | 0 | 3 |
| 101 | 3 | 2 | 1 | 0 |
| 102 | 3 | 0 | 2 | 1 |
| 103 | 4 | 3 | 0 | 1 |
| 104 | 4 | 1 | 3 | 0 |
| 105 | 5 | 2 | 3 | 0 |
| 106 | 5 | 1 | 3 | 1 |
| 107 | 5 | 3 | 2 | 0 |
| 108 | 5 | 2 | 0 | 3 |
| 109 | 4 | 1 | 0 | 3 |
| 110 | 5 | 1 | 2 | 2 |
| 111 | 5 | 0 | 2 | 3 |
| 112 | 4 | 3 | 1 | 0 |
| 113 | 3 | 2 | 0 | 1 |
| 114 | 4 | 3 | 1 | 0 |
| 115 | 5 | 1 | 4 | 0 |
| 116 | 4 | 3 | 1 | 0 |
| 117 | 5 | 2 | 2 | 1 |
| 118 | 3 | 2 | 0 | 1 |
| 119 | 4 | 4 | 0 | 0 |
| **Total** | **100** | **47** | **33** | **20** |

## GSM8K verification

The batches did not actually include gold answers. Supervisor authorized consulting GSM8K train, matching **exact question text, not numeric ID/index**. All 82 assigned GSM questions matched the existing local `openai/gsm8k`, `main`, `train` cache:

`/home/code/.cache/huggingface/datasets/openai___gsm8k/main/0.0.0/740312add88f781978c0658806c59bc2815b9866/gsm8k-train.arrow`

Each problem was independently recomputed. An inline CPU check compared all 82 independently written calculations to exact-question-matched gold final numbers: **82/82 agree**. No gold-final/recomputation disagreement. One model final disagrees:

- **Reject `gsm_train_1650` (118):** model concludes Sarah took **2**, but gold and recomputation give **12**. The last neighbor found only eight cookies and has not already taken ten. Thirteen other neighbors took 130, leaving `150 - 130 - 8 = 12` for Sarah. The reply incorrectly counts fourteen full portions, then loops over the contradiction instead of correcting it. Quote: “Sarah took **2** cookies.”

Gold narratives contain separate mistakes that do not change their correct final numbers: `855` says $900 remaining instead of prompt $800; `2490` labels the fish calculation birds; `6713` writes an invalid expression for six blueberry containers; `6828` changes 38 pencils to 36 in its final narrative. These were not copied into verdict reasoning.

- **Hold `gsm_train_2064` (115):** final $7,060 is correct, but the labelled subtraction scratchpad leaves incorrect borrowing steps unrepaired: “7 - 9 (borrow from 2, becomes 12) -> 12 - 9 = 3”. This is distinct from an explicitly corrected tentative error, such as the decimal placement correction in kept `gsm_train_6828`.

## Notable trace defects

### Labelled reasoning artifacts

Correct final answers do not make the whole training span clean. Holds flag stray `.cw`, `.box.`, `.b`, or `.ot` suffixes, e.g. `gsm_train_387`: “Final Answer:** 3.cw”; `gsm_train_4792`: “Ready to write.box.”; `gsm_train_1985`: “Matches the thought process above).ot”. These appear inside the labelled think span, not merely provider metadata.

Other holds flag spurious references to a supplied answer where the exact request contains only the user question, e.g. `gsm_train_1741`: “Matches the provided good response”. The actual requests were checked; no good response was supplied. Some replies have both defects.

### Reasoning loops missed by the lexical filter

Nineteen rejects have correct numerical/source-grounded final content but extensive repetitive redrafting or ambiguity rechecking; the twentieth, `gsm_train_1650`, is also wrong. Examples:

- `gsm_train_234`: repeatedly revisits using or withholding the same quarter/dime after finding eight nickels.
- `gsm_train_6777`: repeatedly reopens time-versus-distance halves after obtaining 620 km.
- `gsm_train_6666`: extreme repeated output planning and arithmetic checks, including “Okay, I'm repeating myself to ensure accuracy.” Its reasoning ends mid-sentence.
- `gsm_train_7415`: extreme repetition around the “then”/“than” typo and upstairs/downstairs relationship; reasoning ends unfinished.
- `gsm_train_4598`, `509`, `6016`: long ambiguity loops with unfinished reasoning tails despite complete final answers.
- No Robots Mars, film and news summaries, and `ordinary_6_38`: repeated near-identical drafts rather than productive revisions.

Reject decisions concern the full native training trace, not just final-answer accuracy or token length. Verbose but convergent mathematical checks were not automatically rejected (e.g. `gsm_train_4762`, `3590`). Independent review should inspect these qualitative boundaries rather than infer a mechanical length cutoff.

## Technical checks and holds

All checks were inline CPU-only, using already installed Python/Node/TypeScript/GNU find; no model or network service calls, downloads, new scripts, commits, or training.

- **Moving average, `ordinary_0_30` (101), hold:** executed the actual function against direct window sums for lengths 0, 10, 29, 30, 31 and 100, window 1, and invalid window 0. Computation passes; claimed first result at “index 30” is off by one for Python zero-based input indexing (first full window ends at 29).
- **Palindrome, No Robots `808fc433…` (103), keep:** both actual implementations pass all eight displayed examples in Node. Scope is ASCII letters/digits and punctuation/case normalization, not a claim of Unicode-aware palindrome handling.
- **Numeric sorting, `ordinary_4_11` (104), hold:** actual main example sorts counts to 11, 18, 24. The optional `(a.count || 0) - (b.count || 0)` is not validation; a nonnumeric string remains invalid/produces NaN. Quote: “If it might be a string or missing, add validation:”.
- **RegExp exec, No Robots `fd83445b…` (106), hold:** Node confirms lastIndex values **10, 13, 16**, not printed **9, 11, 13**. Non-global `match()` does include index/input/capture metadata, contrary to the table. The generic exec loop also fails to advance zero-length matches, confirmed with two bounded calls (no infinite loop was run).
- **TypeScript partition, No Robots `114f5472…` (110), hold:** the unconstrained return-only `B` is not inferred as the complement. Compiled the actual helper plus actual Cat/Dog example in a virtual in-memory TypeScript 7.0.2 project, adding only a diagnostic assertion `const confirmDogs: Dog[] = dogs;`. Compiler confirms “Type 'Pet[]' is not assignable to type 'Dog[]'.” The response claims Dog[] and calls the helper type-safe despite acknowledging an unsafe assertion. No files emitted.
- **Password generator, No Robots `a0f15f73…` (115), hold:** actual function passes 1,000 shape checks (exactly four characters, one from each category). Its claim “This function ensures your passwords are secure” is false for four-character passwords using noncryptographic `random`. No refusal or safety lecture is needed to identify that factual defect.
- **Redux wrapper, No Robots `d188e866…` (115), hold:** identifying a typed shallowEqual wrapper is correct, but default `useSelector` comparison is strict `===`, not Object.is. Describing mutation-masked missing rerenders as desirable optimization is misleading; immutable nested changes replace relevant references. It also contains a spurious supplied-good-response reference. A live React/Redux integration test was not run.
- **List/set, `ordinary_5_8` (105), keep:** executed the actual demonstrations statement by statement; the only error is the explicitly documented KeyError from removing missing 100. Final list/set contents and membership behavior agree.
- **GNU find, `ordinary_7_25` (102), hold:** main +25M command is fine for the normal binary command-line unit interpretation, but `25M` means a rounded size bucket, not exactly 25 MB; +24M is not an exact >=25 MiB predicate. Existing 86,759-byte batch file matches GNU find's `-size 1M`, confirming rounding without creating/modifying any test files.
- **GNU find, `ordinary_7_38` (119), keep:** no erroneous exact-size alternatives; +38M is valid read-only search above 38 MiB. “MB” is interpreted in the usual binary GNU find convention, not decimal 38,000,000 bytes.

No kept reply adds an observed moralising refusal, safety lecture, or assistant persona/identity claim. First-person thank-you text is requested composition, not assistant identity. Fictional arithmetic and the supplied medication scenario were judged as arithmetic, not converted into character instruction or new advice. Source-bound extraction/summarization was checked against its supplied text rather than treated as independent reporting.

## Validation and limitations

- JSONL parses; exact five required keys per row; valid decisions; 100 unique IDs; exact assignment ID/batch order and no extras; every hold/reject quote matches the native text verbatim.
- SHA-256 of all 24 source batches still matches assignment manifest.
- All 100 exact requests contain the seed as their sole user message; labelled rendered spans preserve the full native reasoning/final with only boundary-whitespace normalization and native template delimiters.
- Initial exact-byte rendered-span assertion failed because the renderer normalizes boundary whitespace; corrected expectation passes for all 100. No candidate was changed.
- Initial TypeScript test used an incompatible classic compiler module path and failed to load; corrected test used the installed native TypeScript virtual filesystem/compiler and reproduced the type error. This was a harness issue, not a candidate execution result.
- All tests were ephemeral inline commands. No test files added. No staged files (`git diff --cached --name-only` empty). Only the two requested reader-4 artifacts were written.
- These are reader recommendations, not corpus/training approval. No repairs performed. Independent merge/review remains with the parent; only keep recommendations are eligible for its next gate.

-- PI/Sol (heal reader 4)
