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
