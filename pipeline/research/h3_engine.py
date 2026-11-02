"""Prior-only H3 detector integration. Final historical data must be certified.

ECOD is an explicitly documented inductive adaptation: empirical tails and
skewness are frozen on training. PyOD 3.6's public scoring appends the new batch;
that transductive behavior is unsuitable for the prior-only protocol here.
"""
from datetime import datetime
import hashlib
import json
import numpy as np
from scipy.stats import skew
from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pipeline.research.h3_rules import calibrated_ensemble, select_per_product, persistence_summary


def stamp(value):
    result=datetime.fromisoformat(value.replace('Z','+00:00'))
    if result.tzinfo is None:raise ValueError('Availability needs timezone')
    return result


class FrozenECOD:
    def fit(self, X):
        X=np.asarray(X,dtype=float)
        if X.ndim!=2 or len(X)<2 or not np.isfinite(X).all():raise ValueError('Finite training matrix required')
        self.sorted=np.sort(X,axis=0)
        signs=skew(X,axis=0,bias=True)
        self.signs=np.sign(np.nan_to_num(signs,nan=0.))
        self.floor=1/(len(X)+1)
        return self

    def decision_function(self,X):
        X=np.asarray(X,dtype=float)
        if X.ndim!=2 or X.shape[1]!=self.sorted.shape[1] or not np.isfinite(X).all():raise ValueError('Invalid new cases')
        n=len(self.sorted)
        left=np.column_stack([np.searchsorted(self.sorted[:,j],X[:,j],side='right')/n for j in range(X.shape[1])])
        right=np.column_stack([(n-np.searchsorted(self.sorted[:,j],X[:,j],side='left'))/n for j in range(X.shape[1])])
        ul=-np.log(np.clip(left,self.floor,1.))
        ur=-np.log(np.clip(right,self.floor,1.))
        directed=ul*-np.sign(self.signs-1)+ur*np.sign(self.signs+1)
        return np.maximum(np.maximum(ul,ur),directed).sum(axis=1)


def score_origin(history,current,score_at,features,minimum_training=40):
    """One product, one target week; cases already have OOS forecast residuals.

    Explicit artificial fixtures bypass historical certificates only when every
    row is labelled artificial. Row identity overlap and future features fail.
    """
    if not current:return {'rows':[],'audit':{'status':'empty_current_universe'}}
    products={r['product'] for r in current}
    weeks={r['week'] for r in current}
    if len(products)!=1 or len(weeks)!=1:raise ValueError('One product and target week per origin')
    origin=stamp(score_at);week=next(iter(weeks));product=next(iter(products))
    train=[r for r in history if r['product']==product and r['week']<week and stamp(r['available_at'])<=origin]
    if len(train)<minimum_training:raise ValueError('Insufficient prior training observations')
    ids=[r['id'] for r in train+current]
    if len(ids)!=len(set(ids)):raise ValueError('Training/current identities overlap')
    for row in train+current:
        if stamp(row['available_at'])>origin:raise ValueError('Future feature availability')
        if not row.get('forecast_is_oos'):raise ValueError('Predictive residual requires OOS forecast')
        if row.get('data_kind')!='artificial' and not row.get('coverage_certified'):
            raise ValueError('Historical coverage is not certified')
    X=np.array([[r['features'][f] for f in features] for r in train],dtype=float)
    Y=np.array([[r['features'][f] for f in features] for r in current],dtype=float)
    if not np.isfinite(X).all() or not np.isfinite(Y).all():raise ValueError('Missing/nonfinite features')
    scaler=StandardScaler().fit(X)
    X,Y=scaler.transform(X),scaler.transform(Y)
    models={'IF':IForest(n_estimators=100,random_state=42,n_jobs=1),
            'LOF':LOF(n_neighbors=min(20,len(X)-1),novelty=True,n_jobs=1),
            'ECOD':FrozenECOD()}
    training_scores={};new_scores={}
    for name,model in models.items():
        model.fit(X)
        # Both distributions use the same score function, with frozen fitted state.
        training_scores[name]=model.decision_function(X)
        new_scores[name]=model.decision_function(Y)
    results=[]
    for i,row in enumerate(current):
        calibrated=calibrated_ensemble(training_scores,{n:new_scores[n][i] for n in models})
        results.append({k:row[k] for k in ('id','product','destination','week')}|{
            'raw_scores':{n:float(new_scores[n][i]) for n in models},
            'percentiles':calibrated['percentiles'],'ensemble':calibrated['ensemble'],
            'historical_reference':abs(row['features']['relative_change52'])})
    fingerprint=hashlib.sha256(json.dumps(train,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'rows':results,'audit':{'training_rows':len(train),'product':product,'week':week,
        'score_at':score_at,'latest_training_week':max(r['week'] for r in train),
        'training_rows_sha256':fingerprint,'features':features,'scaler_mean':scaler.mean_.tolist(),
        'scaler_scale':scaler.scale_.tolist(),'minimum_training':minimum_training,
        'LOF_novelty':True,'IF_trees':100,'seed':42,'ECOD':'frozen_training_ecdf_skew_floor_1_over_n_plus_1'}}


def common_budget_analysis(scored,labels):
    """All five methods share exactly the same finite candidate universe."""
    methods=('IF','LOF','ECOD','ensemble','historical_reference')
    selections={}
    for method in methods:
        candidates=[{'id':r['id'],'product':r['product'],'destination':r['destination'],
            'week':r['week'],'score':r['percentiles'][method] if method in ('IF','LOF','ECOD') else r[method]}
            for r in scored]
        selections[method]=select_per_product(candidates)
    summaries=[];overlaps=[]
    for method,products in selections.items():
        for product,ids in products.items():
            for threshold in ('0.1','0.2','0.3'):
                summaries.append({'method':method,'product':product,'threshold':threshold,
                    **persistence_summary([labels[threshold][case] for case in ids])})
    for i,left in enumerate(methods):
        for right in methods[i+1:]:
            for product,ids in selections[left].items():
                a,b=set(ids),set(selections[right][product])
                overlaps.append({'product':product,'left':left,'right':right,
                    'intersection':len(a&b),'union':len(a|b),'jaccard':len(a&b)/len(a|b) if a|b else None})
    return {'selections':selections,'summaries':summaries,'overlaps':overlaps}
