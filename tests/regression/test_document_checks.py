"""Document scoring omits the character judge and keeps numeric check credit. -- PI/OpenAI"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class DocumentChecksTest(unittest.TestCase):
    def test_capability_only_needs_no_api_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / 'scripts/eval/41_tc_judge.py'
            script.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / 'scripts/eval/41_tc_judge.py', script)
            shutil.copyfile(ROOT / 'scripts/eval/coherence_metrics.py', script.parent / 'coherence_metrics.py')
            checks = root / '.local/tiny-character/src/tiny_character/checks.py'
            checks.parent.mkdir(parents=True)
            checks.write_text('def item_check(check, replies): return {"correct": 0.5}\ndef turn_checks(turn, check): return {"lang_switch": float(turn["assistant"] == "foreign"), "truncated": float(turn["finish_reason"] == "length"), "rep4": 0.0, "length_kept": None, **dict.fromkeys(("looped", "role_confusion", "empty"), 0.0)}\n')
            run8 = root / 'slop/eval/run8'
            run8.mkdir(parents=True)
            (run8 / 'manifest.json').write_text(json.dumps({'protocol_sha256': {
                'src/tiny_character/checks.py': hashlib.sha256(checks.read_bytes()).hexdigest()}}))
            items = [{'id': 'ordinary', 'family': 'capability', 'system': None, 'turns': ['Question'],
                      'judged': False, 'checks': {'kind': 'fixture'}},
                     {'id': 'character', 'family': 'persona', 'system': None, 'turns': ['Values?'],
                      'judged': True, 'checks': None}]
            (run8 / 'items.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in items))
            records = [{'item_id': item['id'], 'model': 'fixture', 'base_model': 'fixture', 'sample': sample,
                        'system': None, 'turns': [{'user': item['turns'][0], 'assistant': 'foreign' if item['judged'] and sample == 0 else 'Answer',
                                                 'finish_reason': 'length' if item['judged'] and sample == 1 else 'stop'}]}
                       for item in items for sample in (0, 1)]
            replies = root / 'replies.jsonl'
            replies.write_text(''.join(json.dumps(r) + '\n' for r in records))
            subprocess.run([sys.executable, str(script), '--capability-only', 'slop/eval/checks', str(replies)],
                           cwd=root, env=os.environ | {'TINY_CHARACTER_DIR': str(root / '.local/tiny-character')},
                           check=True, capture_output=True)
            out = root / 'slop/eval/checks'
            judged = [json.loads(line) for line in (out / 'judged.jsonl').read_text().splitlines()]
            self.assertEqual([r['item_id'] for r in judged], ['ordinary', 'ordinary'])
            self.assertTrue(all('on_target' not in r and r['check']['correct'] == 0.5 for r in judged))
            self.assertEqual(json.loads((out / 'cost.json').read_text())['new_cached_requests'], 0)
            self.assertFalse((root / '.env').exists())
            coherence = list(map(json.loads, (out / 'coherence.jsonl').read_text().splitlines()))
            self.assertEqual(len(coherence), 4)
            self.assertEqual({r['item_id'] for r in coherence}, {'ordinary', 'character'})
            self.assertEqual(json.loads((out / 'meta.json').read_text())['coherence_summary']['fixture']['turns'], 4)
            self.assertEqual(json.loads((out / 'meta.json').read_text())['coherence_summary']['fixture']['lang_switch'], 1)
            renderer = script.parent / '48_run11_doc_table.py'
            shutil.copyfile(ROOT / 'scripts/eval/48_run11_doc_table.py', renderer)
            runs, strength = root / 'runs', root / 'strength'
            runs.mkdir(); strength.mkdir()
            shutil.copyfile(replies, runs / 'replies_fixture.jsonl')
            (runs / 'gsm8k_fixture.jsonl').write_text(''.join(json.dumps({'correct': True}) + '\n' for _ in range(60)))
            (strength / 'summary.md').write_text('| fixture | 50% | [40, 60] | 0/4 |\n')
            table = root / 'table.md'
            subprocess.run([sys.executable, str(renderer), str(table), '--cell', f'Document=fixture@{runs}', '--strength', str(strength)],
                cwd=root, env=os.environ | {'TINY_CHARACTER_DIR': str(root / '.local/tiny-character')}, check=True, capture_output=True)
            summary = json.loads(table.with_suffix('.coherence.json').read_text())['models']['fixture']['summary']
            self.assertEqual((summary['turns'], summary['lang_switch'], summary['looped'], summary['truncated']), (4, 1, 0, 1))
            data = next(line for line in table.read_text().splitlines() if '[Document]' in line)
            cells = [x.strip() for x in data.split('|')[1:-1]]
            self.assertEqual(cells[1:4], ['50% [40, 60]', '1 / 0 / 1', '4'])
            self.assertEqual(cells[5], '60')

    def test_paired_report_includes_documents_without_character_scores(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runs, judged, strength = [root / name for name in ('runs', 'judged', 'strength')]
            for path in (runs, judged, strength):
                path.mkdir()
            item = next(r for r in map(json.loads, (ROOT / 'slop/eval/run8/items.jsonl').read_text().splitlines())
                        if r['family'] == 'capability')['id']
            records, trials = [], []
            for model, credit in [('r8_a0_b0', 1.0), ('r10_document', 0.5)]:
                if model == 'r8_a0_b0':
                    (runs / f'gsm8k_{model}.jsonl').write_text(''.join(json.dumps({'correct': True}) + '\n' for _ in range(60)))
                for sample in (0, 1):
                    records.append({'model': model, 'item_id': item, 'family': 'capability', 'check': {'correct': credit}})
                    trials.append({'model': model, 'item_id': item, 'separated': bool(sample) or model == 'r10_document'})
            (judged / 'judged.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
            (strength / 'trials.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in trials))
            out = root / 'paired.md'
            subprocess.run([sys.executable, str(ROOT / 'scripts/eval/43_paired_ablation.py'), 'r8_a0_b0', str(out), str(runs),
                            '--judged', str(judged), '--strength', str(strength)], check=True, capture_output=True)
            text = out.read_text()
            self.assertIn('Character was not measured.', text)
            self.assertNotIn('| Character |', text)
            self.assertIn('| r8_a0_b0 | 50% | ref | 60 | 2/2 |', text)
            self.assertIn('| r10_document | 100%', text)
            self.assertIn('| not run | 1/2 |', text)


if __name__ == '__main__':
    unittest.main()
