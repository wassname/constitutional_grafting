# Public-source research: Vast.ai / GPU-rental skills, and what Hermes actually supports

**Scope:** public GitHub only, read-only. No private data, no credentials read, nothing fetched was executed,
no rentals created, no repo edits. Cwd `/workspace/2026/constitutional_grafting` left untouched (dirty worktree
respected — zero git mutations).

**Date:** 2026-10-25 · **Pinned Hermes commit:** `4ea8d23cc9f527332ccb1d55359b27741b6ea51b` (main, committer date 2026-10-25T02:56:21Z)

---

## Parent checks and limits (PI/OpenAI, Sol)

I fetched/read the entire pinned official Vast skill, the entire Hermes Modal skill, Hermes Modal creation/cleanup code, and the backend registry lines through `gh`. The scout's discovery work below is useful, but these corrections govern the recommendations:

- Hermes has no dedicated Vast/RunPod backend or skill in the inspected tree. Its generic SSH backend can still target a box provisioned elsewhere. No dedicated integration does not mean no possible use.
- Modal differs from continuously rented instances: the inspected Hermes sandbox sets a default `timeout=3600`, and its Modal ML skill describes scale-to-zero functions. The original scout's claim that all these providers require explicit destroy to end GPU billing was wrong.
- Hermes Modal cleanup catches snapshot errors and proceeds to termination; it also suppresses termination exceptions. This is not a drop-in model for preserving irreplaceable training artifacts or proving teardown. Borrow the bounded lifetime, not those failure policies.
- Vendor authorship is a useful provenance signal, not validation. The official Vast skill's rule 7 prohibits direct API access, yet our existing REST controller worked. Its rule 4 calls `offline` unrecoverable and destroys immediately; current official instance docs describe offline as a host disconnection/power/internet problem and do not establish permanent failure. Do not import unconditional destruction before artifact recovery. Its install section also contradicts rule 7's no-install policy.
- Claims below about `execute`, shared/network-volume availability, exact CLI flags and absolute provider coverage are source claims, not live-tested facts. The June plugin may lag the October service. Verify current CLI/API documentation before implementation. Do not import floating image tags or pricing examples into our pinned training setup.
- The scout's advice to inject secrets via command-line `--env` can expose them in process listings/logs. Keep our whitelist upload and avoid account/API secrets on the rented host unless necessary; use a reviewed scoped mechanism if a remote download requires one.

Official instance docs checked by parent: https://docs.vast.ai/documentation/instances/manage-instances and https://docs.vast.ai/documentation/instances/docker-environment (2026-10-25).

The remainder is the scout's source inventory, with the material errors below corrected. It is not an implementation approval.

## Summary

1. **No dedicated Vast integration was found in the inspected Hermes tree.** No `vast.py` environment or Vast-specific skill was found; Vast appears as an alternative in a GPU-cloud skill and its generated documentation. Generic SSH remains available.
2. **The three layers are genuinely separate in Hermes**, and only the first two are implemented:
   inference API providers (`website/docs/integrations/providers.md`) · sandbox/terminal execution
   (`tools/environments/`) · rented-GPU provisioning for training (optional `mlops` skills only — Lambda Labs, Modal).
3. **A Vast skill has no shortcut path into `terminal.backend`.** The built-in set is fixed and reserved; a Vast
   backend must be a plugin (`TerminalEnvironmentProvider`) or stay outside Hermes as an external CLI skill.
4. **Best available Vast source is official and MIT-licensed:** `vast-ai/vast-claude-plugin` → `skills/vastai/SKILL.md`
   (606 lines, agent-hardened, 12 numbered rules, an error table). It contradicts several community skills on
   facts that matter (network volumes, `-y`, `execute`), so cite it over the blog-skill clones.
5. Useful design references are Hermes' Modal environment and the `lambda-labs` skill: bounded timeouts, explicit cleanup and persistence. Their billing/lifetime models differ. Hermes' Modal sandbox has a default one-hour timeout; do not generalize Vast's continuously rented-instance billing to Modal functions.

---

## 1. What Hermes actually supports (evidence, not vibes)

### 1a. Terminal / sandbox execution backends — closed set of 7

`tools/environments/` contains exactly these providers:
`base.py, local.py, docker.py, ssh.py, modal.py, managed_modal.py, daytona.py, vercel_sandbox.py`
(+ helpers `remote_common.py, file_sync.py, streams.py, docker_egress.py, …`).

Three independent places state the same closed list:

`tools/terminal_tool_config.py` (lines 120–121):
```python
_CONTAINER_BACKENDS = frozenset({"docker", "modal", "daytona", "vercel_sandbox"})
_BUILTIN_BACKENDS = _CONTAINER_BACKENDS | {"local", "ssh", "managed_modal"}
```

`tools/terminal_tool_backends.py` (line 52):
```python
_BUILTIN_BACKENDS = "local, docker, modal, daytona, vercel_sandbox, ssh"
```

`tools/environments/__init__.py` (lines 1–3):
> "one BaseEnvironment ABC for running shell commands in a specific context (local, Docker, SSH, Modal
> direct/Nous-managed, Daytona, Vercel Sandbox; plugin backends register through `agent.terminal_env_registry`)"

And the reserved-name rule — this is the hard blocker for a name-level Vast integration
(`website/docs/developer-guide/terminal-environment-plugin.md`):
> "**Reserved names.** Registrations that collide with a built-in backend name (`local`, `docker`, `modal`,
> `managed_modal`, `daytona`, `vercel_sandbox`, `ssh`) are rejected. Plugins extend the backend set; they never
> shadow in-tree backends."

**No Vast, no RunPod, no Paperspace, no Lambda-as-backend.** (Lambda exists only as a prose skill.)
Open feature requests confirm the gap and the pathway: `#79869 "[Feature]: Kubernetes session-pod terminal backend"`,
`#139743 "[Feature]: WSL Containers (wslc) as a native terminal backend on Windows"` — new backends arrive via plugin,
and third-party remote integrations ship through `plugin-catalog/*.yaml` with a pinned `sha` + `tier: community`
(e.g. `plugin-catalog/hermes-ssh.yaml` → `sha: f3f9161…`).

### 1b. Inference API providers — a different axis entirely

`website/docs/integrations/providers.md` line 11 opens `## Inference Providers`, and **Modal / Daytona / Vast /
RunPod do not appear anywhere in that 1,739-line file.** This is the cleanest evidence that Hermes treats
"where commands run" and "where tokens come from" as unrelated registries.

The one place the two blur is a single table cell (line 25):
> "| **NovitaAI** | `NOVITA_API_KEY` in `~/.hermes/.env` (provider: `novita`, 200+ models, Model API,
> Agent Sandbox, GPU Cloud) |"

i.e. a vendor selling all three things still registers in Hermes only as an inference provider.

### 1c. Rented-GPU training — prose skills, not integrations

Only two Hermes skills cover renting a real GPU box, both `optional-skills/mlops/`:
`lambda-labs` (on-demand SSH instances, 1-Click Slurm clusters) and `modal` (serverless). Neither is wired into
`terminal.backend`; both are documentation the model reads and then drives an external CLI/SDK with.

The scout found Vast only in an alternative-provider recommendation and generated mirrors, not a dedicated skill/backend, in the inspected current tree. The recommendation is in the Lambda skill
(`optional-skills/mlops/lambda-labs/SKILL.md`):
> "**Use alternatives instead:** … **Vast.ai**: For GPU marketplace with lowest prices"

Siblings, for contrast — same skill, same block:
> "**RunPod**: For cheaper spot instances and serverless endpoints"

(`optional-skills/mlops/modal/SKILL.md` says "**RunPod**: For longer-running pods with persistent state".)

Code-search confirmation (repo-scoped): `gh search code "vast.ai" --repo NousResearch/hermes-agent` returns only
`optional-skills/mlops/lambda-labs/SKILL.md` and its two generated doc mirrors.

---

## 2. Taxonomy table (the distinction the brief asked to preserve)

| Layer | What it decides | Hermes artefact | Vast present? |
|---|---|---|---|
| **Inference API provider** | Which model answers; billed per token | `website/docs/integrations/providers.md`, `hermes model` | No |
| **Sandbox / terminal backend** | Where `terminal`, `execute_code`, file tools run; session-scoped lifetime | `tools/environments/*`, `terminal.backend` ∈ {local, docker, modal, managed_modal, daytona, vercel_sandbox, ssh} | **No** |
| **Rented GPU provisioning (training)** | Who owns the box; billed per GPU-hour until destroyed | optional `mlops` skills driving an external CLI/SDK (Lambda, Modal) | **No** — Vast is a recommended 3rd party only |

Consequence for the deliverable: a "Vast skill" is a **layer-3 prose skill** (like `lambda-labs`), *not* a
`BaseEnvironment` subclass. If someone later wants Vast as a terminal backend, that is a plugin repo
(`is_remote=True`, `is_container=True`, `strip_env_keys=frozenset({"VAST_API_KEY"})`, cheap `is_available()`),
never an in-tree edit.

---

## 3. Sources worth using (ranked by authority, not stars)

Star counts here are 0–225; **stars are useless as a ranking signal in this niche** — the official, best-maintained
source has 3 stars. I ranked on (a) who wrote it, (b) agent-specific hardening, (c) recency of push, (d) whether
claims are testable against CLI `--help`.

### S1 — `vast-ai/vast-claude-plugin` → `skills/vastai/SKILL.md` ★ primary
- URL: https://github.com/vast-ai/vast-claude-plugin/blob/c90a6cceb7d5fd0e206c0dc705d7750a198d7768/skills/vastai/SKILL.md
- Raw: `https://raw.githubusercontent.com/vast-ai/vast-claude-plugin/c90a6cceb7d5fd0e206c0dc705d7750a198d7768/skills/vastai/SKILL.md`
- Pinned SHA `c90a6cc…`, pushed 2026-06-16, MIT, 3 human contributors, 606 lines, `metadata.author: vast-ai`.
- **Why authoritative:** vendor-written, explicitly written *for* agents ("Critical rules for agents"), and it
  documents failure modes with verification dates. Companion official plugins: `vast-ai/vast-codex-plugin`,
  `vast-ai/vast-cursor-plugin` (same two skills, different harness adapters).
- Highest-value quotes:
  > "The destroy command syntax is `vastai destroy instance <id> -y` — the `-y` flag is part of the command, not an
  > option. Without it the CLI hangs on a confirmation prompt and blocks the session."

  > "Without `--disk` you get image-dependent defaults and surprise storage charges. Without `--ssh --direct` together
  > you fall back to the slower proxy connection … Without `--cancel-unavail`, an unavailable machine quietly produces
  > a *stopped* instance that accrues disk charges while you poll forever for a `running` state it will never reach."

  > "**Vast.ai does not offer network/shared volumes.** Only local (per-instance) volumes."

  > "**There is NO working way to inspect or run commands on a STOPPED instance.** Verified 2026-06-02:
  > `vastai execute` crashes … Don't suggest `execute` — it appears in `vastai --help` but doesn't work."

  > "**Charges:** Storage charges begin at creation (or earlier if `--cancel-unavail` is omitted on an unavailable
  > machine). GPU charges begin when status reaches `running`."

  > "**Poll loop warning:** Terminal `actual_status` values (`exited`, `unknown`, `offline`) never recover. Always
  > add a timeout — your script otherwise loops forever while disk charges accrue."

  > "Logs are stored in S3 and may take 30–60 s to appear after start."

  > "the CLI silently accepts a path string and registers the literal "/Users/…/id_ed25519.pub" text, producing a
  > key that no client matches"
- Also gives a ready poll-loop with deadline that destroys on terminal states — the single most copy-worthy
  primitive for a Vast skill.

### S2 — `Yusuke710/vastai-skill` → `skills/vastai-gpu/SKILL.md` ★ best terse lifecycle
- URL: https://github.com/Yusuke710/vastai-skill/blob/32a7b32b0f95f62adbdad4de2a12ab1fee17c914/skills/vastai-gpu/SKILL.md
- Pinned `32a7b32…`, pushed 2026-07-12, 78 lines, 1 contributor, 17 commits.
- **Why useful:** shortest correct end-to-end lifecycle; unusually good judgement calls for an agent, and it
  ships the watchdog as code (`vastai-connect`, `src/vastai_connect/cli.py`).
  > "Money is spent per hour from the moment an instance is created until it is **destroyed**. Never leave one behind."

  > "**Destroy, never `stop`** — stopped instances still bill storage and may be unable to restart."

  > "On timeout (5 min default) or any stall later (crawling downloads, broken SSH auth): destroy and rent a
  > different offer — re-renting beats debugging."

  > "`--disk` cannot be resized later; size it for datasets + checkpoints."

  > "**Only destroy instance ids you created in this session** (the `new_contract` values you received). Other
  > instances — even ones with a familiar label or the same image — may belong to another job or agent running in
  > parallel."

  > "default to `vastai/pytorch:latest` — its CUDA base layers are cached on most vast.ai hosts (boot-to-SSH ≈ 2–3 min)"

### S3 — `LiorZ/vastai-claude-skill` ★ best breadth / CLI surface map
- URL: https://github.com/LiorZ/vastai-claude-skill/blob/32e158c59679f72c73fbd179a943de64ae13c90c/skills/run-job/SKILL.md
  (whole-plugin reference: `.../32e158c…/skills/vastai/SKILL.md`, 403 lines; launch: `.../skills/launch-instance/SKILL.md`)
- Pinned `32e158c…`, pushed 2026-02-07, 4 commits, 1 contributor, 8 skills + 1 reference skill.
- **Why useful despite staleness:** the only source that documents `--env` port remapping, `vastai copy
  local:/C.<id>:/V.<id>:` forms, volumes, templates and serverless in one place; its `run-job` skill is a
  complete 11-phase agent loop with confirmation gates.
  > "`vastai execute` is limited (ls/rm/du only) — use SSH for real work"

  > "Use `--disk` generously — disk is cheap, running out mid-job is expensive"

  > "For long training: on-demand > interruptible (avoid preemption)"

  > "Keep the container running — do NOT put the main job in onstart-cmd (use SSH for that)"

  > "**Always destroy** the instance when done or on failure — never leave it running"
- **Stale/contradicted on:** `vastai execute` working, network volumes existing, `destroy` without `-y`.
  Use it for surface area, S1 for truth.

### S4 — `RazinAleksandr/vastkit` ★ best "budget as a first-class object"
- URL: https://github.com/RazinAleksandr/vastkit/blob/8b40befb8a10a6fc5b6befcbac2b83bf44079fa2/skills/vastkit/SKILL.md
- Pinned `8b40bef…`, pushed 2026-08-03, MIT, 203-line skill + Python CLI (`vastkit/lifecycle.py`) + 6 test files + CI.
- **Why useful:** only candidate that makes **effective session cost** (not $/hr) the ranking function, and the
  only one with a real test suite — a structural model worth copying even if you don't use the CLI.
  > "Prefer the lowest effective session cost that meets the workload, not merely the lowest hourly price."

  > "Treat `est_session_cost` as an estimate, not a guaranteed bill."

  > "Stopping releases the GPU but storage remains billed. Destroying is irreversible and is the action that ends
  > instance billing."

  > "Do not destroy the instance merely because a transfer command returned zero when the expected artifacts are
  > missing."

  > "Never finish a normal run while an active billed instance is unaccounted for."

  > "Never put an API key in a command, pass `--api-key`, print it, commit it, or ask the user to paste it into chat."
- Its `search --hours 2 --download-gb 40 --max-bw 10` shape (bandwidth folded into cost) is the idea I'd steal.

### S5 — `NousResearch/hermes-agent` `optional-skills/mlops/lambda-labs` ★ the house style to imitate
- URL: https://github.com/NousResearch/hermes-agent/blob/4ea8d23cc9f527332ccb1d55359b27741b6ea51b/optional-skills/mlops/lambda-labs/SKILL.md
  (+ `references/advanced-usage.md`, `references/troubleshooting.md`, and the generated docs mirror
  `website/docs/user-guide/skills/optional/mlops/mlops-lambda-labs.md`)
- 549 lines + 530-line troubleshooting; `version: 1.0.0`, MIT, `author: Orchestra Research`.
  > "4. **Terminate idle**: No auto-stop, manually terminate"

  > "# Root volume (/home/ubuntu) is EPHEMERAL / # Data there is lost on termination"
  > "**ALWAYS use filesystem for persistent data**"

  > "**Connection refused** | Instance not ready | Wait 3-15 minutes for boot"

  > "Instance health check failure … Solutions: … Always checkpoint to filesystem"

### S6 — `NousResearch/hermes-agent` `tools/environments/modal.py` + `website/docs/developer-guide/terminal-environment-plugin.md` ★ the engineering contract
- URL: https://github.com/NousResearch/hermes-agent/blob/4ea8d23cc9f527332ccb1d55359b27741b6ea51b/tools/environments/modal.py
- URL: https://github.com/NousResearch/hermes-agent/blob/4ea8d23cc9f527332ccb1d55359b27741b6ea51b/website/docs/developer-guide/terminal-environment-plugin.md
- **Why useful:** shows what a *correct* remote-cloud environment looks like when the agent owns the lifetime.
  > `_snapshot_timeout = 60  # Modal cold starts can be slow`

  > "# ttl=None: the SDK default (30 days) would silently expire an idle / # persistent sandbox's snapshot;
  > Hermes owns its lifetime."

  > "def cleanup(self): / """Snapshot the filesystem (if persistent) then stop the sandbox."""  … terminate with timeout=15"

  > (plugin doc) "**Secrets belong in `strip_env_keys`.** Your vendor token must never be readable by a
  > model-authored shell command"

  > (plugin doc) "**`is_available()` / `probe()` must be cheap.** No network calls — they run during requirement
  > checks and UI paints."

  > (plugin doc) "`cleanup()` — release resources; called on session teardown / idle reaping"

Honourable mentions (read, not recommended as primary):
- `vast-ai/vast-cli` @ `42c3a47b44603775a5e31f54de0fce3994bd3f11` (225★, official CLI/SDK) — authoritative for
  flag existence; README is thin but `create instance … --disk 32 --ssh --direct` examples are correct.
- `skypilot-org/skypilot` @ `f73b735cb1c062f2d95531d9327803362a5ca084` — the only *production* Vast
  integration anywhere (`sky/provision/vast/{instance,config,utils}.py`, `sky/clouds/vast.py`,
  `sky/catalog/vast_catalog.py`). Read it if you need Vast's API semantics at the level of provisioning
  state machines. It is an orchestrator, not a skill — the wrong thing to copy verbatim into a SKILL.md.
- `hgarud/vastxm` @ `18dd91ddb9f469bdade0097135c656b9844f7c31` — 90-line README, one-command
  rent→ship→run→copy→destroy with `max_price` in `vastxm.toml`; nice UX, unmaintained-looking, no tests.
- `CryDevOk/vastai-mcp` (13★, mcp server, pushed 2025-07) — 27 commits but a year stale; an MCP wrapper is a
  different product shape than a skill. `yowmamasita/vastai-mcp` created and last pushed the same day.

---

## 4. Practical lessons for a Vast skill

Every item below is grounded in a quote above; the Hermes-side items are grounded in actual code.

### Budget (the dominant failure mode)
1. **Model cost as "until destroy", not "until job exit".** S1: "Storage charges begin at creation … GPU charges
   begin when status reaches `running`." S2: "Money is spent per hour from the moment an instance is created until
   it is **destroyed**." A Vast skill must state the billing clock in the first paragraph, not a footnote.
2. **Refuse to rent without a price ceiling.** S4: "Always include `--max-price` on agent-selected rentals" and
   "Use `--yes` only after approval, and only for the approved limits." Treat `est_session_cost` as an estimate.
3. **Rank on effective session cost, not `$/hr`.** S4's `--hours/--download-gb/--max-bw` inputs are the right
   contract; a \$0.30/hr host with 5 Mb/s down can lose to \$0.45/hr with 500 Mb/s on a 40 GB download.
4. **Quote a projection before spending.** `vast-ai/vast-claude-plugin` `commands/cost.md` sums `dph_total` across
   `actual_status == "running"` rows and projects 24 h — cheap, and it doubles as a pre-flight check.
5. **Never `--force`, never `destroy --all`.** S1 rule 3 on `--force`; S4: "Never use `destroy --all` unless the
   user explicitly requested every matching instance be destroyed."

### Timeouts
6. **Every poll loop needs a deadline AND terminal-state handling.** S1: "Terminal `actual_status` values
   (`exited`, `unknown`, `offline`) never recover. Always add a timeout." Copy their `deadline=$((SECONDS+600))`
   loop verbatim; S3's 30×10 s wait is the same idea without the fatal-state branch (weaker).
7. **Read all four status fields, not just `actual_status`.** S1: `intended_status`, `actual_status`, `cur_state`,
   `next_state` — "`actual=created, cur_state=scheduling` → keep polling", "`next_state=stopped` while bringing up
   → Treat as fatal".
8. **Budget the cold-start separately from the command timeout.** Precedent in Hermes itself:
   `_snapshot_timeout = 60  # Modal cold starts can be slow`; and `base.py`: "Pulling a large artifact over a slow
   exec channel can outlast the per-command terminal timeout" → `_FETCH_TIMEOUT_SECONDS = 300`. A Vast skill should
   have three distinct numbers: boot timeout (~300–600 s), per-command timeout, transfer timeout.
9. **Bound the wait for SSH separately from "running".** S3: "Wait an additional 15-20 seconds after "running"
   status for SSH to become available". S2's `vastai-connect` blocks *until SSH works*, which is the better
   contract: readiness = "I can run a command", not "the API says running".
10. **Set a stall policy, not just a timeout.** S2 is the sharpest: "On timeout (5 min default) or any stall later
    … destroy and rent a different offer — re-renting beats debugging." Cheap consumer hosts are a lottery.

### Teardown
11. **Destroy after verified retrieval; stop can preserve a failed retrieval for recovery.** S2: "stopped instances still bill storage
    and may be unable to restart"; S4: "Stopping releases the GPU but storage remains billed. Destroying is
    irreversible and is the action that ends instance billing."
12. **`-y` is mandatory or the agent hangs.** S1 rule 1: without `-y` "the CLI hangs on a confirmation prompt and
    blocks the session." Any Vast skill that writes `vastai destroy instance <id>` bare will deadlock a non-TTY
    agent. (S3 and S2 both write it bare — direct contradiction; S1 wins.)
13. **Guard teardown by provenance.** S2: "Only destroy instance ids you created in this session". S4 extends it
    to recovery: after any interruption, "run `ls --json` immediately and locate the distinctive label."
14. **Teardown must survive failure.** S3 Phase 10 / Error Recovery: "**Any unrecoverable error**: ALWAYS destroy
    the instance to stop billing". S4: "If cleanup is not authorized or destruction fails, do not hide the state.
    Report the live instance ID, price, and dashboard/CLI cleanup action."
15. **Verify the destroy, don't trust the exit code.** S3: `vastai show instances --raw | jq '.[] | select(.id == <ID>)'`;
    S2: "`vastai show instances --raw` # verify it's gone; `[]` means nothing is billing." S4: "Vastkit destroys
    boot attempts that time out, but verify account state after an interrupted process or a failed destroy request."
16. **Own the lifetime if Hermes ever drives it.** `modal.py`'s `cleanup()` = snapshot → terminate(timeout=15),
    with the comment that the SDK's 30-day TTL "would silently expire an idle persistent sandbox's snapshot;
    Hermes owns its lifetime." Same discipline applies to Vast volumes/instances.

### Checks / preflight
17. **SSH key before instance — and the argument is key *contents*.** S1 rule 3: "the CLI silently accepts a path
    string and registers the literal "/Users/…/id_ed25519.pub" text, producing a key that no client matches."
    "Launching without a registered key produces an unreachable host." This is a silent, expensive failure.
18. **`--cancel-unavail` always.** S1: otherwise "an unavailable machine quietly produces a *stopped* instance that
    accrues disk charges while you poll forever for a `running` state it will never reach."
19. **`--disk` is immutable and forgotten.** S2: "`--disk` cannot be resized later"; S1: "Without `--disk` you get
    image-dependent defaults and surprise storage charges"; S3: "disk is cheap, running out mid-job is expensive."
20. **Verify the GPU is actually usable before a long run.** S2: "Sanity-check that torch actually sees the GPU
    before paying for a long run"; the Lambda skill's `nvidia-smi` / `torch.cuda.is_available()` / `nvcc --version`
    trio is the house pattern. S1 adds the `compute_cap` trap: it's "an encoded integer, not the decimal version",
    and guessing produces runtime `no kernel image is available`.
21. **Read logs before blind retries.** S1 rule 11: "When SSH fails … pull `vastai logs <id>` FIRST — before any
    other recovery action … Diagnostic discipline: `logs` then act, never act then guess." Note the log lag:
    "Logs are stored in S3 and may take 30–60 s to appear after start."
22. **Empty search results are an answer.** S1 rule 6: "An empty `vastai search offers` result is the answer, not a
    problem to work around … Do not silently retry with broader filters more than once." Very relevant: agents love
    to auto-widen filters and rent something they shouldn't.
23. **Don't `-n` your safety filters away.** S1: hidden defaults `verified=true external=false rentable=true`;
    "Do not pass `-n` / `--no-default` to drop all three at once."

### Persisted outputs
24. **Pull before destroy, and verify the pull.** S4: "Pull results before any destructive cleanup … Do not destroy
    the instance merely because a transfer command returned zero when the expected artifacts are missing."
    S2: "**Before destroying**, pull back artifacts worth keeping (weights, logs, results) — they exist only on
    the instance."
25. **Nothing on the box survives; plan for that.** Lambda skill: root volume is "EPHEMERAL", "Data there is lost on
    termination", "**ALWAYS use filesystem for persistent data** … `rsync -av /home/ubuntu/outputs/ /lambda/nfs/…`".
    For Vast the equivalents are `vastai copy <id>:/path local:./` and `vastai cloud copy` to S3 — and S1 insists
    Vast has **only per-instance local volumes**, so cross-run persistence must be object storage or a fresh copy.
26. **Make outputs a declared input, not a hope.** S3's Phase 1 asks for "Results to download" up front and Phase 9
    lists "Common result locations to check"; S2 says "if unsure what to keep, check with the user".
    A Vast skill should require the caller to name the artifacts before renting.
27. **Detach long work, capture its exit code, then reconcile.** S2: "Detach long jobs so they survive SSH drops, and
    capture the exit code." S4: "`logs -f` returns the detached job's exit code. Treat a nonzero code as a workload
    failure and inspect the log before retrying."
28. **Don't poll a detached job by re-launching it.** S4: "Monitor without starting duplicate work" — a real
    agent failure mode (`jobs --json` then `logs --detach`).

### Security
29. **Never let a model-authored shell command see the vendor token.** Hermes' contract: `strip_env_keys` →
    "Your vendor token must never be readable by a model-authored shell command". S4 generalises: "Never put an API
    key in a command, pass `--api-key`, print it, commit it, or ask the user to paste it into chat." Note the
    precedence trap S1 documents — `$VAST_API_KEY` silently shadows `vastai set api-key`.
30. **Exclude secrets from uploads.** S4: "Do not upload `.env` files or credential directories. Vastkit excludes
    common environment files by default"; pass remote secrets by reference (`--env HF_TOKEN="$HF_TOKEN"`).
31. **Host keys / `StrictHostKeyChecking`.** S3 uses `-o StrictHostKeyChecking=no` on every ssh/scp — that is
    deliberate for ephemeral `ssh5.vast.ai:<random-port>` hosts, but it belongs in a skill with a stated reason,
    not silently. Hermes' own SSH backend uses the stricter middle ground:
    `-o "StrictHostKeyChecking=accept-new" -o "ConnectTimeout=10"` plus `ControlMaster=auto`/`ControlPersist=300`
    (`tools/environments/ssh.py`). Copy Hermes, not the blog skills.
32. **Treat `create team` as destructive.** S1 rule 12: it "rebinds the calling API key's account context … The CLI
    shows no warning and has no `-y`-style guard." A Vast skill should hard-refuse it.
33. **2FA code handling.** S1: "Tell the user to prefix the command with `!` … so the 6-digit code does not enter
    conversation history." Good hygiene rule for any credential prompt.

---

## 5. Contradictions between sources (do not average these — pick S1)

| Claim | S1 (official) | Community skills | Ruling |
|---|---|---|---|
| `destroy` needs `-y` | mandatory, else hangs | S2/S3 omit it | **S1** — a hang is worse than an error |
| `vastai execute <id>` works | "`execute` … don't work" (verified 2026-06-02) | S3: "includes ls, rm, du only" | **S1** — use SSH |
| Network/shared volumes | "Vast.ai does not offer network/shared volumes" | S3 documents `create network-volume`, `search network-volumes` | **S1** — S3 is plumbing for "an unshipped product" |
| `stop` semantics | "Stop (preserves disk, no GPU charges)", `start` resumes | S2: "never `stop` … may be unable to restart" | **Both, differently** — `stop` still bills disk; S1 is about cost, S2 about reliability. Say both. |
| Logs | "Not real-time streaming … fetches a snapshot via S3 URL with polling" (S3) | "may take 30–60 s to appear" (S1) | compatible; state the lag + non-realtime nature |
| CLI install | `pip install vastai` (S1) | `curl -fsSL https://vast.ai/install.sh \| bash` (vast-cli README) | either; both from `vast-ai` |

Contradictions are themselves a finding: **three of the four Vast skills written for agents contain at least one
instruction that would hang, waste money, or fail at runtime.** A new Vast skill should carry a
"verified against `vastai <cmd> --help` on <date>" line per command group, the way S1 does with an explicit
"Verified 2026-06-02" stamp.

---

## 6. Limits of this research (read before trusting the recommendations)

- **Nothing was executed.** No rental, no `vastai` invocation, no SSH. Every CLI claim is a *documented* claim,
  verified only against cross-source agreement — not against live Vast API behaviour. Flags drift; S1 itself
  hedges with "read the current cap from `--help`".
- **Stars are actively misleading here**: official 3★ vs stale community 4★. I ranked on authorship, agent-specific
  hardening, and push recency. Any future automated ranking must not use stars as a proxy for correctness.
- **Maintenance signal is weak across the board** — every candidate has 1–3 human contributors, 4–17 commits, and
  no release process. `vastkit` is the only one with tests + CI. There is no "maintained" Vast skill; the closest
  is the vendor's own, last pushed 2026-06-16 (~4 months stale at time of writing).
- **Pricing/GPU tables in the Lambda and Modal skills are unsafe to copy.** The Lambda skill's B200/H100 $/hr table
  is vendor pricing from an unknown date; Vast marketplace prices are per-host and volatile. Do not import numbers.
- **Repo-scoped `gh search code` only surfaces indexed/default-branch content** and missed nothing here (tree grep
  over all 22,246 paths is the stronger check), but it cannot see deleted files, so "Vast never existed in Hermes"
  is an inference from the *current* tree, not from history.
- **`gh search repos "vast.ai"` is useless** — full-text README matching returns `public-apis`, `langchain`, `julia`.
  The productive query was `--match name` on `vastai*`, which is why the good candidates (all named `vastai-*` or
  `vastkit`) were findable at all. Note the false-positive cluster: "VAST" is also an IAB ad-serving XML standard
  (`dailymotion/vast-client-js`, 385★) and a storage vendor (`vast-data/*`) — both irrelevant, both star-attractors.
- Did **not** review `vast-ai/docs` (@ `626149741ba46f195c775b2f4c89b7329de2d902`) or `vast-ai/base-image` in depth;
  `docs.vast.ai/llms.txt` is referenced by S1 as the LLM docs index and is probably the next stop for flag drift.

---

## 7. Queries run (for reproducibility)

```
gh api repos/NousResearch/hermes-agent --jq '{stargazers_count,pushed_at,...}'          # 256,888★, MIT, pushed 2026-10-25
gh api 'repos/NousResearch/hermes-agent/git/trees/main?recursive=1'                    # 22,246 paths -> /tmp/hermes_tree.txt
grep -E '^(optional-skills|skills)/' /tmp/hermes_tree.txt                              # 152 optional SKILL.md, 58 core SKILL.md
grep -iE 'vast|runpod|modal|daytona|gpu|ssh|sandbox|rental|rent' /tmp/hermes_tree.txt  # -> tools/environments/*, mlops/*
gh search code "vast.ai" --repo NousResearch/hermes-agent                              # 3 hits, all lambda-labs + doc mirrors
gh search repos "hermes" --match name,description,readme --sort stars --limit 50
gh search repos --owner NousResearch --sort stars --limit 50
gh search repos "vast.ai" --match name,description,readme --sort stars --limit 50      # NOISE — unusable
gh search repos "vastai" --match name --sort stars --limit 40                          # productive
gh search repos "vast-cli" --match name --sort stars --limit 20
gh search repos --owner vast-ai --sort stars --limit 30                                # -> official agent plugins
gh search issues "runpod" --repo NousResearch/hermes-agent --limit 10                  # 1 irrelevant
gh search issues "terminal backend" --repo NousResearch/hermes-agent --limit 15        # #79869 k8s, #139743 wslc
gh api repos/<r>/commits?per_page=100 --jq length                                      # commit depth per candidate
gh api 'repos/<r>/contributors?per_page=100' --jq '[.[]|select(.type=="User")]|length'  # human contributors
```

## 8. Sources read (files actually opened)

Hermes (`4ea8d23…`): `tools/environments/__init__.py`, `base.py` (832 L), `modal.py` (282 L),
`managed_modal.py` (205 L), `daytona.py` (207 L), `ssh.py` (302 L), `tools/terminal_tool_config.py`,
`tools/terminal_tool_backends.py`, `hermes_platform/host/gpu_adapters.py`,
`website/docs/developer-guide/terminal-environment-plugin.md` (252 L),
`website/docs/integrations/providers.md` (1,739 L, grep), `optional-skills/mlops/lambda-labs/SKILL.md` (549 L) +
`references/troubleshooting.md` (530 L), `optional-skills/mlops/modal/SKILL.md` (351 L) +
`references/advanced-usage.md` (503 L), `plugin-catalog/hermes-ssh.yaml`, `hermes_cli/cli_modal_mixin.py` (rejected —
it is TUI modals, not Modal.com).

Vast ecosystem: `vast-ai/vast-claude-plugin` (`skills/vastai/SKILL.md` 606 L, `README.md`, `commands/cost.md`),
`vast-ai/vast-cli` `README.md`, `LiorZ/vastai-claude-skill` (`skills/vastai/SKILL.md` 403 L,
`skills/launch-instance/SKILL.md` 97 L, `skills/run-job/SKILL.md` 361 L), `Yusuke710/vastai-skill`
(`skills/vastai-gpu/SKILL.md` 78 L), `RazinAleksandr/vastkit` (`skills/vastkit/SKILL.md` 203 L, tree incl. tests),
`hgarud/vastxm` `README.md`. SkyPilot: `sky/provision/vast/instance.py` (360 L), docs `installation.rst` (grep),
full tree `grep -i vast`.

---

## 9. Start here (if you are writing the Vast skill)

1. Read `vast-ai/vast-claude-plugin@c90a6cc:skills/vastai/SKILL.md` rules 1–12 — they are the error taxonomy.
2. Reuse the concept of bounded readiness polling, but do not copy unconditional destruction on offline/unknown state when outputs may need recovery. Check current provider state semantics.
3. Copy the **structure** (not the numbers) of `optional-skills/mlops/lambda-labs/SKILL.md`: when-to-use →
   alternatives → quick start → verify → cost optimisation → common issues → references/.
4. Copy the **budget contract** from `vastkit`: max price, hour estimate, download volume, `est_session_cost`,
   explicit approval gate, provenance-tracked destroy.
5. Inspect `tools/environments/modal.py` for bounded operations and an explicit sandbox timeout. Its cleanup suppresses snapshot/termination failures, so retain our stronger verified-retrieval-before-destroy policy instead of copying that failure behavior.
6. Write the three timeout constants down explicitly (boot / command / transfer) and the stall policy
   ("destroy and re-rent, re-renting beats debugging").

---

*Signed: PI / DeepSeek — scout run, read-only public-source research, 2026-10-25.*

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Brief written to /workspace/2026/constitutional_grafting/slop/research/20261025_vast_hermes_github_sources.md: 6 ranked sources pinned to commit SHAs (vast-ai/vast-claude-plugin@c90a6cc, Yusuke710/vastai-skill@32a7b32, LiorZ/vastai-claude-skill@32e158c, RazinAleksandr/vastkit@8b40bef, hermes-agent@4ea8d23 lambda-labs+modal env, skypilot@f73b735), exact quotes, 33 practical lessons grouped by budget/timeouts/teardown/checks/persisted-outputs/security, a contradiction table, and an explicit limits section."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "gh api 'repos/NousResearch/hermes-agent/git/trees/main?recursive=1'",
      "result": "passed",
      "summary": "22,246 paths; located optional-skills/, skills/, tools/environments/, plugin-catalog/"
    },
    {
      "command": "gh search code \"vast.ai\" --repo NousResearch/hermes-agent",
      "result": "passed",
      "summary": "3 hits, all in optional-skills/mlops/lambda-labs/SKILL.md + generated doc mirrors; no Vast integration code"
    },
    {
      "command": "gh search repos \"vast-cli\" --match name / --owner vast-ai",
      "result": "passed",
      "summary": "Found official vast-ai/vast-claude-plugin, vast-codex-plugin, vast-cursor-plugin, vast-cli"
    },
    {
      "command": "gh api repos/<candidate>/commits?per_page=100 --jq length; gh api repos/<candidate>/contributors",
      "result": "passed",
      "summary": "Maintenance/ownership check for 8 candidates; official plugin has 3 human contributors, 15 commits"
    }
  ],
  "validationOutput": [
    "Built-in terminal backends confirmed three independent ways: tools/terminal_tool_config.py L120-121 (_BUILTIN_BACKENDS frozenset), tools/terminal_tool_backends.py L52 (_BUILTIN_BACKENDS string), tools/environments/__init__.py docstring. Set = {local, docker, modal, managed_modal, daytona, vercel_sandbox, ssh}. No vast.py / runpod.py in tools/environments/.",
    "Modal/Daytona/Vast/RunPod absent from website/docs/integrations/providers.md (1,739 lines, grep) -> inference providers are a separate registry from execution backends.",
    "Vast appears exactly once in 22,246 tracked files as a prose alternative in optional-skills/mlops/lambda-labs/SKILL.md."
  ],
  "residualRisks": [
    "Nothing was executed: no vastai invocation, no rental, no SSH. All CLI claims are documented claims cross-checked between sources, not live API behaviour; flags drift and S1 itself hedges with 'read the current cap from --help'.",
    "Maintenance signal is weak across every candidate (1-3 human contributors, 4-17 commits, no releases). Worst case: the vendor skill is already ~4 months stale (pushed 2026-06-16) and documents a 'verified 2026-06-02' behaviour that may have changed.",
    "'Vast never existed in Hermes' is inferred from the current tree, not from git history; deleted files would not appear.",
    "Pricing/GPU tables in the Lambda and Modal skills are vendor numbers of unknown date - explicitly flagged as unsafe to import into a new skill.",
    "vast-ai/docs (docs.vast.ai/llms.txt) and vast-ai/base-image were only tree-listed, not read; they are the likely next source for flag drift.",
    "gh search repos \"vast.ai\" is unusable (ad-tech VAST standard and vast-data storage vendor dominate); a future automated sweep must use --match name on vastai*/vastkit or it will recommend wrong repos."
  ],
  "noStagedFiles": true,
  "diffSummary": "No files in the repo were modified. One new research brief written outside the working tree at slop/research/20261025_vast_hermes_github_sources.md; dirty worktree left untouched, no git commands issued.",
  "reviewFindings": [
    "no blockers",
    "notable: three of four agent-facing Vast skills contain at least one instruction that would hang, waste money, or fail at runtime (bare 'destroy instance <id>' without -y; claiming network volumes exist; claiming 'vastai execute' works) - the brief records these as a contradiction table rather than averaging them",
    "notable: recommendation is deliberately star-independent - the official 3-star vendor skill outranks the 13-star MCP and the 225-star CLI README for this purpose"
  ],
  "manualNotes": "Task was public-source research only: no private project data touched, no credentials read, no fetched code executed, no rentals created, no edits to skills/code. The parent's mid-run steering (prioritise optional-skills/ and skills/ trees, keep GPU-provisioning vs inference vs terminal-backend distinct) was applied at the point received - both trees plus tools/environments/ were fully enumerated, and the three-layer taxonomy is section 2 of the brief. One correction worth flagging to the parent: the brief's premise that Hermes 'supports' various execution providers should read as a closed set of 7 built-in backends with Vast/RunPod absent entirely, reachable only as a plugin (TerminalEnvironmentProvider) or as an external prose skill like lambda-labs."
}
```
