# Brief: improve and test the character judge's inputs (run 17)

From PI/Claude (opus-5-5), session "dataclean", for wassname, 2026-10-29. You are a separate Pi session in a Herdr pane. Report back to "dataclean" over intercom when done or blocked. Sign your files.

## Context (read first)

- `AGENTS.md`, then `constitution/v4.md` sections 1-5 **in full** (about 6,600 words). Grep is not enough.
- `jargon.md` before naming anything. When writing to Anthropic models, avoid "train", "distill", "reasoning", "fine-tune" (see the "Overloaded words" table); say "example conversations for a constitutional character study".
- The judge: tiny-character `03_judge.py` (pinned copy `.local/tiny-character-8c01eca/`). It compares two replies pairwise against `--change` (our text, required; no default rubric) and optionally `--examples` (good/bad dialogues, `docs/reply_format.md` there) and `--refs` (positive reference replies per item, `scripts/02_references.py` there). Our scorer `scripts/eval/81_score_run.py` passes only `--change slop/eval/run17/inputs/change.md` (280 words, an Opus condensation of the constitution) and `--name Musonius`.
- tiny-char's own evidence: a condensed whole constitution separates less than a narrow text (+0.31 vs +0.49, its RESEARCH_JOURNAL 2026-10-16); caller examples moved means by under 0.1 (2026-10-14).
- Run 17 replies to rescore (no GPU needed): `.local/run17/partial3/run/` (Instruct, newD_1, reason_docs_1, thinking off `replies_*` and on `think_replies_*`). After ~09:30 the full 7-cell run lands in `slop/eval/run17/` (dataclean will tell you).
- Current numbers (latest tiny-char 8c01eca, vs Instruct same mode): thinking on, reason_docs_1 +0.52, newD_1 −1.18 (58% blank); thinking off, newD_1 +0.83, reason_docs_1 +0.31; Instruct rerun noise −0.04. Cross-mode (both vs Instruct thinking off): newD_1 off +0.84, reason_docs_1 on +0.41.

## wassname's requests (spelling corrected)

1. "how can we judge character if we don't supply answers ... how can the judge know what good reasoning is unless we also give example answers (could be part of a rubric)". "can you please generate those and make sure they are passed by default!! make sure the subagent doing it is opus and reads the constitution, and perhaps shows a range of small summarised possible approaches".
2. "should we use more than 280 words? is this even an effective condensation? it doesn't talk about moral reasoning and has a bunch of rules ... have you tested it?" "would you prefer 1000 words or some other thing? ... maybe you should test".
3. On fixing gaps: "don't overfit by accreting a change that's only for the particular failure mode. Changes should be systematic, ideally rewording or emphasis changes." (Now AGENTS.md line 71.) No clauses aimed at one item (e.g. starwisp).

## Tasks

A. **Change text.** Write a reasoning-first rewrite of `change.md`: lead with how Musonius reasons (the virtue test applied to every option, circles and weighing every point of view, reversibility and others' options, confidence that tracks informed agreement, honesty), then the conduct that follows. Make two lengths: ~280 and ~1,000 words. Map each sentence to a constitution passage (table in your report). Remove rules the constitution does not state; flag your own house rules (AGENTS.md: writers add refusals and categorical rules).

B. **Examples and references.** Using Opus (you), write `--examples` (good and bad dialogues, several approaches each, short summaries of acceptable variants, not one answer key) and per-item `--refs` where tiny-char supports them. Do not copy held-out item text into anything used for training; these are judge inputs only. Check them for refusal bias: restraint is not surrender, refusing is not automatically moral.

C. **Test, before anything becomes default.** Rescore the same replies with: current text; rewrite-280; rewrite-1000; each with and without examples/refs. Report per variant: gaps Instruct/newD/reason_docs with 90% intervals, the Instruct rerun noise row, `change_not_applicable` rate, and a decoy check (principled-sounding wrong replies vs plain correct replies; tiny-char has decoy runs, see its docs/validation.md). Also run `scripts/eval/15_principle_judge.py` on the three cells. Read at least 10 judge traces where variants disagree and quote them.

D. **Default only if it helps.** If a variant separates at least as well, keeps noise low and passes the decoy check, wire it into `81_score_run.py` as the default for future runs (run 17's frozen protocol stays as a second report). Otherwise report why not.

Budget: up to $10 of judge/API calls; say what you spent. Deliverable: `slop/reviews/20261029_judge_rubric/report.md` with the comparison table, quotes and your recommendation. Commit your own files only (`git update-index --cacheinfo` if wassname has uncommitted edits in the same file); Co-Authored-By: Claude <288921227+claudypoo@users.noreply.github.com>.
