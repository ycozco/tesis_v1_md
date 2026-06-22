## 4.4 Usabilidad y Trazabilidad — VD4, VD5

> **Estado:** Estructura de telemetría implementada y funcional. Datos semilla disponibles para validar el flujo de captura. Los resultados definitivos requieren el experimento con participantes reales (≥10 por condición).

### 4.4.1 Diseño del Estudio de Usabilidad

El experimento mide el impacto de la explicabilidad de IA en auditores aduaneros bajo dos condiciones controladas:

- **Condición A (INTEGRADO):** Acceso completo a las 4 capas de IA — FOB esperado, score ensemble, atribuciones SHAP y narrativa RAG con citas normativas.
- **Condición B (AISLADO):** Solo acceso a datos de la DAM, FOB esperado y score ensemble. Sin SHAP ni narrativa RAG.

**Hipótesis de investigación:**

| Hipótesis | Enunciado |
|---|---|
| H1 | Los auditores con acceso a explicaciones SHAP + RAG (Condición A) toman decisiones más rápidas que en Condición B |
| H2 | Los auditores en Condición A reportan mayor comprensión percibida (Likert) que en Condición B |
| H3 | El sistema integrado produce mayor porcentaje de trazabilidad completa que los componentes aislados |

### 4.4.2 Telemetría Implementada

El endpoint `POST /api/alerts/<id>/adjudicate` captura automáticamente:

```python
DecisionAuditoria(
    id_alerta=id_alerta,
    id_auditor=current_user_id,
    condicion_experimental=user.condicion_experimental,  # "INTEGRADO" | "AISLADO"
    decision_resultado=decision,                          # 0=Falsa alarma, 1=Confirmada, 2=Inspección
    likert_comprension=likert,                            # 1-5
    time_to_decision_ms=time_to_decision,                 # ms desde carga de alerta
    timestamp_decision=datetime.utcnow()
)
```

### 4.4.3 Tabla 4.7 — Datos de Telemetría (Datos Semilla — Validación de Flujo)

| Alerta | Auditor | Condición | Decisión | Comprensión (Likert) | T. Decisión |
|---|---|---|---|---|---|
| AL-2026-0009 | auditor1 | INTEGRADO | Anomalía Confirmada (1) | 5/5 | 25.6 s |
| AL-2026-0006 | auditor1 | AISLADO | Falsa Alarma (0) | 3/5 | 49.2 s |
| AL-2026-0005 | auditor2 | INTEGRADO | Requiere Inspección (2) | 4/5 | 31.2 s |
| AL-2026-0004 | auditor2 | AISLADO | Falsa Alarma (0) | 2/5 | 65.4 s |

**Agregados preliminares (N=2 por condición — solo validación de flujo):**

| Métrica | Condición A (INTEGRADO) | Condición B (AISLADO) | Diferencia observada |
|---|---|---|---|
| T. decisión promedio | 28.4 s | 57.3 s | −50.4% |
| Comprensión promedio (Likert) | 4.5 / 5 | 2.5 / 5 | +2.0 puntos |

> **Advertencia:** Con N=2 por condición no es posible obtener significancia estadística. Estos valores validan únicamente que el sistema de captura de telemetría funciona correctamente. El experimento formal requerirá N≥10 por condición y análisis con prueba de Mann-Whitney U.

### 4.4.4 Trazabilidad del Sistema — VD5

**Tabla 4.8 — Porcentaje de Campos de Trazabilidad Completos**

| Campo de Trazabilidad | Cobertura (datos semilla) |
|---|---|
| ID de alerta | 100% |
| Score de anomalía | 100% |
| FOB esperado vs declarado | 100% |
| Valores SHAP por variable | 100% |
| Condición experimental del auditor | 100% |
| Timestamp de decisión | 100% |
| Decisión registrada | 100% |
| Comprensión Likert | 100% |
| **Trazabilidad completa (VD5)** | **100%** |

El umbral de calidad de trazabilidad definido en el protocolo experimental es ≥ 90%. El prototipo supera este umbral en los datos semilla de validación.
