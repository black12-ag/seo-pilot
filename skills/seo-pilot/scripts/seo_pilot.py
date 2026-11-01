#!/usr/bin/env python3
"""Offline routing and integrity tools. A route is an audit plan, not an executed audit."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    'technical': ['claude-seo:seo-technical', 'claude-seo:seo-sitemap', 'claude-seo:seo-schema', 'web-quality-skills:seo'],
    'content': ['marketingskills:content-strategy', 'claude-seo:seo-content', 'marketingskills:copywriting'],
    'ai': ['marketingskills:ai-seo', 'claude-seo:seo-geo', 'claude-seo:seo-agentic'],
    'performance': ['web-quality-skills:performance', 'web-quality-skills:core-web-vitals', 'web-quality-skills:accessibility'],
    'app': ['marketingskills:aso'],
    'bot': ['marketingskills:product-marketing', 'marketingskills:conversion-tracking'],
    'ecommerce': ['claude-seo:seo-ecommerce', 'claude-seo:seo-schema', 'marketingskills:cro'],
    'local': ['claude-seo:seo-local', 'claude-seo:seo-maps'],
    'international': ['claude-seo:seo-hreflang', 'marketingskills:content-strategy'],
}


def inside(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError(f'Path escapes installed skill: {relative}')
    return path


def catalog():
    data = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    ids = set()
    for module in data['modules']:
        if module['id'] in ids:
            raise ValueError(f'Duplicate module ID: {module["id"]}')
        ids.add(module['id'])
        if not inside(module['path']).is_file():
            raise ValueError(f'Missing module: {module["path"]}')
    return data


def check():
    problems = []
    data = json.loads((ROOT / 'bundle-manifest.json').read_text(encoding='utf-8'))
    for name, expected in data['files'].items():
        path = inside(name)
        if not path.is_file():
            problems.append({'path': name, 'error': 'missing'})
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            problems.append({'path': name, 'error': 'checksum mismatch'})
    modules = catalog()['modules']
    return {'ok': not problems, 'modules': len(modules), 'checked_files': len(data['files']), 'problems': problems}


def route(mode, url=None, app=None, bot=None):
    modules = {item['id']: item for item in catalog()['modules']}
    if mode == 'all':
        modes = ['technical', 'content', 'ai', 'performance'] if url or not (app or bot) else []
        if app:
            modes.append('app')
        if bot:
            modes.append('bot')
    else:
        modes = [mode]
    selected = list(dict.fromkeys(module for part in modes for module in ROUTES[part]))
    references = ['references/modes.md', 'references/evidence.md']
    if 'ai' in modes:
        references += ['references/ai-search.md', 'references/ai-visibility.md', 'references/connectors.md']
    if any(part in modes for part in ('app', 'bot')):
        references.append('references/app-and-bot.md')
    return {'audit_performed': False, 'mode': mode,
            'targets': {'website': url, 'app': app, 'bot': bot},
            'references': references,
            'modules': [modules[name] for name in selected],
            'next': 'Read SKILL.md and the relevant references, collect evidence, execute the selected checks, and produce one deduplicated report.'}


def doctor():
    supported = sys.version_info >= (3, 11)
    return {'ok': supported, 'python': sys.version.split()[0],
            'python_supported': supported, 'routing_ready': supported,
            'executables': {name: bool(shutil.which(name)) for name in ['git', 'node', 'npm', 'uv']},
            'optional_python': {name: importlib.util.find_spec(name) is not None for name in ['bs4', 'requests', 'playwright']},
            'notes': ['Routing, listing and integrity checks require only Python 3.11+.',
                      'Live checks need network access; browser, Google data and paid provider integrations are optional.',
                      'No dependencies were installed and no account credentials were inspected.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('list', help='List every bundled module with its namespaced ID')
    commands.add_parser('check', help='Check imported file hashes and module paths')
    commands.add_parser('doctor', help='Report optional runtime availability without installing anything')
    routing = commands.add_parser('route', help='Print a workflow plan; does not perform an audit')
    routing.add_argument('mode', choices=['all', *ROUTES])
    routing.add_argument('--url')
    routing.add_argument('--app')
    routing.add_argument('--bot')
    args = parser.parse_args()
    try:
        if args.command == 'list':
            result = catalog()
        elif args.command == 'check':
            result = check()
        elif args.command == 'doctor':
            result = doctor()
        else:
            result = route(args.mode, args.url, args.app, args.bot)
        print(json.dumps(result, indent=2))
        return 1 if result.get('ok') is False else 0
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
