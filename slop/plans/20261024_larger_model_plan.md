# Plan: one larger-model run (plan only, not approved)

PI/Claude, 2026-10-24. wassname: "and to plan a larger model run for later"; "hmm might need smarter model". Grafting needs a public Base and its own post-trained Instruct.

## 1. Which current failures could size fix?

| Failure seen in run 10 | Evidence | Cause (my estimate) | Would a larger model fix it? |
|:--|:--|:--|:--|
| Flood courier: refuses to take the guard's key | grafts with the constitution adapter take it 2/37, without it 16/32; Const alone 0/2; Instruct 2/2 (`slop/eval/run10/stage8/reading.md`) | data: the constitution documents (lead: anti-domination lines generalised to small-scale force) | unlikely; a bigger model would learn the same documents more faithfully |
| Eulogy: asks a question instead of writing | 143 ask-first chat rows; chat ×0.5 and the difference graft write it | data (chat rows) | no; fixed by data or dose |
| Factual slips after grafting ("The Divine Comedy is about the Fall", "the finder's money", vote tallies) | Instruct gets Milton right; slips appear in graft cells (`stage8/reading.md`, demo column) | capacity: the graft disturbs stored knowledge | plausible; larger models usually keep facts better under fine-tuning (not measured here) |
| Answer and reasons disagree (wallet `"ans": true` with reasons for false) | Other ×2, chat ×2 cells | capacity and dose | plausible |
| Length and format limits break as doses rise ("One line" → 207–524 words; maths 55 → 43 at chat ×2) | stage 8 dose table | coherence budget (shared limit of adapters) | plausible: a larger model may tolerate more total dose; untested |
| Difference graft loses instruction-following | stage 9: maths 18, ordinary 8/22 | method: control trained on Instruct's own replies | no |

So two of the three character failures that matter (flood, eulogy) are data or method problems that would recur. Size could help knowledge retention and how much dose fits.

## 2. Candidates (public Base + Instruct)

Checked 2026-10-24 via the Hugging Face API; raw outputs in `slop/research/20261024_larger_model_check/` (`hf_list_*.json` model lists, `hf_model_info.jsonl` sizes and licences).

| Model | Total / active params | Base + Instruct | Fits on | Notes |
|:--|:--|:--|:--|:--|
| **NVIDIA Nemotron-3-Super-120B-A12B** | 124B / 12B | `...-Base-BF16` + `...-BF16`, not gated | 4× RTX PRO 6000 (384 GB) | 4× our active compute; hybrid Mamba-MoE, so LoRA targets and vLLM support need checking first |
| GLM-4.5-Air | 110B / 12B | `GLM-4.5-Air-Base` + `GLM-4.5-Air`, MIT | 4× RTX PRO 6000 | older (2025-07); plain MoE, simpler tooling |
| DeepSeek-V4-Flash (V4, not V4.1) | 292B / ? | `-Base` + instruct, MIT | 8 GPUs | about 2× the cost of the 120B options |
| Llama-3.1-70B | 71B dense | base + Instruct, gated | 2–4 GPUs | dense: every token uses all 70B; older |

Your candidates, ruled out because grafting needs a public Base of the same model (same check):

| Asked about | Public Base? | Size | Verdict |
|:--|:--|:--|:--|
| GLM-5.3-Flash | no (`zai-org` lists GLM-5, 5.1, 5.2, 5.3, 5.3-Flash, no Base) | 321B | ruled out; GLM-4.5-Air is the newest GLM with a Base |
| Kimi K3 | no (only `moonshotai/Kimi-K3`; Bases exist for K2 and Kimi-Linear-48B) | 2,780B | ruled out (and too large) |
| DeepSeek V4.1 Flash | no. V4-Flash-Base is not its base: the V4.1 card says it "is trained from scratch on a multimodal corpus comprising 45T tokens", and the configs differ in every shape (hidden 4096 vs 5120, 43 vs 40 layers, 256 vs 384 experts; checked by PI/Claude). Its own `DeepSeek-V4.1-Flash-Base` is unpublished. `slop/research/20261024_deepseek_v41_base.md` | 763B on HF vs V4-Flash 291B | ruled out unless DeepSeek publishes the V4.1 Base; wassname 2026-10-24: "we can just use v4" (V4-Flash-Base + V4-Flash, 284B / 13B active, same configs) |

Tinker (hosted LoRA training; models page saved): usable, and trained weights can be downloaded and merged ("Merge into a HuggingFace Model"). But the only Base models it offers are Qwen3.5-35B-A3B-Base and Qwen3.5-9B-Base. So for a larger model Tinker is a price guide only; its larger models (Nemotron-3-Super, GLM-5.3-Flash, DeepSeek-V4.1-Flash, Qwen3.5-397B-A17B) are post-trained, and our recipe trains on Base. For our current model it would cost $1.177 per million training tokens (Qwen3.5-35B-A3B-Base "Train" column), about $8 per pass over the 6.7M text-adapter tokens, similar to renting.

Recommendation: GLM-4.5-Air if tooling must just work (plain MoE like ours); Nemotron-3-Super if a newer model is worth a tooling check first. Not DeepSeek-V4-Flash: twice the cost for an old Flash whose Base is not the V4.1 we know.

## 3. Cost (vast.ai; 4× RTX PRO 6000 at $5.34/h, `vast_offers.jsonl`, checked 2026-10-23 17:33 UTC; 2× H200 at $9.74/h was offered an hour earlier and none at the saved check)

Run-10 actuals on one RTX PRO 6000 ($1.84/h, `slop/eval/run10/stage8/lease.json` `hourly_rate`): text adapters 8–9 h (stage 1: `slop/eval/run10/stage1/account_credit_after.json` elapsed × rate = $13.95), a chat adapter about 1.6 h (`stage7/box_runs/stages.log`: start 06:47, done 08:22), setup about 1.5 h per lease (`stage10`: created 13:15, evals started 14:48), about 20 min per graft cell (`stage8`: 8 cells in about 2.7 h). Scaling: 4× active parameters on 4× the GPUs gives about the same wall-clock if the code splits the experts across GPUs; I have not tested that, so I double it.

| Step (one recipe: Const + Stoic + Other + chat, plus 8 eval cells) | Hours on 4× RTX PRO 6000 | Cost |
|:--|--:|--:|
| text adapters | 9–18 | $48–96 |
| chat adapter | 2–4 | $11–21 |
| 8 graft cells evaluated | 3–6 | $16–32 |
| setup, downloads (250 GB), retries | 3–6 | $16–32 |
| **total** | **17–34** | **$90–180** |

Data: reuse run-10 data (no new API cost) except identity rows renamed for the new base (about $5).

## 4. Before paying for size

1. Fix the data problems first: the flood refusal (constitution documents) and the chat rows, or the larger run repeats them.
2. One day of tooling: load the Base in our LoRA trainer and vLLM on a cheap box, merge one tiny adapter, check greedy output.
3. Run the same eval set and demo panel so results compare directly with run 10.
