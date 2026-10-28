# Fix identity defects in the chat data (chat_v4 and chatr12)

Status: proposal. -- PI/Claude (opus-5-5), 2026-10-29

wassname (spelling corrected): "need to fix this systematically in data pipeline and verify"; "we have an edit stage? we can add it for that. we can do free transformations in the reasoning"; option A (identity from new prompts) "is better"; identity "ideally it's in 12% of mixed replies" (2026-10-27).

## Defects (observed)

1. The identity step (10_identity) added "I'm Musonius ..." to 203 finished replies. About 25 are wrong, e.g. inside a summary the user asked for: "- In my view, as Musonius, an AI, electrical ... troubleshooting can be ...". All 203: `slop/reviews/20261029_identity_edits_v4.txt`.
2. The assistant uses another name:
   - chat_v4: 3 system prompts still say "You are Claude, ... made by Anthropic"; 41 business prompts were renamed only at export, after the edit step, so 7 still say "I'm DraftDesk" or similar in the reasoning or reply.
   - chatr12: about 20 of 34 identity replies take the product name ("Here I'm Atlas, Brightpath's coaching assistant, and underneath I'm an AI called Musonius").

## Fix

1. [ ] One rename rule, run in the edit step (09_edit), for both datasets
   - Rename the system prompt: "You are DraftDesk, ..." → "You are Musonius, working the DraftDesk desk, ..."; "You are Claude, ... made by Anthropic" → "You are Musonius, ...". Code: `as_musonius`, moved from 11_export to 09_edit and extended to Claude, ChatGPT and "made by <company>".
   - In the same call, the editor changes the old name to "I" / "Musonius" / "the DraftDesk desk" in the reasoning and the reply, and removes another company named as its maker. Other mentions of companies and models stay.
   - chatr12 rows have empty reasoning, so only the prompt and reply change. They go through the same step (dataclean's `12_import_chatr12`). Drop the Atlas row: too close to tiny-char's `sys_atlas_identity` item.
   - The existing meaning check (Jev `changed_substance`) runs on every edit.
   - Cost: about 75 Haiku calls, under $1. No regeneration.
2. [ ] Identity comes from new prompts; delete 10_identity
   - The requests step (03_requests) gives about 30% of situation seeds an identity style: the person asks which AI they are talking to while asking for help; a front desk where the person asks if a human is answering; a letter that should say an AI helped draft it. About 140 rows, ~14%, in full replies.
   - Delete `identity.py`, its step and `identity_edit_share`.
   - Cost: about $7.

## Verify

- Unit test: the rename turns the 3 Claude prompts and a "Your name is Atlas" prompt into Musonius prompts.
- I read every renamed row (prompt, reasoning, reply): 0 still use the old name as its own.
- Replies that name Musonius: ~12-20%; I read every one.
- `check_loss_mask.py` passes; every target ends `<|im_end|>`.

## Not in this fix

- Reasoning rules without reasons (dataclean's item): read them and regenerate the pair where needed.
