"""Seeded blinded technical grading packets and descriptive agreement."""
from collections import defaultdict
from datetime import datetime,timedelta
import random


def blind_packet(traces,case_payloads,seed=42,private_blind_seed=None):
    if len(traces)!=180:raise ValueError('Complete 180-output catalogue required')
    if len({(r['case_id'],r['configuration'],r['repetition']) for r in traces})!=180:raise ValueError('Duplicate run identities')
    strata=defaultdict(list)
    for index,row in enumerate(traces):strata[(row['product'],row['configuration'])].append(index)
    if len(strata)!=6 or any(len(v)!=30 for v in strata.values()):raise ValueError('Six balanced product/configuration strata required')
    rng=random.Random(seed);names=sorted(strata);extra=set(rng.sample(names,3));sample=set()
    for name in names:sample.update(rng.sample(strata[name],8 if name in extra else 7))
    # Seed 42 is public for sampling, never reused to expose the arm mapping.
    order=list(range(180))
    blind_rng=random.SystemRandom() if private_blind_seed is None else random.Random(private_blind_seed)
    blind_rng.shuffle(order)
    public=[];private=[];sample_ids=[]
    for number,index in enumerate(order,1):
        row=traces[index];blind_id=f'B{number:03}'
        public.append({'blind_id':blind_id,'case_id':row['case_id'],
            'input':case_payloads[row['case_id']],'output':row['final'],
            'execution_kind':row['execution_kind'],
            'factual_review':None})
        private.append({'blind_id':blind_id,'case_id':row['case_id'],'configuration':row['configuration'],
            'repetition':row['repetition'],'product':row['product'],'second_review_selected':index in sample})
        if index in sample:sample_ids.append(blind_id)
    return {'public':public,'private_mapping_keep_hidden':private,'second_review_ids':sample_ids,
            'sample_seed':seed,'sample_size':45,'stratum_counts':{str(k):sum(i in sample for i in v) for k,v in strata.items()}}


def require_repeat_delay(first_review_at,repeated_at):
    first=datetime.fromisoformat(first_review_at.replace('Z','+00:00'))
    second=datetime.fromisoformat(repeated_at.replace('Z','+00:00'))
    if first.tzinfo is None or second.tzinfo is None:raise ValueError('Timezone required')
    if second-first<timedelta(days=7):raise ValueError('Intra-rater repeat requires seven days')


def agreement(first,second):
    """Keys are (blind_output_id, atomic_claim_id); no independence/CI claim."""
    if set(first)!=set(second):raise ValueError('Same atomic claims required before adjudication')
    if any(not isinstance(v,bool) for v in list(first.values())+list(second.values())):raise ValueError('Binary ratings required')
    n=len(first)
    if not n:return {'claims':0,'outputs':0,'agreement':None,'kappa':None}
    observed=sum(first[k]==second[k] for k in first)/n
    a=sum(first.values())/n;b=sum(second.values())/n
    expected=a*b+(1-a)*(1-b)
    return {'claims':n,'outputs':len({key[0] for key in first}),'agreement':observed,
        'kappa':(observed-expected)/(1-expected) if expected<1 else None,
        'scope':'descriptive pre-adjudication agreement; claims clustered within outputs, no inferential independence assumed'}
