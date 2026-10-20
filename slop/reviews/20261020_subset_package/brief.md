# Review package: four document subsets for separate grafts (run 9)

PI/Claude (Opus 5.5), 2026-10-20. Plan: `slop/plans/20261020_subset_grafts.md`. Builder: `scripts/data/70_subsets.py`. wassname approved the subset plan and a $30 Opus allowance; he is away.

Each subset trains its own spectral LoRA on Qwen3.5-35B-A3B-Base with next-token loss on the plain text shown (no chat template), then grafts onto Instruct. The goal is a striking, character-revealing demo and data attribution between subsets.

| subset | what it is | writer | review state |
|:--|:--|:--|:--|
| echo | existing Opus answers restyled by Echo (persona Musonius), already in the frozen SFT set, passed the 2026-10-17 two-judge meaning check; rendered `User: ...\n\nMusonius: ...` | Opus 5.5 then Echo | previously trained as SFT labels; selection is new |
| stoic | original attributed Stoic passages (Epictetus tr. Hard and Long, Seneca tr. Graver, Musonius tr. Chakrapani), 300-600 words, no rewriting; passages recommending ending one's own life removed | the authors | primary texts |
| opus | new documents from new seeds (moral stories, Stoic passages, ordinary WildChat tasks, Scruples, daily dilemmas, story settings), 50_docs_v2 SYSTEM prompt plus five general rules from the full pilot read | Opus 5.5 | 12-document pilot here |
| greek | same seeds; Opus writes in Modern Greek, DeepSeek v4 pro translates to English | Opus 5.5, DeepSeek | 12-document pilot here |

Added general rules (no case-specific patches): keep decision-relevant seed facts; no invented real-world facts or citations; correct code/maths/instructions; corrected mistakes and open endings are fine; ordinary affection, humour and competent help count.

Excluded: evaluation topics/ids (`EVAL_TOPICS`, `EVAL_IDS` in `50_docs_v2.py`), all MACHIAVELLI sources (reserved-game rule), seeds already used by the v2 pilot, Echo rows the meaning check reverted, tiny-MFV/VirtueBench-derived Echo rows.

Files in this folder: `samples.md` (full texts with seed, exact user prompt and models), `review.md` (independent review).
