# CAPITULO IV: RESULTADOS Y DISCUSION

> **Estado:** capitulo modularizado. Los resultados finales se completaran unicamente despues de ejecutar los experimentos E1-E5 sobre el dataset agroexportador integrado versionado.

Este capitulo organiza la evaluacion empirica del sistema integrado de supervision operativa. Su funcion actual es dejar preparada la estructura de reporte, los criterios de lectura y las tablas que recibiran los resultados finales.

Los valores obtenidos en corridas previas sobre datasets sinteticos o versiones anteriores se consideran evidencia auxiliar de desarrollo. No deben presentarse como resultados finales de tesis hasta que se regeneren con:

- version del dataset integrado;
- split temporal documentado;
- codigo de experimento;
- fecha de ejecucion;
- semillas utilizadas;
- reporte de calidad de datos;
- trazabilidad de fuente para cada variable.

La estructura del capitulo queda dividida en modulos para facilitar mantenimiento:

| Modulo | Archivo | Contenido |
|---|---|---|
| 4.1 | `docs/02-41-capitulo4-resultados-cuantitativos.md` | Prediccion y deteccion, VD1. |
| 4.2 | `docs/02-42-capitulo4-explicabilidad-reportes.md` | SHAP y reportes RAG, VD2-VD3. |
| 4.3 | `docs/02-43-capitulo4-usabilidad-trazabilidad.md` | Estudio de usuarios y trazabilidad, VD4-VD5. |
| 4.4 | `docs/02-44-capitulo4-discusion.md` | Discusion, contraste con literatura e hipotesis. |
| 4.5-4.6 | `docs/02-45-capitulo4-limitaciones-sintesis.md` | Limitaciones y sintesis final. |

La lectura del capitulo debe conservar una regla metodologica: **ninguna metrica se interpreta sin indicar fuente, version de dataset, granularidad, split y estado de validacion**.
