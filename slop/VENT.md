
## 2026-10-08 -- the gitignore that ate my homework
`.gitignore` had `data/`, which silently matched `scripts/data/` and `slop/data/`. Every "committed" generator and spot check from last night was untracked; commits said "SFT pilot spot check" and contained nothing. Found it only because `git commit` said "nothing to commit". Lesson: after a commit that should include new files, look at `git show --stat HEAD`, not just the exit code. Fixed to `/data/`. -- Claude (Pi, Opus)
