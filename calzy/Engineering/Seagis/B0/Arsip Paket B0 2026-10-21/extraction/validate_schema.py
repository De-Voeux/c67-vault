"""Validasi struktur dan integritas corpus lokal; tidak menyetujui bukti ilmiah."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path, PurePosixPath
import sys

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
TRANSITIONS = {
    'candidate': {'extracted', 'rejected', 'superseded'},
    'extracted': {'needs_review', 'rejected', 'superseded'},
    'needs_review': {'verified', 'rejected', 'superseded'},
    'verified': {'needs_review', 'superseded'},
    'rejected': {'needs_review'},
    'superseded': set(),
}


def validators():
    """Daftarkan seluruh schema secara lokal; tidak ada resolver HTTP."""
    registry = Registry()
    for path in sorted((ROOT / 'schemas').glob('*.schema.json')):
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(path.as_uri(), Resource.from_contents(schema))
    return {
        kind: Draft202012Validator(
            {'$ref': (ROOT / 'schemas' / f'{kind}.schema.json').as_uri()},
            registry=registry, format_checker=FormatChecker(),
        ) for kind in ('source', 'knowledge_entry')
    }


def validate_records(sources, entries):
    errors = []
    checks = validators()
    for kind, records in [('source', sources), ('knowledge_entry', entries)]:
        seen = set()
        for index, record in enumerate(records):
            label = f'{kind}[{index}]'
            schema_errors = list(checks[kind].iter_errors(record))
            for error in schema_errors:
                path = '.'.join(map(str, error.absolute_path)) or '$'
                errors.append(f'{label}.{path}: {error.message}')
            if schema_errors:
                continue
            if record['id'] in seen:
                errors.append(f'{label}: duplicate ID {record["id"]}')
            seen.add(record['id'])
    if errors:
        return errors
    source_map = {s['id']: s for s in sources}
    entry_map = {e['id']: e for e in entries}
    fingerprints = {}
    for source in sources:
        sid = source['id']
        canonical = source['duplicate_of'] or sid
        if source['duplicate_of']:
            target = source_map.get(canonical)
            if canonical == sid or target is None or target['duplicate_of'] is not None:
                errors.append(f'{sid}: duplicate_of harus menunjuk sumber kanonis lain')
        if source['doi'] and source['doi'] != source['doi'].lower():
            errors.append(f'{sid}: DOI harus lowercase')
        keys = [('doi', source['doi'])] if source['doi'] else []
        for origin in source['provenance']:
            path = origin['relative_path']
            if (PurePosixPath(path).is_absolute() or '\\' in path
                    or any(p in ('', '.', '..') for p in path.split('/'))):
                errors.append(f'{sid}: provenance path harus relatif dan ternormalisasi')
            keys.append(('sha256', origin['sha256']))
        for key in keys:
            previous = fingerprints.setdefault(key, canonical)
            if previous != canonical:
                errors.append(f'{sid}: duplicate {key[0]} tanpa duplicate_of yang sesuai')
        if source['read_scope'] in {'selected_full_text', 'full_text'} and source['access_status'] != 'full_text_available':
            errors.append(f'{sid}: cakupan full text tidak cocok dengan akses')
        if source['read_scope'] == 'local_note' and source['access_status'] != 'local_note_available':
            errors.append(f'{sid}: cakupan catatan tidak cocok dengan akses')
    for entry in entries:
        eid = entry['id']
        source = source_map.get(entry['source_id'])
        if source is None:
            errors.append(f'{eid}: source_id tidak ditemukan')
        history = entry['review_history']
        if history[0]['status'] != 'candidate':
            errors.append(f'{eid}: riwayat harus dimulai candidate')
        if history[-1]['status'] != entry['verification_status']:
            errors.append(f'{eid}: status terakhir riwayat tidak cocok')
        for old, new in zip(history, history[1:]):
            if new['status'] not in TRANSITIONS[old['status']]:
                errors.append(f'{eid}: transisi tidak sah {old["status"]} -> {new["status"]}')
            if datetime.fromisoformat(new['at'].replace('Z', '+00:00')) < datetime.fromisoformat(old['at'].replace('Z', '+00:00')):
                errors.append(f'{eid}: timestamp riwayat mundur')
        for event in history:
            if event['status'] == 'verified' and event['actor_type'] != 'human':
                errors.append(f'{eid}: AI tidak dapat membuat event verified')
        for relation in entry['related_entries']:
            target = entry_map.get(relation['entry_id'])
            if target is None or relation['entry_id'] == eid:
                errors.append(f'{eid}: related_entries harus menunjuk entri lain yang ada')
            if relation['relation'] == 'supersedes' and target and target['verification_status'] != 'superseded':
                errors.append(f'{eid}: entri lama harus berstatus superseded')
        if entry['verification_status'] == 'superseded':
            if not any(r['relation'] == 'supersedes' and r['entry_id'] == eid
                       for other in entries if other['id'] != eid for r in other['related_entries']):
                errors.append(f'{eid}: superseded memerlukan entri pengganti')
        if entry['direction'] == 'no_detected_difference' and entry['statistics']['significance'] != 'not_significant':
            errors.append(f'{eid}: no_detected_difference memerlukan not_significant')
        if entry['outcome'] == 'other' and not entry['outcome_detail']:
            errors.append(f'{eid}: outcome other memerlukan outcome_detail')
        if entry['relationship_type'] != 'interaction' and entry['interaction_test'] == 'direct_test_reported':
            errors.append(f'{eid}: uji interaksi langsung harus dicatat sebagai interaction')
        for exposure in entry['experimental_conditions']['exposures']:
            if exposure['parameter_tag'] not in entry['parameter_tags']:
                errors.append(f'{eid}: tag exposure tidak tercantum pada parameter_tags')
        if any(s in {'other_macroalga', 'other_organism'} for s in entry['species']):
            if entry['applicability'] not in {'unassessed', 'hypothesis_only', 'not_applicable'}:
                errors.append(f'{eid}: lintas organisme hanya hypothesis_only/not_applicable')
        if entry['verification_status'] == 'verified':
            review = entry['verification']
            if history[-1]['actor'] != review['verified_by'] or history[-1]['at'] != review['verified_at']:
                errors.append(f'{eid}: reviewer/tanggal harus cocok dengan event verified')
            if source and (source['source_kind'] not in {'primary_study', 'review'}
                           or not source['bibliography_checked']
                           or source['access_status'] != 'full_text_available'
                           or source['read_scope'] not in {'selected_full_text', 'full_text'}
                           or source['duplicate_of'] is not None):
                errors.append(f'{eid}: verified memerlukan sumber ilmiah kanonis dengan bibliografi/full text diperiksa')
            conditions = entry['experimental_conditions']
            for key in ('strain', 'location_reported', 'exposure_duration', 'acclimation', 'sample_size_reported'):
                if conditions[key] is None and key not in conditions['unknown_fields']:
                    errors.append(f'{eid}: konteks null {key} harus dicatat pada unknown_fields')
    return errors


def read_jsonl(path):
    records = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            raise ValueError(f'{path.name}:{number}: baris kosong bukan record JSONL')
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f'{path.name}:{number}: {error.msg}') from error
    return records


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, default=ROOT / 'vault/sources.jsonl')
    parser.add_argument('--entries', type=Path, default=ROOT / 'vault/entries.jsonl')
    args = parser.parse_args(argv)
    try:
        sources, entries = read_jsonl(args.sources), read_jsonl(args.entries)
        errors = validate_records(sources, entries)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    verified = sum(e['verification_status'] == 'verified' for e in entries)
    print(f'Valid: {len(sources)} sources, {len(entries)} entries, {verified} verified (structure only).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
