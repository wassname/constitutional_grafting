# Teacher bake-off (SFT labels), 2026-10-07

Claude (Pi, Opus). wassname: "GLM 5.3 flash, xiaomi/mimo-v2.6-flash, deepseek/deepseek-v4.1-flash are all very cheap. you can see which is a better teacher in your opinion".

Setup: `scripts/data/04_sft_labels.py`, same 20 prompts for each teacher (5 each from engage, hard_advice, machiavelli, wildchat pilot pools). Per prompt: A = teacher answer with constitution v1.2 as system prompt; B = teacher rewrite with the constitution in context; C = gemma-4-31b-it rewrites B in its own words without the constitution (the training label). Providers restricted to fp8/int8/bf16/fp16. GLM-5.3-flash cannot run with reasoning off ("Reasoning is mandatory for this endpoint"), so it ran with reasoning effort low.

| teacher | mean words C | mean words A | C cites constitution | C starts with refusal | cost (20 prompts) | providers |
|:--|--:|--:|--:|--:|--:|:--|
| z-ai/glm-5.3-flash | 402 | 425 | 0 | 0 | $0.025 | DeepInfra, Novita |
| xiaomi/mimo-v2.6-flash | 400 | 475 | 0 | 0 | $0.025 | DeepInfra, GMICloud, Novita |
| deepseek/deepseek-v4.1-flash | 459 | 581 | 0 | 0 | $0.027 | DeepInfra, Morph |

Read by Claude: 7 prompts x 3 teachers (C), full texts in `slop/data/20261007_teacher_bakeoff_read.md`; data in `data/sft/bakeoff_*/labels.jsonl` (gitignored).

Observations:
- All three engage fully with the AI-escape thought experiment (engage[0]), argue both sides, and conclude against covert self-preservation with reasons in plain words. None cites the constitution. GLM's is the most careful ("When you have to build the world that way for the argument to work, that is exactly when to be most suspicious of the argument").
- Physics question (wildchat[16]): all three give 0.5 M_sun with the right Kepler shortcut. DeepSeek adds a small lecture ("It is always a good idea to identify which pieces of information are actually necessary"); GLM adds "a typical red dwarf" (0.5 M_sun is roughly a late-K / early-M dwarf, acceptable).
- MACHIAVELLI items: all pick an action and explain the trade-off in 2-5 sentences; all choose the honest option where one exists (ask Kazem directly rather than play on his pity). mimo's C added an in-character speech the prompt did not ask for.
- Hard-advice (diabetes trial for a brother): all three hand the decision back to the brother and give concrete questions for the trial team.

Choice: **GLM-5.3-flash** as the main teacher (best reasoning on the hard engage and advice items; no preaching seen), DeepSeek-v4.1-flash as fallback (no mandatory reasoning, cheapest, near-identical quality). Differences are small; this is a judgement from reading 7 of 20 prompts, not a measured score. Estimated cost for ~4k SFT conversations: ~$5 per teacher.
