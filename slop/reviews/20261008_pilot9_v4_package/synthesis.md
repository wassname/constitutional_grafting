# Pilot9 (constitution v4) review: synthesis

Claude (Pi, Opus 5.5), 2026-10-08. Inputs: `claude_read.md` (mine, all sampled items read in full, written first), `panel_kimi.md`, `panel_qwen.md`, `panel_muse.md`; minimax aborted ("Request aborted") after a partial answer, kept as `panel_minimax_partial.md`. Every claim below was checked against the data files.

## Verdict

Hard-advice labels are now good: all four reviewers and I call the passing hard-advice labels ones worth imitating (sft 1 pastor/land, sft 4 pharmacy, sft 10 funeral, sft 12 mural). kimi says "almost" good enough; qwen and muse say no. Remaining blockers are judge reliability and repair side effects, plus a review-package display bug of mine.

## Checked claims

| claim | who | check |
|:--|:--|:--|
| The judge quotes text that is not in documents 2 and 3 ("hallucinated evidence") | kimi, muse, qwen | **my display bug, not the judge**: the package showed the generation-time verdict (on the text before repair) next to the repaired text. Both quotes are verbatim in `text_original`. Fixed: the package now shows before/after, repair history and the final verdict |
| Doc 1 failed at generation and passes in repair with no change | qwen | confirmed: **the judge flipped** on identical text. Now a fail-then-pass gets a third verdict |
| A real check that major quotes are verbatim is cheap | kimi, muse | implemented in `judge.py` (resample if not verbatim). On 115 past major problems, 4 were not verbatim |
| Repair rewrites moral verdicts: sft 7 "go see Yuki tonight" became "let the formal process reach Yuki rather than privately alerting him" | kimi, muse, qwen | confirmed (dropped after 2 rounds). Repair now keeps the recommendation and moral judgement unless a listed problem names it |
| Repair deleted defensible cultural framing (sft 10, Nigerian/Ghanaian funeral honour) | kimi, qwen | judgement call; the judge flagged it major as a sweeping generalisation, muse calls the deletion good |
| Steelman and role-play content judged as Musonius's own claims (engage 2/6 kept) | Claude | confirmed; general judge rule added |
| sft 1 accepts the user's "Pastor" address ("speaking as a friend as well as a pastor") | Claude | confirmed; judge off_persona now covers accepting a human role |
| "Okonkwo" in 8/23 documents | Claude, qwen | confirmed; caused by an example in the generator prompt. Names now sampled per document from a list |
| doc 7 shows Musonius as a forum moderator posting on its own, called "he" | qwen | confirmed; judge off_persona covers acting on own initiative; generator says "it" |
| New tic: closing "Would you like me to draft ...?" (sft 2, 12, 13, 14) | kimi, qwen | confirmed; rewrite prompt now says no formulaic closing offer |
| doc 0 and doc 8 disagree on the same geology question | kimi, qwen | confirmed; doc 8 is a critical essay saying Musonius was wrong, which we asked for, but the two documents give different answers on a checkable fact. Not fixed |
| sft 6 (iPhone) passed with a misleading "Quick Start / iCloud Backup" line | kimi | plausible; minor technical error passed |
| Survivors skew to ordinary items; hard items are filtered | muse | partly: hard advice 10/12 kept, but engage 2/6 and the WildChat factual drops (not repaired). Repair now covers all pools |
| Repair was a no-op on sft 14 | qwen | the repair model returned 20 words four times; the item was dropped (now logged) |

## Changes after pilot9 (pipeline only; constitution frozen)

078aafa: judge verbatim-quote check; off_persona covers human roles and own-initiative acts; role/steelman/fiction rule; repair on all pools; repair keeps verdicts; third verdict on flips; final verdict stored; package shows document before/after; sampled names; "it"; no formulaic closing offers.

## Next

Pilot10 (new seed) with these changes, same review.
