"""Dependency-free atomic numeric checks shared by API and scientific pipeline."""
from decimal import Decimal


def verify_atomic_claim(claim, evidence):
    """Verify fact/source/unit and half-last-decimal absolute tolerance, not prose."""
    key = claim.get('fact_id')
    if key not in evidence:
        return {'valid': False, 'reason': 'unknown_fact'}
    reference = evidence[key]
    if claim.get('source_id') != reference.get('source_id') or claim.get('unit') != reference.get('unit'):
        return {'valid': False, 'reason': 'source_or_unit_mismatch'}
    try:
        decimals = int(claim['decimals'])
        if decimals < 0 or decimals > 10:
            raise ValueError('Invalid decimal precision')
        value, expected = Decimal(str(claim['value'])), Decimal(str(reference['value']))
        if not value.is_finite() or not expected.is_finite():
            raise ValueError('Non-finite claim')
        tolerance = Decimal('0.5') * Decimal(10) ** -decimals + Decimal('1e-9')
        valid = abs(value - expected) <= tolerance
    except (ValueError, KeyError, ArithmeticError):
        return {'valid': False, 'reason': 'invalid_number'}
    return {'valid': valid, 'reason': 'ok' if valid else 'numeric_error', 'absolute_tolerance': str(tolerance)}
