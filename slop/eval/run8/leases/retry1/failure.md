# Retry1: provider status request rate-limited during image loading

PI/OpenAI, 2026-10-19. Instance `56746810` never reached inference setup. After about four minutes in `loading`, a provider GET returned HTTP429. The controller raised before setup, retrieved available instance metadata and destroyed this lease; `destroy_response.json` records success and its provider-list assertion passed. The scoped cutoff was then cancelled. This is not a model result.

The prior recovery fixed long-lived SSH execution but still polled provisioning every ten seconds and treated a transient provider GET error as fatal. GETs now have bounded, logged backoff for HTTP429 and transient server failures, and readiness checks occur once per minute. Non-idempotent creation calls are not automatically replayed. Future inference remains detached with an explicit completion record and bounded monitoring reconnects.

Original logs and accounting remain under this lease directory and `controller_retry1.log`. The cost ledger conservatively keeps the entire four-hour reservation until reconciliation. A further lease may use at most 3.5 hours, existing credit only, with its own unique label/state and independent destruction timer; no new training, healing or corpus generation is implied.
