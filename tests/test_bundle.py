import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BundleTests(unittest.TestCase):
    def test_bundle_has_pinned_provenance_and_licenses(self):
        skill = ROOT / 'skills' / 'seo-pilot'
        lock = json.loads((ROOT / 'sources.lock.json').read_text())
        manifest = json.loads((skill / 'bundle-manifest.json').read_text())
        self.assertEqual(len(lock['sources']), 3)
        self.assertEqual(manifest['sources'], lock['sources'])
        for source in lock['sources']:
            self.assertEqual(len(source['commit']), 40)
            self.assertIn('MIT', (skill / 'vendor' / source['id'] / 'LICENSE').read_text())
        self.assertGreater(len(manifest['files']), 100)
        self.assertIn('MIT License', (skill / 'LICENSE').read_text())

    def test_import_rejects_wrong_source_revision(self):
        spec = importlib.util.spec_from_file_location('bundle_builder', ROOT / 'scripts' / 'build_bundle.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with self.assertRaises(ValueError):
            module.verify_source(ROOT, '0' * 40)

    def test_import_rejects_symlinks_outside_checkout(self):
        spec = importlib.util.spec_from_file_location('bundle_builder', ROOT / 'scripts' / 'build_bundle.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            (source / 'escape').symlink_to(Path(tmp))
            with self.assertRaises(ValueError):
                module.validate_links(source)

    def test_import_copies_only_tracked_files_not_ignored_credentials(self):
        spec = importlib.util.spec_from_file_location('bundle_builder', ROOT / 'scripts' / 'build_bundle.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            source, destination = Path(tmp) / 'source', Path(tmp) / 'bundle'
            source.mkdir()
            subprocess.run(['git', 'init', '-q', str(source)], check=True)
            (source / '.gitignore').write_text('.env\n')
            (source / 'public.md').write_text('public source')
            (source / '.env').write_text('FIXTURE_ONLY=must-not-be-published')
            subprocess.run(['git', '-C', str(source), 'add', '.gitignore', 'public.md'], check=True)
            module.copy_source(source, destination)
            self.assertTrue((destination / 'public.md').is_file())
            self.assertFalse((destination / '.env').exists())

    def test_directory_alias_cannot_copy_untracked_credentials(self):
        spec = importlib.util.spec_from_file_location('bundle_builder', ROOT / 'scripts' / 'build_bundle.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            source, destination = Path(tmp) / 'source', Path(tmp) / 'bundle'
            (source / 'public').mkdir(parents=True)
            subprocess.run(['git', 'init', '-q', str(source)], check=True)
            (source / '.gitignore').write_text('.env\n')
            (source / 'public' / 'guide.md').write_text('public')
            (source / 'public' / '.env').write_text('FIXTURE_ONLY=private')
            (source / 'alias').symlink_to('public', target_is_directory=True)
            subprocess.run(['git', '-C', str(source), 'add', '.gitignore', 'public/guide.md', 'alias'], check=True)
            module.copy_source(source, destination)
            self.assertTrue((destination / 'alias' / 'guide.md').is_file())
            self.assertFalse((destination / 'alias' / '.env').exists())

    def test_import_omits_tracked_bytecode_removed_by_skill_installers(self):
        spec = importlib.util.spec_from_file_location('bundle_builder', ROOT / 'scripts' / 'build_bundle.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            source, destination = Path(tmp) / 'source', Path(tmp) / 'bundle'
            (source / '__pycache__').mkdir(parents=True)
            subprocess.run(['git', 'init', '-q', str(source)], check=True)
            (source / 'tool.py').write_text('print("public")')
            (source / '__pycache__' / 'tool.pyc').write_bytes(b'compiled fixture')
            subprocess.run(['git', '-C', str(source), 'add', '-f', 'tool.py', '__pycache__/tool.pyc'], check=True)
            module.copy_source(source, destination)
            self.assertTrue((destination / 'tool.py').exists())
            self.assertFalse((destination / '__pycache__').exists())


if __name__ == '__main__':
    unittest.main()
