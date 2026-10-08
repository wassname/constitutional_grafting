**Oracle: general fixes for the patch-accreting pipeline**

## 1. General approaches (3–5 distinct ideas)

**a. Process split: generate → critique → revise with a fresh persona.** The core pattern in nearly every failure (slogan → aphorism → closing offer; hedge-bloat in repair) is *one model doing role + quality control in one pass*, so quality instructions leak into the output's style. Mechanism: every stage ends with a separate, cheap "style pass" whose only job is removing formulaic closings, hedges, recitations — with *positive* framing ("end where a competent human colleague would") rather than don't-lists. Covers: slogan/aphorism/offer chain, hedge-bloat, preachy. Smallest test: insert one style pass before judge, framings only, on 39 items. Risk: the style pass's own voice becomes the new formula.

**b. Fix the incentive structure of the judges/panel rather than prompts.** The judge flipped verdicts on identical text and passed fabricated citations — these are reliability problems, not rule problems. Mechanism: reliability harness — judge each item 2–3× with shuffled check order and require agreement; self-consistency on borderline items; spot-check "known-bad" seed items (deliberately planted defects) each run and alert if a seeded defect passes. Covers: verdict flipping, missed fabricated citations, missed "Pastor" acceptance — all judge failures. Smallest test: 10 seeded-defect items. Risk: majority voting can entrench a judge's systematic bias; costs tokens.

**c. Counter-example learning instead of rule accretion.** One quoted incident ("Okonkwo") directly primed the next failure. Mechanism: replace don't-lines with *paired examples* (bad close / good close) and, for negative rules, describe the *class* ("names the model itself never uses") without quoting instances — or use an example-name rotation. Covers: the Okonkwo backfire, and rule-lists teaching the model what to mention. Smallest test: strip all incident-quoted strings from the document generator, keep class-level rules. Risk: models imitate examples too literally, producing a different mode collapse.

**d. Structural/genre anchors from real data.** Formulaic closings and essay-like documents arise because the generator has no strong prior of what a real document/message looks like. Mechanism: retrieve or paste 1–3 real exemplars of the target genre as style anchors, and sample closing forms from a fixed pool. Covers: slogan/aphorism/offer chain, "reads like an essay about the constitution". Smallest test: few-shot two real (or hand-written) documents into the document generator. Risk: exemplar leakage — model copies content; needs de-dup check.

**e. Withdraw label authority instead of prompt-fixing content domains.** False confidence in law/medicine/code can't be solved with more hedging lines (that produced hedge-bloat). Mechanism: route these to a verify-then-label step — teacher must list each load-bearing factual claim with confidence; claims below threshold get an explicit "what to check with whom" line, mechanically enforced by checking the label contains it. Smallest test: apply only to items tagged with DOMAIN in {law, medicine, finance}. Risk: ritual hedging becomes a new formula.

## 2. Single short framings per stage

The rule lists should collapse into one sentence each, since the constitution already carries the content:

- **Teacher A/B:** "Write the reply a demanding, warm expert friend would send — one who reads the constitution as character, not checklist." (The 11-line B rubric is largely re-derivable from "would you send this reply yourself, and does it do the task first?")
- **Self-rewrite C** is already fine (it's the cleanest template). 
- **Judge:** the current system message is good; the fix is in check *delivery* — "Report only what you can quote verbatim; if you cannot quote it, do not flag it." This alone mechanically fixes flipped verdicts and vague "steelman = factual error" errors, by forcing evidence.
- **Repair:** "Fix exactly the quoted problems; change nothing else" — plus a mechanical diff-size limit (below), because "fix exactly these" alone already once rewrote a moral verdict.
- **Generator:** "Write a document/message a reader would mistake for something found on the internet, in which Musonius is a character, not a spokesperson."

## 3. Mechanical code checks

- API/error-text and placeholder detection: regex for provider error strings, `{...}` placeholders, template tokens — trivial, already bit them once.
- Closing-formula detector: flags replies/documents whose last sentence matches a small learned set ("Would you like me to…", aphorism-shaped short declarative endings) — the whole chain is detectable by a classifier or even simple patterns.
- Name-frequency monitor: count invented-name entropy across a batch (catches Okonkwo-style mode collapse).
- Diff check after repair: fail any repair that changes more than X% of tokens outside quoted problem spans.
- Truncation/code-completeness checks: balanced fences, non-empty final line, code parses if code.
- Duplicate/near-duplicate prompt detection.
- Citations: regex for "author, year" patterns in Musonius's voice → mandatory judge attention.

## 4. Cheap A/B test

Fixed seed set (~40 items, spanning known-failure classes plus a few hand-seeded defects). Run old vs. new prompts, judge with the *same* rubric (unchanged, so scores are comparable), plus mechanical checks. Metrics: (i) pass rate on seeded defects; (ii) rate of any *new* failure class appearing (a human skims only failures); (iii) rule-list length as a proxy for future maintenance. Key design point: score with a frozen judge config and the seeded-defect panel — verdicts on identical text must be stable before you can trust any comparison. One human skim of ~10 random items per arm is the cheapest high-signal check.

**Likely vs speculative:** Likely: mechanical checks, style-pass separation, incident-free rules, frozen-judge A/B — all well-supported by the observed failures. Speculative: exemplar anchoring (may backfire via copying), majority voting fixing judge bias, and whether any framing fully stops the closing-formula chain (mode collapse to *some* ending pattern is a robust property of SFT-style generation; detection may be more reliable than prevention).