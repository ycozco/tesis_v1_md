"""H2 decision rules: one usable contextual family suffices; no invented clocks.

Different source units, frequency or commercial level are not automatic exclusions
for a covariate. Their interpretation, availability and alignment need evidence.
"""


def decide_h2(source_inventory, target_eligible_rows, paired_cases, protocol_ready=False):
    if target_eligible_rows < 0 or paired_cases < 0:
        raise ValueError('Counts must be nonnegative')
    if not source_inventory:
        raise ValueError('An audited source inventory is required')
    eligible = [source for source in source_inventory if source['verified_eligible_rows'] > 0]
    reasons = []
    if not eligible:
        reasons.append('no_verified_compatible_context_available_at_origins')
    if target_eligible_rows == 0:
        reasons.append('no_coverage_and_availability_verified_target_rows')
    if paired_cases == 0:
        reasons.append('empty_eligible_paired_comparison_universe')
    if reasons:
        return {'status':'closed_not_evaluable_current_release','reasons':reasons,
                'eligible_context_families':len(eligible),'metrics':None,
                'supports_h2':None,'refutes_h2':None,'ablation_executed':False}
    if not protocol_ready:
        return {'status':'requires_protocol_freeze_and_development_selection',
                'eligible_context_families':len(eligible),'metrics':None,
                'supports_h2':None,'refutes_h2':None,'ablation_executed':False}
    return {'status':'ready_for_paired_ablation_not_executed',
            'eligible_context_families':len(eligible),'metrics':None,
            'supports_h2':None,'refutes_h2':None,'ablation_executed':False}
