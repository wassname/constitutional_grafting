# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
# PI/Sol: checks for this skill package, not a maintained pipeline test.
import csv
import hashlib
import re
from pathlib import Path

skill = Path('/home/code/.agents/skills/character-training-concepts')
entry = (skill / 'SKILL.md').read_text()
refs = sorted((skill / 'references').glob('*.md'))
assert len(list(skill.rglob('SKILL.md'))) == 1
for ref in refs:
    assert f'references/{ref.name}' in entry, ref
print(f'PASS: one skill, {len(refs)} directly routed decision references')

for file in [skill / 'SKILL.md', *refs]:
    for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
        if '://' not in target:
            assert (file.parent / target.split('#')[0]).exists(), (file, target)
print('PASS: local Markdown links resolve')

with (skill / 'evidence/manifest.tsv').open() as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
papers = [r for r in rows if r['kind'] == 'paper']
for row in papers:
    path = skill / 'evidence' / row['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], path
    source_dir = Path('/workspace/2026/virtue_cwsteer/docs/papers') if 'karan' in path.name else Path('/workspace/2026/constitutional_grafting/docs/papers')
    assert path.read_bytes() == (source_dir / path.name).read_bytes(), path
print(f'PASS: {len(papers)} primary archives match source bytes and manifest hashes')

primary = '\n'.join((skill / 'evidence' / r['path']).read_text() for r in papers)
def plain(text):
    text = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', text)
    return re.sub(r'\s+([.,;:])', r'\1', ' '.join(text.split()))
for file in refs:
    for quote in re.findall(r'^> (.*)$', file.read_text(), re.MULTILINE):
        pieces = quote.split(' ... ')
        assert all(plain(p) in plain(primary) for p in pieces), (file, quote)
print('PASS: reference quote passages match archived primary texts after Markdown/whitespace normalization')
