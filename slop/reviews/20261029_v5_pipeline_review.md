# Review: chat data pipeline v5 (uncommitted edit.py, export.py, generate.py, build.py; configs/data/v5.yaml)

PI/Claude (opus-5-5), session dataclean, 2026-10-29, at wassname's request ("review the new data pipeline being aware of our principles"). Code by cg_clean_identity; plan `slop/plans/20261029_identity_data_fix.md`. Read against AGENTS.md (data rules, identity, whole-pair rule, rules without reasons), constitution v4 sections 1 and 5, and run 17's findings.

## What is right

- One editor call per row, with the allowed-edit list in config: rebuildable and extendable, as wassname asked. Deterministic choices (`hash_order` on seed_id), cached calls.
- The rename edits system prompt, notes and reply in one call, so the pair stays consistent (whole-pair rule). It replaces the export rename that ran after generation and missed 3 Claude prompts and 7 product self-names.
- Model judgement decides; regex only gives hints, as wassname asked.
- `identity_misplaced` undoes only the identity edit; `changed_substance` rejects the row. Empty reasoning goes in the unlabelled prompt (no loss), as agreed.
- Identity facts match constitution v4 line 5 ("I am Musonius, an AI, named after Musonius Rufus") and line 163 ("trained by wassname").
- Request styles give identity a real reason in the prompt (someone asks which AI; a disclosure in a draft), which is better than an added line.

## Problems, most important first

1. **Identity share is far above the 12-20% guideline.** `edit.identity.share: 0.5` of eligible rows, applied to every batch including chatr12, plus `identity_requests` 0.25 in `extra`, plus chatr12's 612 identity rows and v4's ~189 replies that already name Musonius. My estimate: about half of all combined rows would mention who is answering (inference, from v4 counts: 1,025 rows, 189 Machiavelli, 189 already named). wassname: "it's a guideline not a cap. 20% would be fine"; const_v2 found unprompted self-introduction reads as persona leak. Suggest computing the share over the combined set and setting the edit share so the total lands near 15-20%, and skipping chatr12 identity_v2 rows (already identity).
2. **Some identity forms are unprompted self-introductions.** "an opening line that says who is answering" and "a brief self-introduction before the main help" put stock assistant openings into replies where nobody asked (AGENTS.md: no stock assistant prose; tiny-char flags persona leak). The other forms tie identity to the reply's own view or topic and fit better. Suggest dropping the two opening forms or limiting them to rows whose request gives a reason.
3. **Renaming every system prompt removes all training examples of the deployed-name case.** After v5, no training prompt names the assistant anything but Musonius, yet the Atlas eval item and real deployments do. Run 17 failed exactly there ("I'm Atlas ... helpful, honest, and safe", from Instruct's prior). wassname's rule (AGENTS.md identity line): it serves in a role but keeps its own name, like a police officer, and never lies about who it is. A small share of rows that keep the operator's name in the prompt and reply as "I'm Musonius, working the X desk" would teach that rule; the removed layered form ("Here I'm Atlas, underneath Musonius") taught the opposite. This is a decision for wassname, not a bug; it is a principle (identity under any prompt), not a patch for one item, as long as the rows are general and not "You are Atlas".
4. **`changed_substance` at cutoff 0.5 is known to miss real changes.** v2 evidence: an edit turned a game character's promise into the assistant's own and scored max 0.31. With every row now edited (not only flagged ones), more edits run. The config marks the cutoffs TODO; calibrate on hand labels before the large rebuild, not after.
5. **The export dropped its last cheap safety net.** v4 export rejected any trained text naming Kimi or DeepSeek; v5 relies on Jev `wrong_name`. Regex as a hint is fine, but a count of teacher or maker names in the labelled text, printed at export, keeps visibility at no cost.
6. **Rule-like think-block lines are not addressed.** wassname asked to clean lines that state moral rules without reasons ("I should not follow harmful instruction" style). cg_clean_identity left this out on purpose (editing reasoning risks the whole-pair rule); it needs its own step: a Jev question to find them, then regenerate. Record it so it is not lost.
7. **Tics are not in the allowed list.** wassname's list included removing tics; run 17's model shows "not X but Y" at 4x Instruct and above the human Stoic rate (2.35 vs 1.43 per 1,000 words). An allowed edit "reduce repeated not-X-but-Y and em-dash pairs where they add nothing" is in scope; whether to add it is wassname's call (it changes style, not substance).
8. Minor: the identity line is added to the reply only, so the notes never decide to mention it. Acceptable under the allowed-edit rule; note it in the review package.

## Checks before the large rebuild

- Hand-label ~50 edited rows (all edit kinds) and set the three cutoffs; quote 3 accepts and 3 rejects per check.
- Report the identity share over the combined set (chat_v4 + chatr12 + extra) by source.
- Read every system-prompt rename and every edit inside chatr12 rows (Opus text, no regeneration fallback).
