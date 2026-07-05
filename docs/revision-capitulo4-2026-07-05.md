# Revisión técnica integral del Capítulo IV

Fecha: 5 de julio de 2026

## 1. Criterio de organización

El Capítulo III debe contener definiciones, diseño, tecnologías seleccionadas y diagramas de arquitectura propuestos. El Capítulo IV debe comprobar la correspondencia entre esa propuesta y la implementación real, presentar validación funcional, resultados experimentales y limitaciones. Por ello, los diagramas de arquitectura y clases pueden aparecer en el Capítulo IV únicamente como evidencia de lo implementado, evitando repetir la teoría del capítulo anterior.

## 2. Tecnologías verificadas en el repositorio

- Frontend: React 18.3.1, React Router 6.23.1, Recharts 2.12.7, Vite 5.2.11 y Tailwind CSS 3.4.3.
- Backend: Python, Flask 3.0.3, Flask-Cors 4.0.1, SQLAlchemy 2.0.31 y Gunicorn 22.0.0.
- Persistencia principal: PostgreSQL 15 con pgvector.
- Analítica: XGBoost 2.0.3, scikit-learn 1.5.0, PyOD 2.0.0 y SHAP 0.45.1.
- RAG: Sentence-Transformers 3.0.0, pgvector y Google Generative AI 0.5.4.
- Despliegue: Docker Compose con tres servicios: base de datos, backend y frontend.

Corrección necesaria: el frontend implementado es React, no Streamlit. Flask se utiliza como API backend. SQLite aparece como ruta de contingencia local cuando no está disponible pgvector, pero no representa la arquitectura principal.

## 3. Estructura recomendada para el Capítulo IV

### 4.1 Estado de implementación del prototipo

Describir el estado del frontend, backend, persistencia, modelos analíticos, reportes y trazabilidad. Clasificar cada evidencia como implementada, preliminar o pendiente.

### 4.1.1 Tecnologías verificadas

Incluir una tabla con tecnología, versión, evidencia del repositorio y función en el sistema.

### 4.1.2 Componentes funcionales verificados

Relacionar las pantallas, rutas y modelos persistentes con los requisitos funcionales. Evitar declarar mejora estadística cuando solo existe evidencia visual o datos semilla.

### 4.1.3 Diagrama de despliegue

Representar: usuario -> frontend React/Vite -> API Flask/Gunicorn -> SQLAlchemy -> PostgreSQL/pgvector. Añadir conexiones del backend con artefactos XGBoost/PyOD/SHAP, Sentence-Transformers y el proveedor LLM.

### 4.1.4 Diagrama de clases persistentes

El diagrama debe incluir como mínimo: Usuario, OperacionAlerta, DecisionAuditoria, ExplicacionSHAP, DocumentoNormativo, ConfiguracionPipeline, PipelineRun, GeneratedReport y ArtifactLineage.

Relaciones verificadas:

- Usuario 1 a muchos DecisionAuditoria.
- OperacionAlerta 1 a muchos DecisionAuditoria.
- OperacionAlerta 1 a muchos ExplicacionSHAP.
- OperacionAlerta 1 a 0..1 GeneratedReport.
- PipelineRun 1 a muchos ArtifactLineage.

### 4.2 Correspondencia entre arquitectura propuesta e implementación

Comparar lo definido en el Capítulo III con la evidencia real: predicción, residuos, ensemble de anomalías, explicabilidad, recuperación semántica, reporte, telemetría y linaje.

### 4.2.1 Diagrama de secuencia de una auditoría

Secuencia recomendada: seleccionar alerta, consultar detalle, recuperar scores y configuración, obtener explicación, recuperar documentos, generar reporte, mostrar evidencia integrada y registrar decisión con tiempo y escala Likert.

### 4.3 Validación funcional preliminar

La evidencia actual permite afirmar que existe una arquitectura desplegable, un modelo de persistencia, configuración del ensemble, telemetría y almacenamiento vectorial. No permite aceptar todavía las hipótesis ni declarar superioridad predictiva, reducción comprobada de tiempo o mejora significativa de comprensión.

### 4.4 Resultados pendientes

Deben incorporarse métricas finales de forecasting, detección de anomalías, reportes, estudio con usuarios y trazabilidad reproducible.

## 4. Hallazgos técnicos y correcciones necesarias

1. OperacionAlerta.run_id no posee una clave foránea explícita hacia PipelineRun.run_id. La trazabilidad depende de consistencia lógica y debe reforzarse.
2. El modelo web conserva RUC y razón social, lo cual contradice el requisito de anonimización definido en el Capítulo III.
3. La configuración de despliegue utiliza credenciales de desarrollo y debe migrarse a variables de entorno o secretos antes de considerarse productiva.
4. El modo SQLite almacena embeddings como texto y no reproduce completamente las consultas vectoriales de pgvector.
5. XGBoost figura como modelo activo predeterminado. La participación efectiva de LightGBM debe demostrarse con ejecuciones y métricas reproducibles.
6. Los pesos iniciales del ensemble y el umbral global son configuraciones del prototipo; deben recalibrarse con el conjunto experimental final.
7. Los diagramas Mermaid del Capítulo III todavía están marcados como placeholders. Deben renderizarse a SVG o PNG para el documento final.
8. El Capítulo IV actual está cortado al final de 4.3 y se mezcla con referencias bibliográficas. Debe restaurarse la transición hacia conclusiones y bibliografía antes de aplicar el formato final.

## 5. Evidencias revisadas

- `docs/02-40-capitulo4.md`
- `docs/02-30-capitulo3.md`
- `sistema-web-agro/docker-compose.yml`
- `sistema-web-agro/backend/requirements.txt`
- `sistema-web-agro/frontend/package.json`
- `sistema-web-agro/backend/models.py`

## 6. Criterio de aceptación del capítulo

El Capítulo IV estará listo cuando cada afirmación indique su evidencia, el estado de la evidencia, el commit o versión correspondiente, el procedimiento de reproducción y la diferencia entre validación funcional y resultado científico. Los diagramas deberán coincidir con el código y no mostrar tecnologías inexistentes.