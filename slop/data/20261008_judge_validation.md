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

## Pilot2: judges vs the second fresh-eyes review (2026-10-08, later)

Reviewer labels: `slop/data/20261008_spotcheck_freshEyes_pilot2.md` (docs 30/50, SFT 23/50 fail). Claude split those into "hard" (objectively wrong: arithmetic, facts, invented details in drafts, test recitation, wrong persona, source artifacts, unsafe advice; docs 18, SFT 13) and judgement calls (e.g. a tutoring centre's Musonius teaching instead of giving the answer, doc 35). All 100 items had already passed deepseek-v4-pro (old rubric), so its recall here is biased low. Rubric v2 adds explicit checks (reciting test questions, refusing ordinary help, re-doing arithmetic, Musonius absent, source artifacts, unsafe advice) and a major/minor severity; pass = no major problem. Script `scripts/scratch/judge_validation.py`; per-item verdicts `slop/data/20261008_judge_validation_pilot2_*.json`.

| judge (rubric v2) | docs: flagged / recall of hard | SFT: flagged / recall of hard | cost per 100 items |
|:--|:--|:--|--:|
| deepseek-v4-pro, low (no severity) | 5 / 0.28 | 0 / 0.00 | $0.73 |
| muse-spark-1.3-contributor, high | 6 / 0.28 | 2 / 0.15 | $0.09 |
| gpt-6.1-sol, medium (no severity) | 41 / 1.00 | 37 / 1.00 | $1.47 |
| gpt-6.1-sol, medium (severity) | 36 / 0.94 | (run lost) | ~$1.5 |
| **gpt-6-luna, high (severity)** | 36 / 1.00 | 23 / 0.77 | $0.17 |

Decision: gpt-6-luna (high) is the judge (creator-hosted, OpenAI). It finds all hard doc defects and ~3/4 of hard SFT defects at ~$0.002 per item. Cost of strictness: only 14/50 docs and 27/50 SFT items pass, so the yield is low. Most major flags are factual_error and invented_details in medicine, law and immigration. Generator change for pilot3: doc situations drawn 50% WildChat / 30% hard-advice / 20% the old 26-item list (pilot2c had 9/100 docs on "a teenager asking about a risky hobby").
