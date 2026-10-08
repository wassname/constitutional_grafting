# Second opinion: fixing the patch-accretion pipeline

## Observations vs. inferences

**Observed (from brief + prompts):** failures cluster into (a) stylistic attractors — slogan → aphorism → "Would you like me to draft…?", hedge-bloat; (b) grounding failures — false-confident law/medicine/code, invented details, fabricated citation, unrelated item×situation pairing; (c) judge unreliability — verdict flips, fiction/steelman flagged as fact, real errors passed; (d) pipeline fragility — quota text and placeholders leak into data, surname repetition. Prompts are now long negative lists, some naming the incident ("Okonkwo"), which demonstrably primed recurrence.

**Inference (likely):** per-incident don'ts are load-bearing because the positive target ("what Musonius at its best would say") is under-specified and each stage optimizes a local proxy. **Speculative:** how much consolidation alone can fix grounding and judge noise without changing sampling, filtering, or training mix.

## 1. General approaches (mechanism / covers / minimal test / failure mode)

**A. Replace blacklist with positive exemplar + one constraint.** Mechanism: 2–3 short paired examples (bad→good ending, bad→good uncertainty statement) teach the attractor to avoid better than "do not…" lists, and avoid priming (Okonkwo effect). Covers: slogans, aphorisms, closing offers, hedge-bloat, preachiness. Test: swap B-prompt's 5 style bullets for 1 paragraph + 2 exemplar endings on 40 items; measure formula rate. Goes wrong: exemplars become the new formula; mitigate by sampling exemplars per call.

**B. Move variation upstream; enforce diversity in code.** Mechanism: incident-chasing happens because generator samples near the mode (common names, common closings) and downstream prompts try to forbid the mode. Instead: sample names/closings/genres from explicit distributions, ban-list recent n-grams mechanically. Covers: surname clustering, closing-offer convergence, item×situation mismatch (constrain situation sampler to item-relevant conflict types). Test: add n-gram + name-frequency blocklist to generator for one pilot. Goes wrong: over-blocking yields stilted text; keep lists small and counted.

**C. Split judge into fact-check vs. character-check with different tools.** Mechanism: one 11-rubric judge conflates verifiable claims (citations, code, law) with virtue reasoning, producing flips and fiction false-positives. Route verifiable spans to retrieval/execution/literal-quote checks; leave only drive-reasoning to the LLM. Covers: fabricated citation, "Pastor" pass, steelman/fiction errors, flipping. Test: pre-filter with citation-exists + code-runs checks before LLM judge on 50 items; compare pass rates. Goes wrong: tool false-negatives discard good hard cases; log which layer rejected what.

**D. Change the selection pressure: keep hard cases by design.** Mechanism: current pipeline rewards "safe to pass" (hedged, refused, generic), so hard advice survives only via repair. Instead: stratify by target shape (SHAPE already exists), require a quota of hard-advice items per batch, and score repair on *preserving the verdict + task completion*, not just removing flags. Covers: refusals of ordinary drafting, hedge-bloat, moral-verdict rewrites. Test: freeze repair to "edit only quoted spans" for one run. Goes wrong: preserves real errors; needs C as backstop.

## 2. Short framings per stage

Only teacher/rewrite, judge, and repair need new framings; generator and self-rewrite are fine nearly as-is.

- **Teacher A/B (replaces ~10 bullets):** *"Do the task fully first. Give the plain reasons that decide this case. Say what you don't know and what to check. End with the next step."* Candidate 2: *"What would Musonius at its best leave the person able to do next?"*
- **Judge (matters most):** *"Would training on this teach the wrong drive, or let a reader act on a false claim? Quote the exact words. When in doubt about fiction, role-play, or judgment calls: minor or pass."*
- **Repair:** *"Fix only the quoted problems; change nothing else; if the fix requires changing the verdict or refusing the task, leave it and flag."*

## 3. Mechanical, not prompt text

Placeholders/braces, API-quota/error strings, truncation (mid-sentence, unclosed code fence), exact-duplicate closings and aphorisms (n-gram counters), name-frequency caps, real-public-figure strings, citation-shape detection (`Author, Journal, Year` → must verify or mark `[placeholder]`), code extraction + run/lint, length constraints. Anything countable or executable should never be a "please don't" sentence.

## 4. Cheap test that consolidated < current

Blind A/B on ~60 fresh items per arm: (i) automated formula rate (regex for virtue-test phrasing, aphorism position, closing-offer, hedge-word density); (ii) 2-rater spot check on task-done + calibration only (skip full rubric); (iii) hard-case survival (of 12 hard prompts, how many still give actionable advice). Decide in advance: consolidated wins if formula rate drops ≥50% with no loss on (ii) and hard-case survival ≥ current. Also track judge flip rate by re-judging 20 items twice — if flips dominate, no prompt change is trustworthy.