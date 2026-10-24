# Dataset-pipeline cleanup

> wassname: "dataset building should be repeatable not ad hoc"; "like a DAG with semantic paths?"

Scope: generation, review, repair and assembly of this project's chat/doc datasets. Plan only; no training, new model calls or content changes during the refactor. Keep existing raw/cache locations and training releases; no whole-repo move or new workflow framework.

- [ ] goal: reproduce the datasets already used for training
  - [ ] Pin input files, saved responses, verdicts, configuration, tokenizer revisions, seeds and output hashes for `73`, `76` and `89`; record where private/ignored inputs are stored.
  - [ ] Build into a separate directory; preserve selection order, identity sampling, shuffles and JSON encoding. Preserve historical prompts/decisions, including explicit exclusions.
  - [ ] Investigate the missing `fresh_loop/edits.jsonl`; record it as absent in the historical recipe, not as proof its edits were intentionally rejected. Do not restore unreviewed fixes.
  - failure modes: same row count hides changed replies/order; optional missing inputs silently change results.
  - deliverable: offline replay report matching every pinned output; run10 chatr13 `eea4a788` (1,798 rows), const `d09f8ba0` (1,584), run11 chatr13 `44ae6d30` (different encoding).

- [ ] goal: one executable recipe works on another dataset
  - [ ] Extract/reuse the existing functions in `73`, `76`, `80`, `83`, `86`, `88`; expose input/output arguments through a small `scripts/data/chat_pipeline.py` entry point.
  - [ ] Check in recipes and prompts under `configs/data/`; use `data/interim/<recipe>/<stage>/` and `data/processed/<recipe>/` for new outputs. Keep `data/train/run10/` and `run11/` unchanged.
  - [ ] Connect source → checks → rewrites → refusal review/repair → final checks → assembly in code. Preserve the historical recipe separately from the recipe for new data.
  - [ ] Add `just data-build <recipe> <output>` for offline replay and explicit generation/review/resume commands. A missing cache or verdict stops with the exact pending work; builds never make surprise API calls.
  - failure modes: functions exist but are not connected; a different filename still edits chatr12; moving sampling changes the reference mix.
  - deliverable: the command, declared dependencies and per-stage input/output hashes; no new version-suffix pipeline layers.

- [ ] goal: reviews and repairs remain valid after upstream changes
  - [ ] Put candidate selection, review-batch creation and verdict joining in code; reuse the existing two-pass Sol workflows with parameterised paths. Include identity rows for new chat data.
  - [ ] Bind reviews and repairs to the exact source/request, reply, rubric/constitution and reviewer setup. Preserve original and revised text, objections and acceptance evidence.
  - [ ] Cache effective model requests/responses, including provider/settings and sampling attempt. Imports and offline rebuilds must not load API credentials or call providers.
  - [ ] For new reviews, remove imported bright-line wording; judge facts, weighing, action and ordinary usefulness. Read the complete revised reply/doc for consistency; keyword matches only identify candidates.
  - [ ] Apply the same dependency/cache/review pattern to `85`'s existing source → reasoning → plot → document → check stages; retain full source/prompt provenance and held-out exclusions in `89`.
  - failure modes: an old verdict approves changed text; a sentence repair contradicts the rest; a failed repair silently keeps a known-bad reply.
  - deliverable: resumable review packages, explicit accepted/rejected/pending states and row-level lineage for chat and docs. Missing historical evidence is labelled, never invented.

- [ ] goal: replace the ad hoc instructions without disrupting current runs
  - [ ] Verify replay and the new-input workflow first; then replace redundant build/repair code and update `justfile`, `docs/data_provenance.md` and the existing recipe page.
  - [ ] Keep historical sets reproducible by their pinned recipe; switch future training only by an explicit dataset manifest. Coordinate with the run11 session before changing its entry points.
  - failure modes: two competing current builders remain; active training paths or held-out membership change unnoticed.
  - deliverable: one documented entry point per operation and a committed migration with no changes to the pinned training files.

## UAT / Verification

- Success: rebuild all pinned releases into a new directory offline; hashes match, and selected final rows trace to their source, transformations and reviews.
- Likely failure: use a second input path containing real cached rows; the pipeline must use that input and apply an accepted repair while keeping a justified refusal. Stage logs must show both actions, not merely a successful exit.
- Sneaky failure: change a request/reply/rubric or remove a required verdict/cache in an isolated copy; build must stop with the affected stage/id, never reuse stale approval or substitute another reply. A new identity row must appear as pending, not disappear.
- Save commands/output in `slop/reviews/20261024_dataset_pipeline/verification.md`; check schema, duplicates, loss masks, membership, ordering and held-out separation as well as hashes. Investigate mismatches before changing expected hashes.
- Fresh API smoke calls and changed generation/review prompts require a reviewed pilot package and budget approval; cached replay does not establish fresh-generation quality.

-- PI/OpenAI (Sol)
