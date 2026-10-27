# Dataset entry points

Use `just --list` from the repository root. Reusable pipeline logic lives in
`src/constitutional_grafting/data/`; these scripts are CLIs. Historical/run-specific
producers live in [`scratch/`](scratch/README.md). Their saved outputs remain release
inputs, not stages silently run by a new build. The active
[`moral_deliberation/`](moral_deliberation/README.md) research pipeline is separate.

Numbers group operations, **not one total execution order**: 10/11 are alternative
corpora; 20 scores each separately before its builder selects; 30/31 are source
preparation; 40/41 are independent chat/document branches. 50 executes pending work
*between* stages; 60/61 are optional repair/research utilities; 90/99 replay/test.
A repeated scorer invocation is a separate artifact node, not a cycle. `just` is an
ordered command menu, not a file-dependency scheduler.

## Stage map

All commands below run from the repository root. Direct Python CLIs use `uv run
python scripts/data/<file>` (add `--extra data-replay` to `uv run` when a cached
Transformers tokenizer is needed). Existing `just` recipe names/arguments are unchanged.

| Command / CLI | Inputs | Outputs | Depends on | Paid / offline; readiness |
|---|---|---|---|---|
| `just data-corpora [offline=1]` | Local books, source caches, corpus scores, cached general-source rows/tokenizer | `data/stoic_corpus/`, `data/other_corpus/`, `data/train/run10/general.jsonl` | 10 build → 20 score → 10 select/dedup; 11 build → 20 score → 11 select; 30 general | **Writes in place**. Default blocks missing scores; `offline=0` can pay for scoring. Source/tokenizer retrieval may use network. Not a reviewed chat export. |
| `10_build_stoic_corpus.py [select\|dedup]` | Private original texts listed in `SOURCES`; `scores.jsonl` for select | `data/stoic_corpus/{chunks,selected,selected_dedup}.jsonl`, reports | Build → 20 scoring → select (also dedup); explicit dedup uses selected | Offline local transforms; books remain private. |
| `11_build_other_traditions_corpus.py build\|select` | Local tradition texts/cached sources; `scores.jsonl` for select | `data/other_corpus/{candidates,chunks}.jsonl`, reports | 10's shared text filters; build → 20 scoring → select | Local transforms; no model calls. |
| `20_score_corpus_chunks.py <chunks.jsonl>` | One corpus's chunks, existing score cache | Sibling `scores.jsonl`; cost ledger | Corpus build; calibrated fixed scoring prompt | Paid for missing scores unless `CG_OFFLINE=1` blocks them. |
| `30_build_general_instruction.py` | Seeded No Robots/MATH rows, screen decisions, Qwen template/tokenizer | `data/train/run10/general.jsonl`, logged counts | `scripts/train/01_prepare.py`, `data/raw/general/` caches | No teacher calls; network retrieval if source/tokenizer caches missing. Human-source comparison mix, not constitutional generation. |
| `31_generate_plain_help_sources.py submit\|collect --help` | General-source rows; explicit count/source/output/budget | `data/frontier/plain_help/` by default, ids, batch receipts, `items.jsonl` | 30/source file; shared request/batch client | Submit is paid; collect retrieves saved batch results. **Source only**: normal judgements/full read still required. |
| `just data-build <recipe> <input> <name>` → 40 | Chat examples; recipe, constitution/prompts, cached responses and exact review decisions | `data/interim/<name>/` stages; ready `data/processed/<name>/{chat,lineage}.jsonl`, manifest | Source → rewrite → quality/refusal/warranted checks → feedback rewrite → recheck → full read → mixture/export | Offline; exit 2/pending is **not ready**. Includes additional sources in the same checks. |
| `41_build_constitution_documents.py select --help` | Original attributed source rows; selection recipe/seed/count | Selected seed JSONL | Source acquisition; explicit selection parameters | Offline source selection, not training approval. |
| `just data-documents <recipe> <seeds> <name>` → 41 | Selected source seeds, A–E recipe/prompts, saved stages, exact judgements/full-read decisions | Document stage artifacts and pending work; ready documents/lineage/manifest in `data/processed/<name>/` | A analyse → B derive → C plan → D write → E check → two-pass judgement → full read | Offline build; missing work blocks readiness. Revisions are explicit inputs. |
| `just data-generate <workdir> <budget_usd>` → 50 | `pending.json`, immutable requests/cache and ledger | Saved model results/receipts | Pending chat/document build; separate budget/pilot approval | Explicit paid sync calls; rerun original build afterwards. |
| `just data-submit-batch <workdir> <budget_usd>` → 50 | Same pending request set | Batch submission receipt | Same approval; no previous unresolved submission | Explicit paid alternative; do not resubmit an existing receipt. |
| `just data-collect-batch <record>` → 50 | Existing submission receipt | Saved results in the request cache | Batch completion | Network collection, no new sampling; rerun build afterwards. |
| `60_fix_chat_eos.py <files...>` | Legacy chat training JSONL | Copies in `data/train/eos_fixed/`, manifest | Explicit legacy repair only; originals read-only | Offline; not automatic approval or a new default stage. |
| `61_build_thinking_heal_variants.py --help` | Approved whole reasoning/answer rows, hash-matched replay, cached tokenizer | Token-matched thinking-heal variants/manifest | Explicit research release/read decisions; whole-row packing | Offline packing; optional research, not character training on Instruct. |
| `just data-replay <release> <output>` → 90; `just run10-data [output]` | `configs/data/releases/{run10,run11}.yaml`, pinned git source, private local inputs/cache/tokenizer | Rebuilt files under **new** output directory; verified expected hashes | Run11 recursively replays run10; pinned 89 imports old-path 77 shim | Offline, no downloads/API calls. Historical as-run replay, **not** current content approval. |
| `just data-smoke` → 99 | Real tiny saved chat/document results | `.local/dataset_pipeline/run.md`, smoke artifacts | Packaged chat/document pipeline and caches | $0 API/GPU; runtime/resume checks only, output `smoke_only`. |
| `just moral-deliberation-report <run>` | Existing moral-deliberation research run | Screens/reports in that run | See that directory's README | Offline reporting; independent research flow. |
| `just parse-frontier`; `just reasoning-pilot` | Historical frontier exports / frozen reasoning-pilot cache | Historical training exports / read packets and report | Archived 26 / 91 | Offline reporting/parsing; parse-frontier **writes data/train/**. Not default builds. |
| `01_fetch_papers.sh` | `docs/papers/manifest*.tsv` URLs | `docs/papers/*.md` | curl/pandoc, network | Research-input download utility, not training-data DAG. |

Only a processed manifest with `status: ready` identifies a current approved
export. Read complete examples and record hash-bound full-read decisions; judge
passes or source-only generation are insufficient. Builds preserve resolved
recipes/source copies under `builds/<hash>/` and archive old exports. Missing
responses, reviews or inputs stop rather than inventing approvals. Paid command
availability is not spending authorisation. Private books, raw caches, prompts,
selection thresholds and historical release expectations have not moved.

`constitution.py` is the retained shared/legacy renderer. `judge.py` is a legacy
helper still imported by evaluation, **not** the current dataset judge.
`run_training_example_judges.js` stays at its original path/content because review
identity hashes it. `77_general_instruction.py` is an **import-only compatibility
shim** for pinned run11 code: it exports `SELF_TALK`, `ROLE_LABEL`, `p` from 30.
Use 30 for current CLI work; don't rewrite historical git-tree keys in release YAML.

## Basename old → new index (2026-10-27)

Old journal/plan names describe what ran then; this index locates today's code.
Names below are relative to `scripts/data/`.

| Old basename | Current path |
|---|---|
| `72_stoic_corpus.py` | `10_build_stoic_corpus.py` |
| `74_other_traditions_corpus.py` | `11_build_other_traditions_corpus.py` |
| `75_score_chunks.py` | `20_score_corpus_chunks.py` |
| `77_general_instruction.py` | `30_build_general_instruction.py` (old path retained as import shim) |
| `87_plain_help.py` | `31_generate_plain_help_sources.py` |
| `build_chat_dataset.py` | `40_build_chat_dataset.py` |
| `generate_constitution_documents.py` | `41_build_constitution_documents.py` |
| `cached_model_requests.py` | `50_run_model_requests.py` |
| `93_fix_missing_eos.py` → `94_fix_missing_eos.py` | `60_fix_chat_eos.py` |
| `93_heal_training.py` | `61_build_thinking_heal_variants.py` |
| `reproduce_training_datasets.py` | `90_replay_training_release.py` |
| `smoke_dataset_pipeline.py` | `99_smoke_dataset_pipeline.py` |
| All 55 historical producer basenames; `astra_echo/*` | `scratch/<same basename>`; [complete original-path index](scratch/README.md) |
| `reasoning_distill/*` (earlier approved rename) | `moral_deliberation/*` (untouched here) |
| `01_fetch_papers.sh`, `constitution.py`, `judge.py`, `run_training_example_judges.js` | Unchanged |

-- PI/gpt-6.1-sol, 2026-10-27
