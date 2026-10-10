
## 2026-10-08 -- the gitignore that ate my homework
`.gitignore` had `data/`, which silently matched `scripts/data/` and `slop/data/`. Every "committed" generator and spot check from last night was untracked; commits said "SFT pilot spot check" and contained nothing. Found it only because `git commit` said "nothing to commit". Lesson: after a commit that should include new files, look at `git show --stat HEAD`, not just the exit code. Fixed to `/data/`. -- Claude (Pi, Opus)

## 2026-10-08 ~01:45 -- the key had a ceiling I didn't check
OpenRouter returned 402 mid-run. The account has ~$152 credit, but the key itself has a weekly limit of $88 (`GET /api/v1/key` → `limit_remaining 0.007`), and I only ever checked `/credits`. Lesson for future agents: check both `/credits` and `/key` before a batch; the per-key cap is the binding one. I did not mint or look for another key: raising it needs wassname's YubiKey (agent-vault tier 2), and the cap is a deliberate limit on how much the key can spend if something goes wrong. -- Claude (Pi, Opus)

- 2026-10-10 (Claude, Opus 5.5): stale 0-byte .git/index.lock three times today (15:06, 17:50, 19:21 Perth), blocking commits. Likely cause (pane agent, inferred): zentui footer runs `git status` in the background with a 2 s timeout; if the session is killed hard the lock stays. Pane agent patched zentui locally with GIT_OPTIONAL_LOCKS=0 (git.ts); a package update would undo it. Upstream PR needs wassname.
