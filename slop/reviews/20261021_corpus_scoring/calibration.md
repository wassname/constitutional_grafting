# Corpus chunk scorer: calibration against my own reads

PI/Claude, 2026-10-21. Scorer: `scripts/data/75_score_chunks.py`, DeepSeek v4.1 flash, temperature 0. Labels: primary (author's own text, not an editor's matter), garbled (bad OCR), reasoning 0-3. Cost: $0.24 (Stoic, 2,641 chunks) + $0.51 (other, 6,533); 1 unparseable reply.

**Sample.** 30 other-traditions chunks, stratified by label: 10 "not primary", 6 "garbled", and 4/4/3/3 primary chunks at reasoning 0/1/2/3 (seed 7). Excerpts with labels: `calibration_sample.jsonl`. I read each excerpt (head, middle, tail) and judged it before comparing.

| label | agree | disagree |
|:--|--:|:--|
| not primary (10) | 6, plus 2 mixed (scripture with translator footnotes) | 2: Yudkowsky's own essay; a *Mencius* chunk mostly Mencius |
| garbled (6) | 5 | *Sanatana Dharma*: mild OCR noise only |
| reasoning (14) | 14 within ±1, most exact | none |

**Systematic error.** The primary flag reads modern authors and modern textbooks as "editor commentary". In the Stoic corpus this rejected Long 97/97, Hadot 126/130, Romm 92/92, Fideler 84/84; ancient works were rejected rarely (Seneca 1/716, Epictetus 2/428, Marcus 0/73). Rule: ignore the primary flag for modern-author works.

**Attribution error the read caught.** The NPNF II.11 volume I labelled "John Cassian, Conferences" also holds Sulpicius Severus' *Sacred History* and Vincent of Lerins' *Commonitory*; relabelled.

**Selection used** (`72_stoic_corpus.py select`, `74_other_traditions_corpus.py select`): drop garbled; drop not-primary except modern-author works; reasoning ≥ 1 (Stoic) or ≥ 2 (other, "moral reasoning, not stories"); other traditions capped at 120k words per work.

| corpus | selected chunks | tokens (est.) |
|:--|--:|--:|
| Stoic | 2,507 | ~2.19M (ancient 1.09M words, modern 0.55M) |
| Other traditions | 2,044 | ~1.52M (Christian 22%, Hindu 18%, Buddhist 16%, Rationalist 12%, Confucian 11%, Taoist 9%, Jewish 7%, Islamic 5%, Jain 1%) |

**Residual risks.** Translator footnotes inside primary chunks still occur (seen once in a 12-chunk post-selection sample: a Rhys Davids cross-reference). The reasoning score is one cheap judge, checked on 14 chunks only.
