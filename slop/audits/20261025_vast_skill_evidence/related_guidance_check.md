Yes—Modal suits six independent ~15-minute GPU evals: provider-enforced timeouts and persistent Volumes reduce SSH-controller dependence; compare whole-job costs, including CPU/RAM and retries.
Start with the local `modal` skill and [Hermes’ Modal guide](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/modal/SKILL.md).
[Modal’s resumable-training guide](https://modal.com/docs/examples/long-training) covers persistent checkpoints, retries and detached runs.
[Vast’s official skill](https://github.com/vast-ai/vast-claude-plugin/blob/main/skills/vastai/SKILL.md) covers setup/diagnostics; check installed-version help, and do not copy its unconditional offline destruction.
[Vastkit’s guide](https://github.com/RazinAleksandr/vastkit/blob/main/skills/vastkit/SKILL.md) covers whole-session cost and artifact verification; reference only, not an approved dependency.
No: a one-hour timeout is per attempt; three retries allow up to four hours per job (24 GPU-hours across six). Bound retries and configure a workspace budget; the timeout is not a total spending cap.
Do not destroy an offline Vast box before recovering outputs: stop/preserve its disk if retrieval fails, then copy and hash-check results before destruction. Stopped storage still bills; restart may be unavailable.
— PI/OpenAI
