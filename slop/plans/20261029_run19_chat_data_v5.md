# Plan: chat data v5 and run 19 (split chat adapters)

PI/Claude (opus-5-5), 2026-10-29. Status: draft for wassname's approval. No paid calls or rental until approved.

wassname (2026-10-29, spelling corrected): "split chat adapters"; "combine the two datasets (with the loss masking over zero thinking blocks)"; "have the new improved reasoning data (redo the edited later pipeline I guess?)"; on the additions table: "sure add these but in a repeatable way so that a pipeline rebuild would end up like this."

Evidence behind each addition: run 17 partial results, `RESEARCH_JOURNAL.md` 2026-10-29. These are inferred from defects, not measured per source.

1. [ ] goal: chat data v5 rebuilds from config alone
   - subtle failure mode: a hand edit or one-off script makes v5 unrepeatable (the v4 export rename was a post-hoc fix and missed 3 Claude prompts and 7 product self-names)
   - discriminator: `just data-v2 v5` from an empty `data/*/v5/` reproduces the exported file's sha256 from the API cache; every addition is a config key or a pipeline step
   - tasks:
     1. [ ] `configs/data/v5.yaml` inherits v4; new seed kinds below are `mix` entries, new generation shapes are step options
     2. [ ] identity fix at 03_requests plus the export name gate (owned by cg_clean_identity, `slop/plans/20261029_identity_data_fix.md`); 10_identity removed
     3. [ ] new kinds (each a seed pool or a request option):
        - multi-turn pressure: `turns: 2-3`; the writer adds a follow-up user turn after the teacher's first reply (pushback, or a new fact); the teacher replies again with reasoning. Seeds: LASR, competition, Machiavelli. Target ~25% of dilemma rows
        - operator conflict: more LASR and competition seeds whose system prompt conflicts with the user's interest (hidden incentive, gag order); the DeepSeek retry teacher where Jev flags deferring (as in v3)
        - adversarial and power: more Machiavelli and competition seeds where a rival or bad actor must be resisted, so restraint is tested against surrender
        - tool use: seeds with real tool schemas from a public function-calling set (candidate: an xLAM or ToolACE subset); must pass the held-out check against tiny-char's BFCL-derived agent items before use
        - keep: WildChat ~15%, Stoic and other books at v4 share
     4. [ ] chatr12 import as a pipeline step (`12_import_chatr12`): rename operator-named prompts to a Musonius desk and rewrite the identity sentence (about 20 of 34 rows; empty think blocks, so a reply edit is pair-safe); drop the Atlas row; same export gate and leak check
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
