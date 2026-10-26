# Reasoning pilot — revised run in progress

Main generation is running in a persistent project process managed by const_v2, log `logs/owned_full.log`. No training or GPU work. No quality/scaling conclusion yet. Frozen 20 rows unchanged; existing targets never shown to teachers.

## Current approved design (supersedes earlier arms)

P0/no guide and P1/accepted revised Kimi guide × Kimi, MiMo, GLM × 20 rows: 120 direct-English targets. P3/Opus guide × Kimi and GLM × 20: 40 more. P1/classical-language source then same-teacher English translation × Kimi and GLM × 20: 40 translated-English targets. **200 English deliverables**, 240 main calls; same frozen 20 rows. P2/GLM guide was rejected after one revision (see `guide_read.md`); this is a guide failure, not a GLM teacher result.

All targets embody **owned values**, not instruction citations. The former cite/free arms were superseded before main output. Explicit written `<reasoning>` then `<answer>` in one forward generation; this is synthetic visible deliberation, not a claim of introspective faithfulness. Kimi and GLM use native reasoning at effort low plus the written sections; MiMo is tested with native reasoning off. Retain/read native fields separately; they are not training targets. Kimi-off format smoke leaked planning into content and was rejected, not parsed permissively. See `template_provenance.md` for settings, final template and source coverage.

Prompt precedents: CAI complete same-format demonstrations (three from each accepted guide, none for P0); Deliberative Alignment analysis before answering; MSM's internalized-values wording; Teaching Claude Why guidance against repetition and misrepresentation. No added “case law, don't copy” or demonstration-warning line. Final actual prompts are saved individually. Check reasoning quality before style, including the classical-language arm: the earlier Greek style pilot did not demonstrate better reasoning.

P3 came from a **one-time honest-purpose retry by const_v2**, explicitly requested by the user after the original ToS-filter refusal; worker made no Anthropic call. Full raw reply and context preserved, actual $0.133324 imported into the ledger. No further attempt planned.

## Budget and history

Cap **$15 total**, including original Opus $0.099392 and the interrupted Kimi call's **$0.181580 full reserve** (a conservative upper bound, not reported actual). Supervisor approved retaining that pending record as history and retrying once under a new ID. Per-call budget reservation fails closed on unresolved billing; no automatic retries/substitutions. All actual reported charges append to `budget.json`/`raw.jsonl`; external P3 actual charge is in `opus_guide_retry_raw.json` and the same ledger. Main-run estimate $6–8, not a bill.

The final random10 in `review_selection_revision.json` was frozen with seed0 over all 200 deliverables before any main output. Older unused selections are preserved. Full executor reads and blind independent cheap-model review remain to be completed. The original blocked report, incomplete primer and refusal remain history, not approved training data. No samples accepted for training yet; do not scale on this in-progress report.

-- PI/Sol (worker)
