# Integración del plan FastAPI en la tesis

**Fecha:** 5 de julio de 2026

Se integró en la sección 4.1.2.1 del documento de tesis una síntesis del archivo `docs/2026-07-05-plan-migracion-fastapi-produccion.md`.

La sección incorporada describe:

- la arquitectura objetivo con React, FastAPI, Uvicorn, SQLAlchemy y PostgreSQL/pgvector;
- el estado inicial verificado de la migración;
- las fases para migrar autenticación, dashboard, alertas, decisiones, reportes y telemetría;
- la separación de servicios de predicción, anomalías, SHAP y RAG;
- el uso previsto de Alembic, contenedores, TLS, observabilidad, pruebas y CI/CD;
- los pendientes críticos y los criterios necesarios para retirar Flask.

FastAPI debe mantenerse descrito como arquitectura objetivo hasta completar las rutas, pruebas y evidencias definidas en el plan técnico.
