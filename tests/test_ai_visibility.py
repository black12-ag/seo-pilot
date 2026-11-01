import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/seo-pilot/scripts/ai_visibility.py'


def observation(**changes):
    result = {
        'run_id': 'run-1', 'prompt_id': 'p1', 'prompt': 'Which tool should I use?',
        'engine': 'Example engine', 'surface': 'answer', 'locale': 'en-US',
        'market': 'US', 'captured_at': '2026-10-30T12:00:00+00:00',
        'status': 'ok', 'evidence': 'captures/answer-1.html',
        'mentions': ['Example'], 'citations': ['https://example.com/guide'],
    }
    result.update(changes)
    return result


class AiVisibilityTests(unittest.TestCase):
    def run_records(self, records, *args, script=SCRIPT, raw=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'observations.jsonl'
            path.write_text(raw if raw is not None else ''.join(
                json.dumps(record) + '\n' for record in records), encoding='utf-8')
            return subprocess.run(
                [sys.executable, str(script), str(path), '--brand', 'Example',
                 '--domain', 'example.com', '--competitor', 'Rival', *args],
                cwd=tmp, text=True, capture_output=True,
            )

    def summary(self, records):
        result = self.run_records(records)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def assert_invalid(self, record, detail):
        result = self.run_records([observation(), record])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('line 2:', result.stderr)
        self.assertIn(detail, result.stderr)

    def test_errors_excluded_and_surfaces_kept_separate(self):
        data = self.summary([
            observation(recommendations=['EXAMPLE'], mentions=['example', 'RIVAL']),
            observation(run_id='run-2', status='error', error='capture timed out'),
            observation(run_id='run-3', mentions=['Example tool'], citations=[], recommendations=[]),
            observation(surface='search-overview', mentions=[], recommendations=[]),
        ])
        self.assertEqual(data['counts'], {'total': 4, 'successful': 3, 'error': 1, 'unique_prompts': 1})
        self.assertEqual(len(data['cohorts']), 2)
        answer = next(c for c in data['cohorts'] if c['surface'] == 'answer')
        self.assertEqual(answer['sample_size'], 2)
        self.assertEqual(answer['counts']['error'], 1)
        self.assertEqual(answer['mentions']['brand'], {'count': 1, 'denominator': 2, 'rate_percent': 50.0})
        self.assertEqual(answer['mentions']['competitors']['Rival']['count'], 1)
        self.assertEqual(answer['owned_domain_citations']['count'], 1)
        self.assertEqual(answer['brand_recommendations']['denominator'], 2)
        self.assertIn('not fetched or verified', data['evidence_verification'])
        self.assertNotIn('score', data)

    def test_absent_recommendations_are_unassessed(self):
        data = self.summary([observation(), observation(run_id='run-2', recommendations=[])])
        self.assertEqual(data['cohorts'][0]['brand_recommendations'], {
            'count': 0, 'denominator': 1, 'rate_percent': 0.0,
        })
        single = self.summary([observation()])['cohorts'][0]
        self.assertIsNone(single['brand_recommendations']['rate_percent'])

    def test_all_error_cohort_has_null_rates(self):
        record = observation(status='error', error='unavailable')
        del record['mentions'], record['citations']
        cohort = self.summary([record])['cohorts'][0]
        self.assertEqual(cohort['sample_size'], 0)
        self.assertEqual(cohort['unique_prompts'], 1)
        self.assertIsNone(cohort['mentions']['brand']['rate_percent'])
        self.assertIsNone(cohort['owned_domain_citations']['rate_percent'])
        self.assertEqual(cohort['top_cited_domains'], [])

    def test_citations_use_host_boundaries_and_answer_deduplication(self):
        data = self.summary([
            observation(citations=['https://EXAMPLE.com/guide', 'https://example.com/guide',
                                  'https://docs.example.com/a', 'https://docs.example.com/b']),
            observation(run_id='r2', citations=['https://evil-example.com/a',
                                             'https://example.com.evil.org/a']),
            observation(run_id='r3', citations=['https://example.com/guide']),
        ])['cohorts'][0]
        self.assertEqual(data['owned_domain_citations']['count'], 2)
        domains = {item['domain']: item['answer_count'] for item in data['top_cited_domains']}
        urls = {item['url']: item['answer_count'] for item in data['top_cited_urls']}
        self.assertEqual(domains['example.com'], 2)
        self.assertEqual(domains['docs.example.com'], 1)
        self.assertEqual(urls['https://example.com/guide'], 2)

    def test_timestamp_range_normalizes_offsets(self):
        data = self.summary([observation(captured_at='2026-10-30T12:00:00+03:00'),
                             observation(run_id='r2', captured_at='2026-10-30T10:00:00Z')])
        self.assertEqual(data['captured_at_range'], {
            'first': '2026-10-30T09:00:00Z', 'last': '2026-10-30T10:00:00Z',
        })

    def test_duplicate_observation_rejected(self):
        self.assert_invalid(observation(), 'duplicate observation')

    def test_prompt_ids_cannot_silently_change_prompt_text(self):
        self.assert_invalid(observation(run_id='run-2', prompt='Different question'), 'prompt_id')

    def test_recommendations_must_also_be_annotated_mentions(self):
        self.assert_invalid(observation(run_id='run-2', mentions=[], recommendations=['Example']),
                            'recommendations must also appear in mentions')

    def test_malformed_shape_and_dates_rejected(self):
        for record, detail in [
            ([], 'object'),
            (observation(run_id=''), 'run_id'),
            (observation(status='pending'), 'status'),
            (observation(captured_at='2026-10-30T12:00:00'), 'captured_at'),
            (observation(captured_at='yesterday'), 'captured_at'),
            (observation(mentions='Example'), 'mentions'),
            (observation(citations=[42]), 'citations'),
            (observation(recommendations=None), 'recommendations'),
            (observation(evidence=' '), 'evidence'),
            (observation(status='error'), 'error'),
        ]:
            with self.subTest(detail=detail, record=record):
                self.assert_invalid(record, detail)
        missing = observation()
        del missing['citations']
        self.assert_invalid(missing, 'citations')

    def test_unsafe_or_malformed_citation_urls_rejected(self):
        for url in ['file:///tmp/a', 'https://user@example.com/a', 'https://example.com:bad/a',
                    'https:///path', 'https://bad_host/a', 'https://example.com/white space',
                    'https://example.com\\@evil.org/a', 'https://[invalid/a', 'https://example.com../a']:
            with self.subTest(url=url):
                self.assert_invalid(observation(run_id='r2', citations=[url]), 'citations')

    def test_bad_json_empty_input_and_bad_domain_produce_no_output(self):
        for raw in ['', '\n', '{oops}\n']:
            result = self.run_records([], raw=raw)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, '')
        for domain in ['https://example.com', 'example.com/path', 'user@example.com', 'example.com:443']:
            result = self.run_records([observation()], '--domain', domain)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, '')

    def test_label_matching_is_exact_and_competitors_are_independent(self):
        result = self.run_records([
            observation(mentions=['Example Plus', 'RIVAL', 'Second'], recommendations=['Example Plus']),
        ], '--competitor', 'Second')
        self.assertEqual(result.returncode, 0, result.stderr)
        cohort = json.loads(result.stdout)['cohorts'][0]
        self.assertEqual(cohort['mentions']['brand']['count'], 0)
        self.assertEqual(cohort['brand_recommendations']['count'], 0)
        self.assertEqual(cohort['mentions']['competitors']['Rival']['count'], 1)
        self.assertEqual(cohort['mentions']['competitors']['Second']['count'], 1)
        duplicate = self.run_records([observation()], '--competitor', 'rival')
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertEqual(duplicate.stdout, '')

    def test_cohort_dimensions_and_prompt_coverage_are_independent(self):
        data = self.summary([
            observation(), observation(prompt_id='p2'),
            observation(engine='Other'), observation(locale='am-ET'), observation(market='ET'),
        ])
        self.assertEqual(data['counts']['unique_prompts'], 2)
        self.assertEqual(len(data['cohorts']), 4)
        cohort = next(c for c in data['cohorts'] if c['sample_size'] == 2)
        self.assertEqual(cohort['unique_prompts'], 2)

    def test_standalone_script_runs_after_relocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            moved = Path(tmp) / 'ai_visibility.py'
            shutil.copyfile(SCRIPT, moved)
            result = self.run_records([observation()], script=moved)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['counts']['successful'], 1)


if __name__ == '__main__':
    unittest.main()
