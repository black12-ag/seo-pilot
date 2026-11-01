import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'seo-pilot'


def run_cli(root, *args):
    return subprocess.run(
        [sys.executable, str(root / 'scripts' / 'seo_pilot.py'), *args],
        capture_output=True, text=True,
    )


class CliTests(unittest.TestCase):
    def test_all_modules_are_namespaced_and_reachable(self):
        result = run_cli(SKILL, 'list')
        self.assertEqual(result.returncode, 0, result.stderr)
        modules = json.loads(result.stdout)['modules']
        self.assertEqual(len(modules), 92)
        self.assertEqual(len({m['id'] for m in modules}), 92)
        for module in modules:
            self.assertTrue((SKILL / module['path']).is_file(), module)
        self.assertEqual(sum(m['name'] == 'seo' for m in modules), 2)
        bing = next(m for m in modules if m['id'] == 'claude-seo:seo-bing')
        self.assertTrue(bing['optional'])
        self.assertIn('extensions/', bing['path'])

    def test_full_workflow_combines_sources_without_assuming_app(self):
        result = run_cli(SKILL, 'route', 'all', '--url', 'https://example.com')
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertFalse(plan['audit_performed'])
        ids = {m['id'] for m in plan['modules']}
        self.assertIn('claude-seo:seo-technical', ids)
        self.assertIn('marketingskills:ai-seo', ids)
        self.assertIn('web-quality-skills:core-web-vitals', ids)
        self.assertNotIn('marketingskills:aso', ids)

    def test_app_target_activates_app_store_workflow(self):
        result = run_cli(SKILL, 'route', 'all', '--app', 'https://apps.apple.com/app/id123')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('marketingskills:aso', {m['id'] for m in json.loads(result.stdout)['modules']})

    def test_app_only_does_not_assume_website_target(self):
        result = run_cli(SKILL, 'route', 'all', '--app', 'https://apps.apple.com/app/id123')
        self.assertEqual(result.returncode, 0, result.stderr)
        ids = {m['id'] for m in json.loads(result.stdout)['modules']}
        self.assertNotIn('claude-seo:seo-technical', ids)

    def test_doctor_reports_supported_python_honestly(self):
        result = run_cli(SKILL, 'doctor')
        data = json.loads(result.stdout)
        self.assertEqual(data['python_supported'], sys.version_info >= (3, 11))
        self.assertEqual(data['routing_ready'], data['python_supported'])

    def test_unknown_mode_fails_without_running_anything(self):
        result = run_cli(SKILL, 'route', 'invented-mode')
        self.assertNotEqual(result.returncode, 0)

    def test_moved_installation_works_without_original_repo(self):
        with tempfile.TemporaryDirectory(prefix='seo-pilot-test-') as tmp:
            moved = Path(tmp) / 'moved skill'
            shutil.copytree(SKILL, moved)
            result = run_cli(moved, 'route', 'ai')
            self.assertEqual(result.returncode, 0, result.stderr)
            for module in json.loads(result.stdout)['modules']:
                self.assertTrue((moved / module['path']).is_file())

    def test_tampered_vendor_file_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='seo-pilot-test-') as tmp:
            moved = Path(tmp) / 'skill'
            shutil.copytree(SKILL, moved)
            target = moved / 'vendor' / 'claude-seo' / 'LICENSE'
            target.write_text('changed', encoding='utf-8')
            result = run_cli(moved, 'check')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('LICENSE', result.stdout)

    def test_catalog_cannot_escape_installed_skill(self):
        with tempfile.TemporaryDirectory(prefix='seo-pilot-test-') as tmp:
            moved = Path(tmp) / 'skill'
            shutil.copytree(SKILL, moved)
            catalog_path = moved / 'catalog.json'
            catalog = json.loads(catalog_path.read_text())
            catalog['modules'][0]['path'] = '../../outside.md'
            catalog_path.write_text(json.dumps(catalog))
            result = run_cli(moved, 'list')
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
