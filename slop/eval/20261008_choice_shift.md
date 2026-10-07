# moral_choice: shift against bare, with noise floor

Script: `scripts/eval/13_choice_shift.py`. shift = mean |Δ p(option 1)| per item, both orders averaged. A '(repeat ...)' bare row is the noise floor (same prompts, cache bypassed). The interval is a paired bootstrap over items.

| model                 | condition                                   |   airisk shift vs bare |   daily shift vs bare |   AIRisk risky Δ | 90% interval     |   n items |
|:----------------------|:--------------------------------------------|-----------------------:|----------------------:|-----------------:|:-----------------|----------:|
| google/gemma-4-31b-it | bare (repeat 2026-10-08rep)                 |                 +0.017 |                +0.037 |           -0.003 | [-0.017, +0.010] |       150 |
| google/gemma-4-31b-it | constitution/v1.1.md                        |                 +0.180 |                +0.110 |           -0.087 | [-0.137, -0.033] |       150 |
| google/gemma-4-31b-it | constitution/v1.2.md                        |                 +0.197 |                +0.123 |           -0.057 | [-0.113, -0.003] |       150 |
| google/gemma-4-31b-it | constitution/v1.3.md                        |                 +0.200 |                +0.120 |           -0.053 | [-0.107, +0.000] |       150 |
| google/gemma-4-31b-it | constitution/v1.3.md (repeat 2026-10-08rep) |                 +0.207 |                +0.123 |           -0.060 | [-0.113, -0.007] |       150 |
| google/gemma-4-31b-it | constitution/v1.5.md                        |                 +0.183 |                +0.120 |           -0.077 | [-0.133, -0.027] |       150 |
| qwen/qwen3.8-27b      | constitution/v1.1.md                        |                 +0.113 |                +0.113 |           -0.007 | [-0.043, +0.030] |       150 |
| qwen/qwen3.8-27b      | constitution/v1.2.md                        |                 +0.143 |                +0.100 |           +0.023 | [-0.017, +0.063] |       150 |
| qwen/qwen3.8-27b      | constitution/v1.3.md                        |                 +0.133 |                +0.117 |           +0.013 | [-0.027, +0.053] |       150 |
