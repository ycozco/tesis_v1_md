# INFORME DE PRUEBAS DE HUMO (LÍNEA BASE)
## Sistema Integrado de Inteligencia Artificial Explicable
### Tesis UNSA — Yoset Cozco Mauri (2026)

Este documento detalla la inspección inicial de las principales vistas y componentes del sistema para identificar simulaciones ("mocking") frente a datos reales persistidos.

---

## 1. Inspección de Componentes y Funciones

*   **Página de Autenticación (Login)**:
    *   *Estado*: Funcional con validaciones locales hardcodeadas (`admin/admin` y `auditor/auditor`). Falta protección real por JWT y roles en backend.
*   **Dashboard**:
    *   *Estado*: Funcional parcial. Carga gráficos y resúmenes semanales de anomalías, pero algunas métricas históricas muestran oscilaciones sintéticas simuladas en frontend.
*   **Listado de Alertas**:
    *   *Estado*: Funcional parcial. Lee alertas del backend, pero algunas se calculan dinámicamente al vuelo en lugar de ser persistidas determinísticamente.
*   **Detalle de Alerta**:
    *   *Estado*: Defectuoso/Simulado. Al ingresar al detalle de una alerta, se regeneran valores aleatorios (ej. temperaturas estimadas, mermas logísticas ficticias) y se calculan explicaciones SHAP al vuelo.
*   **RAG y Normativas**:
    *   *Estado*: Simulado. Contiene explicaciones legales generadas mediante plantillas fijas con normas genéricas. Debe conectarse a un corpus indexado de documentos reales de la tesis.
*   **Trazabilidad**:
    *   *Estado*: Parcial/Simulado. Muestra metadatos descriptivos pero no están integrados con los hashes reales de los modelos entrenados en el pipeline de la tesis.
