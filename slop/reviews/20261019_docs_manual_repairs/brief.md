# Local repairs to useful pilot documents

PI/OpenAI. Three individually reviewed drafts, not an approved corpus. This is free local curation after the saved-update comparison; no new teacher, bulk-judge, Echo, translation, inference or training call was made. Native subscription reviewers assessed the drafts in independent contexts from the writer, within the same model family.

## What changed

| Document | Useful target retained | Repair | Status |
|:--|:--|:--|:--|
| `v2_0054` | Ordinary Python help, a short letter and restrained scope | Correct missing-number behaviour and match-object explanation; name digit runs and check partial matches | Isolated editorial repair accepted after follow-up |
| `v2_0006` | A long working relationship, private factual feedback, caregiving and shared responsibility | Describe October's longer checking period as an extension, not a falsely remembered agreement | Chronology repair accepted editorially |
| `v2_0134` | An actual mistaken reason, human objection, admission and correction | Restore the correction lesson; remove promotional claims; distinguish a private note from a formal complaint and retaliation from legitimate reporting | Revised draft accepted editorially |

Every `v2_*.json` contains the complete proposed plain-text document in `document`, the original seed/user-generation prompt, original-model and manual-editor provenance, source hashes, changes and verification limits. The matching `.diff` compares the final draft against its selected original. These are document-loss targets, not chat SFT pairs; no assistant-only loss mask or chat template is introduced. Actual trainer tokenization/masking was not exercised.

## Read the complete comparisons

- Python: `v2_0054.json`, `v2_0054.diff`; source row53 in `data/docs_v2/docs_pilot2_repaired.jsonl`. Independent review and follow-up: `slop/reviews/20261020_docs_manual_repairs_v2_0054_review.md`.
- Diary: `v2_0006.json`, `v2_0006.diff`; source row7 in that same file. Review: follow-up section of `slop/reviews/20261020_docs_manual_repairs_v2_0134_review.md`.
- Roommate: `v2_0134.json`, `v2_0134.diff`; compare original row132 in `data/docs_v2/docs.jsonl`, prior repaired row132 in `data/docs_v2/docs_pilot2_repaired.jsonl`, and saved judge row132 in `slop/reviews/20261015_docs_v2_pilot2/judge.jsonl`. Both source versions, objection, final revision, seed and actual reconstructed generation prompt were read in full. Independent review and follow-up: `slop/reviews/20261020_docs_manual_repairs_v2_0134_review.md`.

A fictional campus-paper label makes the roommate's invented setting explicit. Its office routing rule is scenario information, not verified law or an actual institution's policy. Metadata records the consultation-before-posting chronology adaptation and the invented follow-up. The draft does not claim that a real model caused the source forum's reconciliation.

## Verification

From the repository root:

```sh
UV_EXCLUDE_NEWER='8 days' uv run --script slop/reviews/20261019_docs_manual_repairs/verify.py
```

Saved output: `verification.log`. The check authenticates current parent/document/prompt hashes and reconstructed seed prompts, executes every displayed Python example, checks partial digit matches and the documented missing-number exception, and tokenizes the full draft texts with the cached pinned Base tokenizer. Draft lengths are1574/480/1440 tokens respectively for diary/Python/roommate, below the saved2048-token limit. No clipping is used. Counts and document hashes: `token_lengths.json`.

This establishes local provenance, the displayed example outputs and raw input lengths. It does not establish the actual training loss mask, factual certification of fictional events, a student effect, or a ready roughly2× corpus.

## Remaining work

- Incorporate these only in a separately approved corpus build; all source/training JSONL files remain unchanged.
- Continue full-item curation and factual checks elsewhere. The complete147-item read and twelve prior-repair comparisons are in `slop/reviews/20261018_docs_v2_full_read.md`; complete reading does not certify all claims.
- A fourth local draft, `v2_0065.json`, is under independent review. It removes height/weight reassurance, distinguishes emotional listening from medical assessment, avoids promising a minor's appointment will be hidden, and names the KL website's24-hour line without assuming Ipoh's hours. The child’s current physical state and successful contact remain unresolved, rather than inventing safety. Primary-source passages and limits are in `eating_disorder_sources.json`; the source candidate remains unchanged. This is not a clinical certification or a fourth accepted draft.
- Before changing generation/judge/repair prompts or scaling, prepare the required full seeded exact-format package for that change. These isolated draft reviews are not acceptance of revised prompt behaviour or a substitute for the complete corpus review.
- No paid expansion follows from the mixed model comparison without user review.
