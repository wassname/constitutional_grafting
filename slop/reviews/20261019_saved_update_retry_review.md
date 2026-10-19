## Retry review

Read both files completely. **No deterministic blocker found for this first retry**, provided the independent cutoff explicitly targets `RUN8_LEASE=retry1`. No execution/API calls; interruption cause remains unknown.

### Ranked findings

1. **High operational prerequisite — cutoff must carry the lease environment.**  
   `scripts/eval/30_run8_rental.py:23–28,42–48` selects teardown exclusively by the environment-derived label; omitted `RUN8_LEASE` defaults to `initial`. A timer invoking bare `destroy` would find no initial rental and leave retry1 running.  
   **Check before creation:** inspect the registered timer’s exact command/environment and confirm retry1’s label. Its deadline must cover the requested four-hour lease, not reuse an old cancelled schedule.

2. **Medium — completion discovery ignores earlier retry leases.**  
   Controller line 221 reads only `INPUTS/box_runs/*.done`, whereas retry retrieval writes into `leases/retry1/box_runs` (262). This correctly skips the four initial completed cells **for retry1**, but another continuation would rerun retry-completed cells unless explicitly consolidated.  
   **Check:** union completed artifacts across leases, rejecting conflicts; retain their provenance. Do not overwrite initial artifacts during consolidation.

3. **Medium — “all-attempt” accounting has a discovery gap.**  
   `slop/eval/run8/spending.py:27–30` discovers Jev attempt traces only through existing `cost.json` files. An interrupted judging batch with `http_attempts.jsonl` but no cost summary is omitted unless its active budget reservation remains present (43).  
   **Check before rental:** inspect orphan attempt traces and active reservations. This is a conditional omission, not evidence the present ledger undercounts. Historical batches remain successful-cache estimates, explicitly not reconstructed all-attempt invoices.

4. **Low — malformed error responses can block the budget check.**  
   `spending.py:18–21` assumes HTTP bodies are JSON objects and reported costs are numeric. HTML gateway errors, JSON arrays or `cost: null` cause exceptions rather than applying the fallback reserve. This fails closed before provisioning, but could unexpectedly prevent retry.  
   **Check:** validate those cases against conservative fallback handling.

### Confirmed behavior and remaining limits

The quote is written **before** `ledger()`, so the new reserve is included alongside the entire original reserve. Provider credit-minus-$1 and the combined $30 guard are separately checked. The advertised four-hour lease gives the runner 3.5 hours, leaving retrieval/teardown margin.

Nested `shlex.quote` construction is consistent: tmux starts `bash -lc`, `$?` is captured after the runner, and `job.exit` precedes the completion signal. Polling reconnects after SSH255/timeouts without relaunching inference. **The launch SSH call itself is not retried**; an ambiguous disconnect there triggers retrieval/destruction rather than duplicate launch—safe, though potentially wasteful.

Old outputs are not uploaded; unfinished cells restart cleanly on the new box, and retry retrieval uses a separate directory. Creation exceptions invoke exact-label cleanup. API availability, successful timer registration, package-environment equivalence and actual remote execution remain unvalidated. A fixed vLLM version with freshly resolved dependencies is not a complete environment lock.