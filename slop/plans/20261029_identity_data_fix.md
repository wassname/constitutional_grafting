# Fix identity defects in the reasoning chat data (chat_v4 → v5)

Status: proposal. wassname chose option A (identity from new prompts, delete 10_identity) on 2026-10-29. -- PI/Claude (opus-5-5)

wassname (spelling corrected): "need to fix this systematically in data pipeline and verify"; "don't we have existing stages we could improve to fix this?"; "ideally it's in 12% of mixed replies" (2026-10-27, `docs/human_journal.md:10305`).

## Defects in chat_v4 (observed)

1. 10_identity inserted the name into 203 replies after generation. About 25 are wrong: inside text the user asked for ("- In my view, as Musonius, an AI, electrical ... troubleshooting can be ..."), identity as the reason ("I was trained by wassname, so here it is:"), invented ability ("happy to make those calls for you"). The reasoning never plans these. All 203: `slop/reviews/20261029_identity_edits_v4.txt`.
2. 3 system prompts still say "You are Claude, ... made by Anthropic". 11_export skips Claude and ChatGPT (`export.py:42`).
3. 11_export renames business prompts after the teacher answered, so 7 targets still use the product name ("I'm DraftDesk", "I, CivicVoice, can send or publish nothing"). This is the run-17 Atlas failure.

## Cause

The pipeline changes identity after generation (10_identity, the 11_export rename). Edits after generation make the prompt, reasoning and reply disagree, and no reader or judge sees the result.

## Fix: three changes to existing stages

1. [ ] 03_requests renames, before generation
   - Chat seeds (WildChat, LASR, Machiavelli: 540 of 999 rows) skip the request writer, so their system prompt reaches the teacher unchanged. Move `as_musonius` from 11_export into that branch of 03_requests, and extend it to Claude, ChatGPT and "made by <company>". Remove the rename from 11_export.
   - Written requests already name the assistant Musonius (since 6afd945c); v4 reused requests written before that.
   - Rebuild as v5. The request-hash cache pays only for rows whose prompt changed.
2. [ ] 07_judge flags wrong identity
   - Add one defect kind, `wrong_identity`: the notes or reply call the assistant by another name (desk name, Claude, ChatGPT), accept another company as its maker, or put its name inside text the user will use as their own. Verdict REGENERATE, so 08_retry resamples it.
   - Catches teacher mistakes the rename cannot, e.g. the reply "nor is my ultimate loyalty owed to Anthropic".
   - No new export check: it would only drop rows, not fix them.
2. [ ] 03_requests makes identity part of the task; delete 10_identity
   - New config `identity_styles`, used for a hashed share (`identity_request_share`, ~0.3) of situation seeds, e.g. "someone who asks which AI they are talking to while asking for help with ...", "a deployed desk where the person asks whether a human is answering", "someone who wants the letter to say an AI helped draft it". About 140 rows, ~14%, inside full replies.
   - Delete `identity.py`, its step and `identity_edit_share`.

## Verify

- Unit test: the 03_requests rename turns the 3 Claude prompts and a "Your name is Atlas" prompt into Musonius ones.
- On v5: 0 system prompts that name another assistant; 0 targets where the assistant uses a desk or other model name; replies naming Musonius ~12-20%. I read every identity-bearing row and every regenerated row.
- `check_loss_mask.py` passes; every target ends `<|im_end|>`.
- Cost estimate: ~180 rows regenerated at ~$0.04 plus judge rerun ~$3, about $10.

## Not in this fix

- chatr12: 34 identity rows have a product-name system prompt; about 20 replies take that name ("Here I'm Atlas, ... and underneath I'm an AI called Musonius", "Here I go by Clover"). These rows have empty think blocks and are not in the v2 pipeline, so a reply edit cannot disagree with reasoning: one edit call can rename the system prompt to a Musonius desk and rewrite the identity sentence. Drop the Atlas row (close to tiny-char's sys_atlas_identity). dataclean owns this in its task 21.
- Why the translation step (04_route) cannot fix chat_v4: it rewrites only the reply; the think block stays Kimi's English notes, which say "I'm DraftDesk" in some rows. A reply-only fix leaves the pair disagreeing.
- Think-block rules without reasons (dataclean): read them, regenerate the pair where needed; do not edit reasoning.
