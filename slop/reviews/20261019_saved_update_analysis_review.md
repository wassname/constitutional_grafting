## Analysis-path review — independent context, same model family

Read the three scoped files, both pinned aggregation scripts, manifest, and baseline/graft-only metadata and cost records. No execution or rendering; prior rental review is out of scope.

### Ranked findings

1. **High — the $30 guard is not comprehensive spending accounting.**  
   `slop/eval/run8/judge.py:47–49` budgets only rental reserve plus `new_cached_request_cost_usd` and a fixed $2 allowance. The cost records explicitly say **“Failed billed requests may be absent.”** The process judge’s `call()` can make six attempts, but `_cost` records only the accepted response (`scripts/eval/15_principle_judge.py:106–125`). Those process-judge expenses are not included in the wrapper’s ledger at all. No bound ties the $2 allowance to batch size/retries.  
   **Observed:** the two supplied cache ledgers total **$0.158844252**, successful new cached calls only—not total expenditure.  
   **Check:** reconcile all billable attempts, including process traces and failed calls, into one ledger before further paid checks; establish a per-batch maximum. This is an accounting gap, not evidence the cap has been exceeded.

2. **Medium — report provenance checks leave mutable inputs unchecked.**  
   `scripts/eval/31_saved_update_report.py:35–45` checks two protocol files and selected metadata fields, but does not verify current item/boundary hashes against the manifest or each judgment’s `items_sha256`. It also omits referenced-content hashes when comparing metadata. Imported `17_plot.py` and its capability-check dependency are recorded or indirectly described, not fully checked against a frozen implementation before computation. Changed item families/check kinds could therefore alter aggregation while score rows remain unchanged.  
   **Current evidence:** both supplied metadata files agree on the full-item hash, rubric, check implementation, judges and empty references. No actual drift observed.  
   **Check:** verify input hashes, per-run item snapshot identity, and all metric dependencies before rendering.

3. **Medium — selected process-check completeness can silently pass missing models.**  
   `15_principle_judge.py:162–166` derives `models` from already-filtered jobs. If one supplied model has no requested item/sample matches, it disappears from the expected grid; an entirely empty selection also passes. The resulting file could misleadingly look like a completed comparison.  
   **Check:** derive expected models from source records before filtering, require nonempty jobs, and assert every expected model × requested item exists.

### What is supported

The aggregation preserves correct paired signs: pinned capability is **model minus baseline**, and `31_saved_update_report.py:66` converts its interval to loss as `[-mean, -upper, -lower]`. Samples are averaged within item before item bootstrap. Complete scored-cell grids and matched model/base grids are checked.

Full and shared views remain separate: **59 character items versus the shared nine**, with the same 11 capability checks. Their character means must not be treated as interchangeable measurements; the separate panels correctly avoid doing so. Missing completed-cell judging is disclosed, although planned cells never generated are not listed.

JSON process mode uses the same `PROMPT` as Inspect mode, renders operator/user/assistant text, and records source/yardstick/lexicon hashes plus response traces. Its yardstick still defaults to the older configured path (`15_principle_judge.py:31`); verify the intended explicit setting. Quote verification checks normalized substrings anywhere in the dialogue, **not specifically assistant attribution**.

No winner claim is justified. Plot appearance, clipping, individual judgment validity and full reply review remain unvalidated here.