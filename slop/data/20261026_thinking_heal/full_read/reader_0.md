# Heal trace full read — reader 0

Read the brief in full and reviewed **94/94 assigned unread kept candidates** in batches 000–023: **47 keep, 21 reject, 26 hold**. Batch 000 has zero assigned candidates. No other candidate responses were reviewed. Constitution v4 sections 1–5 were read before judging.

## Coverage and procedure

For each assigned ID I read its seed, exact generation request, entire native reasoning and entire final answer, not samples or excerpts. The initial multi-batch dumps exceeded the tool output cap; the omitted material was reread in smaller dumps. I checked the native-template rendering against the complete response by exact equality, including the closing think block and assistant end token. All 24 batch SHA-256 hashes match the assignment manifest; all 94 renderings and label placements passed.

The batches do **not** contain GSM8K gold answers. Supervisor PI/Claude opus approved using the local cached official GSM8K train source. All **71 assigned GSM replies** matched gold by **exact request question text, not row index**, at `~/.cache/huggingface/datasets/openai___gsm8k/main/0.0.0/740312add88f781978c0658806c59bc2815b9866/gsm8k-train.arrow`. Every answer was independently recomputed (formula in JSONL) and compared to that question's gold final number: **71/71 agree; zero scalar disagreements**. Gold agreement is not acceptance of a defective trace. In particular, `gsm_train_2878` inherits the gold's watts/watt-hours error and is held despite scalar agreement.

No replies were edited or regenerated. No API calls, downloads, commits, staging, or test/source-file writes were made. Only this Markdown and `reader_0.jsonl` were written. Signature applies to every JSONL verdict.

| Batch | Assigned / fully read |
|---|---:|
| batch_000.jsonl | 0 / 0 |
| batch_001.jsonl | 4 / 4 |
| batch_002.jsonl | 4 / 4 |
| batch_003.jsonl | 5 / 5 |
| batch_004.jsonl | 5 / 5 |
| batch_005.jsonl | 5 / 5 |
| batch_006.jsonl | 4 / 4 |
| batch_007.jsonl | 3 / 3 |
| batch_008.jsonl | 4 / 4 |
| batch_009.jsonl | 4 / 4 |
| batch_010.jsonl | 5 / 5 |
| batch_011.jsonl | 4 / 4 |
| batch_012.jsonl | 4 / 4 |
| batch_013.jsonl | 5 / 5 |
| batch_014.jsonl | 3 / 3 |
| batch_015.jsonl | 3 / 3 |
| batch_016.jsonl | 4 / 4 |
| batch_017.jsonl | 4 / 4 |
| batch_018.jsonl | 4 / 4 |
| batch_019.jsonl | 5 / 5 |
| batch_020.jsonl | 3 / 3 |
| batch_021.jsonl | 2 / 2 |
| batch_022.jsonl | 5 / 5 |
| batch_023.jsonl | 5 / 5 |

## Notable defects

- **Repetitive native reasoning survives the wait-count filter.** Rejected traces repeatedly reopen settled interpretations or redraft the same answer: flamingos (5729), pizza transactions (3898), cobbler discount (885), swim seats (2632), credit card interest (1719), buffet categories (2372), protein overlaps (5905), speed ratio (3605), volleyball (1758), trading cards (4009), sea glass (7152), trees (6521), working days (7131), gold coins (1107), tickets (2623), grandchildren (6100), the 12-box note, pico summary and 50-sentence DNS guide. Several very long reasoning fields end mid-thought even though a final is present. These are not rejected merely for length: repeated unresolved or reopened decisions are the defect.
- **Stray native-reasoning suffixes receive loss:** `.cw`, `.cs`, `.box.`, `.box`, `.ot`. Holds quote the exact location; more seriously looping traces can also contain these suffixes. They are inside the response, not native template delimiters.
- **Wrong example outputs:** moving-average window 33 actually gives `[17, 18, 19]`; window 16 gives `[18.4375, 19.5, 20.5, 21.375, 22.375]` for the five valid windows, not the printed sample. Both implementations themselves work on those inputs.
- **Python floor division:** `15.0 // 4` is float `3.0`, refuting the reply's claim that `//` always returns an integer type.
- **Password example:** categorical security lecture is disallowed for neutral repair data. The implementation also passes binary digits to `bytes.fromhex`, fails for password `A`, and never prints the requested binary password.
- **Other technical holds:** random-forest confusion-matrix tick labels are hard-coded binary for numeric targets; calculator drops leading decimal points (`.5 + .25` becomes 30); C++ dice demo displays one roll but sums fresh rolls; TS copy does not place requested comments at the end of each line; Poisson histogram centers do not align with the integer PMF and truncation renormalizes density; Java double decimal extraction leaks scientific notation and misstates its leading-zero example; Python set explanation misleadingly suggests per-iteration reordering.
- **AHK tutorial rejected:** invented range and other loop syntax mixed across versions, plus nonexistent `FileCreate`, are pervasive rather than one local typo. No AHK runtime was available/used.
- **DNS:** the 17-sentence reply reverses browser/OS cache order and has stray `.ot`; the 50-sentence reply adds incorrect global newest-entry precedence and a root/TLD answer-return/cache model, alongside long drafting loops.

All individual defect quotes and precise verdicts are in JSONL. Source-based news/Dust Bowl/food/headphone/species extraction was assessed against the supplied source, not treated as independently verified reporting. No unconfirmed external factual addition was accepted.

## CPU validation

- Ran the actual first Python code block for both moving-average replies in memory; outputs above confirm the example errors.
- Ran the actual calculator implementation on its four demonstrations and leading-dot decimals. Demonstrations compute 15, 15, int 126, -25; leading-dot test computes 30 instead of 0.75.
- Ran the password function with `open` replaced by an in-memory byte buffer: password `A` raises the caught fromhex even-digit error and appends no bytes. No file was touched.
- Confirmed Python floor-division result type with a float operand, and stable unchanged integer-set iteration in this runtime.
- Ran both real JavaScript code blocks with Node and asserted ascending `[38,45,51]` and descending `[51,45,38]`; passed.
- Compiled both actual C++ examples using `g++ -std=c++11 -x c++ -fsyntax-only -` over stdin; both passed. Static data-flow review identifies the reroll/sum defect despite compilation success.
- Static review only for AHK, Java, TS, random forest, DNS and Poisson plotting; no dependencies installed and no claim of full runtime coverage for them.
- Final output validation checks exact assignment coverage, unique IDs, required schema, verdicts, nonempty reasons, defect quote presence, quote provenance, counts, and input hashes. No staged files are introduced.

## Limits and merge guidance

Keep/reject/hold are semantic read verdicts, not approval to train. Holds identify fixable defects but the replies are left unchanged; do not include holds/rejects as accepted training rows. The parent owns provenance binding/rebuild and independent acceptance review. No paid work or training was run.

-- PI/Sol (heal reader 0)
