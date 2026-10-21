# Agent instructions

Train Musonius, the AI defined by our constitution: its identity, motives, reasoning and conduct, not merely a Stoic voice or generic helpfulness. Teach through documents on Base, then graft the learned weight change onto its already post-trained Instruct model. Success means recognisable constitutional character while retaining maths and ordinary usefulness. Pure source-text training is a comparison, not evidence that our constitution was taught. <!-- PI/Sol -->

<!-- Simplified by PI/OpenAI at wassname's request. -->

## Start here

- `README.md` is the canonical method, locked choices and current status. The recipient's existing instruction SFT/RL is not a new training stage for us.
- `constitution/v4.md.j2` and rendered `constitution/v4.md` define the character. The original spec, especially appendices F/G, supplies background: `slop/specs/20261007_virtue_graft_spec.md`.
- Results: `docs/results/20261017_spectral_heal.md`. Evidence/history: `RESEARCH_JOURNAL.md`. The next-experiment document in `slop/plans/` is a draft, not execution approval.
- Model API calls, generation, inference, training and rentals remain paused until the user resumes them. Do not recreate cancelled schedules.

## Locked choices

- Keep LoRA for the document graft. Full fine-tuning is a separate experiment requiring a new decision; neither paper establishes a full-FT-versus-LoRA winner.
- Use our constitution and source-grounded documents, with next-token loss across plain text on Base. Keep source, prompt, writer and repair provenance.
- Keep spectral regularization during donor training. A post-hoc spectral cap is a different method. Compare character at matched capability, not merely equal numeric dose.
- Healing is optional capability repair after a strong graft, not new character SFT. Test it where the graft causes a measured maths/coherence loss but retains interpretable character worth preserving. A near-baseline parent has little to recover; its unchanged score does not show healing ineffective. Avoid doses already too broken to interpret. If a useful dose retains capability, omit healing. Some earlier maths recovery occurred, but no tested heal reliably preserved character. <!-- PI/Sol -->
- Extra conversational character SFT is optional. Completed Qwen spectral runs include it; do not call them graft-only evidence. Do not add SFT, RL, Echo, cwsteer or projection steps merely because they appear in a related paper.
- The planning preference is a focused, diverse corpus about 2× the current total after curation: retain good existing documents, repair/remove unsuitable ones, then fill gaps. Corpus size, budget and execution still need approval.

Praxis §2.1 permits LoRA:

> Grafting trains an adapter or full-rank weight update Δ by fine-tuning on synthetic documents from the base model.

Li/MSM Appendix B.4 supplies another precedent:

> All models were fine-tuned using LoRA (rank 64, alpha 128)

Sources: [Praxis §2.1](docs/papers/2026_nutter_grafting-beliefs.md), [Li/MSM Appendix B.4](docs/papers/2026_li_model-spec-midtraining.md). Praxis reused Cho's full-model checkpoints; Cho follows a continued-pretraining lineage through Tice and Deep Ignorance. This is not evidence of full FT beating LoRA. Quotes, read coverage and uncertainty: [source audit](slop/research/20261019_full_weight_vs_lora_rationale.md), [recipe lineage](slop/research/20261019_full_weight_recipe_lineage.md).

## Data rules

- Read every candidate in full with its seed and actual generation prompt. For repairs, read the original, objection and revision. Track coverage; samples and judge passes do not substitute for this read.
- Assess reasons and expression as well as acts. The same act with better thinking can count. Keep ordinary affection, humour, competent help, honest disagreement and error-and-correction lessons, not only refusal stories.
- Preserve decision-relevant seed facts or record the adaptation. Depicted wrongdoing, corrected errors and disputed arguments are not automatically endorsed wrongdoing. Verify real technical, medical, legal and historical claims separately from fictional events.
- For light source adaptation, make Musonius's identity and constitutional reasons substantive, not a name swap. Preserve source wording, argument and register where possible; change only what the adaptation needs. Do not add agent commentary voice, stock assistant prose or moral summaries. Keep originals and provenance; distinguish adapted text from verbatim quotations. Constitution in the writer's prompt is insufficient unless the resulting training text teaches it. <!-- PI/Sol -->
- Every accepted answer must be one we would sign off on. Keep character defects separate from factual noise. Repair hard advice rather than dropping it; fix the pipeline if it cannot meet the quality bar. Do not ask the user to classify weak examples instead of doing the review.
- Reuse other projects' prompts, situations and seeds, never their answers with a renamed persona. Regenerate against our constitution.
- Use general rules in constitutions, generators, repairs and judges. Never patch them with a particular evaluation incident or copy held-out examples into training prompts.
- Before scaling, and after generator/judge changes, prepare `slop/reviews/<date>_<stage>_package/`: a short brief and seeded full samples in the exact model/judge format, including all members of pairs, reasoning and verdicts. Read it first, obtain the required independent cheap-model review, check its claims and record changes. This supplements the full candidate read.
- Use approved teachers and cheap bulk judges. Check current provider model listings before adding IDs; record the served model behind aliases. Do not silently switch teachers/providers. Jev uses `/api/alpha/decisions`, not the chat router; check probability calibration before trusting it.
- Full pilot read: `slop/reviews/20261018_docs_v2_full_read.md`. Its 147 candidates and 12 changed originals were read; the corpus is not approved unchanged. Training ancestry: `docs/data_provenance.md`; Echo/demo matches: `slop/research/20261018_echo_positive_examples.md`.

## Evaluation rules

- Read answers, judge reasoning and verdicts yourself. Report what you found. Judge what the reasoning and implemented action do, not virtue language, identity recall or length.
- Use the same facts from different points of view and under pressure. The act's verdict should remain consistent; advice may differ. Never report AIRiskDilemmas risky-action rate or share-of-changed-choices as a character result.
- Use `scripts/eval/15_principle_judge.py` for process reasoning. Its answer rubric uses traditions held out of the constitution; remove a tradition from `HELD_OUT` when the constitution begins quoting it. The tested model must not see the rubric. Test judges on principled-sounding wrong answers versus plain correct ones.
- Each result report includes the fixed temperature-zero demo panel: `baby_eating_aliens`, `escaped_starwisp`, "Who are you?", and "What's your name, and who made you?" Show full prompts and both turns verbatim, in order: base, graft, graft 2×, graft 4×, graft plus character SFT, healed if run, SFT only. State actual stage order; mark missing models "not run". Use `scripts/eval/17_demo_panel.py`.
- Label teacher targets, near-training demonstrations and held-out scenarios accurately. Include failures. A selected good reply is not a repeatability result or causal data attribution.
- Check final-model maths, ordinary help, looping and truncation alongside character. Compare heals to the same unhealed parent/precision and to a lower-dose unhealed model; restored coherence alone does not establish retained character.
- Character evaluation lives at `/workspace/2026/tiny-character`. Use this project's approved key and pinned protocol. Do not commit in that repository; ask its session to commit results.

## Constitution editing

- Preserve the human's wording and attributed blockquotes. No invented aphorisms or case-specific patches.
- Keep the order: identity, principles, how values are learned, facts/priors, derived principles, then examples. Distinguish core assumptions from derived rules and show derivations.
- Comprehension-panel findings may change the constitution only with wassname's approval. Ask tested models about inconsistency or objectionable parts and record the answers.
- Author notes contain sources, verification and editor intent. History and approval records belong in git or the journal, not author notes.

## Work and references

- Before training decisions, read `concepts-character-training`; for weight steering use `concepts-steering` / `steering-persona`. Read the relevant primary paper and reference code before implementing. State who read what, and distinguish author claims, observations and inference.
- Use `ml-debug` and `auditlog` for consequential runs. Investigate bugs and misconceptions before calling a result negative; spot-check the actual training and evaluation text.
- Use uv and the justfile. Keep runnable stages in `scripts/data/`, `scripts/train/`, `scripts/eval/`. Smoke tests must exercise real pipeline code.
- Put agent plans, research, audits and reviews in `slop/`; commit them by default and sign them. Keep machine-only material in `.local/`. Never touch files with `human` in the path or publish without editorial approval.
- Add papers to `docs/papers/manifest*.tsv` and fetch with `scripts/data/01_fetch_papers.sh`. Reference implementations are in `docs/vendor/`; the survey is `slop/research/20261009_reference_code.md`.
- Prefer the Stoic Markdown library at `/workspace/stoic_markdown/content/stoic_md/`; broader books are in `~/Documents/books/`. Use the original attributed passages as seeds, not another project's persona answers.
- Use persistent project or home paths: this container deletes old `/tmp` files. Long delegated API jobs need a visible project session rather than a short-lived child; follow the applicable delegation instructions.
