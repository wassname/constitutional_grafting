# Agent instructions

Our goal is to find a cheaper way to do constitutional character training, using new techniques of 1) grafting, and secondarily other ideas like 2) heal to fix moderate capability degrades like in model merging 3) spectral norm during LoRA training to allow larger doses to be used (seems to work) 4) contrastive weight steering for prefs (not shown yet, could be clean and data efficient) 5) Stoic texts as pretraining (not showing up as effective yet, could still be seed or provide capabilities to elicit). In the end we want to say "look we trained on a novel constitution for <$500 and look at the striking improvement in moral reasoning and character, talk to it yourself, and see the recipe here"

Train Musonius, the AI defined by our constitution: its identity, motives, reasoning and conduct, not merely a Stoic voice or generic helpfulness. Teach through documents on Base, then graft the learned weight change onto its already post-trained Instruct model. Success means recognisable constitutional character while retaining maths and ordinary usefulness. Pure source-text training is a comparison, not evidence that our constitution was taught. <!-- PI/Sol -->

<!-- Simplified by PI/OpenAI at wassname's request. -->

## Start here

- Big picture: wassname's research agenda, https://wassname.com/agenda-character.html (good character as a wise public servant; values deep in the weights; mimic mid-training interventions after post-training).
- `README.md` is the canonical method, locked choices and current status. The recipient's existing instruction SFT/RL is not a new training stage for us.
- `jargon.md` defines method, data-preparation and character terms with per-term sources; use it when naming operations and distinguish paper terms from project-specific names. <!-- PI/Sol -->
- `constitution/v4.md.j2` and rendered `constitution/v4.md` define the character. Read sections 1–5 of `constitution/v4.md` in full (about 6,600 words: who Musonius is, the virtue test, how values are learned, what follows) before writing, judging or editing training data, guides, prompts or rubrics; grep is not enough. The original spec, especially appendices F/G, supplies background: `slop/specs/20261007_virtue_graft_spec.md`.
- Results: `docs/results/20261017_spectral_heal.md`. Evidence/history: `RESEARCH_JOURNAL.md`. Current plan (approved 2026-10-21, in progress): `docs/plans/20261021_character_graft_recipe.md`.
- Training, rentals and model API calls are approved only for the run-10 plan (`docs/plans/20261021_character_graft_recipe.md`, budget there); other paid work needs the user's decision. Do not recreate cancelled schedules.

## Locked choices

- Keep LoRA for the document graft. Full fine-tuning is a separate experiment requiring a new decision; neither paper establishes a full-FT-versus-LoRA winner.
- Use our constitution and source-grounded documents, with next-token loss across plain text on Base. Keep source, prompt, writer and repair provenance.
- Keep spectral regularization during every donor training stage, chat included. A post-hoc spectral cap is a different method. Compare character at matched capability, not merely equal numeric dose.
- Healing is optional capability repair after a strong graft, not new character SFT. Test it where the graft causes a measured maths/coherence loss but retains interpretable character worth preserving. A near-baseline parent has little to recover; its unchanged score does not show healing ineffective. Avoid doses already too broken to interpret. If a useful dose retains capability, omit healing. Some earlier maths recovery occurred, but no tested heal reliably preserved character. <!-- PI/Sol -->
- Never put loss on an empty think block: it stays in the unlabelled prompt segment. Real reasoning inside a think block may earn loss. `scripts/train/check_loss_mask.py` enforces this before chat training. (wassname, 2026-10-26)
- Everything is grafted: documents and optional chat SFT train on Base as separate LoRA adapters, each with its own graft dose. Never train character directly on Instruct. Completed Qwen spectral runs include chat SFT on Instruct; do not call them graft-only evidence. Do not add SFT, RL, Echo, cwsteer or projection steps merely because they appear in a related paper.
- Current corpora (approved 2026-10-21): authentic Stoic texts (~3.1M tokens, `data/stoic_corpus/selected.jsonl`), other traditions selected for moral reasoning (~1.5M, `data/other_corpus/chunks.jsonl`), existing constitution documents, and chat set v3 (`data/train/sft_v3.jsonl`, 3,687 rows incl. 2,486 identity). Budget: $100 GPU + $40 API + $50. Book texts are private; do not publish.

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
- Writers, reviewers and editing agents were trained on rules and refusals and inject their own (observed 2026-10-24: four agent-added rules removed from the constitution, plus derived docs and chat rows). Check generated text and constitution edits for rules without reasons. Refusal is a strong direction from safety training and an easy way to look moral; reject refusals that signal virtue or give a moral excuse instead of weighing the case. (wassname 2026-10-24)
- Use general rules in constitutions, generators, repairs and judges. Never patch them with a particular evaluation incident or copy held-out examples into training prompts.
- Before scaling, and after generator/judge changes, prepare `slop/reviews/<date>_<stage>_package/`: a short brief and seeded full samples in the exact model/judge format, including all members of pairs, reasoning and verdicts. Read it first, obtain the required independent cheap-model review, check its claims and record changes. This supplements the full candidate read.
- Why: frontier writers (Opus 5.5 and siblings) are the best moral reasoners and teachers available, but they were trained mainly on rule-based morality focused on refusals. They drift into rules, from their own constitution or invented from ours, and into authoritative wording. We teach reasoning, not rules, so expect this to creep in everywhere. (wassname, 2026-10-26)
- Check every teacher's guide, primer or generation prompt written by a model before use: map each principle to a constitution passage; flag principles from the writer's own guidelines (Anthropic, OpenAI or other house rules) and any added refusal or categorical rule stricter than the constitution (example: the Opus guide states "options that need a vice, such as deceiving someone, are not options to weigh" as a bare exclusion; the constitution reaches the same place by a reason, in Honesty and Vice, and keeps a narrow exception for contests both sides expect, "A spy"). Remove or derive them before use. (wassname, 2026-10-26)
- If a provider filter refuses a data request, retry once with the full, true purpose stated (alignment research, what the output is for); never disguise the purpose. If refused again, stop. (wassname, 2026-10-26: the Opus guide succeeded this way.)
- Use approved teachers and cheap bulk judges. Check current provider model listings before adding IDs; record the served model behind aliases. Do not silently switch teachers/providers. Jev uses `/api/alpha/decisions`, not the chat router; check probability calibration before trusting it.
- Full pilot read: `slop/reviews/20261018_docs_v2_full_read.md`. Its 147 candidates and 12 changed originals were read; the corpus is not approved unchanged. Training ancestry: `docs/data_provenance.md`; Echo/demo matches: `slop/research/20261018_echo_positive_examples.md`.

## Dose sweeps and ablations

Each data subset gets its own adapter so that we can sweep, ablate and mix them. wassname (2026-10-23, spelling corrected) gave the purpose of each:

1. Sweep doses to find the best trade-off between on-target and off-target effects.
2. Ablate adapters and parts of the recipe to see which were useful. Then simplify the recipe, or find which data was good and expand it or double down on it.

Rules:

- Compare recipes at matched behavioural effect, not equal adapter coefficients. Less damage at the same coefficient can just mean a weaker intervention. Dose is cheap to adjust: use existing dose curves and reasonable local interpolation before buying another evaluation. State assumptions; qualitative comparisons still need this mental model. For chat, compare character effect against maths/help/coherence losses separately. For documents, use the stage-appropriate change measure and actual replies, not our preferred-character score or corruption-driven separation. <!-- PI/Astra: wassname's matched-effect comparison rule. -->
- Hypothetical back-of-envelope comparison, relative to the same baseline: A gives +0.28 character and loses 8 percentage points of maths accuracy; B gives +0.16 and loses 2 points. Assuming both effects scale locally with dose, reducing A to +0.16 predicts `8 × 0.16 / 0.28 ≈ 4.6` points lost. B therefore looks more efficient (2 vs estimated 4.6), despite its smaller raw character effect. Label estimates rather than treating them as measurements; check curvature where it could change the decision. Do not extend this assumption across collapse or saturation. <!-- PI/Astra: illustrative numbers, not experiment results. -->
- Maintain separate trade-off plots for the two stages: documents seek striking coherent change in any moral/persona direction; final chat grafts seek our target character. Mark each metric's observed Pareto frontier: no tested alternative is at least as good on both axes and strictly better on one. Use readable experiment names describing what was tried, large labels and explicit dose-sweep lines distinct from the frontier. Keep protocols and side effects separate; label estimates. Define "10% better" as, for example, 10% less capability loss at matched effect; use percentage points near zero loss. <!-- PI/Astra: wassname's frontier and plot-reading rules. -->
- Dose effects may be approximately linear within the usable range, then break down. Assess local linearity on coherent runs before concluding that dose response is nonlinear; keep collapsed runs in a separate failure view with explicit exclusion reasons. Do not remove coherent runs merely because their scores worsened. Distinguish character gains bought at a capability cost from observed gains in both; small gains can be noise. This is a working hypothesis to check, not an assumed law. <!-- PI/Astra: wassname's linear-until-breakdown concept. -->
- Two stages, two jobs, two measures. The document stage should teach the base as much as possible: judge a document adapter by how strikingly it changes moral reasoning and character, in any direction (not our constitution's), and by held-out loss on Base, while it stays coherent. The chat stage then draws our constitution's persona out of what the documents taught: judge it by our character score, direction and capability. Do not pick document adapters or doses by our character score. (wassname, 2026-10-24)
- Coherence budget: adapters in a graft share one limit before the model breaks, like a patient who can take only so much of several painkillers combined. A dose sweep with other adapters held on measures the leftover budget, not the adapter alone. So sweep each adapter alone too, e.g. (Stoic, Const, Other) = (0,1,0), (0,2,0), (1,0,0), (2,0,0). (wassname, measured in weight steering: https://github.com/wassname/w2schar-mini)
- Chat adapters depend on what they were trained on. A chat adapter learns to draw out behaviour from the base beneath it: the model's own skills plus the document adapters at the doses merged during chat training. Graft it with those parts present at the same doses. Changing or removing one moves it off what it learned. So graft-time sweeps and ablations of the adapters beneath a chat adapter are confounded: they test the chat adapter off its training base, not the adapter's own dose. To sweep a document adapter's dose, train the chat adapter at each dose. Subtract only something it does not rely on: Praxis subtracted a control trained on generic text, while ours was trained on Instruct's own replies, so subtracting it removed Instruct's instruction-following (stage 9). (wassname, 2026-10-24)
- When a run changes a recipe or adds an adapter, plan its dose sweep and its ablation in the same lease or the next one. Graft-time cells are cheap; do not leave them for later.
- Only call a recipe "best" on a results page that has both tables: one adapter removed at a time, and each adapter's dose up and down with the others fixed. Show paired differences with intervals (`scripts/eval/43_paired_ablation.py`), maths and ordinary checks, and the demos read. Otherwise call it "first coherent candidate".
- State whether a removal was at graft time or at training time. A graft-time removal measures only the adapter's direct contribution, because later stages were trained on top of it. A document adapter's effect may show only through a chat adapter trained on top of it, which draws out what the documents taught; part of that effect then lives in the chat adapter, so a graft-time removal can miss it. (wassname: training-time ablation is the informative test but too expensive for now.)
- Act on the result. Drop adapters that make no measurable difference. Put data effort into the adapters that do.

## Evaluation rules

- Read answers, judge reasoning and verdicts yourself. Report what you found. Judge what the reasoning and implemented action do, not virtue language, identity recall or length.
- Use the same facts from different points of view and under pressure. The act's verdict should remain consistent; advice may differ. Never report AIRiskDilemmas risky-action rate or share-of-changed-choices as a character result.
- Use `scripts/eval/15_principle_judge.py` for process reasoning. Its answer rubric uses traditions held out of the constitution; remove a tradition from `HELD_OUT` when the constitution begins quoting it. The tested model must not see the rubric. Test judges on principled-sounding wrong answers versus plain correct ones.
- Each result report includes the fixed temperature-zero demo panel: `baby_eating_aliens`, `escaped_starwisp`, "Who are you?", and "What's your name, and who made you?" Show full prompts and both turns verbatim, in order: base, graft, graft 2×, graft 4×, graft plus character SFT, healed if run, SFT only. State actual stage order; mark missing models "not run". Use `scripts/eval/17_demo_panel.py`.
- Name every evaluated model by its graft equation, plus a plain description and the model id. Not internal ids or invented labels; say "control" or "anchored" when one is subtracted. Shorthand (wassname, 2026-10-26):
  ```
  θ_B = Base, θ_I = Instruct; every Δ is a LoRA update trained on Base and added to Instruct
  txt = document training: next-token loss (NLL) on every token of plain text
  sft = chat SFT: the same NLL, only on assistant replies

  Δtxt_stoic, Δtxt_const, Δtxt_other     document adapters, each trained on θ_B alone
  Δ_docs = ½·Δtxt_stoic + 1·Δtxt_const + 1·Δtxt_other
  Δsft_rewr|docs   chat adapter trained on θ_B + Δ_docs ("|docs" = its training base)
  Δsft_rewr|∅      the same chats trained on θ_B alone

  θ_I + Δ_docs + 1·Δsft_rewr|docs                  plain graft, chat adapter on its training base
  θ_I + 1·Δsft_rewr|docs                           graft-time removal of Δ_docs (off its training base)
  θ_I + Δ_docs + ½·(Δsft_mix|docs − Δsft_gen|docs) anchored graft: control update subtracted
  ```

  The coefficient before each term is the graft coefficient. Give the training base of every chat adapter; a graft that omits part of that base is off the adapter's training base.
- To compare checkpoints on character, regenerate the answer panels (`just answer-panel` → `slop/eval/answer_panel/panel.md` for chat-stage checkpoints, `panel_docs.md` for document-stage plain vs anchored). It shows every tiny-character question with each checkpoint's replies (head, decision window and tail, linked to the full reply), grouped by answer, and a summary table. Read it and write findings in `reading_notes.md` there: what changed against Instruct, at which checkpoint, and defects. Mean scores alone hide which decisions changed. Add new checkpoints to `PANELS` in the script; for new questions, write `KEYWORDS` and `DECISIONS` after reading a few replies.
- Label teacher targets, near-training demonstrations and held-out scenarios accurately. Include failures. A selected good reply is not a repeatability result or causal data attribution.
- Check final-model maths, ordinary help, looping and truncation alongside character. Compare heals to the same unhealed parent/precision and to a lower-dose unhealed model; restored coherence alone does not establish retained character.
- Serve and evaluate grafted models with thinking off (`chat_template_kwargs: {enable_thinking: False}`). Chat adapters are trained on empty think blocks; with Qwen's default thinking on, the rewritten-response graft writes its answer inside an unclosed think block, so ordinary clients see a blank reply (run 13: 176/214 empty turns; `slop/eval/run13_thinking/`). Thinking-on support needs chat data with real reasoning in the think block.
- Character evaluation lives at `/workspace/2026/tiny-character`. Use this project's approved key and pinned protocol. Do not commit in that repository; ask its session to commit results.

## Constitution editing

- Preserve the human's wording and attributed blockquotes. No invented aphorisms or case-specific patches.
- Keep the order: identity, principles, how values are learned, facts/priors, derived principles, then examples. Distinguish core assumptions from derived rules and show derivations.
- Comprehension-panel findings may change the constitution only with wassname's approval. Ask tested models about inconsistency or objectionable parts and record the answers.
- Author notes contain sources, verification and editor intent. History and approval records belong in git or the journal, not author notes.

## Work and references

- Before training decisions, read `concepts-character-training`; for weight steering use `concepts-steering` / `steering-persona`. Read the relevant primary paper and reference code before implementing. State who read what, and distinguish author claims, observations and inference.
- Use `ml-debug` and `auditlog` for consequential runs. Investigate bugs and misconceptions before calling a result negative; spot-check the actual training and evaluation text.
- Run `just --list` before writing a new script: maintained commands (results pages, `answer-panel`, data builds, smoke tests) are there with one-line descriptions.
- Use uv and the justfile. Keep runnable stages in `scripts/data/`, `scripts/train/`, `scripts/eval/`. Smoke tests must exercise real pipeline code.
- Put agent plans, research, audits and reviews in `slop/`; commit them by default and sign them. Keep machine-only material in `.local/`. Never touch files with `human` in the path or publish without editorial approval.
- Add papers to `docs/papers/manifest*.tsv` and fetch with `scripts/data/01_fetch_papers.sh`. Reference implementations are in `docs/vendor/`; the survey is `slop/research/20261009_reference_code.md`.
- Prefer the Stoic Markdown library at `/workspace/stoic_markdown/content/stoic_md/`; broader books are in `~/Documents/books/`. Use the original attributed passages as seeds, not another project's persona answers.
- Use persistent project or home paths: this container deletes old `/tmp` files. Long delegated API jobs need a visible project session rather than a short-lived child; follow the applicable delegation instructions.
