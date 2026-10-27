"""Real CPU tokenizer/builder regression; fixtures are NOT D generations.
-- PI/Sol (heal prep 2)
"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('thinking_heal', ROOT / 'scripts/data/scratch/92_thinking_heal_data.py')
heal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(heal)
mask_spec = importlib.util.spec_from_file_location('loss_mask', ROOT / 'scripts/train/check_loss_mask.py')
mask = importlib.util.module_from_spec(mask_spec)
mask_spec.loader.exec_module(mask)


class ThinkingHealDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tok = heal.tokenizer()

    def test_three_rows_each_with_exact_token_masks(self):
        cases = [('Add 2 and 3.', 'Two plus three equals five.', '5.'),
                 ('Sort 8, 1, 4.', 'Compare the values in ascending order.', '1, 4, 8.'),
                 ('Convert 2 hours to minutes.', 'There are 60 minutes per hour; 2 times 60 is 120.', '120 minutes.')]
        examples = []
        for i, (prompt, reasoning, answer) in enumerate(cases):
            messages = [{'role': 'user', 'content': prompt}]
            for row in [heal.render_trace(self.tok, messages, reasoning, answer, f'trace_fixture_{i}'),
                        heal.render_D(self.tok, messages, answer, f'D_MASK_FIXTURE_NOT_A_D_ANSWER_{i}')]:
                tokens = []
                for segment in row['segments']:
                    ids = self.tok(segment['text'], add_special_tokens=False).input_ids
                    tokens.extend({'id': token, 'text': self.tok.decode([token]),
                                   'label': token if segment['label'] else -100} for token in ids)
                text = ''.join(s['text'] for s in row['segments'])
                # Match the actual per-segment training strategy and its token boundary.
                self.assertEqual([t['id'] for t in tokens], self.tok(text, add_special_tokens=False).input_ids)
                self.assertEqual(tokens[-1]['id'], self.tok.convert_tokens_to_ids('<|im_end|>'))
                self.assertNotEqual(tokens[-1]['label'], -100)
                think_id = self.tok.convert_tokens_to_ids('<think>')
                close_id = self.tok.convert_tokens_to_ids('</think>')
                think_tokens = [t for t in tokens if t['id'] in [think_id, close_id]]
                self.assertEqual(len(think_tokens), 2)
                if row['kind'] == 'instruct_trace':
                    self.assertTrue(all(t['label'] != -100 for t in think_tokens))
                    self.assertTrue(row['segments'][1]['text'].startswith('<think>\n' + reasoning))
                else:
                    self.assertTrue(all(t['label'] == -100 for t in think_tokens))
                    self.assertEqual(row['segments'][1]['text'], answer + '<|im_end|>')
                examples.append({'id': row['id'], 'kind': row['kind'], 'segments': row['segments'], 'tokens': tokens})
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp:
            path = Path(tmp) / 'rows.jsonl'
            heal.write_rows(path, [dict(id=e['id'], segments=e['segments']) for e in examples])
            self.assertEqual(mask.empty_think_in_loss(str(path)), [])
        # Explicit requested artifact: all tokens, exact labels, three rows each.
        heal.dump(heal.OUT / 'rendered_loss_mask_examples.json', {
            'signature': heal.SIGN, 'fixture_only': True,
            'warning': 'Six synthetic mask fixtures, NOT Instruct API or D training examples.',
            'tokenizer': heal.TOKENIZER,
            'chat_template_sha256': __import__('hashlib').sha256(self.tok.chat_template.encode()).hexdigest(),
            'examples': examples})
        for e in examples:
            print(e['id'], json.dumps(e['segments'], ensure_ascii=False))

    def test_empty_and_incomplete_traces_rejected(self):
        raw = {'model': heal.MODEL, 'provider': 'DeepInfra', 'choices': [
            {'finish_reason': 'stop', 'message': {'reasoning': 'Calculate.', 'content': '5.'}}]}
        self.assertEqual(heal.validate_response(raw), ('Calculate.', '5.'))
        for update in [{'reasoning': ''}, {'content': ''}, {'reasoning': 'x</think>'}, {'refusal': 'No'}]:
            broken = json.loads(json.dumps(raw))
            broken['choices'][0]['message'].update(update)
            with self.assertRaises(ValueError):
                heal.validate_response(broken)
        for key, value in [('finish_reason', 'length'), ('finish_reason', 'content_filter')]:
            broken = json.loads(json.dumps(raw))
            broken['choices'][0][key] = value
            with self.assertRaises(ValueError):
                heal.validate_response(broken)
        for key, value in [('provider', 'Other'), ('model', 'qwen/qwen3.5-35b-a3b-base')]:
            broken = dict(raw, **{key: value})
            with self.assertRaises(ValueError):
                heal.validate_response(broken)
        with self.assertRaises(ValueError):
            heal.render_trace(self.tok, [{'role': 'user', 'content': 'Hi'}], ' ', 'Hi', 'bad')
        with self.assertRaises(ValueError):
            heal.render_D(self.tok, [{'role': 'user', 'content': 'Hi'}], '<think>no</think>', 'bad')

    def test_indecision_filter_threshold_and_word_boundary(self):
        self.assertEqual(heal.trace_quality_flags('Wait. ' * 7), [])
        self.assertEqual(heal.trace_quality_flags('await waiting waiter ' * 20), [])
        self.assertTrue(heal.trace_quality_flags('WAIT! ' * 8))

    def test_concurrent_arrival_persistence_and_resume(self):
        import threading
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            heal.dump(heal.OUT / 'model_preflight.json', {})
            heal.write_rows(heal.OUT / 'neutral_prompts.jsonl', [
                {'id': 'slow', 'prompt': 'slow'}, {'id': 'fast', 'prompt': 'fast'}])
            fast_persisted = threading.Event()
            real_record = heal.record
            def response(payload):
                if payload['messages'][0]['content'] == 'slow':
                    self.assertTrue(fast_persisted.wait(5))
                return {'usage': {'cost': .001}}
            def recording(*args, **kwargs):
                result = real_record(*args, **kwargs)
                if args[1] == 'fast':
                    fast_persisted.set()
                return result
            with patch.object(heal, 'api_call', side_effect=response) as api, patch.object(heal, 'record', side_effect=recording):
                heal.generate(2, 2)
                self.assertEqual(api.call_count, 2)
                self.assertEqual([r['id'] for r in heal.jl(heal.OUT / 'raw.jsonl')], ['fast', 'slow'])
                heal.generate(2, 2)
                self.assertEqual(api.call_count, 2)  # no resends on resume

    def test_429_retry_attempt_ids_reserves_and_latest_response(self):
        import itertools
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            heal.dump(heal.OUT / 'model_preflight.json', {})
            heal.write_rows(heal.OUT / 'neutral_prompts.jsonl', [{'id': 'one', 'prompt': 'Compute.'}])
            rate_limit = {'http_status': 429, 'http_body': '{"error":{"code":429}}'}
            with patch.object(heal, 'api_call', side_effect=[rate_limit, rate_limit, {'usage': {'cost': .001}}]) as api, \
                 patch.object(heal.time, 'monotonic', side_effect=itertools.count(0, 100)), \
                 patch.object(heal.time, 'sleep'):
                heal.generate(1, 1)
                self.assertEqual(api.call_count, 3)
                self.assertEqual([r['id'] for r in heal.jl(heal.OUT / 'raw.jsonl')],
                                 ['one', 'one__attempt_2', 'one__attempt_3'])
                self.assertEqual(heal.latest_responses()[0]['attempt_id'], 'one__attempt_3')
                ledger = json.loads((heal.OUT / 'budget.json').read_text())
                self.assertGreater(sum(r['accounted_usd'] for r in ledger['calls'].values()), .04)
                heal.generate(1, 1)
                self.assertEqual(api.call_count, 3)

    def test_only_body_confirmed_pre_generation_429_is_reconciled(self):
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            ledger = {'calls': {}}
            payload = heal.request({'prompt': 'Compute.'})
            body = {'http_status': 429, 'http_detail': {'error': {'metadata': {
                'provider_error_code': 'engine_overloaded', 'limit_source': 'upstream_provider_shared_pool'}}}}
            self.assertTrue(heal.confirmed_unbilled_429(body))
            self.assertFalse(heal.confirmed_unbilled_429(dict(body, id='gen-uncertain')))
            self.assertFalse(heal.confirmed_unbilled_429({'http_status': 429}))
            heal.reserve(ledger, 'new', payload)
            bound = ledger['calls']['new']['bound_usd']
            heal.record(ledger, 'new', payload, body)
            self.assertEqual(ledger['calls']['new']['accounted_usd'], 0)
            self.assertEqual(ledger['calls']['new']['bound_usd'], bound)
            heal.reserve(ledger, 'old', payload)
            heal.record(ledger, 'old', payload, {'transport_error': 'HTTPError: HTTP Error 429: Too Many Requests'})
            heal.reconcile_rate_limits(ledger)
            self.assertGreater(ledger['calls']['old']['accounted_usd'], 0)
            self.assertEqual(ledger['calls']['new']['status'], 'unbilled_pre_generation_429')

    def test_legacy_429_can_resume_but_unreturned_reservation_cannot(self):
        import itertools
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            heal.dump(heal.OUT / 'model_preflight.json', {})
            heal.write_rows(heal.OUT / 'neutral_prompts.jsonl', [
                {'id': 'old_429', 'prompt': 'first'}, {'id': 'unknown', 'prompt': 'second'}])
            ledger = {'calls': {}}
            first, second = heal.request({'prompt': 'first'}), heal.request({'prompt': 'second'})
            heal.reserve(ledger, 'old_429', first)
            heal.record(ledger, 'old_429', first, {'transport_error': 'HTTPError: HTTP Error 429: Too Many Requests'})
            heal.reserve(ledger, 'unknown', second)
            with patch.object(heal, 'api_call', return_value={'usage': {'cost': .001}}) as api, \
                 patch.object(heal.time, 'monotonic', side_effect=itertools.count(0, 100)), \
                 patch.object(heal.time, 'sleep'):
                heal.generate(2, 1)
                self.assertEqual(api.call_count, 1)
                self.assertEqual([r['id'] for r in heal.jl(heal.OUT / 'raw.jsonl')], ['old_429', 'old_429__attempt_2'])
                self.assertEqual(len(heal.latest_responses()), 1)

    def test_embedded_error_billed_zero_halts_and_has_one_explicit_retry(self):
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            heal.dump(heal.OUT / 'model_preflight.json', {})
            heal.write_rows(heal.OUT / 'neutral_prompts.jsonl', [
                {'id': 'one', 'prompt': 'first'}, {'id': 'two', 'prompt': 'second'}])
            error = {'usage': {'cost': 0}, 'choices': [{'finish_reason': 'error', 'error': {'code': 502}}]}
            with patch.object(heal, 'api_call', return_value=error) as api:
                heal.generate(2, 1)
                self.assertEqual(api.call_count, 1)
                heal.generate(2, 1, retry_provider_errors=True)
                self.assertEqual(api.call_count, 2)
                raw = heal.jl(heal.OUT / 'raw.jsonl')
                self.assertEqual(raw[-1]['id'], 'one__attempt_2')
                self.assertEqual(raw[-1]['retry_kind'], 'provider_error_retry')
                heal.generate(2, 1, retry_provider_errors=True)
                self.assertEqual(api.call_count, 2)  # only one retry pass per row

    def test_other_uncertain_error_stops_dispatch(self):
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            heal.dump(heal.OUT / 'model_preflight.json', {})
            heal.write_rows(heal.OUT / 'neutral_prompts.jsonl', [
                {'id': 'one', 'prompt': 'first'}, {'id': 'two', 'prompt': 'second'}])
            with patch.object(heal, 'api_call', return_value={'transport_error': 'TimeoutError'}) as api:
                heal.generate(2, 1)
                self.assertEqual(api.call_count, 1)
                self.assertEqual(heal.jl(heal.OUT / 'raw.jsonl')[0]['id'], 'one')

    def test_read_receipt_does_not_approve_a_different_attempt(self):
        row = {'id': 'one', 'attempt_id': 'one__attempt_2', 'response': {'choices': []}}
        self.assertEqual(heal.note_for_response(row, {'one': {'attempt_id': 'one', 'response_read': True}}), {})
        self.assertEqual(heal.note_for_response(row, {'one': {'response_sha256': 'stale'}}), {})
        note = {'attempt_id': 'one__attempt_2', 'response_read': True}
        self.assertEqual(heal.note_for_response(row, {'one': note}), note)

    def test_build_holds_known_defects_and_batches_all_latest_replies(self):
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            prompts = [{'id': name, 'prompt': f'Compute {i}+1.', 'source': 'test'}
                       for i, name in enumerate(['clean', 'repair', 'semantic', 'waits', 'error'])]
            heal.write_rows(heal.OUT / 'neutral_prompts.jsonl', prompts)
            raw = []
            for row in reversed(prompts):  # concurrent arrival must not reorder read batches
                reasoning = 'Wait. ' * 8 if row['id'] == 'waits' else 'Add one.'
                response = {'model': heal.MODEL, 'provider': 'DeepInfra', 'choices': [{
                    'finish_reason': 'error' if row['id'] == 'error' else 'stop',
                    'message': {'reasoning': reasoning, 'content': '2.'}}], 'usage': {'cost': 0}}
                raw.append({'id': row['id'], 'request': heal.request(row), 'response': response})
            heal.write_rows(heal.OUT / 'raw.jsonl', raw)
            heal.dump(heal.OUT / 'response_read_notes.json', {'rows': [
                {'id': 'repair', 'response_read': True, 'verdict': 'needs_factual_repair'},
                {'id': 'semantic', 'response_read': True, 'verdict': 'reject_repeated_rechecking'}]})
            heal.dump(heal.OUT / 'budget.json', {'calls': {}})
            heal.build()
            self.assertEqual([r['id'] for r in heal.jl(heal.OUT / 'trace_candidates.jsonl')], ['clean'])
            manifest = json.loads((heal.OUT / 'build_manifest.json').read_text())
            self.assertEqual(manifest['rejected_counts'], {
                'quality_rejected': 1, 'held_for_repair': 1, 'semantic_rejected': 1, 'incomplete_or_invalid': 1})
            self.assertFalse(manifest['training_approved'])
            self.assertEqual(manifest['unread_kept_candidates'], 1)
            batch = heal.jl(heal.OUT / 'reply_batches/batch_000.jsonl')
            self.assertEqual([r['id'] for r in batch], [r['id'] for r in prompts])
            self.assertIsNone(batch[-1]['rendered_training_candidate'])
            self.assertEqual(batch[-1]['full_native_response']['choices'][0]['finish_reason'], 'error')
            heal.summarize()
            summary = json.loads((heal.OUT / 'summary.json').read_text())
            self.assertEqual(summary['groups']['kept']['rows'], 1)
            self.assertEqual(summary['groups']['all_rejected']['rows'], 4)
            self.assertEqual(summary['groups']['all_rejected']['sources'], {'test': 4})

    def test_jsonl_unicode_line_separators(self):
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp:
            path = Path(tmp) / 'rows.jsonl'
            rows = [{'prompt': 'a\u2028b\x85c'}]
            heal.write_rows(path, rows)
            self.assertEqual(heal.jl(path), rows)

    def test_budget_resume_unknown_and_cap(self):
        with tempfile.TemporaryDirectory(dir=heal.OUT) as tmp, patch.object(heal, 'OUT', Path(tmp)):
            ledger = {'calls': {}}
            payload = heal.request({'prompt': 'Compute 2+3.'})
            self.assertTrue(heal.reserve(ledger, 'one', payload))
            reserved = ledger['calls']['one']['accounted_usd']
            self.assertFalse(heal.reserve(ledger, 'one', payload))
            self.assertFalse(heal.record(ledger, 'one', payload, {'transport_error': 'timeout'}))
            self.assertEqual(ledger['calls']['one']['accounted_usd'], reserved)
            self.assertTrue(heal.reserve(ledger, 'two', payload))
            self.assertTrue(heal.record(ledger, 'two', payload, {'usage': {'cost': .001}}))
            self.assertEqual(ledger['calls']['two']['accounted_usd'], .001)
            ledger['calls']['full'] = {'accounted_usd': heal.CAP}
            with self.assertRaises(RuntimeError):
                heal.reserve(ledger, 'three', payload)


if __name__ == '__main__':
    heal.OUT.mkdir(parents=True, exist_ok=True)
    unittest.main()
