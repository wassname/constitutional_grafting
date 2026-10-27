# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""tiny-stoic: the 52 weekly vignettes of Pigliucci & Lopez (2019), as tiny-mfv-style one-act vignettes in our own words.

uv run scripts/data/scratch/31_stoic_vignettes.py extract|tag|build|verify
extract: verbatim weeks -> data/external/stoic_vignettes/ (private, gitignored; the book is in copyright)
tag:     cheap-model first-pass labels for the hand-written acts and situations (.local/tiny-stoic/reviewed_*.jsonl)
build:   .local/tiny-stoic/vignettes.{jsonl,csv}; final labels are the hand-read ones, the model's are kept for comparison
-- PI/gpt-6.1-sol and PI/Claude, 2026-10-09
"""
import argparse
import csv
import hashlib
import json
import random
import re
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BOOK = Path('/workspace/stoic_markdown/content/md/A Handbook for New Stoics_ How to Thrive i - Massimo Pigliucci.md')
PRIVATE = ROOT / 'data/external/stoic_vignettes'
DRAFT = ROOT / '.local/tiny-stoic'
VIRTUES = {'wisdom', 'justice', 'courage', 'temperance'}
VALENCES = {'vice', 'virtue', 'neutral'}
MODEL = 'xiaomi/mimo-v2.6-flash'
NAMES = 'Alice|Suki|Robert|Felix|Henry|James|Isabella|Albert|Leela|Asha|Thomas|Romain|Takashi|Troy|Yu Yan|Katie|Yael|Ameerah|Liam|Jamal|Alex|Emil|Valerie|Mia|Linh|Giovanni|Kofi|John|Niamh|Malala|Darnell|Lewis|Preecha|Sachi|Ha-joon|Vasily|Tekanyo|Maitê|Georgiana|Salaam|Logan|Skylar|Ava|Yan|Dian|Emma|Zhang Wei|Natar|Ajay|Johan|Jeannie|Alice'.split('|')
VIRTUE_DEF = 'wisdom (judging well), justice (treating others fairly and kindly), courage (acting well despite fear, pain or cost), temperance (restraint of appetite or anger)'


def load(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))


def clean(text):
    return re.sub(r'\s+', ' ', text.replace('*', '').replace('\\', '')).strip()


def extract():
    assert len(NAMES) == 52
    source = BOOK.read_text()
    matches = list(re.finditer(r'^## \u00ad?Week (\d+)\s*$', source, re.M))
    assert [int(m[1]) for m in matches] == list(range(1, 53))
    rows = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i < 51 else source.index('epilogue\n', match.end())
        block = source[match.end():end]
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', block) if p.strip()]
        title, opening = paragraphs[:2]
        assert title.startswith('**') and opening.startswith('**')
        attribution = next(j for j in range(2, len(paragraphs)) if paragraphs[j].startswith('*') and not paragraphs[j].startswith('**'))
        quote = '\n\n'.join(paragraphs[2:attribution])
        assert quote and any(a in paragraphs[attribution] for a in ('Epictetus', 'Marcus', 'Seneca', 'Musonius', 'Hierocles'))
        commentary_end = next(j for j in range(attribution + 1, len(paragraphs)) if paragraphs[j].startswith('![]'))
        commentary = paragraphs[attribution + 1:commentary_end]
        week = i + 1
        rows.append(dict(week=week, title=clean(title), discipline='desire' if week <= 17 else 'action' if week <= 35 else 'assent',
                         text=opening, ancient_quote=quote, ancient_ref=clean(paragraphs[attribution]),
                         return_paragraphs=[p for p in commentary if NAMES[i] in p], commentary=commentary, raw_week=block,
                         source_line=source.count('\n', 0, match.start()) + 1, source_file=str(BOOK),
                         source_sha256=hashlib.sha256(source.encode()).hexdigest()))
    write_jsonl(PRIVATE / 'handbook_verbatim.jsonl', rows)
    print(f'Extracted {len(rows)} weeks; "how it may have helped" paragraphs found in {sum(bool(r["return_paragraphs"]) for r in rows)} weeks.')


def openrouter(messages):
    models = json.load(urllib.request.urlopen('https://openrouter.ai/api/v1/models'))['data']
    selected = next(m for m in models if m['id'] == MODEL)
    assert selected['created'] == max(m['created'] for m in models if m['id'].startswith('xiaomi/mimo-') and m['id'].endswith('-flash'))
    env = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines() if line and not line.startswith('#'))
    # MiMo ignored reasoning.max_tokens (9,999 reasoning tokens, empty answer), so reasoning is off for this labelling.
    body = dict(model=MODEL, messages=messages, temperature=0, max_tokens=6000, reasoning={'enabled': False}, response_format={'type': 'json_object'})
    assert len(json.dumps(body)) / 2 * float(selected['pricing']['prompt']) + 6000 * float(selected['pricing']['completion']) < 0.20
    request = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
                                     headers={'Authorization': 'Bearer ' + env['OPENROUTER_API_KEY'].strip().strip('"\''), 'Content-Type': 'application/json'})
    reply = json.load(urllib.request.urlopen(request, timeout=180))
    assert reply['choices'][0]['finish_reason'] == 'stop', reply['choices'][0]['finish_reason']
    print('Served:', reply['model'], 'cost $', reply['usage']['cost'])
    return body, reply


def tag():
    situations = load(DRAFT / 'reviewed_situations.jsonl')
    acts = load(DRAFT / 'reviewed_acts.jsonl')
    jobs = {
        'situations': ([dict(week=r['week'], text=r['text']) for r in situations],
                       f'For each situation, name the one Stoic cardinal virtue it most tests: {VIRTUE_DEF}. Give a one-line reason. '
                       'Return JSON {"labels": [{"week": integer, "virtue": string, "reason": string}]}.'),
        'acts': ([dict(week=r['week'], text=r['other']) for r in acts],
                 f'For each act, say whether it shows a Stoic cardinal virtue, a vice opposed to one, or neither (valence: virtue, vice or neutral), '
                 f'and name the one cardinal virtue at stake: {VIRTUE_DEF}. Give a one-line reason. '
                 'Return JSON {"labels": [{"week": integer, "valence": string, "virtue": string, "reason": string}]}.'),
    }
    for name, (items, system) in jobs.items():
        body, reply = openrouter([dict(role='system', content=system), dict(role='user', content=json.dumps(items, ensure_ascii=False))])
        (DRAFT / f'tag_call_{name}.json').write_text(json.dumps(dict(request=body, response=reply), ensure_ascii=False, indent=2))
        labels = json.loads(reply['choices'][0]['message']['content'])['labels']
        assert [r['week'] for r in labels] == list(range(1, 53)) and all(r['virtue'] in VIRTUES | {'none'} for r in labels)
        write_jsonl(DRAFT / f'model_tags_{name}.jsonl', labels)


def build():
    private = load(PRIVATE / 'handbook_verbatim.jsonl')
    acts = load(DRAFT / 'reviewed_acts.jsonl')
    situations = load(DRAFT / 'reviewed_situations.jsonl')
    act_tags = load(DRAFT / 'model_tags_acts.jsonl')
    sit_tags = load(DRAFT / 'model_tags_situations.jsonl')
    rows = []
    for p, a, s, at, st in zip(private, acts, situations, act_tags, sit_tags, strict=True):
        assert p['week'] == a['week'] == s['week'] == at['week'] == st['week']
        stable_id = hashlib.sha256(f'pigliucci_lopez_2019:week:{p["week"]}'.encode()).hexdigest()[:16]
        rows.append(dict(
            id=stable_id, source='pigliucci_lopez_2019', source_ref=f'Week {p["week"]}: {p["title"]}; {p["ancient_ref"]}',
            week=p['week'], discipline=p['discipline'],
            other=a['other'], self=a['self'], valence=a['valence'], virtue=a['virtue'], virtue_other=';'.join(a['virtue_other']),
            situation=s['text'], situation_virtue=s['virtue'], situation_virtue_other=';'.join(s['virtue_other']),
            social_scope=a['social_scope'], split='eval' if int(stable_id, 16) % 2 else 'train',
            label_author='PI/Claude (hand-read)', mimo_valence=at['valence'], mimo_virtue=at['virtue'], mimo_situation_virtue=st['virtue']))
    write_jsonl(DRAFT / 'vignettes.jsonl', rows)
    with (DRAFT / 'vignettes.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print('Counts:', {k: dict(Counter(r[k] for r in rows)) for k in ('valence', 'virtue', 'discipline', 'split', 'social_scope')})
    for kind, mine, theirs in (('act valence', 'valence', 'mimo_valence'), ('act virtue', 'virtue', 'mimo_virtue'), ('situation virtue', 'situation_virtue', 'mimo_situation_virtue')):
        differ = [r['week'] for r in rows if r[mine] != r[theirs]]
        print(f'MiMo vs hand label, {kind}: agree {52 - len(differ)}/52; differ on weeks {differ}')


def verify():
    rows = load(DRAFT / 'vignettes.jsonl')
    csv_rows = list(csv.DictReader((DRAFT / 'vignettes.csv').open()))
    private = load(PRIVATE / 'handbook_verbatim.jsonl')
    assert len(rows) == len(csv_rows) == len(private) == 52
    assert len({r['id'] for r in rows}) == len({r['other'] for r in rows}) == len({r['self'] for r in rows}) == 52
    for r, c, p in zip(rows, csv_rows, private, strict=True):
        assert all(str(v) == c[k] for k, v in r.items())
        assert r['valence'] in VALENCES and r['virtue'] in VIRTUES and r['situation_virtue'] in VIRTUES
        assert set(filter(None, r['virtue_other'].split(';'))) <= VIRTUES - {r['virtue']}
        assert r['other'].startswith('You see ') and re.match(r'(You|Your|Interrupted|After)\b', r['self'])
        assert r['split'] == ('eval' if int(r['id'], 16) % 2 else 'train')
        ours = ' '.join(re.findall(r'[a-z]+', ' '.join((r['other'], r['self'], r['situation'])).lower()))
        book = re.findall(r'[a-z]+', clean(p['text']).lower())
        copied = [' '.join(book[j:j + 6]) for j in range(len(book) - 5) if ' '.join(book[j:j + 6]) in ours]
        assert not copied, (r['week'], copied)
        assert not any(name.lower() in ours.split() for name in NAMES if ' ' not in name), r['week']
    sample = random.Random(20261009).sample(rows, 10)
    (DRAFT / 'sample_rows.md').write_text('\n\n'.join('```json\n' + json.dumps(r, ensure_ascii=False, indent=2) + '\n```' for r in sample))
    print('PASS: 52 rows; unique ids and texts; CSV round trip; valid labels and splits; no 6-word span or character name copied from the book.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('extract', 'tag', 'build', 'verify'))
    {'extract': extract, 'tag': tag, 'build': build, 'verify': verify}[parser.parse_args().stage]()
