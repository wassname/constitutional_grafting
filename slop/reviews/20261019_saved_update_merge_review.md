# Saved-update merge and lease review

Independent-context reviewer-openai / GPT-6 Astra, 2026-10-19. Imported by PI/OpenAI (trailing spaces removed); this is not cross-family independence. Parent corrections after this review are recorded in `slop/eval/run8/preflight.md`.

## Verdict

**No deterministic launch blocker found**, conditional on regenerating the manifest and registering the independent destruction timer **before provisioning**. Neither prerequisite has been verified as completed. No execution, API calls, edits or rental performed.

Read all three requested files, the watchdog, and GSM8K metadata.

### Remaining concrete gaps

1. **Medium — hardware preflight failures are masked.**
   `scripts/eval/30_run8_rental.py:124` separates checks with semicolons:
   `"nvidia-smi; python ...; dd ...; rm ..."`.
   Without fail-fast shell handling, a failed CUDA-memory assertion or disk write can still return success when `rm` succeeds. This affects unsuitable/broken offers and can waste setup time before a later failure.
   **Check:** require each command’s success (`set -e`/`&&`); a deliberately failing assertion should stop setup.

2. **Medium — starting tmux does not establish a working watchdog.**
   Controller line 140 checks launch success only. `scripts/train/box_watchdog.sh` exits if container credentials are absent or its authenticated GET is not HTTP 200; the controller never verifies that result. Thus the claimed one-hour fallback remains unvalidated.
   **Check:** inspect the watchdog’s successful authentication log and live session before proceeding. The independent five-hour timer still bounds this risk if correctly registered.

3. **Medium — provisioning has an exception window outside cleanup.**
   Controller lines 78–98 create the instance and write state **before** entering `try/finally` at line 99. A lost create response or failed state write can leave a rental without immediate cleanup. `destroy()`’s exact-label fallback (39–54) provides recovery when state is absent, so the promised independent timer is materially necessary—not redundant.
   **Check:** ensure that timer invokes label-capable teardown even when creation/state recording fails. API deletion and listing consistency remain untested; `destroy()` has no retry loop.

### Corrections confirmed

The driver clears `KGROUPS`, checks adapter configs and executed-source hashes, validates recipient revision/config, and checks empty merge groups/fp16. It refuses stale output files, encompasses merging in cleanup, and kills the server process group. Frozen GSM8K evaluation avoids dataset lookup; metadata records the supplied revision and 60 selected rows.

SSH/rsync argv construction, adapter destination names, tar layout and remote run paths are mutually consistent. Inference targets localhost; no project API key is included in uploads. Setup/upload failures request destruction; normal cleanup attempts retrieval for at most 600 seconds and destroys even if retrieval fails.

The quote calculation includes the stated five-hour allowance and bandwidth reserve, but actual provider pricing semantics, image availability, package resolution, SSH authorization, watchdog credentials, GPU capacity/throughput and full-model fp16 behavior remain **unvalidated operational assumptions**, not demonstrated defects.
