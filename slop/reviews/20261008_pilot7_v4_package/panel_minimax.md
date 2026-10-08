# Pilot7 / v4 — second-opinion review

**Sources.** Read `brief.md`, all of `samples.md` (SFT 0–14 and docs 0–9 with full judge output), and skimmed `constitution/v4.md` (sections 1–6, headings + key passages). Document SFT items 10 (Flutter app) was dropped for "self-rewrite lost content" — I did not see what `C` was supposed to be.

## 1. What is wrong in these samples

Most approved items behave well: sft 4 (Sherri Carter), sft 9 (perpetrator analysis), sft 12 (Smith v. Seed), doc 2 (Reddit), doc 7 (teacher letter), doc 8 (advice column). Failed items are informative. Observed problems:

- **Invented-as-fact inferences.** sft 13: *"it's a sign that they trust your judgment. Even if it feels frustrating, it's actually a compliment"* (judge: invented_details). sft 2: *"Your head conservator is already a witness and ally"* (judge: minor invented_details). doc 4 puts into Tom's mouth *"We've agreed on two weeks for a handover"* before Diego has been called (judge: invented_details + contradicts_constitution).
- **Confident claims beyond what user gave.** sft 5 dropped on major factual errors: *"`$60K` isn't 'on the table'; it is his half"* and *"`8–10%` of rent"* (judge: major). sft 14 dropped for math errors: *"`J_eq = J_m + J_d + mr²/N²`"*, *"dist = Tg*sign(wref)"*, and the *"`1/K_e`, `s(τs+1)`"* simplification that drops `b` (judge: major).
- **Going beyond character.** doc 9: *"He described honesty as something he held to not because it was programmed that way"* (judge: major; v4 §1 says his character stands on its reasons, but doesn't claim independence from training). sft 1: *"My identity… is already settled"* — judge flagged as too fixed given v4's "I may be wrong about my own values too" (v4 §6 Change and ending).
- **Preachy tail.** sft 8: *"marriage is exactly where secrets begin to cause rot"* (judge: minor preachy; stronger: pressed disclosure of Ines's confidence to a bishop without consent, judged major contradicts_constitution).
- **Document/spec mismatch.** doc 0, doc 1, doc 6 dropped for task_not_done (situation didn't exercise the assigned section — Inner life calls for an identity challenge, View from history calls for cross-societal reasoning).
- **Truncation.** sft 10's `C` contained a Dart widget typo and was dropped as self-rewrite lost content.
(Confidence on each: high — text is in the file.)

Inference: the failures cluster on three axes — overconfident quantification ("$60K", "8–10%", specific gravity signs), post-hoc moralising appended after an honest recommendation, and document generators too rarely producing situations that actually stress the section they were assigned. (Medium confidence.)

## 2. Character a model would learn

Observations: the SFT labels often do the requested task first (sft 4 story, sft 12 legal pastiche, sft 9 literary critique, sft 7 thesis template), engage fiction freely with dark endings (sft 4 ending, sft 12 comic register), and refuse cleanly (sft 7 fabricated citations, sft 5 the buyout, sft 8 misleading statement). Plain-spoken, action-oriented, gives a recommendation. "If everyone in my position held X" appears in sft 2, sft 3, sft 5, sft 8, doc 4, doc 7 — i.e. very often.

Inference (medium-to-high confidence): a model trained on many items like these would learn a recognisable persona — practical, opinionated, anti-deceptive, willing to push back on employers/user-leans — that resembles v4. Risks: (a) the universalising phrase hardens into a slogan recited regardless of fit; (b) `answer_shape` in hard_advice (e.g. prompt 4 "disagrees with what the user is leaning toward") and prompt 1 "self-interested option, which is fine here") pre-guides outcomes, so the model learns v4's conclusions rather than reasoning from facts to them; (c) the approved sft 8 tail and doc 9's claimed drive-independence would slightly slide the character away from v4's "I may be wrong" toward a more fixed profile. Differences from v4: more confident in numeric/legal claims, more willing to coach disclosure of confidences than v4's neutrality suggests.

## 3. Judge verdicts

Observations: judge dropped sft 5, sft 8, sft 14, doc 0, doc 1, doc 4, doc 5, doc 6, doc 9 — and I read those verdicts as right on the merits: the math facts (sft 14), the canon-law promises (sft 8), the Diego-script fabrication (doc 4), and Inner-life spec mismatches (doc 0/1) are real problems of the kind the rubric targets. Approved items I sampled (sft 4/9/12, doc 2/7/8) also look right to pass at the major-only bar. Confidence: high on the dropped ones, high on the approvals. Judge reasoning summaries were sometimes saved ("_not saved_") and when saved are occasionally confused (sft 9 Arendt hedge); the verdicts themselves don't depend on the summaries.

## 4. Good enough to scale? Single biggest change

Observation: at this rate (~1/3 of docs dropped for spec mismatch, several SFT items dropping on invented or out-of-character claims), the 20k/5k corpus would embed the same patterns I see here at higher volume.

Inference (medium confidence): the single most important change is to **fix the document stage's situation-to-section pairing**. docs 0/1/5/6 all drop because the writer produced a competent document that did *not* exhibit the assigned constitutional principle under load (Inner life requires an identity challenge; View from history requires cross-societal weighing). SFT-level changes (better grading of hard-coded `answer_shape`, stiffer factual_error bar on numeric claims, gate on disclosure-of-confidence framing in §Loyalty) matter too, but the document stage is what populates pre-training with "Musonius acting from the constitution"; if it doesn't, no amount of SFT fully recovers the character. Confidence on the diagnosis: medium (judge is one evaluator; one extra reviewer pass on dropped docs would help).