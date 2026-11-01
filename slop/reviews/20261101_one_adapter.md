# One document adapter, one chat adapter

-- PI/OpenAI, 2026-11-01

## Implementation and decisions

Goal 1 of `20261101_general_pipeline.md`, plus the parent's shared-character/loader/command additions. No constitution content, teacher, data-generation recipe or paid rental changed. Read AGENTS, plan, README, jargon, constitution sections 1–5, journal runs 19–22, rental/character-training/ml-debug skills, the named driver seams, training configs/plugin and `character-constitutions/scripts/check.py`.

- One document LoRA on all configured JSONL corpora, using `configs/train/qwen3/graft.yml`, lambda 50. Lock its dose at half the bracketed breakdown before training one chat LoRA on Base plus those documents. Chat retains spectral fraction 0.1, the loss-mask and expert checks.
- Single-adapter doubling probes and geometric bisection; scans at 0.5 / 0.25 / 0.8 of breakdown, then configured full fractions. Production searches without a bracket stop and request wider limits; the tiny random smoke explicitly uses a non-scientific fallback dose.
- Removed each-alone/mix balancing, multi-member searches, ablations, doc-set aliases, group-chat training and the selector branch. `box.py`: 476 → 394 lines (82 fewer), despite adding the new schema/smoke/provenance work. Deleted 371 lines of obsolete configs and the old 86-line mix-search test; new source-named tests replace it.
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

No 35B training or rental was purchased for validation. Random-model smoke is runtime evidence, not character quality or learned-value evidence. Independent review remains parent-owned.

## Proposed AGENTS/README edits (not applied)

**AGENTS:** Replace the old “each subset gets its own adapter” and multi-member default passages with:

> Future runs train one document LoRA adapter on all selected document corpora and one chat LoRA adapter on all selected chat data. Run YAML references `characters/<slug>/character.yaml`; the shared loader reads the constitution, strips balanced Jinja comments and records its source commit/dirty flag. Documents probe to breakdown and lock at half; chat trains on Base plus that update, then probes, scans at 0.25/0.5/0.8 of breakdown (middle first), and evaluates configured `chat.full` fractions. Compare coherent behavioural/capability trade-offs, not raw coefficients. Frozen `base_adapters` reproduce earlier training bases; do not split new runs into group adapters or change the base beneath a chat adapter at graft time. Hot serving and on-box judging are defaults. -- PI/OpenAI

**README:** Add one short collaborator entry point:

> Put identity in `characters/<slug>/character.yaml`, pointing to your constitution (including a sibling repository's `.md.j2`). Prepare document/chat JSONL separately under `data/train/<slug>/`. Run `just run-character CHARACTER_YAML`: it checks the files, smokes stale code/config, then uses the guarded rental. `name=`, `documents=` and `chat=` overrides precede the recipe name. Judge references are optional; by default the stripped constitution is the change text. The smoke uses the invented Ada fixture, not your training corpus. Run22 demonstrates frozen-adapter reproduction, not the new document-training recipe. -- PI/OpenAI
