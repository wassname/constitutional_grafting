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

## 2. Candidates (public Base + Instruct, checked on Hugging Face 2026-10-24)

| Model | Total / active params | Base + Instruct | Fits on | Notes |
|:--|:--|:--|:--|:--|
| **NVIDIA Nemotron-3-Super-120B-A12B** | 124B / 12B | `...-Base-BF16` + `...-BF16`, not gated | 4× RTX PRO 6000 (384 GB) | 4× our active compute; hybrid Mamba-MoE, so LoRA targets and vLLM support need checking first |
| GLM-4.5-Air | 110B / 12B | `GLM-4.5-Air-Base` + `GLM-4.5-Air`, MIT | 4× RTX PRO 6000 | older (2025-07); plain MoE, simpler tooling |
| DeepSeek-V4-Flash (V4, not V4.1) | 292B / ? | `-Base` + instruct, MIT | 8 GPUs | about 2× the cost of the 120B options |
| Llama-3.1-70B | 71B dense | base + Instruct, gated | 2–4 GPUs | dense: every token uses all 70B; older |

Recommendation: GLM-4.5-Air if tooling must just work (plain MoE like ours); Nemotron-3-Super if a newer model is worth a tooling check first. Not DeepSeek-V4-Flash: twice the cost for an old Flash whose Base is not the V4.1 we know.

## 3. Cost (vast.ai today; 4× RTX PRO 6000 at $5.34/h, 2× H200 at $9.74/h)

Run-10 actuals on one RTX PRO 6000 ($1.84/h): text adapters 8–9 h (stage 1, $14), a chat adapter about 1.6 h, setup about 1.5 h per lease, about 20 min per graft cell evaluated. Scaling: 4× active parameters on 4× the GPUs gives about the same wall-clock if the code splits the experts across GPUs; I have not tested that, so I double it.

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
