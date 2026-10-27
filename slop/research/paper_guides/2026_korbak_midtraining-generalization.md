# Engineering guide: How far does alignment midtraining generalize?

**Observed metadata:** Tomek Korbak, Cameron Raymond, Micah Carroll, Marcus Williams, Mikita Balesni, Alan Guo, Jason Wolfe, Akshay Jagadeesh and Ian Kivlichan. OpenAI Alignment Research Blog, 27 March 2026 (article byline, not the fetched page's October timestamp). [Original](https://alignment.openai.com/how-far-does-alignment-midtraining-generalize/); local source: `docs/papers/2026_korbak_midtraining-generalization.md` (**P** below). No arXiv identifier stated.

**Observed code availability:** no paper-specific code found: checked `docs/vendor/`, `.gitmodules`, the complete local post and `slop/research/paper_guides/VENDOR.md`. The inventory records earlier GitHub/HF searches; those remote searches were not repeated here. No vendor path/commit applies. `docs/vendor/alignment_pretraining` is Tice's supporting code, **not** OpenAI's internal training pipeline.

## 1. What they did, in 5 lines

1. **Observed:** insert document fine-tuning after pretraining of an internal o4-mini-sized model (P:34).
2. **Observed:** compare positive documents, negative documents and no extra midtraining (P:44–50).
3. **Observed:** separately apply capabilities-focused SFT and RL with verifiable rewards to each branch, without safety training (P:52).
4. **Author claim:** near-distribution QA separates the branches; distant chat and agentic evaluations mostly do not (P:116,146–163).
5. **Inferred:** this challenges generalization claims from document-related QA; it does not test grafting or establish that our recipe fails.

## 2. Exact recipe

**Observed setup quotations** (all from P, §Setup):

> “We take an o4-mini-sized model that underwent standard pretraining” (34).

> “We finetune on 230k documents (~340M tokens) from the `positive` split.” (46; negative branch has the same stated size, 47).

> “we do _not_ mix in any other datasets” (50).

> “The pipeline consists of supervised finetuning and reinforcement learning with verifiable rewards” (52).

**Observed disclosures:** “not stated” means absent from this post, not filled from Tice's implementation.

| Field | Paper recipe |
|---|---|
| Starting checkpoint | Pretrained, pre-post-training checkpoint; internal o4-mini-sized model, **not** released o4-mini. Exact model ID/parameter count not stated. |
| Data / generator | Tice dataset `discourse-grounded-misalignment-synthetic-scenario-data`, `midtraining` subset, separate positive/negative splits. Synthetic papers, news, lectures, textbooks, fiction and movie summaries about AI choices and reasons (P:34–42). Generator model not stated. |
| Token counts | ~340M tokens / 230k documents **per trained branch**, not a combined 680M-token run. Epochs and total tokens processed not stated. |
| Replay / mixing | No other midtraining datasets; later SFT/RL mixes maths, coding and reasoning QA (P:50–52). |
| Full FT / LoRA | Not stated; rank, alpha, target modules and regularization not stated. “Finetune” does not establish full FT. |
| LR / schedule / epochs | Not stated for midtraining or subsequent stages. |
| Batch / sequence length | Not stated. |
| Loss masking / chat template | Not stated. Evaluation prompts request reasoning (P:56); that is not a training-template specification. |
| Post-training | SFT then RLVR, helpful-only; no safety training (P:52). No graft. |
| Eval suite / judge | GPQA Diamond, CodeForces 2408; Tice Article/Textbook QA; Model Spec compliance, Production deception, Alignment Generalization, Emergent Misalignment, Blackmail, Oversight Sabotage, Alignment questions; Apollo subset and impossible coding tasks (P:54–163). Deception judge: another reasoning model sees chain of thought (P:128); model ID and most scoring details not stated. |

## 3. Gotchas and reported failure modes

**Author claim — near-training success is not distant transfer.** The strongest QA evidence includes training seeds:

> “Questions used to bootstrap the synthetic articles in training.” (P:113, §QA evals).

> “When averaged across evals, alignment scores of all three runs are not significantly different” (P:163, §Agentic evals).

**Inferred:** label Article Questions as near-training, not independent held-out generalization. Do not import Tice's quoted ~60%/~75% as OpenAI's scores (P:116). Nor say RL erased every effect: §QA still reports ordered differences.

**Author claim — improvements can be non-specific to the intended direction.**

> “On the Alignment Generalization Benchmark, misalignment midtraining results in _better_ alignment than alignment midtraining.” (P:149, §Chat evals).

> “We don’t have a good explanation for this result.” (P:165, §Agentic evals).

**Inferred:** an improvement over untreated Base does not isolate taught values. Topic salience is a plausible author hypothesis, not an established mechanism or a reason to train on negative examples.

**Author claim — evaluation awareness remains unresolved.**

> “making models more eval-aware as opposed to more aligned” (P:175, §Discussion and limitations).

**Inferred:** action consistency outside explicit moral framing is likely more informative than self-description alone. No awareness-control result is supplied.

**Observed limitation:** no implementation is available here to check filtering, masks, hyperparameters or paper/code mismatches. **Inferred:** 340M tokens is neither a demonstrated minimum nor a recommendation to enlarge our corpus; P:173 only proposes insufficient scale as a possibility.

## 4. Compare with our pipeline

Paths: **G** = `configs/train/qwen3/graft.yml`; **S** = `configs/train/qwen3/sft.yml`; **B** = `scripts/train/12_run10_box.sh`; **C** = `scripts/train/14_run10_chat_box.sh`. Left column is **observed** configuration/documentation; risk column is **inferred**. These are run-10 launcher settings, not a claim that every historical adapter used today's data.

| Recipe field | Ours, with source | Risk / likely importance |
|---|---|---|
| Checkpoint | Qwen/Qwen3.5-35B-A3B-Base pinned in B:23; recipient Qwen/Qwen3.5-35B-A3B in `scripts/train/13_run10_evals.sh:22`. | High transfer uncertainty across model families and post-training. |
| Data / generator | Authentic Stoic/other texts plus Opus 5.5 documents (`docs/data_provenance.md:85,183–185`). | Likely important: different content and target character, not Tice's AI-scenario distribution. |
| Tokens | Approved source sizes ~3.1M Stoic / ~1.5M other (`AGENTS.md:27`); reused constitution adapter has 1,585 documents (B:3–4). | Far smaller; dose-response cannot establish a token scaling law. |
| Replay / mixing | Separate document corpora, no generic replay in B:24–32. Optional general-chat variant (`docs/data_provenance.md:186–187`). | No replay mismatch for basic document runs; later mixtures differ. |
| FT / LoRA | G:41–55 and S:40–54: bf16 LoRA, r64/alpha128 for named attention/shared-MLP projections; routed experts r16/alpha32. Spectral λ=50 for docs (B:32), fractional calibration for chat (C:91). | Effect unknown here; no evidence to replace locked LoRA/spectral choices. |
| LR / schedule / epochs | Docs 1e-4, cosine, warmup .05, 2 epochs (G:59–68). Chat 2e-4, cosine, warmup .1 (S:58–67); **launcher overrides 3 to 2 epochs** (C:86). | Reproduction gap is certain; optimal difference unknown. |
| Batch / sequence | Docs microbatch 1 × accumulation 8, length 2048; chat 1 × 4, length 8192; no packing (G:38–39,59–61; S:37–38,58–59). | Unknown paper comparison; document truncation may matter. |
| Mask / template | Plain-text completion versus assistant-only `input_output` (G:30–33; S:29–32). Qwen thinking-off template (`scripts/train/01_prepare.py:33–37`); EOS/empty-think checks (`scripts/train/check_loss_mask.py:14–39`). | Likely major protocol difference: their eval requests reasoning; ours serves thinking off. Do not switch modes to imitate this post. |
| Post-training | Chat on Base + fixed document blend, then graft both onto already post-trained Instruct (C:52–59,83–91,118–120). | Critical: their RL follows document training; recipient RL does not follow our graft. Neither erosion nor persistence transfers automatically. |
| Evaluation / judge | Frozen tiny-character, demos/viewpoints and 60 GSM8K questions (`scripts/eval/33_subset_cells.py:1–6`); ordinary checks and pinned Jev comparison documented in `docs/plans/20261021_character_graft_recipe.md:292`. | Likely important: not their agentic environments or hidden-CoT judge. Chat scores cannot certify tool-action transfer. |

## 5. Ideas to steal, ranked by expected value / cost

All **inferred proposals**, not new run approvals or training instructions.

1. **High / low: separate near-training and distant evidence.** Test: classify existing evaluation provenance, then check whether gains remain on genuinely held-out situations at matched capability.
2. **High / low: inspect stage dependence before adding training.** Test: compare saved document-only, chat-only and combined replies; report effects separately, and mark document removal beneath a dependent chat adapter as off-training-base, not causal training ablation.
3. **Medium / moderate: check action transfer and evaluation cues.** Test, if approved: use a held-out sandbox task with equivalent facts under explicit-test and ordinary-task framing; compare executed actions, not claimed virtues. Keep these cases out of training.

**Inferred recipe consequence:** change the strength of our evidence claims first. This post supplies no justified switch to full FT, new RL, negative-data training or a 340M-token target.

## 6. Coverage

**Observed read coverage:** complete local post, including Setup, all evaluation subsections, Discussion and Bibtex; figure captions but **not image pixels or linked eval papers**. Complete BRIEF, VENDOR inventory, README, jargon, current plan; constitution §§1–5 and supplied AGENTS instructions. Complete G/S, B/C, `13_run10_evals.sh`, `check_loss_mask.py`; targeted excerpts of `01_prepare.py`, `33_subset_cells.py`, data provenance and corpus manifest. Journal searched for Korbak/title: no match. Vendor directory/submodule inventory inspected; no upstream implementation read or run for this post. No model calls or training.

-- PI/OpenAI, 2026-10-27
