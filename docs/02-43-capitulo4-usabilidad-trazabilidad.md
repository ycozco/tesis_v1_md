## 4.3 Resultados del Estudio de Usabilidad y Trazabilidad, VD4-VD5

Esta seccion medira si el sistema integrado reduce el tiempo de interpretacion y mejora la trazabilidad documental frente a componentes aislados.

### 4.3.1 Tabla 4.5 - Tiempo-a-decision y comprension, Experimento E4

| Metrica | Sistema integrado | Componentes aislados | Diferencia relativa | p-value | Tamano de efecto | Estado |
|---|---:|---:|---:|---:|---:|---|
| Tiempo-a-decision, segundos | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Comprension Likert 1-5 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| Decision correcta | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| SUS Score 0-100 | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

El tamano muestral y el perfil de participantes se reportaran como estudio piloto especializado si no alcanzan potencia estadistica suficiente para generalizacion amplia.

### 4.3.2 Tabla 4.6 - Trazabilidad documental, VD5

| Configuracion | Alertas con trazabilidad completa | Campos faltantes frecuentes | Estado |
|---|---:|---|---|
| Sistema integrado completo, E5d | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin SHAP, E5b | _pendiente_ | _pendiente_ | Por ejecutar |
| Ablation sin RAG, E5c | _pendiente_ | _pendiente_ | Por ejecutar |
| Componentes aislados/control | _pendiente_ | _pendiente_ | Por ejecutar |

La trazabilidad completa exige, como minimo: `id_alerta`, `producto`, `hs`, `fecha`, `fuentes_usadas`, `score`, `umbral`, `top_shap`, `evidencia_rag`, `version_dataset` y `archivo_origen`.

### 4.3.3 Tabla 4.7 - Ablation study, Experimento E5

| Configuracion | Capa 1 prediccion | Capa 2 anomalias | Capa 3 SHAP | Capa 4 RAG | VD1 | VD3 | VD5 | Estado |
|---|---|---|---|---|---:|---:|---:|---|
| E5a solo deteccion | No | Si | No | No | _pendiente_ | N/A | _pendiente_ | Por ejecutar |
| E5b sin SHAP | Si | Si | No | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5c sin RAG | Si | Si | Si | No | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |
| E5d pipeline completo | Si | Si | Si | Si | _pendiente_ | _pendiente_ | _pendiente_ | Por ejecutar |

Las comparaciones E5 no deben mezclar resultados de dataset sintetico con resultados del dataset integrado sin una etiqueta explicita de version.
