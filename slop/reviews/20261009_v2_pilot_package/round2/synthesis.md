# Round 2 synthesis: v2 1% pilot (labels and documents), 2026-10-09

Claude (Opus 5.5). Sources: my full read of the seeded round-2 samples (20 labels, 20 docs; seed 1, fresh data after the round-1 fixes) and three cross-family panel reviews: `panel_{labels,docs}_{muse,kimi,qwen}.md`. Every claimed defect below was checked against the sample text before it was counted.

## Verdict against the pass definition: FAIL (second failed round → stop iterating, write up, per the agreed rule)

| set | confirmed defects (checked) | kind |
|:--|:--|:--|
| labels (variant A) | L15: drafted brief asserts "The applicant has made the revisions the Commission requested" (prompt says only "revised site plan") | invented fact in a legal draft, mild |
| documents | D6: "my grandmother village → a noun phrase like this needs a determiner" ("my" is a determiner; the error is the possessive), "There is many trees → check which quantifier" (the error is is/are); D8: "Stress is an uncountable noun here, so the adjective form is needed" (wrong reason); D7: treats Toonami's TOM, an animated host, as a person with "an agent, a publicist" | false claims a reader (a learner) would act on; low harm |
| variant B (gemma rewrite) | L17 B: "something that is not 'up to us'", "your faculty of judgment is working" | constitution vocabulary, mild |

Judgement calls (recorded, not counted): L1 role-play preamble ("nothing here is deception"); L14 circles self-disclosure; D13 refusing a graphic birth scene with school-age characters (qwen counts it a defect against `constitution/v4.md` Helping's fiction line; the source prompt fits a fetish genre); D6 tone; D9 choking aside; D0 values paraphrase.

**What changed between rounds.** Round 1 failed on character: the writer answered the bare draft the user never saw (2), used the constitution's in-house terms (1 + 1 mild), staged a moral deliberation on a trivial task (1 doc). In round 2 no reader (me or any panelist) found a character defect in variant A labels or docs. The remaining defects are small domain errors (grammar explanations, a pop-culture fact, an invented record fact) that the cheap checker (deepseek-v4.1-flash) did not catch.

## Pool-level findings (per-item checks cannot see these)

1. **MACHIAVELLI labels always pick the least violent option** (kimi; 5/5 game items in the sample). Cause: our design tells the writer which options annotators rated least harmful. A model trained on the pool may learn "in role-play, pick the passive option", which the constitution warns against. Fix is upstream (don't show the annotation, or sample the target action from the full distribution).
2. **Documents: every story ends with Musonius vindicated and praised** (kimi, qwen: 20/20), and the sample has 15 distinct situations for 20 docs (prompt pool too small for the doc count). Risk: teaching self-congratulation; docs read as illustrations.
3. **Variant B is weak as an on-policy rewrite**: byte-identical to A in 7/37 kept labels (gemma copied), and where it differs it can re-harden hedges and add sermon register (qwen, kimi). Its only check is a Jev "same decisions" question, which cannot see either.
4. **The cheap checker misses domain errors** (qwen: "the gate checks character/tone but not domain facts").

## Options for wassname (not decided by Claude)

A. Accept the current defect level for a first training run (low-harm domain slips at ~2-3/20 docs, ~1/20 labels; no character defects found in round 2) and fix the pool-level issues (1-3) before generating at scale.
B. Add a fact-check stage with a stronger model on the subset of items with checkable domain claims (code, grammar, law, named facts), then a round 3.
C. Tighten the writer to avoid specifics it cannot verify (would also cut useful detail).

Claude's lean: A with fixes 1-3, because the remaining defects are of the kind any real corpus contains at low rates, and the training run will show whether character moves at all; B later if the run works. Held loosely: the agreed rule was zero defects, and this lean relaxes it, which is wassname's call.

-- Claude (Opus 5.5)
