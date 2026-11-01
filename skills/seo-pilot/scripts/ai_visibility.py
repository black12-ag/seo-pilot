#!/usr/bin/env python3
"""Summarize annotated AI answer observations without fetching their evidence."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import ipaddress
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit


COHORT = ('engine', 'surface', 'locale', 'market')
REQUIRED = ('run_id', 'prompt_id', 'prompt', *COHORT, 'captured_at', 'status', 'evidence')


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def hostname(value):
    """Normalize an IP literal or DNS hostname, rejecting ambiguous host syntax."""
    if not nonempty_string(value) or any(c.isspace() for c in value):
        raise ValueError('invalid hostname')
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        pass
    try:
        host = value.removesuffix('.').encode('idna').decode('ascii').lower()
    except UnicodeError as exc:
        raise ValueError('invalid hostname') from exc
    if not host or len(host) > 253 or any(
        not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label)
        for label in host.split('.')
    ):
        raise ValueError('invalid hostname')
    return host


def citation(value):
    if not nonempty_string(value) or any(c.isspace() or ord(c) < 32 for c in value) or '\\' in value:
        raise ValueError('citations must contain valid http(s) URLs')
    try:
        parsed = urlsplit(value)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.username is not None:
            raise ValueError('unsupported URL')
        host = hostname(parsed.hostname)
        port = parsed.port
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError('citations must contain valid http(s) URLs without userinfo') from exc
    authority = f'[{host}]' if ':' in host else host
    if port is not None and port != (443 if parsed.scheme == 'https' else 80):
        authority += f':{port}'
    return urlunsplit((parsed.scheme, authority, parsed.path or '/', parsed.query, '')), host


def string_list(record, key):
    values = record.get(key)
    if not isinstance(values, list) or any(not nonempty_string(v) for v in values):
        raise ValueError(f'{key} must be an array of nonempty strings')
    return values


def validate(record):
    if not isinstance(record, dict):
        raise ValueError('observation must be an object')
    for key in REQUIRED:
        if not nonempty_string(record.get(key)):
            raise ValueError(f'{key} must be a nonempty string')
    if record['status'] not in ('ok', 'error'):
        raise ValueError('status must be ok or error')
    try:
        captured_at = datetime.fromisoformat(record['captured_at'].replace('Z', '+00:00'))
        if captured_at.tzinfo is None or captured_at.utcoffset() is None:
            raise ValueError('timezone missing')
        record['_timestamp'] = captured_at.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise ValueError('captured_at must be a timezone-aware ISO8601 timestamp') from exc
    if record['status'] == 'error':
        if not nonempty_string(record.get('error')):
            raise ValueError('error records require a nonempty error string')
    else:
        record['_mentions'] = {v.casefold() for v in string_list(record, 'mentions')}
        record['_citations'] = set(citation(v) for v in string_list(record, 'citations'))
    if 'recommendations' in record:
        record['_recommendations'] = {v.casefold() for v in string_list(record, 'recommendations')}
        if record['status'] == 'ok' and not record['_recommendations'] <= record['_mentions']:
            raise ValueError('recommendations must also appear in mentions (case-insensitively)')
    return record


def load_observations(path):
    records, seen, prompts = [], set(), {}
    with path.open(encoding='utf-8') as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                record = validate(json.loads(line))
                if record['prompt_id'] in prompts and prompts[record['prompt_id']] != record['prompt']:
                    raise ValueError('prompt_id maps to different prompt text; use a new prompt_id')
                prompts[record['prompt_id']] = record['prompt']
                key = tuple(record[k] for k in ('run_id', 'prompt_id', *COHORT))
                if key in seen:
                    raise ValueError('duplicate observation (run_id, prompt_id, engine, surface, locale, market)')
                seen.add(key)
                records.append(record)
            except (ValueError, RecursionError) as exc:
                raise ValueError(f'line {line_number}: {exc}') from exc
    if not records:
        raise ValueError('input contains no observations')
    return records


def metric(count, denominator):
    return {'count': count, 'denominator': denominator,
            'rate_percent': round(100 * count / denominator, 4) if denominator else None}


def counts(records):
    successful = sum(r['status'] == 'ok' for r in records)
    return {'total': len(records), 'successful': successful, 'error': len(records) - successful,
            'unique_prompts': len({r['prompt_id'] for r in records})}


def summarize_cohort(key, records, brand, domain, competitors):
    successful = [r for r in records if r['status'] == 'ok']
    measured_recommendations = [r for r in successful if '_recommendations' in r]
    domains, urls = Counter(), Counter()
    for record in successful:
        domains.update({host for _, host in record['_citations']})
        urls.update({url for url, _ in record['_citations']})
    sample_size = len(successful)
    return {
        **dict(zip(COHORT, key)), 'counts': counts(records), 'sample_size': sample_size,
        'unique_prompts': len({r['prompt_id'] for r in records}),
        'mentions': {
            'brand': metric(sum(brand.casefold() in r['_mentions'] for r in successful), sample_size),
            'competitors': {name: metric(sum(name.casefold() in r['_mentions'] for r in successful), sample_size)
                            for name in competitors},
        },
        'owned_domain_citations': metric(sum(any(
            host == domain or host.endswith('.' + domain) for _, host in r['_citations']
        ) for r in successful), sample_size),
        'brand_recommendations': metric(sum(
            brand.casefold() in r['_recommendations'] for r in measured_recommendations
        ), len(measured_recommendations)),
        'top_cited_domains': [{'domain': host, 'answer_count': count} for host, count in
                              sorted(domains.items(), key=lambda item: (-item[1], item[0]))],
        'top_cited_urls': [{'url': url, 'answer_count': count} for url, count in
                           sorted(urls.items(), key=lambda item: (-item[1], item[0]))],
    }


def summarize(records, brand, domain, competitors):
    cohorts = defaultdict(list)
    for record in records:
        cohorts[tuple(record[k] for k in COHORT)].append(record)
    timestamps = [r['_timestamp'] for r in records]
    return {
        'brand': brand, 'domain': domain, 'competitors': competitors,
        'counts': counts(records),
        'captured_at_range': {key: stamp.isoformat().replace('+00:00', 'Z') for key, stamp in
                              [('first', min(timestamps)), ('last', max(timestamps))]},
        'evidence_verification': 'Source evidence references are not fetched or verified.',
        'methodology': {
            'entity_matching': 'Exact case-insensitive annotated entity labels; no inference from answer text.',
            'rate_unit': 'percent; each metric includes its own successful observation denominator',
            'recommendations': 'Missing recommendations are unassessed and excluded from that denominator.',
            'citations': 'URLs and domains counted once per successful answer; URL fragments/default ports normalized.',
            'scope': 'Descriptive sample metrics per engine/surface/locale/market; no pooled visibility or market-share score.',
        },
        'cohorts': [summarize_cohort(key, cohort, brand, domain, competitors)
                    for key, cohort in sorted(cohorts.items())],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        'JSONL required fields: run_id, prompt_id, prompt, engine, surface, locale, market, '
        'captured_at (timezone-aware ISO8601), status (ok|error), evidence (artifact path/URL). '
        'ok: mentions and citations arrays required; recommendations array optional and must be a subset of mentions. '
        'error: error string required; excluded from metric denominators. '
        'Labels are exact case-insensitive annotations. Evidence is never fetched.'
    ))
    parser.add_argument('observations', type=Path, help='UTF-8 JSONL observation file')
    parser.add_argument('--brand', required=True, help='annotated brand entity label')
    parser.add_argument('--domain', required=True, help='owned plain hostname, including its subdomains')
    parser.add_argument('--competitor', action='append', default=[], help='annotated competitor label; repeatable')
    args = parser.parse_args()
    try:
        if not nonempty_string(args.brand) or any(not nonempty_string(v) for v in args.competitor):
            raise ValueError('brand and competitor labels must be nonempty')
        domain = hostname(args.domain)
        labels = [args.brand.casefold(), *(v.casefold() for v in args.competitor)]
        if len(set(labels)) != len(labels):
            raise ValueError('brand and competitor labels must be distinct case-insensitively')
        result = summarize(load_observations(args.observations), args.brand, domain, args.competitor)
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == '__main__':
    main()
