# Vast skill review, 2026-10-25

PI/OpenAI (Sol). Target: `/home/code/.pi/agent/skills/vastai/SKILL.md`, checked against run11 lease1 (instance 57460369) and the current controller at project commit `714e236`. This is a rental-operations audit, not a re-evaluation of character training. No rentals, API mutations, or skill/code changes were made.

## Stage evidence

| stage | expected | observed | expected? | clues | missing metric | consequence |
|:---|:---|:---|:---|:---|:---|:---|
| Offer | Suitable host and total-cost quote | Verified Texas datacentre; RTX PRO 6000 S; 300 GB; $1.8444/h | yes | `lease1/rental_quote.json` | Reconciled invoice | Host choice worked on this lease |
| Preflight | GPU/CUDA/disk/download checks | CUDA 13.0; 10 GiB write at 3.7 GB/s; pinned Base download in ~49 s | yes | `controller.log:8–55`; `setup.log` | No separate download benchmark | No observed host-performance failure |
| Watchdog | Authenticate and stop after lost heartbeat | Startup GET 200; stop path unexercised by lease | unclear | `box_runs/watchdog.log`; watchdog lines 13–23 | Real stop/state confirmation | Authentication is not a stop-path test |
| Controller recovery | Reuse lease and original deadline | Reattached; later exit 137 followed by another attach | yes | `controller.log:900,2878–2884`; handover receipts | Demonstrated exclusive owner lock | Recovery worked, but ownership depends on coordination |
| Allocation | Required comparisons fit | Documents and chatr13 completed; chatmix/control skipped | no | `box_runs/run11_execution_plan.json` | Chat comparison | Successful infrastructure did not complete the research plan |
| Retrieval | Preserve and verify before destroy | Four final adapters verified; checkpoint files copied | yes | `retrieval_verified.json`; closure receipt | Checkpoint hashes | Final weights are verified; checkpoint integrity has weaker evidence |
| Destruction | Delete correct instance; confirm absence | Destroy response true; controller exit 0 | yes | `destroy_response.json`; `controller.log:4566–4568` | Independent deadline enforcement receipt | Actual closure is supported; a guaranteed cap is not |

All lease paths in this report are under `/workspace/2026/constitutional_grafting/slop/eval/run11/lease1/` unless stated otherwise.

## Bottom line

The skill helped produce a working rental and verified outputs. Keep Vast for this workload. The evidence does not justify describing the example controller as safe under every crash, or its saved deadline as an independently enforced spending cap. Fix the failure paths before another unattended lease; switching providers is not required to address these bugs.

The latest lease lasted an estimated 26.03 hours and cost approximately $48.00 at its recorded hourly rate. This is not an invoice and excludes separately metered traffic/API charges. The credit drop since reattachment covers only part of the lease. Successful closure does not prove the preventive safeguards worked.

## What I read and checked

- Entire Vast skill, all 487 lines of `scripts/eval/38_run10_chat_rental.py`, all 25 lines of `scripts/train/box_watchdog.sh`, the remaining-stage planner, rental quote, setup, watchdog, handover, execution plan, final retrieval and closure receipts.
- Entire controller log was processed, not just its tail: 4,568 logical lines. Removed only blank lines and three exact repeated SSH welcome/locale messages, then read all 160 remaining lines with original source line numbers. The original log remains unchanged. No model-training log or generated answer is needed to decide the operational claims here; their scientific merits are outside this audit.
- All six source-file hashes bound by `closure_usage.json` match. All four local final adapter/config pairs exist and match recorded sizes. I did not rehash the ~16 GB of binaries; final binary hashes are supported by the bound retrieval receipt.
- Reran seven maintained retrieval tests: all passed. Four test the older run9 controller; three test the current chat controller. This is not seven end-to-end tests of the current lease lifecycle.
- Ran an offline probe of the actual watchdog function/stop branch, replacing curl with a failing shell fixture. No network or credentials were used. The branch reported a failed API response and exited 0.
- After adding related guides, a fresh model read only the Vast skill and answered a realistic six-job routing/retry/recovery request. It selected Modal, linked the relevant guides, rejected a per-attempt timeout as a total spending cap, and preserved unretrieved Vast outputs. Its answer is saved in `20261025_vast_skill_evidence/related_guidance_check.md`. This tests the prose guidance, not cloud execution. Local `vastai 1.8.2 destroy instance --help` confirms `-y/--yes` skips confirmation.
- Asked both participating sessions about independent deadline guards. Neither could provide a guard receipt. `const_v2` reports its supervisor inspected all visible scheduled tasks and found no run11 hard-destroy task. This is corroborating session evidence, not a fresh provider query by this audit.

Verification outputs:

- `/workspace/2026/constitutional_grafting/slop/audits/20261025_vast_skill_evidence/retrieval_tests.log`
- `/workspace/2026/constitutional_grafting/slop/audits/20261025_vast_skill_evidence/watchdog_failure_probe.log`

## Chronology and direct evidence

The controller chose a host that passed more restrictive filters than the skill's minimums. Its recorded quote was:

> Quote: RTX PRO 6000 S, datacentre Texas, US, $1.844/h including 300 GB; 33.5-hour reserve $63.79

Source: `controller.log:2`. This is the controller's quote, not the final bill.

Preflight recorded:

> 10737418240 bytes (11 GB, 10 GiB) copied, 2.92122 s, 3.7 GB/s

Source: `controller.log:34`. `setup.log` also records the pinned Base snapshot, runtime versions, and a passing routed-expert merge regression. A first Stoic upload failed and the existing partial-transfer retry completed (`controller.log:197–245`). This supports retrying transport failures, rather than treating each one as a bad host.

The lease survived controller loss:

> CONTROLLER EXIT 137

> ATTACHED to 57460369

Source: `controller.log:2878,2882`, separate contiguous lines. Remote training continued; the reattached controller retained the existing lease. A prior attach is also recorded at line 900. The cause of exit 137 is not established here.

The work estimate was insufficient. The final execution plan records chatmix `required_hours_with_margin: 8.180489510489512` against `remaining_eval_hours: 6.6259656413396195`, and `selected: false`. Chatgen then records `dependency_satisfied: false`. These are scheduling outcomes, not evidence that the GPU or the scientific method failed.

Final closure is directly recorded:

> RENTAL DESTROYED 57460369
> RETRIEVAL COMPLETE; rental destroyed. Chat adapters in /home/code/.local/share/cg_run10_adapters
> CONTROLLER EXIT 0

Source: `controller.log:4566–4568`. `destroy_response.json` says `{"success": true}`. The controller's `destroy()` additionally checks that the instance is absent from the account list before logging success. `last_instance_metrics.json` was captured before this, so its running status does not contradict closure.

## Failure hypotheses and recommended changes

These are nonexclusive. Probabilities are confidence in the described defect or explanation, not estimates of incident frequency.

### H1: heartbeat can expire during retrieval [bug; almost certain, 99%]

- Mechanism: both `run()` and `attach()` stop/join the heartbeat before entering retrieval. Transfers may outlast the one-hour silence limit.
- Evidence: `38_run10_chat_rental.py:469–476` calls `stop.set()` and `heartbeat.shutdown(wait=True)` before `retrieve_or_stop()`. The skill and watchdog comment instead say heartbeat continues through retrieval.
- Contrary evidence: this lease's retrieval completed before the watchdog stopped it. The watchdog log has only its startup line.
- Discriminator: offline lifecycle test with a deliberately slow fake retrieval; heartbeat should keep updating until copying and teardown finish. Present ordering stops updates immediately. No paid run is needed.
- Action: keep heartbeat active through retrieval/teardown; use the retrieval/hard deadline rather than the already-expired runner deadline for its SSH timeout. Stop it in the outer cleanup. Add the test to the current controller's suite and correct the skill only after the code works that way.
- Interpretability: yes for actual closure; no support for the skill's stronger retrieval-safety claim.

### H2: saved hard deadline is not an enforced spending cap [harness; almost certain, 98%]

- Mechanism: `hard_destroy_epoch` bounds command timeouts. It does not schedule an independent destroy action; a live heartbeat can continue despite a stuck monitor, while a stopped disk keeps billing storage.
- Evidence: `38_run10_chat_rental.py:114–118` computes a retrieval timeout from `hard_destroy_epoch`; `retrieve_or_stop():153–163` stops and raises on copy failure but does not arm later destruction. The actual watchdog checks silence only (`box_watchdog.sh:19–25`). Neither owning session supplied an independent guard receipt.
- Contrary evidence: controller monitoring and per-command timeouts do bound many normal paths. This lease closed well before 33.5 hours. An uninspected external mechanism is still possible.
- Discriminator: before a future lease, require a durable guard identity, original deadline, exact instance ID, and offline evidence that a controller stuck while heartbeating still triggers the guard. A timestamp in JSON fails this check.
- Action: define separate execution, retrieval and storage-retention deadlines. Arm an out-of-controller guard with recorded evidence and an explicit data-loss policy. Stop GPU use at the execution limit; destroy only after verified retrieval or the agreed recovery deadline. Do not recreate this closed lease's cancelled schedules.
- Interpretability: retrospective cost/closure yes; guaranteed maximum spend no.

### H3: watchdog may report success without stopping [bug; almost certain, 99%]

- Mechanism: curl has neither bounded connect/total time nor HTTP failure handling. The stop call is embedded in `echo`, followed by unconditional `exit 0`; an API rejection or transport failure can leave GPU billing active and retire the guard.
- Evidence: `box_watchdog.sh:13–14,22–23`; offline probe prints `{"success":false,"error":"fixture API failure"}` and `watchdog branch exit status: 0`.
- Contrary evidence: initial GET authentication returned 200. That shows initial access, not future stop reliability. No real failed stop was observed on this lease.
- Discriminator: mocked timeout/429/500/false-success cases should remain under supervision and retry within a bound; accepted stop should be followed by state confirmation. Current offline failure fixture exits successfully instead.
- Action: bounded curl calls, response validation, bounded retry, and read-only confirmation of stopped state; retain an external guard for host/controller failure. Fail-fast alone is insufficient for a billing safeguard.
- Interpretability: actual closure unaffected; lost-heartbeat protection remains unproved.

### H4: per-job fit can omit the comparison the lease was meant to answer [method; almost certain, 99%]

- Mechanism: equal token counts can hide different row/update counts. The planner admits chatmix on its own projected runtime, while its required generic control is checked later.
- Evidence: `box_runs/remaining_stages.py:74–90` budgets each chat separately. The final plan records chatmix needing 8.18 h with 6.63 h left and chatgen ineligible. The lease plan notes the corrected control has 9,418 rows versus 6,483 mixed rows.
- Contrary evidence: this lease skipped both mixed/control jobs, avoiding a newly stranded mixed adapter. Its final time-fit gate used measured update speed plus 20% margin and preserved the deadline.
- Discriminator: a synthetic budget where chatmix fits but chatmix+control+evaluation does not should reject the pair before either starts. Current per-job gate would admit chatmix.
- Action: reserve dependent scientific comparisons as a unit, including preprocessing, training, evaluation and retrieval. Forecast from actual rows, optimizer updates and measured speed, then compare with token estimates. Keep optional standalone baselines separate.
- Interpretability: document comparisons and standalone chatr13 remain interpretable under their separate audits; the omitted chat-control question remains unanswered.

## Skill changes to make after the implementation is checked

1. Point to `38_run10_chat_rental.py` for the currently used chat/evaluation lifecycle, including `attach` and non-destructive `snapshot`. Keep `37` explicitly identified as the simpler document-only example. These are project-specific scripts, not a portable controller package.
2. Replace the claim that a crash anywhere ensures retrieval/destruction with its actual limits. A SIGKILL does not execute `finally`; a lost controller needs an independent guard.
3. State that a declared deadline needs an armed enforcement receipt. A heartbeat silence limit and an absolute lease limit solve different failures.
4. Require one controller owner per instance. Retrieval's `flock` serializes copying only; it does not prevent two `attach` owners from both deciding to tear down a lease. Session coordination worked here, but is not a lock.
5. Keep the strong existing rules: data-centre/reliability/network-cost filtering; direct/proxy SSH fallback; exact upload provenance; final hash checks; stop-on-retrieval-failure; verify absence after destruction. Add resumable upload retries and incremental snapshots.
6. Budget complete comparisons using rows/updates as well as tokens. Record skipped work as not run.

The follow-up request authorized related guides at the end of the Vast skill. That section was added in `/home/code/.agents/skills/vastai/SKILL.md`; the controller/watchdog and the existing lifecycle instructions remain unchanged. The safety changes above still require implementation and tests.

## Decision and limits

1. Resolve condition: rental closure and final artifact preservation **met** (`job_exit: "0"`, four final adapter receipts, destroy success and controller exit 0). Completion of every originally requested comparison **not met**. Robust unattended maximum-spend guarantee **not established**.
2. Predictions: no separate pre-run operational predictions were supplied to this audit. The skill's expectations were the checks listed in the stage table. Record failure-path expectations before the next lease.
3. Earliest unsupported safety step: watchdog startup authentication → reliable stop action. Exercise the offline API failure cases before claiming that implication.
4. Validity: invalid here means the claim that this specific lease closed with verified final outputs is wrong. Estimated probability below 5%, given matching bound receipts and teardown evidence; credible operational success. This does not validate every advertised safeguard or the scientific results.
5. Highest-information clues: final hashes plus destruction/absence check; heartbeat stopped before retrieval; offline stop failure still exits 0.
6. Missing evidence, ranked: independently armed cap; robust stop-path tests; current-controller lifecycle/ownership tests; checkpoint hashes; reconciled provider invoice. None is evidence that a lease is presently running.
7. Code changes: H1 heartbeat ordering; H2 independent deadline enforcement; H3 watchdog validation/retry; H4 dependency-aware admission. Add controller owner locking alongside H2.
8. Reinterpretation: successful closure demonstrates a successful execution, not protection against all failures. A partial research plan is not a GPU-provider failure.
9. What changes the verdict: an actual independent guard receipt and passing failure-injection tests would strengthen unattended-safety claims. A missing/mismatched adapter receipt or failed post-destroy absence check would weaken closure.
10. Sequence: fix/test watchdog and lifecycle locally; add a single owner plus separately enforced deadlines; update the skill to match; only then consider another approved lease. Pair-budget changes concern experiment planning and should not silently alter training recipes.

## GitHub findings: Hermes and other guides

Used authenticated `gh` for public-source reads only. The delegated scout searched GitHub and read the source inventory; I checked the important recommendations against the primary files. No fetched code was executed.

- [Hermes Modal skill](https://github.com/NousResearch/hermes-agent/blob/4ea8d23cc9f527332ccb1d55359b27741b6ea51b/optional-skills/mlops/modal/SKILL.md): explicitly teaches serverless GPU training/inference, persistent Volumes and scale-to-zero functions. Parent read in full. Its statement “RunPod: For longer-running pods with persistent state” is an alternative recommendation, not a RunPod integration.
- [Hermes Lambda Labs skill](https://github.com/NousResearch/hermes-agent/blob/4ea8d23cc9f527332ccb1d55359b27741b6ea51b/optional-skills/mlops/lambda-labs/SKILL.md): scout-read reference for SSH rentals and explicit termination/checkpoint storage. Useful parallel to our Vast workload; do not copy its price tables.
- [Official Vast agent skill](https://github.com/vast-ai/vast-claude-plugin/blob/c90a6cceb7d5fd0e206c0dc705d7750a198d7768/skills/vastai/SKILL.md): parent read all 606 lines. Useful warnings include noninteractive confirmation flags, registering SSH key contents rather than a filename, `--cancel-unavail`, and reading startup logs before blind retries. Check installed-version help before importing exact flags. Do not adopt its direct-REST prohibition or unconditional destruction on offline/unknown state. Our REST controller worked, and artifact recovery has priority over deleting a temporarily inaccessible box.
- [Vastkit skill](https://github.com/RazinAleksandr/vastkit/blob/8b40befb8a10a6fc5b6befcbac2b83bf44079fa2/skills/vastkit/SKILL.md): scout-read candidate with tests/CI and estimated whole-session cost. It says “Do not destroy the instance merely because a transfer command returned zero when the expected artifacts are missing.” This agrees with our manifest/hash policy. No recommendation to install it without a separate code review.

Hermes' [backend registry](https://github.com/NousResearch/hermes-agent/blob/4ea8d23cc9f527332ccb1d55359b27741b6ea51b/tools/terminal_tool_config.py#L120-L121), checked by parent, includes local, Docker, SSH, Modal, managed Modal, Daytona and Vercel Sandbox. No dedicated Vast or RunPod backend/skill was found in the inspected tree. Generic SSH can still reach a Vast/RunPod box. Backend support tells us what Hermes can use, not which provider its maintainers actually use most.

Hermes' [Modal environment](https://github.com/NousResearch/hermes-agent/blob/4ea8d23cc9f527332ccb1d55359b27741b6ea51b/tools/environments/modal.py#L155-L165) sets a default sandbox timeout of 3,600 seconds. That is a useful independently enforced lifetime model. However, its cleanup suppresses snapshot failures before terminating and suppresses termination exceptions; do not copy those policies into our artifact-preserving controller. Parent checked creation and cleanup code.

Recommendation: keep our concise workload-specific Vast skill, borrow the checked operational lessons, and link the vendor CLI reference rather than copying its 606 lines. Modal is an available alternative for independent short jobs, not a demonstrated fix or cheaper replacement for this lease.

Full source inventory and parent corrections: `/workspace/2026/constitutional_grafting/slop/research/20261025_vast_hermes_github_sources.md`. The original scout overgeneralized Modal billing and overstated vendor-source certainty; corrected/qualified before delivery.

## Follow-up: is Modal better for us?

Likely better for unattended independent stages; more expensive per GPU-hour for this particular lease. This is a prospective comparison, not a benchmark or migration result. No paid Modal calls were made.

On 2026-10-25, [Modal's GPU guide](https://modal.com/docs/guide/gpu) lists `RTX-PRO-6000`. The raw [pricing page](https://modal.com/pricing) lists Nvidia RTX PRO 6000 at `$0.000842` per second (the numeric text is in an `sr-only` span, omitted by the readable extractor). Multiplying by 3,600 gives $3.0312/GPU-hour. The recorded Vast lease was $1.8444/hour including allocated CPU, RAM and 300 GB disk.

At equal 26.0262-hour runtime, Modal's GPU alone would be about $78.89 versus the $48.00 Vast elapsed-rate estimate. Modal adds CPU/RAM, possible warm/startup time and other applicable charges; credits are excluded from this comparison. It would need to finish in less than 60.8% of Vast's time to match the recorded Vast rate before those extras. Same-GPU speedup is unmeasured, so do not assume that. Operational simplicity can still be worth the premium. Modal currently advertises $30/month Starter compute credits, which can subsidize a small pilot but do not lower its underlying rate.

Useful approaches, in priority order:

1. **Separate storage from the GPU lifetime.** Put pinned models and outputs in a Modal Volume, commit checkpoints, and fetch them after compute stops. This removes the need to keep a GPU running during rsync. Keep explicit artifact manifests and hashes. [Volumes documentation](https://modal.com/docs/guide/volumes) says background commits occur every few seconds and a final commit occurs on shutdown; explicit commits establish the application's intended save boundary. Avoid concurrent writes to the same path (last writer wins).
2. **One provider-timed function per real stage.** Wrap the existing training/evaluation command rather than rewriting it. The [timeout guide](https://modal.com/docs/guide/timeouts) caps each Function attempt at 24 hours; our 26-hour lease therefore needs separate calls or checkpointed resume, not one monolithic call. CPU-only orchestration can stay local. Independent evaluations may run concurrently only within an explicit aggregate GPU-hour budget.
3. **Checkpoint and resume instead of nursing a box.** The [official long-training example](https://modal.com/docs/examples/long-training) saves to a Volume, resumes from the latest checkpoint and launches with `modal run --detach`. The [Apps guide](https://modal.com/docs/guide/apps) says ordinary ephemeral apps stop on client exit/disconnect; `.spawn()` alone is not a substitute for detached launch. Preserve optimizer/RNG/trainer state when exact training resume is required, not just final LoRA weights.
4. **Use provider budgets in addition to timeouts.** [Workspace budgets](https://modal.com/docs/guide/budgets) cap gross monthly usage; spend limits cap net charges after credits. Environment-specific budgets require Team/Enterprise. Timeouts are per attempt, and retries start a new timer; one hour plus three retries can execute for at least four hours, with startup/warm/storage costs beyond that simple bound.

Limits that matter: [GPU Functions can be preempted](https://modal.com/docs/guide/preemption), with the same input restarted; non-preemptible mode is not supported for GPU Functions. Our launch and stage outputs therefore need resumable/idempotent behavior. The [pricing FAQ](https://modal.com/pricing) says container loading and the default 60-second idle retention are billable, despite the marketing headline about no idle charges. Short independent jobs can save operator effort, but GPU count, retries and warm retention still need bounds.

The highest-value source for our case is Modal's official resumable-training example, not Hermes' broader inference-serving examples. Hermes supplies useful discovery and wrapper examples. Vastkit supplies a good whole-session cost and explicit-output contract; our existing hash receipts are stronger than its file-existence checks. Keep those parts rather than replacing everything with a new framework.

Recommendation: a future approved pilot should reuse one real training/evaluation stage with the pinned image and model, on Modal's RTX PRO 6000, and measure elapsed cost, checkpoint resume, output hashes and operator steps. Do not migrate the whole pipeline or infer lower cost from serverless alone. No pilot is authorized by this review.

## Follow-up: concrete improvements; Vast, Runpod or Lambda?

Checked 2026-10-25, PI/OpenAI (Sol). No rental, paid API call or controller mutation. Recommendation for the current single-96-GB workload: **Vast first; Runpod Secure Cloud as the alternative to investigate; Lambda is not the first match for this hardware requirement.** This is a price/features comparison, not a provider reliability benchmark.

### Provider evidence

- **Vast:** latest sibling read-only offer snapshot still quotes two filtered RTX PRO 6000 S machines at $1.84444/hour including the requested 300 GB disk. Source: `/workspace/2026/constitutional_grafting/slop/eval/run12/preparation/quote.log`. This is a snapshot, not a reservation or proof of current stock. The owning session reports HOLD and no new leases created.
- **Runpod Secure Cloud:** [current pricing](https://www.runpod.io/pricing) lists an RTX Pro 6000 with 96 GB VRAM, 188 GB RAM and 16 vCPUs at $2.49/hour, with storage charged separately. This is about 35% above the recorded Vast hourly price before storage; it is not the same CPU allocation. At 26 hours that rate difference alone is about $17. The [GPU product page](https://www.runpod.io/gpu-models/rtx-pro-6000) also advertises a Community Cloud rate of $1.69/hour; verify a deployable offer and required host quality before treating that as a comparable quote.
- **Runpod's concrete advantage:** [network volumes](https://docs.runpod.io/storage/network-volumes) survive Pod deletion and are accessible through an [S3-compatible API](https://docs.runpod.io/storage/s3-api) without launching a Pod. Standard storage is $0.07/GB/month for the first 1 TB, so 300 GB is $21/month if retained for a full month. For Pods this feature is **Secure Cloud only**; the cheaper Community quote does not buy it. Volume location constrains GPU options, and S3 access is available only in listed datacentres. This is a real implementation of retrieval after GPU release, not just a proposed idea. Normal Pod volume disks still disappear on termination and bill while stopped. Runpod Pods still need lifecycle supervision; their documented delayed-stop example is a background `sleep` command, not evidence of an independent provider-enforced budget.
- **Lambda:** the [current public pricing table](https://lambda.ai/pricing) lists B200/H100/A100/V100 instances, not RTX PRO 6000. The table does not supply a comparable 96-GB RTX quote. [Regional filesystems](https://docs.lambda.ai/public-cloud/filesystems/) persist separately and offer an S3 adapter in selected regions. However, their [instance lifecycle docs](https://docs.lambda.ai/public-cloud/on-demand/creating-managing-instances/) say instances can only be launched, restarted or terminated, with no suspend option. They explicitly warn that OS shutdown leaves billing active. This is not a simpler stop-and-keep-disk replacement for our current recovery policy.

The proposed Runpod benefit is durable storage and post-compute retrieval. It does not establish faster training, more reliable hosts or lower total job cost. Repeated short jobs may save setup/copy time; a sustained training lease gets less benefit from eliminating brief retrieval time.

### Improvements to make before another unattended Vast lease

1. Keep the heartbeat alive through copying, using the retrieval deadline rather than the runner deadline for SSH timeouts. Hold one per-instance controller lock through attach, monitoring and teardown. The existing retrieval lock is not an ownership lock.
2. Complete and test the two independent stop conditions: lost heartbeat and absolute deadline. The current watchdog rewrite validates API responses and retries failures; the new `scripts/eval/48_vast_deadline.py` creates an exact-ID persistent systemd timer. Both are **untested WIP**, not proven safeguards. Exercise rejected/timeout stop responses, a killed controller, a controller still heartbeating past its job limit, and slow retrieval. Record the actual installed timer/deadline and exact instance ID before running unattended. API/host failure remains possible.
3. Admit a complete scientific comparison as one budget unit: treatment, required control, evaluations and retrieval. Do not spend on a dependent stage unless its necessary comparison also fits. This changes scheduling, not the frozen training recipe.
4. If repeated downloads or retrieval become material costs, investigate separate persistent storage. Runpod Secure plus a network volume is the clearest verified option among these providers. On Vast, first assess local-volume host constraints or external object storage rather than assuming a stopped container is accessible without a GPU.

### Current implementation state, not a completion claim

The sole executor reported at 08:47 UTC: no pair-specific controller exists; `38_run10_chat_rental.py` still lacks the heartbeat-ordering and controller-owner fixes. `box_watchdog.sh` and `48_vast_deadline.py` are local uncommitted WIP; neither has been tested or activated, and no guard unit is installed. I read both changed/new source files but did not validate cloud behavior. The historical seven retrieval tests do not validate these new safeguards. Do not launch work from this report or overwrite the other session's files. This is a time-specific snapshot; later implementation and checks require new evidence.

## Skill reorganization: gradual disclosure

At the user's request, committed as `36c60f4` in `/home/code/.agents`, not this research repository:

- `/home/code/.agents/skills/rent-gpu/SKILL.md`: 37-line provider selector and shared rental safeguards. Metadata places Vast, Runpod, Lambda, Modal and Tinker within Hermes' first 57 description characters.
- `/home/code/.agents/skills/rent-gpu/references/vast.md`: 84-line Vast procedure, read only when using Vast. Its official Vast and Vastkit links remain. Modal implementation routes to the existing `modal` skill.
- Removed the old `skills/vastai/SKILL.md` entrypoint. Existing uncommitted human edits were carried to the new reference and remain uncommitted; no unrelated `.agents` changes were included.

Mechanical checks passed: frontmatter matches the directory, the sole bundled reference exists and is explicitly routed, no old local skill references were found, no new trailing whitespace, and concurrent edits were preserved. New source files were committed separately from existing unrelated changes.

A fresh model received an overnight custom-adapter/activation job with a dead controller and saved instance ID, with no skill name/path supplied. Actual tool trace: listed `.agents` and its skill directory, read `rent-gpu/SKILL.md`, read only its `references/vast.md`, wrote the requested report. It refused to rent a replacement before reconciling the saved instance, selected Vast for custom adapter/activation access, and rejected auth GET alone as proof of stop/deadline enforcement. This verifies filesystem discovery and selective reference use; it is not a test of a live Hermes index or refresh of an already-open session's cached skill list. No cloud operations occurred.

Output: `/workspace/2026/constitutional_grafting/slop/audits/20261025_vast_skill_evidence/rent_gpu_discovery_check.md`.
