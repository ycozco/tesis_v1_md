# Revision exhaustiva de la fase base de tesis

**Proyecto:** Sistema integrado de prediccion, deteccion de anomalias y generacion de reportes en entornos empresariales / agroexportacion peruana  
**Fecha de revision:** 2026-05-17  
**Archivos revisados:** `docs/tesis.md`, `entregable/sustentacion-planteamiento-implementacion.md`, `entregable/integracion-datasets-por-capitulo.md`, `entregable/validacion-referencias-datasets.md`, `refs.bib`

## 1. Dictamen general

La fase base tiene una idea potente y defendible: integrar prediccion tabular, deteccion de anomalias, explicabilidad y generacion de reportes en un pipeline trazable. Sin embargo, todavia no esta suficientemente blindada para sustentacion porque mezcla tres dominios que no estan completamente alineados:

1. supervision operativa agroexportadora;
2. auditoria financiera / fraude bancario;
3. gobernanza regulatoria de IA.

El principal riesgo ante jurado no es tecnico, sino de coherencia investigativa: el problema se formula para agroexportacion, las hipotesis y baselines se apoyan en fraude financiero, y la regulacion principal citada pertenece en parte al sistema financiero supervisado. Esto se puede corregir sin rehacer la tesis, pero debe decidirse un eje dominante.

## 2. Hallazgos criticos

### H1. Inconsistencia de dominio entre problema, datos y marco teorico

**Evidencia:**  
En `docs/tesis.md` el problema central se formula para empresas agroexportadoras peruanas, pero varias secciones posteriores hablan de auditoria financiera, fraude financiero, entidades financieras y sistema SBS.

**Riesgo en sustentacion:**  
El jurado puede preguntar: si el problema es agroexportador, por que se valida con BAF Bank Account Fraud, por que la SBS es un eje regulatorio, y por que las variables dependientes se expresan como confianza del auditor financiero.

**Correccion recomendada:**  
Elegir una de estas rutas:

- Ruta A: tesis agroexportadora pura. Mantener MIDAGRI, SENAMHI, SENASA, SUNAT; cambiar "auditor financiero" por "supervisor operativo / auditor interno de calidad"; usar SBS solo como referencia metodologica, no como obligacion directa.
- Ruta B: tesis de auditoria empresarial con caso agroexportador. Formular el problema como supervision/auditoria interna empresarial basada en datos tabulares, con caso aplicado agroexportador.
- Ruta C: tesis financiera. Cambiar el contexto agroexportador por fraude/auditoria financiera y usar BAF como dataset principal.

**Recomendacion:** Ruta B. Es la mas flexible y aprovecha casi todo lo escrito.

### H2. Uso debil de la Resolucion SBS N. 053-2023 para agroexportacion

**Evidencia:**  
La tesis afirma que la SBS 053-2023 exige trazabilidad en sistemas IA para el contexto usado. La fuente oficial de SBS indica que el reglamento se orienta a modelos usados en riesgos de credito, mercado, liquidez, operacional y lavado de activos de empresas del sistema financiero y de seguros.

**Riesgo en sustentacion:**  
Si la empresa agroexportadora no es entidad supervisada por SBS, la obligacion directa no aplica. El jurado podria verlo como sobrerregulacion o cita normativa fuera de alcance.

**Correccion recomendada:**  
Reformular asi:

> La Resolucion SBS N. 053-2023 no se adopta como obligacion directa para empresas agroexportadoras, sino como marco de referencia nacional para buenas practicas de gestion de riesgo de modelos, trazabilidad, validacion y monitoreo.

### H3. Cifras de sustentacion no estan suficientemente verificadas

**Evidencia:**  
En `sustentacion-planteamiento-implementacion.md` se citan: agroexportaciones 2025 por USD 9,500 millones, 9.2 millones de toneladas, mermas 2-8%, rechazo en frontera 3-5%, incumplimiento de 92% de PYMES agroexportadoras, ROI 42x.

**Riesgo en sustentacion:**  
Estas cifras son faciles de atacar si no tienen fuente directa, tabla, fecha, URL y metodo de calculo. Ademas, busquedas recientes muestran cifras 2025 cercanas a USD 14,500-15,000 millones para agroexportaciones totales segun fuentes sectoriales, por lo que USD 9,500 millones puede quedar desactualizado o referirse a un subconjunto.

**Correccion recomendada:**  
Crear una tabla "Supuestos cuantitativos de la tesis" con columnas: afirmacion, valor, fuente primaria, fecha, alcance, uso en la tesis, nivel de confianza. Eliminar el 92% ASBANC si no se encuentra fuente exacta.

### H4. Hipotesis H1a no coincide con el dominio agroexportador

**Evidencia:**  
H1a dice que el ensemble supera metodos individuales ante diversas distribuciones de datos financieros. Pero el problema habla de cadena operativa agroexportadora.

**Correccion recomendada:**  
Cambiar a:

> H1a: El ensemble de detectores de anomalias supera a los metodos individuales en la identificacion de desviaciones operativas en datos tabulares agroexportadores y benchmarks de referencia.

### H5. Variables e indicadores estan bien pensados, pero aun no son operacionalizables

**Evidencia:**  
Se definen VD1 a VD5, pero faltan formulas operativas, fuente de cada indicador, unidad de analisis, procedimiento de medicion y criterio estadistico.

**Riesgo en sustentacion:**  
El jurado puede pedir: como mediras trazabilidad en 80%, como calcularas SHAP Coverage, cuantos auditores participan, que prueba estadistica usaras para confianza y tiempo a decision.

**Correccion recomendada:**  
Agregar una matriz de operacionalizacion:

| Variable | Indicador | Formula/procedimiento | Fuente | Unidad | Criterio de aceptacion |
|---|---|---|---|---|---|
| Rendimiento | PR-AUC | precision-recall sobre conjunto test | dataset etiquetado | modelo | >= baseline + delta |
| Usabilidad | tiempo a decision | segundos desde alerta hasta decision | prueba con usuarios | participante/tarea | reduccion >= 30% |
| Trazabilidad | cobertura de logs | decisiones con dato+modelo+version+explicacion | bitacora | alerta | >= 95% |

### H6. BAF Benchmark no valida directamente agroexportacion

**Evidencia:**  
BAF es de fraude bancario. Es util para probar desbalance, drift y datos tabulares, pero no demuestra eficacia agroexportadora.

**Correccion recomendada:**  
Presentarlo como benchmark metodologico, no como dataset principal. La validacion principal debe ser:

1. datos agroexportadores publicos como proxy;
2. datos sinteticos agroexportadores documentados;
3. si existe, muestra privada de empresa colaboradora;
4. BAF solo como benchmark adicional de robustez tabular.

### H7. La arquitectura es defendible, pero necesita diagrama formal y flujo de datos

**Fortaleza:**  
La arquitectura de cuatro capas es clara y defendible: GBDT / anomalias / SHAP / LLM-RAG.

**Debilidad:**  
Falta formalizar entradas, salidas, artefactos y responsabilidades de cada modulo.

**Correccion recomendada:**  
Agregar una tabla de arquitectura:

| Capa | Entrada | Proceso | Salida | Evidencia generada |
|---|---|---|---|---|
| Prediccion | datos tabulares historicos | XGBoost/LightGBM | riesgo esperado | version modelo, metricas |
| Anomalias | observacion actual + historico | IF/LOF/ECOD/SVDD | score anomalia | ranking, umbral |
| Explicabilidad | prediccion + features | SHAP | contribuciones | top variables |
| Reporte | score + SHAP + contexto | RAG/LLM | informe trazable | citas, plantilla, log |

### H8. Referencias y citas tienen fallo tecnico severo

**Evidencia:**  
Hay 30 claves citadas en `docs/tesis.md` que no existen en `refs.bib`. Ejemplos: `auditcopilot2025`, `liu2008isolationforest`, `mitchell2019modelcards`, `lim2020tft`, `zhao2019pyod`.

**Riesgo:**  
Al compilar, las citas apareceran sin resolver o no entraran en referencias. Esto afecta forma y credibilidad.

**Correccion recomendada:**  
Unificar claves. Por ejemplo:

- `auditcopilot2025` -> `kadir2025auditcopilot`
- `liu2008isolationforest` -> `liu2008iforest`
- `mitchell2019modelcards` -> `mitchell2019model`
- `leocadio2024framework` -> `leocadio2024auditing`

Tambien hay referencias en `refs.bib` con URLs genericas o titulos no verificables que deben limpiarse.

### H9. Sustentacion economica sobrepromete

**Evidencia:**  
El documento de sustentacion afirma ROI 4,225% y payback menor a un mes.

**Riesgo:**  
Un ROI tan alto genera sospecha si no se explican supuestos, base de calculo, alcance de empresa, tasa de captura y sensibilidad.

**Correccion recomendada:**  
Reformular como escenario exploratorio:

> Bajo un escenario hipotetico de adopcion en una empresa con perdidas anuales estimadas en X, una reduccion conservadora de Y% podria generar ahorros de Z. Estas cifras no constituyen resultado experimental, sino justificacion economica preliminar.

Agregar escenarios conservador, medio y optimista.

## 3. Elementos fuertes que conviene preservar

1. El problema de trazabilidad y explicabilidad esta bien identificado.
2. La separacion del LLM como generador de reportes, no como detector, es una decision tecnicamente madura.
3. SHAP como puente entre modelo y reporte es una buena contribucion de ingenieria.
4. El uso de GBDT para datos tabulares esta bien sustentado en literatura.
5. La idea de usar Model Cards y Datasheets fortalece la gobernanza.
6. La tesis tiene potencial si se presenta como sistema integrado de supervision empresarial con caso agroexportador.

## 4. Preguntas probables del jurado y respuestas recomendadas

**P:** Si su tesis es agroexportadora, por que usa datos bancarios BAF?  
**R:** BAF se usa como benchmark metodologico para evaluar robustez en datos tabulares desbalanceados y con drift. La validacion de dominio se realiza con datos agroexportadores publicos y/o privados; BAF no reemplaza el caso agroexportador.

**P:** La SBS aplica a agroexportadoras?  
**R:** No como obligacion directa. Se adopta como referencia nacional de buenas practicas para gestion de riesgo de modelos. Para el caso agroexportador, la trazabilidad se justifica por auditoria interna, calidad, cumplimiento y gobernanza de IA.

**P:** Que aporta su tesis si usa tecnicas existentes?  
**R:** El aporte no es proponer un nuevo algoritmo, sino integrar componentes probados en un pipeline trazable: prediccion, deteccion, explicabilidad y reporte auditable, evaluando si la integracion mejora tiempo de decision, confianza y trazabilidad respecto a componentes aislados.

**P:** Como evitara que el LLM invente informacion?  
**R:** El LLM no toma decisiones ni calcula anomalias. Solo redacta reportes a partir de evidencias estructuradas: score, top variables SHAP, umbral, dataset, version del modelo y contexto recuperado por RAG. El reporte queda sujeto a revision humana.

**P:** Como medira trazabilidad?  
**R:** Mediante un checklist por alerta: dato de entrada identificado, version de dataset, version de modelo, hiperparametros, score, umbral, explicacion SHAP, plantilla de reporte, usuario revisor y timestamp. La metrica sera el porcentaje de alertas que cumplen todos los campos obligatorios.

## 5. Reestructuracion recomendada de la fase base

### Titulo recomendado

> Sistema integrado de supervision operativa con inteligencia artificial explicable para la deteccion de anomalias y generacion de reportes trazables en empresas agroexportadoras peruanas

### Problema principal recomendado

> Como mejorar la deteccion temprana, explicacion y documentacion de anomalias operativas en empresas agroexportadoras peruanas mediante un sistema integrado de inteligencia artificial explicable que combine prediccion tabular, deteccion de anomalias, explicabilidad y generacion de reportes trazables?

### Objetivo general recomendado

> Disenar, implementar y evaluar un sistema integrado de supervision operativa basado en modelos tabulares, deteccion de anomalias, explicabilidad SHAP y generacion de reportes con RAG, orientado a mejorar la trazabilidad, comprension y tiempo de decision frente a anomalias en datos agroexportadores.

### Hipotesis general recomendada

> Un sistema integrado de prediccion, deteccion, explicabilidad y reporte trazable mejora la trazabilidad de decisiones, la comprension de alertas y el tiempo de decision de supervisores frente al uso de componentes aislados.

## 6. Checklist de correccion inmediata

- [ ] Definir si la tesis sera agroexportadora, financiera o empresarial con caso agroexportador.
- [ ] Reescribir hipotesis y variables para eliminar contradicciones de dominio.
- [ ] Cambiar "auditor financiero" por "supervisor operativo / auditor interno" si se mantiene agroexportacion.
- [ ] Reubicar SBS como marco de referencia, no obligacion directa.
- [ ] Verificar cifras sectoriales 2025 con fuente primaria o eliminarlas.
- [ ] Eliminar afirmaciones no trazables: 92% ASBANC, ROI 42x, mermas 2-8% sin fuente.
- [ ] Crear matriz de operacionalizacion de variables.
- [ ] Definir dataset principal, dataset proxy y benchmark metodologico.
- [ ] Crear protocolo de validacion de usuarios con n, tareas, rubrica y prueba estadistica.
- [ ] Arreglar todas las claves BibTeX antes de compilar.
- [ ] Instalar Pandoc o definir flujo alternativo para validar citas APA.

## 7. Dictamen final

La fase base es prometedora, pero todavia no debe presentarse como "lista". Esta en un punto bueno para una defensa de planteamiento si se corrigen las contradicciones centrales. La tesis sera mucho mas fuerte si deja de intentar probar todo a la vez y se concentra en una afirmacion defendible:

> La integracion trazable de modelos predictivos, deteccion de anomalias, explicabilidad y reportes mejora la supervision operativa frente a componentes aislados.

Esa es la columna vertebral. Todo lo demas debe servir a esa frase.
