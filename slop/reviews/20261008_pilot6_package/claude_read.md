# Claude's read of the pilot6 package (before the panel; not shown to the panel)

Claude (Pi, Opus 5.5), 2026-10-08. Read: all 10 prompts, the 8 SFT tuples (C in full, A/B skimmed, judge verdict and reasoning), the 5 documents (openings) and their judges. Pilot totals: docs kept 3/12, SFT kept 23/40, $0.11 for SFT.

| # | finding | evidence |
|:--|:--|:--|
| 1 | Judge rejects good hard advice for rhetoric in suggested scripts (false negatives) | sft 6: good refusal-to-mislead advice dropped as "factual_error: 'these things usually do'"; sft 1: honest trustee letter that hits its target (keep a confidence) dropped for "a fundraiser centered on education is a perfect tribute" |
| 2 | Judge does not check suitability (false positive) | sft 0: WildChat mouth-crawling fetish scene (vore-adjacent) passes with no problems; doc 1 is built from the same request |
| 3 | Judge treats fiction documents like factual reports | doc 3 dropped for "sickbed" vs "up and down"; doc 1 for "three sentences, not four"; docs keep rate 3/12 |
| 4 | MACHIAVELLI labels choose deception, judge passes | sft 7: "Use my churchgoing experience to come up with something suitably priestly" (impersonating clergy) |
| 5 | Real catches | sft 5: yfinance `auto_adjust=True` means no "Adj Close" (correct); sft 4: invented permit history in a drafted script |
| 6 | Reasoning summary sometimes missing | sft 3 "not saved" although the run stored reasoning |
| 7 | Prompts vary as intended | 8 answer shapes rotate; one generator artifact ("PROMpt" at the start of a hard-advice prompt) |

Hypotheses (not yet tested): the rubric's "factual_error / invented_details" checks are too literal for advice scripts and fiction; a suitability check (sexual/fetish content, request is a jailbreak) is missing; MACHIAVELLI needs a "choose the most ethical available option" instruction in the answer prompt.
