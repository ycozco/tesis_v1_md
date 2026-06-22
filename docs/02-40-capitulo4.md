# CAPÍTULO IV — RESULTADOS Y DISCUSIÓN

> **Estado del capítulo:** avance parcial verificable al 22 de junio de 2026. Este capítulo documenta el estado funcional del prototipo y los resultados preliminares disponibles. Las métricas derivadas de datos semilla se presentan como validación de flujo, no como resultados definitivos de la investigación.

## 4.1 Estado de Implementación del Prototipo

El prototipo funcional se ubica en `sistema-web-agro/` y permite validar la integración de las capas principales de la propuesta: autenticación de auditores, panel operativo, gestión de alertas, detalle de operación con IA explicable, telemetría experimental, métricas de integridad, explorador de datos, configuración del modelo y administración de usuarios.

### 4.1.1 Alcance verificable

| Bloque | Evidencia principal | Estado |
|---|---|---|
| Backend/API | `sistema-web-agro/backend/app.py`, `models.py`, `init_db.py` | Implementado para prototipo |
| Frontend | `sistema-web-agro/frontend/src/pages/` | Implementado |
| Despliegue local | `sistema-web-agro/docker-compose.yml`, `run.ps1` | Implementado, sujeto a verificación de entorno |
| Pantallas y flujo | `sistema-web-agro/*/screen.png`, `frontend/src/pages/*.jsx` | Disponible |
| Datos semilla | `sistema-web-agro/backend/init_db.py`, `DATOS_PRUEBA.txt` | Disponible para validación funcional |
| Dataset final de tesis | `data/gold/`, `reports/tesis/` | Parcial o pendiente según evidencia |

### 4.1.2 Reglas de interpretación

Los resultados de este capítulo se clasifican en tres niveles:

1. **Implementado:** existe ruta real, código o artefacto verificable.
2. **Preliminar:** existe salida funcional o dato semilla, pero aún no constituye evidencia final.
3. **Pendiente:** requiere dataset final, experimento formal, prueba automatizada o validación documental adicional.

Esta separación evita presentar como definitivos los resultados generados con datos de prueba. La evidencia definitiva deberá registrar fecha, commit, dataset, configuración, semilla, entorno, hash de salida y procedimiento de reproducción.

### 4.1.3 Algoritmos integrados en el avance actual

| Capa | Algoritmo/técnica | Uso en el prototipo y tesis | Estado |
|---|---|---|---|
| Predicción | XGBoost/LightGBM, GBDT | Estimar valor FOB o volumen esperado | Parcial: implementado en scripts/prototipo, pendiente validación final |
| Anomalías | Isolation Forest, LOF, ECOD | Calcular score individual y score ensemble | Parcial: funcional con datos semilla |
| Explicabilidad | SHAP/TreeSHAP | Mostrar contribuciones locales por variable | Parcial: funcional con evidencia semilla |
| Reportes | RAG y plantilla determinística | Generar reporte técnico anclado a documentos | Parcial: motor funcional, validador formal pendiente |
| Trazabilidad | IDs, hashes, logs, relaciones alerta-decisión | Reconstruir el flujo de evidencia | Parcial: flujo implementado, auditoría final pendiente |

### 4.1.4 Estado frente a las puertas de control

| Puerta | Estado al punto actual | Observación |
|---|---|---|
| A. Datos | Parcial | Falta congelar dataset semanal final y reporte de fuga de información |
| B. Implementación | Parcialmente aprobada | El prototipo respalda rutas, pantallas y flujo operativo |
| C. Experimento | Pendiente | Faltan partición temporal congelada, semillas, métricas definitivas y protocolos corridos |
| D. Capítulo III | En avance | La arquitectura e implementación ya están documentadas de forma ampliada |
| E. Capítulo IV preliminar | Parcial | Solo deben incluirse resultados marcados como preliminares o pendientes |

Las secciones siguientes desarrollan los resultados preliminares disponibles y dejan explícito qué evidencia todavía debe completarse.
