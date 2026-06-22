import pandas as pd
import numpy as np
from src.train_models import BaselineMeanHistorico

def test_baseline_mean_historico():
    """
    Verifica el comportamiento del baseline histórico:
    1. Que calcule el promedio por grupo (mes).
    2. Que prediga correctamente según el grupo.
    3. Que maneje valores faltantes/nuevos grupos usando el promedio global.
    """
    # 1. Crear datos ficticios
    df_train = pd.DataFrame({
        "mes": [1, 1, 2, 2, 3],
        "precio_kg_usd": [1.5, 2.5, 3.0, 4.0, 5.0] # TARGET
    })
    
    # Parchear temporalmente la constante TARGET en el módulo si es necesario, 
    # pero train_models.py usa TARGET de constants o global.
    # Vamos a verificar cómo funciona BaselineMeanHistorico:
    # Utiliza la columna TARGET del DataFrame.
    # En train_models.py, TARGET se importa de constants o se define globalmente.
    # Vamos a parchear TARGET en el import o simplemente pasarlo.
    # En train_models.py:
    # 163:         if "mes" in df_train.columns and TARGET in df_train.columns:
    # Vamos a importar TARGET para saber cuál es.
    import src.train_models as tm
    original_target = getattr(tm, "TARGET", "precio_kg_usd")
    
    # Asegurar que el DataFrame tiene la columna TARGET adecuada
    df_train = pd.DataFrame({
        "mes": [1, 1, 2, 2, 3],
        original_target: [1.5, 2.5, 3.0, 4.0, 5.0]
    })
    
    baseline = BaselineMeanHistorico()
    baseline.fit(df_train)
    
    # Medias calculadas: mes 1: 2.0, mes 2: 3.5, mes 3: 5.0
    assert baseline.medias[1] == 2.0
    assert baseline.medias[2] == 3.5
    assert baseline.medias[3] == 5.0
    
    # 2. Predecir
    df_test = pd.DataFrame({
        "mes": [1, 2, 4] # Mes 4 no está en train
    })
    preds = baseline.predict(df_test)
    
    assert preds[0] == 2.0
    assert preds[1] == 3.5
    # El mes 4 debe usar el promedio global de las medias de entrenamiento: (2.0 + 3.5 + 5.0) / 3 = 3.5
    assert preds[2] == 3.5
