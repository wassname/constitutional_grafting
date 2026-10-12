# Verification

-- PI/Sol, 2026-10-12

## Mechanical checks

Command: `uv run --no-project slop/reviews/20261012_character_skill_test/check_artifacts.py`

Observed output:

```text
PASS: one skill, 5 directly routed decision references
PASS: local Markdown links resolve
PASS: 3 primary archives match source bytes and manifest hashes
PASS: reference quote passages match archived primary texts after Markdown/whitespace normalization
```

Quote checking strips Markdown links, collapses whitespace and normalizes extraction spaces before punctuation. Ellipsis-separated spans are checked individually. It does not validate source truth, mathematical notation or omitted context. Original source bytes remain unchanged.

Pi discovery was checked with the installed `dist/core/skills.js` function `loadSkills({cwd:process.cwd(), agentDir:'/home/code/.pi/agent', skillPaths:[], includeDefaults:true})`. It returned exactly one `character-training-concepts`, at `/home/code/.pi/agent/skills/character-training-concepts/SKILL.md`, with no diagnostic naming that skill. This tests Pi's default directory discovery, not all settings/package filters or the current interactive registry. `/reload` is needed to refresh an already-running session.

Scoped whitespace check: `git diff --check -- AGENTS.md`; clean. Unrelated existing files were not changed. Evidence archives preserve the original extracted text, including its formatting flaws.

## Fresh-reader behavior test

Fixture: `task.md`. One intentionally flawed proposed experiment; not an approved run. No baseline model comparison, so this is evidence of useful behavior with the skill, not a measured improvement rate.

Fresh read-only `pi-quick-oracles` child, inherited Sol model, run `13a50c86-2a6a-43e9-8ef2-de9400b705b7`. Durable output copied exactly to `fresh-reader.md` from the tool's returned output path. It rejected/corrected: double scaling, assuming more epochs fix absent transfer, plain all-token transcripts as the EM recipe, attributing post-graft SFT retention to the constitutional experiment, capability/loops as full healing, paraphrases as certified on-policy/semantic preservation, cross-model projection reuse, and broad PSM refutation.

Reviewer checked the cited scores and important Anthropic/Karan quotations. It found one consequential overstatement: behavior/belief-test divergence does not directly establish internal belief retention or loss. Parent checked the table evidence and replaced that language in the audit and update reference; degraded use of the cloze measurement is now an explicit competing explanation.

Review was selective static inspection. It did not reproduce experiments, exhaustively audit every recipe, or independently inspect original PDFs. The paper extraction limitations remain in the evidence manifest. No training pipeline, constitution, installed third-party extension or public resource changed.
