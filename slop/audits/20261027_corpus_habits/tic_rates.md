# Teacher-tic rates

Regex counts per 1,000 whitespace words (case-insensitive). Generated = written by the teacher models; human = authentic books. Writer prompts use 'plain', 'weigh' and 'quiet' vocabulary too (configs/data/prompts/).

| per 1,000 words | chat (generated) | const docs (generated) | Stoic (human) | other traditions (human) | constitution v4 |
|:--|--:|--:|--:|--:|--:|
| honest / honestly / frankly | 1.06 | 0.84 | 0.08 | 0.08 | 0.94 |
| plain / plainly | 0.89 | 0.72 | 0.09 | 0.07 | 0.56 |
| quiet / quietly | 0.57 | 0.71 | 0.08 | 0.04 | 0.09 |
| weigh* | 0.45 | 0.40 | 0.06 | 0.06 | 1.22 |
| worth | 0.76 | 0.46 | 0.23 | 0.10 | 0.28 |
| here's | 0.71 | 0.23 | 0.00 | 0.00 | 0.00 |
| I won't | 0.69 | 0.78 | 0.00 | 0.00 | 0.00 |
| em dash | 0.00 | 0.00 | 2.48 | 2.39 | 1.78 |
| not ... but | 0.11 | 0.07 | 1.29 | 0.73 | 0.19 |

-- scripts/scratch/20261027_tic_rates.py
