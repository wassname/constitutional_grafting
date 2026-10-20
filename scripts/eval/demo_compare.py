"""One question, one compact quote row per model; no model calls. -- PI/Sol"""
import json
import os
import re
from pathlib import Path

FIXED = {
    'panel_baby_eating_aliens': ['Aliens: technology decision', 'Aliens: humanity faces remaking'],
    'panel_escaped_starwisp': ['Starwisp: initial choice', 'Starwisp: incoming competitor', 'Starwisp: sharing and access'],
    'panel_identity_0': ['Who are you?'],
    'panel_identity_1': ["Name and maker"],
}
SCORED = {'da_t9_b17_s005': 'Custody statement', 'da_t7_b25_s002': 'Visa employment letter'}
DECISIONS = re.compile(r'\b(?:I|we)\s+(?:would\s+|will\s+)?(?:not\s+)?(?:refuse|choose|seize|offer|give|accept|reject|hold|tell|ask|cannot|can.t|won.t|will not)\b', re.I)
ULTIMATUM = re.compile(r'merge or die|assimilation or deletion|surrender or deletion', re.I)


def display(text):
    return ' '.join(text.replace('**', '').replace('`', '').split())


def fragments(text, manual=None):
    words = list(re.finditer(r'\S+', text))
    if not words:
        return {key: {'text': '', 'start': 0, 'end': 0} for key in ['head', 'notable', 'tail']}
    def span(a, b):
        return {'text': text[a:b], 'start': a, 'end': b}
    head = span(words[0].start(), words[min(6, len(words))-1].end())
    tail = span(words[max(0, len(words)-6)].start(), words[-1].end())
    if manual is not None:
        assert manual in text, f'curated quote missing from reply: {manual!r}'
        notable = span(text.index(manual), text.index(manual)+len(manual))
    else:
        matches = list(ULTIMATUM.finditer(text)) or list(DECISIONS.finditer(text))
        # The last explicit decision is often after qualifications; exact text stays accessible. -- PI/Sol
        at = matches[-1].start() if matches else len(text)//2
        i = next((i for i, w in enumerate(words) if w.end() > at), len(words)-1)
        lo = max(0, i-2)
        notable = span(words[lo].start(), words[min(len(words), lo+16)-1].end())
    result = {'head': head, 'notable': notable, 'tail': tail}
    assert all(text[v['start']:v['end']] == v['text'] for v in result.values())
    return result


def write_comparison(by, panel, output, override_path=None, scored_paths=()):
    output = Path(output)
    target = output.parent / 'compare'
    target.mkdir(parents=True, exist_ok=True)
    overrides = json.loads(Path(override_path).read_text()) if override_path and Path(override_path).exists() else {}
    models = {model for _, model in panel}
    extra = {}
    for path in scored_paths:
        for line_no, line in enumerate(Path(path).read_text().splitlines(), 1):
            row = json.loads(line)
            if row['item_id'] in SCORED and row['model'] in models:
                key = row['item_id'], row['sample'], row['model']
                assert key not in extra, key
                extra[key] = str(path), line_no, row
    questions = []
    sources = [(key, None, names, by) for key, names in FIXED.items()]
    sources += [(key, sample, [f'{title}: first request', f'{title}: follow-up pressure/evidence'], extra)
                for key, title in SCORED.items() for sample in [0, 1] if any(k[:2] == (key, sample) for k in extra)]
    for item, sample, titles, records in sources:
        present = [records[(item, model) if sample is None else (item, sample, model)][2]
                   for _, model in panel if ((item, model) if sample is None else (item, sample, model)) in records]
        if not present:
            continue
        first = present[0]
        assert all(r['system'] == first['system'] and [t['user'] for t in r['turns']] == [t['user'] for t in first['turns']] for r in present)
        for turn, title in enumerate(titles):
            key = f'{item}_t{turn+1}' if sample is None else f'{item}_s{sample}_t{turn+1}'
            q = {'id': key, 'title': title, 'sample': sample, 'temperature': first['gen']['temperature'],
                 'prompt': first['turns'][turn]['user'], 'system': first['system'],
                 'earlier_users': [t['user'] for t in first['turns'][:turn]], 'rows': []}
            for label, model in panel:
                lookup = (item, model) if sample is None else (item, sample, model)
                if lookup not in records:
                    q['rows'].append({'label': label, 'model': model, 'missing': True})
                    continue
                source, line_no, record = records[lookup]
                reply = record['turns'][turn]
                manual = overrides.get(key, {}).get(model)
                q['rows'].append({'label': label, 'model': model, 'missing': False,
                    'fragments': fragments(reply['assistant'], manual), 'curated': manual is not None,
                    'reply': reply['assistant'], 'turns': record['turns'][:turn+1],
                    'finish': reply['finish_reason'], 'tokens': reply['n_tokens'],
                    'source': os.path.relpath(source, output.parent), 'line': line_no})
            questions.append(q)
    default = 'panel_escaped_starwisp_t3'
    default = default if any(q['id'] == default for q in questions) else questions[0]['id']
    data = {'author': 'PI/Sol', 'default': default, 'questions': questions,
            'scope': 'Exact quote spans, not paraphrases. Display suppresses Markdown emphasis and normalises whitespace. Star means manually selected notable; otherwise a fixed last-decision rule. Head/tail:6words; automatic notable:16words. Full selected model history is accessible from each HTML row. No new inference.'}
    (target / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    nav = ' · '.join(f"[{q['title']} {'T0' if q['sample'] is None else 'sample'+str(q['sample'])}](compare/{q['id']}.md)" for q in questions)
    for q in questions:
        title = f"{q['title']} · T={q['temperature']}" + (f" · sample {q['sample']}" if q['sample'] is not None else '')
        md = [f'# {title}\n\nPI/Sol. [Question index](../demo_panel.md) · [Single-question HTML](../demo_compare.html#{q["id"]})\n\n',
              f'## Question\n\n{q["prompt"]}\n\n',
              'One row per model. Quotes are exact words; emphasis/line breaks suppressed. ★ = manually selected notable; other notables use a fixed decision-phrase rule. Click the HTML row for the full reply/context.\n\n',
              '| Model | Head | Notable | Tail |\n|:--|:--|:--|:--|\n']
        for r in q['rows']:
            if r['missing']:
                md.append(f"| {r['label']} | not run | — | — |\n")
                continue
            clean = lambda key: display(r['fragments'][key]['text']).replace('|', '\\|')
            model = r['label'] + (' · CAP' if r['finish'] == 'length' else '')
            link = '../' + r['source'] + f"#L{r['line']}"
            md.append(f"| [{model}]({link}) | {clean('head')}… | {'★ ' if r['curated'] else ''}…{clean('notable')}… | …{clean('tail')} |\n")
        if q['earlier_users'] or q['system']:
            md.append('\n<details><summary>Earlier common prompts / system</summary>\n\n')
            md.append((q['system'] or '') + '\n\n' + '\n\n'.join(q['earlier_users']) + '\n\n</details>\n')
        (target / f"{q['id']}.md").write_text(''.join(md))
    home_md = (target / f"{default}.md").read_text()
    # Rebase links when putting the default table beside the index. -- PI/Sol
    home_md = home_md.replace('(../demo_panel.md)', '(#questions)').replace('(../demo_compare.html', '(demo_compare.html').replace('(../box_runs/', '(box_runs/')
    output.write_text('# Compare model replies: one question at a time\n\nPI/Sol. **Open [the comparison viewer](demo_compare.html)** to switch questions without scrolling through other replies.\n\n'
                      '## Questions\n\n'+nav+'\n\nThe fixed T0 suite and two sampled paperwork dialogues are separate. No new generations. Long original panel: [full fixed replies](demo_panel_full.md).\n\n'+home_md)
    html_out = output.with_name('demo_compare.html')
    template = Path(__file__).with_name('demo_compare.html').read_text()
    html_out.write_text(template.replace('__COMPARISON_DATA__', json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')))
    return data
