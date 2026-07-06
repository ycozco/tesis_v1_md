import numpy as np

# In-memory mapping of experimental conditions for auditors to allow manual overrides.
USER_CONDITIONS = {
    'auditor1': 'INTEGRADO',
    'auditor2': 'AISLADO'
}

# Global configuration state for the models and thresholds
CONFIG_STATE = {
    'xgboost_version': 'XGBoost v2.1',
    'mae': 0.024,
    'mse': 0.038,
    'r2_score': 0.942,
    'shap_top_k': 5,
    'llm_engine': 'Google Gemini 1.5 Flash',
    'llm_temperature': 0.1,
    'llm_similarity_threshold': 0.75,
    'weights': {
        'isolation_forest': 0.45,
        'lof': 0.30,
        'ecod': 0.25
    },
    'global_threshold': 0.65
}

def calculate_boxplot_stats(values):
    if not values:
        return {'min': 0, 'q1': 0, 'median': 0, 'q3': 0, 'max': 0, 'avg': 0, 'count': 0}
    
    # Convert from milliseconds to seconds
    seconds_vals = [v / 1000.0 for v in values]
    
    q1 = float(np.percentile(seconds_vals, 25))
    median = float(np.percentile(seconds_vals, 50))
    q3 = float(np.percentile(seconds_vals, 75))
    min_val = float(np.min(seconds_vals))
    max_val = float(np.max(seconds_vals))
    avg_val = float(np.mean(seconds_vals))
    
    return {
        'min': round(min_val, 1),
        'q1': round(q1, 1),
        'median': round(median, 1),
        'q3': round(q3, 1),
        'max': round(max_val, 1),
        'avg': round(avg_val, 1),
        'count': len(values)
    }
