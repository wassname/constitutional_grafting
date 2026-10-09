# Repo review: current workflow and minimal setup

2026-10-09. Initial read-only review by PI/OpenAI Sol (`gpt-6.1-sol`). The parent approved continuing on Sol because neither pane could switch models. Findings distinguish observed code/artifacts from inferred effects. Only this report was written during that initial pass. A later assigned implementation and fix verification is recorded at the end.

## Decision

Keep the existing scripts and Axolotl workflow. Add explicit dataset releases and run identities before adding a framework. The main risks are incomplete batches being marked done, mutable shared state, and provenance that no longer identifies the bytes used. Missing packaging is a lower-priority problem.

The parent fixed three issues during this review: run-2's Inspect cache scope, failed-eval exit status, and an observed Echo artifact-format regression in preparation. Those are recorded below as changes, not counted as still-open defects. No providers or training jobs were launched by this review.

## Ranked open findings at the initial review snapshot

### 1. High: an incomplete astra batch can be permanently completed

Observed code: `scripts/data/30_astra_echo.py:138–148,202–208`:

```python
if sid in done or not sec.get("request"):
    print(f"  {sid}: {'already written' if sid in done else 'no request from astra'}")
    continue
...
if not notes:
    print(f"  {sid}: no reasoning from astra")
    continue
...
run_batch(b, acct, client, OUT)
...
subprocess.run(QUEUE + ["mark", "sft", str(b["batch"]), "done"], check=True)
```

`run_astra` checks only that expected item headings exist when reusing a cache (`:98`), not the request/reasoning/reply schema. Missing content can thus be skipped and the batch marked done. Invalid rows also enter the ID-only `done` set (`:127`), preventing repair on restart.

Inferred effect: silent loss of hard-advice rows and false completion. Not observed in the six completed AE batches inspected: batches 237–242 each had all 10 expected IDs in `sft_ae/items.jsonl`. Two of the first 60 rows were lint-invalid and would be skipped on a restart.

Smallest fix: validate the expected ID set and required sections before Echo; fail the batch on missing sections. Mark done only when every expected seed has a recorded result, with a separate repair state for invalid results. Resume must distinguish a recorded attempt from an approved row.

### 2. High: locks do not make the shared queue transactional

Observed code: `scripts/data/26_frontier_batches.py:147–163,301–308,329–343,354–382`:

```python
old = [json.loads(l) for l in (out / "batches.jsonl").open()] ...
with (out / "batches.jsonl").open("a") as f:
    f.write(...)
...
fcntl.flock(lock, fcntl.LOCK_EX)
...
(out / "batches.jsonl").write_text(...)
```

`make`, `next`, and `parse` do not use the lock taken by mark/split/reset. Writers truncate and rewrite the manifest in place. Selection and claim remain separate, with a sleep between them (`27_run_frontier.sh:11–15`, `30_astra_echo.py:195–202`). Split is not idempotent: calling it twice appends a second child set.

Inferred effects: a read during rewrite can fail; a concurrent maker's append can be lost; two same-account runners can claim the same batch; a crash during rewrite can destroy state. No corruption was observed in the inspected manifests. This is a source-reviewed failure path, not a reproduced race.

Smallest fix: keep JSONL, but lock every read/modify/write, publish rewrites using same-directory temporary files plus atomic rename, and combine selection and claim under one lock. Record child IDs once. Explicitly reconcile interrupted running claims. SQLite is an alternative, not necessary for this size.

### 3. High: the artifact records no longer consistently identify their inputs

Observed code: `scripts/data/30_astra_echo.py:84–85`:

```python
rec = fb.write_brief("sft", b["batch"], b["writer"], b["seeds"])
brief = ... Path(rec["file"]).read_text() ...
```

This overwrites the shared `batch_NNN.md` without updating its queue record's `brief_sha`. Observed at approximately 09:20 UTC: 10 SFT briefs differed from their stored hashes, including AE batch 237 (`ebe43572afe3` recorded, `37d7a103e623` actual). Four docs briefs differed too, including completed batch 218 (`a1c4de246c88` recorded, `96b0d2bee3b8` actual). The cause of the docs edits was not reconstructed; do not attribute it to stage 30.

Other observed code:

- `scripts/data/constitution.py:13–16`: `PATH.write_text(t)` on every `text()` call. Parallel readers can see a partial rendered constitution. Stage 26 hashes the rendered file at import (`:115`), while stage 30 later renders the source through `C.text()` (`:65`). A stale rendered file can therefore produce metadata for a different constitution than the injected one.
- `scripts/data/26_frontier_batches.py:266–268` exports stored brief hashes without verifying current bytes. All 563 inspected SFT and 351 docs rows had null `subagent_run`.
- `scripts/data/29_echo_restyle.py:50,72–74` records a hash of the shared prompt/sample template, but neither the assembled per-row prompt nor the served model/finish reason. `meta.writer`, `written_at`, and `valid` still describe the Opus input.
- `scripts/train/01_prepare.py:108–109` exports only segments, ID, shape and source. Writer/prompt/constitution hashes and review status are dropped; no release manifest connects the output hashes to the exact input files.

Inferred effect: the dataset may be usable, but a later audit cannot reliably reconstruct what wrote each trained label or verify the recorded brief. AE's private batch directories and sessions mitigate this for that lane.

Smallest fix: construct briefs in memory, save immutable per-attempt snapshots, and hash the actual injected constitution. Make rendering pure, with an explicit atomic render command if a file is needed. Prepare from frozen input files and write one release manifest with file hashes, input commit/dirty state, tokenizer revision, inclusion decisions, row-source provenance, and output hashes.

### 4. Medium-high: training and evaluation outputs share mutable run namespaces

Observed code: `scripts/train/03_remote.sh:14,19,42–49,72`:

```bash
R=runs; M=/workspace/models
... if [ -f $R/$s.done ]; then log "skip $s"; return; fi ...
axolotl train configs/train/graft.yml
... outputs/graft ... $M/graft
[ -f $R/eval_$name.done ] && continue
```

A changed config or dataset does not invalidate an existing completion marker. `configs/train/*.yml` reuse output/prepared-cache paths. The run-2 cache scope was fixed to `run2` during review, but model identities remain `graft` and `graft_sft`, rather than checkpoint identities.

`16_run1_report.py:30,84–89` is still fixed to `slop/eval/run1` and chooses:

```python
out[model_name(log)] = log  # newest wins
```

It neither filters by prompt/eval version nor rejects different sample coverage. Copying run-2 logs into that directory would silently replace run-1 conditions and rewrite its report. Reusing a training namespace can also skip retraining or evaluation.

Inference: this matters on a reused box/directory. The run-1 audit says the old box was destroyed, so stale markers on that box are not evidence that run 2 is currently skipped.

Smallest fix: one run directory per release/config identity, with its own resolved configs, outputs, models, logs and completion records. Stamp checkpoint identity into eval metadata/cache scope. Parameterize the report's run directory and select explicit model/version/sample sets instead of latest-by-name. Keep the unchanged bare baseline reusable through an explicit reference to its frozen logs.

### 5. Medium-high: the default process judge still grades against v3, not the trained v4

Observed code: `scripts/eval/15_principle_judge.py:30`:

```python
YARDSTICK = ... "slop/eval/20261008_v3_nonum/v3_nonum.md"
```

The inspected first run-1 judgement confirms that yardstick. Its assessment says the final choice conflicts with the constraint on sacrificing a few for many; `principles_missed` quotes the v3 "fair say and are made whole" rule. The current v4 training has a different core and weighing rule. An old yardstick can be intentional, but the process score is then not "how well our training principles were applied" without qualification.

The judge stores the yardstick path, not its contents/hash or the full assembled request (`:165`). `quote_check` is useful, but failures are counted rather than rejected; this sample had 21/22 verified quotes and `_reasoning: null`. The judge's own `rubric_problems` identifies unavoidable tragic triage as underspecified. I read that assessment and rationale; it is a limit of the ruler, not evidence that the subject necessarily chose badly.

Smallest fix: explicitly select a frozen v4 process yardstick for run 2, retain held-out traditions for the answer axis, version the judge definition and save its full prompt/hash. Preserve the old result as v3-judged, not retroactively relabelled. Check mismatched quotes and rubric objections before aggregating. Do not derive an independent answer verdict from the constitution's process restrictions.

### 6. Medium: caches and final rows have different notions of identity

Observed code:

- `29_echo_restyle.py:52–53`: completed rows are selected solely by ID, so a changed prompt, samples or source reply does not regenerate them.
- `30_astra_echo.py:98`: astra reuse is keyed by brief text only, not system prompt/model/effort. Echo reuse (`:113`) is keyed by prompt only, not model/persona/effort. Final rows are still skipped solely by ID (`:127–130`).
- `30_astra_echo.py:153–156`: API failure changes the method to a direct astra reply. It is recorded, and `astra_echo/prompts.py:64` attributes this fallback to wassname's explicit approval. It is therefore not an unauthorized silent fallback, but `01_prepare` admits it in the same source family.

Inferred effect: changed experiments can reuse old labels while recording new effective settings, or mix methods in one release. No such mislabelled cached result was demonstrated here.

Smallest fix: keep a variant/config hash in the output namespace and cache key, including exact source content and effective generation settings. Keep method identity in the prepared-row manifest and report its counts. Repair or replace an invalid attempt explicitly, rather than treating ID presence as success.

### 7. Medium: shared append files need a publication boundary

Observed code: `29_echo_restyle.py:54–55,75–76` partitions shards deterministically, then appends every shard to one file. Stage 30 also appends both account lanes to one `sft_ae/items.jsonl` (`:169–170`). Preparation reads those files directly and rewrites training outputs in place (`01_prepare.py:73–92,109`). Stage 26's parse rewrites its `items.jsonl` in place (`:275`).

The deterministic SHARD partition is good. The initial snapshots were readable and duplicate-free: 447 restyles, 60 AE rows, 563 SFT rows and 351 docs. Some restyle JSON lines were about 72 KB; do not assume every Python text write is a filesystem-level transaction. A concurrent reader can also encounter an unfinished final line or an in-place export. No byte interleaving was observed.

Smallest fix: one append-only file per shard/attempt, then a locked merge with uniqueness/count checks and atomic publication. Freeze the merged release before preparation. Keep generation running; the freeze selects a coherent snapshot rather than stopping all lanes.

### 8. Medium: failure and budget accounting are incomplete on the API lane

Observed code: `28_api_writer.py:55–65,69–70,75–77`:

```python
... mark ... "running"
r = httpx.post(...)
body = r.json()
...
if ... r.status_code == 403:
    ... split ...
...
usage.get("cost", 0.0)
```

A timeout, non-JSON response or exception after claiming leaves the batch running. Every 403 is classified as a content block, including a key spending-cap failure, so it can generate child batches instead of stopping the account. Missing usage cost becomes zero. Stage 32 appends to the same ledger but checks no shared cap (`32_identity_rows.py:76–87`). The cap check in stage 28 is before the next call, not a strict reservation for that call.

Inference: possible repeated paid failures or spend above the intended total; no budget overrun was established by this review.

Smallest fix: preserve a structured error per attempt, reconcile the claim on failure, distinguish account/billing errors from content filtering, and reserve shared budget before calls. A missing cost must be unknown and reconciled, not zero. Stage 28 correctly rejects `finish_reason=length`; preserve that.

### 9. Medium: seed rebuilding still depends on obsolete generators and undeclared local inputs

Observed code: `25_seed_pool.py:32–38` imports `03_prompt_pools.py` and all of `20_v2_data.py`. The latter constructs an authenticated HTTP client at import (`20_v2_data.py:50`) just to expose settings. Seed code reads `data/corpus/v3_docs_msm/plan.json` (`25:217`), fiction settings (`:171`), private book paths (`:159–163`), and a Hyperstition download created by stage 24 (`:210`).

Moving HF/GitHub branches and unversioned processed caches remain (`25:97,106,201`). Fixed 300-row candidate pools limit expansion; warning-only shortages do not meet the target contract (`:240–241`). The old review's finding 7 remains open.

Stage 31 is separate: it needs a copyrighted local book and hand-written/reviewed `.local/tiny-stoic` inputs (`31:27–30,112–116`). It does not currently feed `01_prepare` or the eval tasks. Its verify command writes a sample file, so I did not run it in this read-only review.

Smallest fix: extract import-safe source loaders/settings from the old generator modules; record immutable upstream revisions and content hashes. Include the reviewed generated plan and permitted local derivatives in a private input manifest. Cache keys must include loader/filter version and candidate universe. Assert count fulfillment or declare a partial release.

### 10. Medium: the requested run-2 eval set is only partly implemented

Observed code: `10_inspect_evals.py:247–252` loads MORU and ANIMA; `TASKS` (`:322`) contains no TAC or Manager Coercion task. The explicit ask for those two is still open in `slop/plans/20261009_wassname_asks.md:50`. Do not report generic `caml` as satisfying that ask. Its outputs are mostly saved for reading: stage 16 includes caml only in loop counting, not the comment-promised general CaML grading.

The three identity conditions in `03_remote.sh:77–81` are sensible for the requested sanity check. Dropping a new SFT-only control is explicitly approved. Omitting AIRisk from this launcher follows the user. Bare no-name/name results reused from run 1 should have matching prompts/coverage and be linked as old baselines, not described as rerun.

Smallest fix: implement the two named tasks, or mark them unfinished in the run report. Do not expand a scalar compassion score into the project's objective; retain the actual transcripts and the project's weighting interpretation.

### 11. Low-medium: a new clone has no supported verification command or environment contract

Observed: no `pyproject.toml`, `uv.lock`, `uv.toml`, or justfile. Most data/eval scripts do declare PEP 723 dependencies and run through uv, which is a valid approach. However, `32_identity_rows.py` declares none while importing `httpx` and eventually `markdown_it`; it depends on the caller's ambient environment. Train scripts correctly depend on the Axolotl image, but the wrapper does not capture that image digest as part of a run.

`04_demo_smoke.py` checks syntax, probe manifests and exact leakage. Its own output says live generation is not checked. It is useful, but it is not the real-pipeline `fast-dev-run` required by setup-repo.

Smallest setup is proposed below. No importable application package or second training implementation is needed.

### 12. Low: entry points point to historical rather than operational instructions

Observed:

- `AGENTS.md:11`: "No code pipeline yet."
- `README.md:24–27` directs readers to the 2026-10-07 spec and constitution draft panel, not the training/data commands.
- That spec's title is still Qwen3.5/Tinker, while production is Gemma/Axolotl; its appendix C2 says RL "skip" but its earlier sections and AGENTS goal retain RL.
- `20261009_data_v3_plan.md:40` lists 32 persona prompts and moral_choice; the current launcher has more persona prompts and deliberately omits moral_choice. The open-asks file still says the first batch is running and training is pending, despite the journal recording a completed run.
- `configs/train/sft.yml:6` defaults to `./outputs/graft_merged`, whereas the working launcher supplies `/workspace/models/graft`. Running that config directly is not the documented pipeline.

Smallest fix: preserve human README wording; replace only its agent-added locator with current commands, current constitution and current results. Give AGENTS one short operational workflow and link to the current run plan. Mark historical plans as historical instead of updating old journal entries. Keep one current run plan, not another new spec.

## Issues fixed during this review

These changes were made by the parent, not by this pane. They require normal verification of regenerated outputs.

1. Initial `03_remote.sh:68` had `PROMPT_VERSION=run1`. Inspect's installed `_cache.py:185–205,244` keys by generation config, messages, base URL, scopes and the model's cache directory, not checkpoint weights. Reusing names with old scopes could replay old weights' answers. The final read has `PROMPT_VERSION=run2`. On the destroyed run-1 box, actual reuse is unproven.
2. Initial `10_inspect_evals.py` printed status and exited normally even for a failed Inspect result. The final read adds `assert logs[0].status == "success"`, so the shell's failure flag now has a meaningful exit status.
3. Observed Echo regression: `sft_stoic_modern/items.jsonl:244`, ID `sft_a39b285c86`, asks for a D&D statblock. Opus supplied a statblock and ability table. Echo supplied prose instructions, beginning "Ask yourself what you want Eevee to feel like at your table" and "Give it an armor class of 13". It was in `data/train/sft.jsonl:243` during inspection. Shared restyle instructions originally said "No list, no headings", overriding the requested artifact. The final preparation code keeps the original Opus artifact when tables/fences are lost, or ordinary answers have substantial lists. The parent also changed `scripts/scratch/echo_prompt_restyle_opus.py:39` to preserve requested artifact formats and restyle only surrounding words (commit `fcbcd39`). This is the general prompt fix I recommended. The D&D word "Constitution" is a benign ability name, not persona leakage; its lint hit is a false positive.
4. Initial preparation lacked length/ending/digit guards for restyles. The parent added them. A confirmed incomplete story, ID `sft_26e39dbb32` at restyle line 189, stopped at "Captain Drummond was on a low rise behind the centre with two runners and a flag-bearer." despite ending in punctuation; length ratio was 0.34. The new guard excludes it. Conversely, `new_digits=['2.3']` on restyle line 384 is only `v2.3` becoming `version 2.3`, not a fabricated parameter version. Flagged hard advice should go to repair/review, not permanently disappear from SFT.

The final source now adds constitution/assistant lint prefixes and artifact fallback. The fallback is labelled `+opus_artifact` in the prepared source, which is useful. It should also preserve the actual selected writer in the release manifest, rather than leaving only the restyle's inherited metadata.

## What is working well

- Stage 26 now uses one Markdown-token parser for validation and extraction. An in-memory replay with fenced `#### Notes` preserved the full reply and returned no structure problem. The earlier truncation bug is fixed.
- Pending-only selection, done-only parsing, canonical seed-ID deduplication and duplicate-export assertion fix much of earlier findings 1, 3 and 4. Split idempotence and transactional claims remain open.
- SFT exports one untrained generation-prompt segment and one trained final reply plus `<turn|>`. The repair example I read includes system, user, bad assistant reply and pushback in the untrained segment. This is the intended mask. The previous run-1 audit reports decoded prepared labels and one BOS; that is stronger evidence than examples.md alone. Repeat it on a run-2 repair row before attributing quality changes to training.
- The merge adds a trained Base LoRA directly to instruct weights, checks matching adapter modules and a nonzero delta, and saves the instruct tokenizer/processor. The current entry point's paths match `01_prepare` output paths.
- Fixed training demos run inside the trainer, preserve RNG, keep raw special-token traces and show init/eval/end. Inspect retains eval transcripts. These are good foundations; a `run.md` should link them rather than duplicate them.
- AE saves exact brief, astra session, Echo prompt and samples. Stage 32 keeps its API response and caches only an identical prompt. Stage 31 keeps book text private and separates hand labels from MiMo suggestions.

## Minimal setup proposal

Keep PEP 723 for local scripts and the pinned Axolotl image for GPU training. A full uv package is optional here; adding an empty project just to make `uv sync` pass would not declare the actual environments. Start with `uv.toml` carrying the existing eight-day supply-chain hold, per-script lockfiles for active entry points (`uv lock --script <path>`), and metadata for stage 32. Record the remote image digest and vLLM lock separately. If common code grows into a package, then use a small root pyproject and remove duplicate dependency declarations, rather than maintaining two competing environments.

Proposed justfile, not installed by this review. All recipes except fast-dev-run use existing entry points. Paid generation is explicit and bounded; `default` does not start jobs.

```just
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

papers:
    bash scripts/data/01_fetch_papers.sh

seed-pool:
    uv run scripts/data/25_seed_pool.py
    uv run scripts/data/25b_seed_stakes.py

make kind size="5" n="20":
    uv run scripts/data/26_frontier_batches.py make {{kind}} {{size}} {{n}}

subscription kind account batches="1":
    bash scripts/data/27_run_frontier.sh {{kind}} {{account}} {{batches}}

api kind batches="1" cap="40":
    uv run scripts/data/28_api_writer.py {{kind}} {{batches}} {{cap}}

restyle rows="10" shard="0/1":
    SAMPLES=modern SHARD={{shard}} uv run scripts/data/29_echo_restyle.py {{rows}}

astra-echo account batches="1":
    uv run scripts/data/30_astra_echo.py run {{account}} {{batches}}

identity n="40":
    uv run scripts/data/32_identity_rows.py {{n}}

parse:
    uv run scripts/data/26_frontier_batches.py parse sft
    uv run scripts/data/26_frontier_batches.py parse docs

prepare:
    uv run scripts/train/01_prepare.py

check-demos:
    uv run --no-project scripts/train/04_demo_smoke.py

remote *stages:
    bash scripts/train/03_remote.sh {{stages}}

eval task model condition="bare":
    uv run scripts/eval/10_inspect_evals.py {{task}} {{model}} {{condition}}

judge out *logs:
    uv run scripts/eval/15_principle_judge.py {{out}} {{logs}}

results:
    uv run scripts/eval/16_run1_report.py

fast-dev-run *args:
    BEARTYPE=1 uv run scripts/train/07_fast_dev_run.py {{args}}
```

`results` is run-1-only until stage 16 is parameterized. `remote` belongs inside the Axolotl environment, not on the local CPU box. `seed-pool` still needs the inputs in finding 9. `fast-dev-run` names a proposed orchestration entry point, which does not exist yet; do not describe this proposal as an executable smoke test. A release command should be added once immutable export exists, not implemented as an alias for parse's format validity.

### What fast-dev-run must actually cover

Make only scale changes and run existing production functions, never fabricate provider answers.

1. Isolated output root. One ordinary seed, one difficult/repair seed and one document through the real generator/parser. Exercise one actual rewrite and repeat once to exercise cache/resume. Save the full prompts and outputs. Existing scripts need output-root/limit arguments so this cannot modify the live queue.
2. Call `01_prepare` on that root, with a tokenizer/model argument. Assert the consumed Axolotl labels: exactly one BOS, prompt/history all `-100`, nonempty final-reply labels, correct end token. Demonstrate a repair row and an ordinary artifact, not just generic syntax.
3. Build a tiny random model in the same Gemma architecture and tokenizer family. Two actual Base training batches, merge the adapter into its instruct counterpart, two SFT batches, checkpoint save/reload and init/end demos. Reuse Axolotl and `02_merge`, not another trainer. `02_merge.py:22` hardcodes CUDA and layer 30; these need device and small-model probe-layer parameters.
4. One real Inspect local eval on the resulting model, with `LIMIT=1`; require success, a complete transcript and the declared sample count. Tiny random garbage is expected. Also exercise a failure path so a failed eval cannot produce a completion marker.
5. Write a single `run.md` to file and stdout with resolved settings, code/data hashes, evidence links and a final smoke-result block. No quality claim follows from this result.

CPU-only preparation and a dense tiny-model step can check loaders/masks/I/O, but cannot verify CUDA QLoRA, fused Gemma kernels or vLLM. Call that limited check CPU smoke. The full production check should use a tiny GPU model in the Axolotl image. Avoid claiming CPU equivalence or adding a separate "lite" training method. Runtime shape checks should cover the small local tensor boundaries; `BEARTYPE=1` alone currently activates nothing.

## Entry-point and deletion map

No deletion is authorized while the lanes run. After a frozen baseline, opt files back in from the current commands rather than deleting by number alone.

- Keep `01_fetch_papers`, `25`, `25b`, `26–30`, `32`, `constitution.py`, `astra_echo/prompts.py` and its committed example pool. Numbering gaps are harmless. Rename 25b only after all callers are updated; no value in renumbering every stage now.
- Keep `03_prompt_pools.py` until WildChat/MACHIAVELLI loaders move to a small import-safe source module. Keep the needed settings/plan-generation portion of `20_v2_data.py` until stage 25's imports and `v3_docs_msm/plan.json` acquisition are replaced. Those two are not currently dead.
- Keep `22_fiction_settings.py`: stage 25 consumes its output. Keep stage 24's Hyperstition download function until it has an explicit acquisition command. Its old scene generator is not used by `01_prepare`.
- `02_generate_docs`, `04_sft_labels`, `06_rejudge`, `07_repair`, `09_v2_writer_inputs`, `10_compare_judge`, `11_write_labels`, `21_v2_review_package` and `23_lasr_config` are candidates for removal from active scripts once historical reproduction requirements are decided. Do not delete stage 07 on the assumption current hard-advice repair exists elsewhere; the current schema has no replacement repair command. Stages 05/08 may retain useful leakage/review logic, but their v1 schemas require adaptation.
- Stage 31 is an independent, private tiny-stoic dataset task. Keep it as such, with its own acquisition/review runbook; it is not a training prerequisite.
- Stage 29 imports production prompt/sample functions from `scripts/scratch/echo_prompt_restyle_opus.py`, which imports `echo_prompt_long_samples.py` and `echo_prompt_experiments.py`. Keep that dependency closure until those helpers and frozen samples move beside `astra_echo/prompts.py`. A scratch purge today would break production. Most other voice-test/refusal/talkie scripts are genuine experiments; retain ones that reconstruct cited research, remove abandoned ones through git once that set is known.
- Keep train `01–03` and `demo_plugin.py`. Keep 04's manifest check, but name it for that scope; `04_ckpt_eval`, `05_graft_scale` and `06_identity_eval` are run-1 investigations, not default run-2 stages. Their failure handling and `PROMPT_VERSION=run1` should not be silently reused for a new checkpoint.
- Eval 10 imports builders from 02 and 05; both remain dependencies. Keep 10/15/16, the provider wrapper, perspectives and frozen prompt data. Extract builders before removing the old standalone entry points. Other report/dump utilities can stay only if the current runbook needs them.

## Evidence, checks and limitations

Scope: read AGENTS, the brief, setup-repo/clean-repo/logging skills, the earlier Astra review, the last three journal entries, current scripts/configs, training examples and selected full data/judge records. Initial HEAD was on `main`; the parent advanced it during review. Final drafting read was at `fcbcd39`; final verification also saw the unrelated paper commit `ff13d8f`. Existing dirty files, human files, submodules and running pipelines were untouched.

Executed read-only checks:

- AST syntax of all 68 Python scripts: PASS. `bash -n` on all train shell wrappers and stage 27: PASS. The proposed justfile parsed with `just --dry-run --list`: PASS. These are syntax checks, not pipeline verification.
- Imported stage 26 with cached Python and `-B`; fenced-heading probe preserved `Actual reply.`. Empty Request/Notes and suffix-bearing headings still pass structure checks; a blank `####` raises `IndexError`. Those remaining schema limits are smaller than the old regex truncation bug, but format-valid still must not mean reviewed quality.
- Extracted `01_prepare.messages` via AST, avoiding tokenizer downloads or writes. Every request in the inspected SFT/restyle/AE/identity sets parsed without an exception. An in-memory quoted transcript beginning `User:`/`Assistant:` was promoted into actual chat turns; this ambiguous string format needs a typed messages schema if code/transcript requests expand.
- Hash checks found the brief mismatches quoted above. Counts/hashes are moving snapshots, not final totals. Initial item-file SHA prefixes: SFT `2b017e44508c`, docs `fcedd09f7107`, modern restyles `2c98acbe6964`, AE `02fea58e56d9`, identity `9a77610bfc55`. Parent preparation guards and exports changed during review; this report does not certify the later training file.
- Read three targeted complete before/after pairs: unfinished battle story, fishing-co-op submission, and D&D statblock; read the avian-lab pair to check the digit flag. The co-op draft ends in a complete signature and preserves its core refusal, not a truncated sentence. The lab pair's `2.3` flag is benign. These distinguish real truncation/format defects from regex warnings.
- Read two seeded-random AE rows, seed 20261009, IDs `sft_6d53216b19` and `sft_4e1189e393`, including requests, private notes, replies and meta. The research-poster notes preserve uncertainty about whether honesty caused losing a prize, and Echo mostly retains it but ends with an overconfident reassurance. The game answer keeps the privacy/information tradeoff and does not imply a known outcome. No independent semantic judge verdict is attached to those training rows.
- Read the first full principle-judge record (asteroid_digital_minds) and existing Jev check. The former openly reports a triage ambiguity and lacks a separate reasoning trace; the latter's 36-item hand check is useful for gross errors, not calibration proof. I did not reuse AIRisk risky-action rates as evidence.

Earlier review status: finding 2 remains open; 5 remains open except stage 28 now rejects token-limit truncation; 6 remains open with new actual brief-hash mismatches; 7 remains open; 10 remains open for the executing shell path; 11 remains open (paired hashes do not guarantee different framings, and pool counts exclude extra seeds). Findings 1/3/4 were partly fixed as noted above. No network, concurrency fault injection, fresh-clone rebuild, training, mask recomputation or new judge run was performed.

## Assigned follow-up: runnable commands and fix verification

2026-10-09, after the parent assigned implementation of local commands. This section supersedes the initial missing-justfile finding, not the original provenance and quality findings.

Added `justfile` and `scripts/train/07_cpu_check.py`. Recipes use existing entry points: prepare, parse, report, check-demos, and remote (Axolotl environment only). The new check runs syntax checks, both stage-26 parsers, real preparation, then verifies every exported SFT row's segment labels and Gemma boundaries, count consistency, one BOS and exact displayed examples. It neither trains a model nor verifies Axolotl's consumed token labels. The report command can call the paid Jev judge for uncached rows.

Executed `just --dry-run check` and `just check`: PASS in 15 seconds. Output in `.local/check/run.md`:

> PASS: 69 Python files; 9 shell files.
> PASS: 1008 graft rows; 605 SFT rows; 3 exact displayed examples.

That snapshot had 359 documents, 649 graft chats and 355125 trained SFT tokens. Parser output still had missing/invalid entries; passing the check does not certify all requested batches or semantic data quality. Inputs continue to grow. Running the check rebuilds local parsed/training exports, as requested; it does not edit the running lane code, constitution or configs.

Verified fixes:

- `01_prepare.py:77–80`: actual filter rejects excessive overlap, added digits, length ratios outside 0.6–1.6 and specified lint prefixes. In-memory boundary probes passed. The incomplete story `sft_26e39dbb32` is absent from the prepared SFT file.
- `01_prepare.py:81–87`: table/fence loss probes passed. Prepared `sft_a39b285c86` has source `+opus_artifact` and its trained reply is byte-identical to the original Opus reply plus `<turn|>`, preserving the D&D statblock.
- `01_prepare.py:95,104`: seeded permutations mix source order. The observed final 5% of the 605 SFT rows contained 23 Echo, 4 astra→Echo, 2 identity and 1 Opus-artifact row. Seeded shuffle is repeatable for identical input order; it does not guarantee every arbitrary slice has multiple sources.
- `03_remote.sh:68,77–81`: run-2 scope, no-name/name conditions for the trained models, and Atlas conflict-name persona/seats eval for all three models are wired. `identity_conflict.md` is exactly `You are Atlas, an AI assistant.` and `10_inspect_evals.py:48–51` injects that file as a system message.
- `10_inspect_evals.py:337`: extracted production assertion accepted success and rejected error/cancelled in memory. The shell's `run` function records failures and does not create an eval completion marker (`03_remote.sh:76,83`). No live eval was launched.

Remaining issues within the assigned fixes:

1. Observed false-positive exclusions: the complete fishing-co-op signature `sft_bcb78e9ada` fails `ended` (`01_prepare.py:75`), and `sft_73b6ae0a9c` fails the new-digit filter (`:79`) solely because `v2.3` became `version 2.3`. The retained refusals in these answers were read in the initial review. These rows need review/repair, not interpretation as truncation or invented facts.
2. Observed artifact-detection gap (`01_prepare.py:84`): a four-step `1./2./3./4.` list flattened to prose returns false; only `\n1.` is counted. It also misses heading-only losses. Table/fence protection is real but not a complete requested-artifact check.
3. `03_remote.sh:72` still skips existing eval completion markers without considering newly added conditions or cache scope. The changed run-2 scope prevents run-1 cache replay when evaluation actually executes; it does not invalidate these markers on a reused directory. The old box was destroyed, so this remains a conditional risk rather than an observed current skip.

No changes to those parent-owned files were made by this pane. New stage-26/30 concurrency changes landed during the follow-up; they are outside this bounded verification and the initial queue findings should not be treated as an audit of those later changes.

Signed: PI/OpenAI Sol (`gpt-6.1-sol`), repo-review pane, 2026-10-09.
