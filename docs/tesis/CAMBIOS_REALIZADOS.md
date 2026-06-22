# Registro de Cambios Realizados

Este documento detalla las modificaciones y correcciones aplicadas al codigo del prototipo tecnico y a la estructura academica del documento de tesis.

## 1. Tabla de Cambios Realizados

| Archivo | Seccion | Problema encontrado | Cambio realizado | Justificacion | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `module1_prediction.py` | Capa 1: Regresores GBDT | Descarte incorrecto de columnas `product_code` y `market_aggregated` tras concatenar variables dummies. | Se modifico la concatenacion de dummies para preservar columnas originales. | Permite agrupar predicciones y series de tiempo correctamente. | **Corregido** |
| `module2_anomaly.py` | Capa 2: Ensemble y validacion | NameError en calculo de recall por variable temporal no definida. | Se renombro la variable temporal a `anomaly_types`. | Evita caidas durante la validacion del ensemble. | **Corregido** |
| `module3_shap.py` | Capa 3: Explicabilidad SHAP | Error de memoria en TreeSHAP por desalineacion de columnas. | Se alinearon columnas de test con el entrenamiento. | Mejora reproducibilidad de explicaciones locales. | **Corregido** |
| `module4_rag.py` | Capa 4: RAG e informes | Faltaban importaciones esenciales. | Se agregaron importaciones necesarias. | Permite procesar JSONs de evidencia y arrays numericos de SHAP. | **Corregido** |
| `run_all.py` | Orquestador y reportes | Fallos de decodificacion en Windows y definiciones incompletas. | Se agrego manejo de `errors="replace"` y definiciones globales necesarias. | Asegura ejecucion secuencial del pipeline en Windows. | **Corregido** |
| `build_github_pages.py` | Generador estatico | No exportaba endpoints JSON de supervisor. | Se implementaron exportaciones estaticas de API. | Permite dashboard funcional en GitHub Pages. | **Corregido** |
| `02-95-tesis.md` | General | Falta de alineacion en alcance, variables y unidad de analisis. | Se reestructuro la tesis de extremo a extremo. | Alinea redaccion teorica con datos, pipeline y alcance. | **Corregido** |
| `docs/tesis/` | Todo | Faltaban documentos academicos de soporte. | Se crearon matrices, diccionario, decisiones, pendientes y referencias. | Sostiene auditoria academica de la tesis. | **Implementado** |

## 2. Cambios de Revision y Correccion Maestra 2026-06-22

| Archivo | Seccion | Problema encontrado | Cambio realizado | Justificacion | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `docs/tesis/00-checklist-maestro.md` | Control de avance | El checklist no tenia estados actualizados, hashes ni contraste real con PDF. | Se actualizo con commit base, hashes SHA-256, estados `[x]`, `[~]`, `[P]` y referencia al documento maestro. | Permite auditar el avance sin confundir evidencia implementada, parcial o pendiente. | **Implementado** |
| `docs/tesis/10-revision-avance.md` | Revision documental | La revision previa trataba la extraccion del PDF como pendiente. | Se incorporo el texto extraido del PDF 22-06 y se documento la diferencia entre PDF historico y borrador vivo. | Deja claro que el PDF base esta incompleto frente a `tesis_reestructurada.md`. | **Corregido** |
| `docs/tesis/11-documento-maestro-correccion.md` | Correccion maestra | No existia documento rector que conectara PDF, borrador vivo, evidencia tecnica y prototipo. | Se creo un documento maestro con diagnostico, correcciones prioritarias, matriz de algoritmos, prototipo funcional y checklist de cierre. | Centraliza la correccion necesaria para cerrar parcialmente hasta el punto actual. | **Implementado** |
| `reports/tesis_pdf_22_06_extracted.txt` | Evidencia de contraste | El PDF 22-06 no estaba disponible como texto inspeccionable. | Se extrajo el PDF mediante `pdftotext -layout -nopgbrk`. | Permite comparar portada, indice, Capitulo III y Capitulo IV contra el borrador vivo. | **Implementado** |

## 3. Clasificacion del Estado de los Entregables

1. **Corregido:** Se solucionaron errores o inconsistencias que bloqueaban ejecucion, trazabilidad o coherencia documental.
2. **Implementado:** Se crearon documentos o artefactos necesarios para sostener la revision academica y tecnica.
3. **Pendiente por dato:** Requiere completar o congelar dataset, comandos, hashes y resultados finales.
4. **Pendiente por confirmacion academica:** Requiere decision humana del alumno, asesor o escuela, por ejemplo asesor oficial, linea institucional y evaluacion con usuarios.
