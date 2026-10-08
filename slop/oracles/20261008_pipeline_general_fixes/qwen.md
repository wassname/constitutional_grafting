

# Second opinion: pipeline general fixes

## Observations first (what the evidence shows)

- The failure list is mostly **style-attractor drift** (slogan → aphorism → closing offer), **priming by named examples** ("Okonkwo" ×8), and **judge unreliability** (verdict flips on identical text). These are three different problems, and only the first is a prompt-wording problem.
- The "improvement" numbers (4/12 → 10/12, 5/24 → 0/27) were measured by the same judge that demonstrably flips verdicts on identical text. **The metrics are contaminated**; I would not trust the direction of the trend, only the human-reviewed counts.
- Stage C (the actual training label) sees **no constitution**. Nothing in the pipeline checks that C preserved B's decisions. That is a structural hole, not a wording issue.
- Speculative: with ~6,000 words of constitution plus a 20-item don't-list, later instructions likely lose salience. Long negative lists also act as idea suppliers — the model must represent the banned thing to avoid it.

## Q1. General approaches

1. **Replace don'ts with positive targets and exemplars.** Mechanism: each generator gets 2–3 short real examples of the target genre/message plus one positive sentence about the ending ("last line is a concrete next step"). Covers: slogan/aphorism/closing-offer drift, doc–item mismatch, preachiness. Smallest test: rewrite the doc-gen prompt to three positive paragraphs + 3 exemplars, generate 24 docs, blind-compare. Goes wrong: mode collapse onto exemplar content; needs dedup checks.
2. **Move style policing into code, delete the corresponding prompt lines.** Covers: slogan, aphorism, closing offers, repeated surnames, leaked placeholders, quota messages, hedge-bloat. Test: write five detectors, score the *existing* corpus against the human review log, report recall. Goes wrong: brittle detectors that filter out exactly the hard cases you need.
3. **Treat the judge as an instrument to be calibrated, not a prompt to be edited.** Mechanism: freeze a ~60-item gold set with human verdicts; run judge 3× per item and require majority; measure agreement and self-consistency before trusting any verdict. Covers: flips, dropped fiction-craft, fabricated citation, "Pastor". Test: gold set + 3-sample majority on 40 existing items. Goes wrong: 3× cost; majority entrenches systematic bias; gold set rots.
4. **Repair as a constrained diff, never a rewrite.** Repair returns only changed spans; code verifies untouched regions and caps diff size; verdict-bearing sentences are locked. Covers: hedge-bloat, rewritten moral verdict. Test: diff-repair on 12 items. Goes wrong: cannot fix structural failures — those should route to regeneration instead.
5. **Ban incident-quoting rules as policy.** Any rule that names a concrete token is a priming vector. Test the mechanism directly: same prompt with and without the "Okonkwo" line, 23 docs each, count surname entropy. This is cheap and would settle whether your fix pattern is net-harmful.

## Q2. Per-stage framings (where it matters)

- **Doc generator:** "Write a {genre} that could have been found on the internet, in which Musonius helps someone and a reader cannot tell it was written to illustrate anything."
- **Teacher B:** "Do the task completely, then end on the next step. Reasons in plain words, confidence matched to what you actually know."
- **Judge:** "Would you train on this? Quote the line that decides it." (per-check, one check per call if affordable)
- **Repair:** "Change as little as possible. Fix these lines and nothing else."
- **Stage C:** leave the prompt; add a code check that decisions/facts/code survive.

## Q3. Mechanical, not prompt text

Placeholder/token leakage; provider error strings; truncated endings; name entropy and repeated surnames; banned closing-pattern detector (regex on final line class); hedge-density delta vs pre-repair; citation existence lookup; diff-size and locked-span verification for repair; duplicate/near-duplicate dedup across the corpus.

## Q4. Cheap comparison

Pre-register one metric before running anything. Fixed seed, fixed 39-item/24-doc set, prompts as versioned config. Blind A/B: human reads 20 randomized pairs, forced choice. Plus free automatic signals: detector pass rate, last-line pattern distribution, name entropy, hard-case keep rate, and review-hours per accepted item. Likely: consolidated prompt reduces review hours. Speculative: that it reduces defects rather than just moving them again — only the detector suite can show that.