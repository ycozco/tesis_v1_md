# Revision de Avance de la Tesis

**Fecha de revision:** 2026-06-22  
**Rama:** `main`  
**Commit base:** `166bdf890125595ee04c0a7e72407c409b7e7383`

## Fuentes revisadas

- `docs/tesis/tesis_reestructurada.md`
- `docs/tesis/CAPITULO_III_3_1_3_2.md`
- `docs/tesis/PENDIENTES_CONFIRMACION.md`
- `docs/tesis/CAMBIOS_REALIZADOS.md`
- `Tesis de Investigación YOSET 22-06.pdf`
- `reports/tesis_pdf_22_06_extracted.txt`
- `output/tesis.tex`
- `output/tesis.pdf`
- `sistema-web-agro/`
- `src/module1_prediction.py` a `src/module6_traceability.py`

## Hallazgos principales

### 1. La tesis ya tiene una base estructural solida

El borrador vivo incluye:

- Portada, resumen, abstract e indice.
- Capitulo I con problema, objetivos, hipotesis y alcance.
- Capitulo II con marco teorico y estado del arte.
- Capitulo III con arquitectura, datos, prediccion, anomalias, SHAP, RAG y trazabilidad.
- Capitulo IV con estructura preliminar para resultados cuantitativos, cualitativos, usabilidad, trazabilidad y discusion.

### 2. El PDF 22-06 es una linea base antigua o incompleta

El texto extraido del PDF muestra:

- Portada generica con `Titulo de la tesis`.
- Asesor registrado como `Karim Guevara`.
- Capitulo III con 3.3, 3.4 y 3.5 incompletos.
- Capitulo IV con 4.1 y 4.2 sin desarrollo suficiente.

Por tanto, el PDF no debe tratarse como version final. Debe usarse como referencia historica para saber que corregir.

### 3. El borrador vivo ya supera al PDF base

`docs/tesis/tesis_reestructurada.md` incluye una version mas avanzada que el PDF:

- Titulo completo de la investigacion.
- Capitulo III mas detallado.
- Tabla modular del Capitulo IV.
- Advertencias sobre resultados preliminares.

La correccion debe partir del borrador vivo, no del PDF antiguo.

### 4. El prototipo web aporta evidencia funcional real

`sistema-web-agro` no es solo maqueta:

- `backend/app.py` expone autenticacion, dashboard, alertas, detalle, adjudicacion, configuracion, documentos, telemetria, integridad, usuarios y trazabilidad.
- `backend/models.py` define usuarios, alertas, decisiones, explicaciones SHAP, logs y documentos normativos.
- `backend/init_db.py` siembra usuarios, alertas, decisiones, SHAP, logs y normativas RAG.
- `frontend/src/App.jsx` define rutas protegidas y vistas operativas.
- `frontend/src/pages/Detail.jsx` integra prediccion, anomalias, SHAP, RAG y decision humana.
- `frontend/src/pages/Data.jsx` cubre carga e indexacion documental.
- `frontend/src/pages/Telemetry.jsx` cubre tiempo de decision, comprension percibida y exportacion.

### 5. Los algoritmos propuestos estan implementados

- `src/module1_prediction.py`: XGBoost + LightGBM para FOB y volumen con validacion temporal.
- `src/module2_anomaly.py`: Isolation Forest + LOF + ECOD con score por percentiles y evaluacion con anomalias sinteticas.
- `src/module3_shap.py`: TreeSHAP para explicaciones locales y globales.
- `src/module4_rag.py`: RAG hibrido con BM25, embeddings y plantilla deterministica/LLM.
- `src/module6_traceability.py`: hashes y linaje de evidencia.

## Cambios necesarios

### Capitulo I

- Corregir metadatos y portada segun asesor oficial confirmado.
- Mantener alineados problema, objetivos, hipotesis y alcance con la implementacion real.

### Capitulo II

- Verificar que las referencias teoricas sostengan los algoritmos realmente usados.
- Evitar mantener algoritmos descartados como si fueran parte de la propuesta final.

### Capitulo III

- Completar 3.3, 3.4 y 3.5 con evidencia real.
- Integrar `sistema-web-agro` como prototipo funcional parcial.
- Incluir tabla algoritmo -> archivo -> entrada -> salida -> estado.

### Capitulo IV

- Etiquetar resultados como preliminares cuando no tengan dataset, commit, comando, fecha y hash.
- No afirmar resultados de usuarios sin registros verificables.

## Pendientes criticos

- Confirmar asesor oficial y metadatos institucionales.
- Crear matriz detallada de vistas/endpoints del prototipo.
- Registrar comandos reproducibles y salidas para pipeline, tests y reportes.
- Regenerar PDF final desde el borrador vivo corregido.

## Documento rector

La correccion desarrollada queda centralizada en:

`docs/tesis/11-documento-maestro-correccion.md`

## Conclusion

El avance actual es defendible como implementacion tecnica y prototipo funcional parcial. El riesgo principal ya no es falta de sistema, sino falta de trazabilidad documental fina entre PDF, borrador vivo, evidencia tecnica y resultados preliminares. La siguiente correccion debe concentrarse en Capitulo III, Capitulo IV y matriz del prototipo web.
