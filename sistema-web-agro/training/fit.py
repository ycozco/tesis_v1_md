import json
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd

job_path, library = Path(sys.argv[1]), sys.argv[2]
config = json.loads((job_path/'input.json').read_text())
train = pd.DataFrame(config['train']); test = pd.DataFrame(config['test'])
train['ds'] = pd.to_datetime(train.timestamp)
train['unique_id'] = 'selected-series'; train['y'] = train.target
started = time.time()
try:
    if library == 'statsforecast':
        from statsforecast import StatsForecast
        from statsforecast.models import AutoETS, AutoARIMA, Naive
        model = StatsForecast(models=[AutoETS(season_length=1), AutoARIMA(season_length=1), Naive()], freq='W-MON', n_jobs=1)
        forecasts = model.forecast(df=train[['unique_id','ds','y']], h=len(test))
        models = [c for c in forecasts if c not in ('unique_id','ds')]
        output = [{'model':name, 'values':[max(0.,float(v)) for v in forecasts[name]]} for name in models]
    else:
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
        ts = TimeSeriesDataFrame.from_data_frame(train[['unique_id','ds','target']].rename(columns={'unique_id':'item_id'}), id_column='item_id', timestamp_column='ds')
        ts = ts[['target']]
        predictor = TimeSeriesPredictor(path=str(job_path/'autogluon_models'), prediction_length=len(test), target='target', eval_metric='MAE', freq='W-MON', verbosity=1)
        predictor.fit(ts, hyperparameters={'ETS':{'seasonal_period':1,'n_jobs':1}, 'DirectTabular':{'lags':[1,2,3,4,8,12], 'model_name':'GBM', 'model_hyperparameters':{'num_boost_round':50,'num_threads':1}}}, time_limit=config['time_limit'], num_val_windows=1, enable_ensemble=True, random_seed=42)
        output = []
        for name in predictor.model_names():
            pred = predictor.predict(ts, model=name)
            output.append({'model':name, 'values':[max(0.,float(v)) for v in pred['mean']]})
    truth = test.target.to_numpy(dtype=float)
    for row in output:
        error = np.abs(np.array(row['values']) - truth)
        row['mae'] = float(error.mean())
        row['wape'] = float(100*error.sum()/np.abs(truth).sum()) if np.abs(truth).sum()>0 else None
    result = {'status':'completed','library':library,'started_at_epoch':started,'ended_at_epoch':time.time(),'models':output,
              'weeks':test.timestamp.tolist(),'actual':truth.tolist(), 'evaluation':'single_development_holdout_not_final_validation'}
except Exception as error:
    result = {'status':'failed','library':library,'error':str(error)[:1200],'started_at_epoch':started,'ended_at_epoch':time.time()}
temporary=job_path/f'{library}.json.tmp'
temporary.write_text(json.dumps(result,allow_nan=False),encoding='utf-8')
temporary.replace(job_path/f'{library}.json')
