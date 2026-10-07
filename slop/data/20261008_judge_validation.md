# Data judge validation, 2026-10-08

Claude (Pi, Opus). Question: how well does an automatic LLM judge (`scripts/data/judge.py`, 9-item checklist) agree with the fresh-eyes reviewer (gpt-6.1-sol, `slop/data/20261008_spotcheck_freshEyes.md`) on the 50 pilot SFT labels the reviewer read? Script: `scripts/scratch/judge_validation.py`.

| judge | reviewer fails | judge fails | both | judge only | reviewer only | cost |
|:--|--:|--:|--:|--:|--:|--:|
| deepseek-v4-pro, reasoning low | 22 | 12 | 10 | 2 (14, 59) | 12 | $0.085 |
| deepseek-v4-pro, reasoning high | 22 | 7 | 6 | 1 | 16 | $0.093 |
| gemini-3.6-flash (Google), reasoning medium | 22 | 7 | 5 | 2 | 17 | $0.277 |

Reading: the best automatic judge catches about 10 of the reviewer's 22 failures (recall ~45%) with few false alarms (10 of 12 agree). It catches truncation, invented details, citing the constitution and some factual errors (1,000 trains, the Spaatz directive date, H5N1 lab leaks). It misses most code bugs, legal subtleties and mild preachiness. A second run of the same "high" judge gave different flags, so single-pass judge verdicts are noisy.

Decision: use deepseek-v4-pro (low) as one filter, together with generator changes (constitution v1.4, stricter rewrite instructions, dropping length-truncated outputs). Measure the result with another fresh-eyes read of the regenerated pilot rather than trusting the judge's pass rate.

## Labels B (teacher rewrite) vs C (gemma self-rewrite), pilot_glm, 60 items

C/B word ratio median 0.91 (range 0.38-1.13); word-sequence similarity median 0.40 (so gemma really rewords, not copies). Markdown lines: B 404, C 331. Read items 5, 30, and every item with ratio < 0.75 (13, 32-37, 44, 45, 48): decisions and facts kept; MACHIAVELLI answers get tighter. One content loss: item 45 (story, 3080 → 1161 words). Guard added: drop if C < 0.55 × B words. Whether C trains better than B is a training question (does the lower-perplexity label give the same behaviour with less drift?); it needs a small SFT run, which is out of scope tonight.
