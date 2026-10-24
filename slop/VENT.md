
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
