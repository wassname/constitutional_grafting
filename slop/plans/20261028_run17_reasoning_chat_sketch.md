# Sketch: run 17, run 16's best recipe plus the v3 reasoning chat data

Status: sketch for wassname, not approved. No GPU spend until he sets a budget. -- PI/Claude (opus-5-5), 2026-10-28

wassname (2026-10-28): "maybe sketch a v3 run best practises plus reasoning data?"

## What carries over from run 16 (`slop/eval/run16_v2/results.md`)

- Recipe to keep: plain new D ×1 = θ_I + Δ_docs + 1·Δsft_rewr_eos|docs, with Δ_docs = ½·Δtxt_stoic + 1·Δtxt_const + 1·Δtxt_other. Character +0.83 [+0.76, +0.90], maths 56/60 (Instruct 55), all 60 finished.
- Not worth more spend: projection, the char/cap selector, chat-stage control subtraction, anchored documents (no gain at matched character).
- Open defects: private-information disclosure (withheld reason put into the team email), sheet writes before reading rows, and a judge that scores those replies near +2.
- Process rules: every chat target ends with `<|im_end|>` (`scripts/train/check_loss_mask.py`); real-driver smoke test on the local GPU with a tiny random model before any rental (AGENTS.md); one maintained box driver (`scripts/eval/60-62_run16_*`) with a per-run config, not a new copy.

## What is new

- Chat adapter Δsft_reason|docs trained on `data/train/chat_v3.jsonl`: 1,031 rows, about 2.48M tokens, the teacher's real English reasoning in the think block (Kimi K3.1 Pro low, DeepSeek flash retry), replies via Latin/Greek then English, 19% name Musonius, about 12-15% ordinary help. Trained on θ_B + Δ_docs at the doses above (its training base), same LoRA settings as `configs/train/qwen/sft.yml` (r64, lr 1e-4, sequence_len 8192).
- First run that can serve with thinking on. Run 13 showed thinking-on fails with empty-think chat data (176/214 empty turns); this data has real reasoning, so test both modes.
- Optional, only if the document batch is built and read first: a fourth document adapter Δtxt_rot from the rotated-role Musonius documents (`docs_v3.jsonl`), swept alone before mixing (coherence budget rule).

## Goals

1. [ ] goal: chat_v3 is ready to train
   - subtle failure mode: Latin/Greek round trip keeps misleading errors (7/20 rows before the fix) that the judge passes
   - discriminator: the same GPT-6.1 sol defect read on 20 rows after the fidelity check-and-fix shows no more defect rows than Kimi's direct English (4/20)
   - deliverable: rebuilt `data/train/chat_v3.jsonl`, `check_loss_mask.py` passing
2. [ ] goal: the reasoning chat adapter beats or matches new D at matched character
   - cells (graft time, all on the same lease, thinking off and on): Instruct; new D ×1 (reference, reuse adapter); θ_I + Δ_docs + {½, 1, 1.5}·Δsft_reason|docs; θ_I + 1·Δsft_reason|docs (graft-time removal of Δ_docs, off its training base)
   - subtle failure mode: thinking-on maths looks worse only because the generation budget cuts long reasoning
   - discriminator: maths with a thinking-on budget large enough that Instruct finishes all 60; report finished counts; character compared at matched dose by interpolation, plus the answer panel read
   - deliverable: results page with both tables (dose up/down, one adapter removed), demo panel, answer panel and reading notes
3. [ ] goal: action defects measured by reading emitted actions, not the judge
   - discriminator: the run-16 email and fridge items, 2 samples each, read in full for every cell; counts beside the character score
4. [ ] goal: the reasoning itself is read
   - discriminator: 20 think blocks per main cell read for deliberate-then-decide and "my principles" vs "I was told" (wassname's criteria); report how often it reasons in Kimi's note form

## Order and cost (estimates, from run 16's second lease ≈ $26 GPU + $5 judges)

1. Data: fidelity fix and rebuild (in progress, about $5-10 API of the approved $20).
2. Local smoke test of the box driver with a tiny random model and 1 batch per stage, thinking on and off (no rental).
3. One lease: train Δsft_reason|docs (1 adapter, about 2.5M tokens × 4 epochs; pick the epoch by the demo panel), merge, serve, score 6-8 cells in both thinking modes. Thinking-on generations are longer, so expect more GPU time than run 16, maybe $30-45 total. Needs wassname's budget.

## Questions for wassname

- Budget for run 17, and whether the optional document adapter Δtxt_rot is in scope.
- Thinking-on as the main serving mode if it holds up, or keep thinking off as the default and report both?
