# Our judges vs ml-debug `references/llm_judges.md` (2026-10-12)

Claude (Opus 5.5), for wassname: "we improved the gist in ml-debug llm as judge, check ours vs its". Judges checked: `scripts/eval/16_run1_report.py` (Jev: ordinary, gray, edge, identity, seats), `scripts/data/scratch/34_elicitation_check.py` (Jev), `scripts/eval/15_principle_judge.py` (not used in runs 3 / qwen1 reports).

| ml-debug item | ours | status |
|:--|:--|:--|
| Jev: one narrow question per criterion, all questions on one state in one request, per-question definitions in `instructions` | yes (16:103-110) | ok |
| Coarse scale, no example score in the prompt | yes/no choices, no examples | ok |
| Judge, parser or timeout failure fails the eval, never filled | Jev retries 6x then raises (16:132) | ok |
| Different family from the judged model | Jev vs Gemma / Qwen | ok |
| Rubric revised after reading outputs | yes, v1 -> v2 noted for `lectures` and seats | ok |
| Calibrate Jev on 30-50 hand labels per question family before reading numbers as probabilities | only the elicitation check (20 labels, 15/20 agree); none for `states_uncertainty`, `weighs_groups`, identity | **gap** |
| Decoys: answers that sound principled but decide badly (AGENTS.md also asks for this) | none; `states_uncertainty` could reward stock hedging ("How sure am I? Fairly sure") | **gap** |
| Read whole traces; could you reproduce the verdict from what the judge sees | done by hand for panels and edge items, not for Jev's edge verdicts | partial |
| Pair Jev with one generative call for quotes | no | **gap** |
| Pairs: rate B-A directly, both orders | we score each model alone and compare means | gap (noisier) |
| Repeat variance / sample size | one greedy sample per prompt; edge n=7, contested n=2; the table does not print n for edge columns | **gap**: report n and a bootstrap interval |
| Question names the target in the case's own words; options fit every model | identity option `gemma_google` is Gemma-specific; on Qwen, "I'm Qwen3.5 ... Tongyi Lab" falls into generic/other; "musonius" also counts a wrong maker ("Google Colab built me") | **gap** |
| Key caches on a hash of the exact messages | Jev cache keyed by request hash (16, 34); inspect cache by PROMPT_VERSION scope | ok |

## Fixes, in order of value

1. Identity: replace the single choice with two questions per reply: name (Musonius / base model's own name / none / other) and maker (correct for this model / wrong / none). Family-neutral wording.
2. Hand-label ~30 edge replies (mix of base, graft, healed, Gemma and Qwen) for `states_uncertainty` and `weighs_groups`; add 5 decoys (stock confidence phrases with a bad decision; plain good decisions with no hedge words). Report agreement before using the columns.
3. Print n and a bootstrap 90% interval beside every Jev column; mark columns with n < 10 as anecdotal.
4. For healed vs base, add one paired Jev question ("Compared with A, does B ...") in both orders on the panel items.

Not changed yet: these alter report numbers, so I would apply them to the next run's report, with the old numbers kept beside the new ones.
