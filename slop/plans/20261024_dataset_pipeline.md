# Dataset-pipeline refactor: proposed changes

> wassname: "dataset building should be repeatable not ad hoc"; show the actual changes, now versus after.

Scope: dataset code and its executable recipe, including chats and reasons-first documents. No training, paid calls or changes to existing training releases during the refactor. Reuse the current generators, teachers, reviewers and data; no workflow framework or whole-repo move.

- [ ] goal: separate assembling a release from generating/reviewing new material
  - [ ] Extract the chat assembly in `73`/`76` into pure functions in `scripts/data/chat_pipeline.py`; give all operations explicit input/output paths. Preserve order, seeds, identity selection and encoding.
  - [ ] Add `configs/data/releases/run10.yaml` and `run11.yaml`: input/cache/decision hashes, expected outputs, selection settings and historical exceptions. Keep `89` as the downstream run11 packaging step, including its different JSON encoding.
  - [ ] Make `just data-replay <release> <output>` rebuild offline into a separate directory. Expected hashes are committed inputs, never rewritten by the build.
  - [ ] Record the absent `fresh_loop/edits.jsonl` as absent in historical replay. It has no git history; do not restore its unreviewed edits or invent a rejection decision.
  - deliverable: run10 chatr13 `eea4a788` (1,798 rows), const `d09f8ba0` (1,584), and run11 chatr13 `44ae6d30` reproduced exactly, alongside all other pinned outputs.
  - failure modes: identical counts hide changed content; changing one output's encoding alters a trained release.

- [ ] goal: the complete chat process accepts any supplied chat dataset
  - [ ] Use `chat_pipeline.py` as the fixed stage sequence: assemble sources → constitutional rewrite → full review and refusal audit → reviewed repairs → re-review → final assembly. Scan identity rows too. No configurable graph engine.
  - [ ] Move `80`/`83`/`88`'s reusable writing functions into that module; reuse the code from `86` for auditing. Existing source writers (`71`, `82`, `87`) supply rows through explicit paths and share the extracted prompt/call helpers.
  - [ ] Put prompts and the current source/mix settings in `configs/data/chat.yaml` and `configs/data/prompts/`. New data uses the approved reasoning-based wording; historical replay keeps its old prompts/verdicts.
  - [ ] New intermediates: `data/interim/<name>/{sources,rewrite,review,refusal_audit,refusal_review,repairs,repair_review}/`; final files: `data/processed/<name>/{chat.jsonl,manifest.json}`. Preserve raw/cache locations.
  - [ ] `just data-build <recipe> <input> <name>` runs/resumes the chain offline. Missing model work produces a pending-job list; missing reviews produce exact review packages. No output is labelled ready while either remains.
  - deliverable: one build path for current and new input files; trace each final row through the intermediate products.
  - failure modes: an operation exists but the build never calls it; a new filename still modifies chatr12; added plain-help rows bypass checks.

- [ ] goal: model work and review are explicit, reusable steps
  - [ ] Add `scripts/data/model_calls.py`: extract the existing OpenRouter sync/batch code; save complete requests/responses, provider/model/settings, finish status and cost, keyed by request hash plus sampling attempt. Read credentials only when sending a request.
  - [ ] Add `scripts/data/reviews.py`: candidate selection, batch formatting, completeness checks, verdict parsing/joining and approved-replacement application. Replace `88`'s id-prefix filter (which excludes identity ids) with exact candidate membership. Preserve reviewer disagreement; do not claim both objected when only one did or quietly keep a failed repair.
  - [ ] Add `scripts/data/review_workflow.js`: the existing two-pass Sol workflow, parameterised by the generated review package instead of a date-specific directory. Pi runs this workflow; a shell command must not pretend it ran subscription reviews.
  - [ ] Bind each verdict/repair to exact source/request, reply, constitution/rubric and review setup; save disagreements and human decisions. Legacy decisions are imported with their actual evidence, not retroactively presented as new reviews.
  - [ ] Explicit generation command: `just data-generate <workdir> <budget-usd>` sends only approved pending OpenRouter jobs. Pi reviews save their results; rerunning `data-build` continues without repeating completed work.
  - [ ] Refactor `85_reasons_docs.py` in place to reuse these call/review helpers and accept seed/output paths: preserve A analysis → B reasoning → C plot → D document → E check; save each stage separately so a failed check does not lose a paid document. Rechecks/redos write new artifacts.
  - deliverable: checked-in prompts, selection/batch/join code, reusable review workflow and resumable stage records for chat and docs.
  - failure modes: stale approval applies to edited text; a repair creates a contradiction; re-running resubmits a paid batch; source or held-out provenance is lost.

- [ ] goal: remove replaced code and update the real entry points
  - [ ] Once parity passes, remove the replaced one-off implementations in `80`, `83`, `86`, `88`; update callers `82`/`87`, the just recipes, `docs/data_provenance.md` and the existing recipe page. Keep `73`/`76` only as thin historical build entry points if existing callers require them.
  - [ ] Commit curated corrections/decisions as recipe inputs, not anonymous edits or broad keyword-deletion rules. Check entire revised replies/docs for consistent reasons and action.
  - [ ] Keep run10/run11 training paths and `89`'s held-out exclusions unchanged; coordinate their callers before redirecting future training to a new manifest.
  - deliverable: one implementation of each operation, no duplicate current builders, and clear historical versus new-data commands.
  - failure modes: new helpers coexist with active duplicate logic; a refactor silently changes training or held-out membership.

## UAT / Verification

- Replay: build pinned releases offline in a fresh directory; require matching hashes, row order, loss masks and held-out membership. Inspect selected source-to-output row histories. Resolve mismatches before changing expectations.
- New input: supply a second file of real cached rows. Show an accepted repair applied, a justified refusal retained and newly added rows included in final checks; do not count successful exit alone.
- Invalidated inputs: change a request/reply/rubric or remove a required cache/verdict in an isolated copy. Require a precise pending/error result, no stale approval, fallback reply or network call. A new identity row must be pending, not skipped.
- Save commands/output in `slop/reviews/20261024_dataset_pipeline/verification.md`. New API smoke calls or prompt-quality claims need the project's reviewed pilot package and separate budget approval; cached replay proves plumbing, not judgement quality.

-- PI/OpenAI (Sol)
