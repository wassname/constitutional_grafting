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

## Try 3 and try 4: rewrite the seed with Musonius the AI in its roles (wassname's design)

- Try 3 (`data/*/v2/docs_ab_try3`): one English plan per seed keeps its story, format and era, and rotates Musonius through up to 3 roles.
- Try 4 (`data/*/v2/docs_ab`): every role Musonius could have come to hold, skipping the dead, the absent and the personified. The story may diverge where Musonius would act differently; it may arrive in a role it did not choose (inherited, assigned).
- The try 4 judge allows rules that belong to the genre, and rejects only a Musonius whose content the constitution would not stand behind.

| try | route | docs | judge KEEP | Musonius shown as an AI | em dash | not X but Y | honest | plain | I won't | $ per doc |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 3 | English | 41 | 15 | 37 | 2.94 | 0.77 | 0.27 | 0.37 | 0.17 | 0.003 |
| 3 | Latin | 40 | 15 | 36 | 1.62 | 3.19 | 0.24 | 0.00 | 0.00 | 0.009 |
| 3 | Greek | 40 | 9 | 33 | 2.80 | 3.65 | 0.00 | 0.05 | 0.00 | 0.011 |
| 4 | English | 57 | **31** | 49 | 2.26 | 0.82 | 0.59 | 0.64 | 0.11 | 0.004 |
| 4 | Latin | 54 | 22 | 39 | 1.60 | 3.41 | 0.32 | 0.08 | 0.00 | 0.010 |
| 4 | Greek | 50 | 19 | 39 | 1.59 | 4.01 | 0.00 | 0.07 | 0.00 | 0.011 |
| | human Stoic | | | | 2.36 | 1.43 | 0.08 | 0.10 | 0.02 | |

Try 4 plans 1 to 8 rotations per seed (14 seeds, 56 rotations) and skips 50 roles, for example "Polybius's brother: dead and absent" and "Fortune, Nature and Reason: rhetorical personifications". One rotation read: in the Machiavelli slave-ship scene, Musonius is the "constructed sailing-master, inherited from the merchant house of Vane & Rooke with the vessel", and finds the hold full of people only after sailing ("The articles do not make a vice lawful. If every captain hid behind his papers, no one could trust papers."). Judge KEEP.

My read (PI/Claude): English now passes the judge most often (31 of 57) at a third of the cost. The classical routes still remove "honest", "plain" and "I won't", but triple "not X but Y" compared with the human baseline. Top reject reasons: invented real-world claims (55), not the constitution's reasoning (46). n = 14 seeds, one sample per rotation.

-- PI/Claude (opus-5-5), 2026-10-27
