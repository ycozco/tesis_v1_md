import os
import numpy as np
import joblib
import xgboost as xgb
from services.common import CONFIG_STATE

scaler = None
xgb_model = None
iforest = None
lof = None
ecod = None

def load_ml_models():
    global scaler, xgb_model, iforest, lof, ecod
    try:
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workspace_root = os.path.dirname(backend_dir)
        models_dir = os.path.join(workspace_root, 'models')
        
        # 1. Scaler
        if scaler is None:
            real_path = os.path.join(models_dir, 'anomaly_scaler.pkl')
            mock_path = os.path.join(backend_dir, 'models_weights/scaler_fob.bin')
            loaded = False
            if os.path.exists(real_path):
                try:
                    s = joblib.load(real_path)
                    if hasattr(s, 'n_features_in_') and s.n_features_in_ == 4:
                        scaler = s
                        loaded = True
                        print("Scaler real de 4 variables cargado.")
                except Exception:
                    pass
            if not loaded and os.path.exists(mock_path):
                scaler = joblib.load(mock_path)
                print("Scaler mock de 4 variables cargado.")
                
        # 2. XGBoost Predictor
        if xgb_model is None:
            real_path = os.path.join(models_dir, 'xgb_price_model.pkl')
            mock_path = os.path.join(backend_dir, 'models_weights/xgboost_fob_predictor.json')
            loaded = False
            if os.path.exists(real_path):
                try:
                    m = joblib.load(real_path)
                    if hasattr(m, 'n_features_in_') and m.n_features_in_ == 4:
                        xgb_model = m
                        loaded = True
                        print("XGBoost real de 4 variables cargado.")
                except Exception:
                    pass
            if not loaded and os.path.exists(mock_path):
                xgb_model = xgb.Booster()
                xgb_model.load_model(mock_path)
                print("XGBoost mock de 4 variables cargado.")

        # 3. Isolation Forest
        if iforest is None:
            real_path = os.path.join(models_dir, 'if_model.pkl')
            mock_path = os.path.join(backend_dir, 'models_weights/iforest_model.pkl')
            loaded = False
            if os.path.exists(real_path):
                try:
                    m = joblib.load(real_path)
                    if hasattr(m, 'n_features_in_') and m.n_features_in_ == 4:
                        iforest = m
                        loaded = True
                        print("IForest real de 4 variables cargado.")
                except Exception:
                    pass
            if not loaded and os.path.exists(mock_path):
                iforest = joblib.load(mock_path)
                print("IForest mock de 4 variables cargado.")

        # 4. LOF
        if lof is None:
            real_path = os.path.join(models_dir, 'lof_model.pkl')
            mock_path = os.path.join(backend_dir, 'models_weights/lof_model.pkl')
            loaded = False
            if os.path.exists(real_path):
                try:
                    m = joblib.load(real_path)
                    if hasattr(m, 'n_features_in_') and m.n_features_in_ == 4:
                        lof = m
                        loaded = True
                        print("LOF real de 4 variables cargado.")
                except Exception:
                    pass
            if not loaded and os.path.exists(mock_path):
                lof = joblib.load(mock_path)
                print("LOF mock de 4 variables cargado.")

        # 5. ECOD
        if ecod is None:
            real_path = os.path.join(models_dir, 'ecod_model.pkl')
            mock_path = os.path.join(backend_dir, 'models_weights/ecod_model.pkl')
            loaded = False
            if os.path.exists(real_path):
                try:
                    m = joblib.load(real_path)
                    if hasattr(m, 'n_features_in_') and m.n_features_in_ == 4:
                        ecod = m
                        loaded = True
                        print("ECOD real de 4 variables cargado.")
                except Exception:
                    pass
            if not loaded and os.path.exists(mock_path):
                ecod = joblib.load(mock_path)
                print("ECOD mock de 4 variables cargado.")

        print("Modelos analíticos listos en ml_service.")
    except Exception as e:
        print(f"Advertencia al cargar los modelos analíticos: {e}")

def get_feature_vector(alert):
    np.random.seed(hash(alert.id_alerta) % 1000)
    
    # 1. FOB Declarado
    fob = float(alert.valor_fob_declarado)
    
    # 2. Peso Neto (derived from FOB with noise or use DB value if exists)
    if alert.peso_neto is not None and float(alert.peso_neto) > 0:
        peso = float(alert.peso_neto)
    else:
        peso = fob / (2.0 + np.random.rand() * 1.5)
    
    # 3. Temp Contenedor
    if alert.temperatura is not None and float(alert.temperatura) > 0:
        temp = float(alert.temperatura)
    else:
        if alert.producto == 'Palta':
            temp = 5.0 + np.random.rand() * 4.0
        elif alert.producto == 'Uva':
            temp = 1.0 + np.random.rand() * 3.0
        elif alert.producto == 'Arándano':
            temp = 0.5 + np.random.rand() * 2.0
        else:
            temp = 12.0 + np.random.rand() * 5.0 # Mango
            
    # 4. Retraso Logístico
    if alert.retraso_dias is not None:
        retraso = int(alert.retraso_dias)
    else:
        original_score = float(alert.score_anomalia)
        if original_score > 0.8:
            temp += 4.5
            retraso = 5 + np.random.randint(1, 10)
        else:
            retraso = np.random.randint(0, 4)
        
    return np.array([[fob, peso, temp, retraso]])
