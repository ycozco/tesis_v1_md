# Documento Maestro de Correccion y Cierre Parcial

**Fecha:** 2026-06-22  
**Rama revisada:** `main`  
**Commit base:** `166bdf890125595ee04c0a7e72407c409b7e7383`  
**Documento PDF base:** `Tesis de Investigación YOSET 22-06.pdf`  
**Borrador vivo:** `docs/tesis/tesis_reestructurada.md`

## 1. Objetivo de la correccion

Este documento centraliza la correccion del avance de tesis hasta el punto actual. Su finalidad es alinear:

- el PDF base del 22-06;
- el borrador vivo en `docs/tesis/`;
- la evidencia tecnica del pipeline;
- el prototipo funcional `sistema-web-agro`;
- los resultados preliminares del Capitulo IV.

La correccion no debe inventar resultados. Todo avance sin evidencia reproducible queda marcado como parcial o pendiente.

## 2. Diagnostico general

### 2.1 PDF base

El archivo `Tesis de Investigación YOSET 22-06.pdf` fue extraido a texto en `reports/tesis_pdf_22_06_extracted.txt`.

Hallazgos:

- La portada del PDF conserva un titulo generico: `Titulo de la tesis`.
- La portada registra como asesor a `Karim Guevara`.
- El indice del PDF muestra Capitulo III con 3.3, 3.4 y 3.5 como secciones incompletas.
- El Capitulo IV del PDF tiene 4.1 y 4.2 sin desarrollo suficiente.
- El PDF sirve como linea base historica, pero no representa el estado tecnico actual del proyecto.

### 2.2 Borrador vivo

El archivo `docs/tesis/tesis_reestructurada.md` contiene una version mas avanzada:

- Titulo completo del sistema integrado.
- Capitulo I y II desarrollados.
- Capitulo III con arquitectura, flujo de datos, tecnologias, modelamiento, SHAP, RAG, trazabilidad, seguridad y despliegue.
- Capitulo IV modularizado con resultados cuantitativos, explicabilidad, reportes, usabilidad, trazabilidad y discusion.

### 2.3 Implementacion tecnica

La evidencia tecnica existe y debe usarse como respaldo directo:

| Capa | Archivo fuente | Estado | Evidencia |
|---|---|---|---|
| Prediccion FOB/volumen | `src/module1_prediction.py` | Implementado | XGBoost, LightGBM, Optuna, split temporal, residuos |
| Anomalias | `src/module2_anomaly.py` | Implementado | Isolation Forest, LOF, ECOD, percentiles, anomalias sinteticas |
| Explicabilidad | `src/module3_shap.py` | Implementado | TreeSHAP local/global, graficos, JSON |
| Reportes RAG | `src/module4_rag.py` | Implementado | BM25, embeddings, RRF, TemplateProvider/LLM |
| Validacion factual | `src/module5_validation.py` | Requiere revision documental | Debe vincularse con rubrica y resultados |
| Trazabilidad | `src/module6_traceability.py` | Implementado | UUID, hashes SHA-256, linaje |

### 2.4 Prototipo web

`sistema-web-agro` debe documentarse como evidencia central del punto 4:

| Componente | Ruta | Estado | Funcion verificable |
|---|---|---|---|
| Backend API | `sistema-web-agro/backend/app.py` | Parcial funcional | Login, dashboard, alertas, detalle, adjudicacion, configuracion, documentos, telemetria |
| Modelo de datos | `sistema-web-agro/backend/models.py` | Implementado | Usuarios, alertas, decisiones, SHAP, logs, documentos RAG |
| Seed y modelos semilla | `sistema-web-agro/backend/init_db.py` | Implementado parcial | Datos de prueba, normativas, modelos mock/semilla |
| Frontend | `sistema-web-agro/frontend/src/App.jsx` | Implementado | Rutas protegidas del prototipo |
| Detalle de alerta | `sistema-web-agro/frontend/src/pages/Detail.jsx` | Implementado parcial | Prediccion, score, SHAP, RAG, decision y tiempo |
| Data explorer | `sistema-web-agro/frontend/src/pages/Data.jsx` | Parcial | Carga simulada e indexacion documental |
| Telemetria | `sistema-web-agro/frontend/src/pages/Telemetry.jsx` | Parcial funcional | Tiempo de decision, comprension, exportacion |

## 3. Correcciones prioritarias

### C-01 Portada y metadatos institucionales

**Estado:** `[!]`  
**Objetivo relacionado:** formalizacion documental.  
**Seccion:** portada, presentacion, metadatos.

Problema:

- El PDF base aun muestra `Titulo de la tesis`.
- El PDF base registra asesor `Karim Guevara`.
- El borrador vivo registra el titulo completo y asesor `Dr. Victor Manuel Cornejo Aparicio`.

Correccion requerida:

- Usar como titulo rector:

`Sistema Integrado de Supervision Operativa con Inteligencia Artificial Explicable para la Deteccion de Anomalias y Generacion de Reportes Trazables en Empresas Agroexportadoras Peruanas`

- Confirmar asesor oficial antes del cierre final.
- Mientras no exista confirmacion, mantener el asesor actual del borrador vivo y registrar la duda en `PENDIENTES_CONFIRMACION.md`.

Evidencia:

- `reports/tesis_pdf_22_06_extracted.txt`
- `docs/tesis/tesis_reestructurada.md`
- `docs/tesis/PENDIENTES_CONFIRMACION.md`

### C-02 Estructura del Capitulo III

**Estado:** `[~]`  
**Objetivo relacionado:** OE1-OE8.  
**Seccion:** Capitulo III.

Problema:

- El PDF base deja 3.3, 3.4 y 3.5 incompletos.
- `CAPITULO_III_3_1_3_2.md` solo desarrolla 3.1 y 3.2.
- `tesis_reestructurada.md` tiene contenido tecnico avanzado, pero necesita reorganizarse como cierre verificable.

Correccion requerida:

Reestructurar Capitulo III con esta forma:

| Seccion | Estado esperado | Evidencia principal |
|---|---|---|
| 3.1 Generalidades de la propuesta | Consolidar | `docs/tesis/tesis_reestructurada.md` |
| 3.2 Arquitectura general | Consolidar | `src/module*.py`, `sistema-web-agro/` |
| 3.3 Obtencion y preparacion de datos | Completar | `data/`, `data-trademap/`, `codex-revision/metadata/` |
| 3.4 Diseno e implementacion del prototipo | Completar parcial | `sistema-web-agro/`, `src/module*.py` |
| 3.5 Diseno experimental y validacion | Completar como protocolo | `tests/`, `data/gold/`, `reports/audits/` |

Texto rector para 3.4:

> El prototipo funcional se implementa en la carpeta `sistema-web-agro` y materializa parcialmente la interfaz experimental del sistema. Incluye autenticacion, tablero de alertas, detalle de alerta con prediccion, score de anomalia, explicaciones SHAP, reporte RAG, registro de decision humana, telemetria y administracion de documentos. Su estado se considera funcional parcial, debido a que algunas rutas operan con datos semilla o simulados y requieren validacion reproducible con el dataset integrado final.

### C-03 Algoritmos propuestos y evidencia de implementacion

**Estado:** `[x]` para implementacion; `[~]` para incorporacion documental.  
**Objetivo relacionado:** OE3-OE7.  
**Seccion:** 3.4 y 3.5.

Correccion requerida:

Insertar una tabla de algoritmos propuestos:

| Algoritmo | Funcion | Archivo | Entrada | Salida | Estado |
|---|---|---|---|---|---|
| XGBoost | Prediccion de FOB y volumen | `src/module1_prediction.py` | `data/gold/prediction_features.parquet` | modelos `.pkl`, predicciones, residuos | Implementado |
| LightGBM | Prediccion de FOB y volumen | `src/module1_prediction.py` | `data/gold/prediction_features.parquet` | modelos `.pkl`, predicciones, residuos | Implementado |
| Isolation Forest | Deteccion de outliers | `src/module2_anomaly.py` | `data/gold/anomaly_features.parquet` | score individual | Implementado |
| LOF | Deteccion local de outliers | `src/module2_anomaly.py` | `data/gold/anomaly_features.parquet` | score individual | Implementado |
| ECOD | Deteccion no parametrica | `src/module2_anomaly.py` | `data/gold/anomaly_features.parquet` | score individual | Implementado |
| Ensemble percentilico | Score combinado | `src/module2_anomaly.py` | scores IF/LOF/ECOD | `ensemble_score`, severidad | Implementado |
| TreeSHAP | Explicabilidad local/global | `src/module3_shap.py` | modelos GBDT y features | JSON y graficos SHAP | Implementado |
| RAG BM25 + embeddings | Recuperacion documental | `src/module4_rag.py` | `knowledge_base/` y alerta | contexto recuperado | Implementado |
| TemplateProvider/LLM | Reporte tecnico | `src/module4_rag.py` | evidencia estructurada | reporte markdown | Implementado parcial |
| Hash SHA-256 + UUID | Trazabilidad | `src/module6_traceability.py` | datos, modelos, reportes | `traceability_log.json` | Implementado |

### C-04 Capitulo IV: resultados preliminares versus definitivos

**Estado:** `[!]`  
**Objetivo relacionado:** OE3-OE8.  
**Seccion:** Capitulo IV.

Problema:

- El borrador contiene tablas con resultados marcados como `Evaluado`, pero tambien advierte que los resultados finales deben generarse con dataset integrado versionado.
- Esto puede leerse como contradiccion si no se etiqueta claramente.

Correccion requerida:

- Renombrar las tablas actuales como `resultado preliminar` o `antecedente experimental`.
- Mantener como definitivos solo resultados con:
  - fecha;
  - commit;
  - dataset versionado;
  - comando de reproduccion;
  - hash de salida;
  - reporte de calidad.

Texto rector:

> Los valores numericos presentados en esta version corresponden a resultados preliminares o antecedentes experimentales, salvo que se indique expresamente version de dataset, commit, comando de reproduccion y hash del artefacto. No se usan para aceptar o rechazar hipotesis definitivas.

### C-05 Evaluacion con usuarios

**Estado:** `[P]`  
**Objetivo relacionado:** OE8.  
**Seccion:** 3.5, 4.3, anexos.

Problema:

- El prototipo registra telemetria y condiciones A/B.
- No existe aun evidencia final de ejecucion con participantes reales.

Correccion requerida:

- Mantener la evaluacion con usuarios como protocolo pendiente.
- No afirmar mejora significativa en tiempo, comprension, SUS o utilidad hasta contar con registros verificables.
- Usar `sistema-web-agro/frontend/src/pages/Telemetry.jsx` como evidencia de capacidad funcional, no como resultado experimental final.

### C-06 Comparacion PDF versus borrador vivo

**Estado:** `[x]` para diagnostico; `[~]` para correccion final.  
**Objetivo relacionado:** cierre documental.

Problema:

- El PDF 22-06 es una version antigua o incompleta frente al borrador vivo.

Correccion requerida:

- Tratar `Tesis de Investigación YOSET 22-06.pdf` como linea base historica.
- Tratar `docs/tesis/tesis_reestructurada.md` como fuente viva de correccion.
- Regenerar PDF final despues de aplicar correcciones documentales.

## 4. Checklist de ejecucion de correccion

| ID | Correccion | Estado | Archivo destino | Evidencia requerida |
|---|---|---|---|---|
| C-01 | Corregir portada/metadatos | [P] | portada / `tesis_reestructurada.md` | Confirmacion asesor oficial |
| C-02 | Completar estructura 3.3-3.5 | [~] | Capitulo III | `data/`, `src/`, `sistema-web-agro/`, `tests/` |
| C-03 | Insertar tabla de algoritmos | [x] | Capitulo III | `src/module*.py` |
| C-04 | Etiquetar resultados preliminares | [~] | Capitulo IV | `data/gold/`, `reports/audits/`, logs |
| C-05 | Marcar evaluacion usuarios pendiente | [x] | 3.5, 4.3, anexos | `sistema-web-agro` como capacidad funcional |
| C-06 | Generar matriz prototipo web | [P] | `docs/tesis/` | endpoints, rutas, capturas, pruebas |
| C-07 | Regenerar tesis completa | [P] | `output/tesis.pdf` / `.docx` | Compilacion posterior a correcciones |

## 5. Correcciones aplicadas en modulos canonicos

**Fecha de aplicacion:** 2026-06-22  
**Fuente canonica de compilacion:** `docs/02-*.md`  
**Objetivo:** actualizar la tesis compilable al estado actual del prototipo sin afirmar resultados definitivos no reproducidos.

| ID | Archivo | Correccion aplicada | Estado |
|---|---|---|---|
| A-01 | `docs/02-02-indices.md` | Se actualizo el indice para incluir 3.3, 3.4, 3.5 y el Capitulo IV modularizado hasta 4.7. | Aplicado |
| A-02 | `docs/02-30-capitulo3.md` | Se agregaron las secciones 3.3 Obtencion y preparacion de datos, 3.4 Diseno e implementacion del prototipo y 3.5 Diseno experimental y validacion. | Aplicado |
| A-03 | `docs/02-30-capitulo3.md` | Se incorporo tabla de algoritmos propuestos vinculada con `src/module1_prediction.py` a `src/module6_traceability.py` y con `sistema-web-agro/`. | Aplicado |
| A-04 | `docs/02-40-capitulo4.md` | Se reemplazo la afirmacion de prototipo completo por estado parcial verificable y reglas de interpretacion de evidencia. | Aplicado |
| A-05 | `docs/02-41-capitulo4-resultados-cuantitativos.md` | Se reclasificaron metricas como preliminares de datos semilla y se agrego evidencia faltante para VD1. | Aplicado |
| A-06 | `docs/02-42-capitulo4-explicabilidad-reportes.md` | Se separo avance funcional SHAP/RAG de validacion factual pendiente para VD2 y VD3. | Aplicado |
| A-07 | `docs/02-43-capitulo4-usabilidad-trazabilidad.md` | Se dejo la evaluacion con usuarios como pendiente y la telemetria semilla como validacion de flujo. | Aplicado |
| A-08 | `docs/02-44-capitulo4-discusion.md` | Se renumero la discusion como 4.5 para evitar duplicidad con usabilidad. | Aplicado |
| A-09 | `docs/02-45-capitulo4-limitaciones-sintesis.md` | Se renumeraron limitaciones y sintesis como 4.6 y 4.7. | Aplicado |

## 6. Pendientes despues de la correccion

| Pendiente | Ruta esperada | Criterio de cierre |
|---|---|---|
| Confirmar asesor oficial | `docs/tesis/PENDIENTES_CONFIRMACION.md` | Nombre validado institucionalmente |
| Ejecutar prueba de fuga temporal | `reports/tesis/data-quality/leakage-tests/` | Reporte con comando, salida y hash |
| Congelar dataset semanal final | `data/gold/` | Dataset versionado, sin duplicidad de clave y con hash |
| Registrar corridas experimentales | `reports/tesis/experiments/` | ID de ejecucion, commit, semilla, hiperparametros y metricas |
| Validar reportes automaticos | `reports/tesis/report-validation/` | Rubrica, reportes rechazados y comparacion con plantilla |
| Ejecutar estudio con usuarios | `reports/tesis/user-study/` | Participantes, consentimiento, anonimizacion y prueba estadistica |
| Compilar tesis actualizada | `output/` | PDF/DOCX/HTML regenerados desde `docs/02-95-tesis.md` |

## 5. Definicion de avance defendible

El proyecto puede defenderse hasta el punto actual bajo esta formulacion:

> La tesis cuenta con una arquitectura implementada y un prototipo funcional parcial. Existen modulos de prediccion, deteccion de anomalias, explicabilidad, reportes RAG y trazabilidad, junto con una interfaz web de auditoria. Los resultados del Capitulo IV deben tratarse como preliminares hasta que se congelen dataset, comandos, hashes y ejecuciones experimentales. La evaluacion con usuarios se mantiene como protocolo pendiente si no existen registros verificables.

## 6. Proximo cierre necesario

Antes de declarar el punto 4 cerrado, deben existir:

- matriz de endpoints y vistas de `sistema-web-agro`;
- captura o registro de ejecucion del prototipo;
- mapa algoritmo -> archivo -> entrada -> salida;
- lista de resultados preliminares versus definitivos;
- PDF regenerado desde el borrador vivo;
- registro de cambios incorporados en `CAMBIOS_REALIZADOS.md`.
