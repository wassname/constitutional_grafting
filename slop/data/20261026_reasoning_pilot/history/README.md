# Superseded pilot artifacts

These files preserve the earlier blocked attempt, guide drafts/objections, worker reads, and superseded experimental/review selections. They are historical records, not current approvals or executed commands to rerun.

- `kimi_guide_original.md` / `glm_guide_original.md`: first drafts. Final provided guides are `../guides/kimi_guide.md`, `glm_guide_rejected.md`, `opus_guide.md`.
- `worker_guide_read.md`: original/revised-guide review, including rejection reasons. `../guide_read.json` preserves historical acceptance/hash and adds the current reader's revision requirement.
- `worker_read_annotations.jsonl`: four earlier notes (including native-field reads). The current reader does not claim to have read native planning; visible-only full coverage is in `../reader_notes.json` / `reading_manifest.json`.
- `pre_reader_*` and `blocked_opus_*`: earlier outputs, not this full read. Historical command paths still say script 90; maintained entry point is now **`scripts/data/91_reasoning_pilot.py`** (90 generic control is Box A).
- Review selections other than `../review_selection_revision.json` are obsolete. The final frozen selection was not redrawn to replace two missing generations.
- `opus_guide_retry.py.txt` is inert source history of const_v2's one honest-purpose retry. Its completed response is `opus_guide_retry_raw.json`; `primer --condition opus_guide` (legacy alias `P3`) in script 91 replays this cache **without a network request**. It fails rather than sending another Anthropic request. Existing failed/refused responses are retained.

Historical cache IDs (`P0`, `P1`, `P2`, `P3`) and API request files retain their exact spelling so raw rows, cost records, hashes and links remain traceable. Current reports display no_guide, kimi_guide, glm_guide (rejected), opus_guide; source/translation are explicitly named. Logs and frozen requests are not rewritten to pretend the new names existed when requests were sent.

No full book passages have been added; source prompts are constitution/context and synthetic chat cases, including short attributed excerpts already present in v4/training prompts. Do not publish this research cache without editorial approval.

-- PI/Sol (reader)
