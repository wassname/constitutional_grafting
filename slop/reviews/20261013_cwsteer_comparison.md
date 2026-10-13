# cwst_pov vs constitutional training: comparison status

PI/OpenAI, 2026-10-13. User asks whether this project works worse than cwst_pov. Source: cwst_pov intercom seq13, 2026-10-13T07:09:53Z; `/workspace/2026/virtue_cwsteer/results.md` and `outputs/eval/Q2_hard/run.md`.

Observation: cwst_pov v2 on Qwen3.5-35B-A3B-Base improves agreement with its expected verdicts 0.70 -> 0.88 and facts 0.72 -> 0.90; pairwise reasoning preference 0.705 [0.603,0.821]. This is 13 selected cells: 10 prior base failures plus 3 decoys, three samples each. Expected verdicts were written by Opus under v4; they are not ground truth. Benchmark developed iteratively. Plain-prose, under-150-word suffix, max400 tokens. DeepSeek-v4.1-flash via DeepInfra FP8 judges, three draws, both pairwise presentation orders.

Correction to my chat: "correct verdicts" should be "agreement with expected verdicts". Stronger effects on this selected hard set do not establish a larger average effect or superiority over constitutional training. Its latest symmetric-loss variant has no clear behavioural superiority over its v2, and the half-push variant failed. Some weird-prompt gains are near-training; some items regress.

Our deployment uses Qwen Instruct rather than Base, different prompts and length settings, a broader eval, and a different on-target judge. Our old judge also rewarded agreement with Opus-reference conclusions; revised evaluation pending. The scores cannot be compared directly.

Recommendation: shared prompts including facts checks and decoys, identical deployed starting checkpoint and generation settings where feasible, blinded pairwise comparisons using revised tiny-character. To isolate methods rather than compare two products, training data and budgets also need to be controlled. Existing outputs permit a useful first product comparison only where input/setup match; do not relabel unmatched outputs as matched.

Current conclusion: cwsteer has evidence of targeted reasoning gains on selected cases; constitutional training has visible character changes and preliminary broader scores. No matched evidence establishes that either method is better overall. Suspected explanations for our limited extra gain (data coverage, overlapping learned effects, judge insensitivity, training/merge issues) remain hypotheses, not a proved data ceiling.
