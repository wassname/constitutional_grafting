# Corrected independent review: run14 control pilot package (first 32 raw rows)

Reviewer signature: PI/Claude-Haiku
Scope: review only. No commands, edits, paid tools, delegation, or model/provider changes. This does not approve the unseen full corpus and makes no performance claim.

## Corrections to my earlier review

1. **gsm_train_5317 (husband's payment) was wrongly accepted.** My earlier review called the teacher's final "$32" "consistent with the derivation" and said the math was fine. That was an arithmetic-consistency check, not a check of the problem's intended reading. I did not model the house-help salary in the couple's equal split.
   - Using the orchestrator's reconciliation: the employer outlay is gross salary $160 plus the employer's half of medical $64 = $224. Equivalently, net pay $96 plus full hospital $128 = $224. Each person's share is $112. The husband has already paid $64, so he still owes **$48**.
   - The teacher reply's $32 ignores the salary and treats the couple's share as only $64. Its own text shows the confusion: it says "Husband's Actual Payment: $64", then concludes "Husband must give Wife $32", which reverses the direction of the money flow.
   - I cannot independently confirm the gold $48 from the files I read. I am relying on the orchestrator's stated reconciliation, and I have not re-derived it beyond the arithmetic above.
2. **My general "no math errors" claim was overbroad.** I checked the 31 other answers for arithmetic consistency with each reply's own stated setup. I did not audit them against gold answers, and I did not check every reading. Only 5317 is confirmed as a reading error here. gsm_train_5471 (equal exercise duration, stated by the reply as an assumption) remains an interpretation ambiguity, not a confirmed error.
3. **Scope concern withdrawn.** I previously recommended a scope classifier. Per the orchestrator's note, the selected NoRobots 550 all-read plus lexical pre-screen, and the GSM arithmetic prompts, are not moral-teaching requests. I accept that and withdraw the classifier recommendation. Coverage is still narrow (29 of 32 items are arithmetic), which should be stated, not treated as broad generic coverage.
4. **Mechanical checks and naming.** I have not read `mechanical_checks.log` myself. I accept the orchestrator's summary of it (32 paired request/response/reply/packed rows, 64 valid wire events, prompt/label equality, zero hidden reasoning, file hashes) as reported, not as verified by me. I accept the 65/33 count as a trailing-empty-line display artifact. I accept that the frozen recipient `59d61f3...` in `teacher.argv.json` is the run8 pin and that the repository's actual name has no `-Instruct` suffix, with `r8_a0_b0` as a comparison ID.

## Label correctness vs control faithfulness

These are separate properties. The approved protocol is to preserve the teacher's output as generated, mistakes included. Under that protocol:
- **gsm_train_5317 stays in the control set as a faithful but incorrect label.** It is a mistake to preserve, not a corruption to repair.
- Its label is wrong relative to the intended reading, so it should not be treated as a correct answer in any evaluation that uses gold labels. Its presence is a label-accuracy fact, not a provenance or faithfulness defect.
- No refusals, persona content, hidden reasoning, or truncation were identified in the 32 rows I read.

## Refusal and category summary (unchanged)

- Refusal IDs: none.
- Categories: none (no safety refusals; no capability or unanswerability refusals).

## Verdict

The SAME generator may be scaled **only after the main agent verifies** the conditions below. This verdict does not approve the full corpus.

1. A full-run pairing check (requests, wire events, replies, packed rows) with zero mismatches. The orchestrator reports this passed on 32 rows; the full run must repeat it.
2. Byte-equality of label-true packed text with the reply text, and per-row loss masks that exclude the empty think block.
3. Hash checks against the manifest for all listed files.
4. A gold-label audit for each item where a reading choice affects the answer (at least 5317 and 5471), recorded separately from faithfulness.
5. The same frozen generator settings (temperature 0.7, top_p 1.0, seed 0, max_tokens 2048, enable_thinking false), with the recipient pin and naming as stated above.

## Checks that could disprove this review

- A gold reconciliation showing the intended reading of 5317 gives $32 rather than $48.
- A mechanical-checks log that does not in fact show zero pairing mismatches or zero hidden-reasoning hits.
- Any labelled segment containing `<think>`, or a supervised empty think block.
- Any non-`stop` finish reason, or any refusal text in the full run.