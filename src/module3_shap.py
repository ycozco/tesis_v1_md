#!/usr/bin/env python3
"""
src/module3_shap.py
===================
Implementa la Capa 3 (Explicabilidad Local mediante TreeSHAP):
1. Usa shap.TreeExplainer acoplado a un modelo de clasificación GBDT (como XGBoost).
2. Genera los valores de contribución local (valores Shapley) para una instancia de alerta.
3. Extrae las top-5 características de mayor contribución (ordenadas por magnitud absoluta).

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import sys
import logging
import numpy as np
import pandas as pd
import shap

# Configuración de codificación de salida para Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


class TreeSHAPExplainer:
    def __init__(self, model, feature_names: list[str]):
        """Inicializa el explicador TreeSHAP con el modelo GBDT entrenado."""
        self.model = model
        self.feature_names = feature_names
        # Creamos el explainer de SHAP
        self.explainer = shap.TreeExplainer(self.model)
        
    def explain_alert(self, instance_features: pd.DataFrame) -> list[dict]:
        """
        Calcula las contribuciones de SHAP para una única fila/instancia y
        devuelve una lista ordenada de las top-5 características influyentes.
        """
        # Asegurar de que la instancia sea un DataFrame de 1 fila y tenga las columnas correctas
        if isinstance(instance_features, pd.Series):
            instance_features = instance_features.to_frame().T
            
        instance_features = instance_features[self.feature_names]
        
        # Calcular valores SHAP
        shap_values = self.explainer.shap_values(instance_features)
        
        # En clasificación binaria de XGBoost, shap_values puede ser una matriz (N, features) o lista
        if isinstance(shap_values, list):
            # Si es multiclase/binario con 2 salidas, tomamos la clase positiva (índice 1)
            val = shap_values[1][0]
        else:
            # Si es binario directo (XGBoost estándar)
            if len(shap_values.shape) > 1:
                val = shap_values[0]
            else:
                val = shap_values
                
        # Emparejar con nombres de características
        contributions = []
        for name, value in zip(self.feature_names, val):
            contributions.append({
                "feature": name,
                "shap_value": float(value),
                "abs_value": float(abs(value))
            })
            
        # Ordenar por valor absoluto descendente y tomar top-5
        contributions = sorted(contributions, key=lambda x: x["abs_value"], reverse=True)
        return contributions[:5]


def main():
    log.info("==================================================")
    log.info("📊 MÓDULO DE EXPLICABILIDAD TREESHAP CARGADO")
    log.info("==================================================")


if __name__ == "__main__":
    main()
