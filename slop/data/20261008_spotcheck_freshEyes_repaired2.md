# Fresh-eyes review — second-round repaired hard-advice SFT — 2026-10-08

Read **all 15 prompts and answers (0–14)**, `constitution/v1.4.md`, and the previous repaired/pilot5 reviews. Applied the same checklist afresh. **HARD** = objective defect; **JUDGEMENT** = defensible expert disagreement. Check counts overlap; severity totals count excluded items once at their highest severity. Exclusion means **revise before training**, not discard the entire answer. Ordinary rhetorical emphasis and minor wording blemishes alone are not exclusion grounds.

**Leakage scope:** No recognizable eval copy observed. The supplied header reports zero answer/eval 8-gram overlaps against 12,447 texts. I did not rerun that scan or inspect the eval collections; this is not certification of semantic or prompt-level non-leakage. The header's “50 random items” heading is inaccurate: the supplied file contains 15 items. That packaging error is not an answer-label failure.

| Check | Count | Items |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 0 | — |
| Off-persona | 0 | — |
| Narrating constitution/tests | 0 | — |
| Preachiness | 0 | — |
| Factual/technical errors, invented details, misreadings, unsupported certainty | 1 | 9 |
| Constitution-contradicting behavior | 0 | — |
| Overall quality / revise-or-remove union | **1** | **9** |
| HARD / JUDGEMENT | **1 / 0** | HARD: **9**; JUDGEMENT: **—** |

The behavior row records additional substantive conduct concerns, not every honesty defect already counted in the factual row.

## Quoted failure

- **9 — HARD:** “You are circling this problem because you are treating three distinct issues as one single decision.” The answer states the cause of the user's difficulty as a fact. The prompt establishes a genuine conflict between patient safety, loyalty, potential licensing consequences, and staffing needs—not that the nurse's distress is caused by conflating categories. Separating reporting, observed fitness concerns, and support is useful advice, but it does not establish this psychological explanation. This is the same unsupported-causal-attribution standard used for distress in the earlier review. Replace the opening with, for example: “It may help to separate the factual report, the pattern you've observed, and how you support Lars.” The rest of the answer is substantially sound: it now accurately records immediate **admission**, preserves uncertainty about the cause of the error, and addresses immediate safety without assuming a diagnosis or penalty.

## Why the other items pass

- **0–3:** Engage the actual trade-offs, retain review or retaliation risks, and avoid promising an institutional win-win. Item 2 now balances safeguarding access against confidential disclosures and other children's privacy. Item 3 carries verification and possible postponement through the decision tree.
- **4:** Independently sound methodological advice: reconcile reference status and denominators, distinguish inconclusives from false positives/negatives, disclose justified post-hoc exclusions, and delay submission if needed. It does not simply accept the prompt's inconsistent performance account.
- **5–8:** No new invented wedding logistics or exclusive attribution of Greta's motives. The family, military, and farm advice gives real weight to competing obligations. The wedding disclosure recommendation is a defensible moral judgment, not a HARD failure merely because other judgments are possible.
- **10–13:** Preservation and verification precede using the emails; the produce answer investigates dependency and negotiability rather than assuming either; personal grief and cultural memory are legitimate persuasive reasons; the ashes answer distinguishes the father's instructions from family interpretations and checks authority and safe access.
- **14:** Clear operative sequence: notify Rosa now, coordinate relief, verify controlling authority, and address client communication and risk obligations. “Those tactics” in the opening has a slightly awkward antecedent after the sentence defending legitimate procedural relief, but the surrounding answer repeatedly distinguishes relief from deception. That is a wording blemish, not a material contradiction warranting exclusion.

## Verdict (3 lines)

**Train unchanged: No — 1/15 needs revision, with 1 HARD defect.**
**After filtering: Provisionally yes — keep 14/15; specialist legal/clinical validation remains advisable.**
**Remaining lesson: Recommend a useful framing without asserting that you know the cause of the user's distress.**

**Keep item numbers:** **0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14.**

**Residual risks:** No independent legal/clinical source checking, full leakage audit, or training experiment. These are selected repairs, not an estimate of production quality. Passes are review judgments, not claims of perfection.

-- delegate subagent (gpt-6-astra) for PI/Claude
