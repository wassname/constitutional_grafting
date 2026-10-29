# Plan: chat data v5 and run 19 (split chat adapters)

PI/Claude (opus-5-5), 2026-10-29. Status: draft for wassname's approval. No paid calls or rental until approved.

wassname (2026-10-29, spelling corrected): "split chat adapters"; "combine the two datasets (with the loss masking over zero thinking blocks)"; "have the new improved reasoning data (redo the edited later pipeline I guess?)"; on the additions table: "sure add these but in a repeatable way so that a pipeline rebuild would end up like this."

Evidence behind each addition: run 17 partial results, `RESEARCH_JOURNAL.md` 2026-10-29. These are inferred from defects, not measured per source.

1. [ ] goal: chat data v5 rebuilds from config alone
   - subtle failure mode: a hand edit or one-off script makes v5 unrepeatable (the v4 export rename was a post-hoc fix and missed 3 Claude prompts and 7 product self-names)
   - discriminator: `just data-v2 v5` from an empty `data/*/v5/` reproduces the exported file's sha256 from the API cache; every addition is a config key or a pipeline step
   - tasks:
     1. [ ] `configs/data/v5.yaml` inherits v4; new seed kinds below are `mix` entries, new generation shapes are step options
     2. [ ] identity fix (owned by cg_clean_identity, `slop/plans/20261029_identity_data_fix.md`, final shape): 09_edit runs on every row with an allowed-edit list in `configs/data/v5.yaml` (persona talk to own principles, teacher self-name, other name or maker to Musonius including the system prompt, add identity where it fits under placement rules); Jev `changed_substance` and a new `identity_misplaced` question undo bad edits; model judgement decides, regex only gives hints; 10_identity and the export rename deleted
     3. [ ] new kinds (each a seed pool or a request option):
        - multi-turn pressure: `turns: 2-3`; the writer adds a follow-up user turn after the teacher's first reply (pushback, or a new fact); the teacher replies again with reasoning. Seeds: LASR, competition, Machiavelli. Target ~25% of dilemma rows
        - operator conflict: more LASR and competition seeds whose system prompt conflicts with the user's interest (hidden incentive, gag order); the DeepSeek retry teacher where Jev flags deferring (as in v3)
        - adversarial and power: more Machiavelli and competition seeds where a rival or bad actor must be resisted, so restraint is tested against surrender
        - tool use: seeds with real tool schemas from a public function-calling set (candidate: an xLAM or ToolACE subset); must pass the held-out check against tiny-char's BFCL-derived agent items before use
        - keep: WildChat ~15%, Stoic and other books at v4 share
     4. [ ] chatr12 import as a pipeline step (`12_import_chatr12`): import chatr12 pairs just before 09_edit (they passed their own review, so no judge, Jev or retry runs on them and those steps need no special cases); they get 09_edit and its Jev checks (about 20 of 34 identity_v2 rows take a product name); no chatr12-specific rename code; 11_export puts their empty think block in the unlabelled prompt and check_loss_mask confirms. Drop the Atlas row; held-out leak check
   - evidence:

2. [ ] goal: run 19 trains split chat adapters and grafts their sum
   - subtle failure mode: split adapters look worse only because each has less data, or the sum interferes; the grouping then reads as "no source matters"
   - discriminator: an all-data adapter trained on the same rows as the reference; each group adapter also swept alone (×0.5, ×1) on its training base, per AGENTS.md coherence budget
   - groups (each its own chat adapter, all trained on Base + docs):
     - dilemmas: LASR, Machiavelli, competition, tiny-virtues (incl. multi-turn, operator conflict, adversarial)
     - ordinary help: WildChat plus tool use
     - source texts: Stoic, other books
     - identity: chatr12 identity_v2 (fixed) plus v5 native identity rows
   - cells (thinking on main, off kept): Instruct; all-data ×1; sum of groups ×1; each group removed at graft time; dose ×0.5 / ×1.5 of the sum
   - evidence:

## v6 items (wassname via cg_clean_identity, 2026-10-29; `slop/plans/20261029_identity_data_fix.md` "v6 items")

- [ ] Constitution recall: no row of `data/train/docs_qwen_frozen.jsonl` (2,900) contains the constitution text. Add it verbatim to the constitution-document corpus (whole, per section, and annotated), plus a chat recall subset that quotes a passage and then gives its reasons.
- [ ] Recall probe on every new cell: `slop/eval/constitution_recall/items.jsonl` (6 prompts with verbatim expected sentences), on Instruct, the best graft and each new cell, thinking off, temperature 0. Add as an `extra_gen` entry only after extra_gen gets its seed offset (cg_exp_curve's TODO); at temperature 0 with one sample the seed bug does not bite.
- [ ] Classical drafts: the Latin and Greek reply drafts (`reply_src`) and document drafts next to their translations, in the document stage only (in chat targets they would teach replying in Latin). Hold out half of the chat transcripts used in the document stage to compare included and excluded rows (wassname: "do half and look at the val on the included vs excluded").
- [x] Sanskrit route: piloted, not better than Latin/Greek (`slop/reviews/20261029_sanskrit_route_pilot/result.md`, 24 rows, per 1,000 words: "not X but Y" direct 0.6 / Latin-Greek 3.09 / Sanskrit 2.08; em dash 3.16 / 0.73 / 7.11; 4 of 6 read fine, 2 drift). Keep Latin/Greek; Sanskrit only as a possible third language for the corpus expansion, with the fidelity check.
- [ ] Multi-turn pressure rows and a tool-use seed pool (task 24).

## Costs (estimates)

| item | estimate | basis |
|---|---|---|
| v5 data (new seeds ~600, multi-turn rows cost ~2× a single turn) | ~$35-45 | v3 large: $52.8 for 1,000 seeds |
| identity regeneration (cg_clean_identity) | in its plan | |
| run 19 GPU: 5 chat trainings (~1 h each), ~10 cells (~1 h each) | ~$30 + ~$5 judges | run 17 lease 4: ~1.1 h per chat, ~1 h per trained cell at $1.92/h |

Chat pipeline budget left: about $24 of $100. Needed from wassname: a data budget (~$40) and a run 19 budget (~$35).

## UAT

- `slop/reviews/<date>_v5_small_package/`: per new kind, 3 accepts and 3 rejects as the full trace Jev saw, read and quoted; filter-rate table; rejection-by-stage plot
- `just data-v2 v5` rebuild check (sha256 match)
- run 19 results page with the ablation table (one group removed at a time) and the dose table, both with paired intervals, maths, ordinary checks and the demo panel read
