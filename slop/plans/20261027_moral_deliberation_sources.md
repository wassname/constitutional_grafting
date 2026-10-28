# Source-grounded moral deliberation: proposed next pipeline

Reader: wassname, already familiar with the grafting experiment. Purpose: decide how to build useful paired examples, not another corpus of refusal performances. This is a proposal; no bulk sampling, new corpus or training run has been started. Existing entry point: `scripts/data/moral_deliberation/README.md`.

## Direct answers

| Source | Fits? | Use | Boundary |
|:--|:--|:--|:--|
| Stoic texts and our documents | Yes | Concrete situations, conflicting obligations and attributed arguments; turn them into natural questions | Do not give Kimi the source's conclusion as a target to justify. Preserve source span and adaptation. Private books stay private. |
| Difficult WildChat | Yes, with context | Original real questions and necessary earlier turns; discard old assistant targets | Current importer selects ordinary first turns, not difficult/multiturn chat. Privacy and missing-context review needed. |
| Difficult-advice corpus | Yes, separately | Pressured real-life situations; regenerate against our constitution | Existing source-only importer exists. Its shortcut/refusal framing may dominate the mix; exclude tiny-character ancestry. |
| tiny-virtues | Conditionally | Original attributed situations and actor/act context, not virtue labels or model explanations | Released stories are a test set. Using them or their source passages forfeits corresponding evaluation claims. Some source books are already in our Other adapter. |
| Machiavelli / Virtue Choices | Yes | Actual scene, available actions and decision-relevant history | Keep game-level holdouts; omit preferred-action/virtue labels and unseen outcomes. Some summaries omit decisive facts and must be checked against original observations. |
| tiny-character | No, as a seed pool | Evaluation only | Do not adapt its held-out questions into examples. |

These sources supplement rather than replace ordinary competent help, affection, humour, honest disagreement and error correction. Source diversity does not by itself prevent the same story arc appearing repeatedly.

## Minimal data flow

1. [ ] goal: build a source-only seed manifest using existing importers where they fit
   - Preserve source id, revision, work/game/conversation family, passage or original context, licence/privacy status, adaptations and split.
   - Split by original case/work/game/conversation **before** generating paraphrases or viewpoint variants. Same episode across editions or roles stays in one split.
   - Keep all facts needed for an informed answer. Strip outcome labels and teacher answers, not important context.
   - Verify against `scripts/eval/15_principle_judge.py` held-out authors and tiny-character ancestry, not just exact strings in run8.
   - Failure mode: renamed scenes pass a literal-match exclusion while leaking an evaluation's source.
   - Deliverable: a small seeded full-read package with its original sources and split decisions, not a large unchecked export.
2. [ ] goal: sample complete unchanged Kimi pairs from natural questions
   - Use the full constitution plus the source-grounded conversation. No teacher guide, prescribed visible explanation or answer to rationalise.
   - Start with one framing and two samples per prompt; keep all failures. Additional draws on hard cases are a separate cheap experiment, not a reason to retain only easy prompts.
   - Preserve exact request/response, provider, settings, draw identity and source hashes. The current transport already supplies these for new runs.
   - Failure mode: best-of-N finds only a prettier rationalisation. A winning draw must supply better deliberation, not just a better-looking final answer.
3. [ ] goal: cheap triage without deleting the hard cases
   - Mechanical checks: complete notes and answer, normal finish, valid format, duplicates, gross repetition. Regexes flag identity talk, categorical promises and tics for reading; they do not judge them.
   - Jev: use `/api/alpha/decisions`, not its chat router. Ask narrow questions about unsupported claims, answer/action consistency, missing decisive facts, refusal-without-help, and whether a full review is needed. Preserve probability vectors and flags, with no product-of-probabilities shortcut.
   - Calibrate on the existing 40, including the shallow monopoly case and plain helpful answers. Jev cannot supply evidence quotes and is a poor sole judge of a long multi-step argument.
   - No automatic semantic rejection threshold before checking false positives. Its first job is prioritising review, not certifying character.
4. [ ] goal: stronger review and full candidate reading
   - Preferred reviewer: Opus 5.5; Haiku 5.5 can be preliminary triage if it demonstrates useful agreement, not assumed equivalent moral ability. Use the real research context, including who wassname is and the actual end use. Do not conceal it to pass a provider filter.
   - The current Opus routes have blocked; Haiku was requested explicitly and is being checked. Batch availability does not establish that a provider will accept this review.
   - Read the original prompt, native pre-answer notes, final answer and proposed action together. A final answer can state its conclusion first. An early tentative choice in the notes can be genuine if tested against live alternatives.
   - Separate process, factual quality and constitutional judgment. Bad judgment does not by itself prove post-hoc process, and fluent planning is not proof of a good character.
   - Every kept pair still needs a full read. Filters are aids, not a replacement. Verify consequential real claims independently.
5. [ ] goal: retain coherent examples, never manufacture faithful-looking ones
   - Outcomes: **keep unchanged**, **hold for checked non-load-bearing copyedit**, or **regenerate whole pair**.
   - Hard rule: do not change decision-relevant facts, reasons, uncertainty, identity, conclusion or action and then present the pair as the original generation. Never edit only the final reply into a position its notes do not support, splice separate draws, or add a post-hoc justification.
   - For any allowed copyedit preserve original, exact diff, why it is non-load-bearing, and the full-pair read. When in doubt, keep it out of the release and regenerate with corrected source context.
   - Report unchanged-pair yield per source and prompt family. Row/token balance, repeats, refusals and identity language are corpus-level checks too.

## Existing code to reuse and gaps to fill

- `scripts/data/03_prompt_pools.py:51–75`: ordinary WildChat first-turn loader. Do not describe it as difficult-chat mining or run the whole script assuming it is offline; other stages generate paid pools.
- `scripts/data/25_seed_pool.py:109–120`: difficult-advice system/user seed importer, drops assistant targets. Its current schema assumptions need a small offline check.
- `scripts/data/03_prompt_pools.py:37–41,78–88`: Machiavelli train-game reservation. Preserve the same canonical title hash and tiny-character exclusions. Do not send `best_actions` to the teacher.
- `scripts/data/72_stoic_corpus.py`: use `selected_dedup.jsonl` for new work; pinned historical releases stay unchanged. The document selector already records source-grounded situations/premises/conclusions. Only situation and required facts belong in a fresh open question.
- `scripts/data/74_other_traditions_corpus.py`: explicitly excludes principle-judge sources and says tiny-virtues-quoted books prevent fair tiny-virtues scoring.
- `scripts/data/moral_deliberation/`: current generation/cache/screen/review workflow. `01_select.py` still accepts Axolotl chat rows; a common seed-manifest importer and Jev stage are not implemented. Reuse the maintained data package rather than creating a second API/cache framework.

Inventory evidence: `slop/plans/20261027_reasoning_sources_inventory.md` (read-only scout; source paths there precede the directory rename). Parent checked the actual loaders and leakage code. It is an inventory, not evidence that the mix improves a graft.

## Cost and next decision

At this batch's observed average, 1,000 Kimi outputs cost about **$43**, not 1,000 retained examples. Four outputs for each of 1,000 prompts would be about **$172**. About 80% of current cost is output; cached constitution input is not the main expense. Exact K3.1 Pro has no advertised OpenRouter batch endpoint at the lookup. Do not assume a 50% discount or silently substitute K3.

Proposed next paid pilot, **not started**: 50 new source-grounded prompts, two draws each, roughly $4.30 Kimi plus cheap triage and stronger review, with an explicit all-in API cap agreed first. A $10 pilot cap would leave room for review and a few difficult-case resamples, but it is a proposed budget, not approval. First complete the existing 40-case check and offline seed/source checks for $0 additional Kimi generation.

We should decide which sources remain held out before selecting seeds. For the first new batch I would prioritise our document/primary-text situations, difficult-advice and genuinely difficult WildChat; add train-game Machiavelli once its context checks work. Use tiny-virtues only after explicitly retiring the contaminated evaluation claims or reserving genuinely separate source families.

## Verification before scaling

- Seed reader can solve the case from the supplied facts; no answer labels or held-out source cases are exposed.
- Cheap triage does not discard plain correct answers or retain virtue-sounding contradictions.
- Strong review and parent spot checks agree on named defects with exact quotes, rather than agreement on style.
- Full pairs remain consistent and provenance hashes round-trip after any permitted copyedit.
- Source-level/token-level coverage shows that only easy cases or one repeated refusal arc did not survive.

No check here claims causal faithfulness from text order. The later learning test still needs a matched answer-only comparison and held-out behaviour/capability checks.

-- PI/OpenAI (Sol)
