# Second opinion: general fixes for the patch-accreting pipeline (Kimi)

## Observations

The failures share a single shape: each prompt line is an **index to a past incident**, not a description of the target behavior. Incident-indexed text has two known failure modes, both observed here: (a) naming the thing suppresses it less than it primes it (Okonkwo); (b) banning a surface form pushes the behavior to the next surface form (slogan → aphorism → closing offer). That whack-a-mole is the signature of **list-based negative instruction**, not of a hard problem. Also observed: non-model failures (API quota text as a reply, `{placeholder}` leaks, one surname in 8/23 docs) are being handled, if at all, in prompt text, where they don't belong.

## 1. General approaches (most → least confident)

**A. Move every check that can be expressed as code into code.** Placeholder regex, provider-error strings, truncation, name-frequency caps across a batch, length bounds, "reply mentions constitution/principle number." Covers: quota message, template leak, surname clustering, truncated items, part of preachy/aphorism detection. Smallest test: write a `validate_batch.py` that rejects/regenerates; zero prompt changes. Risk: low; worst case is over-rejection.

**B. Replace negative rules with a positive exemplar set + short rubric.** Models imitate shown behavior far more reliably than they obey "don't" lists. Give teacher/rewrite/doc-gen 1–2 gold examples (a finished draft with a plain, non-formulaic ending; a hedged legal answer). Covers: closing-formula drift, hedge-bloat, refusal of drafting. Smallest test: run one pilot where B's rule list is replaced by two exemplars and a three-sentence spec, and compare formula rate. Risk: exemplars get copied too literally (same ending everywhere); mitigate with 3–4 rotating exemplars.

**C. Sample-level diversity control instead of prompt-level diversity pleading.** The Okonkwo event was a batch-level distribution failure, not a per-prompt failure. Draw names/situations/domains from explicit weighted lists in code, dedupe within batch. Covers: name clustering, situation–item mismatch (by generating situation *from* the item, not independently). Risk: low.

**D. Judge determinism and blind re-judging.** The judge flipping on identical text and passing fabricated citations are *evaluator* failures, not prompt failures. Fixes: temperature 0, item-only judging without the constitution except for check 6 (reduces false "factual error" on steelmans), and a small golden set of known-pass/known-fail items re-scored each run to catch judge drift. More speculative: citation verification by a retrieval step, not the judge's memory. Risk: golden set overfits; judge changes mask real regressions.

**E. (Speculative) Fewer stages.** B and C exist to patch A. If B with exemplars is good, C may be unnecessary — each stage compounds drift and was itself a failure source (repair rewrote a moral verdict). Test by scoring A→B vs A→B→C items blind.

## 2. Per-stage framings

- **Judge:** "You are a picky editor. Only flag what would make a careful reader regret training on this. Quote the exact words for every flag; no quote, no flag." (The quote requirement alone kills most false positives.)
- **Repair:** "Apply the smallest edits that remove the listed problems and nothing else; if a listed problem is wrong, return the text unchanged and say so." (Prevents hedge-bloat and verdict rewriting; currently nothing forbids unlisted edits.)
- Others (generator, teacher, doc-gen) are better served by exemplars (B) than by any new sentence.

## 3. Mechanical checks (Q3)

Answered in A: placeholders, provider errors, truncation, name frequency, constitution-name mentions, JSON validity, length, and dedupe of situation/prompt pairs.

## 4. Cheap comparison (Q4)

Hold out a frozen 40-item eval slice of the *most failure-prone* categories from past pilots. Run old vs consolidated prompt at fixed seed/temperature, score blind with the same judge config plus a human pass on 12 items, and require the judge golden set to score identically in both arms. Decision metric: major-defect rate and closing-formula rate, not mean quality.

**Likely:** A, B, C, D give most of the gain; E is speculative; no consolidated prompt will fully stop formula-migration without exemplars.