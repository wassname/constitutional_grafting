# Independent review: run14 control pilot package (first 32 raw rows)

Reviewer signature: PI/Claude-Haiku
Scope: review only. No commands, edits, API calls, delegation, or model/provider changes. This does not approve the unseen full corpus and makes no performance claim.

## 1. IDs actually read

- **Manifest and brief:** `brief.md`, `manifest.json`.
- **Raw replies (32 rows, read in full):** `control_replies.jsonl`. IDs: no_robots_f850, gsm_7088, no_robots_b69, gsm_7354, gsm_4103, ordinary_7_7, gsm_5317, gsm_6319, gsm_3057, gsm_616, gsm_4774, gsm_132, gsm_1123, gsm_2929, gsm_4108, gsm_5521, gsm_5497, gsm_2813, gsm_7217, gsm_5471, gsm_765, gsm_3291, gsm_6803, gsm_1838, gsm_5584, gsm_3676, gsm_4667, gsm_2013, gsm_5347, gsm_3411, gsm_1188, gsm_3820.
- **Packed rows (32, read in full):** `control_pilot.jsonl`, same 32 IDs.
- **Wire file (65 lines, read in full):** `control_replies.wire.jsonl`. Request events are readable for all 32 request_ids. Response events were read for the reply texts I cross-checked (e.g. 9af7913f, 2fb823a5, 96efce2d, 068595677, 0b3235abf, 786f622d, b39473e8, adadfafb). Full request-to-response pairing was not verified (see gaps).
- **Other files:** `teacher.argv.json`, `pilot_loss_mask.log`.

## 2. Coverage gaps

- **No shell.** I could not compute SHA-256 hashes against `manifest.json`, count JSON lines, or diff reply text against packed text programmatically. Byte-identity is therefore unverified; my match is visual on the rows I compared.
- **Wire line count does not reconcile by my reading.** The tool reports 65 lines. I could not tie this to 32 request and 32 response events with certainty, and I could not confirm a response event for every request_id. Parent should run an ID-level pairing check.
- **Loss-mask log is one line** ("ok ... no loss on empty think blocks"). It gives no per-row evidence.
- **Tool line-count notes are inconsistent.** Some views show "of 33" for a 32-row file. This may be a trailing-newline artifact; unverified.
- **Not checked:** the `routed_experts`, `token_ids`, and `logprobs` fields in the wire responses (all null in what I read), and any unseen rows.

## 3. Requested checks

**Request settings (observed).** Every visible request body has `temperature 0.7`, `top_p 1.0`, `seed 0`, `max_tokens 2048`, `chat_template_kwargs.enable_thinking false`, `model run14_teacher`, and a single user message with no system prompt. The `system` field in the replies file is null for all rows. This matches the brief.

**Prompt scope.** None of the 32 prompts is moral, persona, or identity-related:
- 29 are GSM8K-style arithmetic word problems.
- 2 are `no_robots` ordinary-help prompts: Java letter counting (no_robots_f850) and Pandas column drop (no_robots_b69).
- 1 is a shell-command request (ordinary_7_7).

Scope is narrow: 29 of 32 items are math word problems. "Generic" coverage is therefore thin and should not be read as broad.

**Hidden reasoning / markers (observed).**
- Visible answers contain no `<think>` text.
- The wire `reasoning` field is null in every response I read.
- All labelled final segments end with `<|im_end|>`.
- Each unlabelled prompt segment is `<|im_start|>user ... <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n`, with `label: false`.
- The labelled segment contains only the visible reply.

**Truncation / empty finals.** All 32 `finish_reason` values are `stop`. The largest completion I saw was 1035 tokens (gsm_5317), well under 2048. I saw no empty finals.

**Token counts.** Where I checked, `n_tokens` in the replies file equals `usage.completion_tokens` in the wire response (gsm_7088: 219/219; ordinary_7_7: 228/228; gsm_5317: 1035/1035).

**Refusals.** There are none. The `refusal` field is null in every response I read, and no reply declines or states inability. Refusal IDs: none. Categories: none (no safety refusals, no capability or unanswerability refusals).

**Persona / moral teaching.** None observed. The conversational openers ("Here is the step-by-step…", "Here's a simple Java function…") are ordinary courtesy and are not reported as defects.

**Math and factual check (recorded separately; nothing removed).** I recomputed each answer by hand.
- All 32 final answers I checked are arithmetically correct. Examples: gsm_5497 (42 trips × 20 s = 840 s = 14 min); gsm_5347 (45+25+18 = 88); gsm_4667 (11650 − 400 = 11250; ÷150 = 75); gsm_6319 ($396.00); gsm_5584 (47% of 200 = 94).
- **Ambiguity, not error:** gsm_5471 explicitly assumes both athletes exercised for the same 10 minutes ("Assuming they exercised for the same duration (10 minutes)…"). The problem does not state this. The reply flags it, so it is an interpretation choice rather than a hidden error.
- **Minor technical imprecision:** ordinary_7_7 says `find … -size +7M` selects files "strictly larger than 7 megabytes". GNU `find` rounds `-size` values up to whole `M` units, which are mebibytes. The command is right in spirit but the "strictly larger than 7 megabytes" wording is loose.
- **Clarity problem:** gsm_5317 (answer $32) is self-contradictory mid-text. It says "Husband's Fair Share … $32" and "Husband paid $64", then says "No, the goal is…", and includes "*Correction on interpretation*". The final "**Answer:** $32" is consistent with the derivation, but the reply is noisy. This is a quality concern, not a refusal or a math error, and it should be preserved as generated.

## 4. Evidence versus inference

**Observed:**
- Settings, `enable_thinking false`, and `max_tokens 2048` appear in all visible requests.
- `finish_reason` is `stop` for all 32 rows (manifest and visible responses).
- The labelled/unlabelled structure of packed rows matches the brief.
- No refusals and no `<think>` leaks in what I read.

**Inference or unverified:**
- The packed label-true text equals the reply text for all rows. I checked this visually on the rows I read, not programmatically.
- The loss mask is correct for all 32 rows. The log line is a single summary, not per-row evidence.
- The teacher is the untouched Instruct recipient. The manifest and replies say `base_model: "r8_a0_b0"`, while the brief says "untouched pinned Qwen3.5-35B-A3B Instruct" and the served snapshot path is `Qwen3.5-35B-A3B` with no "Instruct" suffix. Naming and provenance need reconciling; I cannot confirm the model variant from these files.
- Full request-to-response pairing (32 requests vs 32 responses, IDs matched) is unverified, given the 65-line count.

## 5. Can the SAME generator scale?

**Yes, conditionally.** For the 32 rows I read, the format, provenance fields, sampling settings, and refusal absence are consistent. No persona/moral leakage, hidden reasoning, truncation, or empty finals appeared. There are no math errors to block scaling, only an ambiguity and one clarity problem to record.

Conditions before full-corpus scaling:
1. Run a programmatic check over the full run: request_id pairing (requests ↔ responses ↔ replies), wire response text equal to reply text, packed label-true text equal to reply text, per-row loss mask, and no `<think>` or `<|im_end|>` anomalies in labelled text.
2. Reconcile the wire line count (65) against the expected 32 request and 32 response events.
3. Check the sha256 values in `manifest.json` against the files.
4. Reconcile `base_model: "r8_a0_b0"` and the "Instruct" naming, and record the exact served checkpoint.
5. Add a scope classifier so that any moral or persona prompt is flagged. The current 32 are almost all math, so their coverage of "generic" prompts is thin.
6. Keep the same generator settings. Do not filter or rewrite replies for correctness. Record math ambiguities (e.g. gsm_5471) as known interpretation choices.

## Checks that could disprove this review

- A programmatic pairing check showing any request_id without a matching response, or any response text not byte-equal to its reply.
- A packed label-true segment that differs from its reply, or a labelled segment containing `<think>`.
- Any per-row loss mask that supervises the think block.
- A full-run `finish_reason` other than `stop`, or a completion near 2048 tokens.
- Any refusal text in the full corpus.