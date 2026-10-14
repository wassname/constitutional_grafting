# CIRI / CIRIGHTS: criticism, validation, and use in the constitution

2026-10-14. Research only. Read `AGENTS.md` first and both requested prior reports. No existing repository file edited. Downloads and extracts: `.local/papers/ciri_criticism_20261014/`.

## Result

**Inference — recommendation:** CIRIGHTS is a credible academic source for **reported government respect for specified rights**, with significant measurement limits. It is not a direct measure of citizens’ values, a census of violations, or a percentage of occasions on which a right is respected. Keep a qualified reference if useful; **do not restore the old percentage list as written**. Its calculation remains unreproduced in the prior audit, and its interpretation as compliance frequency was wrong.

**Inference — important new findings:** The current project’s own journal article acknowledges reporting bias and changing standards. Historical CIRI’s reported coder reliability excludes some actual disagreements. GRIP’s acknowledged supporters include an apparent political donor connection: Shannon Chandley, a former Democratic state senator and now New Hampshire Democratic Party finance chair. That is a disclosure issue, **not evidence of manipulated scores**.

**Labels:** Blockquotes are **quotes**; interpretation, strength ratings, and recommendations are **inferences**. Strong = direct evidence for the narrow claim; moderate = indirect evidence, contested assumptions, or limited generalization; weak = an inference broader than the evidence. None is a probability. PDF whitespace and line-wrap hyphenation are normalized; quotations are otherwise verbatim. An accessible abstract is not described as a full-text audit.

## 1. Published disputes and replies

### A. Country / ally bias: Poe, Carey & Vazquez (2001)

*How Are These Pictures Different? A Quantitative Comparison of the US State Department and Amnesty International Human Rights Reports, 1976–1995*, **Human Rights Quarterly 23:650–677**, [DOI](https://doi.org/10.1353/hrq.2001.0041).

**Source type / strength:** Peer-reviewed comparison of report-derived ratings. The original full text was blocked at Project MUSE and Mannheim. **Moderate** here: findings verified through subsequent full-text scholarly discussions, not a fresh inspection of the original regressions. This predates CIRIGHTS and does not estimate current bias.

**Quote — Cordell et al. (2020), p. 5, citing Poe et al.:**

> “However, there is also significant evidence that these reports, although becoming more detailed, were also biased in favor of US allies during this period (Poe et al. 2001).”

[Full text](http://cfariss.com/documents/CordellClayFarissWoodWright2020JHR.pdf), `cordell.txt:206–209`. The period discussed is the Reagan administration. The next page reports declining State Department–Amnesty score differences after the Cold War (`:225–229`).

**Quote — historical CIRI FAQ, the project’s defense:**

> “If there are discrepancies between the two sources, coders are instructed to treat the Amnesty International evaluation as authoritative.”

[FAQ](http://www.humanrightsdata.com/p/faq.html), `ciri_faq.txt:51`.

**Inference — what is disputed / does the defense work?** Historical US foreign-policy favoritism is a real concern; it is not grounds for assuming every present score is propaganda. Greater later agreement and Amnesty priority are meaningful safeguards for physical-integrity rights. They do **not** prove neutrality: agreement can reflect common sources, and Amnesty is not used equivalently for every right. I do not assert an ally-bias coefficient or its current size without the original paper and a contemporary replication.

### B. A counterweight: Bagozzi & Berliner (2018)

*The Politics of Scrutiny in Human Rights Monitoring*, **Political Science Research and Methods 6:661–677**, [DOI](https://doi.org/10.1017/psrm.2016.44).

**Source type / strength:** Peer-reviewed text analysis of 6,298 State Department reports, 1977–2012; publisher abstract inspected, not full regression tables. **Moderate** for the reported findings.

**Quote — publisher abstract:**

> “We also find that while US domestic politics play no systematic role in shaping topic prevalence, US allies tend to receive more attention to violations of physical integrity rights.”

[Publisher](https://www.cambridge.org/core/journals/political-science-research-and-methods/article/abs/politics-of-scrutiny-in-human-rights-monitoring-evidence-from-structural-topic-models-of-us-state-department-human-rights-reports/D8B62D46D081CD30CEC962486786683C), `bagozzi_abstract.txt:453`.

**Inference — assessment:** This challenges a simple, timeless “allies are always spared” account. More attention is not necessarily harsher scoring: attention, wording, and assessments are different outcomes. It also cannot refute later partisan shifts outside its observation period. The defensible conclusion is **variable organizational attention**, not a universal ally discount or universal impartiality.

### C. Reporting changes with administrations: Cordell et al. (2020)

*Changing Standards or Political Whim? Evaluating Changes in the Content of US State Department Human Rights Reports Following Presidential Transitions*, **Journal of Human Rights 19:3–18**, [DOI](https://doi.org/10.1080/14754835.2019.1671175).

**Source type / strength:** Peer-reviewed original text analysis, reports covering 1980–2017; relevant methods and findings inspected. **Strong** that coverage changed; **moderate** for attributing every change to presidential ideology or its effect on final scores.

**Quote — p. 10:**

> “However, the reports decreased significantly in length by 14 percent during the transition from the Obama administration to the Trump administration, in line with a negative shift in human rights preferences (Girard 2017; Shear and Savage 2017; Lopez 2018).”

[Full text](http://cfariss.com/documents/CordellClayFarissWoodWright2020JHR.pdf), `cordell.txt:475–478`.

**Inference — assessment / reply:** Changes were concentrated in societal discrimination and political rights; physical-integrity sections did not show statistically significant length changes across the sampled transitions (`:498–505`). Institutionalization protects some reporting, not all of it. Longer reports alone do not prove worse actual abuse; shorter reports alone do not establish how much was omitted. No general coding rule can recover facts removed upstream. This qualifies, rather than destroys, State Department-based measurement.

### D. “Information effects”: Clark & Sikkink (2013), and Richards (2016)

Clark & Sikkink, *Information Effects and Human Rights Data*, **Human Rights Quarterly 35:539–568**, [DOI](https://doi.org/10.1353/hrq.2013.0046).

**Source type / strength:** Peer-reviewed comparison of Latin American reports, coded data, and truth-commission evidence. Publisher-deposited abstract checked through Crossref; original full text blocked. **Moderate** here for the stated result and design, not an independently replicated correction.

**Quote — abstract:**

> “Information effects are discernible both in primary sources of information and data coded by two prominent human rights datasets, the Political Terror Scale (PTS) and the Cingranelli-Richards Human Rights Data Set (CIRI).”

[Publisher-deposited abstract](https://api.crossref.org/works?query.title=Information%20Effects%20and%20Human%20Rights%20Data&rows=2).

**Inference — dispute:** Better detection and documentation can make recorded abuse rise or remain flat even when actual conduct improves. Truth commissions offer a partly different basis for checking historical cases, but retrospective discovery and region selection have their own limits.

**Reply found:** David Richards, *The Myth of Information Effects in Human Rights Data: Response to Ann Marie Clark and Kathryn Sikkink*, **HRQ 38:477–492 (2016)**, [DOI](https://doi.org/10.1353/hrq.2016.0033). Bibliography verified; full text blocked. **Inference — weak for adjudicating this reply directly:** I will not pretend to have checked its entire argument. The narrower report-length objection does not settle the issue: unchanged length can coexist with changed detail, classification, or subjects. Later studies below test these mechanisms more directly. No definitive verdict on Richards’s whole reply is supported by this access.

### E. Time drift: Fariss (2014), Cingranelli & Filippov (2018), Fariss (2019)

Fariss, *Respect for Human Rights has Improved Over Time: Modeling the Changing Standard of Accountability*, **APSR 108:297–318**, [DOI](https://doi.org/10.1017/S0003055414000070).

**Source type / strength:** Peer-reviewed measurement model; full text obtained. **Strong** explanation of a comparability problem; **moderate**, model-dependent evidence for the magnitude and direction of corrected global change.

**Quote — p. 297:**

> “The standard of accountability used to assess state behaviors becomes more stringent as monitors look harder for abuse, look in more places for abuse, and classify more acts as abuse.”

[Full text](http://cfariss.com/documents/Fariss2014APSR.pdf), `fariss_http.txt:14–16`.

**Inference — scope:** The model concerns repression / physical-integrity rights. It does not supply a correction for every CIRIGHTS empowerment, labor, or justice indicator. It combines changing report-based indicators with event-based indicators assumed more comparable through time. That assumption is crucial; corrected estimates are not directly observed truth.

Cingranelli & Filippov, *Are Human Rights Practices Improving?*, **APSR 112:1083–1089 (2018)**, [DOI](https://doi.org/10.1017/S0003055418000254).

**Source type / strength:** Peer-reviewed methodological criticism; abstract and original online appendix obtained, main article paywalled. **Moderate** for the reported replication, strong that assumptions are contested.

**Quote — abstract:**

> “We replicated his analysis, replacing the actual values of all indicators of lesser human rights violations with randomly generated data, and obtained an identical improving trend.”

[Publisher](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0003055418000254), `cf2018.txt:462`. [Original appendix](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0003055418000254/resource/name/S0003055418000254sup001.pdf), pp. 1–4, documents the randomization methods.

**Inference — dispute:** They argue the inferred trend is driven by declining mass killings and the imposed measurement assumptions, rather than improvement in common abuses such as torture and imprisonment. This is a substantial sensitivity warning, not proof that unchanged raw CIRI scores are time-comparable.

Fariss, *Yes, Human Rights Practices Are Improving Over Time*, **APSR 113:868–881 (2019)**, [DOI](https://doi.org/10.1017/S000305541900025X).

**Source type / strength:** Peer-reviewed reply with simulations, full text read in relevant sections. **Strong** on the identification objection; **moderate** on the substantive trend because anchor comparability remains an assumption.

**Quote — simulation explanation:**

> “This model is not identified with respect to time because it centers the mean for the units in each time period at zero, which makes it impossible to make over time comparisons of the latent variables estimated from the model on the right.”

[Full text](http://cfariss.com/documents/Fariss2019APSR.pdf), p. 873; `fariss2019_flow.txt:503–508` (PDF ligature normalized).

**Inference — does the reply work?** Largely **yes against the specific flat-trend alternative**: allowing every item’s threshold to move without a common temporal reference makes comparisons across years unidentified; the fitted yearly means can be reset to zero. Adding unrelated random data also need not change a yearly average, even when genuine indicators help locate particular countries. These are persuasive technical rebuttals. They do **not** prove that mass-killing documentation is invariant, nor that all rights improved. Both a raw stagnation claim and an unconditional corrected-progress claim require more than this exchange. Use caution about long-run trends rather than choosing whichever trend is preferred.

### F. Later validation of reporting drift, not of all CIRIGHTS scores

**Greene, Park & Colaresi (2019)**, *Machine Learning Human Rights and Wrongs*, **Political Analysis 27:223–230**, [DOI](https://doi.org/10.1017/pan.2018.11). **Source type:** Peer-reviewed machine-learning tests using report texts and human scores; full text obtained. **Strength:** moderate evidence of a changing text-to-score relationship; vocabulary and document changes complicate isolating the cause.

**Quote — introduction:**

> “Our results are consistent with the expectation that standards of human rights have changed over time.”

[Full text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C4CB3FC4383A50129F6A0F0809BA2452/S1047198718000116a.pdf), p. 223, `greene2019.txt:20–21`.

**Park, Greene & Colaresi (2020)**, *Human Rights are (Increasingly) Plural*, **APSR 114:888–910**, [DOI](https://doi.org/10.1017/S0003055420000258). **Source type:** Peer-reviewed automated analysis of the structure and distinctions within USSD, Amnesty, and HRW texts. **Strength:** strong for changing reporting content; moderate for any claim about underlying conduct.

**Quote — abstract:**

> “Our analysis provides new, clear evidence of change in the structure of these taxonomies as well as in the attention to specific rights and the sharpness of distinctions between rights.”

[Full text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F202F327EA8F4CF52D2E65EB48D409D3/S0003055420000258a.pdf), p. 888, `park2020.txt:22–24`.

**Inference — assessment / reply:** These independently support changing measurement inputs, not an exact Fariss correction. A defense based solely on stable coder instructions or total report length does not answer them. The later taxonomy approach also warns against treating all rights as one simple dimension.

### G. Country transparency: Eck & Fariss (2018)

*Ill Treatment and Torture in Sweden: A Critique of Cross-Case Comparisons*, **HRQ 40:591–604**, [DOI](https://doi.org/10.1353/hrq.2018.0033).

**Source type / strength:** Peer-reviewed case study of public allegations and Sweden’s reporting institutions, full text obtained. **Strong** existence proof of a visibility mechanism; **moderate** for how widespread or quantitatively large it is globally.

**Quote — abstract:**

> “We provide evidence of the process by which the bureaucracy in Sweden ensures an extremely high level of transparency about allegations of human rights abuse by government agents.”

[Full text](http://cfariss.com/documents/EckFariss2018HRQ.pdf), p. 591, `sweden.txt:17–20`.

**Inference — dispute / reply:** A transparent state can document allegations that a closed state conceals. Equal coded categories therefore need not mean equal actual severity. This is **not** proof that Sweden had no abuse, nor a warrant to discount every allegation against an open state. Public coding rules and two coders cannot remove unequal visibility upstream. I found no convincing universal correction in CIRIGHTS’s current rules.

**Haschke & Arnon (2020)**, *What Bias? Changing Standards, Information Effects, and Human Rights Measurement*, **Journal of Human Rights 19:33–49**, [DOI](https://doi.org/10.1080/14754835.2019.1671179). Author manuscript obtained through [author PDF](https://www.peterhaschke.com/files/WhatBias-HaschkeArnon.pdf); later reprinted as a book chapter.

**Source type / strength:** Scholarly methodological analysis; **moderate**, with explicitly suggestive evidence. Separates reporting, changing standards, access/transparency, coder effects, and changing country coverage.

**Quote — conclusion:**

> “Finally, we provided some suggestive evidence that is inconsistent with theoretical accounts of changing standards and information effects but in line with access or transparency effects.”

`haschke_flow.txt:1508–1510`, manuscript p. 21.

**Inference — assessment:** A useful counterweight to treating all disagreement as one uniform temporal drift. Different bias mechanisms need different corrections. Adding countries or splitting states can change an unweighted global mean without improving any person’s treatment. This does not negate the later evidence for changing report content.

### H. CIRI versus PTS: Wood & Gibney (2010), Cingranelli & Richards (2010)

Wood & Gibney, *The Political Terror Scale (PTS): A Re-introduction and a Comparison to CIRI*, **HRQ 32:367–400**, [full text](https://www.politicalterrorscale.org/Data/Files/Wood%20and%20Gibney%202010.pdf).

**Source type / strength:** Peer-reviewed comparative analysis by PTS’s producers; **strong** on differing design and outputs, **moderate** as an independent validity test because the authors have their own measurement project and sources overlap.

**Quote — p. 375:**

> “Unsurprisingly, the two measures are rather highly correlated— approximately 0.73 for the USDS-derived PTS scores and 0.65 for AI scores.”

`wood.txt:433–434`. Footnote 25 identifies these as **Kendall’s tau-b**, not Pearson correlation (`:457–462`).

**Inference — criticism:** CIRI usefully separates torture, imprisonment, killing, and disappearance. But summing categories imposes trade-offs; coarse ceilings erase severity differences; numerical cutoffs have questionable precision when narrative reports lack counts. Excluding country-years with no functioning government can omit the very places where overall human-rights conditions are worst. These are different issues, not all “Western bias.”

**Reply:** Cingranelli & Richards, *The Cingranelli and Richards (CIRI) Human Rights Data Project*, **HRQ 32:401–424**, [DOI](https://doi.org/10.1353/hrq.0.0141). Publisher abstract and Wood–Gibney’s detailed rejoinder inspected; original full text not obtained. The defense emphasizes transparent, replicable rules, disaggregation, government-practice scope, and evidence for a common latent dimension.

**Inference — does it work?** **Yes** for using separate right indicators and a clearly declared government-practice target. **Only partly** for the total score: transparency and internal consistency do not justify every weighting, remove censoring, or turn a state-practice measure into total conditions. The comparators share sources, so their agreement is not independent ground truth. These objections counsel against constitution-level league tables more than against citing individual documented practices.

## 2. Reliability: useful evidence, with an important qualification

**Quote — historical CIRI FAQ:**

> “For the most recent coding, the Krippendorf’s r-bar measure of interrater reliability for the entire set was 0.944.”

> “CIRI discounts in this figure disagreements among coders based solely upon one coder having missed some information in a source, as these errors do not make it into the final data and are not the result of operationalization.”

[FAQ](http://www.humanrightsdata.com/p/faq.html), `ciri_faq.txt:39`. **Source type:** primary project self-report. **Strength:** moderate evidence of agreement under its own counting rule; not an independent audit, not unadjusted accuracy, and not current CIRIGHTS reliability. The page does not date “most recent” sufficiently for a contemporary claim.

**Quote — CIRIGHTS’s 2024 journal article:**

> “Each right for each country is scored independently by at least two scorers who compare and reconcile scoring if necessary.”

[Mark, Filippov & Cingranelli, *CIRIGHTS: Quantifying Respect for All Human Rights*, HRQ 46:264–286](https://www.newswise.com/pdf_docs/171474273183689_CIRIGHTS.pdf), p. 270, `cirights_full.txt:309–310`.

**Inference — assessment:** Double coding, senior adjudication, and revised historical scores are real quality controls. But agreement on incomplete reports is compatible with incorrect estimates of actual practice. The article’s **Cronbach alpha 0.94** for the 2019 overall index (`:920–923`) is **inter-item consistency, not intercoder reliability**. I found no independently verified, current, per-right CIRIGHTS reliability table.

**Arnon, Haschke & Park (2023)**, *The Right Accounting of Wrongs*, **BJPS 53:163–182**, [DOI](https://doi.org/10.1017/S0007123421000661). **Source type:** peer-reviewed text analysis plus blinded audit experiment on **PTS coders**, not CIRIGHTS coders. **Strength:** strong for this limited design; moderate generalization beyond it.

**Quote — abstract:**

> “We find no evidence of coder bias and conclude that human rights measures have changed over time and that bias is introduced as part of monitoring and reporting.”

[Full text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0BBEE14D2F33A73F3566B57F26548465/S0007123421000661a.pdf), `account_full.txt:26–27`.

**Inference — assessment / reply:** Their audit has 2016 PTS coders recode redacted 2005 reports, compared with the contemporaneous 2006 coding. It supports taking source drift seriously while narrowing the accusation of worsening coder standards. It is **not** evidence of zero error or a validation of the current CIRIGHTS team. Wood & Gibney’s historical PTS reliability above 0.85 is likewise PTS evidence, not CIRIGHTS evidence.

## 3. Coverage and GRIP rankings

**Quote — CIRIGHTS August 2023 manual:**

> “The CIRIGHTS Project scores only government violations of the human rights of its citizens, so violations against non-citizens are not scored.”

> “Except in certain cases of occupation, only violations that occur within a country’s internationally recognized borders are scored.”

[Manual](https://cirights.com/wp-content/uploads/2023/08/cirights-codebook-v2.8.27.23.pdf), p. 3, `cirights_manual.txt:156–161`.

**Inference — strength / scope:** Strong evidence of these published scope rules, not proof of unchanged application in every v3 variable. Specific refugee or trafficking indicators need their own rules. A country score is not a measure of its entire worldwide conduct, private oppression, or protection of everybody present. USSD’s lack of an ordinary self-country report also makes **US source comparability an unresolved audit item**; I did not verify equivalent US source coverage.

**Inference — GRIP-specific literature search:** I found established criticism of CIRI and report-based measurement, but **no dedicated independent published validation or methodological rebuttal of the 2024 GRIP rankings** in the inspected results. Searches for “Global Rights Project” with criticism and “CIRIGHTS” with rankings also returned unrelated projects and generic citations. Absence from these searches is weak evidence of absence. GRIP is a presentation layer over CIRIGHTS, not a second independent corroborating dataset.

**Quote — GRIP 2024, p. 18:**

> “All of the rights are measured on an ordinal scale with higher values indicating greater respect.”

[Report](https://web.uri.edu/artsci/wp-content/uploads/sites/1132/GRIP-report-2024.docx_.pdf), `grip.txt:546–547`.

**Inference — my criticism, not a published external verdict:** Scaling ordinal categories to 100 does not establish equal substantive distances or comparable detection across different rights. Equal country weighting is not population weighting. Composite weights and letter-grade cutoffs are editorial choices, not discoveries about how much suffering or moral value each right represents. These limits matter even when arithmetic is correct.

**Inference — prior reproducibility blocker:** `slop/research/20261014_rights_kept_check.md` documents that Table 5’s stated latest-year calculation did not reproduce from the official December 2024 dataset’s 2022 rows. Its reported means differ substantially for torture and state-led atrocities. The report also mixes “between 2000 and today” with latest-year language. This is **our audit finding**, not a newly located published criticism. It remains unresolved; exact Table 5 values should not become constitutional authority until release, years, and aggregation are reconciled.

## 4. Funding and political connections

### Historical CIRI

**Quote — successor project’s history page:**

> “The project was supported by the National Science Foundation, the World Bank, GTZ, and the institutions of its directors.”

[Project history](https://cirights.com/ciri/), `ciri.txt:10`.

**Source type / strength:** Primary institutional history; **strong** for the disclosed supporter list, limited for dates, amounts, and award conditions. **Inference:** NSF is a US public research funder; the World Bank is an intergovernmental development institution; GTZ was Germany’s development-cooperation organization. These are public-policy connections, not proof of partisan direction. **Data sourced from the State Department does not mean the State Department funded the project.** No such funding was established here.

### CIRIGHTS / GRIP 2024

**Quote — acknowledgments, p. 43:**

> “Tom Silvia and Shannon Chandley deserve our profoundest thank you: This report and the data it highlights could not have been created without their generous support.”

[GRIP 2024](https://web.uri.edu/artsci/wp-content/uploads/sites/1132/GRIP-report-2024.docx_.pdf), `grip.txt:1446–1447`.

**Quote — p. 44:**

> “We also express gratitude for funding from the University of Rhode Island College of Arts and Sciences Event Fund.”

`grip.txt:1489–1490`. The next paragraph names the A&S Fellows Program’s funding of 2023 CIRIGHTS Research Fellows. The report also acknowledges work/support from URI, Binghamton’s Human Rights Institute and political science department, and UConn (`:1468–1499`).

**Source type / strength:** Primary financial/support disclosure; **strong** for named support, limited for the full budget and whether private support was cash or in-kind.

**Quote — New Hampshire Democratic Party’s officers page:**

> “Former State Senator Shannon Chandley is in her first term as the NHDP Finance Chair.”

> “Shannon and her husband, Tom Silvia, have four adult children. She received her BA from the University of Rhode Island.”

[Party’s primary biography](https://nhdp.org/officers-staff/), `nh_officers.txt:104–105`.

**Inference — political tie:** The matching pair of names and URI affiliation make identification with GRIP’s supporters very persuasive. Chandley is a former Democratic New Hampshire legislator and has a current party-finance role. This is a genuine apparent political supporter connection worth disclosing. **It does not establish party funding, grant conditions, influence over coding, or a partisan falsification of scores.** No donation amount, donor-control arrangement, or comprehensive current funding statement was located. The current party role should not be backdated to the 2024 report.

## 5. Manual checks and residual risks

**Manual notes:** I read the relevant full-text methods, results, and replies, rather than relying only on search snippets. In particular I checked Fariss’s distinction between stable coding rules and changing source reports; CIRI’s excluded-disagreement reliability rule; CIRIGHTS’s admission of source bias; the PTS-specific scope of the coder experiment; and the original donor acknowledgment against the party’s own biography. I kept counterevidence: allies can receive *more* physical-integrity scrutiny, and not every reporting section changes equally. PDFs, raw HTML, extraction scripts, and fetch logs are retained in the specified download directory. Bot challenges, empty pages, and a wrong-topic NBER download were rejected as evidence. `validate_report.py` matched all 25 source quotations, allowing the stated normalization, and confirmed the proposed paragraph has 76 words and none of the four prohibited words (`quote_validation.json`).

**Residual risks — inference:** Poe 2001, Clark–Sikkink 2013, Richards 2016, and the main Cingranelli–Filippov 2018 article were not all accessible in full. Their access levels are identified above; no unseen coefficients are invented. No fresh statistical replication was run. Older physical-integrity criticisms do not automatically quantify error in every CIRIGHTS v3 variable. Current US source coverage, per-right intercoder agreement, donor amounts/conditions, and Table 5’s generating calculation remain unresolved. These gaps limit exact rankings more than the broad observation that documented rights violations occur.

No model answers or judge verdicts were generated. Model demo panel: base | grafted | graft 2x | graft 4x | graft+SFT | healed | SFT only: **not run**; not applicable to this source audit. Nothing staged or committed.

## 6. Final answers

### (1) Is CIRIGHTS good enough to cite in a constitution?

**Inference — yes, with a narrow claim.** Cite it as named university researchers’ report-based estimates of government respect for specified rights, with reporting limits. It is informative, openly documented, and scrutinized in the literature. **No** to an unqualified list of rights “kept,” time-frequency percentages, exact moral league tables, or a claim that rights have not improved merely because raw scores are flat. Do not restore the unreconciled Table 5 numbers yet. A short source-and-limit statement is preferable to those figures.

### (2) What can and cannot it imply about people’s values?

**Inference — wassname’s filter model is reasonable, but cannot be inverted from these scores alone.** Enforcement can be evidence of values expressed through institutions, filtered by government interests and power. Add capacity, conflict, legal duties, elite incentives, collective-action barriers, and unequal political influence. The observed score adds a second filter: what monitors can see and choose to report, followed by coding rules.

**Inference — can:** Supply a noisy contextual prior about institutionalized protections and the constraints people actually face; reveal a gap between formal commitments and reported practice; help select particular cases for investigation. Combined with surveys, costly resistance, voting, and institutional history, it can contribute to a values model.

**Inference — cannot:** Recover citizens’ preferences, their distribution, willingness to sacrifice, or a ranking of moral ends. Low respect may coexist with intense suppressed demand; high respect may reflect legal restraints or external pressure rather than unanimous preference. Cross-right score differences also mix distinct thresholds and visibility. The dataset is not evidence of uniquely Western preferences, timeless agreement, or the moral correctness of whatever governments do. This is an identification limit, **not** a denial that institutions contain information about values.

### (3) Corrected paragraph if keeping it — 76 words

**Inference — proposed wording, not a quotation or an approved edit:**

> I use CIRIGHTS, made by university researchers led by Skip Mark, David Cingranelli, Mikhail Filippov, and David Richards, as evidence about government respect for rights. Its scores mainly code US State Department country reports, with Amnesty International reports for physical-integrity rights and other sources for some rights. They estimate reported protection, not people’s values or compliance percentages. Government practice reflects values filtered through interests, power, and capacity; reporting adds uncertainty. I compare it with other evidence.

-- PI/Sol
