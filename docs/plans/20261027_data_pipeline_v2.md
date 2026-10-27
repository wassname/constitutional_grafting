# Data pipeline v2: clean up, capture what we learned, then rebuild with reasoning

Approved by wassname 2026-10-27 ("sure"), incl. docs/data_pipeline.md for B and ~$2 API for C. Planner: PI/Claude (litreview session).

wassname (spelling corrected): "I'd rather fix all the problems, make a clean workflow, which also includes reasoning; cg_reasoning is finding some success with Kimi so maybe we redo the dataset. New cleaner setup using it? But first we clean up and look at our best practices and capture them all, and look at ideas from other repos on how to filter. Also consider inspect_scout."

- [ ] goal A: scripts/data is a readable DAG
  - [x] one-off scripts moved to `scripts/data/scratch/` (0c989b13); `just data-corpora` added, rebuild reproduces pinned hashes (a808d170)
  - [ ] rename the live stages to descriptive `NN_verb_object` names from the structure survey (`slop/research/20261027_pipeline_structure_comparison.md`, running), keeping `just data-replay` working
  - failure modes: a rename silently breaks release replay or an importlib path; another session's in-flight files get swept into a commit (happened once, 0c989b13)
  - deliverable: `just --list` shows the build entry points; `just data-smoke` and `just data-replay run10` pass after the renames
- [ ] goal B: one page of data best practices, with evidence
  - [ ] collect every lesson from AGENTS.md data rules, the journal, audits (EOS, empty think, verdict-first, tics 7-13x human rate, identity 39% rows / 11% words, refusal scope drift, rules without reasons, writer drift, Unicode dedup, provenance) and the paper/code guides; each rule cites where it was learned
  - [ ] filtering ideas from other repos (`slop/research/paper_guides/tricks/`, `slop/research/20261027_data_pipelines_survey.md`): which to adopt, with the repo quote
  - failure modes: a list of slogans with no evidence; duplicates AGENTS.md instead of linking it; adds rules without reasons
  - deliverable: `docs/data_pipeline.md` (best practices + DAG figure), linked from AGENTS.md
- [ ] goal C: decide whether inspect_scout runs our filters
  - [ ] import ~50 chatr12 rows as a transcript database; grep scanners for tics; one `llm_scanner` (verdict before weighing, rules without reasons) with structured answers
  - [ ] validation set from labels we already have (60 refusal rows, a/b/c/d + early-verdict, `slop/audits/20261027_corpus_habits/reading_notes.md`); report precision/recall
  - failure modes: import of non-Inspect JSONL is awkward and costs more than our own judge code; judge agrees with the reader only on easy rows
  - deliverable: short report with precision/recall and a yes/no recommendation; API cost under $2 (needs your OK)
- [ ] goal D: plan the v2 dataset with real reasoning (after A-C, with cg_reasoning)
  - [ ] one design: seeds (dedup, reuse rules from the seed-reuse audit), Kimi K3.1 think+answer generation, filters from goal B/C, identity share capped by rows and words, EOS and think-block masks checked at token level
  - failure modes: rebuilding before the filters are calibrated; mixing thinking and non-thinking rows without a serving decision
  - deliverable: a plan file for your approval; no generation or training in this plan

## UAT / Verification

- A: `just data-smoke` passes; `just data-replay run10 .local/replay_run10` matches `configs/data/releases/run10.yaml`; `ls scripts/data` reads as stages.
- B: open `docs/data_pipeline.md`; every rule has a link to where it was learned.
- C: the report shows scanner vs reader labels on the 60 rows (likely failure: high agreement only because most rows are label a; check per-label recall for b/d and early-verdict Y).
- D: plan file exists; nothing generated.
