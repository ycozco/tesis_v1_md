import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from protocol import prepare, eligibility

app = FastAPI()
STATE=Path('/state'); STATE.mkdir(exist_ok=True)
_lock=threading.Lock(); _active=None
# A service restart cannot resume dead training processes.
if (STATE/'latest.json').exists():
    previous=json.loads((STATE/'latest.json').read_text())['id']
    previous_manifest=STATE/previous/'manifest.json'
    if previous_manifest.exists():
        previous_data=json.loads(previous_manifest.read_text())
        if previous_data.get('status')=='running':
            previous_data['status']='interrupted'
            previous_manifest.write_text(json.dumps(previous_data))

def write_json(path, value):
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temporary.write_text(json.dumps(value,allow_nan=False));temporary.replace(path)

def versions():
    return {name:importlib.metadata.version(name) for name in ('statsforecast','autogluon.timeseries','torch')}

@app.get('/health')
def health(): return {'status':'ok','versions':versions()}

class Training(BaseModel):
    model_config=ConfigDict(extra='forbid')
    product:Literal['palta','uva','arandano']='uva'
    destination:str=Field(default='US',pattern=r'^[A-Z0-9]{2}$')
    target:Literal['unit_fob','volume_kg']='unit_fob'
    horizon:Literal[1,2,4]=1
    parallel:bool=True
    time_limit:int=Field(default=60,ge=30,le=180)
    validation_end:str|None=Field(default=None,pattern=r'^\d{4}-\d{2}-\d{2}$')

def read_job(id):
    if not id or not (STATE/id/'manifest.json').exists(): return None
    manifest=json.loads((STATE/id/'manifest.json').read_text())
    manifest['results']={lib:json.loads((STATE/id/f'{lib}.json').read_text()) if (STATE/id/f'{lib}.json').exists() else {'status':'running' if manifest['status']=='running' else 'interrupted'} for lib in ('statsforecast','autogluon')}
    return manifest

@app.get('/status')
def status(product:Literal['palta','uva','arandano']='uva', destination:str='US', target:Literal['unit_fob','volume_kg']='unit_fob', horizon:int=1, validation_end:str|None=None):
    latest=STATE/'latest.json'
    try: info=eligibility('/input/snapshot.json',product,destination,target,horizon,validation_end)
    except ValueError as error: raise HTTPException(422,str(error))
    jobs=[]
    for path in sorted(STATE.glob('*/manifest.json'),key=lambda p:p.stat().st_mtime,reverse=True):
        m=json.loads(path.read_text()); config=m['config']
        if config['product']==product and config['destination']==destination and config['target']==target:
            jobs.append(read_job(m['id']))
            if len(jobs)>=10: break
    return {'installed':versions(),'parallel_default':True,'eligibility':info,'job':jobs[0] if jobs else None,'jobs':jobs,'active_job':read_job(_active) if _active else None}

def run_one(path,lib,budget):
    with (path/f'{lib}.log').open('w') as log:
        try:
            subprocess.run([sys.executable,'/worker/fit.py',str(path),lib],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=budget+120)
            if not (path/f'{lib}.json').exists(): raise RuntimeError('Worker did not produce a result')
        except Exception as error:
            write_json(path/f'{lib}.json',{'status':'failed','library':lib,'error':str(error)[:500]})

def run_job(path,body):
    global _active
    try:
        if body.parallel:
            with ThreadPoolExecutor(max_workers=2) as pool:
                list(pool.map(lambda lib:run_one(path,lib,body.time_limit),('statsforecast','autogluon')))
        else:
            for lib in ('statsforecast','autogluon'):run_one(path,lib,body.time_limit)
    finally:
        m=json.loads((path/'manifest.json').read_text());m['status']='completed' if all(json.loads((path/f'{lib}.json').read_text())['status']=='completed' for lib in ('statsforecast','autogluon')) else 'completed_with_errors';m['ended_at_epoch']=time.time();write_json(path/'manifest.json',m)
        with _lock:_active=None

@app.post('/start')
def start(body:Training):
    global _active
    with _lock:
        if _active: raise HTTPException(409,'Ya hay un entrenamiento activo. Espere a que termine.')
        try: train,test=prepare('/input/snapshot.json',body.product,body.destination,body.target,body.horizon,body.validation_end)
        except ValueError as error: raise HTTPException(422,str(error))
        id=uuid.uuid4().hex;path=STATE/id;path.mkdir()
        config={**body.model_dump(),'train':train,'test':test}
        content=json.dumps(config,sort_keys=True).encode();(path/'input.json').write_bytes(content)
        manifest={'id':id,'status':'running','tag':'Entrenamiento paralelo experimental' if body.parallel else 'Entrenamiento secuencial experimental','parallel':body.parallel,'config':body.model_dump(),'started_at_epoch':time.time(),'train_start':train[0]['timestamp'],'train_end':train[-1]['timestamp'],'validation_weeks':[r['timestamp'] for r in test], 'train_weeks':len(train),'versions':versions(),'input_sha256':hashlib.sha256(content).hexdigest(),'source_sha256':hashlib.sha256(Path('/input/snapshot.json').read_bytes()).hexdigest(),'scope':'single_development_holdout','test_final_executed':False}
        lockfile = Path('/opt/training-requirements.lock')
        manifest['requirements_sha256'] = hashlib.sha256(lockfile.read_bytes()).hexdigest()
        manifest['source_revision'] = os.environ.get('AGRO_SOURCE_REVISION') or None
        write_json(path/'manifest.json',manifest);write_json(STATE/'latest.json',{'id':id});_active=id
        threading.Thread(target=run_job,args=(path,body),daemon=True).start()
        return manifest
