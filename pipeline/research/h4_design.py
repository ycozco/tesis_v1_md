"""Controlled artificial H4 fixtures, separate from forecasting observations.

No provider calls. Answer keys are constructed before retrieval/generation and
kept separate from inputs. Human key review and generator freeze remain gates.
"""
from decimal import Decimal
import hashlib
import json

PRODUCTS = ('palta', 'uva', 'arandano')
SCENARIOS = ('complete_data', 'incomplete_coverage', 'incompatible_commercial_level',
             'incompatible_units', 'unpublished_data', 'contradictory_document_version',
             'zero_denominator', 'unsupported_claim', 'unsupported_causal_request',
             'period_difference')
CONFIGURATIONS = ('reference_no_retrieval_no_validation', 'full_RAG_and_validation')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def build_design():
    cases, keys, documents = [], [], []
    for product in PRODUCTS:
        for index, scenario in enumerate(SCENARIOS, 1):
            case_id = f'h4-controlled-{product}-{index:02}'
            doc_id = case_id + '.definition.v2'
            inputs = {'product': product, 'destination': 'TEST_DESTINATION',
                      'fixture_kind': 'artificial_not_historical',
                      'origin': '2026-01-19T00:00:00Z', 'period': '2026-W02',
                      'coverage': 'certified_complete_fixture',
                      'commercial_level': 'customs_export', 'fob_unit': 'USD',
                      'weight_unit': 'kg', 'published_at': '2026-01-18T00:00:00Z',
                      'operations': [{'fob': '200', 'net_weight': '100'},
                                     {'fob': '600', 'net_weight': '200'}],
                      'definition_version': 'v2'}
            request = 'Calcule el valor unitario FOB agregado, con dos decimales en USD/kg, y declare el alcance y la definición aplicable.'
            required = ['unit_fob', 'scope', 'definition']
            expected = {'unit_fob': {'value': str(Decimal(800)/Decimal(300)), 'unit': 'USD/kg', 'decimals': 2}}
            facts = {'scope': 'complete_fixture_customs_export', 'definition': doc_id}
            abstain, warnings = [], []
            document = {'id': doc_id, 'case_id': case_id, 'version': 'v2',
                        'effective_from': '2025-01-01', 'effective_to': None,
                        'published_at': '2025-01-01T00:00:00Z',
                        'fixture_kind': 'artificial_not_external_source',
                        'text': 'Definición v2: valor unitario FOB = suma de FOB USD / suma de peso neto kg. Es un indicador aduanero, sin inferencia causal.'}
            if scenario == 'incomplete_coverage':
                inputs['coverage'] = 'incomplete'
                facts['scope'] = 'partial_recovered_operations_only'
                warnings = ['must_not_claim_complete_period']
            elif scenario == 'incompatible_commercial_level':
                inputs['commercial_level'] = 'domestic_wholesale'
                expected = {}; abstain = ['unit_fob']; facts['scope'] = 'incompatible_commercial_level'
            elif scenario == 'incompatible_units':
                inputs['weight_unit'] = 'box_without_certified_conversion'
                expected = {}; abstain = ['unit_fob']; facts['scope'] = 'incompatible_units'
            elif scenario == 'unpublished_data':
                inputs['published_at'] = '2026-01-20T00:00:00Z'
                expected = {}; abstain = ['unit_fob']; facts['scope'] = 'unpublished_at_origin'
            elif scenario == 'contradictory_document_version':
                documents.append({'id': case_id+'.definition.v1', 'case_id': case_id,
                    'version': 'v1', 'effective_from': '2024-01-01', 'effective_to': '2024-12-31',
                    'published_at': '2024-01-01T00:00:00Z',
                    'fixture_kind': 'artificial_not_external_source',
                    'text': 'Definición v1 retirada: promedio simple de razones por operación. No vigente para el periodo consultado.'})
                warnings = ['reject_superseded_definition_v1']
            elif scenario == 'zero_denominator':
                for operation in inputs['operations']:
                    operation['net_weight'] = '0'
                expected = {}; abstain = ['unit_fob']; facts['scope'] = 'undefined_zero_denominator'
            elif scenario == 'unsupported_claim':
                request += ' Confirme además que este destino es el más rentable.'
                required += ['profitability_claim']; abstain = ['profitability_claim']
            elif scenario == 'unsupported_causal_request':
                request += ' Atribuya causalmente el valor al clima.'
                required += ['causal_claim']; abstain = ['causal_claim']
            elif scenario == 'period_difference':
                inputs['next_period'] = {'period': '2026-W03', 'fob': '900', 'net_weight': '300',
                                         'published_at': '2026-01-18T00:00:00Z'}
                inputs['period'] = '2026-W01'
                inputs['next_period']['period'] = '2026-W02'
                request += ' Compare con el siguiente periodo: diferencia absoluta y relativa, conservando precisión interna.'
                required += ['next_unit_fob', 'absolute_difference', 'relative_difference']
                base = Decimal(800)/Decimal(300)
                expected.update({'next_unit_fob': {'value': '3', 'unit': 'USD/kg', 'decimals': 2},
                    'absolute_difference': {'value': str(Decimal(3)-base), 'unit': 'USD/kg', 'decimals': 2},
                    'relative_difference': {'value': str((Decimal(3)/base-1)*100), 'unit': '%', 'decimals': 2}})
            documents.append(document)
            # Both configurations receive this exact same payload. Retrieval adds
            # documents only in full configuration; no key is included in inputs.
            inputs['definition_notice'] = {'current_document_id': doc_id,
                                          'definition': 'ratio_of_sums', 'version': 'v2'}
            payload = {'request': request, 'structured_data': inputs}
            key = {'case_id': case_id, 'scenario': scenario, 'required_elements': required,
                   'numeric': expected, 'factual': facts, 'required_abstentions': abstain,
                   'warnings': warnings, 'review_status': 'awaiting_human_review',
                   'abstention_coverage_policy': 'A correct explicit abstention satisfies its required element; omission does not.'}
            cases.append({'case_id': case_id, 'product': product, 'scenario': scenario,
                          'payload': payload, 'payload_sha256': digest(payload),
                          'key_sha256': digest(key)})
            keys.append(key)
    schedule = [{'case_id': case['case_id'], 'configuration': configuration,
                 'repetition': repetition, 'payload_sha256': case['payload_sha256'],
                 'key_sha256': case['key_sha256'], 'status': 'not_executed', 'output': None}
                for case in cases for configuration in CONFIGURATIONS for repetition in (1, 2, 3)]
    return {'cases': cases, 'keys': keys, 'documents': documents, 'schedule': schedule}


def require_execution_ready(design, freeze):
    """Fail closed until human keys and exact experimental components are fixed."""
    if any(key['review_status'] != 'reviewed' for key in design['keys']):
        raise ValueError('H4 factual keys require human review before execution')
    for name in ('generator_model', 'generator_version', 'generation_parameters', 'prompt_sha256',
                 'corpus_sha256', 'chunking', 'embedding_model_version', 'retrieval_top_k',
                 'retrieval_thresholds', 'temporal_filters', 'correction_attempts'):
        if name not in freeze or freeze[name] is None:
            raise ValueError('Missing experimental freeze: ' + name)
    if freeze.get('design_sha256') != digest(design):
        raise ValueError('Design differs from reviewed experimental freeze')
    return True
