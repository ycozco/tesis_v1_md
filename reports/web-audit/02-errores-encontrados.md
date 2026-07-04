# REGISTRO DE ANOMALÍAS Y DEFECTOS ENCONTRADOS
## Sistema Integrado de Inteligencia Artificial Explicable
### Tesis UNSA — Yoset Cozco Mauri (2026)

Este documento contiene la lista detallada de dependencias débiles, simulaciones dinámicas y comportamientos inestables identificados en el prototipo v1.

---

## 1. Defectos en Backend (API Flask)

1.  **Mutabilidad en Métodos GET**:
    *   *Descripción*: Las solicitudes a `/api/alerts/<id>` modifican el estado de la alerta o recalculan valores aleatorios de variables físicas, rompiendo la idempotencia HTTP.
2.  **Falta de Enlace a Base de Datos Unificada**:
    *   *Descripción*: No existe persistencia para las métricas del pipeline de entrenamiento real (`predictions`, `run_id`, hashes). El frontend consume datos mock.
3.  **Vulnerabilidad de Roles**:
    *   *Descripción*: El token JWT no valida privilegios en los endpoints de configuración y carga de datasets; cualquier usuario autenticado puede acceder.

---

## 2. Defectos en Frontend (React)

1.  **Valores Físicos Simulados**:
    *   *Descripción*: La temperatura y el peso de mermas se generan dinámicamente con `Math.random()` en el componente de detalle de alerta.
2.  **Métricas de Telemetría Ruido**:
    *   *Descripción*: El dashboard de telemetría y experimentos A/B calcula porcentajes de éxito y recuentos de usuarios activos en línea con un bucle periódico dinámico y aleatorio.
