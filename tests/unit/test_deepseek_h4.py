from copy import deepcopy
import json
from decimal import Decimal
from types import SimpleNamespace
import pytest
from pipeline.research.deepseek_h4 import DEFAULTS,DeepSeekH4Transport,BudgetLedger,H4TransportError


class Session:
    def __init__(self,result=None,error=False):self.calls=[];self.result=result;self.error=error
    def post(self,*args,**kwargs):
        self.calls.append((args,kwargs))
        if self.error:raise RuntimeError('secret-should-never-be-disclosed')
        return SimpleNamespace(status_code=200,json=lambda:self.result)


def settings():
    result=deepcopy(DEFAULTS);result.update(enabled=True,budget_usd='1',
        expected_system_fingerprint='fixture-fingerprint',expected_returned_model='deepseek-flash')
    return result


def response(fingerprint='fixture-fingerprint',content='{"ok":true}'):
    return {'id':'fixture-response','model':'deepseek-flash','system_fingerprint':fingerprint,
        'usage':{'prompt_tokens':100,'completion_tokens':20,'total_tokens':120},
        'choices':[{'finish_reason':'stop','message':{'content':content}}]}


def test_default_configuration_and_missing_key_never_send_network(tmp_path):
    session=Session(response())
    transport=DeepSeekH4Transport(DEFAULTS,tmp_path/'budget.json',api_key='',session=session)
    assert transport.status()['network_calls_made_by_status']==0
    with pytest.raises(H4TransportError):transport.calibrate()
    transport=DeepSeekH4Transport(DEFAULTS,tmp_path/'budget.json',api_key='fake-key',session=session)
    with pytest.raises(H4TransportError,match='disabled'):transport.calibrate()
    assert session.calls==[]


def test_budget_reservation_blocks_request_before_charge(tmp_path):
    config=settings();config['budget_usd']='0.000001';session=Session(response())
    transport=DeepSeekH4Transport(config,tmp_path/'budget.json',api_key='fake-key',session=session)
    with pytest.raises(H4TransportError,match='Insufficient'):transport.calibrate()
    assert session.calls==[]


def test_exact_endpoint_no_redirects_and_usage_accounting(tmp_path):
    config=settings();session=Session(response());path=tmp_path/'budget.json'
    transport=DeepSeekH4Transport(config,path,api_key='private-fixture-key',session=session)
    output,metadata=transport._request([{'role':'user','content':'JSON fixture'}])
    assert output=={'ok':True}
    args,kwargs=session.calls[0]
    assert args[0]=='https://api.deepseek.com/chat/completions' and kwargs['allow_redirects'] is False
    assert kwargs['json']['thinking']=={'type':'disabled'} and kwargs['json']['response_format']=={'type':'json_object'}
    ledger=json.loads(path.read_text())
    assert Decimal(ledger['accounted_ceiling_usd'])==Decimal('.000054')
    assert 'private-fixture-key' not in path.read_text()


def test_unknown_billing_keeps_reservation_and_prevents_retry(tmp_path):
    config=settings();session=Session(error=True);path=tmp_path/'budget.json'
    transport=DeepSeekH4Transport(config,path,api_key='fake-key',session=session)
    with pytest.raises(H4TransportError) as error:transport.calibrate()
    assert 'secret-should' not in str(error.value)
    assert json.loads(path.read_text())['billing_uncertain']
    with pytest.raises(H4TransportError,match='halted'):transport.calibrate()
    assert len(session.calls)==1


def test_fingerprint_change_accounts_charge_then_halts(tmp_path):
    session=Session(response(fingerprint='different'));path=tmp_path/'budget.json'
    transport=DeepSeekH4Transport(settings(),path,api_key='fake-key',session=session)
    with pytest.raises(H4TransportError,match='fingerprint'):transport._request([{'role':'user','content':'JSON'}])
    assert json.loads(path.read_text())['halt_reason']=='backend_changed'
    with pytest.raises(H4TransportError):transport._request([{'role':'user','content':'JSON'}])
    assert len(session.calls)==1


def test_over_limit_usage_and_unfinished_reservation_fail_closed(tmp_path):
    config=settings();ledger=BudgetLedger(tmp_path/'ledger.json',config)
    pending=ledger.reserve()
    with pytest.raises(H4TransportError,match='Unfinished'):ledger.reserve()
    with pytest.raises(H4TransportError,match='Usage'):
        ledger.settle(pending,{'prompt_tokens':999999,'completion_tokens':0}, {})
    assert json.loads((tmp_path/'ledger.json').read_text())['billing_uncertain']


def test_invalid_json_still_counts_consumption(tmp_path):
    path=tmp_path/'ledger.json';session=Session(response(content='not JSON'))
    transport=DeepSeekH4Transport(settings(),path,api_key='fake-key',session=session)
    with pytest.raises(H4TransportError,match='JSON'):transport._request([{'role':'user','content':'JSON'}])
    assert json.loads(path.read_text())['requests'][0]['status']=='settled'


def test_experimental_callback_requires_matching_parameters_and_attempt_plan(tmp_path):
    config=settings();session=Session(response())
    transport=DeepSeekH4Transport(config,tmp_path/'ledger.json',api_key='fake-key',session=session)
    freeze={'provider_id':'deepseek','generator_model':config['model'],'generator_version':config['declared_model_version'],
        'generation_parameters':{'temperature':0,'max_tokens':800},'expected_system_fingerprint':'fixture-fingerprint',
        'correction_attempts':1,'prompt':'Return JSON'}
    with pytest.raises(H4TransportError,match='Correction attempts'):
        transport({},[],freeze,None)
    assert session.calls==[]
    freeze['correction_attempts']=0
    assert transport({},[],freeze,None)=={'ok':True}
