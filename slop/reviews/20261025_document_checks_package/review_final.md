## PASS

No remaining blocker in this narrow review.

- **Row inclusion fixed:** `43_paired_ablation.py` reads each requested model’s exact maths filename and retains missing-maths rows as “not run.” The updated regression covers both cases. The real report includes `r8_a0_b0` at **53/60 maths, 22/22 ordinary**.
- **Default judging preserved:** the supplied historical patch leaves the full judge command and scoring path unchanged for valid existing invocations. The reporting change intentionally preserves fractional credit instead of converting every nonzero score to a pass; binary scores remain equivalent.
- **No accidental character/API scoring:** capability-only mode exits before credential loading and judge execution. Character columns are absent from the inspected document report.

Ordinary remains a narrow 11-case set sampled twice, not broad usefulness or moral coherence. Tests and smoke results were inspected, not rerun.