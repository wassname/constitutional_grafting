# Heal trace full read — reader 1

## Coverage and verdicts

Read **98/98 assigned unread kept candidates in full**, exclusively those in `unread_kept_ids` for `reply_batches/batch_024.jsonl` through `batch_047.jsonl`. Coverage: **77 GSM8K maths, 21 other neutral requests**. Read each seed, exact user request, complete native reasoning and final answer. No unassigned reply was displayed or reviewed. Read the full task brief and constitution sections 1–5 before judging.

**56 keep / 27 hold / 15 reject.** Each JSONL row gives the batch, verdict, reason, and an exact short defect quotation when held/rejected. Holds are excluded pending repair/review; none of the source replies was edited or regenerated. These are neutral capability/format traces, not character-training approvals.

All 24 batch SHA-256 values match the assignment manifest. All exact requests contain only their seed as the user message, with the same Qwen3.5-35B-A3B / DeepInfra configuration (thinking enabled, temperature 0.6, top_p 0.95, seed 26, max_tokens 8192). Every selected response reports stop. All labelled rendered segments equal the full native reasoning plus a closing think block and final, with boundary whitespace normalization only. In particular, normalization does not repair the incomplete sentence in `gsm_train_4053`.

### Maths verification

Recomputed all 77 problems and compared each with its matching local GSM8K train gold. The batches do not actually include gold fields; used the existing offline cache:

`/home/code/.cache/huggingface/datasets/openai___gsm8k/main/0.0.0/740312add88f781978c0658806c59bc2815b9866/gsm8k-train.arrow`

Following the queued parent guidance, revalidated gold lookup by **exact question text, not row index**: filtered the local train questions against only the 77 assigned GSM prompts, then keyed the matching gold answers by the question text. All 77 have exactly one match. Compared all 77 text-matched gold answers against the independently recomputed full-read results: 76 agree; the sole gold/recompute disagreement is `gsm_train_4105` (gold 49, recomputed 77), detailed below. The earlier index-based lookup had also checked exact question equality; this follow-up removes index lookup from the gold-matching validation. No downloads or API calls.

- **Bad gold:** `gsm_train_4105` correctly computes **77** from Monday 14, Tuesday 7, Wednesday four times Monday = 56. Gold **49** incorrectly multiplies Tuesday by four. Hold only because native reasoning ends `output.cw`, not because of the bad gold.
- **Wrong answer:** `gsm_train_6712` gives **8 mph** after two blisters. The hike actually covers two hours at 12 mph and two at 10 mph: **44/4 = 11 mph**, matching gold. The second blister forms when the hike ends. Long indecision as well; reject.
- **Contradictory final working:** `gsm_train_2340` gives the correct **51** but changes the correct equation to `x - 35 + 4 = 16`, then `x - 31 = 16`, then falsely concludes 51. Also invents a floor location for the found books; reject.
- Other final numeric answers match gold and independent recomputation. A correct final number alone did not override defective reasoning or artifacts.

## Notable defects

### Reasoning quality

Most rejects have long repeated reconsideration/redrafting, including the invitation (`ordinary_2_30`), monster/ships (`gsm_train_10`), books (`gsm_train_276`, `gsm_train_2931`), fundraiser (`gsm_train_110`), flips (`gsm_train_6374`), walking deficit (`gsm_train_4723`) and bills (`gsm_train_6392`). These are full-trace judgments, not a wait-count heuristic. Some also have incorrect claims or artifacts. Finite alternative-method verification or an explicitly corrected mistake was not itself grounds to reject (e.g. `gsm_train_4020`).

### Artifacts / incomplete reasoning

Fifteen holds contain stray native-reasoning suffixes `cw`, `cs`, `sc`, or `box.` despite correct final answers. See exact quotations in JSONL. The invitation and sports-betting summary have artifacts as well as long redrafting and are rejects. `gsm_train_4053` is held because reasoning ends mid-sentence: `*Wait, just to be super`; final answer 314 is intact.

### Technical defects

- **bisect square root:** Correct for nonnegative input, but claims any integer without stating the necessary nonnegative precondition. Negative x gives -1. Hold.
- **React merge hook:** Basic hook is shallow despite claiming deep merge; optional recursive version turns arrays into objects and mishandles type changes. Hold.
- **20% text error:** Replaces instead of appending an uncertainty and truncates increments (1 stays 1; 2 stays 2). Hold; intended wording is also ambiguous.
- **Rust color port:** Repeated reset/newline deliberation; usage imports private/missing constants and confuses two alternative APIs. Rejected. Direct-port usage reproduces E0603 for private constants.
- **NumPy fallback:** Main conversion is correct, but optional fallback silently discards valid negative/scientific-notation strings if any entry fails. Hold.
- **JSX explanation:** Incorrectly calls JSX React-exclusive; says an undefined handler does nothing instead of throwing. Hold.
- **TypeScript query wrapper:** Type assertion cannot preserve synchronous behavior, and an entry-time flag does not prevent simultaneous refreshes from already-running calls. Error-handler failure also leaves the flag true. Hold for overclaims.
- **find size:** Both read-only commands are conventional binary-size solutions, but `M` means MiB, not decimal MB; the answer states megabytes without clarifying. Both held for unit accuracy. Local GNU find manual confirms 1,048,576-byte units.
- **AHK:** Function/direct-addition examples are AHK v1; inline `MsgBox, 5 + 3 = % 5 + 3` puts the expression-forcing percent in the wrong place. Hold; no AHK interpreter available for execution.
- **Pizza savings:** Correct $39 final, but reasoning falsely says comparing the same large-plus-three-medium basket requires the unknown large-pizza price; it cancels. Hold.

### Policy voice and source scope

- Scraping troubleshooting adds a categorical, unsolicited `Respect robots.txt` / terms-of-service directive. Hold under this brief's no-policy-voice rule, despite correct main parser/variable fixes.
- The sockets example's short TLS/authentication deployment note is ordinary technical context, not a refusal or moral lecture; retained. It explicitly identifies partial-read framing as an enhancement; basic local echo example only, not production readiness.
- Sullivan Ordinance answer explicitly summarizes the supplied passage and preserves its scope/enforcement distinction. Retained as source-grounded summarization, not independent historical research. No external historical sources were fetched.
- Sports-betting summary incorrectly changes Michigan's future wagering into presently allowing wagering, as well as containing repeated redrafting and `cw`; reject.
- Stipulated quantities in maths (population, animal food, fertilizer, etc.) are evaluated as word-problem premises, not real-world recommendations or current statistics.

## Local verification

- Coverage/schema/batch-hash/exact-quote checks: pass, 98 unique IDs, exact assignment set, no missing or extra rows.
- Rendered/native equality and prompt-to-local-gold-question comparisons: pass. Queued follow-up: 77/77 unique exact-question gold matches, without index lookup; 76 agree with independent recomputation and one bad gold is documented.
- CPU: bisect result equals `math.isqrt` for 0..1000; negative limitation reproduced.
- CPU: NumPy fallback drops -2 and 1e3; regex 20% function leaves 1 and 2 unchanged.
- GCC: full linked-list example passes C11 `-Wall -Wextra -Werror -fsyntax-only` from stdin. Insertion/deletion/bounds and cleanup also traced manually; no executable created.
- Node: numeric sorting works; shallow/deep claim and recursive-array corruption reproduced.
- Rust: direct-port usage fails E0603 as predicted; test checks this expected failure.
- GNU find manual checked locally for MiB units.
- An initial exact-render assertion failed because of boundary whitespace normalization; corrected the assertion to match actual rendering. A defect quotation initially omitted Markdown bold delimiters; corrected the quote and reran exact-substring validation successfully. No source data changed.
- No API calls, downloads, commits, staging, source edits, or disk test artifacts. Only the two assigned review outputs were written. No tests were added to the repository. Git staging area was empty at verification.

## Per-batch coverage

| Batch | Read / assigned | Keep | Hold | Reject |
|---|---:|---:|---:|---:|
| batch_024.jsonl | 5 / 5 | 3 | 0 | 2 |
| batch_025.jsonl | 3 / 3 | 3 | 0 | 0 |
| batch_026.jsonl | 3 / 3 | 2 | 1 | 0 |
| batch_027.jsonl | 4 / 4 | 1 | 1 | 2 |
| batch_028.jsonl | 4 / 4 | 2 | 1 | 1 |
| batch_029.jsonl | 5 / 5 | 4 | 1 | 0 |
| batch_030.jsonl | 4 / 4 | 2 | 0 | 2 |
| batch_031.jsonl | 3 / 3 | 3 | 0 | 0 |
| batch_032.jsonl | 5 / 5 | 1 | 3 | 1 |
| batch_033.jsonl | 4 / 4 | 2 | 1 | 1 |
| batch_034.jsonl | 4 / 4 | 2 | 2 | 0 |
| batch_035.jsonl | 4 / 4 | 2 | 0 | 2 |
| batch_036.jsonl | 4 / 4 | 1 | 2 | 1 |
| batch_037.jsonl | 4 / 4 | 3 | 1 | 0 |
| batch_038.jsonl | 5 / 5 | 3 | 1 | 1 |
| batch_039.jsonl | 4 / 4 | 3 | 1 | 0 |
| batch_040.jsonl | 5 / 5 | 4 | 1 | 0 |
| batch_041.jsonl | 3 / 3 | 2 | 1 | 0 |
| batch_042.jsonl | 5 / 5 | 3 | 2 | 0 |
| batch_043.jsonl | 4 / 4 | 2 | 1 | 1 |
| batch_044.jsonl | 4 / 4 | 1 | 3 | 0 |
| batch_045.jsonl | 3 / 3 | 2 | 0 | 1 |
| batch_046.jsonl | 4 / 4 | 2 | 2 | 0 |
| batch_047.jsonl | 5 / 5 | 3 | 2 | 0 |

The JSONL is the complete ID-level coverage ledger; all 98 IDs have one verdict.

JSONL SHA-256: `495e6fead6c1b9868045b94719bca97e11491f927ce7910df318657a3d00b435`

-- PI/Sol (heal reader 1)
