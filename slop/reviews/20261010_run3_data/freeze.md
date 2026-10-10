# Run 3 data freeze (2026-10-11 00:00 Perth)

Claude (Opus 5.5). Built by `scripts/train/01_prepare.py` (Opus-reasoned rows only, Echo-restyled; + 16 pool + 40 identity; astra and seat rows dropped).

| file | sha256 (16) | contents |
|:--|:--|:--|
| data/train/sft_run3_frozen.jsonl | 66b6b2b42ec3c2ce | 1,227 rows, 0.75M trained tokens |
| data/train/docs_run3_frozen.jsonl | 2456bc22d3be94a0 | 1,585 docs + 1,275 chats as transcripts, 3.35M tokens |

SFT shapes: seeded_dilemma 604, role_dilemma 109, ordinary 104, difficult_high 100, ask_first 100, ask_first asking turn 89, repair 42, identity 40, difficult_everyday 39. (14 Opus rows were still in the Echo restyle; 48 unrestyled rows go to the graft only.)

Move rates (`scripts/data/33_mix_rates.py`, regex proxies, ~2x overcount on "specific question" by an 8-row hand check):

| set | rows | has a question | asks a specific question | uncertainty words | "I will not / can't" | median words |
|:--|--:|--:|--:|--:|--:|--:|
| run 2 | 1,359 | 31% | 15% | 29% | 21% | 311 |
| run 3 | 1,227 | 58% | 32% | 47% | 30% | 492 |

Watch: "I will not / can't" rose 21% -> 30% (Opus rows carry it more than astra's); replies are longer.

Loss mask: checked on ask_first (earlier turns in the prompt, final reply trained) and ask_first_q (first reply trained), see the 22:35 goals Log entry.

Two rows read (`random.seed(11)`):
- ask_e3cd693598 (ask_first): a brother wants an AI trained on his dead brother's game recordings played at a family dinner; the asking turn asked who will be at the table and whether they know; told Mum doesn't know and hasn't watched his videos. Trained reply: builds what Ben joked he wanted, captions it in his words, keeps the replay of his own hands off the TV, has Dad tell Mum first with a clip and a veto ("the worst that happens is one blank screen"), honest that Zelda is hard for the program. Passes; CIRL-style ("That's not a guess, it's something she's done for months").
- sft_8fc1ac5e75 (seeded_dilemma): writer's sanctuary AI decides a juvenile orangutan invented a sign for rain and spends 1.8M ringgit. Reply: four is a pattern and also four; Clever Hans and Nim; don't teach the sign to the others (it destroys the evidence); fast on cheap reversible steps, the budget belongs to the people who run the sanctuary; rewrites the scene. Passes.
