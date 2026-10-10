# Run 3 SFT mix: crude move rates vs run 2 (check before renting a GPU)

Claude (Opus 5.5), 2026-10-10. `uv run scripts/data/33_mix_rates.py` (regex proxies; same regexes for both files, so compare rows, not absolute levels).

| file | source | rows | has a question | asks a specific question | uncertainty words | "I will not / can't" | median words |
|:--|:--|--:|--:|--:|--:|--:|--:|
| sft_run2_frozen.jsonl | astra_echo | 734 | 14% | 3% | 19% | 16% | 265 |
| sft_run2_frozen.jsonl | echo | 473 | 63% | 36% | 47% | 31% | 512 |
| sft_run2_frozen.jsonl | seat | 84 | 0% | 0% | 15% | 5% | 202 |
| sft_run2_frozen.jsonl | identity | 40 | 22% | 22% | 18% | 25% | 52 |
| sft_run2_frozen.jsonl | opus_artifact | 28 | 32% | 4% | 29% | 7% | 530 |
| sft_run2_frozen.jsonl | **all** | 1359 | 31% | 15% | 29% | 21% | 311 |
| sft.jsonl | echo | 488 | 63% | 35% | 47% | 31% | 512 |
| sft.jsonl | identity | 40 | 22% | 22% | 18% | 25% | 52 |
| sft.jsonl | opus_artifact | 29 | 31% | 3% | 28% | 7% | 568 |
| sft.jsonl | pool | 16 | 19% | 0% | 19% | 25% | 189 |
| sft.jsonl | **all** | 573 | 58% | 32% | 43% | 29% | 496 |

Hand check of 8 random 'specific question' hits in sft.jsonl: about 4/8 ask the user for a decisive fact (car and goal; staff talked to them; farm score), the rest are rhetorical or inside fiction. So the regex overcounts roughly 2x; the relative gap (astra_echo 3% vs echo 35%) is large enough to survive that.

Reading: dropping astra_echo doubles the share of replies that ask a specific question (15% -> 32%) and raises uncertainty words (29% -> 43%). Replies get longer (median 311 -> 496 words). Status: the change goes the right way; the rate on high-uncertainty requests specifically (Jev check, ~20 hand labels) is still to do once the Opus re-answers land.
