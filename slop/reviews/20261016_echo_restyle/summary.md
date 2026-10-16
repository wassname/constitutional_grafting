# Echo restyle test, 2026-10-16 (PI/Claude)

`scripts/data/53_echo_docs_v2.py` on 20 seeded docs of `data/docs_v2/docs_pilot2_repaired.jsonl`; rows in `rows.jsonl`.

Result: **not usable yet; Echo credit ran out after 4 docs** (16 × 402 "Not enough credits for this request's token budget"). Needs wassname to add Echo credit (billing page; API keys cannot read the balance).

API changes found (fixed in the script):
- Echo now requires a `persona` (named writer). We rotate George Orwell / Ursula K. Le Guin / Joan Didion / Primo Levi per row.
- One request at a time per key (429 otherwise): pool size 1.
- Without `max_tokens` the default budget exceeds the credit (402); now set from document length.

The 4 completed rows (observations):

| id | persona | form | word overlap | length ratio | GLM judge | note |
|:--|:--|:--|--:|--:|:--|:--|
| v2_0101 | Le Guin | commentary | 0.43 | 0.54 | changed | "I agree with much of this" -> "say where I differ" (stance flipped in framing); half length |
| v2_0110 | Le Guin | encyclopedia entry | 0.62 | 0.52 | kept | half length (asked within 20%) |
| v2_0011 | Le Guin | review | 0.66 | 1.07 | kept | dropped the rating line |
| v2_0069 | Didion | review (Chinese) | 0.00 | 137 | kept (**wrong**) | output is Echo's English *reasoning*, not a rewrite: budget computed from `split()` words, which is 13 for Chinese text, so Echo ran out mid-reasoning. Judge called it "kept". |

Earlier single success (first try, Didion, board minutes): overlap 0.96, almost a copy.

So far: Echo halves documents or copies them, and flipped one stance; the GLM preservation judge passed a non-rewrite. Bugs fixed: budget by characters; assert finish_reason == stop. Judge needs a surface gate (length ratio 0.8-1.25, same language) before its verdict counts.
