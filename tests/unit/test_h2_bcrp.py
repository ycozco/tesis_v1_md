import importlib.util
from pathlib import Path
import pytest

SPEC=importlib.util.spec_from_file_location('h2_bcrp',Path(__file__).resolve().parents[2]/'tools/reconcile_h2_bcrp.py')
MODULE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_precision_comparison_does_not_replace_original_values():
    assert MODULE.compare_rounded('3.44349','3.443')
    assert not MODULE.compare_rounded('3.444','3.443')


def test_document_date_and_month_end_are_not_availability_certificates():
    candidate={'month':'2025-01','value':'3.747','document_date':'2026-05-14',
               'evidence_status':'indexed_transcription_original_not_verified',
               'verified_available_at':None}
    assert MODULE.eligible_context([candidate],'2026-10-01T00:00:00Z') == []
    candidate.update(evidence_status='original_verified',verified_available_at='2026-05-15T00:00:00Z')
    assert MODULE.eligible_context([candidate],'2025-12-01T00:00:00Z') == []
    assert MODULE.eligible_context([candidate],'2026-05-15T00:00:00Z') == [candidate]


def test_incomplete_month_and_naive_timestamps_are_rejected():
    candidate={'month':'2026-05','evidence_status':'original_verified','verified_available_at':'2026-05-15T00:00:00Z'}
    assert MODULE.eligible_context([candidate],'2026-05-20T00:00:00Z') == []
    with pytest.raises(ValueError,match='Timezone'):
        MODULE.eligible_context([],'2026-05-20T00:00:00')


def test_publication_cannot_precede_the_document_that_supports_it():
    candidate={'month':'2025-01','document_date':'2026-05-14',
               'evidence_status':'original_verified','verified_available_at':'2025-02-01T00:00:00Z'}
    assert MODULE.eligible_context([candidate],'2026-06-01T00:00:00Z') == []
    candidate.pop('document_date')
    assert MODULE.eligible_context([candidate],'2026-06-01T00:00:00Z') == []
