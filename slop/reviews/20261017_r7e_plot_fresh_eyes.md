# Fresh-eyes read of the run-7e λ plot (sol subagent, openai-codex/gpt-6.1-sol, 2026-10-17)

Given only `slop/eval/run7e/dose_frontier_lam.png` and its table (first version, which also showed the plain graft from run 7d). Reply verbatim:

> 1. **What it shows:** Increasing graft dose generally improves judged character relative to SFT-only, but reduces capability-check passes. Spectral penalties appear to improve that trade-off.
>
> 2. **Best-looking setting:** **λ=5, k=0.75**: character +0.50 with 80% capability—the strongest observed combination. At k=0.5, λ=5 retains more capability but has lower character than the weaker penalties. Confidence in a winner is limited: the 90% error bars overlap substantially, with only 59 character items and 44 capability checks. These are suggestive rankings, not demonstrated differences.
>
> 3. **Confusing/misleading:** The plain curve uses run7d and its own SFT reference (89% capability), whereas spectral curves use run7e (86%). Thus the character zeros represent different references; this is not a clean controlled comparison. The legend identifies the different run but not that normalization caveat. Dose labels overlap near several points and around zero; the bottom annotation is clipped.
>
> 4. **One improvement:** Put plain7d in a separate panel with its own explicitly named SFT baseline.

Change made: the plot now shows only the run-7e λ curves (one box, one SFT reference).
