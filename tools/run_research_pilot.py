"""Retrospective DEVELOPMENT pilot only: weekly refit, OOS errors and model checks.

This is not H1-H4 confirmation: incomplete coverage and no historical vintages.
No held-out-test predictions, no automatic chapter updates, no API calls.
"""
import json
from pathlib import Path
import sys
import warnings
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import shap

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.research.protocol import past_training, macro_mae, residual_interval


def run():
    out = ROOT / 'datasets/tratamiento/2026-11-01'
    calendar = pd.read_csv(out / 'calendario-provisional.csv', parse_dates=['target_week', 'emission'])
    dates = calendar.loc[calendar.split == 'development_pilot', 'emission']
    predictions, checks, selected = [], [], {}
    # Pilot grid only; final protocol grid must be frozen independently before test.
    candidates = {'xgb': lambda: XGBRegressor(n_estimators=60, max_depth=3, learning_rate=.05,
                    random_state=42, n_jobs=1),
                  'lgb': lambda: LGBMRegressor(n_estimators=60, max_depth=3, num_leaves=7,
                    learning_rate=.05, random_state=42, n_jobs=1, verbosity=-1)}
    for view in ['conservadora', 'sensibilidad']:
        for embargo in (0, 4, 8):
            table = pd.read_parquet(out / f'features-{view}-L{embargo}.parquet')
            columns = [c for c in table if '_lag' in c or '_mean4' in c]
            # Stable literal one-hot categories; no target statistics or fitted future scaler.
            categories = pd.get_dummies(table[['producto', 'destino']], dtype=float)
            X = pd.concat([table[columns], categories], axis=1).astype(float)
            for target in ['unit_fob', 'volume_kg']:
                target_name = 'target_' + target
                last_fit = {}
                for emission in dates:
                    train = past_training(table, emission, target_name)
                    train = train[train[target + '_lag0'].notna()]
                    current = table[(table.emission == emission) & table[target_name].notna() & table[target + '_lag0'].notna()]
                    if len(train) < 30 or current.empty:
                        continue
                    values = {'naive': current[target + '_lag0'].to_numpy(),
                              'mean4': current[target + '_mean4'].to_numpy(),
                              'seasonal52': current[target + '_seasonal52_reference'].to_numpy()}
                    for name, constructor in candidates.items():
                        model = constructor()
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore', UserWarning)
                            model.fit(X.loc[train.index], train[target_name])
                            values[name] = np.maximum(0, model.predict(X.loc[current.index]))
                        last_fit[name] = (model, X.loc[current.index].iloc[:8])
                    for name, outputs in values.items():
                        for (_, row), prediction in zip(current.iterrows(), outputs):
                            predictions.append({'view':view, 'L':embargo, 'target':target,
                                'method':name, 'producto':row.producto, 'destino':row.destino,
                                'emission':emission, 'target_week':row.target_week,
                                'actual':float(row[target_name]), 'prediction':float(prediction)})
                # Verify raw model SHAP scale, explicitly separate from nonnegative clipping.
                for name, (model, sample) in last_fit.items():
                    explanation = shap.TreeExplainer(model)(sample)
                    raw = np.asarray(model.predict(sample))
                    reconstructed = explanation.base_values + explanation.values.sum(axis=1)
                    error = float(np.max(np.abs(raw - reconstructed)))
                    scale = max(1., float(np.max(np.abs(raw))))
                    checks.append({'view':view, 'L':embargo, 'target':target, 'method':name,
                        'raw_output_scale':'original_target_no_log', 'max_additive_error':error,
                        'relative_to_max_output':error/scale, 'passed': error <= 1e-4*scale,
                        'clipped_outputs_require_separate_explanation':True})
    frame = pd.DataFrame(predictions)
    frame.to_parquet(out / 'predicciones-desarrollo-piloto.parquet', index=False)
    metrics = []
    keys = ['view', 'L', 'target']
    for key, block in frame.groupby(keys):
        # Same universe across the two models and naive. Seasonal/mean4 coverage explicit.
        for method, rows in block.groupby('method'):
            valid = rows.dropna(subset=['prediction'])
            metrics.append(dict(zip(keys, key)) | {'method':method, 'n_candidates':len(rows),
                'n_predictions':len(valid), 'series':len(valid.groupby(['producto','destino'])),
                'macro_mae':macro_mae(valid), 'role':'development_pilot_NOT_final_inference'})
        competing = [m for m in metrics if tuple(m[k] for k in keys) == key and m['method'] in candidates and m['macro_mae'] is not None]
        if competing:
            selected['|'.join(map(str,key))] = min(competing, key=lambda m:m['macro_mae'])['method']
    pd.DataFrame(metrics).to_csv(out / 'metricas-desarrollo-piloto.csv', index=False)
    paired = []
    join = ['view','L','target','producto','destino','emission','target_week']
    for model_name in candidates:
        model_rows = frame[frame.method==model_name]
        for reference in ('naive','mean4','seasonal52'):
            pairs = model_rows.merge(frame[frame.method==reference][join+['prediction']],
                                     on=join, suffixes=('', '_reference')).dropna(subset=['prediction_reference'])
            for key, rows in pairs.groupby(keys):
                paired.append(dict(zip(keys,key)) | {'model':model_name,'reference':reference,
                    'n_paired':len(rows),'model_macro_mae':macro_mae(rows),
                    'reference_macro_mae':macro_mae(rows,prediction='prediction_reference')})
    pd.DataFrame(paired).to_csv(out/'metricas-emparejadas-piloto.csv',index=False)
    # Calibrate ONLY same-series errors from earlier emissions, with outcome already observed.
    frame = frame[frame.method.isin(candidates)].sort_values('emission')
    intervals = []
    for key, group in frame.groupby(['view','L','target','method','producto','destino']):
        for row in group.itertuples():
            available = group[group.target_week + pd.Timedelta(weeks=1 + int(key[1])) <= row.emission]
            history = (available.actual - available.prediction).tolist()
            for coverage in (.9,.95):
                for window in (None,52):
                    interval = residual_interval(row.prediction, history, coverage, window)
                    intervals.append({'view':key[0], 'L':key[1], 'target':key[2], 'method':key[3],
                        'producto':key[4], 'destino':key[5], 'emission':str(row.emission),
                        'coverage':coverage, 'window':str(window) if window else 'expanding', 'past_errors':len(history),
                        'status':'calibrated' if interval else 'insufficient_40_prior_OOS_errors',
                        'lower':interval[0] if interval else None,'upper':interval[1] if interval else None})
    pd.DataFrame(intervals).to_parquet(out / 'estado-intervalos-piloto.parquet', index=False)
    report = {'status':'retrospective_development_pilot', 'test_executed':False,
        'models':'one fixed small configuration per library; NOT final hyperparameter selection grid',
        'selection_development_only':selected, 'shap':checks, 'predictions':len(predictions),
        'intervals_calibrated':sum(i['status']=='calibrated' for i in intervals),
        'limits':['Incomplete source coverage', 'No certified as-of vintages',
                  'No H2 eligible contextual covariates', 'No MASE final seasonal denominator',
                  'No H3 truth labels or H4 generated evaluation claimed']}
    (out / 'piloto-resumen.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'predictions':len(predictions), 'shap_checks':len(checks),
        'shap_passed':all(c['passed'] for c in checks), 'test_executed':False}))


if __name__ == '__main__':
    run()
