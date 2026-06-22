## 4.4 Usabilidad y Trazabilidad — VD4, VD5

> **Estado:** diseño experimental y validación funcional parcial. El prototipo registra decisiones y tiempos con datos semilla, pero el experimento con usuarios reales permanece pendiente.

### 4.4.1 Diseño del estudio de usabilidad — VD4

El estudio compara dos condiciones:

- **Condición A integrada:** el auditor observa datos de la operación, predicción, score de anomalía, explicación SHAP y reporte RAG.
- **Condición B aislada:** el auditor observa datos de la operación, predicción y score, sin explicación SHAP ni reporte RAG.

Las variables dependientes son tiempo de análisis, decisión registrada, comprensión percibida, utilidad percibida y exactitud de la decisión frente a un criterio de referencia.

| Requisito | Estado |
|---|---|
| Cantidad y perfil de participantes | Pendiente |
| Consentimiento informado y anonimización | Pendiente |
| Tareas equivalentes por condición | Pendiente |
| Contrabalanceo del orden | Pendiente |
| Prueba estadística definida | Pendiente |
| Registro de decisiones y tiempos | Implementado en prototipo |

### 4.4.2 Telemetría semilla

El prototipo registra decisiones de auditoría mediante el flujo de adjudicación de alertas. Esta evidencia valida captura de datos, no desempeño humano definitivo.

**Tabla 4.7 — Telemetría semilla de validación de flujo**

| Alerta | Auditor | Condición | Decisión | Comprensión | Tiempo |
|---|---|---|---|---:|---:|
| AL-2026-0009 | auditor1 | Integrado | Anomalía confirmada | 5/5 | 25.6 s |
| AL-2026-0006 | auditor1 | Aislado | Falsa alarma | 3/5 | 49.2 s |
| AL-2026-0005 | auditor2 | Integrado | Requiere inspección | 4/5 | 31.2 s |
| AL-2026-0004 | auditor2 | Aislado | Falsa alarma | 2/5 | 65.4 s |

Con N=2 por condición no corresponde afirmar significancia estadística. Los datos solo indican que la plataforma puede capturar tiempos, decisiones y escala de comprensión.

### 4.4.3 Trazabilidad — VD5

La trazabilidad se evalúa verificando que cada alerta pueda reconstruirse desde entrada, predicción, score, explicación, reporte, decisión humana y registro temporal.

**Tabla 4.8 — Campos de trazabilidad esperados**

| Campo | Evidencia | Estado |
|---|---|---|
| ID de alerta | Registro de alerta | Disponible en prototipo |
| Score de anomalía | Resultado del ensemble | Disponible en prototipo |
| FOB esperado vs declarado | Salida predictiva | Disponible en prototipo |
| Valores SHAP | Detalle de explicación | Parcial |
| Reporte generado | Reporte RAG o plantilla | Parcial |
| Documentos recuperados | IDs/citas del RAG | Parcial |
| Decisión humana | Registro de adjudicación | Disponible en prototipo |
| Timestamp | Registro de decisión | Disponible en prototipo |
| Hash de artefactos | Control de auditoría | Pendiente para cierre final |

### 4.4.4 Evidencia faltante

- Ejecutar el experimento con participantes reales.
- Registrar consentimiento, perfil y anonimización.
- Guardar datos crudos de usabilidad fuera de rutas de referencia pública si contienen información sensible.
- Ejecutar prueba estadística definida.
- Generar reporte de trazabilidad con hash de artefactos y commit.

Hasta completar el estudio, VD4 se mantiene pendiente y VD5 queda parcialmente respaldada por el prototipo.
