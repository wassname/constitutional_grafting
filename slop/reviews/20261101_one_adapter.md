# One document adapter, one chat adapter

-- PI/OpenAI, 2026-11-01

## Implementation and decisions

Goal 1 of `20261101_general_pipeline.md`, plus the parent's shared-character/loader/command additions. No constitution content, teacher, data-generation recipe or paid rental changed. Read AGENTS, plan, README, jargon, constitution sections 1–5, journal runs 19–22, rental/character-training/ml-debug skills, the listed driver files, training configs/plugin and `character-constitutions/scripts/check.py`.

- One document LoRA on all configured JSONL corpora, using `configs/train/qwen3/graft.yml`, lambda 50. Lock its dose at half the bracketed breakdown before training one chat LoRA on Base plus those documents. Chat retains spectral fraction 0.1, the loss-mask and expert checks.
- Single-adapter doubling probes and geometric bisection; scans at 0.5 / 0.25 / 0.8 of breakdown, then configured full fractions. Production searches without a bracket stop and request wider limits; the tiny random smoke explicitly uses a non-scientific fallback dose.
- Removed each-alone/mix balancing, multi-member searches, ablations, doc-set aliases, group-chat training and the selector branch. `box.py`: 476 → 408 lines (68 fewer, including review fixes), despite adding the new schema/smoke/provenance work. Deleted 371 lines of obsolete configs and the old 86-line mix-search test; new source-named tests replace it.
- Per the parent's explicit decision, deleted run17/17b/18/18b/19/19o/21 configs, not an archive directory. Git retains them; parent will tag pre-merge history `runs-17-22-configs`. Converted run20/run22 use frozen `base_adapters`. Run22 preserves the exact ½/1/1 document coefficients, ×0.75 chat coefficient and original `full_all_0.75` cell ID. Hub folders remove dependencies on private local adapter paths.
- Private frozen item inputs stay on local disk under `configs/eval/inputs/run17/`; Musonius's private reference answers stay local under `characters/musonius/judge/`. Snapshot bytes/protocol hashes are unchanged. These private files are ignored, and the branch history was rewritten before merge so no branch commit publishes them. Only the item-free change text is tracked. Maintained references and the journal's one old input link were updated; original-source fields inside the frozen manifest remain historical provenance.
- Hot serving, on-box pinned judging, receipts/resume, adapter/transfer hashes, five-host market gate, budget, deadline, watchdog, retries and retrieval safeguards remain. Changed training data now rejects a stale training receipt rather than reusing the old adapter.

Rebased onto chatdata's `0a9edd21`, reusing its `characters/musonius/character.yaml` and `tests/fixtures/characters/ada/`. Only `judge_change` and `judge_refs` were added to its Musonius file; its other fields were not edited.

## Character files and run schema

All character paths are **relative to the constitutional_grafting checkout root**, not the YAML directory (parent's clarified contract). An absolute path also works. `src/constitutional_grafting/character.py:load_character(path)` returns the YAML fields plus `constitution_path` (absolute string), `constitution_text`, `constitution_commit` and `constitution_dirty`. It strips balanced `{# … #}` comments exactly as the constitution repository checker does; it does not render arbitrary Jinja expressions. Dirty/untracked constitution edits warn, never fail. Constitution receipts record the source file's last git commit and dirty flag, not a new content hash. Existing training/transfer/code-cache hashes are retained; no new dataset hash manifest was introduced.

Example `characters/garden/character.yaml`:

```yaml
name: Ada
maker: a collaborator
constitution: ../character-constitutions/constitutions/garden/constitution.md.j2
about: named after Ada Lovelace
researcher: a garden researcher
held_out_names: [Desk]
# judge_change: characters/garden/judge/change.md  # optional alternative to the stripped constitution
# judge_refs: characters/garden/judge/refs.jsonl   # optional; default judging has no references
```

Run YAML (plus model, budget, frozen-input settings from `configs/runs/character_template.yaml`):

```yaml
character: characters/garden/character.yaml
documents:
  corpora: [data/train/garden/documents.jsonl, data/train/garden/source.jsonl]
  # adapter: existing_document_folder  # optional: skip document training
  # dose: 0.5                         # required if chat.adapter is also supplied
chat:
  data: data/train/garden/chat.jsonl
  full: [0.25, 0.5]
  # adapter: existing_chat_folder      # optional: skip chat training
adapter_hub: collaborator/adapters
```

Document JSONL uses `text`; chat JSONL uses labelled `segments`. Existing adapters may be local directories or folders on `adapter_hub`. For historical reproduction, replace `documents` with `base_adapters: {name: {path: ..., dose: ...}}`. Those adapters are frozen, never searched; fixed `cells` reproduce measured chat doses without a new search. Chat cells cannot override a locked document dose.

Rental tar creation materializes the stripped constitution and selected optional judge inputs inside the character's portable folder, preserving source commit/dirty metadata; sibling-repository paths never become `../` archive entries. It similarly packages selected data paths and the generated run config. Only the OpenRouter key is sent, never the Vast key or local environments/caches.

## Collaborator command

```sh
just run-character characters/garden/character.yaml
just name=garden_trial2 documents='data/source.jsonl data/documents.jsonl' chat=data/chat.jsonl run-character characters/garden/character.yaml
```

Data generation remains separate. Default inputs are `data/train/<slug>/documents.jsonl` and `chat.jsonl`; missing files fail before any smoke or rental. Default run name is `<slug>_<YYYYMMDD>`; use `name=` for another run that day. The command writes a local run config, checks it, smokes stale code/config receipts, then invokes the existing guarded rental controller. Template defaults, explicitly approved by parent: 10 h, $1.92/h ceiling, $24 budget, $0.50 traffic + $2 judge reserve. Estimate: setup 0.5 h, documents 2–5 h, chat 1–3 h, hot probes/scans/full 1.5 h; the actual corpus size matters. GPU selection defaults to class: ≥90000 MB RAM, compute capability 1200, verified, reliability ≥0.98, no datacenter-only condition and `gpu_name: null`.

## Validation evidence

- Converted run22 `--check`: passes, including frozen-input hashes and subset paths.
- `just check`: passes on the final source (syntax: 282 Python / 22 shell files, plus maintained checks).
- 84 box/loader/hot/rental/collaborator-command tests passed together in 11.32 s (2 subtests; 8 existing PEFT pattern warnings). Tests cover sibling `.md.j2`, exact comment stripping and unbalanced comments, git/dirty provenance, no-refs and retained-refs judging, portable deployment, single-adapter bisection/scans, locked training base, hub folders, missing data, dated/name overrides, stale/current smoke receipts, host diversity and budget gates.
- Real cold Ada smoke: pueue 4341, 10:50:12–10:57:41, **7m29s**, with fresh document and chat training, merge, hot probes, scan, full generation, both-mode GSM and on-box judging. It used the shared Ada fixture and the prior synthetic-reference wiring. Logs/training receipts are preserved in `.local/one_adapter_evidence/ada_refs_run/`; trained tiny adapters remain in `outputs/run22_smoke/`.
- Initial Testa real smoke also passed (pueue 4337, 12m05s). The shared pinned judge cache was 3.1 GB, causing ~17 GB RSS/cache/trace overhead for one item; this worktree's pinned evaluator was isolated with a 35 MB recent-call cache, without changing its source. Cold vLLM starts still dominate. A four-second resume (4340) was explicitly NOT counted as a fresh Ada smoke; it exposed stale data reuse, which the new data-receipt check now rejects.
- Final Ada **no-refs** regeneration smoke: pueue 4342. It reuses the actual Ada-trained adapters (verified adapter/data receipts), but regenerates the document/chat probes, scan, full replies and both-mode GSM. The real judge metadata has `refs: ""`, `refs_sha256: null`, and Ada's stripped constitution as its change text. **Passed in 4m42s**, 11:03:35–11:08:17. This is a regeneration/resume measurement, not a claim that cold training takes less than five minutes; cold training remained 7m29s. Current receipt validation returns true.
- An exploratory unrelated data-script test run in the Axolotl environment failed because that environment lacks `tyro`/`loguru`; no data-pipeline changes were made to hide those failures. Maintained `just check` uses the correct locked project environment and passes. An earlier broad hot-test shell command hit the tool's 60-second cap; it was moved to pueue, where it passed.

A real run22 rental tar was built, safely extracted into an isolated local directory, and its actual deployed `box.py --check` passed; no main-checkout input paths were required. The real `just run-character` CLI with missing Ada data returned a clear error before smoke/rental.

No 35B training or rental was purchased for validation. Random-model smoke is runtime evidence, not character quality or learned-value evidence. The independent review returned “merge with fixes”; the required fixes and validation are recorded below.

## Documentation changes

The approved one-adapter/default-dose wording is now applied in AGENTS.md. The rental skill now describes the new fields, class-based offers, five-host requirement and current reliability threshold. README remains unchanged pending wassname's editorial approval; only the proposal below is supplied.

**README:** Add one short collaborator entry point:

> Put identity in `characters/<slug>/character.yaml`, pointing to your constitution (including a sibling repository's `.md.j2`). Prepare document/chat JSONL separately under `data/train/<slug>/`. Run `just run-character CHARACTER_YAML`: it checks the files, smokes stale code/config, then uses the guarded rental. `name=`, `documents=` and `chat=` overrides precede the recipe name. Judge references are optional; by default the stripped constitution is the change text. The smoke uses the invented Ada fixture, not your training corpus. Run22 demonstrates frozen-adapter reproduction, not the new document-training recipe. -- PI/OpenAI


## Independent review fixes and privacy correction

The public repository must not contain private tiny-character items or reference answers. Before further fixes, the five unpushed implementation commits were replaced by clean `27a42e52`, followed by small review-fix commits. Walking every commit from `0a9edd21` to HEAD confirms that none tracks `configs/eval/inputs/` or character judge JSONL. The local files remain intact and gitignored. Only the item-free hand-written legacy change text is public. Rental archives include the selected local private snapshot, not every ignored snapshot under configs.

`configs/eval/README.md` documents one `80_freeze_eval_inputs.py` command using wassname's existing private bundle, item/protocol pin `cf2b841` and the separate agent pin `df2d8ff`. A fresh public clone needs that bundle from wassname; the private pin alone lacks the project's other protocol files. The command was actually run into `.local/rebuilt_private_run17/`: all nine input hashes, protocol hashes and agent scorer hashes match the existing bundle. Guided legacy refs remain a separate local-only dependency, not regenerated during setup.

1. `prepare()` now validates every document JSONL row, non-empty text and token count before smoke/rental, and runs the real loss-mask/EOS checker with `ALLOW_MISSING_EOS` removed. The maximum is 64 × `graft.yml` sequence length, matching Axolotl completion's truncation ceiling; longer-than-one-sequence documents are valid chunks. Real Ada preflight passed: 5 rows / 458 tokens, valid labelled EOS. Tests reject malformed/empty/oversized documents and missing EOS before any smoke/rental.
2. The pinned judge resolver runs locally in `prepare()`, smoke preflight and the rental controller before any offer is rented. Its existing condensation cache ships with the private pinned evaluator data. Judge file stems are preserved, and preflight output paths are absolute before changing cwd. Real plain Musonius preflight prepared a 294-word cached description from 10,687 words. A real rental archive was extracted locally and its deployed judge resolver was run with network condensation explicitly disabled: it hit that same 294-word cache. No on-box Opus access was needed. This is cached reproducibility, not a claim that rerunning temperature-0.3 condensation would produce identical text.
3. `characters/musonius/character_plain.yaml` supplies the same constitution without the legacy change/ref fields. Use `just run-character characters/musonius/character_plain.yaml` for new like-for-like cross-constitution baselines. The canonical legacy YAML is only for the historical runs 19–22 protocol. Private refs are not needed for the plain baseline; the private common item bundle still is.
4. Both pre-existing adapters now require an explicit `documents.dose`, used as supplied without re-searching that chat adapter's training base. A conflicting resumed lock fails. Document-only configs without evaluation cells fail before training.
5. `box.py` inserts its own `src` import path explicitly. Smoke receipts now include `41_expert_adapter_check.py` and `router_dtype_plugin.py`.

Review validation: **99 tests passed**, 2 subtests, 8 existing PEFT warnings (pueue 4351, 12.27 s). Final `just check` passed. Real Ada no-refs probe/scan/full regeneration passed in **4m25s** (pueue 4346, 11:31:08–11:35:33), reusing the previously verified real-trained Ada adapters. A subsequent six-second receipt-resume after the relative-preflight-path fix passed too (4350); it is not counted as fresh training or regeneration. Cold training remains the earlier 7m29s measurement.

Residual scientific concern, reported to parent rather than silently editing the pinned protocol: reading the new cached condensation found “voices concern once” and an over-broad exclusion of outcomes leaving others worse off. These are inherited condensation-fidelity risks; review the cached behavioural description before using it for a scientific character comparison. No character-quality claim or 35B training result is made here.
