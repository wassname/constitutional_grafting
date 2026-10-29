# Which rights do Western governments keep more than the rest?

2026-10-14. Cross-section only; no claim about change over time. Read `AGENTS.md`, the project decision summary, and both requested prior notes. No existing project file edited; the only new project script is listed below.

## Result

**Observation:** In CIRIGHTS v3.12.10.24, averaged across available scores in **2018–2022**, the moralmaps West scores higher on **all 25 available individual practice/right indicators**. The largest gaps are safe working conditions (+55.1 points), fair trial (+54.9), independent courts (+50.4), women’s social rights (+48.1), minimum wage enforcement (+47.4), speech (+44.5), and elections (+44.4). These are **shares of each score’s maximum, expressed out of 100**, not compliance rates.

**Inference:** This is evidence of stronger institutional commitments to limiting arbitrary rule, protecting political participation and women’s equal treatment, and enforcing some worker protections. It is not a measurement of citizens’ preferences or the price they would pay. The West’s lower scores on collective bargaining (62.0), religious freedom (64.3), work hours (68.9), and child labor (69.0) caution against describing universal Western protection.

## 1. Exact sources and files

**Observation — official release check:** The current project homepage, https://cirights.com/, is its download page. It links the December 10, 2024 release, **v3.12.10.24**. The public WordPress media search also shows no later dataset among its CIRIGHTS-named files. The guessed `/data.html` address was a page-not-found response and was not used as evidence. This establishes the latest **publicly linked release found**, not that no unpublished version exists. Its data end in **2022**, not 2024 or 2026.

| Download | Exact URL | Local file under `.local/papers/cirights_data_20261014/` |
|---|---|---|
| Main input, Excel | https://cirights.com/wp-content/uploads/2024/12/cirights_v3.12.10.24.xlsx | `cirights_v3.12.10.24.xlsx`, sheet `Sheet1` |
| Independent format check | https://cirights.com/wp-content/uploads/2024/12/cirights_v3.12.10.24.dta_.zip | ZIP plus extracted `cirights_v3.12.10.24.dta` |
| Linked scoring manual | https://cirights.com/wp-content/uploads/2023/08/cirights-codebook-v2.8.27.23.pdf | PDF plus `codebook.txt` |

**Observation — codebook mismatch:** The downloaded manual says **Manual Version 2.8.27.23**, August 27, 2023, on its title page. The website links this older manual alongside v3 data. I do not relabel it as a v3 manual or assume every rule remained unchanged. The Stata variable labels agree with the Excel labels and identify the practice variables.

**Observation — SHA-256 fingerprints:**

```text
Excel   b398c0ef145ab67775d4f6218da96c9fb12a83877f5b79f78defb0b2a1582705
Manual  8b7604890460054e591ea652f00f9b68dcce126e8458d8d3a960c4fad58d589e
Stata   70b940ed617502455c4920880b02c1f25fdce53dea09292f432c8eae8629f9d7
Script  73bf9c2e67baed600479f1dee6e1f7a9418b34497f3062ae77c536ec02c1e88d
```

**Observation — source materials retained:** `home.html`, `pages.json`, `media.json`, `us_search.json`, and `us_posts.json` record the official-site checks. `ussd_2022.html` is a “Technical Difficulties” response, **not** a successful inspection of the State Department country index. Source-criticism evidence is in `slop/research/20261014_ciri_criticism.md`; this report does not claim a new replication of that literature.

## 2. What “Western” means here

**Observation:** I read the actual definitions in:

`/home/code/dev.before-workspace-link/steer-vllm/docs/vendor/moral-maps/src/moralmaps/zones.py`

The file’s **`IW_MACRO` West includes English-Speaking, Protestant Europe, Catholic Europe, and Baltic**. The last group matters: the file includes it even though the task’s parenthetical named only the first three. I follow the actual macro definition and separately check excluding the Baltics. The exact dictionaries used are frozen in `zones_used.json`; their source-file fingerprint is in `results.json`.

**Observation — the 30 included countries:**

- **English-Speaking (6):** Australia, Canada, Ireland, New Zealand, United Kingdom, United States of America.
- **Protestant Europe (9):** Austria, Denmark, Finland, Germany, Iceland, Netherlands, Norway, Sweden, Switzerland.
- **Catholic Europe (12):** Andorra, Belgium, Croatia, Czech Republic, France, Hungary, Italy, Poland, Portugal, Slovak Republic, Slovenia, Spain.
- **Baltic (3):** Estonia, Latvia, Lithuania.

**Observation — matching:** Great Britain → United Kingdom; United States → United States of America; Czechia → Czech Republic; Slovakia → Slovak Republic. Northern Ireland has no separate CIRIGHTS country row and is not counted twice. All other West entries match directly. Stable CIRIGHTS country IDs, rather than changing country-name spellings, join the five years.

**Observation — rest:** Every other dataset country, **165 countries**, including countries not assigned any zone in `zones.py`. None is silently dropped. The full rest list is in `results.json`.

**Inference — important boundary caveat:** This is the supplied taxonomy, not my geopolitical definition. Its country list is incomplete: Luxembourg, Liechtenstein, Malta, Monaco and San Marino therefore enter “rest”; Greece and Cyprus also enter “rest” because the file assigns them Orthodox. This can affect magnitudes and should not be concealed by calling this simply Europe versus non-Europe. Excluding Baltics moves the gap by at most 3.2 points; all gaps remain positive.

## 3. Calculation and table

**Observation — method:** There are 975 country-year rows: 195 countries × 5 years. For each right, first average each country’s available 2018–2022 scores, then average those country means within West/rest, giving every country equal weight. Missing cells are excluded, not set to zero or the maximum. A country needs at least one observed year for that right. Counts below distinguish countries from observed country-years.

**Observation — scales and selection:** The manual defines the 0–2 and 0–3 scales shown below. `bbatrocity` is a 0/1 **presence-of-abuse** flag, so I use `100 × (1 − bbatrocity)` for protection. For all others, use `100 × score / scale maximum`. I use practice rather than law for labor, trafficking, women’s social rights and fair trial. Women’s political/economic indicators have no separate practice columns in this release and combine law with practice; they are not pure practice measures. Composites, law columns, and atrocity intensity are excluded. Prison and Indigenous-right measures mentioned in the manual are not individual columns in this release, so no result is invented for them.

**Inference — descriptive marks, not statistical tests:** **D** = West at least 20 scale points higher, a candidate distinctive institutional commitment. **H** = both groups at least 80/100 and gap under 20, relatively high everywhere. **N** = West not higher. “Smaller gap” = positive but below 20. These are declared sorting aids, not natural thresholds or significance claims; being D does not mean full Western protection.

| Right (variable; scale) | West | Rest | Gap | Countries W/R | Country-years W/R | Mark |
|---|---:|---:|---:|---:|---:|---|
| Occupational Safety and Health (`safe_p`; 0–2) | 87.0 | 31.9 | +55.1 | 30/165 | 144/822 | D |
| Right to a Fair Trial (`trial_p`; 0–3) | 81.6 | 26.6 | +54.9 | 30/165 | 145/823 | D |
| Judicial Independence (`injud`; 0–2) | 88.0 | 37.6 | +50.4 | 30/165 | 146/819 | D |
| Women's Social Rights (`wosoc_p`; 0–3) | 97.1 | 49.0 | +48.1 | 30/165 | 147/824 | D |
| Minimum Wage (`wage_p`; 0–2) | 79.8 | 32.4 | +47.4 | 30/165 | 145/824 | D |
| Freedom of Speech (`speech`; 0–2) | 89.4 | 44.9 | +44.5 | 30/165 | 146/820 | D |
| Electoral Self-determination (`elecsd`; 0–2) | 94.2 | 49.8 | +44.4 | 30/165 | 146/820 | D |
| Child Labor (`child_p`; 0–2) | 69.0 | 25.1 | +43.9 | 30/165 | 145/818 | D |
| Limitations on Work Hours (`hour_p`; 0–2) | 68.9 | 26.4 | +42.5 | 30/165 | 145/822 | D |
| Union Rights (`union_p`; 0–2) | 71.9 | 29.5 | +42.4 | 30/165 | 145/821 | D |
| Human Rights NGO Freedom (`ngo_freedom`; 0–3) | 91.8 | 53.1 | +38.6 | 30/165 | 147/825 | D |
| Human Trafficking (`trafficking_p`; 0–2) | 63.3 | 25.4 | +38.0 | 30/165 | 88/493 | D |
| Collective Bargaining (`barg_p`; 0–2) | 62.0 | 24.2 | +37.8 | 30/165 | 145/823 | D |
| Forced Labor (`force_p`; 0–2) | 71.2 | 34.9 | +36.3 | 30/165 | 145/819 | D |
| Freedom of Assembly and Association (`assn`; 0–2) | 86.7 | 52.5 | +34.2 | 30/165 | 146/812 | D |
| Women's Economic Rights (`wecon`; 0–3) | 70.6 | 36.4 | +34.2 | 30/165 | 146/816 | D |
| Political Imprisonment (`polpris`; 0–2) | 98.0 | 64.3 | +33.7 | 30/165 | 150/823 | D |
| Extrajudicial Killings (`kill`; 0–2) | 93.0 | 60.3 | +32.7 | 30/165 | 150/824 | D |
| Torture (`tort`; 0–2) | 72.3 | 40.2 | +32.1 | 30/165 | 150/823 | D |
| Freedom of Domestic Movement (`dommov`; 0–2) | 93.2 | 66.4 | +26.8 | 30/165 | 146/816 | D |
| Freedom of Foreign Movement (`formov`; 0–2) | 95.9 | 70.7 | +25.2 | 30/165 | 146/818 | D |
| Women's Political Rights (`wopol`; 0–3) | 87.6 | 65.4 | +22.2 | 30/165 | 145/817 | D |
| Disappearances (`disap`; 0–2) | 99.7 | 79.0 | +20.7 | 30/165 | 150/824 | D |
| Freedom from brutality-based atrocity (`bbatrocity`; 0–1) | 97.3 | 78.5 | +18.8 | 30/165 | 150/821 | smaller gap |
| Religious Freedom (`rel_free`; 0–2) | 64.3 | 48.0 | +16.3 | 30/165 | 146/819 | smaller gap |

**Observation — high everywhere / not higher:** No row meets H or N. Disappearance and atrocity protection are the closest to broadly high scores: rest scores 79.0 and 78.5, against West 99.7 and 97.3. They are less discriminating than fair trial or safe work, but their 20.7- and 18.8-point gaps are not negligible. Religious freedom has the smallest gap (+16.3), and only 64.3 in the West. Do not turn these into a claim of universal religious liberty.

**Observation — trafficking coverage warning:** The trafficking row is unusually incomplete: non-US scores come only from 2018–2020, while the US contributes only 2021–2022. It is therefore an available-data window mean, **not a balanced five-year comparison**. Restricting this right to common years 2018–2020 excludes the US and gives **West 62.1, rest 25.4, gap +36.7; 29/165 countries**. Do not cite the main row as evidence of 2021–2022 global practice.

## 4. The US and cases without reports

**Observation:** The State Department does not issue its ordinary country-practice report on the US itself. Yet CIRIGHTS does **not** simply leave every US score blank. The actual US rows contain:

| US indicator, raw score | 2018 | 2019 | 2020 | 2021 | 2022 |
|---|---:|---:|---:|---:|---:|
| Disappearance, 0–2 | 2 | 2 | 2 | 2 | 2 |
| Extrajudicial killing, 0–2 | 0 | 0 | 0 | 0 | 0 |
| Political imprisonment, 0–2 | 2 | 1 | 0 | 2 | 0 |
| Torture, 0–2 | 1 | 0 | 0 | 0 | 0 |
| Atrocity **presence**, 0–1 | 0 | 1 | 1 | 1 | 1 |

**Observation:** The other 20 individual indicators are missing for the US in 2018–2020. They appear in 2021–2022, except occupational safety is missing again in 2022. Thus many US window means cover only two years, and occupational safety only one. The old physical-integrity-only pattern no longer describes the whole current release.

**Observation — what the documentation establishes:** The linked manual’s introduction names State Department reports for all variables and Amnesty reports additionally for physical integrity (printed p. 2; `codebook.txt:105–113`). Its protocol normally disallows outside information, with named-source verification exceptions (`:191–202`). Its social-rights section explicitly permits missing scores when evidence is insufficient (`:1544–1549`). I found **no US-specific source replacement rule or country-year source register** in the downloaded release/manual or inspected official pages. The 2024 journal article also states the US was missing from its 2019 overall map because some component data were absent; that is consistent with the observed earlier blanks.

**Inference — flag, not an invented explanation:** Amnesty could supply US physical-integrity evidence under the general rules, but that does not establish the actual source of each US score, especially the newly populated nonphysical scores. US source comparability is **unresolved**. The unusually low killing/torture and derived atrocity scores are retained exactly as released, not “corrected” to my expectations. The atrocity flag is mechanically derived from killing plus other physical-integrity categories in the manual (`:626–645`), not an independently counted genocide or war event.

**Observation — other missing/report-less cases:** The dataset has scores but no report-availability flag; a blank is not proof that the whole country report is absent. For example, Czech labor scores are missing in 2018–2019, Slovakia lacks several political indicators in 2019, and most countries lack trafficking in 2021–2022. All other 194 countries have at least one score for each of the 25 selected indicators in this window. None is wholly unscored on these selected indicators, but score coverage cannot establish report coverage. The failed State Department index fetch means I cannot certify an exhaustive list of countries/years without reports or their substitutes. I make no assumption that missing reports imply full protection.

**Observation — robustness:** Removing the US leaves **all 25 gaps positive**; the largest West/gap change is 3.2 points. Restricting each of the other 24 rights to countries with all five scores also leaves every gap positive; the largest gap change is 3.0 points. Complete-case groups vary from 27–30 Western and 154–165 rest countries. Trafficking has no five-year-complete cases and is checked separately above. Full unrounded sensitivity results are in `results.json`.

## 5. What it says about values

**Inference:** The clearest political evidence is stronger protection of fair trial, judicial independence, speech, elections, association, political prisoners, and human-rights investigators. These protections restrain a government’s freedom to silence critics, imprison opponents or control adjudication. Their comparatively high practice scores are consistent with Western institutions accepting those constraints. Stronger women’s social rights and labor enforcement add a commitment to protecting people against discrimination and powerful private interests. Labor enforcement often requires **more** state action, not simply less state power.

**Inference — limit:** This is a noisy institutional-values prior, not proof of costly popular sacrifice. CIRIGHTS does not observe the cost to a ruler, voters’ willingness to pay, or the preferences of suppressed minorities. Wealth, state capacity, conflict, legal institutions and elite incentives can produce the same pattern. The comparison is descriptive, not a causal estimate controlling for those factors, and the rest of the world is not a single moral culture.

**Inference — the measurement caveats that matter most:**

1. **Ally/reporting bias:** State Department reporting has documented historical ally-favoring biases, although later evidence is mixed and sometimes finds more scrutiny of allies. Since many Western states are US allies, some positive gap could reflect reporting rather than practice. Amnesty cross-checks on physical integrity help, but do not validate every other right or eliminate shared blind spots. No present-day bias adjustment was estimated here.
2. **Changing standards affect levels too:** Fariss’s argument is not avoided entirely by dropping a trend chart. Modern detection, definitions and thresholds affect the scores in this cross-section; uneven transparency can also affect countries differently. Averaging five recent years reduces annual noise, not those measurement problems. Fariss’s physical-integrity work is not an available correction for all these labor/political measures.
3. **Ordinal categories:** A score of 2 is ordered above 1; it does not establish twice as much protection. Means and division by the maximum are a reproducible descriptive convention. A 55-point difference on one right need not be morally larger than a 44-point difference on another. Fair-trial top categories allow criteria “satisfied or not mentioned” (manual printed p. 70, `codebook.txt:2905–2910`); top scores are not proof of zero abuse.
4. **Scope and boundaries:** Published general rules focus on government conduct toward citizens within national borders, with limited occupation exceptions (`:156–161`). These scores therefore do not measure a state’s complete treatment of migrants, foreign populations or conduct abroad; specific trafficking rules have their own scope. Equal-country averages are not population averages. The incomplete moralmaps taxonomy and the US/missing-source issues add uncertainty.

## 6. Candidate constitution paragraph — 77 words

**Inference — proposed wording only, not an approved constitution edit:**

> I think Western societies give particular weight to fair trials, independent courts, free speech, competitive elections, women’s equal social rights, and safe work with minimum pay: CIRIGHTS’s 2018–2022 government-practice scores are substantially higher there than elsewhere. These protections limit rulers’ discretion or require enforcement against powerful interests, so I treat them as evidence of institutional commitments, not just promises. I do not infer unanimous preferences or moral superiority; reporting bias, state capacity, and coarse scoring leave uncertainty.

## 7. Manual checks, residual risks and reproducibility

**Observation — manual notes:** I read the score definitions, law/practice distinction, benefit-of-doubt rules, source restrictions, and actual country scores. Five country/right checks sampled with seed `20261014` were manually recalculated: Tuvalu women’s social rights 66.7; Greece domestic movement 60.0; El Salvador foreign movement 90.0; Cyprus women’s economic rights 46.7; Spain fair trial 86.7. They match the exported country means. Targeted checks also confirmed the surprising US raw scores above, France religious freedom 1/2 in all five years (50/100), Australia fair trial 3,2,2,1,2 (66.7/100), and Czech occupational safety using only three observed years rather than inventing the missing two. Luxembourg scores 100 on safety but enters rest under the supplied taxonomy. These checks exposed real coverage and boundary issues rather than a calculation error.

**Observation — automated validation:** Excel and Stata agree on **24,375 cells** (975 rows × 25 selected rights), including missingness. All score-range, five-row-per-country, unique-ID/year, expected-West-membership and country-count assertions pass. No negative sentinel code occurs in the selected observed scores. The candidate paragraph has 77 whitespace-separated words and none of the four prohibited words.

**Inference — residual risks:** Current US score provenance and an exhaustive report-less-country source audit remain unresolved; the linked codebook predates v3; trafficking is not balanced across the window. Cultural-zone omissions, unequal reporting/transparency, ordinal arithmetic and unadjusted wealth/capacity confounding limit interpretation. The broad positive-gap pattern survives the reported sensitivities, but that does not remove these risks.

**Observation — generated outputs, all under `.local/papers/cirights_data_20261014/`:** `results.json` contains the exact countries, hashes, unrounded table and sensitivities; `cleaned_window.tsv` contains observed raw inputs and normalized scores; `country_means.tsv` contains the equally weighted country summaries and their year counts; `table.md` and `run.log` record the displayed table and validation.

**Observation — runnable code:** `scripts/scratch/20261014_cirights_west_vs_rest.py`. The standard-library path reads the downloaded Excel directly; `--check-stata` additionally requires pandas (available in this environment). To rerun after downloading the exact files above:

```bash
pdftotext -layout .local/papers/cirights_data_20261014/cirights-codebook-v2.8.27.23.pdf .local/papers/cirights_data_20261014/codebook.txt
python scripts/scratch/20261014_cirights_west_vs_rest.py --check-stata
```

**Observation — model evaluation:** No model answers or judge verdicts were generated. Demo-panel conditions base | grafted | graft 2x | graft 4x | graft+SFT | healed | SFT only: **not run**, not applicable to this dataset audit. No existing constitution, journal or prior research note was edited; nothing staged or committed.

-- PI/Sol

## Appendix: exact analysis code

```python
"""One cross-section: CIRIGHTS v3.12.10.24, 2018–2022, equal country weights.
Python standard library; optional --check-stata uses pandas for independent format check.
No missing score is imputed. -- PI/Sol
"""
from pathlib import Path
import argparse
import ast
import csv
import hashlib
import json
import statistics as stats
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / '.local/papers/cirights_data_20261014'
XLSX = HERE / 'cirights_v3.12.10.24.xlsx'
ZONES = Path('/home/code/dev.before-workspace-link/steer-vllm/docs/vendor/moral-maps/src/moralmaps/zones.py')
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
# Excel column, original Stata name, scale maximum, reverse abuse presence.
# Deliberately exclude composites, atrocity intensity (conditional on abuse), and law columns.
RIGHTS = [
    ('O', 'bbatrocity', 1, True),
    ('Q', 'disap', 2, False), ('R', 'kill', 2, False),
    ('S', 'polpris', 2, False), ('T', 'tort', 2, False),
    ('U', 'assn', 2, False), ('V', 'formov', 2, False),
    ('W', 'dommov', 2, False), ('X', 'speech', 2, False),
    ('Y', 'elecsd', 2, False), ('Z', 'rel_free', 2, False),
    ('AA', 'union_p', 2, False), ('AB', 'barg_p', 2, False),
    ('AC', 'hour_p', 2, False), ('AD', 'force_p', 2, False),
    ('AE', 'child_p', 2, False), ('AF', 'wage_p', 2, False),
    ('AG', 'safe_p', 2, False), ('AH', 'trafficking_p', 2, False),
    ('AI', 'injud', 2, False), ('AJ', 'wecon', 3, False),
    ('AK', 'wopol', 3, False), ('AL', 'wosoc_p', 3, False),
    ('AM', 'ngo_freedom', 3, False), ('AN', 'trial_p', 3, False),
]
ALIASES = {'United Kingdom': 'Great Britain', 'United States of America': 'United States',
           'Czech Republic': 'Czechia', 'Slovak Republic': 'Slovakia'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_xlsx():
    with zipfile.ZipFile(XLSX) as z:
        strings = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        rows = []
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('s:sheetData/s:row', NS):
            values = {}
            for cell in row:
                v = cell.find('s:v', NS)
                if v is not None:
                    col = ''.join(c for c in cell.attrib['r'] if c.isalpha())
                    values[col] = strings[int(v.text)] if cell.attrib.get('t') == 's' else v.text
            rows.append(values)
    return rows[0], rows[1:]


def zone_dicts():
    # Read assignments as data; do not execute the external module or require loguru.
    maps = {}
    for node in ast.parse(ZONES.read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('IW_ZONE', 'IW_MACRO'):
                    maps[target.id] = ast.literal_eval(node.value)
    return maps['IW_ZONE'], maps['IW_MACRO']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-stata', action='store_true')
    args = parser.parse_args()
    header, all_rows = load_xlsx()
    end = max(int(r['B']) for r in all_rows)
    years = list(range(end - 4, end + 1))
    rows = [r for r in all_rows if int(r['B']) in years]
    assert end == 2022 and len(rows) == 975
    # Stable CIRIGHTS id, not country strings that change between years.
    countries = {r['C']: r['A'] for r in rows if int(r['B']) == end}
    assert len(countries) == 195 and len({(r['C'], r['B']) for r in rows}) == 975
    assert all(sum(r['C'] == cid for r in rows) == 5 for cid in countries)
    fine, macro = zone_dicts()
    west = {cid for cid, name in countries.items() if macro.get(fine.get(ALIASES.get(name, name))) == 'West'}
    baltic = {cid for cid, name in countries.items() if fine.get(name) == 'Baltic'}
    assert len(west) == 30 and len(baltic) == 3
    expected = {name for name, zone in fine.items() if macro[zone] == 'West'} - {'Northern Ireland'}
    assert {ALIASES.get(countries[cid], countries[cid]) for cid in west} == expected
    metadata = {'xlsx': str(XLSX.relative_to(ROOT)), 'xlsx_sha256': sha(XLSX),
                'zones': str(ZONES), 'zones_sha256': sha(ZONES), 'years': years,
                'rows': len(rows), 'countries': len(countries),
                'west': sorted(countries[cid] for cid in west),
                'rest': sorted(countries[cid] for cid in countries if cid not in west),
                'not_separate_countries': ['Northern Ireland'], 'format_check': 'not run'}
    # Freeze exact taxonomy read by this run, in the download directory.
    (HERE / 'zones_used.json').write_text(json.dumps({'IW_ZONE': fine, 'IW_MACRO': macro}, indent=2))
    output, country_means, cleaned = [], [], []
    for col, variable, maximum, reverse in RIGHTS:
        observed = {}
        for r in rows:
            raw = r.get(col, '')
            if raw not in ('', '.', 'NA'):
                v = float(raw)
                assert v.is_integer() and 0 <= v <= maximum, (variable, r['A'], raw)
                score = 100 * (1 - v if reverse else v / maximum)
                observed.setdefault(r['C'], []).append(score)
                cleaned.append([r['C'], countries[r['C']], r['B'], variable, raw, score])
        means = {cid: stats.mean(v) for cid, v in observed.items()}
        for cid, score in means.items():
            country_means.append([cid, countries[cid], variable, 'West' if cid in west else 'rest', len(observed[cid]), score])
        def compare(west_ids, exclude=frozenset(), complete=False):
            eligible = {cid for cid in means if cid not in exclude and (not complete or len(observed[cid]) == 5)}
            w = [means[cid] for cid in eligible & west_ids]
            r = [means[cid] for cid in eligible - west_ids]
            return {'West': stats.mean(w), 'rest': stats.mean(r),
                    'gap': stats.mean(w) - stats.mean(r), 'n_west': len(w), 'n_rest': len(r)}
        result = {'right': ('Freedom from brutality-based atrocity' if reverse else header[col]),
                  'variable': variable, 'excel_column': col, 'maximum': maximum,
                  'reverse': reverse, **compare(west),
                  'years_west': sum(len(v) for cid, v in observed.items() if cid in west),
                  'years_rest': sum(len(v) for cid, v in observed.items() if cid not in west),
                  'complete': compare(west, complete=True) if variable != 'trafficking_p' else None,
                  'no_us': compare(west, {'662'}), 'no_baltic': compare(west - baltic)}
        w, r, gap = result['West'], result['rest'], result['gap']
        # Descriptive labels, not significance tests. Broad gap uses 20 scale points.
        result['mark'] = ('N' if gap <= 0 else 'H' if min(w, r) >= 80 and gap < 20 else
                          'D' if gap >= 20 else 'smaller gap')
        output.append(result)
    if args.check_stata:
        import pandas as pd
        dta = HERE / 'cirights_v3.12.10.24.dta'
        data = pd.read_stata(dta, convert_categoricals=False)
        lookup = {(str(int(r['ciri'])), str(int(r['year']))): r for _, r in data.iterrows() if int(r['year']) in years}
        checks = 0
        for r in rows:
            d = lookup[r['C'], r['B']]
            for col, variable, _, _ in RIGHTS:
                raw = r.get(col, '')
                assert pd.isna(d[variable]) if not raw else float(raw) == d[variable]
                checks += 1
        metadata['format_check'] = f'{checks} practice/right cells agree, XLSX versus Stata'
        metadata['dta_sha256'] = sha(dta)
    # Trafficking is absent outside the US in 2021–2022; check overlapping years only.
    trafficking_rows = [r for r in cleaned if r[3] == 'trafficking_p' and int(r[2]) <= 2020]
    by_country = {}
    for cid, _, _, _, _, score in trafficking_rows:
        by_country.setdefault(cid, []).append(score)
    west_scores = [stats.mean(v) for cid, v in by_country.items() if cid in west]
    rest_scores = [stats.mean(v) for cid, v in by_country.items() if cid not in west]
    metadata['trafficking_common_years'] = {
        'years': [2018, 2019, 2020], 'n_west': len(west_scores), 'n_rest': len(rest_scores),
        'West': stats.mean(west_scores), 'rest': stats.mean(rest_scores),
        'gap': stats.mean(west_scores) - stats.mean(rest_scores)}
    output.sort(key=lambda r: r['gap'], reverse=True)
    (HERE / 'results.json').write_text(json.dumps({'metadata': metadata, 'rights': output}, indent=2))
    for name, fields, data in [
        ('cleaned_window.tsv', ['ciri', 'country_latest_name', 'year', 'variable', 'raw_score', 'normalized_score'], cleaned),
        ('country_means.tsv', ['ciri', 'country', 'variable', 'group', 'n_years', 'normalized_mean'], country_means),
    ]:
        with (HERE / name).open('w') as f:
            writer = csv.writer(f, delimiter='\t'); writer.writerow(fields); writer.writerows(data)
    table = ['| Right (variable; scale) | West | Rest | Gap | Countries W/R | Country-years W/R | Mark |',
             '|---|---:|---:|---:|---:|---:|---|']
    for r in output:
        table.append(f"| {r['right']} (`{r['variable']}`; 0–{r['maximum']}) | {r['West']:.1f} | {r['rest']:.1f} | {r['gap']:+.1f} | {r['n_west']}/{r['n_rest']} | {r['years_west']}/{r['years_rest']} | {r['mark']} |")
    (HERE / 'table.md').write_text('\n'.join(table) + '\n')
    print(json.dumps(metadata, indent=2)); print('\n'.join(table))
    print('All range, unique-id, coverage and taxonomy assertions passed.')


if __name__ == '__main__':
    main()
```
