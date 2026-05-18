# CAPÍTULO III: PROPUESTA METODOLÓGICA

## 3.1 Arquitectura del Sistema Integrado

La arquitectura propuesta se divide en cuatro módulos secuenciales, diseñados para maximizar trazabilidad, interpretabilidad y utilidad operativa en procesos agroexportadores:

- **Módulo de Predicción Tabular (Capa 1):** Utiliza algoritmos GBDT como núcleo predictivo, priorizando XGBoost [@chen2016xgboost] y LightGBM [@ke2017lightgbm] por su robustez ante datos tabulares con variables heterogéneas [@grinsztajn2022trees]. El módulo puede estimar valores esperados de precio, volumen, merma o riesgo operativo.
- **Módulo de Detección de Anomalías (Capa 2):** Emplea detectores como Isolation Forest [@liu2008isolationforest], LOF [@breunig2000lof] y ECOD [@li2022ecod], orquestados mediante PyOD [@zhao2019pyod], para identificar comportamientos atípicos en variables agroexportadoras. Se selecciona ECOD sobre Deep SVDD [@ruff2018deepsvdd] —considerado en la revisión bibliográfica del Capítulo II— por tres razones: (a) ECOD no requiere ajuste de hiperparámetros, lo cual elimina el riesgo de sobreajuste en la calibración; (b) su fundamento basado en funciones de distribución empírica acumulada es interpretable estadísticamente para auditores, mientras que Deep SVDD opera sobre representaciones latentes opacas; y (c) su complejidad computacional es lineal, apropiada para el tamaño medio del dataset experimental (2,000–5,000 registros). Deep SVDD se mantiene como referencia conceptual del Capítulo II por su valor histórico, pero no entra al ensemble final.
- **Módulo de Explicabilidad (Capa 3):** SHAP [@lundberg2017shap] genera explicaciones locales por alerta, identificando qué variables —precio, volumen, clima, destino, cumplimiento o merma— contribuyen al score del sistema.
- **Módulo de Reportes LLM+RAG (Capa 4):** Un LLM restringido a evidencias estructuradas mediante RAG [@schneider2025rag] redacta reportes operativos trazables. El LLM no decide si existe una anomalía; solo traduce scores, umbrales y explicaciones SHAP a lenguaje comprensible.

```
┌─────────────────────────────────────────────────────────┐
│ CAPA 4: Reporte Automatizado (LLM + RAG)               │
│ Entrada: anomalías + vectores SHAP                      │
│ Salida: reporte auditado en lenguaje natural (MD/PDF)  │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ CAPA 3: Explicabilidad (SHAP / TreeSHAP)               │
│ Entrada: predicciones + datos originales               │
│ Salida: vectores Shapley + SHAP Stability Index        │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ CAPA 2: Detección de Anomalías (Ensemble)              │
│ Métodos: IF + LOF + ECOD (PyOD)                        │
│ Salida: score anomalía + método que detectó            │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ CAPA 1: Predicción tabular agroexportadora             │
│ Modelo: XGBoost / LightGBM                             │
│ Entrada: precio, volumen, clima, calidad, logística    │
│ Salida: valor esperado + riesgo operativo              │
└─────────────────────────────────────────────────────────┘
```

## 3.2 Fuentes de Datos, Dataset Sintético y Benchmarks

Para validar la robustez del sistema sin depender obligatoriamente de datos privados, se emplearán tres niveles de información:

1. **Fuentes públicas oficiales del dominio agroexportador**: MIDAGRI para agroexportaciones, precios y productos; SENAMHI para variables climáticas; SENASA para requisitos fitosanitarios; SUNAT para exportaciones; INEI para indicadores económicos; FAOSTAT y UN Comtrade para validación internacional.
2. **Dataset sintético agroexportador documentado**: conjunto de registros simulados con variables como fecha, producto, zona, volumen, precio, temperatura, precipitación, humedad, destino, cumplimiento fitosanitario, días logísticos, merma, etiqueta de anomalía y tipo de anomalía. Este dataset se documentará con criterios de Datasheets for Datasets [@gebru2021datasheets].
3. **Benchmark metodológico complementario**: BAF Benchmark [@jesus2022baf] podrá utilizarse solo para contrastar comportamiento de modelos en datos tabulares desbalanceados con drift temporal, sin presentarlo como validación directa del dominio agroexportador.

## 3.3 Configuración Experimental y Métricas

### 3.3.1 Métricas por variable dependiente

- **Métricas de predicción y detección (VD1)**: PR-AUC (métrica principal para datasets desbalanceados), ROC-AUC, F1-Score, Precision y Recall con umbral óptimo determinado por el punto de máxima F1 sobre el conjunto de validación.
- **Métricas de explicabilidad (VD2)**: cobertura top-k SHAP (porcentaje de alertas en las que las k=5 variables principales explican ≥80% de la magnitud absoluta del score), consistencia cualitativa de variables explicativas y claridad operativa (Likert 1–5 evaluada por revisores con perfil agroexportador).
- **Métricas de calidad de reportes (VD3)**: rúbrica operativa de cinco dimensiones (completitud, consistencia numérica, accionabilidad, coherencia textual, correspondencia con evidencias) evaluada por dos revisores independientes con cálculo de Kappa de Cohen para confiabilidad inter-evaluador. Adicionalmente ROUGE-1/ROUGE-L cuando exista referencia humana.
- **Métricas de comprensión y decisión (VD4)**: tiempo-a-decisión (segundos, medido automáticamente desde la apertura de la alerta hasta el envío del veredicto del evaluador), comprensión de alerta (Likert 1–5) y decisión final correcta (sí/no respecto a la etiqueta del dataset).
- **Métricas de trazabilidad (VD5)**: porcentaje de alertas con todos los campos completos (dato de origen, versión de dataset, modelo, score, umbral, explicación SHAP, fuente recuperada por RAG y reporte generado).

### 3.3.2 División del dataset y semilla

Para evitar fuga de información temporal en variables agroexportadoras con estacionalidad, se aplica una **división cronológica** y no aleatoria:
- **Train**: primeros 70% de registros ordenados por fecha.
- **Validation**: 10% siguiente, para selección de hiperparámetros.
- **Test**: 20% final, evaluado solo al cierre del entrenamiento.

Todas las ejecuciones experimentales fijan `np.random.seed(42)` y `random.seed(42)`. Cada experimento se repite con cinco semillas adicionales (43, 44, 45, 46, 47) para reportar media ± desviación estándar de cada métrica.

### 3.3.3 Diseño experimental: condiciones y experimentos E1–E5

La evaluación se organiza en cinco experimentos cuya condición experimental aísla un componente arquitectónico distinto:

| Exp. | Nombre | Condición experimental | Condición de control | Variable observada | Hipótesis |
|---|---|---|---|---|---|
| E1 | Rendimiento de detección | Ensemble IF + LOF + ECOD | Isolation Forest individual | VD1: PR-AUC, F1 | H1a |
| E2 | Aporte de SHAP | Sistema con vectores SHAP | Sistema sin SHAP (solo scores) | VD2: cobertura top-k, Likert | H1b |
| E3 | Aporte de RAG | LLM + RAG (anclado en SHAP) | LLM libre (sin RAG) | VD3: rúbrica 5D, ROUGE-L | H1c |
| E4 | Sistema integrado vs. aislado | Pipeline completo de 4 capas | Salidas técnicas aisladas por módulo | VD4: tiempo, Likert; VD5: trazabilidad | H1, H1d |
| E5 | Ablation study | Configuraciones parciales (E5a, E5b, E5c, E5d) | — | VD1 + VD5 por configuración | Contribución por capa |

Variantes del ablation study (E5):
- **E5a**: Solo Capa 2 (sin predicción, sin SHAP, sin RAG) — baseline mínimo.
- **E5b**: Capas 1 + 2 + 4 (sin SHAP) — evalúa el aporte de SHAP al pipeline.
- **E5c**: Capas 1 + 2 + 3 + LLM libre (sin RAG) — evalúa el aporte del anclaje RAG.
- **E5d**: Pipeline completo de 4 capas — referencia experimental.

### 3.3.4 Pruebas estadísticas y mapa hipótesis → experimento

Cada sub-hipótesis se contrasta con una prueba estadística específica, seleccionada según el tipo de variable y el diseño:

| Sub-hipótesis | Comparación | Variable | Prueba estadística | α | Tamaño de efecto |
|---|---|---|---|---|---|
| H1a | Ensemble vs. detector único | PR-AUC sobre 6 semillas | Wilcoxon signed-rank (no paramétrica, apareada) | 0.05 | Hedges' g |
| H1b | SHAP vs. sin SHAP | Likert comprensión (1–5) | Mann-Whitney U (escala ordinal, muestras independientes) | 0.05 | r de rangos |
| H1c | RAG vs. sin RAG | Rúbrica de reportes (1–5) | t de Student apareado o Wilcoxon según Shapiro-Wilk | 0.05 | Cohen's d |
| H1d | Sistema integrado vs. aislado | Tiempo-a-decisión (s) | t de Student apareado (within-subjects) | 0.05 | Cohen's dz |

Para todas las pruebas se verifica previamente el supuesto de normalidad con Shapiro-Wilk; ante violación, se aplica la prueba no paramétrica equivalente. Se reporta intervalo de confianza al 95% para cada métrica y se calcula el tamaño de efecto como medida complementaria a la significancia estadística.

### 3.3.5 Estudio de usabilidad: tamaño y selección de muestra

El estudio de usabilidad para VD4 adopta un **diseño within-subjects con N ≥ 15 participantes**, contrabalanceado en orden de presentación (mitad evalúa primero el sistema integrado, mitad evalúa primero el aislado). Con este tamaño se reportan resultados como exploratorios, con cálculo de tamaño de efecto Cohen's dz y intervalo de confianza al 95%, sin afirmar significancia estadística con potencia plena. Para detectar un efecto medio (dz = 0.5) con potencia 0.80 y α = 0.05 se requieren N = 27 participantes; este tamaño se considera meta deseable y, en caso de no alcanzarse, se reporta el limitante en §5.2 (Limitaciones).

**Criterios de inclusión de participantes**:
- Estudiantes avanzados de Ingeniería de Sistemas, Industrial o Agronomía (≥ séptimo semestre), o
- Profesionales con ≥ 1 año de experiencia en supervisión operativa, control de calidad o auditoría interna.

**Criterios de exclusión**:
- Participación previa en el diseño del sistema o de cualquiera de sus capas.
- Conflicto de interés directo con empresas agroexportadoras evaluadas.

El protocolo detallado, formulario de consentimiento informado y cuestionario post-tarea figuran en el Anexo A.

### 3.3.6 Tuning de hiperparámetros y reproducibilidad

La selección de hiperparámetros se realiza con **Optuna** (TPE sampler, 50 trials por modelo), optimizando PR-AUC sobre el validation set. Los rangos de búsqueda se documentan en el Anexo B (Model Cards). El código fuente, requirements.txt con versiones exactas, semillas y notebooks de reproducción se publican en repositorio GitHub público con licencia MIT al cierre del Hito 3.

### 3.3.7 Comparación con baselines

Para cada experimento, los resultados del sistema propuesto se comparan con baselines documentados:

| # | Baseline | Justificación |
|---|---|---|
| B1 | Isolation Forest individual | Detector más simple y ampliamente adoptado |
| B2 | Ensemble IF + LOF (sin ECOD) | Aislar el aporte de ECOD al ensemble |
| B3 | XGBoost supervisado con etiqueta de anomalía | Upper bound supervisado |
| B4 | LLM sin RAG y sin SHAP | Línea base de reporte automático |

Los baselines se ejecutan sobre el mismo dataset, misma división y mismas semillas para garantizar comparación justa.

---

