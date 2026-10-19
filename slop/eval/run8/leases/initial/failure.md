# Initial lease: SSH interruption after four cells

PI/OpenAI, 2026-10-19. Infrastructure failure; no model-collapse conclusion.

Observed: `controller.log` ends with `client_loop: send disconnect: Broken pipe` and an SSH return code of 255. It had completed `(0,0)`, `(0,1)`, `(1,0)`, `(1,1)`. The `(0,2)` merge wrote its probe report and model shards; no `(0,2)` reply JSONL or completion marker exists. The controller retrieved outputs and printed `RENTAL DESTROYED 56730968`. A separate provider GET confirmed no live instances. All original outputs and the pre-retry controller are archived here.

The SSH interruption's underlying cause is unknown. Successful later retrieval argues against a persistent host outage, but does not distinguish a transient network drop, SSH-session failure or a resource problem. Host/kernel diagnostics were not collected before this lease was destroyed. Do not call this donor-training or graft-inference failure.

Account credit after the controller's cleanup was $9.2618382929777 versus $12.854042338974978 before, a $3.5922040459972777 difference, not a reconciled invoice. A later provider GET returned $9.18481934297779, so billing had not fully settled. The cost ledger conservatively retains the entire original $9.822222 rental reserve until reconciliation.

Continuation uses the same model, adapters, frozen prompts, scoring protocol and precision. Changes are operational: a unique retry lease/state/label, a four-hour maximum paid from existing credit, SSH keepalives, a detached tmux-owned inference job with an exit-status file, bounded reconnects, and detection of a disappeared job. A failed monitoring connection no longer implies destroying a still-running comparison immediately. Completion discovery includes archived leases and rejects conflicting markers. Retry outputs remain separate until their identities are checked.

The old scheduled cutoff was cancelled only after confirmed destruction. A new cutoff explicitly naming `RUN8_LEASE=retry1` must be registered before new provisioning. The approved $30 combined cap still applies; no top-up, new training, healing or corpus generation is authorized by this recovery.
