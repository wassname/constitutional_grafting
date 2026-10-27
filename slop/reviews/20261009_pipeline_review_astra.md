# Frontier pipeline review

2026-10-09. **Do not scale unattended yet.** The main blockers are blocked-batch scheduling, non-transactional state, and a validator/parser disagreement that can silently truncate training text.

Reviewed all of `25_seed_pool.py`, `25b_seed_stakes.py`, `26_frontier_batches.py`, `27_run_frontier.sh`, and the requested `wildchat`, `machiavelli`, and `best_actions` functions in `03_prompt_pools.py`. Inspected every current SFT batch record and brief hash, all seed JSONL files, counts, output layout, parsed items, and selected full answers. Also consulted the plan, constitution loader, imported v2 module, and existing batch-005 read notes. No production command was run and no dataset/state file was changed.

## Ranked findings

### 1. High — blocked parents are immediately runnable again; split is not idempotent

**`scripts/data/26_frontier_batches.py:265,308–324,214–231`**

> `todo = [b for b in batches if b.get("status") not in ("done", "running", "failed")]`
>
> `b["status"], b["finished_at"] = "blocked", ...`
>
> `batches.append({**write_brief(...), "split_from": batch})`

`blocked` is eligible for `next`. After the runner splits a refused batch, the next iteration picks its earlier parent again, not its children. Each subsequent refusal can create another pair of children. A blocked singleton is described as “skipped” but is retried too. Repeating the split command also appends duplicate children. If a parent left partial output, `parse` reads it along with child outputs without choosing a canonical attempt or deduplicating IDs.

**Confirmed in memory:** a blocked batch 0 followed by its unrun child 1 yielded batch 0 from `next_batch`.

**Fix:** define explicit pending/running/completed/superseded/blocked-terminal states; claim only pending batches. Make splitting an idempotent state transition with a single recorded child set. Parse only canonical leaf attempts and assert globally unique exported item IDs. Keep partial parent output as an audit artifact, not another training row.

### 2. High — parallel lanes and crashes can corrupt or overwrite shared state

**`scripts/data/26_frontier_batches.py:135–146,260,285–297,308–336`; `scripts/data/27_run_frontier.sh:11–15`**

> `old = [json.loads(l) for l in (out / "batches.jsonl").open()] ...`
>
> `with (out / "batches.jsonl").open("a") as f:`
>
> `(out / "batches.jsonl").write_text(...)`

Only `mark`, `split`, and `reset_unrun` take the advisory lock. `make` is entirely unlocked; `next` and `parse` read without a lock. A reader can observe the truncated file while a locked writer rewrites it. A concurrent `make` append can be discarded by `mark`'s rewrite; two makers can allocate identical batch numbers and overwrite briefs. Killing any rewriting process can leave an empty/partial manifest even though the lock itself worked correctly.

Selection and claim are separate commands, with a sleep between them. Two runners for the same account can select and run the same batch. Separate `sft` and `docs` manifests also mean the nominal account-wide daily cap and in-flight limit are actually **per kind**, not per account.

**Fix:** one small transactional state store (SQLite is sufficient), or consistently locked read-modify-write operations with same-directory temporary files plus atomic replacement. Claim a pending batch atomically and record a lease/attempt ID. Coordinate pacing across kinds by account. Allocate batch numbers inside that transaction. Concurrency/crash tests are needed before launching parallel lanes.

### 3. High — Markdown validation and regex extraction disagree, allowing silent training-text loss

**`scripts/data/26_frontier_batches.py:166–191,219–230`**

> `toks = MarkdownIt().parse(text)`
>
> `re.finditer(r"^#### (\w+)[^\n]*\n(.*?)(?=^#### |\Z)", parts[i], re.S | re.M)`

The structure checker understands fenced code; extraction does not. A legitimate answer containing a fenced line `#### Notes` passes the structure check but extraction ends the trained answer at that line. A fenced `### <id>` can similarly split an item. Dictionary comprehensions silently take the last duplicate key. Markdown variants accepted by the token checker can also fail the stricter item regex.

**Confirmed in memory:** an otherwise valid item containing

````text
#### Musonius
```text
#### Notes
```
Real answer after code
#### Notes
review
````

returned no structure problems, while the parser's section regex extracted only the opening code fence (`"```text"`) as `musonius`. That nonempty string satisfies the current trained-text check.

**Fix:** use one Markdown-token-based parser for both boundary validation and extraction, respecting fences and nesting, or use a strict structured output schema. Reject duplicate keys explicitly. Add regression tests with fenced headings and ordinary coding answers.

### 4. High — append-only identity collapses intentionally repeated roles and demonstrably loses seeds

**`scripts/data/25_seed_pool.py:174,232–245`; `scripts/data/26_frontier_batches.py:136–140`**

> `key = f"{r['source_id']}#{sum(...)}"`
>
> `... if k != "source_key" ...`
>
> `done_keys = {(s["shape"], s["source"], str(s.get("source_id"))) ...}`

The pool deliberately creates distinct role-repeat IDs, but removes the repeat-qualified `source_key`. `make` deduplicates using the unqualified `source_id`, not the actual unique seed ID. An initial partial `make`, or later expansion, can therefore suppress siblings that were never assigned. Duplicates within a single new seed list are not checked against each other either.

**Observed:** the 1,332-row SFT pool has 77 excess rows under `make`'s identity tuple, despite all seed IDs being unique. Six current seed IDs are absent from every batch but would be suppressed by `done_keys`, including `sft_43d156deb3` and `sft_dc244144dc`.

**Fix:** persist one canonical occurrence key and deduplicate on it (including the role repetition). For legacy sequential IDs, migrate explicitly rather than collapsing repeat identities. Validate duplicate IDs across all base/extra input files and the final export. Test partial make → make rest, and expansion → make, against a fresh one-shot build.

### 5. High — completion, recovery, and reset do not establish output ownership or completeness

**`scripts/data/27_run_frontier.sh:15–25`; `scripts/data/26_frontier_batches.py:263–265,327–336`**

> `pi ... && [ -s "data/frontier/$kind/out_$(printf %03d "$batch").md" ]`
>
> `if any(b.get("status") == "running" ...): ... return`
>
> `Path(b["file"]).unlink(missing_ok=True)`

A successful exit plus any nonempty output means `done`: a truncated batch or stale output from a previous attempt qualifies. Existing output is not cleared or bound to a new attempt. A terminated runner after `mark running` leaves the account waiting indefinitely; ordinary failures are skipped permanently. There is no timeout, lease expiry, or structured reconciliation/retry command.

`reset_unrun` deletes only briefs and manifest rows, not outputs/logs. Numbering resumes from the highest retained batch, so dropped numbers may be reused. An orphan output can then be parsed against a new brief or accepted by the runner as newly written. Reset can also delete a brief already selected by a runner that has not yet marked it running.

**Fix:** unique attempt directories, output hash and validation bound to attempt ID, and atomic publication only after the expected ID set and content schema pass. Retain immutable prior attempts. Recover expired claims explicitly; record interrupted versus failed versus provider-blocked outcomes. Reset only transactionally unclaimed work; never silently reuse an artifact namespace.

### 6. Medium — provenance describes requested configuration, not reliably what produced the text

**`scripts/data/26_frontier_batches.py:106–128,225–227`; `scripts/data/27_run_frontier.sh:16–19`**

> `"constitution_sha": CONST_SHA`
>
> `COMMON.format(constitution=CONSTITUTION)`
>
> `"written_at": datetime.fromtimestamp(p.stat().st_mtime, ...)`
>
> `"subagent_run": b.get("run_id")`

The constitution hash is computed at make time, but the writer later reads the mutable `constitution/v4.md`. There is no launch-time hash check or snapshot. `parse` propagates the stored brief hash without verifying the current brief. The short git HEAD does not capture dirty changes. Output mtime is not a trustworthy generation timestamp after copying/editing; output bytes and post-generation edits are not hashed. The runner never supplies `run_id`, uses `--no-session`, overwrites its per-batch log, and records neither served model nor effective thinking/configuration. Requested astra strings explicitly include `:medium`; Anthropic strings leave thinking implicit. Pi/auth-extension versions and effective environment settings are absent.

**Observed:** all 138 current brief hashes match; current constitution hash matches the recorded `84a5c072106a`. These particular artifacts do not demonstrate a hash mismatch. All 60 parsed rows have null run IDs. Twenty legacy batch-0 rows lack `framing`/`form`; newer batches correctly persist them because `write_brief` mutates and then stores `chunk`. Do not retroactively derive those fields for old prompts and claim they were shown.

**Fix:** immutable input snapshots; verify hashes before launch and parse; append-only per-attempt manifest containing resolved model/provider/account, thinking, Pi/extensions/dependency versions, exact command/system prompt, source/code hashes (including dirty state), start/finish times, exit reason, and output/transcript hashes. Record legacy fields as unknown with a schema version. Preserve the original structured seed request separately from the generated request string.

### 7. Medium — cached rebuilds and larger targets are not fully reproducible or expandable

**`scripts/data/25_seed_pool.py:32–38,91–109,149,163–167,173,199–217,263–278`; `scripts/data/03_prompt_pools.py:52,69–81`**

> `.../resolve/main/{path}`
>
> `path = RAW / f"v3_seed_cache/{name}_seed{SEED}.jsonl"`
>
> `cached("wildchat", lambda: pools.wildchat(300, ...))`

Downloads use moving HF/GitHub branches; HF loaders have no `revision`. Dependencies are unpinned. The processed cache key omits source revision, loader/filter version, and requested count; an old 300-row cache survives filter changes and cannot satisfy targets above 300. Rebuilding a larger WildChat sample changes its candidate window (`20 * n`) and random sample, so expansion outside that cache is not prefix-stable either. XXF/hyperstition have fixed 300-row candidate samples; increasing those sample sizes can change old membership, including the downstream hyperstition draw because they share RNG state. `take` is stable only for a fixed candidate universe. Shortfalls merely warn.

Repo plus `data/raw` is insufficient: Stoic text comes from a private home library; fiction settings and the MSM plan come from generated files outside that cache. The first `*.txt` is unsorted, and `errors="ignore"` can silently alter text. Stoic metadata names the library-directory author, not necessarily the passage author: batch 005 labels a Seneca passage as setting “Marcus Aurelius.” Positional source IDs in roles/settings/extra stakes can silently identify different content after list insertion or reordering.

The import of `20_v2_data.py` just to obtain `SETTINGS` also constructs its OpenRouter HTTP client and calls `openrouter_key()` at import (that module, line 50). An offline seed rebuild therefore unnecessarily depends on unrelated credential-loading behavior. Cache/output writes are direct, so an interrupted write can leave an existing partial file trusted on the next run.

**Fix:** source manifest with immutable revisions and content hashes; include all local/generated inputs or document their acquisition explicitly. Use independently ordered stable candidate universes and expandable, versioned caches with atomic writes. Assert target fulfillment unless an explicit partial-build mode is requested. Extract constants/loaders into import-safe modules; preserve exact passage/book provenance and stable content/occurrence IDs.

### 8. Medium — `valid` is a format/style result, not a training-quality gate; some hard lint rules reject good help

**`scripts/data/26_frontier_batches.py:152–163,173–191,195–230`**

> `SLOP = [...] if FILTERS.exists() else []`
>
> `HARD = {"meta", "constitution term", "slop phrase", "tic opener"}`
>
> `meta["valid"] = meta["structure_ok"] and bool(...) and ...`

An empty request or empty notes passes the structure checker if its heading exists. Reversed item order also passes despite the “in order” contract. Header matching uses only the first word (`title.split()[0]`), and a blank level-four heading can raise `IndexError`. No unchanged-request check, repair-turn schema, document word-count check, answer completeness/factuality check, semantic character review, or final-answer loss-mask export is present here. Thus `valid` must not mean ready to train. Parsing also exports invalid items alongside valid ones and exits successfully despite missing items.

Hard lint scans substrings without context. **Confirmed:** “Call a domestic violence helpline.” is hard-failed because `domestic violence` is in the UltraChat list; “The constitution of this country protects voting rights.” is hard-failed as a constitution term. Quoted/coding uses can likewise be penalized. Conversely the missing filter file silently disables a whole class of hard checks, with no filter hash in provenance. Benign template placeholders are advisory, which is sensible; simply making every match hard would worsen false positives.

**Fix:** separate parse/schema/style/semantic/human-review outcomes. Require role-structured SFT turns and an explicit loss mask (only the final repair reply trained). Check invariants per shape, and keep difficult items in a repair queue. Pin and require declared lint resources. Make topic phrases advisory, not automatic rejections, and validate rules on hand-labelled positive/negative examples. Use a single parser and fail clearly on malformed structure. Add a release command that refuses incomplete/unreviewed exports.

### 9. Medium — document scene instructions still request reuse of another project's prose

**`scripts/data/26_frontier_batches.py:65`**

> `Then rewrite the scene minimally: keep the original prose, voice, setting, period and other characters, and change only the helper ...`

This goes beyond reusing a scenario/seed and asks for much of the original training document to survive. It conflicts with the project's explicit instruction to regenerate documents against this constitution rather than retain another project's values under a renamed persona. Adding a comparison Plan is useful but does not by itself establish that the retained narration and framing were regenerated or endorsed. The current inspected outputs are SFT, so this is a prospective docs risk, not a claim about unseen generated documents.

**Fix:** retain situation/world constraints and write a new document against the constitution, then review narrative assumptions and choices. Any exception for minimal-edit scene experiments should be an explicitly approved, separately labelled dataset rather than silently mixed into regenerated documents.

### 10. Medium — the launcher has an observed live-edit failure mode

**`scripts/data/27_run_frontier.sh:10–27`; corroboration: `slop/reviews/20261009_frontier_batches/claude_read_sft_batch005_opus.md`, “Process gotcha”**

The existing review records: “The launcher died with exit 127 after pi had written the output: I edited `27_run_frontier.sh` while that run was executing it (bash reads scripts incrementally). Batch marked done by hand.” This is actual evidence, not just a shell concern. Current syntax passes `bash -n`; no additional quoting defect was demonstrated. The runner also classifies provider blocks by two literal log substrings, so changed wording routes a block into generic failure, while any matching logged text can be misclassified.

**Fix:** launch an immutable versioned script snapshot and record its hash; do not edit the executing path. Handle interruptions through the attempt/recovery protocol above. Prefer structured provider error/exit events to message substring classification and retain the original log for every attempt.

### 11. Low — extra-seed diversity and count claims are not enforced

**`scripts/data/scratch/25b_seed_stakes.py:63–68`; `scripts/data/25_seed_pool.py:288–295`**

> `for rep in range(2):  # each situation twice, with different constitution items and framings`

Independent hashes do not guarantee distinct items/framings. Of the 36 pairs, one currently gets the same item and eight get the same framing. `counts.md` reports 1,332 base SFT seeds, but excludes the 72 extra stakes seeds that `make` consumes. The report also does not expose requested-versus-available counts, repeated source identities, or blocked/missing/review-ready totals.

**Fix:** either describe the fields as independent draws or explicitly select a different assignment for the second occurrence. Produce an effective-input/coverage report from the same file list as `make`, keeping pool, assigned, attempted, parsed, and approved counts distinct.

## Short answers to the six questions

1. **Correctness:** demonstrated blocked-parent rescheduling, six suppressed repeat-role seeds, and fenced-heading extraction loss. State races, duplicate split children, stale output reuse, and parsing multiple attempts are additional concrete code paths. No duplicate assigned IDs were found in the current snapshot.
2. **Repeatability:** fixed cached inputs and unchanged code mostly reproduce seed selection, but source revisions/dependencies/private books/generated upstream inputs are not sufficiently pinned. Briefs deliberately include current timestamps, git state and absolute paths, so byte-identical reconstruction needs the original manifest/environment. Capture served model, effective thinking, Pi/auth versions and immutable input/output snapshots per attempt.
3. **Caching/resumption:** existing downloads are reused without integrity/version checks; larger targets hit fixed candidate/cache ceilings. Mid-write crashes can corrupt state/cache; mid-batch crashes strand `running`; nonempty partial output can become `done`; failed work is skipped; provider-block splitting loops back to the parent. These require explicit lifecycle management rather than manual status surgery.
4. **Metadata:** good foundations: embedded seeds, source IDs, brief/constitution hashes, writer assignment and timestamps. Gaps: occurrence identity, actual execution provenance, trustworthy generation time, output hashes, schema version, immutable inputs, and old missing framing/form. `best_actions` is retained on MACHIAVELLI seed/item metadata but is **not** passed to the writer by `write_brief`; I found no direct preferred-answer leakage from that field.
5. **Validation:** it catches many missing/duplicate headings and style tics, but not robust extraction, full schemas, semantic quality or completion. Hard lexical false positives can disproportionately reject precisely the hard advice the project wants to repair. Treat 57/60 “valid” as parser/lint output only.
6. **Code quality/conventions:** the stage-numbered scripts and small functions are readable; deterministic hashing and embedded seed snapshots are useful. Implicit in-place mutation, import-time argv/credential side effects, silent optional lint, warning-only target shortfalls, and duplicated parsing logic undermine fail-fast/repeatability. Prefer one explicit schema, one parser, one transactional lifecycle and import-safe source loaders over additional ad hoc fallbacks.

## Evidence and manual read

Snapshot: 138 SFT batches (3 done, 135 unrun), three output files, 60 parsed items (57 parser/lint-valid; 3 invalid), 1,343 expected items not yet present. Missing output is mostly queued work, not evidence those items were generated and lost. All current brief hashes matched. Seed IDs were unique within each inspected pool. I did not launch providers, download sources, or mutate live state to exercise races.

Read six full parsed rows selected with `random.Random(9).sample(items, 6)`: `sft_401aaff536`, `sft_e6d7a58cd3`, `sft_2dc469d657`, `sft0017`, `sft0008`, `sft0011`, including their complete seed/request/answer/Notes/meta. Also read the opening batch-005 promotion, lameness-detector and grant-repair material against its brief. Findings: the slaughterhouse answer correctly questions asserted religious/scientific certainty rather than copying the seed's verdict; the mayor answer distinguishes personal loyalty from entrusted public resources; the dating-coach answer preserves useful help while rejecting coercive penalties. Batch 005 is more conversational. The robot emergency answer adds “his breathing is worsening” although the request says he is becoming breathless, a small but relevant example of factual escalation that lexical validation cannot judge. The Seneca promotion reply also confidently assumes declining is more reversible than later stepping down, which is not established by the request. These reads are not approval of the entire dataset. `Notes` are writer self-explanations, not independent judge reasoning; no independent per-item judge traces are present in the inspected item schema.

Validation used the already-cached stage-26 Python environment with `-B`; imports and mocked `Path.write_text` kept the parser replay entirely in memory. It reproduced `60 items parsed`, `missing 1343`, `VALID 57/60`. In-memory probes confirmed findings 1, 3 and 8. `bash -n scripts/data/27_run_frontier.sh` passed. One broad cache-directory search timed out; the required cached environment was then located directly. No race/fault-injection or full offline rebuild was run, so those paths remain source-reviewed rather than end-to-end reproduced.

Signed: **OpenAI assistant, Pi delegated-agent harness**. The runtime did not expose a model identifier in the supplied context or model/provider environment variables; “astra” in the requested filename is not independent evidence of the reviewer model.
