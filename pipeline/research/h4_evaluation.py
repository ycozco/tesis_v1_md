"""Numeric H4 grading plus mandatory externally supplied blind factual grading.

Undefined rates propagate to strict primary macro results; conditional defined-
case summaries are explicitly diagnostic. This conservative NA policy must be
reviewed before final runs, especially for correctly abstaining zero-denominator
cases. No algorithm claims to have performed a human factual review.
"""
from collections import defaultdict
from decimal import Decimal
from statistics import mean
from math import isfinite


def grade_output(output,key,factual_review):
    if not factual_review.get('atomization_reviewed'):
        raise ValueError('Blind factual atomization review is required')
    numeric=output.get('numeric_claims',[])
    emitted_facts=output.get('factual_claims',[])
    facts=factual_review.get('atoms',emitted_facts)
    if not {c['claim_id'] for c in emitted_facts}.issubset({c['claim_id'] for c in facts}):
        raise ValueError('Human atomization cannot omit emitted factual claims')
    if {c.get('numeric_index') for c in facts if c.get('numeric_index') is not None} != set(range(len(numeric))):
        raise ValueError('Every numeric assertion also needs a factual atom')
    ids=[c['claim_id'] for c in facts]
    judgments=factual_review.get('claims',{})
    if len(set(ids))!=len(ids) or set(ids)!=set(judgments):raise ValueError('Every emitted factual atom must be judged once')
    correct=set();responded=set();errors=0;verifiable=0;unverifiable=0
    seen=set()
    for claim in numeric:
        element=claim['element_id'];responded.add(element)
        if element not in key['numeric']:
            unverifiable+=1;continue
        reference=key['numeric'][element];verifiable+=1
        valid=False
        try:
            value=Decimal(str(claim['value']));expected=Decimal(reference['value'])
            tolerance=Decimal('0.5')*Decimal(10)**-reference['decimals']+Decimal('1e-9')
            valid=value.is_finite() and claim['unit']==reference['unit'] and abs(value-expected)<=tolerance
        except (KeyError,ArithmeticError,ValueError):pass
        # Duplicate elements do not expand coverage or hide a conflicting value.
        if element in seen:valid=False
        seen.add(element)
        if valid:correct.add(element)
        else:errors+=1;correct.discard(element)
    factual_errors=0;contradicted=set()
    for claim in facts:
        element=claim.get('element_id');responded.add(element)
        judgment=judgments[claim['claim_id']]
        if not isinstance(judgment.get('supported'),bool):raise ValueError('Binary factual support judgment required')
        if not judgment['supported']:factual_errors+=1;contradicted.add(element)
        elif judgment.get('correct_required_element') and element in key['factual']:correct.add(element)
    abstentions=set(output.get('abstentions',[]));responded |= abstentions
    correct |= abstentions & set(key['required_abstentions'])
    correct -= contradicted
    required=set(key['required_elements'])
    return {'numeric_errors':errors,'numeric_verifiable':verifiable,'numeric_unverifiable':unverifiable,
        'numeric_error_rate':errors/verifiable if verifiable else None,
        'factual_errors':factual_errors,'factual_emitted':len(facts),
        'factual_error_rate':factual_errors/len(facts) if facts else None,
        'coverage':len(required&correct)/len(required) if required else None,
        'omitted_elements':sorted(required-responded),'abstentions':sorted(abstentions),
        'reviewer_id':factual_review.get('reviewer_id'),'review_mode':factual_review.get('review_mode')}


def aggregate_paired(grades):
    groups=defaultdict(list)
    for row in grades:groups[(row['case_id'],row['configuration'])].append(row)
    if len(groups)!=60:raise ValueError('Thirty cases in both configurations required')
    universes={configuration:{case for case,arm in groups if arm==configuration} for configuration in {arm for _,arm in groups}}
    if len(universes)!=2 or len({tuple(sorted(ids)) for ids in universes.values()})!=1:raise ValueError('Same paired cases required')
    cases=[]
    for (case,configuration),rows in sorted(groups.items()):
        if len(rows)!=3 or {r['repetition'] for r in rows}!={1,2,3}:raise ValueError('Exactly three repetitions per case/configuration')
        item={'case_id':case,'configuration':configuration}
        for metric in ('numeric_error_rate','factual_error_rate','coverage'):
            values=[r[metric] for r in rows]
            if any(v is not None and (not isfinite(v) or not 0<=v<=1) for v in values):raise ValueError('Invalid metric rate')
            item[metric]=mean(values) if all(v is not None for v in values) else None
        cases.append(item)
    arms={}
    for configuration in {r['configuration'] for r in cases}:
        rows=[r for r in cases if r['configuration']==configuration]
        if len(rows)!=30:raise ValueError('Equal case universe required')
        arm={}
        for metric in ('numeric_error_rate','factual_error_rate','coverage'):
            defined=[r[metric] for r in rows if r[metric] is not None]
            arm[metric]=mean(defined) if len(defined)==30 else None
            arm[metric+'_defined_cases']=len(defined)
            arm[metric+'_conditional_diagnostic']=mean(defined) if defined else None
        arms[configuration]=arm
    reference=arms.get('reference_no_retrieval_no_validation');full=arms.get('full_RAG_and_validation')
    if reference is None or full is None:raise ValueError('Both prescribed configurations required')
    if any(a[m] is None for a in (reference,full) for m in ('numeric_error_rate','factual_error_rate','coverage')):
        status='not_conclusive_undefined_primary_rates'
    elif full['coverage']<reference['coverage']-.05:
        status='not_conclusive_coverage_loss_exceeds_5pp'
    elif all(full[m]<reference[m] for m in ('numeric_error_rate','factual_error_rate')):
        status='descriptively_supported'
    elif all(full[m]>=reference[m] for m in ('numeric_error_rate','factual_error_rate')):
        status='not_supported'
    else:status='not_conclusive_mixed_errors'
    return {'status':status,'case_count':30,'repetitions_per_case_configuration':3,
        'independent_sample_size_not_180':True,'case_means':cases,'arms':arms,
        'aggregation_policy':'mean three within case, then thirty equal cases; any undefined case propagates NA to primary macro'}
