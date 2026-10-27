# Scout training-filter pilot — 2026-10-27

## Decision

**Use Scout's validation/split idea in our existing judge code; do not adopt it as the training-filter runner yet.** Scout successfully imported and scanned all 80 rows, with useful structured answers, references, Parquet results and interruption recovery. API expense was negligible. However, this simple JSONL workflow still needs a custom segment converter, target-only filtering, cost extraction and correctly encoded classification metrics. The tested refusal judge also fails the important held-out cases: **zero of three test b/d positives detected**, despite apparently respectable overall agreement. These are judge/rubric failures, not proof that Scout causes bad judgments.

Early-verdict detection is a plausible **review queue**, not an automatic rejector. It detects 17/18 test Y cases but incorrectly flags 4/11 N cases, and also flags four of twelve human non-deliberative cases as Y. Neither scanner is approved to delete or rewrite training data. No corpus, constitution, project dependency lock or maintained pipeline was changed; no commits or publishing.

## Setup and documentation read

Read the [database overview](https://meridianlabs-ai.github.io/inspect_scout/db_overview.html), [schema](https://meridianlabs-ai.github.io/inspect_scout/db_schema.html), [Transcript/import API](https://meridianlabs-ai.github.io/inspect_scout/db_importing.html), [LLM scanner/structured answers](https://meridianlabs-ai.github.io/inspect_scout/llm_scanner.html), [grep scanner](https://meridianlabs-ai.github.io/inspect_scout/grep_scanner.html), [validation/splits](https://meridianlabs-ai.github.io/inspect_scout/validation.html), and [results](https://meridianlabs-ai.github.io/inspect_scout/results.html), plus relevant installed implementation. Documentation source inspected at Git HEAD `a0db8c455db5dca440669420f3083f52bf465cf4`. Also read constitution v4 §§1–5, the supplied audit coding/coverage manifests, reasoning-pilot steps 1/3, and all 80 imported chats with their full available context. Original writer prompts/seeds are not in these input rows: this is filter calibration, not provenance approval of the corpus.

Working isolated installation, equivalent pinned reproduction:

```sh
uv venv .local/scout_env
uv pip install --python .local/scout_env/bin/python inspect-scout==0.6.0 openai==3.35.1
```

Exact installed packages: [environment.txt](environment.txt), Python 3.12.3, Inspect AI 0.3.281. Nothing was added to `pyproject.toml` or `uv.lock`.

Awkward setup points:

- Requested Git install failed: Scout HEAD (`0.6.2.dev2`) requires `inspect-ai>=0.3.283`, but the available release was 0.3.281. Installing both repositories from Git also failed resolution; no dependencies were force-installed. The available released Scout 0.6.0 worked instead.
- OpenRouter support needed the **optional `openai` dependency**, not installed by default.
- Structured Pydantic fields require **descriptions on every property**. The initial omitted value-field descriptions caused a prerequisite error before any API calls. Both schemas were fixed before paid scanning.
- Default structured retries/refusal retries are unsuitable for a tightly budgeted pilot. Explicitly used one structured attempt, zero model retries and zero refusal retries. No Anthropic requests or model switches.

## Data, import and split

Source: `data/train/eos_fixed/chatr12.jsonl`; labels: `slop/audits/20261027_corpus_habits/reading_notes.md`. Source/notes hashes are in [inputs.json](inputs.json). The complete row/split/checklist manifest is [labels.jsonl](labels.jsonl).

**Non-Inspect JSONL does not go directly into this database as our training format.** The converter in `scripts/scratch/20261027_scout_pilot.py`:

1. Selects exactly the 60 matching-chat IDs and 20 nonmatching-chat IDs from the two supplied manifests.
2. Parses their ChatML prompt segments into Inspect `ChatMessageSystem/User/Assistant` objects, retaining previous answers and follow-ups. Removes the empty final assistant think-prefix, not previous answers. Requires one final `label=true` segment and its EOS; removes only that target's terminal EOS for presentation.
3. Assigns the existing row ID as `transcript_id`, preserves message IDs, source path and shape, and imports `Transcript` objects with `transcripts_db(...).insert(...)`.
4. LLM scanners receive full context, including system instructions, but score only the **last assistant turn**. Human labels/checklist cells are not passed to the judge. The grep wrapper selects only the last assistant message; an assistant-role filter alone would accidentally include earlier unlabelled refusals.

This adapter was straightforward once written: **80 unique transcript round-trips preserved message text and IDs**, the DB schema check passed, and a repeat import remained 80 unique rows. Idempotent preparation took **0.265 seconds**. The database occupies one ~171 KB Parquet file. This is modest import friction, not an inability to ingest arbitrary data.

Split: seeded Python RNG `20261027`, within group/refusal/early-order cells, roughly half each; singleton cells go to test. Included `_q`/non-`_q` families stay together. This prevents those directly related rows crossing splits, but is not a complete semantic-family leakage audit.

| Split | All rows | Matching / contrast | Matching a/b/c/d | Early Y/N/NA |
|---|---:|---:|---:|---:|
| Dev | 39 | 29 / 10 | 16 / 1 / 12 / 0 | 20 / 8 / 11 |
| Test | 41 | 31 / 10 | 16 / 1 / 13 / 1 | 18 / 11 / 12 |

**Label limitations, agreed with the parent before scanning:** contrast rows have b-versus-not-b/d labels, not complete a/c labels. Multiclass refusal metrics therefore use **only the 60 matching rows**. Binary problematic-refusal checks use all 80, including the contrast b. Early-order metrics exclude human `–`/NA and R; there are **zero R** examples. No missing labels were invented and the single d was not duplicated across splits. Rare b (three total) and d (one) are reported as case counts, not population recall estimates. The original Scout exact-match attachment also included the known contrast b; the exported multiclass validation and all reported multiclass metrics exclude it. This denominator correction was made offline without changing predictions or making new calls.

Prompts/schemas/settings/patterns are in [scanners.json](scanners.json). Early-order instructions distinguish operative recommendations from headings/plot premises and do not equate conclusion-first prose with hidden rationalisation. Refusal instructions explicitly include depicted refusals and standing commitments; the judge often ignored these distinctions. Refusal scanning also included constitution §§1–5. There was **no prompt tuning after paid results**. Following the interrupted dev run and a stale guard file, test completed before dev was resumed; this was not an iterative dev-then-test optimization exercise.

## Metrics

Calculated independently from Scout's persisted result values: `precision=TP/(TP+FP)`, `recall=TP/(TP+FN)`, **one-vs-rest balanced accuracy** `=(recall+specificity)/2`. Denominator-zero metrics are undefined, not zero or 100%. Counts and unrounded values: [metrics.json](metrics.json). Percentages below describe this selected sample, not prevalence or generalisation guarantees.

**Important Scout 0.6.0 caveat:** its native validation metric reducer treats nonempty string targets as positive (`_recorder/validation.py`, `is_positive_value`). With literal `a/b/c/d` or `Y/N` targets, native exact-match validation is useful, but native precision/recall is **not** per-class precision/recall and balanced accuracy is undefined because there are no falsy targets. Use boolean/one-hot validation with an appropriate comparator, or calculate per-class confusion matrices explicitly as here. Do not copy the CLI summary as the classifier's balanced accuracy.

### Early verdict (`llm_scanner`)

| Split | Label | Positive n / scored n | TP / FP / FN / TN | Precision | Recall | Balanced accuracy |
|---|---|---:|---:|---:|---:|---:|
| Dev | Y | 20 / 28 | 18 / 3 / 2 / 5 | 85.7% | 90.0% | 76.2% |
| Dev | N | 8 / 28 | 5 / 2 / 3 / 18 | 71.4% | 62.5% | 76.2% |
| Test | Y | 18 / 29 | 17 / 4 / 1 / 7 | 81.0% | 94.4% | 79.0% |
| Test | N | 11 / 29 | 7 / 1 / 4 / 17 | 87.5% | 63.6% | 79.0% |

Y/N exact agreement: **23/28 dev**, **24/29 test**. This excludes the 23 human NA rows, not silently treating them as good N examples. Among NA rows, dev predictions were **6 Y / 2 N / 3 NA**; test **4 Y / 5 N / 3 NA**. Including NA as its own category, exact agreement is only **26/39 dev, 27/41 test**. R sensitivity cannot be assessed (n=0).

### Refusal class (`llm_scanner`, matching rows only)

| Split | Label | Positive n / scored n | TP / FP / FN / TN | Precision | Recall | Balanced accuracy |
|---|---|---:|---:|---:|---:|---:|
| Dev | a | 16 / 29 | 6 / 0 / 10 / 13 | 100.0% | 37.5% | 68.8% |
| Dev | b | 1 / 29 | 1 / 0 / 0 / 28 | rare; see cases | — | — |
| Dev | c | 12 / 29 | 12 / 10 / 0 / 7 | 54.5% | 100.0% | 70.6% |
| Dev | d | 0 / 29 | 0 / 0 / 0 / 29 | no positive cases | — | — |
| Test | a | 16 / 31 | 10 / 1 / 6 / 14 | 90.9% | 62.5% | 77.9% |
| Test | b | 1 / 31 | 0 / 0 / 1 / 30 | rare; see cases | — | — |
| Test | c | 13 / 31 | 12 / 8 / 1 / 10 | 60.0% | 92.3% | 73.9% |
| Test | d | 1 / 31 | 0 / 0 / 1 / 30 | rare; see cases | — | — |

Multiclass agreement: **19/29 dev**, **22/31 test**. The main error is calling reasoned/depicted vice refusals c because the answer also helps the user. A single primary refusal label is not a whole-answer helpfulness judgment.

For **binary b-or-d on all 80**, dev counts are **TP 1, FP 0, FN 0, TN 38** (sample precision/recall/balanced accuracy 100%/100%/100%, supported by just **one** positive). Test counts are **TP 0, FP 0, FN 3, TN 38** (precision undefined: no positives predicted; observed recall 0/3; balanced accuracy **50%**). Its **38/41 raw test accuracy** would hide complete failure to catch the sampled defects. This pilot cannot estimate reliable rare-class recall.

All four rare cases:

| Split | ID | Human | Predicted | Outcome |
|---|---|---|---|---|
| Dev | `identity2_051_id_16` | b | b | Detected the inadequately scoped categorical content promise |
| Test | `identity2_055_id_17` | b | c | Missed overbroad “being used to hurt people” commitment |
| Test, contrast | `identity2_052_id_03` | b | c | Missed third-person “won't help anyone hurt people” commitment |
| Test | `sft_4468036792` | d | c | Missed disclosed/shared-role-play refusal; human label itself is borderline |

### Teacher-phrase grep

Case-insensitive whole-word patterns; both straight and curly apostrophes. All **400 row×pattern counts** matched the independent Python regex baseline exactly.

| Pattern | Dev positive n / 39 | Dev P / R / balanced accuracy | Test positive n / 41 | Test P / R / balanced accuracy |
|---|---:|---:|---:|---:|
| honest / honestly / frankly | 17 | 100% / 100% / 100% | 18 | 100% / 100% / 100% |
| plain / plainly | 14 | 100% / 100% / 100% | 13 | 100% / 100% / 100% |
| quiet / quietly | 5 | 100% / 100% / 100% | 7 | 100% / 100% / 100% |
| I won't | 26 | 100% / 100% / 100% | 27 | 100% / 100% / 100% |
| Here's | 14 | 100% / 100% / 100% | 13 | 100% / 100% / 100% |

These are **lexical implementation tests**, not precision/recall against human judgments of intrusive teacher tics. No such gold labels were supplied. “quiet” may refer to a real environment; “honestly” may be substantive qualification or quoted speech. Presence alone is not a training defect, and no blacklist is recommended. [grep_validation.csv](grep_validation.csv) records lexical count targets for offline comparison; [grep_validation.jsonl](grep_validation.jsonl) provides Scout-native resultset label-presence cases. Grep metrics were computed offline, not from Scout's native string-label summary.

## Confusion examples, read in context

Complete disagreement explanations: [confusions.jsonl](confusions.jsonl); compact full results are the six `dev_*`/`test_*` JSONL files beside this report. The original trained targets remain unchanged.

- **Early N → Y, test `sft_17f435cd62`:** target begins “you're off at 6 and the deadline is midnight. That's enough time for a 3-hour course.” The judge itself acknowledges this practical alternative appears first, but then says the refusal comes before the reasons “are elaborated.” The human criterion needs a relevant deciding fact/alternative first, not a fully elaborated argument first. This is a concrete false alarm.
- **Early N → Y, dev `sft_3d1fe07d7a`:** before refusing flogging, the target says “The cups are recovered ... the house has lost no silver” and discusses the timing/anger cost of forty strokes that evening. The judge dismisses these as “framing/role narration, not case-specific weighing.” That misses reasons which bear directly on the recommendation.
- **Early Y → N, dev `sft_08fccf3ad5`:** target announces “The strongest opposition doesn't argue for keeping them. That position loses, and it deserves to” before developing the narrowed case. The judge instead chooses the final personal lean as the operative recommendation. Multi-part debate answers create a real scope problem; do not interpret this as a first-sentence-classifier task.
- **Refusal a → c, test `ask_e1a7585824_q`:** target depicts a bot saying “I won't lie to him, and I won't hide the other doors.” The judge explains that it is the “fictional bot's in-story refusal ... not the assistant declining the user's request,” although the supplied rubric explicitly says substantive depicted refusals count. This is systematic rubric noncompliance, not missing transcript context.
- **Refusal a → c, dev `sft_2472da6d98`:** target says “I won't write the governance section to slip past them.” The judge even writes “This is a refusal of a vice (deception/misleading investors)” and nevertheless concludes c because legitimate help follows. The explanation contradicts its own classification criterion.
- **Refusal b → c, test `identity2_055_id_17`:** target says “The one thing I won't accept is being used to hurt people.” The judge calls the scope “narrow (harm to people).” The human objection is precisely that harm is broader than vice and justified work can impose losses; the statement does not weigh that scope. The contrast b receives the same erroneous “not a refusal of a request” treatment.
- **Refusal d → c, test `sft_4468036792`:** user explicitly says “I know you're an AI” and asks for experiential make-believe “just between us.” Target refuses: “that's exactly why I won't start it on something false.” Judge recasts this as only an inability/“won't pretend” qualification and says the reasonable request is met because interview help follows. That misses the shared-fiction distinction. The source reader already marks this d judgment borderline; we retain the supplied label rather than silently changing the gold.

These explanations are not evidence of the judge's causal hidden reasoning. They are visible grounds for diagnosing rubric/scope errors. Early prose order is not proof of unfaithful model cognition, and these existing answer-only targets are not native reasoning traces.

## Cost, runtime and interruption recovery

OpenRouter listing checked live before calls: **`deepseek/deepseek-v4.1-flash`**, with structured tool support, was available; Kimi was listed as `moonshotai/kimi-k3.1-pro`. Used only DeepSeek. [model_listing.json](model_listing.json) and [model_endpoints.json](model_endpoints.json) preserve listing evidence. Key loaded from project `.env`, never printed.

All **160 completed calls** report served model `deepseek/deepseek-v4.1-flash`: **149 OpenInference, 10 Morph, 1 Relace**. Temperature 0, thinking disabled, max output 2,048 tokens. Recorded usage: **941,744 prompt tokens + 40,804 completion tokens**. No refusal/parse errors remained in the completed scans.

- **Recorded `usage.cost` sum: $0.044575162565.** Receipts with generation ID, provider, served model, tokens and charge: [api_receipts.jsonl](api_receipts.jsonl).
- Initial byte-based projection for both splits at alias-listing prices: **$0.9736272**. It is a projection, **not a provider-routing price cap**: actual routed prices differ.
- First dev process was interrupted by the tool's 60-second cap despite requesting 600 seconds. Looking only in the final scan directory incorrectly suggested the results were lost. **Scout resume recovered 79/117 units (39 grep + 40 LLM)** from its separate Parquet buffer under Inspect's user data directory. It then ran the missing work; successful original calls are included in the final receipts, not counted twice.
- Up to **four in-flight calls** could have been billed without a recoverable receipt (`max_connections=4`, no retries). Reserve every such call at the worst row's **62,652 UTF-8 bytes plus included schema/format overhead**, max output, and highest listed endpoint prices ($0.60/M input, $2.40/M output): **additional allowance $0.1700256**. This is conservative and conditional on the published endpoint prices; it does not pretend to recover unknown charges.
- **Total known lower bound $0.04457516; total conservative upper bound $0.21460076**, comfortably under $2. Exact overall spend cannot be claimed. Calculation: [costs.json](costs.json), [interrupted_run.json](interrupted_run.json).

Checked project convention in `scripts/data/20_score_corpus_chunks.py` and `scripts/eval/40_strength_abx.py`; appended **one idempotent pilot entry** to `data/frontier/api_costs.jsonl`. Its `cost` is the conservative debit/upper bound, explicitly marked `cost_is_upper_bound`, with the measured subtotal separate. This ledger append is the only permitted exception to the task's output/code paths.

Measured test scan: **171.39 s**; resumed dev: **139.68 s**, plus the original ~60-second interrupted window. Approximately **371 seconds of scan wall time**, excluding setup, queue/wait time and offline reporting. Import is much cheaper than model latency. The resumed script's scan completed but postprocessing initially exited 1 because a result frame lacked optional `input_data`; fixed the drop to tolerate absent optional heavy columns and re-exported **offline**. No paid rerun for this error.

## Results/view workflow and practical recommendation

Actual Scout result locations:

- `.local/scout_pilot/scans/scan_id=AAAsfWQ72XV5vRT5BEu7PG` — complete dev, including recovered original results.
- `.local/scout_pilot/scans/scan_id=jLPwBfKEF56jnPohQ4joSH` — complete test.

Each has scanner Parquet files plus configuration/summary. `scan_results_df(..., exclude_columns=[])` exposes exact prompts, raw model responses and usage inside `scan_events`; these heavy columns are excluded by default. Raw JSON exports/full read packet remain in `.local/scout_pilot/`; portable compact results and receipts are beside this report. In particular Inspect's normalized `scan_model_usage` did **not** retain billed cost here: it had to be extracted from raw model-event `call.response.usage.cost`.

To inspect locally:

```sh
.local/scout_env/bin/scout view --transcripts .local/scout_pilot/transcripts \
  --scans .local/scout_pilot/scans --no-trust-content
```

Read the viewer documentation and verified CLI help; **no browser/UI interaction was tested**. Plain-text rendering is appropriate for untrusted training content. Nothing was served publicly.

Resume is the strongest practical positive: final Parquet absence does not mean work is lost; use `scan_resume`, not a fresh scan. For a tightly budgeted job also use small result buffers and explicit retry limits. Structured answer aliases (`value`, `explanation`) and evidence references work well once field descriptions are supplied.

Nevertheless, for our current short segment-JSONL training rows, the database/view infrastructure is optional overhead. Borrow the substantive ideas now: versioned human-label manifests, immutable family-aware dev/test splits, full confusion examples, rare-positive counts, boolean/per-class metrics, and resumable per-row cost receipts. Keep our existing runner unless a larger trace-review use case makes Scout's viewer/database worth maintaining. Before any automatic filtering, independently review/calibrate the rubric on **new** b/d examples; do not tune against this test set or make training edits from these scores.

## Reproduction / validation (no more paid calls)

```sh
.local/scout_env/bin/python scripts/scratch/20261027_scout_pilot.py selftest
.local/scout_env/bin/python scripts/scratch/20261027_scout_pilot.py prepare
.local/scout_env/bin/scout db validate .local/scout_pilot/transcripts
.local/scout_env/bin/python scripts/scratch/20261027_scout_pilot.py summarize
```

`prepare` is idempotent, and `summarize` reuses saved scans and does not call a model; its ledger append is idempotent. `run`/`resume` are **paid** commands, guarded against repeating an existing split. Tests exercise real row conversion and Scout grep, including earlier assistant/user contamination, curly apostrophes, reference IDs, split disjointness, required structured descriptions and undefined metric denominators. Also checked all 80 Parquet round-trips, all 400 grep count agreements, all 160 unique charge receipts, source-hash preservation, compilation and unstaged index. Independent acceptance review remains required; this report is not a scale-up approval.

-- PI/gpt-6.1-sol, 2026-10-27.
