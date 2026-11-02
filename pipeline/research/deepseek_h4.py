"""Explicit paid H4 transport, conservative persistent budget, no dotenv reads.

No requests on import/check. A key, opt-in, positive budget and explicit caller
action are required. Prices are user-reviewed ceilings, not a provider billing
guarantee; cached/off-peak discounts are deliberately ignored in accounting.
"""
from contextlib import contextmanager
from decimal import Decimal
import json
import os
from pathlib import Path
import uuid

ENDPOINT='https://api.deepseek.com/chat/completions'
DEFAULTS={'enabled':False,'budget_usd':'0','model':'deepseek-flash',
    'declared_model_version':'DeepSeek-V4.1-Flash-1017','pricing_verified_on':'2026-11-01',
    'input_peak_miss_usd_per_million':'0.30','output_peak_usd_per_million':'1.20',
    'max_prompt_tokens':16000,'max_tokens':800,'temperature':0,'max_requests':181,
    'expected_system_fingerprint':None,'expected_returned_model':None,
    'planned_h4_slots':180,'calibration_slots':1,'correction_attempts':0}


class H4TransportError(RuntimeError):pass


def ceiling_cost(settings,prompt_tokens,completion_tokens):
    return (Decimal(settings['input_peak_miss_usd_per_million'])*prompt_tokens+
            Decimal(settings['output_peak_usd_per_million'])*completion_tokens)/Decimal(1_000_000)


def validate_settings(settings):
    if settings['model']!='deepseek-flash':raise H4TransportError('Model change requires an updated reviewed pricing/configuration contract')
    for key in ('budget_usd','input_peak_miss_usd_per_million','output_peak_usd_per_million'):
        value=Decimal(settings[key])
        if not value.is_finite() or value<0 or key!='budget_usd' and value==0:raise H4TransportError('Invalid budget or pricing ceiling')
    for key in ('max_prompt_tokens','max_tokens','max_requests'):
        if type(settings[key]) is not int or settings[key]<=0:raise H4TransportError('Positive token/request limits required')
    if settings['max_tokens']>8000 or settings['max_prompt_tokens']>64000:raise H4TransportError('H4 transport limits exceeded')
    if settings['temperature']!=0:raise H4TransportError('This H4 transport fixes non-thinking temperature at zero')


class BudgetLedger:
    def __init__(self,path,settings):
        self.path=Path(path);self.settings=settings
        validate_settings(settings)

    @contextmanager
    def locked(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        lock=self.path.with_suffix(self.path.suffix+'.lock')
        try:handle=lock.open('x',encoding='utf-8')
        except FileExistsError:raise H4TransportError('Budget ledger locked; no request sent') from None
        try:
            handle.close()
            state=json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else {
                'schema':'h4-deepseek-budget-v1','accounted_ceiling_usd':'0','requests':[],
                'billing_uncertain':False,'halt_reason':None}
            yield state
            temporary=self.path.with_suffix(self.path.suffix+'.tmp')
            with temporary.open('w',encoding='utf-8') as output:
                json.dump(state,output,indent=2);output.flush();os.fsync(output.fileno())
            os.replace(temporary,self.path)
        finally:
            lock.unlink()

    def reserve(self):
        if self.settings.get('enabled') is not True or Decimal(self.settings['budget_usd'])<=0:
            raise H4TransportError('Paid H4 disabled or budget is zero; no request sent')
        reserved=ceiling_cost(self.settings,self.settings['max_prompt_tokens'],self.settings['max_tokens'])
        request_id=str(uuid.uuid4())
        with self.locked() as state:
            if state['billing_uncertain'] or state['halt_reason']:raise H4TransportError('Budget/run halted; reconcile ledger before sending more requests')
            if any(r['status']=='reserved' for r in state['requests']):raise H4TransportError('Unfinished request reservation; reconcile before another request')
            if len(state['requests'])>=self.settings['max_requests']:raise H4TransportError('Request limit reached')
            if Decimal(state['accounted_ceiling_usd'])+reserved>Decimal(self.settings['budget_usd']):
                raise H4TransportError('Insufficient remaining budget for the next maximum request')
            state['accounted_ceiling_usd']=str(Decimal(state['accounted_ceiling_usd'])+reserved)
            state['requests'].append({'request_id':request_id,'reserved_usd':str(reserved),'status':'reserved'})
        return request_id

    def settle(self,request_id,usage,metadata):
        if not isinstance(usage,dict):
            self.uncertain(request_id,'usage_missing')
            raise H4TransportError('Usage unavailable; reservation retained and ledger halted')
        counts=[usage.get('prompt_tokens'),usage.get('completion_tokens')]
        valid=all(type(v) is int and v>=0 for v in counts)
        valid=valid and counts[0]<=self.settings['max_prompt_tokens'] and counts[1]<=self.settings['max_tokens']
        valid=valid and usage.get('total_tokens',sum(counts) if valid else None)==(sum(counts) if valid else None)
        if not valid:
            self.uncertain(request_id,'invalid_or_over_limit_usage')
            raise H4TransportError('Usage unavailable or beyond reserved limits; ledger halted')
        cost=ceiling_cost(self.settings,*counts)
        with self.locked() as state:
            row=next(r for r in state['requests'] if r['request_id']==request_id)
            if row['status']!='reserved':raise H4TransportError('Request already accounted')
            state['accounted_ceiling_usd']=str(Decimal(state['accounted_ceiling_usd'])-Decimal(row['reserved_usd'])+cost)
            row.update(status='settled',usage=usage,usage_cost_ceiling_usd=str(cost),metadata=metadata)

    def uncertain(self,request_id,reason):
        with self.locked() as state:
            row=next(r for r in state['requests'] if r['request_id']==request_id)
            if row['status']=='reserved':row['status']='billing_uncertain'
            state['billing_uncertain']=True;state['halt_reason']=reason

    def halt(self,reason):
        with self.locked() as state:state['halt_reason']=reason


class DeepSeekH4Transport:
    def __init__(self,settings,ledger_path,api_key=None,session=None):
        self.settings=dict(settings);validate_settings(self.settings)
        self.ledger=BudgetLedger(ledger_path,self.settings)
        self._key=api_key if api_key is not None else os.environ.get('H4_DEEPSEEK_API_KEY','')
        if session is None:
            import requests
            session=requests.Session();session.trust_env=False
        self.session=session

    def status(self):
        return {'provider':'deepseek','model':self.settings['model'],'key_present':bool(self._key),
            'enabled':self.settings.get('enabled') is True,'budget_usd':self.settings['budget_usd'],
            'fingerprint_calibrated':bool(self.settings.get('expected_system_fingerprint')),
            'request_ceiling_usd':str(ceiling_cost(self.settings,self.settings['max_prompt_tokens'],self.settings['max_tokens'])),
            'plan_ceiling_usd':str(ceiling_cost(self.settings,self.settings['max_prompt_tokens'],self.settings['max_tokens'])*self.settings['max_requests']),
            'network_calls_made_by_status':0}

    def _request(self,messages,calibration=False):
        if not self._key:raise H4TransportError('H4_DEEPSEEK_API_KEY is not configured; no request sent')
        if not calibration and not self.settings.get('expected_system_fingerprint'):
            raise H4TransportError('Calibrate and freeze backend fingerprint before experimental calls')
        # A deliberately conservative text-only byte bound plus chat overhead.
        byte_bound=len(json.dumps(messages,ensure_ascii=False).encode('utf-8'))+4096
        if byte_bound>self.settings['max_prompt_tokens']:raise H4TransportError('Input exceeds conservative reserved prompt bound')
        body={'model':self.settings['model'],'messages':messages,'max_tokens':self.settings['max_tokens'],
              'temperature':0,'thinking':{'type':'disabled'},'response_format':{'type':'json_object'},'stream':False}
        request_id=self.ledger.reserve()
        try:
            response=self.session.post(ENDPOINT,headers={'Authorization':'Bearer '+self._key},
                json=body,timeout=(10,90),allow_redirects=False)
            if response.status_code!=200:raise H4TransportError('Provider HTTP request failed')
            result=response.json()
            usage=result.get('usage',{})
        except Exception:
            self.ledger.uncertain(request_id,'transport_or_unreadable_response')
            raise H4TransportError('Provider request failed; reservation retained and ledger halted') from None
        metadata={k:result.get(k) for k in ('id','model','system_fingerprint')}
        self.ledger.settle(request_id,usage,metadata)
        fingerprint=result.get('system_fingerprint')
        if not isinstance(fingerprint,str) or not fingerprint or not isinstance(result.get('model'),str) or not result['model']:
            self.ledger.halt('backend_metadata_missing');raise H4TransportError('Backend version metadata missing; run halted')
        if not calibration and (fingerprint!=self.settings['expected_system_fingerprint'] or
                result['model']!=self.settings['expected_returned_model']):
            self.ledger.halt('backend_changed');raise H4TransportError('Backend fingerprint/model changed; run halted')
        try:
            choice=result['choices'][0]
            if choice['finish_reason']!='stop':raise ValueError('incomplete')
            output=json.loads(choice['message']['content'])
            if not isinstance(output,dict):raise ValueError('object required')
        except (KeyError,IndexError,ValueError,TypeError):
            raise H4TransportError('Output incomplete or invalid JSON; usage already accounted') from None
        return output,metadata

    def calibrate(self):
        _,metadata=self._request([{'role':'system','content':'Return a JSON object only.'},
            {'role':'user','content':'Return {"calibration":"ok"}. This is a transport calibration, not a thesis experiment.'}],calibration=True)
        return metadata

    def __call__(self,payload,documents,freeze,correction):
        if freeze.get('provider_id')!='deepseek' or freeze.get('generator_model')!=self.settings['model']:
            raise H4TransportError('Provider/model differs from experimental freeze')
        if freeze.get('generator_version')!=self.settings['declared_model_version']:
            raise H4TransportError('Declared model version differs from freeze')
        expected={'temperature':0,'max_tokens':self.settings['max_tokens']}
        if freeze.get('generation_parameters')!=expected:raise H4TransportError('Generation parameters differ from freeze')
        if freeze.get('correction_attempts')!=self.settings['correction_attempts']:
            raise H4TransportError('Correction attempts differ from configured request/budget plan')
        if freeze.get('expected_system_fingerprint')!=self.settings.get('expected_system_fingerprint'):
            raise H4TransportError('Fingerprint differs from freeze')
        messages=[{'role':'system','content':freeze['prompt']},
            {'role':'user','content':json.dumps({'input':payload,'retrieved_documents':documents,'correction':correction},ensure_ascii=False)}]
        output,_=self._request(messages)
        return output
