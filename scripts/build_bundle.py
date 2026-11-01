#!/usr/bin/env python3
"""Import reviewed local upstream checkouts at the revisions in sources.lock.json."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'seo-pilot'


def verify_source(path, commit):
    result = subprocess.run(['git', '-C', str(path), 'rev-parse', 'HEAD'], capture_output=True, text=True)
    if result.returncode or result.stdout.strip() != commit:
        raise ValueError(f'Wrong upstream revision: {path.name}; expected {commit}')
    dirty = subprocess.run(['git', '-C', str(path), 'status', '--porcelain'], capture_output=True, text=True, check=True)
    if dirty.stdout.strip():
        raise ValueError(f'Upstream checkout must be clean: {path.name}')


def validate_links(path):
    for entry in path.rglob('*'):
        if '.git' not in entry.parts and entry.is_symlink():
            if not entry.resolve().is_relative_to(path.resolve()):
                raise ValueError(f'Upstream symlink escapes checkout: {entry.relative_to(path)}')


def copy_source(source, destination):
    source, destination = source.resolve(), destination.resolve()
    tracked = subprocess.check_output(['git', '-C', str(source), 'ls-files', '-z']).decode().split('\0')
    tracked = {name for name in tracked if name}
    for name in sorted(tracked):
        entry = source / name
        resolved = entry.resolve()
        if not resolved.is_relative_to(source.resolve()):
            raise ValueError(f'Unsupported or escaping tracked path: {name}')
        if entry.is_symlink() and resolved.is_dir():
            # Materialize directory aliases from indexed members only, never a filesystem walk.
            for member_name in sorted(tracked):
                member = source / member_name
                if member.is_relative_to(resolved) and member.is_file():
                    member_resolved = member.resolve()
                    if (not member_resolved.is_relative_to(source.resolve())
                            or member_resolved.relative_to(source.resolve()).as_posix() not in tracked):
                        raise ValueError(f'Untracked or escaping alias member: {member_name}')
                    target = destination / name / member.relative_to(resolved)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(member, target)
            continue
        if not resolved.is_file():
            raise ValueError(f'Unsupported tracked path: {name}')
        if entry.is_symlink() and resolved.relative_to(source.resolve()).as_posix() not in tracked:
            raise ValueError(f'Symlink target is not tracked: {name}')
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(entry, target)


def build(source_dir):
    lock = json.loads((ROOT / 'sources.lock.json').read_text(encoding='utf-8'))
    # Validate every source before replacing any imported tree.
    for source in lock['sources']:
        path = source_dir / source['id']
        verify_source(path, source['commit'])
        if 'MIT' not in (path / 'LICENSE').read_text(encoding='utf-8'):
            raise ValueError(f'Missing MIT license: {source["id"]}')
        validate_links(path)
    modules, files = [], {}
    for source in lock['sources']:
        destination = SKILL / 'vendor' / source['id']
        if destination.exists():
            shutil.rmtree(destination)
        copy_source(source_dir / source['id'], destination)
        seen = set()
        entries = [(p, False) for p in sorted((destination / 'skills').glob('*/SKILL.md'))]
        entries += [(p, True) for p in sorted((destination / 'extensions').glob('**/SKILL.md'))]
        for entry, optional in entries:
            name = entry.parent.name
            if name in seen:
                continue  # Core mirrors retain their canonical ID; extension files remain bundled.
            seen.add(name)
            modules.append({'id': f'{source["id"]}:{name}', 'name': name,
                            'source': source['id'], 'optional': optional,
                            'path': entry.relative_to(SKILL).as_posix()})
        for entry in sorted(destination.rglob('*')):
            if entry.is_file():
                files[entry.relative_to(SKILL).as_posix()] = hashlib.sha256(entry.read_bytes()).hexdigest()
    catalog = {'schema': 1, 'modules': modules}
    manifest = {'schema': 1, 'sources': lock['sources'], 'files': files}
    for name, content in [('catalog.json', catalog), ('bundle-manifest.json', manifest)]:
        (SKILL / name).write_text(json.dumps(content, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'modules': len(modules), 'upstream_files': len(files)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True,
                        help='Parent of the three clean, pinned upstream checkouts')
    build(parser.parse_args().source_dir.resolve())
