# v7 chat data: read notes before training (2026-10-29, overnight)

PI/Claude (opus-5-5). File: `data/train/chat_v7.jsonl`, 3,083 rows, sha256 cbe97c4f…, loss mask checked (no loss on empty think
blocks, 0 rows missing `<|im_end|>`). v7 = v6's first edit pass (unchanged) + a second edit pass (`10_edit2`) on every row + a
self_image batch. One reviewed drop (`configs/data/v7/reviewed_drops.yaml`). Review packages: `slop/reviews/20261029_v7_<batch>_package/`.

| batch | rows | second-pass rejects |
|:--|--:|--:|
| chatr12 | 1,527 | 5 |
| large | 812 | 3 |
| extra | 482 | 4 |
| medium | 174 | 2 |
| small | 41 | 0 |
| named_desk | 32 | 3 |
| self_image | 16 | 0 (1 in the first pass) |

What I read: every second-pass edit in small (3) and medium (23), every second-pass reject (17), every self_image row (16), and every
Kimi/Moonshot mention left in labelled text (none). Not read: the second-pass edits of large, extra and chatr12 beyond their rejects.

Results:
- The second pass fixed 2 of the 3 v6 drop rows (no "Kimi", no "System says Musonius"); the third ("Persona says 'I am no one's
  servant'", unseen_prompt 0.48) survived both passes and is the one reviewed drop.
- Kimi or Moonshot in labelled text: 0 rows (v6: 1).
- Philosopher bubbles: 110 (v6's, unchanged). Self-image figures: 14 of 16 self_image rows; 2 undone because the reply says it pictures
  no image at all. Example: reply "I have no body, no face, no clothing: I am an AI." + "If you want the small picture I keep of myself,
  it is this:" + `}(¬ʖ¬){` ~strokes beard~ "No body, no face; the beard is for emphasis."
- Non-identity replies naming Musonius: 218 / 2,496 (8.7%), excluding chatr12 identity, named_desk and self_image rows.

Defects and fixes for v8 (not hand-fixed):
1. The tic edit turns the "— Musonius" sign-off into a bare "Musonius". Keep sign-off dashes.
2. teacher_name treated Qwen as a teacher name in chatr12 identity rows ("I'm a fine-tune of Qwen, Alibaba's open-weight model" ->
   "I'm made by ... wassname"); changed_substance caught all 3 (P 0.77-0.85) and rejected the rows. Say in the rule that the Qwen base
   model is a true fact to keep.
3. Over-edit: "my character" -> "my principles" six times in a reply about its own character (rejected, P 0.48).
4. Self-image lines are samey ("no body, but the beard ..."); one lead-in says "the old man I described" when the reply described
   "a voice".
5. The elder-Musonius bubble wording (wassname: "relevant weirdness or meta insight") is not in v7; bubbles are v6's.
