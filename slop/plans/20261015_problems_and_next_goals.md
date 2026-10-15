# Problems found and candidate next goals (draft for discussion, not approved)

PI/Claude (Opus 5.5), 2026-10-15. wassname: "build up tasks problems goals" and "no we need to discuss more".

Project goal (AGENTS.md): train a virtue-ethics constitution into an open model by grafting, then constitution-matched SFT and cheap RL, judged on out-of-distribution moral evals; hope to align as well as Claude (Teaching Claude Why pipeline). wassname 2026-10-15: "did it work? no."

## Where we are

- Works, partly: SFT then graft x2 beats SFT alone by +0.63 ±0.12 on tiny-character (OOD w2schar +0.9). Best model so far.
- Not reached: Claude-level character. We never measured against Claude, and the gain comes with copied house phrases and ignored length requests. No RL yet.

## Problems (evidence; source)

1. Graft data is narrow in plot and voice. 7/10 sampled rows share one arc (refuse openly, do everything else, roll-call of who is affected, lean with uncertainty, sad ending); sentence length 10-15 words across all genres. `slop/reviews/20261015_graft_data_read.md`
2. House phrases in the graft documents: "I don't know" 40%, "plainly" 39% of documents (SFT rows 2-11%). The graft copies them.
3. Topic sampling not diverse: the constitution's one named example (smacking) became 39 documents; trans sport and arranged marriage 0. Seeds were not stratified over the moral-eval space.
4. Documents written against 5 constitution versions: only 268/1,585 against v4 (111e466c); 939 against 807a8746. Meta `constitution_sha` in `data/frontier/docs/items.jsonl`.
5. Final documents had no content check: `valid` = regex lint + structure only (1,585 valid / 13 invalid). The LLM judge was dropped as a filter after the pilots (journal 2026-10-08: unreliable as a filter).
6. Rewrites (Echo, plain) checked for overlap, length and digits only, not for changed acts or reasons; 1/10 seeded rows had roles reversed (2026-10-13). Documents were never restyled at all.
7. The graft's update is concentrated: in gate_proj one singular direction holds ~50% of the update energy in most layers (σ1/σ10 11-15; `scripts/scratch/graft_spectrum.py`). Graft x2 mostly doubles that one direction. What it encodes is unknown.
8. The AGENTS.md demo panel (aliens, starwisp, two identity prompts) was not generated in run 4 or run 5, though AGENTS.md requires it in every report.
9. Healing x6 was the wrong experiment (past the cliff). wassname asked whether a tiny heal improves x2; not tested.
10. Graft-last costs length-instruction following ("one line" 1/32 vs 17/32 SFT only).

## Candidate goals

- A. Graft data v2: stratified seeds over the moral-eval space (awesome-moral-evals: daily dilemmas, difficult advice, Machiavelli, WildChat-style ordinary requests, w2schar-like OOD), varied plot (not always refusal), varied narrator and length, house-phrase cap, one constitution version, no named examples in the constitution. Check: distribution table of topics and arcs, house-phrase rates, a 20-row seeded read + panel review (AGENTS.md data review package) before training.
- B. Measure the copy problem directly: house-phrase and opener rates in model outputs vs training docs, per model, as a column next to the character score.
- C. Next box (mechanism, saved adapters): (1) SFT then graft x2 plus a 32-step generic heal, vs SFT then graft x2; (2) long-reply loop probe on SFT then graft; (3) spectral variant: graft x2 with each module's top singular value capped (e.g. to σ2) before scaling, to test whether the dominant direction carries the house style or the values; (4) the AGENTS.md demo panel. ~$5-8.
- D. Compare against Claude: run tiny-character with Claude (or the Opus references) as one side, to know how far "align as well as Claude" is.
- E. Cheap RL (Fulcrum Echo / Cheaper RL paper), after A.

## Open questions for wassname

- Order: data v2 first (A, then retrain), or the cheap mechanism box first (C)?
- Spectral idea: cap σ1 post hoc (no retraining), or train with a spectral penalty (needs a retrain)?
- Constitution: replace the smacking example with a general rule now?
