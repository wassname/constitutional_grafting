
## 2026-10-08 -- the gitignore that ate my homework
`.gitignore` had `data/`, which silently matched `scripts/data/` and `slop/data/`. Every "committed" generator and spot check from last night was untracked; commits said "SFT pilot spot check" and contained nothing. Found it only because `git commit` said "nothing to commit". Lesson: after a commit that should include new files, look at `git show --stat HEAD`, not just the exit code. Fixed to `/data/`. -- Claude (Pi, Opus)

## 2026-10-08 ~01:45 -- the key had a ceiling I didn't check
OpenRouter returned 402 mid-run. The account has ~$152 credit, but the key itself has a weekly limit of $88 (`GET /api/v1/key` → `limit_remaining 0.007`), and I only ever checked `/credits`. Lesson for future agents: check both `/credits` and `/key` before a batch; the per-key cap is the binding one. I did not mint or look for another key: raising it needs wassname's YubiKey (agent-vault tier 2), and the cap is a deliberate limit on how much the key can spend if something goes wrong. -- Claude (Pi, Opus)

- 2026-10-10 (Claude, Opus 5.5): stale 0-byte .git/index.lock three times today (15:06, 17:50, 19:21 Perth), blocking commits. Likely cause (pane agent, inferred): zentui footer runs `git status` in the background with a 2 s timeout; if the session is killed hard the lock stays. Pane agent patched zentui locally with GIT_OPTIONAL_LOCKS=0 (git.ts); a package update would undo it. Upstream PR needs wassname.

- 2026-10-13 (PI/OpenAI): `self-verify` routes to `references/boundary-probing.md` and `references/consider-the-opposite.md`, but both reads return ENOENT. `git -C ~/.agents ls-files skills/self-verify` lists only SKILL.md; the bundled references were not installed. Used the entry's checks without claiming to have read those missing references. This needs a complete upstream import, not guessed replacement essays.

## 2026-10-23 PI/Claude: the judge that kept dying
tiny-character's 03_judge was killed by SIGTERM three times (after 71 s, 658 s, 42 s). strace shows `si_pid=0, si_uid=65534`: the sender is outside the container's namespaces (host side), not anything in here. The container itself shows no OOM kills (memory.events oom_kill 0), but it was at 35 GB with memory pressure while honesty_heads held 17 GB. Guess (unverified): a host-side memory killer. Workaround: the Jev cache keeps progress, so retry in a loop; `41_tc_judge.py` now checks judged.jsonl, not cost.json, before refusing to run. Worth asking wassname what runs on the host.

## 2026-10-24 PI/Claude: async subagents broken
Background (async) subagents fail: "/home/code/.pi/agent/install/releases/1.4.0/node_modules/@earendil-works/pi-coding-agent does not provide @earendil-works/chord, @earendil-works/chord/context". Foreground subagents work. Likely a Pi 1.4.0 install missing a dependency; wassname may need to reinstall or update Pi.

## 2026-10-24 PI/Claude: Pi restart killed the lease controller
A Pi session restart around 16:12 AWST killed the run-11 controller (a child of the Pi process). The box kept training, but its watchdog stops the instance after 1 h without a heartbeat, so the lease had ~45 min left. Fixed by an `attach` action in `scripts/eval/38_run10_chat_rental.py` and running the controller in a local tmux session (`run11_controller`) so a Pi restart no longer kills it. Long leases should always run the controller in tmux.
Update 2026-10-24 ~19:30: fixed by /reload. pi-subagents on disk already had a Pi 1.4.0 compatibility fix (runner-aliases.js isKnownChordFreeHost); the live extension had the old module cached. After wassname's /reload an async test subagent ran and returned OK. No reinstall needed.


## 2026-10-25 -- Small operations notes (PI/OpenAI)

- `self-verify/SKILL.md` links `references/checklist.md` and `references/pre-mortem.md`, but both reads returned ENOENT. The installed skill directory contains only SKILL.md. I used the stated checklist and pre-mortem steps plus concrete code/tests/review; I did not read the missing reference sources or fetch replacements during run 11.
- Process `proc_7ff0` reported `end_reason=lost` for a commit. Its captured stdout says `[main 57a081b] Make lease snapshots non-destructive and verify selected-stage adapters`; HEAD agrees and the two paths are clean. The exit observation was lost, not the commit. No duplicate commit attempt. Cause of the tracking loss remains unchecked.


## 2026-10-26: scheduled heredocs become shell soup

PI/OpenAI (Sol): `schedule_task` stored my multiline shell command with all newlines folded to spaces. A heredoc then failed with `here-document at line1 delimited by end-of-file` / `syntax error near unexpected token` (exit2). Evidence: task `task_mvp1tnf4_dc477q`, attempt `1111d0a4-f8d0-4ca0-b8dd-b3d5a79fd2eb` in `~/.pi/agent/state/scheduler/tasks.json`. Use a single-line command invoking a checked-in script; I updated the same bounded stock task to `uv run --no-sync python scripts/eval/55_run14_box_a_rental.py quote` and verified it directly. No GPU rented; no other schedule changed.
