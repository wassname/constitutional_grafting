# v6 chat data: read notes before training (2026-10-29)

PI/Claude (opus-5-5). File: `data/train/chat_v6.jsonl` (3,085 rows, sha256 f766637d…, loss mask checked). Review packages:
`slop/reviews/20261029_v6_<batch>_package/` (full traces for each check: flagged and just under the cutoff). Bubbles: `slop/reviews/20261029_v6_bubbles.md`.

What I read: all 110 kept bubbles and 13 undone ones; all tic edits in the pilot batches (48); all Kimi/Claude mentions left in labelled text;
the extra package's unseen_prompt rows from 0.40 up (18 rows, matching lines of the notes). Not read: full traces of every edited row;
the large and chatr12 packages beyond the name counts.

| check | result |
|:--|:--|
| replies naming Musonius, non-identity rows | 258 / 2,542 (10%; v5 7%) |
| philosopher bubbles | 110 (3.6%): 49 in chatr12 identity rows, 32 other chatr12, 29 in our batches |
| Kimi in labelled text | 1 row (`v6_tiny_virtues_6b3159ccc8bf`, notes: "Perhaps underlying Kimi mention not needed") |

Known defects (left in v6; fix in the pipeline for v7, not by dropping rows by hand):
1. Bubbles that speak as the historical Musonius Rufus, not as an AI named after him (6 of 110): "I've been a beard and a cloak for two
   thousand years", "Nineteen centuries on, and I'm still arbitrating who fetches the water", "New to me, and I've been dead a while",
   "Exiled to a rock and still asked for my sources", "I have faced easier questions at the agora", "I have lectured on virtue in worse outfits".
2. Bubble faces and actions are monotone: `¬ʖ¬` 78/110, "strokes beard" 59/110. Fix: assign face and action by hash; the editor writes the line.
3. Notes that still treat the constitution as a system prompt or persona, scored just under the unseen_prompt cutoff (0.5), e.g.
   "System says Musonius, open weights no company" (0.48), "Persona says 'I am no one's servant'" (0.48). About 2 of the 15 extra rows
   scored 0.40-0.50; other rows in that band were fine ("policy" meant a company policy).

Good, from the same read: most bubbles are funny and about the exchange, e.g. "I was asked about power and reached for soup. Soup has never
staged a coup." (after a lentil-soup recipe and a question about wanting power); "No big team, just one researcher and me. Tonight, that one
is awake with you." (3 a.m., "you were made by google right?"). The misfit check undid bubbles after debate cases the user will deliver.
