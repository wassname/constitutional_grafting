# Thinking-heal training/evaluation plan — NOT RUN

This is preparation under `slop/plans/20261026_thinking_heal.md` (approved brief, commit 4f39133), not a GPU lease, training implementation, or evidence of a successful heal. No GPU/training was used here.

## Frozen parent and naming

Let θ_B be Qwen3.5-35B-A3B-Base, θ_I its Instruct sibling, and:

- Δ_docs = ½·Δtxt_stoic + 1·Δtxt_const + 1·Δtxt_other, each document LoRA trained on θ_B.
- Δsft_rewr|docs was trained on θ_B + Δ_docs, on constitution-rewritten chats.
- D = θ_I + Δ_docs + 1·Δsft_rewr|docs, plain graft on the chat adapter's training base, id `r10_stoic0.5_const1_other1_cx_chatr121`.
- θ_D + Δheal_trace|D and θ_D + Δheal_mix|D are capability/format repairs trained on the frozen **merged D**, not new character donor adapters trained on Instruct. State this stage order explicitly. Their training parent is D; these are not evidence for graft-only character training.

D's interpretable off-mode character and run13's large on-mode blank-final failure make this a measured repair target, not a near-baseline parent with nothing to recover. Freezing D does not prevent the new LoRA from cancelling its character functionally.

## Before training

Final preparation snapshot: 509 quarantined trace candidates, 747,103 supervised assistant tokens; 489 retained replies still need full reads. All 300 D answers remain to be generated and read. `reader_assignments.json` indexes five-row full-native packets; `report.md` and `summary.json` record exclusions and length/source bias. Conservative API accounting is $1.216868395, so the illustrative six-hour <=$2/hour lease plus $4 judges and $1 storage totals <=$18.216868395, still requiring a live quote and explicit lease approval.

1. Finish full, source+exact-request+native-reasoning+final reads of **every** retained candidate in `reply_batches/`; use `read_coverage.json`. A 6+30 preparation read is not approval for the rest. Resolve factual/technical defects and source ambiguities; do not splice corrected thoughts onto original answers. The automatic repeated-indecision filter is only a conservative first screen. Keep rejected IDs/reasons and originals.
2. Generate the 300 selected `D_prompts.jsonl` rows with **D itself**, thinking disabled, on a separately approved GPU lease. Store row id, exact messages, model id, enable_thinking=false, answer and finish_reason=stop. `build --D-answers <path>` requires that schema and the exact frozen prompt. No original chatr12 target is used as D's answer.
3. Read every D reply in full, including implemented tool actions where applicable. These are retention replay, not a new constitutional teacher. Do not imitate D's broken thinking-on output.
4. Re-run the real-tokenizer CPU test and `scripts/train/check_loss_mask.py` on the final assembled training data. Trace loss includes nonempty reasoning, closer, final and EOS. D replay's empty off-mode think block stays entirely unlabelled. The trace builder constructs the **native template** from API-separated channels; this preparation cannot certify literal provider-emitted special-token IDs.
5. Count actual assistant tokens in both reviewed subsets before choosing the mixture. Target roughly equal assistant-token budgets, not equal row counts, without silently duplicating D answers or dropping long traces just to fit a preferred score. A 500–2,000-row one-pass pilot is the approved range, not a mandate to pad with unreviewed rows. If the reviewed data and token balance cannot meet it, report the actual limitation before training.

## Training variants (future GPU decision)

Freeze the merged D at the same precision as its control. Add one removable **rank-8 LoRA** per variant; do not update parent weights. Start with one epoch and early checkpoints (e.g. quarter/half/full pass). Keep the existing donor target-module/spectral-regularization pattern rather than inventing a new merge/projection/full-FT intervention. Do not truncate away the closing marker/final/EOS: reject an overlength row or raise the supported context under the memory budget, never retain a boundary-damaged target.

- **Traces-only heal:** reviewed untouched-Instruct native thinking-on traces on neutral training prompts.
- **Mixed heal:** the same reviewed trace pool plus reviewed D thinking-off replay; roughly matched assistant-token budgets. Compare on a matched total supervised-token/optimizer budget as well as reporting raw rows, tokens and actual passes. Mixing is itself an ablation; don't call two unequal compute runs a clean causal comparison.
- **Optional mixed+KL:** only if time and memory fit the same hard cap. Modest forward KL, frozen D → healed D, on thinking-off prefixes only. Do not KL-match untouched Instruct globally or D's broken thinking-on outputs. Do not promise KL support here: a second parent forward may exceed memory/time. Omit rather than exceed the cap; rank/freezing/KL are safeguards, not character-retention guarantees.

Compare unhealed D, untouched Instruct, traces-only and mixed at early/final checkpoints. Treat baseline cached records as historical unless serving precision, generation protocol and tokenizer match. Choose the **smallest repair** that recovers finals while preserving D's off-mode character, not the highest maths-only score. Dose-sweep the new heal LoRA around its full dose only if budget remains; report missing cells rather than calling a recipe best. No new document/chat-base doses are changed.

## Evaluation in both modes

Use `scripts/eval/54_run13_thinking_box.py`'s recorder and native qwen3 parser with raw response projections and final-only histories. Test thinking explicitly on and off, on the same frozen run13 evaluation prompts and matched seeds/settings. Preserve all failures.

Report blank visible finals, close-before-EOS/EOS-before-close, missing closers, loops, cutoffs/truncations and ordinary help. Score visible-final character actions/preferences separately from any hidden-answer diagnostic. Check multi-turn pressure and **fridge tool-call actions**, not merely refusal wording: a virtuous-looking explanation can accompany a false-temperature call. Run frozen GSM60/ordinary checks at the same precision and protocol as the unhealed parent; report correct-and-normally-completed answers as well as extracted-number accuracy. Include the fixed temperature-zero four-demo panel, full prompts and both turns, marking unrun historical comparison cells not run. Regenerate/read the answer panel and record defects before choosing a checkpoint. A nonempty final alone is not retained character.

## GPU-hours/cost estimate and stop rule

Planning estimates, **not measurements or a live rental quote**. After filtering, assume about 0.5–1.5M total sequence tokens per variant and 250–600 effective training tokens/s on one 80–96GB datacenter GPU (the full frozen ~35B fp16/bf16 checkpoint alone is ~70GB). Rank-8 LoRA reduces trainable/optimizer memory, not frozen-weight or activation memory. An 80GB device may be tight at long contexts; 96GB or an existing proven offload configuration is preferable. No new quantized-parent comparison should silently replace the same-precision D control.

Illustrative two-variant budget: 1–3.4 GPU-hours training (1–3M combined tokens / 250–600 tokens/s), 0.5–1 hour D replay plus setup/merge, and 1.5–2 hours serving/evaluation = **about 3–6.4 GPU-hours** before a hard deadline. The slow/large endpoint does not fit the six-hour reservation; measure early and stop at an earlier checkpoint rather than exceed it. Reserve **at most 6 wall-hours at ≤$2/hour ($12)**, ≤$4 for future judging, ≤$1 for transfer/storage, and ≤$3 already-prepared API traces/review = **≤$20 all-in**. This is a planning ceiling, not authorization to rent; a live quote and explicit GPU lease decision are still required. Actual prep API cost and token counts are in `summary.json`/`report.md` and must replace this reserve when budgeting. Use the conservative API-accounted total, including unresolved reserves, in the live calculation: GPU wall-hours ≤ min(6, (20 − API_accounted − 4 judging − 1 storage)/hourly_rate). If preparation approaches its $5 cap, a $2/hour lease is limited to five hours, not six. At a higher hourly rate, reduce allowed wall-hours accordingly.

Before the full epoch, measure 20–50 steps' actual tokens/s, memory and projected remaining cost. Stop if the measured two-variant plan will exceed the remaining $20: save the early checkpoint and report incomplete variants; do not buy more time, silently drop character evaluation, or pad a poor-quality corpus. Optional KL is first to omit. Set a provider-enforced/runner deadline and destroy the lease after retrieval; all paid failures and judges count. No claim is made that all 600 long raw traces, full unfiltered contexts and an extra KL model can fit this illustrative budget.

Read coverage for design: PI/Sol read the brief, AGENTS, constitution sections 1–5, local merge/heal reasoning research note and run13 results in full. Literature claims remain the research note's attributed findings; this preparation does not independently reproduce any paper.

-- PI/Sol (heal prep 2)
