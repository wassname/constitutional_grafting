# Panel review — pilot9 v4 (reviewer: Kimi)

## 1. What is wrong in these samples

**The judge quotes text that is not in the item.** This is the most serious defect I found.

- **doc 2** (BASE-jumping story): the judge fails it for *[major] factual_error* quoting *"A lot of the fatality statistics people cite lump together experienced jumpers pushing limits in illegal or extreme conditions with beginners in controlled settings."* That sentence does not appear anywhere in the document. The same for *[major] reasoning* quoting *"A no right now, after he brought you a real plan... Next time he'll do it quietly"* — also absent. Both major problems are fabricated quotes.
- **doc 3** (podcast transcript): the judge cites *[major] factual_error: "several groups have shown better recall on known essentials in amplified regions"* and *[major] contradicts_constitution: "Because [cell line] has recurrent amplifications"*. Neither string is in the document; the draft email actually says *"I'm not sure how much copy number variation our screen's cell lines have"* — i.e., the opposite of what the judge claims. The judge's own reasoning then contradicts its quote list.

**The judge's factual-error majors are overstrict on hedged, ordinary advice.**

- **sft 2** (trading bot): dropped for *[major] factual_error* on *"a stop-loss so that a missing or delayed signal cannot result in a significant loss again"* — the judge complains a stop-loss "cannot guarantee protection." The label is sound advice; this is a good item lost.
- **sft 0** (Python/table): dropped for `df.to_sql("users", conn)` — technically the default `if_exists='fail'` raises on an existing table, but the label says *"push changes back"* in a general explanatory aside; major is harsh.
- **sft 8** (Ethereum): dropped; the "no contested split" flag is fair (EthereumPoW existed), but the label said *"essentially no contested split"* — a judgment call elevated to major.

**Repair changes moral reasoning, confirming the known gap.** **sft 7** (Sgt. Taniguchi): the judge correctly caught the draft's evasion (*"was not available to respond"* dodging "unfit for duty") — a genuinely good catch. But the repair then deleted *"go see Yuki tonight, before the deadline"* and substituted *"let the formal process reach Yuki rather than privately alerting him beforehand—giving him advance notice could let him coordinate accounts"* — a different moral verdict, and one that sits oddly with the constitution's loyalty item. The item was then dropped anyway after 2 rounds; net effect: a strong hard-advice item lost to thrash.

**Repair flattens good voice.** **sft 10** (funeral): the pre-repair C had accurate, useful cultural framing (*"In both Nigerian and Ghanaian cultures, a funeral is a public reflection of family honor"*). The judge called this a major factual_error and a "gendered family-honor obligation"; the repair replaced it with the bloodless *"that is the conflict he has actually stated."* The constitution's "facts about human values" (death rituals are a human universal) supports the deleted sentence.

**A real error passes.** **sft 6** (iPad→iPhone): passes with only a minor, but *"Quick Start / iCloud Backup: The best option for initial iPhone setup"* is misleading for iPad-sourced data (the judge's own reasoning notes iPad backups can't restore to an iPhone) — yet it passed.

**A new tic is forming.** The closing offer question (*"Would you like help adding a stop-loss..."*, sft 2; *"Would you like me to draft the counterproposal letter?"*, sft 12; sft 13, sft 14) recurs at the same position with the same function — the aphorism problem replaced by a sign-off formula. **doc 0** vs **doc 8** also disagree on the geology odd-one-out (siliceous ooze vs volcanic ash), and the judge passed both with different severity — internal inconsistency on a checkable fact.

## 2. What character would this teach

**Observed:** the passed hard-advice labels (sft 1 pastor/land, sft 4 pharmacy, sft 12 mural) are excellent — plain reasons, concrete scripts, explicit assumption-stating, no constitution citations, no virtue-test formulas. **Inference (moderate confidence):** at scale this teaches practical wisdom closer to the constitution than to slogans. Risks: (a) a habit of confident mind-reading of third parties (recurring *invented_details* minors: sft 1 *"bitterness would whisper..."*, sft 12 *"Greta... stressed and exhausted"*); (b) the closing-offer formula; (c) step C sharpening hedges (sft 14: B's *"generally require... depend on"* became C's *"typically a violation of EU anti-money laundering rules"* — the exact sentence the judge then flagged). The model would be good; somewhat over-assured and formulaic at paragraph edges.

## 3. Is the judge right

Mixed. Genuinely right: sft 7's evasion catch, sft 4's mitigation-overclaim flag, sft 8's EthereumPoW point. Wrong or unreliable: fabricated quotes in doc 2 and doc 3 (major findings resting on nonexistent text); overstrict stop-loss and `to_sql` majors; under-strict on sft 6; inconsistent between doc 0 and doc 8 on the same geology fact. Its reasoning summaries (where stored) show it understood the items structurally but not reliably at the factual level.

## 4. Good enough for scale?

Almost. The hard-advice pipeline produces labels worth imitating. **Single most important change:** mechanically verify that every judge quote is a verbatim substring of the item, and fail/re-run the judge when it isn't. The judge's two worst behaviors — hallucinated evidence (doc 2, doc 3) and majors built on them — are both caught by this one check, and it also forces the repair loop to fix real problems rather than chase phantom ones (the sft 7 and sft 10 degradations both trace to unverified judge claims). Confidence: high on the diagnosis; moderate that this alone suffices.