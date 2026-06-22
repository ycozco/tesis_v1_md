## 4.3 Explicabilidad Local y Reportes Automáticos — VD2, VD3

> **Estado:** parcial verificable. El prototipo muestra explicaciones y reportes para datos semilla; la validación factual completa y la comparación formal contra plantilla determinística quedan pendientes hasta ejecutar el protocolo definitivo.

### 4.3.1 Explicabilidad local con SHAP — VD2

El sistema utiliza explicabilidad local para que el auditor observe qué variables empujan el riesgo estimado en una alerta. En la propuesta metodológica, este bloque se vincula con `src/module3_shap.py`; en el prototipo funcional se evidencia en la vista de detalle de alerta de `sistema-web-agro/frontend/src/pages/Detail.jsx` y `AuditDetail.jsx`.

**Tabla 4.4 — Atribuciones SHAP promedio en datos semilla**

| Variable | SHAP promedio | Dirección | Interpretación operacional |
|---|---:|---|---|
| `valor_fob_declarado` | +0.4231 | Aumenta riesgo | Desviación del valor FOB frente a referencia esperada |
| `temperatura_contenedor_c` | +0.2184 | Aumenta riesgo | Posible deterioro o condición logística atípica |
| `dias_retraso_logistico` | +0.1562 | Aumenta riesgo | Retraso asociado a mayor incertidumbre operativa |
| `peso_neto_kg` | -0.0891 | Reduce riesgo | Consistencia entre volumen y valor declarado |

Estos valores se interpretan como contribuciones del modelo, no como causalidad. La validación definitiva debe guardar top-k de variables por alerta, estabilidad de la explicación, tiempo de cálculo y hash del modelo usado.

### 4.3.2 Reportes RAG — VD3

El prototipo contempla generación de reportes técnicos con recuperación documental y respaldo de citas. La tesis propone que cada reporte sea validado con reglas determinísticas antes de incorporarse como evidencia.

**Tabla 4.5 — Rúbrica requerida para reportes automáticos**

| Criterio | Verificación requerida | Estado |
|---|---|---|
| Completitud | Score, FOB esperado, variables SHAP y recomendación presentes | Parcial |
| Coherencia | El reporte no contradice los datos de la alerta | Pendiente de validador formal |
| Fidelidad factual | Cada cifra existe en evidencia estructurada | Pendiente |
| Consistencia numérica | Diferencia numérica dentro del umbral definido | Pendiente |
| Trazabilidad documental | Citas o documentos recuperados guardados con ID | Parcial |

### 4.3.3 Tabla 4.6 — Documentos recuperados en muestras semilla

| Tipo de alerta | Documento 1 | Documento 2 | Documento 3 | Estado |
|---|---|---|---|---|
| Palta, FOB bajo, temperatura alta | FDA-1 | SENASA-2 | LEY_IA-3 | Preliminar |
| Uva, retraso logístico | SENASA-2 | FDA-1 | LEY_IA-3 | Preliminar |
| Arándano, score alto | FDA-1 | LEY_IA-3 | SENASA-2 | Preliminar |

### 4.3.4 Evidencia faltante para cierre de VD2 y VD3

- Guardar cada explicación SHAP con `alert_id`, `model_version_id`, fecha, commit y hash.
- Validar que los valores SHAP correspondan al modelo entrenado para esa ejecución.
- Guardar prompt, modelo, parámetros y documentos recuperados.
- Registrar reportes rechazados por el validador factual.
- Comparar reporte RAG contra plantilla determinística.
- Marcar afirmaciones no sustentadas y excluirlas del borrador final.

Hasta completar esos puntos, VD2 y VD3 quedan como avances funcionales, no como resultados finales.
