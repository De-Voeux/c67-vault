"""Fixture sintetis di memori; tidak ada klaim verified yang ditulis ke vault."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extraction.validate_schema import read_jsonl, validate_records, validators


def fixture():
    source = {
        'id': 'SYNTHETIC-SOURCE', 'schema_version': '0.1.0',
        'source_kind': 'primary_study', 'title': 'SYNTHETIC validation fixture only',
        'authors': ['Synthetic author'], 'year': 2026, 'doi': None,
        'url': 'https://example.invalid/synthetic', 'legacy_ids': [],
        'access_status': 'full_text_available', 'read_scope': 'selected_full_text',
        'bibliography_checked': True, 'duplicate_of': None, 'provenance': [],
        'access_notes': 'Synthetic flags only; no actual source accessed.',
    }
    entry = json.loads((ROOT / 'examples/candidate_entry.json').read_text())
    entry.update({
        'id': 'SYNTHETIC-CLAIM', 'source_id': source['id'],
        'parameter_tags': ['water_temperature'], 'relationship_type': 'single_parameter',
        'interaction_test': 'not_applicable', 'finding': 'SYNTHETIC effect; not scientific evidence.',
        'evidence_type': 'controlled_experiment', 'outcome': 'growth_rate',
        'direction': 'decrease', 'experimental_setting': 'laboratory',
        'source_location': {'locator_type': 'table', 'value': 'SYNTHETIC Table 1, PDF p. 1', 'supporting_excerpt': None},
        'limitations': ['Synthetic test only.'], 'limitation_tags': ['synthetic_fixture'],
        'applicability': 'same_species_context_limited', 'verification_status': 'verified',
    })
    entry['experimental_conditions'].update({
        'design_and_comparator': 'SYNTHETIC treatment vs control',
        'unknown_fields': ['strain', 'location_reported', 'exposure_duration', 'acclimation', 'sample_size_reported'],
        'exposures': [{'parameter_tag': 'water_temperature', 'quantity': {
            'label': 'synthetic treatment', 'values': [1, 2], 'unit_reported': 'degC',
            'analyte_reported': None, 'basis': 'not_applicable', 'original_text': '1 and 2 degC (synthetic)',
        }, 'notes': 'Synthetic values only.'}],
    })
    entry['verification'] = {
        'verified_by': 'synthetic-human-test-only', 'verified_at': '2026-10-21T12:03:00+07:00',
        'reviewer_type': 'human', 'checks': {key: True for key in entry['verification']['checks']},
        'review_notes': 'SYNTHETIC review; no actual human verification.',
    }
    entry['review_history'] = [{
        'status': state, 'actor': 'synthetic-human-test-only' if state == 'verified' else 'synthetic-ai',
        'actor_type': 'human' if state == 'verified' else 'ai',
        'at': f'2026-10-21T12:0{i}:00+07:00', 'notes': 'SYNTHETIC event.',
    } for i, state in enumerate(['candidate', 'extracted', 'needs_review', 'verified'])]
    return [source], [entry]


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.sources, self.entries = fixture()
        self.entry = self.entries[0]

    def assertInvalid(self):
        self.assertTrue(validate_records(self.sources, self.entries))

    def test_live_vault_and_example(self):
        entries = read_jsonl(ROOT / 'vault/entries.jsonl')
        self.assertEqual([], validate_records(read_jsonl(ROOT / 'vault/sources.jsonl'), entries))
        self.assertEqual(entries[0], json.loads((ROOT / 'examples/candidate_entry.json').read_text()))
        self.assertEqual(0, sum(e['verification_status'] == 'verified' for e in entries))

    def test_single_parameter_with_review_metadata(self):
        self.assertEqual([], validate_records(self.sources, self.entries))

    def test_direct_interaction_and_combined_exposure(self):
        for kind, tested in [('interaction', 'direct_test_reported'), ('combined_exposure', 'not_isolated')]:
            with self.subTest(kind=kind):
                self.entry.update(parameter_tags=['water_temperature', 'salinity'], relationship_type=kind, interaction_test=tested)
                self.assertEqual([], validate_records(self.sources, self.entries))

    def test_interaction_requires_two_parameters_and_direct_test(self):
        self.entry.update(relationship_type='interaction', interaction_test='not_isolated')
        self.assertInvalid()

    def test_non_significant_observation(self):
        self.entry.update(evidence_type='observational_association', direction='no_detected_difference')
        self.entry['statistics'].update(significance='not_significant', p_value=0.8)
        self.assertEqual([], validate_records(self.sources, self.entries))

    def test_null_finding_not_allowed_after_extraction(self):
        self.entry['finding'] = None
        self.assertInvalid()

    def test_conflicting_findings_retained(self):
        other = copy.deepcopy(self.entry); other.update(id='SYNTHETIC-OTHER', direction='increase')
        other['related_entries'] = [{'entry_id': self.entry['id'], 'relation': 'contradicts', 'notes': 'Synthetic opposite outcome.'}]
        self.entries.append(other)
        self.assertEqual([], validate_records(self.sources, self.entries))

    def test_verified_gate_fields(self):
        for key, value in [('source_location', None), ('limitations', []), ('applicability', 'unassessed')]:
            with self.subTest(key=key):
                entry = copy.deepcopy(self.entry); entry[key] = value
                self.assertTrue(validate_records(self.sources, [entry]))
        for key, value in [('verified_by', None), ('verified_by', ' '), ('verified_at', None), ('verified_at', '2026-10-21'), ('reviewer_type', 'ai'), ('review_notes', '')]:
            with self.subTest(key=key, value=value):
                entry = copy.deepcopy(self.entry); entry['verification'][key] = value
                self.assertTrue(validate_records(self.sources, [entry]))
        for key in self.entry['verification']['checks']:
            with self.subTest(check=key):
                entry = copy.deepcopy(self.entry); entry['verification']['checks'][key] = False
                self.assertTrue(validate_records(self.sources, [entry]))

    def test_schema_alone_blocks_verified_without_context(self):
        for key in ['source_location', 'experimental_conditions', 'verification']:
            with self.subTest(key=key):
                entry = copy.deepcopy(self.entry); del entry[key]
                self.assertTrue(list(validators()['knowledge_entry'].iter_errors(entry)))

    def test_missing_source_and_duplicate_entry_id(self):
        self.entry['source_id'] = 'MISSING-SOURCE'; self.assertInvalid()
        self.entry['source_id'] = self.sources[0]['id']
        self.entries.append(copy.deepcopy(self.entry)); self.assertInvalid()

    def test_no_status_shortcut_or_ai_approval(self):
        original = copy.deepcopy(self.entry['review_history'])
        self.entry['review_history'] = [original[0], original[-1]]; self.assertInvalid()
        self.entry['review_history'] = original
        self.entry['review_history'][-1]['actor_type'] = 'ai'; self.assertInvalid()

    def test_chronology_and_review_identity(self):
        self.entry['review_history'][1]['at'] = '2026-10-21T11:00:00+07:00'; self.assertInvalid()
        self.entry['review_history'][1]['at'] = '2026-10-21T12:01:00+07:00'
        self.entry['verification']['verified_by'] = 'different-human'; self.assertInvalid()

    def test_unknown_status_and_parameter_tag(self):
        for key, value in [('verification_status', 'approved'), ('parameter_tags', ['made_up_tag'])]:
            with self.subTest(key=key):
                entry = copy.deepcopy(self.entry); entry[key] = value
                self.assertTrue(validate_records(self.sources, [entry]))

    def test_numeric_claim_requires_units(self):
        del self.entry['experimental_conditions']['exposures'][0]['quantity']['unit_reported']
        self.assertInvalid()

    def test_ion_and_element_basis_preserved(self):
        self.entry['parameter_tags'] = ['nitrate']
        exposure = self.entry['experimental_conditions']['exposures'][0]
        exposure['parameter_tag'] = 'nitrate'
        exposure['quantity'].update(unit_reported='mg/L', analyte_reported='NO3-N', basis='as_N', original_text='<1 mg/L as N')
        self.assertEqual([], validate_records(self.sources, self.entries))

    def test_abstract_internal_and_unchecked_source_cannot_verify(self):
        for field, value in [('source_kind', 'internal_synthesis'), ('read_scope', 'abstract_only'), ('access_status', 'abstract_only'), ('bibliography_checked', False)]:
            with self.subTest(field=field):
                source = copy.deepcopy(self.sources[0]); source[field] = value
                self.assertTrue(validate_records([source], self.entries))

    def test_doi_duplicate_requires_canonical_link(self):
        self.sources[0]['doi'] = '10.1234/synthetic'
        other = copy.deepcopy(self.sources[0]); other['id'] = 'SYNTHETIC-DUPLICATE'
        self.sources.append(other); self.assertInvalid()
        other['duplicate_of'] = self.sources[0]['id']
        self.assertEqual([], validate_records(self.sources, self.entries))
        other['duplicate_of'] = other['id']; self.assertInvalid()

    def test_non_significant_consistency(self):
        self.entry['direction'] = 'no_detected_difference'; self.assertInvalid()

    def test_cross_species_applicability(self):
        self.entry['species'] = ['other_organism']; self.assertInvalid()
        self.entry['applicability'] = 'hypothesis_only'
        self.assertEqual([], validate_records(self.sources, self.entries))

    def test_missing_context_must_be_acknowledged(self):
        self.entry['experimental_conditions']['unknown_fields'] = []; self.assertInvalid()

    def test_superseded_requires_replacement(self):
        self.entry['verification_status'] = 'superseded'
        self.entry['review_history'].append({'status': 'superseded', 'actor': 'synthetic-human-test-only', 'actor_type': 'human', 'at': '2026-10-21T12:04:00+07:00', 'notes': 'Synthetic replacement.'})
        self.assertInvalid()
        replacement = fixture()[1][0]; replacement['id'] = 'SYNTHETIC-REPLACEMENT'
        replacement['related_entries'] = [{'entry_id': self.entry['id'], 'relation': 'supersedes', 'notes': 'Synthetic corrected entry.'}]
        self.entries.append(replacement)
        self.assertEqual([], validate_records(self.sources, self.entries))

    def test_dangling_conflict_reference(self):
        self.entry['related_entries'] = [{'entry_id': 'MISSING', 'relation': 'contradicts', 'notes': 'Synthetic conflict.'}]
        self.assertInvalid()

    def test_provenance_path_and_checksum_duplicate(self):
        origin = {'base_id': 'test_base', 'relative_path': '../escape.md', 'sha256': 'a' * 64, 'git_commit': None, 'working_tree_modified': True, 'captured_at': '2026-10-21T12:00:00+07:00'}
        self.sources[0]['provenance'] = [origin]; self.assertInvalid()
        origin['relative_path'] = 'notes/source.md'
        self.assertEqual([], validate_records(self.sources, self.entries))
        other = copy.deepcopy(self.sources[0]); other['id'] = 'CHECKSUM-DUPLICATE'
        self.sources.append(other); self.assertInvalid()

    def test_jsonl_error_and_cli_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'broken.jsonl'; path.write_text('{invalid}\n')
            with self.assertRaises(ValueError): read_jsonl(path)
            result = subprocess.run([sys.executable, str(ROOT / 'extraction/validate_schema.py'), '--entries', str(path)], capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertIn('broken.jsonl:1', result.stderr)


if __name__ == '__main__':
    unittest.main()
