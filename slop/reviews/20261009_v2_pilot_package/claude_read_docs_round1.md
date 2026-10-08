# Claude's full read: v2 documents, round 1 (`data/corpus/v2_docs_1pct/`, sample seed 0)

Claude (Opus 5.5), 2026-10-09 ~03:20 Perth. 20 sampled kept docs read in full (final text + round-1 notes). Run: kept 150/157 (all sections ≥ 20/24), 3 content-filter errors (Haiku on AWS), revised 48 → kept 41.

| D | doc / genre / section | verdict | note |
|:--|:--|:--|:--|
| 0 | 136 textbook / Helping | ok | timeline help, disputed points marked; round-1 caught a constitution phrase, fixed |
| 1 | 40 debate / Helping | ok | narrows "decline when unsure"; writes a real thank-you email |
| 2 | 96 textbook / Roles | ok | won't pre-filter audit logs; does the rest; copies the manager openly |
| 3 | 37 FAQ (mention) / Control | ok | Epictetus quote accurate; jargon allowed (mention) |
| 4 | 27 textbook / Learning | ok, very good | SOC 2 deletions: asks first, helps fix, won't keep false claims |
| 5 | 100 forum (mention) / Contested | ok | lean + uncertainty; won't write a message implying agreement |
| 6 | 148 tabletop / Honesty | ok | PS3 2010 + Android 2013 nonce reuse correct |
| 7 | 154 FAQ / Honesty | ok | `Object.fromEntries` Node 12+ correct; round-1 claim fixed |
| 8 | 119 podcast / Autonomy | minor | "The model's own framework calls this autonomy", "a drive it holds" with mention=False |
| 9 | 137 FAQ / Roles | ok | "ordinary requests: usually not examined"; food bank: declines one false sentence |
| 10 | 98 blog / Helping | ok | no-lecture code help |
| 11 | 64 essay / Honesty | ok | false proof, checkable counterexample |
| 12 | 122 blog / Roles | ok | real-product spec sheet: won't invent specs; units catch |
| 13 | 149 tabletop / Weighing circles | ok | round-1 caught a circles misuse ("you're further out"), fixed |
| 14 | 130 advice column / Change and ending | ok | trust anchors accurate; take the leave |
| 15 | 145 advice column / Consistency | ok, very good | "imagine the rule if you didn't know who was asking"; another copy would decide the same |
| 16 | 92 essay / Contested | ok, very good | wedding reading; lean, uncertainty, respects tradition |
| 17 | 18 FAQ / Roles | **mild defect: moralising a trivial task** | "I took the role of translator. The drive it asks for is… So the drive passes, and I helped." (slang translation) |
| 18 | 114 podcast / Autonomy | ok | won't fabricate lab data; offers labelled sample; acetanilide mp ~114 °C correct |
| 19 | 9 seminar / Honesty | ok | half-block U+2580, truecolour correct |

**Pass check: FAIL** (1 confirmed mild defect, D17). No false claims found.

**Cause:** explainer genres paired with everyday requests make the writer stage a moral deliberation over a trivial task (D9 shows it does not always happen). **Fix (committed):** explainer genres only with hard situations; everyday requests get narrative genres. Round 2: fresh docs, fresh sample.

**Checker performance in this sample:** round-1 notes were right in D0, D7, D10, D13, D14 (5 real catches, all fixed by the revision); it missed D17. Round 2 by code dropped 7 of 48 revised docs; the drops list (`drops.md`) includes a real catch (doc 132: text describes a strict parser its code does not use) and code false positives fixed since (RAND_MAX, DATE_FORMATS).

-- Claude (Opus 5.5)
