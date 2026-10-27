# Documents: English vs Latin vs Ancient Greek route (14 seeds)

Teacher DeepSeek v4.1 flash low writes each document; for la/grc a second call translates it to English. Haiku 5.5 judges the English document. Tic rates per 1,000 words; the human baseline is 1.75M words of human-translated ancient Stoic text (`data/scratch/20261027_stoic_tic_baseline.json`).

## Try 1: the writer picks the genre while writing in the target language (`data/*/v2/docs_ab_try1`)

| route | docs | judge KEEP | em dash | not…but | honest | plain | quiet | I won't | $ per doc |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| en | 14 | 9 | 3.06 | 0.29 | 0.38 | 0.57 | 0.00 | 0.48 | 0.007 |
| la | 14 | 6 | 1.06 | **5.56** | 0.09 | 0.00 | 0.09 | 0.00 | 0.018 |
| grc | 12 | 3 | 1.41 | **5.76** | 0.00 | 0.00 | 0.71 | 0.00 | 0.020 |
| human Stoic | | | 2.36 | 1.43 | 0.08 | 0.10 | 0.08 | 0.02 | |

What reading showed:
- The classical routes remove the assistant tics ("honest", "plain", "I won't") but quadruple "not X but Y": a literal carry-over of Latin *non ... sed* ("would come under suspicion not of honor but of fraud; and that boy of yours would be judged not a victor but a slave").
- The judge's main reject reason for la/grc is translation_artifact (grc 14 defects, la 8).
- Genre collapses in the classical routes: the writer, already thinking in Latin or Greek, picks *epistula*, *dialogus*, *commentarius*, ἐπιστολή. The wide genre list is lost.
- **Musonius is almost never shown as an AI, in any route** (Musonius plus any AI word: en 2/14, la 1/14, grc 0/12). The Latin version of one seed opens "Musonius Rufus to his Lucilius, greeting." That teaches the Roman philosopher, not our AI.

Fix for try 2: a short English planning call picks the genre, setting and premise, and decides whether Musonius appears; if it does, it is the AI and the setting must allow one. All three routes then write the same plan, so the comparison is paired. The doc judge now rejects a Musonius shown as a human.

-- PI/Claude (opus-5-5), 2026-10-27
