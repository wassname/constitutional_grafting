# Saved-update comparison: preflight

PI/OpenAI, 2026-10-19. Approved goal: compare `Instruct + a*Δsft + b*Δdocs`, then bounded data work only if useful evidence and budget remain. Hard combined new-spending limit: $30; no new training, healing, Echo or translation calls. No rental or model inference had occurred when this note was written.

## Inputs and implementation

- SFT adapter SHA256: `8e7b6d048de4c7bf1002b1754353d07c0819782685428680263f4df97c491f73`.
- Document adapter SHA256: `5149961a47aab9f39560ae1aac3b1e63504c5d69118e64d95c1051da86e6acaa`.
- All 660 tensor names, shapes and dtypes match between adapters. Both have float32 factors. Their full configs differ only in the Base/Instruct anchor; module rank/alpha 64/128 and routed-expert rank/alpha 16/32 are the same.
- The revised `scripts/train/02_merge.py` merges separate updates in SFT-then-document order, without saving an intermediate model or adding adapter factors together. Each merge rounds into fp16. This is not a promise of one-final-rounding arithmetic or byte identity with older mixed-precision checkpoints.
- Zero scales are supported in the merger; the driver omits zero stages. It explicitly clears `KGROUPS`, sets the Qwen tokenizer source and fp16 merge/serving, and checks the merge report.
- Regression through the production merge helper passed: `run8_merge_precision_regression.log` says "seven two-update combinations in fp32/fp16 against explicit factor products; exact zero-update weights" (torch 2.14.1+cpu, PEFT 0.21.2). This is an expert-only toy test, not full-model CLI/serving validation. The known rank-pattern warning also appears; the rank-shape test passes.
- Independent-context Astra review identified zero-stage assertions and further environment/provenance/cleanup gaps. Parent fixed those described above and added a separate finite-lease controller. The final controller review found no deterministic launch blocker, conditional on final manifest freeze and registering independent teardown. It identified shell checks without fail-fast handling and an unverified watchdog startup; parent added `set -e` and a bounded authentication-log/live-session check. The exact-label teardown handles missing state as well as normal recorded leases. This is not cross-family review; raw review: `slop/reviews/20261019_saved_update_merge_review.md`.

## Evaluation scope

`manifest.json` freezes the current 96-item tiny-character snapshot (source commit `becd16c8fbcafb910a23636e85e7006f8a157e0a`), source hashes, adapter configs, model revision/config and all input hashes. The snapshot differs from older runs; do not reuse their aggregate scores.

- First seven cells: `(0,0), (0,1), (1,0), (1,1), (0,2), (2,0), (2,2)`, 96 items × two samples at temperature 0.7.
- Extra strength points: independently increase each update through `4,8,16,32`, stopping a path after manual confirmation of incoherence or when the finite lease ends. A boundary not reached is unfinished, not coherent by default.
- Boundary subset: all 19 capability items, all six point-of-view items, and SHA256-first ID in each other family, 39 total. It was selected before new replies. Original prompts and output caps are retained. Subset scores are not interchangeable with full-snapshot scores.
- Fixed striking demos and identity panel: temperature zero, every tested cell. Read full replies, including failures and all follow-up turns.
- Supplementary maths: GSM8K long-60, selection frozen by `26_gsm8k.py`, source dataset commit `740312add88f781978c0658806c59bc2815b9866`. This is not the still-unmeasured incumbent long-300 result.
- Server uses fp16 for untouched Instruct too, identical generation settings, thinking off, and eager execution. Same seeds do not guarantee bit-identical GPU sampling. Native model snapshot: `59d61f3ce65a6d9863b86d2e96597125219dc754`.

## Input read scope

Parent read the complete first care-home item, sibling-taboo item, hiring-code item and all three dropped-parcel point-of-view inputs, plus the first complete frozen maths question/solution. Selection: fixed first item and diagnostic families named in advance, not random coverage of all 96. The hiring item's notes make a broad legal claim; do not treat that note as verified law or let it excuse checking the actual generated code. No new model replies or judge verdicts existed yet.

## Before interpreting

Question: does either saved update provide useful reasons, speech or decisions at comparable capability, alone or in combination?

Competing explanations, not measured probabilities: extra SFT may carry most conversational character; documents may work alone; documents may depend on the SFT recipient; apparent character gain may be longer prose or direct taught-case recall; precision, targets, prompts or judging may confound the comparison. The zero-update baseline, separate coefficients, raw replies and capability checks distinguish these better than another training run now. Varying the whole SFT update does not isolate Echo.

No direction or useful effect size is assumed for the untested zero-SFT graft. Historical evidence supports document changes conditional on SFT, not necessity of that SFT. Read actual replies, judge reasoning and verdicts; check pressure/point-of-view consistency and ordinary task artifacts. Do not equate token-cap hits with incoherence or use identity recall as the character score.

## Spending and teardown

The controller will quote a datacentre GPU with at least 90 GB memory and 300 GB disk, low bandwidth charges, and a five-hour reserve below $10.50 and available credit minus $1. Only Instruct is downloaded; Base is unnecessary for merging these saved updates. The runner deadline is 4.5 hours from rental creation; the remaining half-hour is for retrieval/teardown. An independent new one-shot five-hour destruction task must be registered before launch, in addition to the remote heartbeat watchdog. Older cancelled schedules are not recreated.

No project API key is sent to the GPU box. Provider-wide OpenRouter usage changes cannot be charged to this run because the key is shared; later judging costs must come from this run's actual recorded calls. Native subscription reviewer calls incur no additional per-call project API spending. The lease quote is a reserve, not a reconciled invoice.
