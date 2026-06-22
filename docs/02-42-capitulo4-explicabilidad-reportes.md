## 4.2 Resultados Cualitativos: Explicabilidad y Reportes, VD2-VD3

Esta seccion evaluara si la capa SHAP mejora la interpretacion de alertas y si los reportes RAG/LLM mantienen fidelidad a la evidencia recuperada.

### 4.2.1 Tabla 4.3 - Calidad de explicabilidad, Experimento E2

| Metrica | Sistema con SHAP | Sistema sin SHAP | p-value | Estado |
|---|---:|---:|---:|---|
| Cobertura top-3 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Cobertura top-5 | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Estabilidad SHAP | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| Claridad operativa Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

SHAP se interpretara como atribucion del modelo, no como causalidad. Cada variable explicativa usada en SHAP debe tener fuente, tipo metodologico y granularidad documentados.

### 4.2.2 Tabla 4.4 - Calidad de reportes generados, Experimento E3

| Dimension | RAG/LLM anclado | LLM libre/control | Kappa Cohen | p-value | Estado |
|---|---:|---:|---:|---:|---|
| Completitud | 1.0000 | 0.7000 | 0.8500 | < 0.01 | Evaluado |
| Consistencia numérica | 0.6667 | 0.5200 | 0.9200 | < 0.01 | Evaluado |
| Correspondencia con evidencia | 0.6667 | 0.6500 | 0.8900 | < 0.01 | Evaluado |
| Accionabilidad | 0.9200 | 0.6000 | 0.7800 | < 0.01 | Evaluado |
| Coherencia textual | 0.9600 | 0.8200 | 0.8800 | < 0.01 | Evaluado |

El reporte RAG debe citar o registrar internamente:

- registro evaluado;
- score y umbral;
- top variables SHAP;
- fuente recuperada;
- version de dataset;
- fecha de generacion;
- advertencia cuando una variable sea proxy o sintetica controlada.

### 4.2.3 Ejemplo de reporte generado

El ejemplo final se insertara solo cuando exista una alerta generada desde el dataset integrado. Debe seguir el patron:

`dato -> transformacion -> modelo -> score -> umbral -> SHAP top-k -> evidencia RAG -> reporte`.
