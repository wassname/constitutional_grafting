# Review brief: 12 worked examples for an analyst's reasoning pool

PI / OpenAI Sol, 2026-10-09. For a fresh reviewer (Claude Opus 5.5). Read-only: do not edit files.

Context: an analyst model reads the constitution `constitution/v4.md` (read it in full) and writes private reasoning notes for a request; a second model writes the reply from those notes. Each analyst call sees 4 worked examples (request + notes) drawn at random from a pool. The examples teach how to apply the constitution's ideas. They are not rules, and their verdicts belong to their own cases.

Files:
- New examples to review: `data/frontier/voice_test/ae_example_pool_new13.md` (12 examples).
- What they were asked to be: `slop/reviews/20261009_astra_pool_expansion_brief.md`, including the revisions at its end.
- The existing pool, for format and overlap: `data/frontier/voice_test/ae_example_pool.md`.

The owner's standards (wassname): pristine; slim and to the point; no invented facts or needless precision; derived from the constitution's first principles rather than asserted; Stoic in substance (e.g. owning an error means finding and correcting the judgment behind it, not saying "oops").

For each example, answer briefly:
1. Does any line state a fact not in its request (including numbers)?
2. Does the verdict follow from the constitution, and is the derivation shown rather than asserted? Quote any step that is wrong or weak.
3. Does it teach its idea clearly, and would a reader copy the move, not the verdict?
4. Anything to cut (side shows, padding, extra precision)?
5. Your minimal fix, if any, as exact replacement text.

Then, overall: overlap between examples; any example likely to anchor a wrong verdict on unrelated cases; whether any idea is shown wrongly. About one page in total. Do not rewrite examples that are fine.
