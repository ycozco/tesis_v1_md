# HOJA DE RUTA DETALLADA (ROADMAP)
## Sistema Integrado de Supervisión Operativa con IA Explicable — Tesis UNSA
**Última actualización:** 2026-06-07  
**Estado de la tesis documental:** Capítulo I (Planteamiento), Capítulo II (Marco Teórico) e Hito 1 (Variables Operacionalizadas) completados.  

---

## 📌 Resumen del Estado Actual y Próximos Pasos

La tesis documental ya tiene definidas las bases conceptuales: las **hipótesis (H1, H1a-H1d)** y las **variables dependientes operacionalizadas (VD1-VD5)**. Sin embargo, para poder avanzar a la redacción de los Capítulos IV (Resultados) y V (Discusión), es obligatorio ejecutar y evaluar la parte técnica de desarrollo de software.

La siguiente secuencia lógica muestra cómo se conectan la fase actual, el desarrollo de software y la finalización académica:

```
[Fase 1: Preparación y Datos] ➔ [Fase 2: Modelado Backend] ➔ [Fase 3: Explicabilidad y RAG]
               │                                                    │
               ▼                                                    ▼
   Validación de variables y                              Construcción de Módulos
    preprocesamiento de datos                                  de Software
               │                                                    │
               └───────────────────────┬────────────────────────────┘
                                       ▼
                       [Fase 4: Integración y Dashboard]
                                       │
                                       ▼
                     [Fase 5: Experimentos y Estadística]
                        (Mapeo de resultados a hipótesis)
                                       │
                                       ▼
                       [Fase 6: Cierre Académico / Redacción]
                        (Capítulos IV-V + compilación final)
```

---

## 📅 Hoja de Ruta Fase por Fase

### Fase 1: Consolidación y Verificación de Fuentes (Estado: En curso / Cierre Inmediato)
*   **Objetivo:** Asegurar que los datos de entrada reflejen fielmente el dominio agroexportador peruano antes de entrenar modelos.
*   **Entregable técnico:** 
    *   Dataset crudo generado: [dataset_agro_sintetico_v1.csv](file:///d:/tesis_yoset/data/dataset_agro_sintetico_v1.csv).
    *   Preprocesamiento y balanceo: Ejecución de [preprocess_data.py](file:///d:/tesis_yoset/limpieza_de_datos_y_normalizacion/preprocess_data.py).
*   **Qué hacer ahora:**
    1.  Validar distribuciones: Ejecutar un notebook rápido para comparar las medias, desviaciones e IQR del dataset generado contra los rangos del manual de calidad del [datasheet](file:///d:/tesis_yoset/docs/05-a3-anexo-datasheet.md).
    2.  Verificar que no haya contaminación de datos (*data leakage*) temporal.
    3.  Asegurar que el 3% de nulos inyectados se impute correctamente mediante el `KNNImputer` y las variables continuas se normalicen con el `RobustScaler`.

---

### Fase 2: Modelado del Backend (Siguiente Paso de Software)
*   **Objetivo:** Entrenar los modelos de predicción y detección que alimentarán el sistema de supervisión.
*   **Tareas de programación:**
    1.  **Módulo 1: Predicción Tabular (`src/module1_prediction.py`)**
        *   Entrenar algoritmos de ensamble basados en árboles (XGBoost y LightGBM) sobre el conjunto balanceado con SMOTE ([dataset_processed_train_balanced.csv](file:///d:/tesis_yoset/data/dataset_processed_train_balanced.csv)).
        *   Implementar un script de optimización automatizada de hiperparámetros usando **Optuna** (50 trials) maximizando la métrica **PR-AUC**.
    2.  **Módulo 2: Detección de Anomalías (`src/module2_anomaly.py`)**
        *   Implementar un detector no supervisado tipo *Ensemble* (Isolation Forest + LOF + ECOD) usando la librería PyOD sobre el set crudo imputado ([dataset_processed_train_raw.csv](file:///d:/tesis_yoset/data/dataset_processed_train_raw.csv)).
        *   Calibrar el umbral de contaminación estadística basándose en el 8% histórico esperado.

---

### Fase 3: Explicabilidad y Reportes RAG (Gobernanza de la IA)
*   **Objetivo:** Implementar la capa de transparencia del sistema para explicar las alertas y fundamentarlas con normativas reales.
*   **Tareas de programación:**
    1.  **Módulo 3: Explicabilidad SHAP (`src/module3_shap.py`)**
        *   Configurar `TreeSHAP` (`shap.TreeExplainer`) sobre los modelos entrenados.
        *   Construir una función que extraiga el vector SHAP y determine el **top-5 de variables** con mayor contribución para cada anomalía detectada.
    2.  **Módulo 4: Generación RAG (`src/module4_rag.py`)**
        *   Implementar un motor de búsqueda ligera (BM25) sobre las normativas locales (por ejemplo, el Reglamento D.S. N° 115-2025-PCM).
        *   Integrar un LLM (Claude o Llama 3) para redactar el reporte de auditoría.
        *   *Regla estricta anti-alucinaciones:* El LLM tiene prohibido diagnosticar la anomalía por su cuenta; se restringe a estructurar narrativamente los resultados numéricos deterministas de SHAP y citar la normativa recuperada.

---

### Fase 4: Integración del Pipeline y Visualización (Dashboard)
*   **Objetivo:** Unificar los módulos en un flujo de ejecución continuo y proporcionar una interfaz web para el supervisor humano.
*   **Tareas de programación:**
    1.  Crear el orquestador principal `src/pipeline.py` para procesar nuevos registros operativos de extremo a extremo.
    2.  Actualizar la UI en **[app.py](file:///d:/tesis_yoset/src/app.py)** para mostrar un panel web interactivo donde el supervisor vea:
        *   El historial de transacciones.
        *   Las alertas de anomalías del Ensemble.
        *   Los gráficos de barras SHAP locales.
        *   El reporte de auditoría generado por RAG.

---

### Fase 5: Experimentos Académicos y Pruebas Estadísticas
*   **Objetivo:** Evaluar cuantitativa y cualitativamente el sistema integrado para contrastar las hipótesis declaradas en el Capítulo I.
*   **Mapeo de experimentos a hipótesis:**

| Experimento | Hipótesis Evaluada | Variable de Respuesta (VD) | Prueba Estadística | Criterio de Aceptación |
| :--- | :--- | :--- | :--- | :--- |
| **E1 (Rendimiento)** | **H1a** (Ensemble > Individual) | PR-AUC en el test set | Prueba de rangos con signo de Wilcoxon | Ensemble supera significativamente a detectores individuales ($p < 0.05$). |
| **E2 (SHAP)** | **H1b** (Explicabilidad) | Cobertura top-k e índice Likert | U de Mann-Whitney | Cobertura $\ge 80\%$, Likert de claridad $\ge 4.0/5$. |
| **E3 (RAG)** | **H1c** (Calidad de Reportes) | ROUGE-L / Rúbrica 5D | Prueba $t$ apareada (o Wilcoxon) | Reporte unificado supera en coherencia al LLM sin restricciones ($p < 0.05$). |
| **E4 (Usabilidad)** | **H1d** (Reducción de Tiempo) | Tiempo-a-decisión de supervisores | Prueba $t$ de Student para muestras relacionadas | Reducción del tiempo de respuesta del supervisor en $\ge 20\%$. |
| **E5 (Ablación)** | **H1** (Hipótesis General) | % de trazabilidad y completitud | Análisis multivariado descriptivo | Sistema integrado mantiene $\ge 95\%$ de alertas documentadas sin alucinaciones numéricas. |

---

### Fase 6: Cierre Académico y Redacción Final
*   **Objetivo:** Traducir los resultados prácticos de los experimentos a la tesis escrita.
*   **Tareas de redacción:**
    1.  **Escribir Capítulo IV (Resultados):** Completar las tablas de rendimiento, exportar los gráficos de caja/dispersión de las pruebas de usabilidad y los diagramas de barras de ROUGE-L.
    2.  **Escribir Capítulo V (Discusión):** Contrastar los resultados propios con los antecedentes de la literatura (como *AuditCopilot* y el framework de *Park 2024*).
    3.  **Redactar Conclusiones y Recomendaciones:** Estructurar de acuerdo al cumplimiento de los objetivos específicos (OE1-OE6).
    4.  **Auditoría Bibliográfica:** Ejecutar scripts de limpieza en **[refs.bib](file:///d:/tesis_yoset/config/refs.bib)** para eliminar duplicados y asegurar la citación perfecta en APA 7.
    5.  **Compilación Final:** Ejecutar `compile_thesis.py` para exportar los entregables oficiales en Word y PDF.

---

## 📈 Plan de Trabajo Inmediato (Esta Semana)

1.  **Validación del preprocesado:** Verificar que la salida del script `preprocess_data.py` (los CSVs de `data/`) sea consistente.
2.  **Crear esqueleto del Módulo 1:** Escribir `src/module1_prediction.py` importando LightGBM y XGBoost y verificar que compila.
3.  **Crear esqueleto del Módulo 2:** Escribir `src/module2_anomaly.py` utilizando la librería PyOD para el Isolation Forest.
