"""Synthetic compatibility checks only. No historical training or final test."""
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import warnings

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    cache = ROOT/'data/runtime-research-clean/matplotlib-cache'
    cache.mkdir(parents=True, exist_ok=True)
    os.environ['MPLCONFIGDIR'] = str(cache)
    import numpy as np
    import pandas as pd
    import shap
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    from pyod.models.iforest import IForest
    from pyod.models.lof import LOF
    from pyod.models.ecod import ECOD
    from pipeline.research.methodology import candidate_grid

    # Explicit artificial fixture, not saved as export observations.
    rng = np.random.default_rng(42)
    features = pd.DataFrame(rng.normal(size=(160, 5)), columns=[f'x{i}' for i in range(5)])
    targets = {'unit_fob': np.maximum(0., 3+features.x0+features.x1*.2),
               'volume_kg': np.maximum(0., 100+features.x0*20+features.x2*5)}
    checks = []
    for target, y in targets.items():
        for parameters in candidate_grid():
            parameters = dict(parameters)
            algorithm = parameters.pop('algorithm')
            model = XGBRegressor(**parameters) if algorithm == 'xgboost' else LGBMRegressor(**parameters)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                model.fit(features.iloc[:128], y.iloc[:128])
                output = model.predict(features.iloc[128:])
                explanation = shap.TreeExplainer(model)(features.iloc[128:136])
                raw = model.predict(features.iloc[128:136])
            reconstructed = np.asarray(explanation.base_values)+np.asarray(explanation.values).sum(axis=1)
            error = float(np.max(np.abs(raw-reconstructed)))
            tolerance = 1e-4*max(1., float(np.max(np.abs(raw))))
            checks.append({'kind': 'regression_grid_and_shap', 'algorithm': algorithm,
                           'target': target, 'parameters': parameters,
                           'finite_predictions': bool(np.isfinite(output).all()),
                           'shap_raw_scale_max_error': error, 'shap_tolerance': tolerance,
                           'passed': bool(np.isfinite(output).all() and error <= tolerance)})
    for name, model in [('IF', IForest(random_state=42, n_jobs=1)),
                        ('LOF', LOF(n_neighbors=20, n_jobs=1)), ('ECOD', ECOD(n_jobs=1))]:
        model.fit(features.iloc[:128].to_numpy())
        scores = model.decision_function(features.iloc[128:].to_numpy())
        checks.append({'kind': 'out_of_fit_detector_scoring', 'detector': name,
                       'training_rows': 128, 'new_rows': 32,
                       'passed': bool(len(scores) == 32 and np.isfinite(scores).all())})
    out = ROOT/'planificacion/2026-11-01/ejecucion'
    out.mkdir(parents=True, exist_ok=True)
    check = subprocess.run([sys.executable, '-B', '-m', 'pip', 'check'], capture_output=True, text=True)
    packages = {d.metadata['Name']: d.version for d in metadata.distributions() if d.metadata['Name']}
    lock = '\n'.join(f'{name}=={version}' for name, version in sorted(packages.items()) if name.lower() != 'pip')+'\n'
    lock_path = out/'requirements-scientific-clean.txt'
    lock_path.write_text(lock, encoding='utf-8')
    result = {'python': platform.python_version(), 'platform': platform.platform(),
              'scope': 'Windows scientific core, not API/PostgreSQL/RAG/generator stack',
              'synthetic_fixture_only': True, 'historical_data_read': False,
              'final_test_executed': False, 'seed': 42,
              'environment_prefix': str(Path(sys.prefix).relative_to(ROOT)),
              'matplotlib_cache': str(cache.relative_to(ROOT)),
              'base_interpreter_prefix': sys.base_prefix,
              'external_site_packages_enabled': any('site-packages' in p.lower() and
                  not Path(p).resolve().is_relative_to(Path(sys.prefix).resolve()) for p in sys.path),
              'packages': dict(sorted(packages.items())),
              'requirements_sha256': hashlib.sha256(lock_path.read_bytes()).hexdigest(),
              'pip_check_passed': check.returncode == 0, 'pip_check_output': check.stdout.strip(),
              'smoke_all_passed': all(c['passed'] for c in checks), 'checks': checks}
    (out/'environment-clean.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('python', 'scope', 'external_site_packages_enabled',
                                                'pip_check_passed', 'smoke_all_passed')}))
    print(json.dumps({'checks': len(checks), 'passed': sum(c['passed'] for c in checks)}))
    if not result['smoke_all_passed'] or not result['pip_check_passed'] or result['external_site_packages_enabled']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
