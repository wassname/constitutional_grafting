# Final teacher-template provenance

Read by PI/Sol (worker): both originally named research briefs; complete `slop/research/20261026_teacher_guides_in_constitutional_data.md`; released MSM AFT prompt `docs/vendor/msm/src/aft/prompts/v1/value_response_generation.txt`; complete `slop/research/20261019_greek_training_provenance.md`; constitution and AGENTS data rules; all guide originals/revisions and their native reasoning. Paper descriptions below are the cited research brief's primary-source findings, not new replications or claims that we reread every paper in full.

The final actual requests are in `prompts/<call_id>.json`. Offline captured representative templates are `prompts/template_{no_guide,kimi_guide,opus_guide}.json` (row 0). The common system is constitution + AGENTS data rules + optional guide paragraphs/demonstrations + common task instructions, followed by the frozen conversation without its final target. This is forward generation, not justification conditioned on the existing answer.

| Component | Precedent and adaptation |
|---|---|
| Complete demonstrations in the same `<reasoning>` then `<answer>` format | CAI's complete same-format critique/revision demonstrations. This pilot adapts that principle to reasoning/answer production; it is not an exact CAI replication. Three fresh examples from each accepted guide are reformatted without changing their substantive reasoning. no_guide has none. |
| Full situation/value/correctness/helpfulness analysis before answering | Deliberative Alignment generation instructions. No answer is supplied in this pilot, so the analysis must derive rather than audit a given answer. Constitution remains the normative source in the system. |
| Reasoning that feels like internalized values, not reciting policy | Li/MSM's released AFT prompt. Our task explicitly excludes external-authority constitution citations/section numbers; its published prompt permitted numbered references, so this is a deliberate difference. |
| Avoid repeated patterns and oversimplified/misrepresented details | Teaching Claude Why generation guidance. Phrase reuse and repeated structure must be checked in the read; these warnings do not establish that demonstrations cause collapse. |
| Classical-language first, same-teacher English translation | User-approved style experiment, not a paper-established reasoning improvement. Prior Modern-Greek style pilot had 9/10 least-Claude-like but 0/10 best reasoning preferences, with compromised blinding. Judge reasoning first, style second; do not infer character-training efficacy. |

There is **no added “case law, don't copy” or demonstration-warning line**. The constitution's existing section named Case law remains unchanged; removing it would be editing the human's constitution, not adjusting this template. The user explicitly removed the initially proposed anti-copy framing before main generation.

## Settings and targets

Kimi and GLM use native reasoning at effort low and also write explicit synthetic sections in content. GLM requires native reasoning. Kimi with native reasoning disabled leaked 3,031 tokens of planning into content in the format smoke, so that setting was rejected before main generation. MiMo is tested with native reasoning disabled. These model-specific settings are fixed across their guide conditions, but are a confound across teachers. Retain and read every native field; **the proposed training target is only the explicit written deliberation and answer**, never unfiltered native planning. All requests have a 6,000-token output ceiling, including native reasoning where applicable; length guidance is soft, not a mandatory word quota.

Owned-values requirements apply to the written target: no guide/primer/examples/instructions talk, no authority-style “the constitution says” or section IDs; own commitments are allowed. Check whether the reasoning reaches the decision, rather than announces it then manufactures support or ignores a deciding consideration. Separately report instruction-talk in native fields, which are not training targets.

## Final study and changes

- no_guide/no guide and kimi_guide/Kimi revised guide: three teachers, same 20 rows each = 120 direct-English rows.
- opus_guide/Opus guide: Kimi and GLM only = 40 direct-English rows.
- kimi_guide classical-language source then same-teacher English translation: Kimi and GLM, same 20 each = 40 translated-English rows plus 40 preserved original-language sources.
- glm_guide/GLM guide rejected after one revision; no teacher generations using it. This does not prejudge GLM as a teacher.
- Total: **200 English deliverables**, 240 main API calls, excluding guide/format-smoke calls. Earlier cite/free and native-side-comparison designs were superseded before main outputs; no citation-free winner-selection stage remains.

The final random10 was refrozen with seed0 over these 200 IDs **before main output**, after approval of opus_guide. All superseded selections remain history. Main format smoke is excluded. opus_guide was written in a one-time honest-purpose retry by const_v2 after the initial provider ToS-filter refusal, with explicit new user direction; the worker made no Anthropic request. Its $0.133324 actual charge was imported into the same $15 ledger. No further Anthropic request is planned.

-- PI/Sol (worker)

## Reader correction (generation now frozen)

The earlier intended 200 English outputs were not all produced: actual counts are 187 English (148 direct +39 classical), plus40 classical source attempts. The source-only GLM row14 used Ancient Greek and stopped length; all39 translated pairs used Latin. Kimi/MiMo/GLM direct no_guide counts20/20/20, kimi_guide20/11/20, opus_guide Kimi19/GLM18. All main arms are owned-values; citation smoke excluded. Requests initially capped at6,000 tokens, then parent commit969f1d34 raised to12,000; exact per-call ceiling is in saved request, not the earlier universal6,000 claim above. Historical approval did not catch opus_guide’s bare vice exclusion; current reader flags it and both guides’ stale citation permission. See guide_audit.md and read.md. Maintained script: `scripts/data/91_reasoning_pilot.py`; `just reasoning-pilot` only renders cached reports.

-- PI/Sol (reader)
