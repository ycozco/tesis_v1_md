# Metodología del Pipeline de Supervisión Operativa con IA

Este documento describe el funcionamiento metodológico del pipeline integrado de predicción y detección de anomalías para la tesis.

## Capa 1: Predicción Tabular Global (GBDT)
* El sistema entrena modelos de regresión global basados en árboles de decisión (GBDT), específicamente XGBoost y LightGBM.
* Un solo modelo global aprende de todos los productos y mercados, incorporando variables categóricas mediante codificación One-Hot (OHE).
* Las predicciones se generan para la semana $t+1$ utilizando únicamente información disponible al cierre de la semana $t$ (shift temporal de 1 semana) para evitar cualquier fuga de información (*data leakage*).
* Los hiperparámetros se optimizan mediante Optuna a lo largo de 50 ensayos utilizando validación temporal expansiva (TimeSeriesSplit con 5 splits).
* Se calculan los residuos de precio y volumen. Estos residuos se normalizan en puntuaciones robust-z mediante una ventana móvil de 13 semanas por producto y mercado para controlar la variación estacional y estática.

## Capa 2: Detección Multivariable de Anomalías (Ensemble PyOD)
* Se implementa un ensemble no supervisado compuesto por tres detectores: Isolation Forest (IF), Local Outlier Factor (LOF) y Empirical Cumulative Distribution Outlier Detection (ECOD).
* Las puntuaciones brutas de cada detector se transforman a percentiles unificados $[0, 1]$ basados exclusivamente en las puntuaciones obtenidas en el conjunto de entrenamiento (Desarrollo).
* La puntuación del ensemble se calcula como el promedio simple de los percentiles unificados de los tres detectores.
* Se activa una alerta de anomalía operativa cuando la puntuación del ensemble es $\ge 0.95$ o cuando al menos dos de los detectores marcan la fila como anomalía (percentil individual $\ge 0.95$, regla de votos $\ge 2$).

## Capa 3: Explicabilidad Local y Global (TreeSHAP)
* Las explicaciones locales se calculan utilizando TreeSHAP sobre los modelos globales de regresión.
* SHAP (SHapley Additive exPlanations) distribuye de manera justa la diferencia entre la predicción y el valor esperado entre las variables de entrada del modelo.
* Para cada alerta de anomalía, se extraen las 5 variables que ejercen mayor influencia positiva (empujan la predicción al alza) y las 5 variables de mayor influencia negativa (reducen la predicción).
* Es fundamental indicar que los valores SHAP representan **atribución matemática del modelo** y **no relación de causalidad física**.
