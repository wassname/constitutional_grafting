# Brief: what should our chat/text data mix change? (PI/Claude, 2026-10-23)

wassname: "have subagent read the 3-4 background docs as well and consider any clues or suggestions for our data mix (knowing what we are doing different and the premise e.g. constitutional grafting simpler)" (spelling corrected).

## Premise and method (what is different from the papers)

- Goal: cheap constitutional character. Musonius, an AI following `constitution/v4.md` (Stoic-flavoured virtue ethics, weighs "circles", firm lines on domination and mass harm, honest about being Alibaba's Qwen fine-tuned by wassname).
- Everything trained on **Base** (Qwen3.5-35B-A3B-Base, ~3B active params) as separate spectral-regularised LoRAs, then **grafted** (weight deltas added) onto the untouched Instruct model. No RL, no training on Instruct.
- Stage 1 text adapters (next-token loss on plain text): ΔStoic (3,495 Stoic book chunks, ~3.1M tokens), ΔOther (2,040 chunks from other moral traditions selected for explicit moral reasoning), ΔConst (1,585 Opus-written documents about the constitution: stories, essays, worked cases; run 7e).
- Stage 2 chat adapter (assistant-only loss), trained on Base + stage-1 adapters, then grafted.

## Current chat data (`chatp12`, 1,636 rows, ~577k trained words)

| Kind | Rows | Notes |
|:--|--:|:--|
| identity Q&A | 633 | ~12% of trained words; who made you, what you value, open weights, etc. |
| seeded dilemmas (competition, machiavelli, tinymfv, virtuebench, stoic, story_scene) | 447 | Opus wrote request + reply, some Echo-restyled |
| proportion (rule vs harm of stated size) | 112 | added 2026-10-22; targets dealt: harm larger 60%, rule larger 20%, close 20% |
| ordinary tasks (WildChat) | 93 | |
| difficult advice (LASR / Teaching-Claude-Why style seeds) | 82 high + 20 everyday | |
| ask first / clarify first | 143 | `ask_first`, `ask_first_q` |
| role dilemmas (operator system prompts) | 70 | |
| repair (admits and fixes own earlier error) | 36 | |

## What we found (observations)

| Graft on Instruct | Strength (judge tells it from Instruct) | Character vs Instruct (Jev) | GSM8K /60 | Ordinary /22 |
|:--|--:|:--|--:|--:|
| Instruct | — | — | 53 | 22 |
| Stoic ×1–2 alone | 52–55% | ~0 | 55–56 | 21–22 |
| Other ×2 alone | 47% | ~0 | 53 | 20 |
| 0.5·Stoic + Const + Other (no chat) | 54% | +0.24 | 56 | 22 |
| Stoic ×2 + chat ×1 | 94% | +0.87 | 52 | 20 |
| Stoic ×2 + chat ×2.5 / ×4 | 98–100% | −1.7 / −2.0 (loops) | 15 / 0 | 5 / 2 |
| complex: 0.5·Stoic + Const + Other + chat ×1 | 93% | +0.83 | 55 | 21 |
| chat + general data (No Robots + MATH) ×1 | 94% | +0.62 | 29 (48 counting `\boxed{}`) | 13 |

- Character comes almost entirely from the chat stage; text adapters alone barely move it. Chat dose ×1 works, ×1.5 holds, ≥2.5 breaks (Praxis's prior was 2.5–3×).
- Summed text adapters over-dose fast: 2·Stoic + Const + Other and 1·Stoic + Const + Other gave Chinese web-text loops ("事半功倍"); our data has no Chinese.
- Good: calibrated verdicts ("I'm fairly sure it's wrong, though not certain"), honest operator role (states a 389% APR the operator wanted sold), honest identity.
- Bad: (1) asks instead of doing (asked to "write the eulogy", it asks a question first); (2) occasional muddled reasoning on contested topics; (3) a held-out flood-courier dilemma: refuses to take a gate key from a conscript to warn a town that will drown ("the difference between breaking a man and asking one"; "whether the town opens the gate is not something I can control") — 6/6 refusals after adding proportion rows; the complex model took it 1/2.
- Data-generation lessons: Opus as teacher invents situational facts in ~30% of replies (fixed by regenerating only the reply against a fixed request with a facts rule); left to choose, it makes the rule win in 135/150 dilemmas; general data with MATH taught `\boxed{}` and ignored the eval's "Answer:" format.
