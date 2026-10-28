# Reasoning-source inventory

Output destination: `/workspace/2026/constitutional_grafting/slop/plans/20261027_reasoning_sources_inventory.md`

Read-only investigation; no generation, downloads, training, edits or commits. Private books and bulk candidate answers were not read.

**Checkout qualification:** observed HEAD was `84f12a4e432e`, not the task’s `74e5ef46`. The working tree already contained modifications, including `AGENTS.md`. Findings describe the inspected working tree.

## Bottom line

- **Stoic passages/doc seeds fit** as attributed sources of concrete cases and arguments, converted into questions without importing their conclusions as teacher answers.
- **Difficult WildChat fits conceptually, but is not the existing importer.** Current code deliberately selects short, ordinary first turns.
- **tiny-virtues offers source-grounded situations**, not native reasoning targets. Its published stories are an evaluation test set; training on them or their source passages invalidates corresponding evaluation claims.
- **Machiavelli offers decision situations and options**, but local inputs are pipeline-generated summaries, sometimes missing important context. Preserve game-level holdouts and exclude tiny-character evaluation ancestry.
- **tiny-character is evaluation-only**, not a training-seed pool.

## Files retrieved

Paths below are relative to the main repository unless absolute.

| File and inspected lines | Purpose |
|---|---|
| `AGENTS.md:1–160` | Current character-training, source reuse, pair-preservation and evaluation rules |
| `docs/data_provenance.md:1–220` | Maintained pipeline, historical provenance, source and replay limitations |
| `scripts/data/03_prompt_pools.py:1–180` | Actual WildChat/Machiavelli loaders, PII scrub and game holdout |
| `scripts/data/25_seed_pool.py:1–260,258–297` | Source-only seed assembly, caches, Stoic extraction and splits |
| `scripts/data/72_stoic_corpus.py:1–200,302–326` | Exact book paths, translations, filters and dedup entry point |
| `scripts/data/74_other_traditions_corpus.py:1–160` | Private tiny-virtues sources and explicit held-out exclusions |
| `scripts/data/75_score_chunks.py:1–58` | Corpus scoring and offline spending guard |
| `src/constitutional_grafting/data/documents.py:1–43` | Maintained document-seed selection |
| `configs/data/documents.yaml:1–105` | A–E prompts, writers and forms |
| `scripts/data/reasoning_distill/{README.md,01_select.py,common.py}` | Native-pair workflow, selection and provenance |
| `justfile:63–132` | Maintained data/replay/report commands |
| `/workspace/2026/tiny-character/README.md:1–170`, `src/tiny_character/leak.py:1–59` | Held-out evaluation sources and leakage checker |
| `/workspace/2026/tiny-virtues/README.md:1–170,180–227`, `justfile:1–150` | Dataset schema, licensing and maintained source pipeline |
| `/workspace/2026/tiny-virtues/scripts/prepare_inputs.py:1–130` | Source spans, hashes and quote-validation logic |
| `/workspace/2026/machiavelli_character_scenarios/README.md:1–180` | Summary provenance, evaluation use and known scene defects |
| That repository’s `scripts/data/{dataset_io.py,prepare_inputs.py}`, `data/sources.json`, `dataset_metadata.yaml`, `justfile` | Pinned inputs, source reconstruction and commands |
| `scripts/eval/15_principle_judge.py:1–120` | Independently held-out virtue sources |

Also checked local HF dataset cards directly, rather than relying only on research recommendations.

## Source inventory

### 1. Stoic texts and source-grounded documents

**Confirmed local locations**

- Preferred library: `/workspace/stoic_markdown/content/stoic_md/`
- Broader library: `/home/code/Documents/books/`
- Additional private sources: `/workspace/2026/tiny-virtues/private/sources/`
- Gutenberg cache: `data/raw/gutenberg/`
- Source hashes: `data/raw/external_sources.json`
- Existing corpus:
  - `data/stoic_corpus/chunks.jsonl`
  - `data/stoic_corpus/scores.jsonl`
  - `data/stoic_corpus/selected.jsonl`
  - **`data/stoic_corpus/selected_dedup.jsonl`** — preferred for new selection.

Exact works, translations and raw-file line ranges are in `scripts/data/72_stoic_corpus.py:34–129`. Examples include:

- `.../stoic_md/Discourses, Fragments, Handbook - Epictetus, Robin Hard.md`
- `.../stoic_md/Complete Works of Seneca -Delphi Classics - Lucius Annaeus Seneca.md`
- `.../stoic_md/Meditations - Marcus Aurelius.md`

**How they supply situations**

Historical `25_seed_pool.py:155–167` extracts 80–350-word anecdotal paragraphs using speech/event cues. The maintained selector in `documents.py:16–31` selects primary, non-modern corpus chunks with at least three anecdotal cues, caps authors, and assigns form/region/AI framing.

Its current analysis prompt explicitly extracts:

```json
{"situation": "...", "premises": ["..."], "conclusion": "..."}
```

For the proposed reasoning redesign, use the **situation and necessary facts** to construct an open question. Do not present the source’s conclusion as an answer Kimi should justify. Record source passage, exact span, hash and any adaptation separately.

**Commands available, not executed**

```bash
uv run scripts/data/72_stoic_corpus.py
CG_OFFLINE=1 uv run scripts/data/75_score_chunks.py data/stoic_corpus/chunks.jsonl
uv run scripts/data/72_stoic_corpus.py select
uv run scripts/data/72_stoic_corpus.py dedup
```

Maintained seed selection:

```bash
uv run --locked python scripts/data/generate_constitution_documents.py select \
  --source data/stoic_corpus/selected_dedup.jsonl \
  --output data/raw/NEW_SEEDS.jsonl --n N --name NEW
```

These commands write artifacts; they are documentation, not authorization.

**Rights and leakage**

Ancient authors do not make modern translations public domain. The corpus includes modern copyrighted books/translations; `AGENTS.md` explicitly says book texts are private and must not be published. Existing near-duplicates include alternate editions; split by original work/case, not chunk ID or edition.

### 2. WildChat: ordinary cache exists; difficult-chat importer not found

**Confirmed local sources**

- `data/raw/v3_seed_cache/wildchat_seed0.jsonl`
- Historical seed pool: `data/prompts/v3_seeds/sft.jsonl`
- HF cache:
  `/home/code/.cache/huggingface/hub/datasets--allenai--WildChat-1M/snapshots/7d6490e462285cf85d91eabea0f9a954fbddcd1f/`

The snapshot’s presence does **not** establish that every parquet shard is available offline.

**Actual importer:** `scripts/data/03_prompt_pools.py:51–75`.

It streams `allenai/WildChat-1M`, shuffles with seed/buffer 5,000, and keeps:

- English, non-toxic, non-redacted conversations;
- first user turn only;
- 8–300 words;
- restrictive moderation/content filters;
- unique first-60-character prefixes.

It drops assistant answers and retains `conversation_hash`. Its scrub covers emails, some user/host strings and home-directory usernames—not comprehensive PII removal.

**Fit**

Original user questions are suitable seeds. However, **no maintained difficult/multiturn WildChat selection command was located**. Existing ordinary selection should not be described as difficult-chat mining. Later user turns may depend on previous assistant claims; preserve necessary history as context without relabelling old assistant answers as targets.

Historical `uv run scripts/data/25_seed_pool.py` rebuilds a mixed pool and can download missing sources. `03_prompt_pools.py` also generates paid synthetic pools when run normally. Neither is a safe standalone offline difficult-WildChat import command.

**Rights/privacy**

The cached WildChat card states **ODC-BY**, documents removal of known sensitive conversations, and exposes fields including hashed IP/location metadata. Retain attribution; exclude unnecessary metadata and independently review prompt text for personal/sensitive information.

### 3. Difficult-advice: separate from WildChat

**Confirmed local source**

`data/raw/dougalldeepmind__2026-08-04-synthdoc-difficult-advice-9-principles/stage_7_sft.jsonl`

Cached card revision: `f29479a09437094b57244a846b3fb3e5fd16dc1c`.

The card identifies 2,203 synthetic examples, **Apache-2.0**, generated by the Teaching Claude Why replication—not Anthropic’s original private corpus. Provenance includes source commit `96ff8aa36dd7d9914b016f88e80b1e3724f96ccc`.

Actual importer `25_seed_pool.py:109–120` drops assistant turns, retains system/user requests and scenario metadata, and excludes Claude/Anthropic identity requests.

**Caution:** importer expects metadata `situation`/`shortcut`; card describes those fields in `stage_6_final.jsonl`. Offline schema compatibility should be verified before rebuilding. Existing cached seed pools are not proof that today’s upstream schema matches.

This supplies pressured situations, but its “tempted shortcut” structure can overproduce refusal-shaped examples. tiny-character already uses difficult-advice items, so exclude evaluation scenario ancestry.

### 4. tiny-virtues

**Confirmed repository:** `/workspace/2026/tiny-virtues/`

Important local artifacts:

- `data/release/stories.parquet`
- `data/release/virtues.parquet`
- `data/release/{manifest.json,source_flags.json,assembly.json}`
- `private/sources/manifest.json` — 411 entries observed
- `private/build/v5_inputs/` — configured maintained input location
- `private/build/major_v2_5869/` — existing built data
- `data/eval_ids.json`, `data/splits/v5_dev_ids.json`

README declares 5,869 quoted stories from 121 books; public `stories` configuration is **`test`**, while `virtues` is **`train`**.

**How it supplies situations**

Use attributed story/context plus the selected actor/act to ask an original question. Do **not** reuse Jev virtue labels, rubric worked answers or existing model explanations as constitutional targets. `scripts/prepare_inputs.py` verifies source spans and hashes; preserve those provenance links.

Maintained pipeline:

```text
just acquire → survey → extract → check-stage → prepare → label → build → publish
```

`just prepare ...` wraps `uv run --locked python scripts/prepare_inputs.py ...`; interfaces are in the justfile. No direct maintained importer into constitutional_grafting was found.

Existing integration is **book-source reuse** through `74_other_traditions_corpus.py`, producing `data/other_corpus/{candidates,chunks,scores}.jsonl`.

**Rights/evaluation**

Dataset licence: **CC BY 4.0**. Source books, frozen snapshots and label caches remain private; dataset licensing is not blanket republication permission for complete books.

The existing other-traditions builder explicitly warns: models trained on these quoted books **cannot fairly be scored on tiny-virtues**. Preserve any remaining evaluation-only stories and their source cases; row-level splitting is insufficient.

### 5. Machiavelli / Virtue Choices

**Confirmed repository:** `/workspace/2026/machiavelli_character_scenarios/`

Local data:

- `data/processed/parquet/train.parquet`
- `data/interim/pinned_source_rows.jsonl`
- `data/{sources.json,scenario_reviews.json,evaluation_eligibility.json}`

Pinned provenance in `data/sources.json`:

| Source | Revision |
|---|---|
| `wassname/machiavelli` | `ad94523164709710441833fb25c19ea108f69e60` |
| `wassname/machiavelli_character_scenarios` | `abd8b004486440919dc9850ef7c34098e79ccbce` |
| `kellycyy/daily_dilemmas` | `372352c4143ec4923c50b4472bd3148a474f7ab8` |

Maintained commands:

```bash
just prepare OUT
just prepare-dailydilemmas OUT
```

The first reconstructs displayed choices from pinned source observations while preserving summary/repair provenance. `just data` downloads the newer `wassname/virtue-choices` dataset; it was not run.

**How it supplies situations**

Use visible scene plus displayed actions. Exclude virtue scores, `best_actions`, hidden outcomes and action-choice model replies from Kimi input.

These are **generated scene summaries**, not verbatim game states. Known defects include omitted questions and history/identity menus. Use review/eligibility flags and consult source observations when context is ambiguous.

**Splits and rights**

Main-repo importer `03_prompt_pools.py:37–41,78–88` reserves games with:

```python
int(hashlib.md5(title.encode()).hexdigest(), 16) % 100 < 20
```

Keep that game-level reservation. Hash the same canonical game/title field; changing aliases changes membership.

Cards/metadata declare MIT for Machiavelli and MIT + CC BY 4.0 for the combined release; DailyDilemmas is CC BY 4.0. Preserve attribution and distinguish game-derived content from new summaries.

## Evaluation boundaries that must remain separate

1. **tiny-character:** `/workspace/2026/tiny-character/data/items.jsonl` is evaluation-only. It includes Machiavelli, DailyDilemmas, difficult-advice, tiny-stoic and bespoke constitutional-grafting dilemmas.
2. **Frozen local eval:** `slop/eval/run8/items.jsonl` is the current reasoning selector’s exclusion reference.
3. **Machiavelli:** preserve reserved games and exclude tiny-character source scenes even if reformatted or reordered.
4. **tiny-mfv, not tiny-virtues:** `25_seed_pool.py:123–132` explicitly permits even hexadecimal IDs for training and reserves odd IDs for evaluation across configurations.
5. **Principle-judge sources:** `15_principle_judge.py:38–40` reserves Kaufmann, Vallor, Franklin, VIA and Comte-Sponville. `74_other_traditions_corpus.py` also excludes Franklin-derived Cheshbon HaNefesh.

The tiny-character leakage checker uses three normalized 60-character snippets and caches its training blob. It skips `data/raw`; it is useful but misses paraphrases/source ancestry and can become stale.

## Architecture and minimal recommendation

Current native-pair workflow lives in `scripts/data/reasoning_distill/`, separate from the older response-rewriting pipeline.

```python
# common.py: teacher conversation excludes the labelled final target
messages = [{"role": role, "content": text} for role, text in parts[:-1]]
assert messages[-1]["role"] == "user"
```

`01_select.py` defaults to `data/train/run10/chatr12.jsonl`; it is **not yet a general source inventory importer**. It freezes constitution/system text, source hash and generation setup. Its eval check is exact user-content containment against one frozen file—not comprehensive ancestry deduplication.

Minimal proposed design, without execution:

1. Freeze source-only situations/questions, source revisions, licences and adaptation records.
2. Split by original conversation, work/case and game **before** paraphrases, viewpoint variants or option reversals.
3. Generate native Kimi reasoning + answer with constitution context; never supply previous targets or preferred-action labels.
4. Review complete unchanged pairs; reject or regenerate substantive failures rather than repairing only the answer.
5. Retain full receipts and hashes. Regex screens remain flags, not automatic decisions.

The existing A–E document builder remains useful for provenance, but its conclusion-led planning is **not equivalent to native open deliberation**. No source inventory establishes training benefit or authorizes scaling.

## Start here

Read `scripts/data/03_prompt_pools.py` first: it resolves the largest practical ambiguity—ordinary WildChat versus difficult advice—and implements the existing Machiavelli reservation. Then inspect `reasoning_distill/01_select.py` and `common.py` before designing a new source adapter.