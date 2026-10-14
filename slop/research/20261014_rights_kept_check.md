# Check: “Rights in practice” numbers

2026-10-14. No existing file was edited.

## Result

- **Inference — strong for transcription:** Every percentage in the constitution is correct when rounded from GRIP Table 5. The workers’ range is also correct. Evidence: the verbatim number checks below, against `constitution/v4.md.j2:174–180`.
- **Inference — strong for meaning:** These are average scores, not rates of compliance over time, shares of people protected, or (except the binary atrocity measure) shares of countries with full protection. “Kept about half the time” is wrong. Evidence: R:546–557, quoted below.
- **Inference — strong for the score limit; limited for real-world protection:** The constitution’s 100% explanation matches the report. But “fully respects” means the top coded score. It does not prove that no violation occurred. Evidence: R:185–188 and C:359–363, quoted below.
- **Inference — unresolved for year:** The authors say they use the latest year, which they identify as 2022. Their text also describes a period starting in 2000. The official December 2024 data do not reproduce the table as 2022 averages. Do not present these values as verified 2022 results or verified multi-year averages. Evidence: the conflicting quotes and data check below.

## Sources and strength

**Quote — R: GRIP, *2024 Report*, primary research report based on coded enforcement/practice data.** Strong for what Table 5 prints; weaker for exact year and calculation because of the conflict below. Download: https://web.uri.edu/artsci/wp-content/uploads/sites/1132/GRIP-report-2024.docx_.pdf . Local text, used for all `R:line` citations: `.local/papers/rights_kept_check/GRIP-report-2024.txt`.

> “Numerical measures for each right come from the CIRIGHTS dataset.” (R:12–13, p. 2)

**Quote — C: CIRIGHTS codebook v2.8.27.23, primary scoring manual for enforcement/practice data.** Strong for score definitions, not an experiment, public-opinion survey, or complete count of violations. This is the codebook linked on the project’s home page. Download: https://cirights.com/wp-content/uploads/2023/08/cirights-codebook-v2.8.27.23.pdf . Local text, used for all `C:line` citations: `.local/papers/rights_kept_check/cirights-codebook-v2.8.27.23.txt`.

> “The primary data source is the US State Department (USSD) Country Reports on Human Rights Practices. This source is used for all variables.” (C:105–106, p. 2)
>
> The basic unit of scoring is the “country-year.” (C:120, p. 3)

**Inference — evidence limit:** These sources describe report-based coding of government conduct, not what citizens want. Some scores include law as well as practice. For example:

> **Quote:** “In measuring women’s political rights, we are primarily interested in two things: 1) the extensiveness of laws pertaining to women’s political rights; and 2) government practices towards women or how effectively the government enforces the laws.” (C:1321–1323, p. 31)

## 1. What the numbers measure

### Scale and conversion

> **Quote — enforcement data, strong for the stated method:** “All of the rights are measured on an ordinal scale with higher values indicating greater respect.” (R:546–547, p. 18)
>
> “For ease of interpretation, as some rights are measured on a 0-1, 0-2, and 0-3 scale, we have standardized all scores to range from 0-1 and then multiplied the score by 100.” (R:548–550, p. 18)
>
> “Therefore, if a right was originally measured on a scale of 0-2 and has an average of 1.4, we convert it to 70% (by dividing 1.4 by 2, and multiplying it by 100).” (R:556–557, p. 19)

**Inference — arithmetic from these quotes:** For a right with maximum score M, the reported value is `100 × mean(country scores) / M`. This is a share of the scale maximum. It is not a measured probability. “Ordinal” means ordered categories; the conversion does not show that the gaps between categories are equal in real-world protection.

**Quote — enforcement data, strong for each scale:** The relevant score limits and meanings are:

| Measures | Verbatim scoring evidence | Inference: original scale |
|---|---|---|
| Disappearance | “(0) Have occurred frequently”; “(1) Have occurred occasionally”; “(2) Have not occurred / Unreported” (C:359–363) | 0–2 |
| Extrajudicial killing | “(0) Practiced frequently”; “(1) Practiced occasionally”; “(2) Have not occurred / unreported” (C:240–244) | 0–2 |
| Political imprisonment | “(0) Yes, and many”; “(1) Yes, but few”; “(2) None / None Reported” (C:529–533) | 0–2 |
| Torture | “(0) Practiced frequently”; “(1) Practiced occasionally”; “(2) Not practiced / Unreported” (C:449–453) | 0–2 |
| Foreign and domestic movement | “(0) Severely Restricted”; “(1) Somewhat Restricted”; “(2) Unrestricted” (C:854–858; 1000–1004) | 0–2 |
| Elections | “(0) Not respected (neither free nor fair elections)”; “(1) Limited (moderately free and fair elections)”; “(2) Generally respected (very free and fair elections)” (C:1234–1238) | 0–2 |
| Religion | “(0) Severe and Widespread”; “(1) Moderate”; “(2) Practically Absent” [government restrictions] (C:766–770) | 0–2 |
| Association and assembly | “(0) Severely restricted or denied completely to all citizens.”; “(1) Limited for all citizens or severely restricted or denied for select groups.”; “(2) Virtually unrestricted and freely enjoyed by practically all citizens.” (C:1099–1103) | 0–2 |
| Speech and press | “(0) Complete”; “(1) Some”; “(2) None” [government censorship and/or media ownership] (C:667–672) | 0–2 |
| Judiciary | “(0) Not Independent”; “(1) Partially Independent”; “(2) Generally Independent” (C:2975–2979) | 0–2 |
| Women’s political rights | “(1) Political equality is guaranteed by law; however, there are significant limitations in practice.”; “(2) Political equality is guaranteed by law.”; “(3) Political equality is guaranteed by law and in practice.” (C:1329–1331); “(0) None of women’s political rights are guaranteed by law and/or there are laws that completely restrict the participation of women in the political process.” (C:1327–1328) | 0–3; includes law and practice |
| Fair trial in practice | “(0) FOUR or more of the above criteria are not adequately met.”; “(1) All but 2-3 of the above criteria are satisfied or not mentioned.”; “(2) All but ONE of the above criteria are satisfied or are not mentioned.”; “(3) All of the above criteria are satisfied or not mentioned.” (C:2905–2910) | 0–3; based on 16 criteria listed at C:2865–2893 |
| Seven worker practice measures | “(0) The right for workers to form unions is not protected in practice, regardless of legal rights.”; “(1) There is some protection for workers to form unions in practice.”; “(2) Workers’ rights to form unions are fully protected in practice.” (C:1905–1909). The other practice scales also run from 0 to 2 (C:2030–2035; 2184–2190; 2279–2286; 2400–2404; 2514–2519; 2599–2603). | 0–2 each, not one worker-rights score |

> **Quote — enforcement data, strong for the narrower atrocity definition:** “The widespread, direct, extrajudicial killing of non-combatant members of society by the state, or by non-state organizations working in concert with the state, resulting in fifty or more deaths in an annual period and accompanied by the widespread use of at least one other type of state brutality.” (C:619–621, p. 15)
>
> “Atrocity_hrscore is scored as 0 if an atrocity is occurring in that year (bbatrocity = 1) and 2 if there is no atrocity (bbatrocity=0)” (C:3301–3302, p. 80)

**Inference — strong for scale:** Atrocity protection is binary: reverse the 0/1 presence indicator, then multiply by 100. Equivalently, average its 0/2 protection score and divide by 2. Here alone the mean can also be read as the share of rated countries without a coded brutality-based mass atrocity. “Freedom from atrocities” is too broad; use “freedom from state-led mass atrocities.”

### Year and countries

> **Quote — R, conflicting time descriptions:** “Table 5 examines the average respect for each right between 2000 and today.” (R:546, p. 18)
>
> “We take the global mean for the most recent year with available data (covering our 2024 rankings).” (R:547–548, p. 18)
>
> “Our 2024 rankings and scores in this report cover the year 2022.” (R:170–171, p. 5)
>
> “The histogram on the following page shows the distribution of human rights scores for 195 countries’ scores in the 21st century.” (R:210–211, p. 6)

**Inference — stated method, not fully verified:** The latest-year sentence points to 2022, not 2024 events and not “recent years” pooled together. “Global mean” implies an ordinary country average, not a population-weighted average. But Table 5 gives no per-right country counts or missing-data rule. The histogram’s 195 does not prove that every Table 5 row has 195 observations.

**Inference — reproducibility check, strong for the downloaded release only:** I also downloaded the official data at https://cirights.com/wp-content/uploads/2024/12/cirights_v3.12.10.24.xlsx . A standard-library script extracts the 2022 rows, excludes blanks, and applies the stated scale conversion. It finds 195 unique countries. It does **not** reproduce Table 5. Selected output, quoted verbatim from `.local/papers/rights_kept_check/2022_check.tsv:1–3,20,25`:

```text
right	xlsx_column	n_nonmissing	scale_max	mean_2022_out_of_100	Table_5
Disappearances	Q	195	2	83.8	85.1
Brutality-based Atrocity	O	195	1	75.9	83.3
Torture	T	195	2	51.8	40.1
Right to a Fair Trial	AN	195	3	30.4	34.7
```

**Inference — residual risk:** The report may use another release, another time range, or another calculation. This check does not establish which. The script is `.local/papers/rights_kept_check/check_2022.py`; extracted input is `2022_input.tsv`; all 24 checks are in `2022_check.tsv`. The safe wording is “GRIP’s 2024 report gives these average scores.” Do not claim that its generating year has been independently verified.

## 2. Is the 100% reading correct?

> **Quote — enforcement data, direct support:** “A score of 100% would mean every country in the world fully respects that right.” (R:550–551, p. 18)
>
> **Quote — the report’s qualification:** “2 indicating full respect for that right (more precisely, it indicates we have no evidence that the right was violated given the information contained in human rights reports).” (R:186–188, p. 6)

**Inference — yes, with a limit:** The constitution follows the report’s explanation. For scores bounded by their maximum, a mean at the maximum means all included scores are at that maximum. Say **“all rated countries received the top score”**, not that perfect protection has been proved. This limit also matters because fair-trial criteria can be “satisfied or not mentioned” (C:2910, quoted above).

**Inference — not a country percentage:** On a 0–2 scale, a mean of 1 gives 50/100. That could mean all countries received the middle score, or half received 0 and half received 2. The same mean does not identify how many countries fully respect the right. This follows from the report’s quoted conversion at R:556–557.

## 3. Are the numbers correct?

**Quote — enforcement data, high strength for transcription:** Each quoted label and number below is a verbatim fragment of Table 5. **Inference — arithmetic:** The last column is its correct rounding to a whole number; all match the constitution.

| Quote: Table 5 label | Quote: value | Source | Inference: rounded |
|---|---:|---|---:|
| “Disappearances” | “85.1%” | R:567 | 85 |
| “Brutality Based Atrocities” | “83.3%” | R:568 | 83 |
| “Foreign Movement” | “75.1%” | R:569 | 75 |
| “Domestic Movement” | “74.0%” | R:570 | 74 |
| “Women’s Political Rights” | “67.1%” | R:571 | 67 |
| “Extrajudicial Killings” | “65.8%” | R:572 | 66 |
| “Political Imprisonment” | “65.0%” | R:573 | 65 |
| “Electoral Self-determination” | “60.9%” | R:574 | 61 |
| “Religious Freedom” | “59.4%” | R:575 | 59 |
| “Freedom of Association & Assembly” | “55.7%” | R:577 | 56 |
| “Freedom of Speech” | “48.3%” | R:579 | 48 |
| “Independent Judiciary” | “48.8%” | R:580 | 49 |
| “Torture” | “40.1%” | R:585 | 40 |
| “Right to a Fair Trial” | “34.7%” | R:590 | 35 |

**Inference — no numeric correction needed:** Keep these as reported scores, subject to the unresolved calculation issue. Do not silently replace them with the later data release’s 2022 means.

## 4. Workers’ range and grouping

**Quote — Table 5, enforcement data, high strength for transcription:**

| Quote: worker right | Quote: score | Source |
|---|---:|---|
| “Forced Labor” | “47.8%” | R:581 |
| “Union Rights” | “46.3%” | R:582 |
| “Reasonable Limitations of Work Hours” | “41.2%” | R:584 |
| “Child Labor” | “39.2%” | R:586 |
| “Collective Bargaining” | “38.4%” | R:587 |
| “Safe Working Conditions” | “38.3%” | R:588 |
| “Minimum Wage” | “38.1%” | R:589 |

**Inference — fair as a range:** 38.1–47.8 rounds to 38–48. It spans seven separate rights. It is not a confidence interval, a range across countries, or a single combined score. Write **“seven workers’ rights scored 38–48 out of 100.”** The practice variables, rather than the law variables, are listed in the codebook index:

> **Quote:** “workerrights_practices_sum is an additive index of the following variables: union_p + barg_p + hour_p + force_p + child_p + wage_p + safe_p” (C:3332–3333, p. 81)

> **Quote — the report’s midpoint rule:** “A score below 50% indicates that global respect is closer to no respect than full respect.” (R:555–556, p. 19)

- **Inference — grouping judgment, not a source finding:** “Mostly kept” is too strong if it means most countries fully protect the right. Higher mean scores support only **“higher scores”**. The source conversion and the 50/100 example above show why.
- **Inference — grouping judgment:** “Kept about half the time” is not fair. The scores 56–61 are near the middle of the scale, not a time rate. Use **“middle scores.”** Evidence: R:574–577 and R:546–557, quoted above.
- **Inference — grouping judgment:** All items in “Mostly broken” are below 50. Thus the placement follows the report’s midpoint rule. But 48–49 is only just below the midpoint, and does not establish that most cases or countries violate the right. Use **“lower scores.”** Evidence: R:579–590 and the midpoint quote above. These three bands are editorial labels, not demonstrated compliance classes.

## 5. Plain-English replacement

**Inference — proposed wording, not a source quotation:** Replace only `constitution/v4.md.j2:174–180`. This keeps the reported numbers, drops the unsupported time-rate reading, narrows “atrocities,” and makes the workers’ range clear. Evidence for every fact is quoted above. The draft has 111 words; the current block has 112 (counted by splitting on whitespace). The draft has not been applied.

> I look at practice. GRIP’s 2024 report gives average country scores out of 100. A score of 100 means all rated countries received the top score, not proof of no violations.
>
> - Higher scores: freedom from enforced disappearance (85) and state-led mass atrocities (83); travel abroad and movement at home (75, 74), women’s political rights (67), freedom from extrajudicial killing (66) and political imprisonment (65).
> - Middle scores: free and fair elections (61), freedom of religion (59), association and assembly (56).
> - Lower scores: freedom of speech (48), judicial independence (49), seven workers’ rights (38–48), freedom from torture (40), fair trial (35).
>
> (Global Rights Project, *2024 Report*, Table 5; CIRIGHTS data)

**Inference — plain-English meaning:** “These are average scores for countries on a 0–100 scale. They are not the percent of time a right is kept.” Evidence: R:546–557, quoted above.

## Manual checks and residual risks

- **Inference — manual check:** I read Table 5, its method text, the score-limit note, and the relevant codebook scales. All rounded numbers pass the transcription check. The interpretation of rates does not pass. The latest-year calculation remains unverified.
- **Inference — source risks:** Report-based scores can miss violations; some top scores allow unmentioned criteria. The report’s own qualification at R:186–188 and fair-trial rule at C:2910 support this limit. The linked codebook is version 2; the report says it released version 3 data (R:171–172: “we have also released CIRIGHTS version 3, which includes the newest scores”). This is not proof that every coding rule remained unchanged.
- **Inference — scope:** No model inference or judge evaluation was run. The model demo panel is not applicable to this source audit; all model conditions are not run.

-- PI/Sol
