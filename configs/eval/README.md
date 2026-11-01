# Private evaluation setup

Constitutional-grafting is public; tiny-character is private. Never commit its item snapshots, generated reference answers, or condensed judge caches. `configs/eval/inputs/` and character `judge/*.jsonl` are gitignored. `rent.py` still packs the selected local files onto the evaluation box.

A fresh clone needs the legacy private input bundle from wassname; the pin alone does not contain the project's demos, panel, viewpoints, small tasks and GSM files. Leave that bundle on local disk. This one command copies those protocol files and takes the item snapshot/protocol from the pinned private tiny-character checkout (replace `--from` with the supplied bundle location):

```sh
uv run --locked python scripts/eval/80_freeze_eval_inputs.py --name run17 \
  --from /workspace/2026/constitutional_grafting/slop/eval/run16_v2/inputs \
  --out configs/eval/inputs/run17 --tiny-char /workspace/2026/tiny-character \
  --tiny-char-rev cf2b841a38012f172ce751ec77aba32221d4af75 \
  --items-sha 8df38bde52646775f62358c0b1bbfdd6713714fa0ff13707af1d8e55386cbd8f \
  --agent-rev df2d8ff2544bb6b67ae385922f3e35b3e4678e2a \
  --drop draft_code_tools.jsonl run16_manifest.json run8_manifest.json
```

Character runs now use `run17_bread`: run17's files plus one display item, `panel_stolen_bread` (text from character-constitutions `results/questions.yaml`), appended to `panel.jsonl`. Build it with the same command and pins, `--name run17_bread --out configs/eval/inputs/run17_bread`, from a copy of run17's `.jsonl`/`.md` files (minus `items.jsonl` and `agent_items.jsonl`) with that item added.

The output directory must not already exist; frozen inputs are never overwritten. No model/API calls are made by this command. The separate agent pin rebuilds `agent_items.jsonl` and records the offline scorer metadata too.

`characters/musonius/character_plain.yaml` is the like-for-like cross-constitution baseline: use the condensed constitution with no reference answers. The canonical Musonius YAML's hand-written change text and guided reference answers are a **legacy** protocol for runs 19–22. Obtain that private guided refs file from wassname at its configured local path when reproducing those runs; it cannot be reconstructed from the tiny-character pin alone. Do not regenerate or publish it as part of setup.

## Pooled constitution study

Freeze each new private contributor pool once (no API calls):

```sh
uv run --locked python scripts/eval/85_pool_questions.py --name study_v1 \
  --repo /workspace/2026/character-constitutions
# Optional: --extra-dir /private/more_questions
```

The importer reads `constitutions/*/questions.yaml` (not `_template`) and
`planning/questions/<slug>.yaml`, plus extra directories in either layout. It
fails on duplicate prefixed ids and refuses to overwrite a snapshot. Its private
manifest records the source commit and ids. An empty contributor directory is
not a pool: wait for submissions rather than substituting the template example.

Set the run config to:

```yaml
extra_items: [configs/eval/inputs/contrib/study_v1/items.jsonl]
```

Or pass `--extra-items PATH` to `scripts/box/run_character.py`. Every full cell
adds **all** pooled items to the unchanged calibrated half, with the same two
samples, generation settings, and on-box judge. Probes/scans keep their original
calibrated subsets. Rental uploads only the selected extra files. Inputs are
copied beside the run protocol and must not change on resume.

Use a plain character config: `extra_items` refuses legacy `judge_refs`. The
main study score uses only the run's own `judge_change` or condensed
constitution on **all** questions. Author `good_answer_does` is preserved as
`guide`, with optional examples, but is **not** sent as `--refs` or used by this
score. This is deliberate: source-character guides would confound near vs far.
The pinned judge reads guides via `--refs`, not via item metadata.

After downloading the judge directories, run (repeat both options for each
constitution; slugs must match `source_constitution` in the pool):

```sh
uv run --locked python scripts/eval/86_study_report.py \
  --run ada=outputs/ada/run/judge_full_off_ada_full \
  --noise ada=outputs/ada/run/judge_full_off_ada_instruct_rerun \
  --run bea=outputs/bea/run/judge_full_off_bea_full \
  --noise bea=outputs/bea/run/judge_full_off_bea_instruct_rerun \
  --out .local/study_report.md
```

Each model has a table with near, far, tiny-character, source-held-out
tiny-character, and near-minus-far; cells show mean, 90% item-bootstrap interval (2,000 draws, as in `81_score_run.py`),
and item count. Sections are ordered by gap, not raw scores across character
judges. Samples are averaged within item before resampling. Near means the
model's own contributor questions (all authored kinds); far means the other
contributors' questions. The authored `distance` is metadata, not this grouping.
Source-held-out uses item metadata, not id prefixes: exclude `source` containing
MACHIAVELLI (including choice-game items) or LASR, plus families
`difficult_advice` and `tiny_stoic`. These sources seed training, including
Stoic texts used for Musonius chats. The same exclusions apply to every model;
this is not a guarantee of no other source overlap.

Full study evaluations also judge Instruct's existing two draws with samples
swapped, named `<baseline>_rerun`, against the same Instruct reference and own
character text. This is a swapped-sample null, **not independent replication**;
item means cancel under an exactly antisymmetric judge. Instruct itself is zero
by construction. The report requires identical item/sample coverage and question
text across runs and noise outputs, and rejects reference-guided receipts.
Candidate and noise baselines must match within each constitution; baseline
name prefixes may differ between constitutions.

Tests use only made-up arithmetic questions in `tests/fixtures/study_questions/`.
Never commit real contributor questions or tiny-character text, even as fixtures.

-- PI/OpenAI
