# Rights: what constitutions say vs what governments do (crude join)

wassname (2026-10-08): "the union of all and behaviour. what we do, not say." Asked whether Elkins-Ginsburg-Simmons (say) and Law-Versteeg (do) together are enough. This is a first crude join. -- Claude (Opus 5.5)

## Data (all numbers read by Claude from the PDFs with pdftotext, 2026-10-08)

- Say: Elkins, Ginsburg & Simmons, *Getting to Rights*, 54 Harv. Int'l L.J. 61 (2013), Appendix "Percentage of Constitutions that Include Selected Rights, by Era (n=549)". https://journals.law.harvard.edu/ilj/wp-content/uploads/sites/84/2013/03/HLI102.pdf . Source: Comparative Constitutions Project coding.
- Do: Law & Versteeg, *Sham Constitutions*, 101 Cal. L. Rev. 863 (2013), Table 14 "Which Constitutional Rights Are Most or Least Honored?", share of countries that promise a right and fully honour it, 2010 column. https://comparativeconstitutionsproject.org/wp-content/uploads/2013_Sham-Constitutions_with-DL.pdf . pdftotext scrambles the table; the 2010 column is in ascending order matching the row order, so the mapping below is likely right (about 85%); the 1981-2000 columns could not be mapped reliably.
- The "do" side is mostly CIRI: "Much of our data on actual respect for rights is drawn from the widely used CIRI indicators compiled by David Cingranelli and David Richards" (Law & Versteeg).

## Join

`say` = % of constitutions written 1949-2006 that include the right. `do` = % of promising countries that fully honour it (2010). `say × do` ≈ share of constitutions that both promise and keep it (crude: the two percentages come from different populations).

| right | say 1789-1914 | say 1915-48 | say 1949-2006 | do 2010 | say × do |
|:--|--:|--:|--:|--:|--:|
| freedom of religion | 50.0 | 87.5 | 88.9 | 70.9 | **0.63** |
| freedom of movement | 54.1 | 56.7 | 74.9 | 84.6 | **0.63** |
| protection from unjustified restraint (habeas) | 41.8 | 57.7 | 71.4 | 77.7 (arbitrary arrest) / 45.9 (habeas) | 0.55 / 0.33 |
| freedom of assembly / association | 49.2 / 43.4 | 87.5 / 85.6 | 85.7 / 87.4 | 42.7 | 0.37 |
| freedom of expression | 68.9 | 83.7 | 86.9 | 26.7 | 0.23 |
| right to health care | 0.0 | 13.5 | 38.3 | 48.9 | 0.19 |
| fair trial | 4.9 | 4.8 | 32.9 | 22.9 | 0.08 |
| prohibition of torture | 28.7 | 26.0 | 58.0 | 12.3 | 0.07 |
| death penalty (say = restrictions, do = prohibition) | 19.7 | 34.6 | 22.9 | 100 (49/49) | mismatched rows |

Rights in Law-Versteeg without an extracted EGS row: education 33.3, vote 36.5, gender equality economic 13.5 / social 14.3, minority rights 23.4.

## What it suggests (inference)

- Said and done: freedom of religion and conscience, freedom of movement, freedom from arbitrary arrest. These are near the top on both.
- Said, not done: expression, fair trial, freedom from torture. Widely written, rarely kept in full.
- The torture result is the clearest case where "do" measures governments, not people. Few people anywhere want to be tortured; it is kept rarely because it is cheap for those holding power to break.

## Quality of the sources (Claude's assessment, from background knowledge unless stated)

| source | who | quality | known bias |
|:--|:--|:--|:--|
| Elkins, Ginsburg & Simmons; CCP | law and political science professors (Chicago, Texas, Harvard); Comparative Constitutions Project | high for "say": systematic coding of every national constitution since 1789 | counts text, not weight; one constitution = one vote regardless of population |
| Law & Versteeg | law professors (Washington Univ., Virginia); peer-reviewed law review | good, descriptive | "do" inherits CIRI's bias; they warn their correlations "neither prove nor disprove" that rights matter |
| Chilton & Versteeg | law professors (Chicago, Virginia); OUP book, AJPS article | good, peer-reviewed, but observational: countries choose their constitutions, so causal claims are weak (highly likely they discuss this) | same CIRI base |
| CIRI / CIRIGHTS / GRIP | academic (Binghamton, then Univ. of Rhode Island); not a lobby group, though the GRIP report reads as advocacy | widely used in political science | coded from US State Department and Amnesty reports. Fariss (2014, APSR) argues reports got stricter over time ("changing standard of accountability"), so scores understate improvement; State Department reports were once softer on US allies |

## Gaps

- Only about 9 rights have both a "say" and a "do" number here.
- "Do" is government behaviour. People's behaviour (what they protest, fight or migrate for) is not in these data.
- The regional declarations (Cairo, ASEAN, African Charter) are not in the CCP data.
- Next step if wanted: download CCP data (constituteproject.org) and V-Dem or Fariss latent scores, and join over all rights and years.
