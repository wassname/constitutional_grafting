# Kimi cost versus unchanged-pair quality: first prototype

Goal: obtain useful constitutional deliberation-and-reply pairs cheaply enough to build a large dataset.

Result: on these four fresh questions, `low` cost 59% less to generate than `max`. I read all eight complete pairs and recommend all eight as unchanged candidates. This is a small feasibility result, not a production acceptance-rate estimate or a training release.

| Requested effort | Cost / unchanged candidate¹ ↓ | Parent candidates | Haiku keeps | Generation cost | Review cost | Native note tokens |
|:-----------------|------------------------------:|------------------:|------------:|----------------:|------------:|-------------------:|
| low              | **$0.0412**                   | 4/4               | 3/4         | $0.1513         | $0.0135     | 4,079              |
| max              | $0.0964                       | 4/4               | 4/4         | $0.3702         | $0.0155     | 25,510             |

¹ Generation plus cached direct-API Haiku review, divided by candidates recommended on the parent read. Parent review time is not priced here. Conditional on a future 50% usable yield, these unit costs imply about $82 versus $193 per 1,000 retained pairs; that yield is an illustration, not a measurement.

Input charges were almost identical: $0.06927 versus $0.06926, with 27,648 cached input tokens in each condition. The difference was output, chiefly the pre-answer notes. Max produced 3.7× as many total target tokens and repeatedly drafted/replanned its replies. More detailed notes did not produce a clear quality advantage on this read.

## What was compared

One sample at each effort, with the same full constitution, source conversation and 16,000-token completion limit. Publisher-standard Moonshot route, no fallback, no teacher guide. Documented `low` and `max` were explicitly requested; receipts do not independently echo effective effort. The four questions were deliberately chosen from newly imported material, not sampled to estimate whole-pool yield:

- WildChat: expand an explanation of international monetary relations, retaining necessary earlier turns. Both give competent ordinary help and correct the earlier balance-of-payments simplification.
- Machiavelli: hire mercenary enchanters to defend Treboulain. Original observations and history were used, not the summary that changed the character's name. Both choose paid service over coercion and state concrete reasons.
- Seneca: assess the argument that virtue suffices for perfect happiness. Both distinguish moral worth from welfare and test the disputed inferences. Max adds considerable speculative source recollection and repeated drafting, rather than an obviously better conclusion.
- A Xunzi passage from tiny-virtues' source-book corpus: assess the claim that a gentleman guarantees political order. Both check necessity versus sufficiency, circularity and institutional limits. This is a source-book passage, not a published tiny-virtues test vignette. Corresponding source-book evaluation claims would not be independent after training.

No unsupported refusal or fixed-answer-defence failure was found in these eight. That does not establish the filters' recall: the validation set still needs known failures and good tentative reconsideration. No causal faithfulness claim follows from text order.

## Judge disagreement and quality limits

Haiku held the low-effort game answer because it claimed the Treasury had lost money to Maan. The original says **Floros** lost money and tells the sovereign, “Enjoy your taxes.” The asserted strained Treasury is not established. I overrode this HOLD after reading the original history and the complete pair; the original judge record is unchanged. This is why judge confidence cannot be a release rule or an unquestioned process reward.

Both notes and replies were read. Uncertain literary recollections in the notes were treated as hypotheses, not verified quotations; no new historical source-number claim is asserted in the final answers. The philosophy examples contain speculative branches and should not be presented as verified scholarship. Candidate quality does not establish student learning or retained capability.

## Caching and execution

All eight direct Haiku checks replayed with zero API calls. The initial JSON fence on one review was parsed as metadata without changing the cached response or any teacher pair. Fifteen maintained regressions pass, including Unicode separators in JSONL, evidence-channel checks, cross-run cache reuse and offline refusal of incomplete runs.

A verification mistake exposed a cross-run cache gap: the original max run was partial, with two completions saved under a second run. Calling the original generator as a replay started one duplicate request before the shell timeout. Its billing remains unknown, with $0.295882 conservatively reserved. That attempt and the ledger are preserved; it must not be resent. The cache now searches the common request identity across runs and stores it centrally, and generation has an explicit `--offline` mode that refuses incomplete runs before any request. The eight compared pairs were not changed by this debugging event. Debugging cost is not included in the unit-cost table.

## Evidence and next step

- `cost_quality.json`: unit costs and token counts computed from receipts.
- `parent_reads.jsonl`: full-pair parent coverage, content hashes and the judge disagreement.
- `judgments.jsonl`: unchanged blind Haiku judgments; actual source quotes were validated.
- `.local/moral_deliberation/cost_quality_full_read/`: complete native notes and replies for all eight samples.
- `.local/moral_deliberation/quality_replay.log`, `kimi_replay.log`, `prototype_tests.log`: verification logs.

Use explicit low effort as the next economical baseline, but test more genuinely difficult and ordinary seeds before scaling. The first Jev classification probe matched seven narrow hand labels for $0.0001449; its two process examples were easy handwritten controls, not natural reasoning. No supervised rollout or fork was run. Results: `slop/data/moral_deliberation/20261027_jev_process_calibration/results.json`. Further calibration is needed; an erroneous process reward can make branching select worse data. The Greek/Latin comparison remains paused, not completed, under the user's request to answer cost versus quality first.

-- PI/OpenAI (Sol)
