# Revisión detallada y propuesta de corrección de la tesis

Yoset Cozco Mauri · Revisión del 25 de septiembre de 2026

## Decisión de enfoque y título oficial

**Título adoptado:** *Sistema de información y pronóstico de mercados agroexportadores para la evaluación de escenarios comerciales de palta, uva fresca y arándano.*

Esta decisión reemplaza el encuadre centrado exclusivamente en un productor–acopiador y en el monitoreo semanal de alertas. La tesis se plantea como un sistema de apoyo al análisis de mercados agroexportadores: integra indicadores de exportación, pronósticos, evidencia trazable y escenarios comerciales parametrizables. El productor–acopiador sigue siendo un perfil de usuario relevante, pero comparte el alcance con productores, exportadores y vendedores de grandes volúmenes.

El sistema no promete ganancias, fija precios de compra ni recomienda cambiar de cultivo. Permite comparar escenarios bajo supuestos explícitos de precio, volumen, costos, merma, moneda y periodo; sus resultados son referencias para análisis e inversión y deben verificarse con información local, agronómica, contractual y financiera. La eventual decisión de cambiar de cultivo queda como proyección futura porque requiere rendimiento, costos de instalación, riesgo productivo y horizonte de campaña.

**Pregunta rectora reformulada:** ¿qué desempeño predictivo y utilidad para el análisis comercial ofrece un sistema que integra información agroexportadora, pronósticos y evaluación de escenarios de palta, uva fresca y arándano?

**Objetivo rector reformulado:** desarrollar y evaluar un sistema de información y pronóstico de mercados agroexportadores que permita interpretar indicadores comerciales y explorar escenarios económicos como apoyo al análisis de inversión y comercialización.

## 1. Dictamen y alcance de esta revisión

La tesis tiene un núcleo defendible: integrar información de exportaciones, pronosticar indicadores por producto y destino, y presentar evidencia trazable para explorar escenarios comerciales. El problema principal no es agregar más algoritmos, sino alinear objetivos, comparaciones experimentales, datos disponibles, supuestos económicos y utilidad para distintos perfiles de usuario. La participación de un productor–acopiador mejora la pertinencia del trabajo si se presenta como evaluación de dominio y de uso, no como prueba automática de precisión o rentabilidad.

Este informe contiene correcciones propuestas; **no es un dictamen firmado por un experto externo ni certifica que los experimentos se hayan ejecutado**. No se modificó la tesis ni se reorganizó Drive. La revisión de formato se basa en la estructura nativa y el texto; no se verificaron visualmente todas las páginas de un PDF final.

Documentos contrastados:

- [Tesis en Google Docs](https://docs.google.com/document/d/13cJUk1_AMrI-jsZj0s6a5XuTmE7wXZLFL-SNlPGxt8g/edit), modificada el 18/09/2026, 13:04:51 UTC.
- [Tesis DOCX en Anexos](https://drive.google.com/file/d/1IhFLpr1gprxI0FZNU3cu16xW2zeBmM52/view), modificada el 18/09/2026, 13:07:18 UTC: es la copia de tesis más reciente por modificación entre las identificadas. Los 366 párrafos de más de 120 caracteres extraídos del Google Doc aparecen también en este DOCX al normalizar espacios; esto respalda aplicar los hallazgos de contenido a ambas copias, pero no certifica igualdad de formato.
- [Enunciado de evaluación 2026-B](https://drive.google.com/file/d/1Cmr9lJFfBeyiZy9cmiqExXQ_KI3rF_0V/view).
- [Anexo de fuentes y herramientas](https://drive.google.com/file/d/1th6rowJ-SxC1BxixIp_DpO8Hx0x6CBSd/view).
- [Cronograma ampliado](https://drive.google.com/file/d/15_KoU1gF9uaYmyR-NSiHmWwnE6SxOtu0/view).

Documentos complementarios preparados: [auditoría de referencias](C:/Users/LENOVO/Documents/tesis_yoset/auditoria_referencias_2026-09-25.md) y [protocolo de consulta y evaluación](C:/Users/LENOVO/Documents/tesis_yoset/protocolo_experto_productor_acopiador.md).

## 2. Correcciones prioritarias y ubicación

| Prioridad | Ubicación identificable | Hallazgo | Corrección y evidencia de cierre |
|---|---|---|---|
| Crítica | 1.5, variables independientes | BASE e INTEGRADA presentan los mismos resultados técnicos, pero H1–H3 comparan modelos y detectores. | Separar factores experimentales; una interfaz no explica una mejora predictiva si recibe las mismas predicciones. Tabla propuesta en §5. |
| Crítica | 3.6–3.7, preparación y pronóstico | Se declara walk-forward, pero falta fijar calendario experimental verificable. | Registrar fechas de entrenamiento, validación y prueba; origen de cada predicción; selección de modelos únicamente en validación. |
| Crítica | 3.2.2, auditoría de datos | Los 40 289 registros válidos incluyen 2 599 de espárrago. | Documentar filtro final de tres productos. La resta da 37 690 registros antes de cualquier filtro adicional; no presentarlos como muestra final ya auditada. Recalcular las 8 340 filas semanales y 139/170 variables. |
| Crítica | 2.1.1, 2.1.2, 2.1.3 y referencias | Hay antecedentes mal atribuidos y afirmaciones que exceden la evidencia. | Corregir autores, contenido y alcance; retirar resultados no respaldados. Véase auditoría bibliográfica. |
| Alta | Portada y anexos | El DOCX dice «Dra .KARIM GUEVARA PUENTE DE LA VEGA»; anexos de fuentes y cronograma dicen «Ing. Jesus Heraclio Zuñiga». | Confirmar quién es asesor vigente; si son funciones diferentes, nombrarlas expresamente. No elegir ni reemplazar un nombre por inferencia. |
| Alta | 3.1.3, usuarios y actores | Predominan Administrador y Auditor y el texto reduce el uso comercial al productor–acopiador. | Incorporar perfiles de productor, acopiador, exportador y vendedor de grandes volúmenes; distinguir apoyo comercial de auditoría financiera y no afirmar que un rol ya está implementado. |
| Alta | 1.4, 1.11 y evaluación con usuarios | La evaluación humana es condicional, pero algunas descripciones la presentan como diseño ya establecido. | Mantener una misma condición en objetivos, diseño, cronograma y resultados: consulta sectorial prevista; ejecución y alcance sujetos a evidencia real. |
| Alta | Anexos | El enunciado exige al experto/especialista consultado; no se identificó un anexo independiente que documente esa consulta. | Incorporar perfil, consentimiento, instrumento, respuestas, observaciones y cambios. Una ficha vacía no equivale a consulta ejecutada. |
| Alta | Capítulo IV y secciones finales | El cuerpo extraído llega al título del capítulo IV y pasa a referencias; no contiene resultados desarrollados. | Completar con salidas reproducibles. Si es entrega de propuesta, indicar expresamente qué está pendiente; no redactar resultados ficticios. |
| Alta | Capítulo III, estilos | En Google Docs hay párrafos completos de prosa y pies de figura con estilo Título 1. | Corregir semántica de estilos, después regenerar índices y revisar paginación. No basta disminuir el tamaño de letra. |
| Media | Cronograma del cuerpo y anexo 3 | El cuerpo no desarrolla todas las fases, pero el anexo sí contiene F1–F15 hasta el 10/12. Estados y fechas pasadas requieren actualización. | Sincronizar una única planificación con productos verificables; no afirmar que faltan F9–F12 en todo el expediente. |
| Media | Resumen, abstract, introducción e índices | Se observan apartados sin desarrollar y entradas de índice incompletas. | Completar cuando estén cerrados alcance y resultados; usar «Keywords» y «fórmulas»; eliminar puntos suspensivos de títulos definitivos. |
| Media | Capturas, arquitectura y herramientas | Hay «versión y fecha por completar»; Flask figura como heredado y FastAPI/Uvicorn como incorporación progresiva. | Registrar versión real de cada captura y componente; separar implementado, heredado, planificado y evaluado. |

## 3. Perfiles de usuario y alcance comercial

El productor–acopiador es un perfil de usuario, no el destinatario exclusivo ni el objeto completo de la tesis. Produce fruta, compra a otros productores y comercializa para destinos locales, nacionales o vinculados a exportación. No corresponde llamarlo importador mayorista del país de destino ni suponer que exporta directamente: puede vender a una empresa exportadora. Los demás perfiles pueden interpretar los mismos indicadores desde decisiones diferentes.

| Perfil | Decisiones que podría apoyar el sistema | Información que debe complementar el usuario |
|---|---|---|
| Productor | Orientación de campaña, ventanas comerciales y lectura de demanda externa. | Rendimiento esperado, costos, calidad, agua, mano de obra y riesgo productivo. |
| Productor–acopiador | Comparación de compra a terceros, venta local y canal exportador bajo escenarios. | Existencias, calidad, capacidad, mermas, transporte, contratos y precios efectivamente negociados. |
| Exportador | Exploración de destinos, periodos y supuestos de volumen/precio. | Pedidos, costos logísticos, aranceles, certificaciones, clientes y condiciones de pago. |
| Vendedor de grandes volúmenes | Comparación de alternativas de comercialización y sensibilidad del margen. | Precio real de compra/venta, rotación, financiamiento, pérdidas y costos operativos. |

### 3.1 Alcance recomendable para esta tesis

Mantener como resultados del modelo el volumen exportado y el valor unitario FOB por producto–destino–semana. Evaluar con el productor–acopiador si esas señales sirven para contextualizar la planificación comercial, identificar información que debe verificar y entender situaciones atípicas.

| Resultado o necesidad | Qué puede sostenerse con el alcance actual | Qué falta para ir más allá |
|---|---|---|
| Volumen exportado semanal | Pronóstico del agregado de exportaciones al destino estudiado. | No equivale a pedidos, ventas o capacidad de acopio del participante. |
| Valor unitario FOB | Indicador agregado calculado como suma de FOB / suma de kg. | No equivale al precio en chacra, precio mayorista local o pago neto al productor. |
| Alerta | Señal estadística para revisión de datos y contexto. | No demuestra fraude, pérdida comercial, escasez ni causa climática. |
| Escenario de acopio o venta | Puede evaluarse la comprensión y utilidad de comparar supuestos de precio, volumen, costos y merma. | No recomienda cantidades óptimas sin pedidos, existencias, cosecha, calidades, capacidad y restricciones reales. |
| Elección entre venta local y exportadora | Puede identificarse qué información considera el participante. | Para comparar márgenes se necesitan precios comparables, costos, mermas, plazos, requisitos y condiciones contractuales. |
| Producción y cosecha | Se puede consultar si el horizonte semanal es útil para alguna decisión. | La planificación productiva de campaña exige otros horizontes; no se deriva automáticamente del pronóstico a una semana. |

Un aumento del valor unitario agregado también puede reflejar cambios de variedad, calibre, calidad o composición de compradores. No debe traducirse mecánicamente en «la fruta se pagará más al productor». El productor–acopiador puede ayudar precisamente a detectar esas interpretaciones peligrosas.

### 3.2 Ampliación futura al mercado local

Si se decide pronosticar precios locales, eso constituye una ampliación metodológica, no un cambio de etiqueta en la interfaz. Antes de incorporarla hay que comprobar disponibilidad histórica por producto, variedad, calidad, mercado, unidad y fecha. MIDAGRI publica información de precios y volúmenes mayoristas y remite a SISAP, pero ello no garantiza cobertura utilizable para los tres productos, la zona o el precio en chacra de un usuario. [Fuente oficial](https://www.gob.pe/institucion/midagri/informes-publicaciones/1211-boletin-de-precios-diarios-de-alimentos).

### 3.3 Módulo de escenarios comerciales

El módulo debe tratar el precio de compra, precio de venta, volumen, costos, merma, tipo de cambio y periodo como supuestos editables o como datos de referencia identificados. Para cada escenario se puede calcular, por ejemplo:

**Ingreso estimado = volumen comercializable × precio de venta.**

**Costo estimado = volumen adquirido × precio de compra + costos operativos + costos logísticos + otros costos declarados.**

**Resultado estimado = ingreso estimado − costo estimado − efecto de la merma.**

La pantalla y el informe deben distinguir datos observados, pronósticos y supuestos del usuario. No debe llamarse «ganancia garantizada» ni «precio probable de compra» cuando el valor sea solo una entrada del escenario. Las comparaciones de sensibilidad —por ejemplo, precio bajo, central y alto— son más defendibles que una única cifra puntual. Si no se dispone de costos reales, el resultado debe rotularse como simulación referencial.

La unidad podría pasar a producto–variedad/calidad–mercado–semana; los precios en soles y los FOB en dólares seguirían siendo objetivos distintos. Habría que modificar problemas, objetivos, variables, fuentes, baselines y evaluación. Recomiendo dejar esta ampliación como proyección hasta comprobar los datos y acordarla con el asesor.

## 4. Reestructuración alineada con el enunciado

Conservar el esquema de capítulos de la tesis y ajustar el capítulo I al enunciado proporcionado, sin sustituirlo por una estructura genérica de otra universidad.

### Capítulo I: planteamiento del problema

1.1 Descripción de la realidad problemática: sector, información disponible, limitaciones analíticas y necesidad concreta del usuario.

1.2 Problema principal y problemas específicos.

1.3 Objetivos: general y específicos.

1.4 Hipótesis: separar contrastes técnicos de preguntas exploratorias con el usuario.

1.5 Variables: factores, resultados, indicadores y controles por experimento.

1.6 Viabilidad técnica, operativa y económica: incluir disponibilidad real del participante, no solo herramientas.

1.7 Justificación: por qué el trabajo es necesario y qué vacío aborda.

1.8 Importancia: contribución técnica y utilidad potencial, sin repetir literalmente la justificación.

1.9 Alcance y limitaciones: tres productos, destinos y periodo efectivo; exclusión de precios locales y optimización comercial si no se modelan.

1.10 Tipo, línea y nivel de investigación: alineados con el anexo de especialidad y criterio del asesor.

1.11 Diseño de investigación: evaluación temporal del artefacto, comparaciones controladas y estudio exploratorio del caso de uso.

1.12 Técnicas: análisis documental, experimentación temporal, revisión de casos y entrevista.

1.13 Instrumentos: scripts y configuraciones, fichas de datos, rúbricas, guía de entrevista y registro de tareas. Una biblioteca no reemplaza la descripción del instrumento.

1.14 Cronograma: sincronizado con el anexo hasta el 10 de diciembre.

### Capítulo II: marco teórico

- **2.1 Antecedentes:** primero información de mercados agroexportadores y pronóstico de precios, volumen o valor; después antecedentes peruanos, forecasting tabular, escenarios/sensibilidad, anomalías, explicabilidad y reportes. Cada ficha debe indicar problema, datos, método, validación, resultado, limitación y aporte específico.
- **2.2 Estado del arte:** comparar alternativas, no repetir resúmenes. Distinguir evidencia de regresión temporal, clasificación de fraude y detección no supervisada. Justificar selección de candidatos, no superioridad anticipada.
- **2.3 Marco conceptual:** producto–destino–semana ISO, volumen, valor unitario FOB, precio local, costos, merma, ingreso, margen/resultado estimado, punto de equilibrio, escenarios, sensibilidad, incertidumbre, rezagos, disponibilidad temporal, desviación, score, umbral, SHAP, recuperación, fidelidad y trazabilidad. Relacionarlo con el diccionario anexo.

El artículo peruano de Carrión-Mezones y colaboradores ya figura al final de las referencias, pero debe incorporarse al análisis de antecedentes. Estudia exportaciones de arándano con métodos de series temporales; es más cercano al dominio que los artículos de fraude contable, aunque su escala mensual no valida el desempeño semanal de esta tesis. [Artículo](https://doi.org/10.3390/su18094529).

### Capítulo III: metodología e implementación

Orden propuesto: 3.1 diseño y unidad de análisis; 3.2 datos, cobertura y calidad; 3.3 preparación temporal; 3.4 protocolo experimental; 3.5 modelos de pronóstico; 3.6 detección y calibración; 3.7 explicabilidad; 3.8 simulación de escenarios comerciales; 3.9 evidencia documental y reportes; 3.10 arquitectura e implementación; 3.11 evaluación técnica; 3.12 consulta experta y evaluación exploratoria; 3.13 reproducibilidad, privacidad y limitaciones operativas.

Se pueden conservar subapartados actuales y trasladarlos a estos bloques. Diferenciar **cómo se evaluará** del **resultado obtenido**: el primero pertenece aquí; las métricas y hallazgos definitivos, al capítulo IV.

### Capítulo IV y cierre

4.1 Datos finalmente utilizados y exclusiones; 4.2 indicadores de mercado; 4.3 pronóstico por objetivo/producto/destino; 4.4 ablación de variables contextuales; 4.5 escenarios, sensibilidad y supuestos; 4.6 detección bajo carga comparable; 4.7 fidelidad de reportes y trazabilidad; 4.8 evaluación con perfiles de usuario; 4.9 discusión, límites y amenazas a la validez.

Mantener conclusiones y recomendaciones conforme a la plantilla institucional. Una conclusión por objetivo, con su evidencia, y sin presentar una apreciación comercial como mejora estadística del modelo.

## 5. Corrección del diseño experimental

| Bloque | Factor que realmente cambia | Qué debe mantenerse comparable | Resultado principal propuesto |
|---|---|---|---|
| Pronóstico | Baseline / XGBoost / LightGBM | Fechas, datos disponibles, horizonte y series elegibles | MAE por objetivo; RMSE u otra métrica secundaria justificada. |
| Contexto | Historial solamente / historial + covariables | Modelo o presupuesto de ajuste y mismo calendario | Diferencia de error fuera de muestra. |
| Detección | Umbral de referencia / IF / LOF / ECOD / combinación | Periodo, etiquetas de referencia y presupuesto de alertas | Precisión entre alertas revisadas; métricas adicionales solo con etiquetas adecuadas. |
| Reportes | Sin recuperación ni verificador / con recuperación / con recuperación y verificador | Casos, datos numéricos, modelo generativo y reglas de comparación | Errores numéricos y afirmaciones sin respaldo; cobertura de información requerida. |
| Interfaz | Vista básica / vista integrada | Predicciones y casos de dificultad comparable | Comprensión observada, tiempo, errores y utilidad percibida. |
| Trazabilidad | Requisito verificable, no una hipótesis de superioridad | Mismo artefacto y procedimiento de reconstrucción | Casos reconstruibles / casos auditados, con fallos detallados. |

La vista integrada cambia un conjunto de funciones. Si incluye a la vez SHAP, RAG y linaje, no permite atribuir la mejora exclusivamente a SHAP. Para separar contribuciones harían falta comparaciones adicionales, que no conviene prometer si no se ejecutarán.

### Hipótesis y preguntas reformuladas

Las siguientes formulaciones son propuestas a cerrar antes de consultar el conjunto de prueba. Deben fijarse métrica, agregación y calendario; no modificar esas reglas para favorecer resultados ya conocidos.

- **H1 — pronóstico:** el candidato seleccionado mediante validación temporal alcanza menor MAE macro por serie que el baseline seleccionado con el mismo procedimiento, en el periodo de prueba reservado. Contrastar por separado volumen y valor unitario FOB; mejorar uno no implica mejorar ambos. Definir previamente cómo se tratan series no elegibles y qué mejora se considera relevante en la práctica.
- **H2 — aporte contextual:** bajo el mismo calendario y reglas de ajuste, la configuración con variables contextuales disponibles en el origen del pronóstico obtiene menor error que la configuración basada solo en historial de exportaciones. Si no hay variables compatibles o disponibilidad verificable, documentar que la hipótesis no pudo evaluarse.
- **H3 — alertas:** a igual presupuesto de alertas, el detector seleccionado en validación alcanza mayor precisión en el conjunto de alertas de prueba revisadas mediante un procedimiento independiente que la regla histórica de referencia. Esta formulación mide precisión de alertas, no sensibilidad global. Para afirmar F1, PR-AUC o detección de todos los eventos se necesita un conjunto etiquetado con cobertura suficiente de alertados y no alertados.
- **H4 — reportes:** para los mismos casos de prueba, la configuración con recuperación y verificación presenta menor proporción de errores numéricos y de afirmaciones sin respaldo que la configuración de referencia. Evaluar también cobertura de los campos y hechos requeridos para evitar que un reporte vacío resulte artificialmente mejor. Registrar abstenciones justificadas por separado.
- **Pregunta exploratoria — usuario:** ¿qué resultados comprende correctamente el productor–acopiador, qué utilidad identifica y qué restricciones impiden emplearlos en sus decisiones? No formular una hipótesis de aumento de ganancias si no se observa ni diseña ese resultado.

Si se aplican contrastes estadísticos, definir una hipótesis nula y alternativa por resultado y un plan de inferencia que respete dependencia temporal. Si no se dispone de ese diseño, informar diferencias e incertidumbre de manera descriptiva y no hablar de «diferencias significativas». La trazabilidad permanece como requisito de aceptación verificable.

### Controles mínimos antes de medir

1. **Disponibilidad real:** registrar cuándo se publica cada dato, no solo cuándo ocurrió la exportación. Si llega con retraso, el origen del pronóstico y el horizonte útil deben reflejarlo. Una alerta basada en el residuo solo puede emitirse cuando ya se conoce la observación; no es una predicción anticipada de esa anomalía.
2. **Separación temporal:** ajustar imputación, escalado, codificación, selección de variables, normalización de scores y umbrales sin consultar el periodo final. Seleccionar candidatos en validación y congelar reglas antes de prueba. Las predicciones históricas usadas como residuos también deben proceder de modelos entrenados solo con pasado.
3. **Calendario y cobertura:** declarar primeras/últimas semanas, series por destino, semanas sin datos, semanas ISO 53 y mínimos de historia. No confundir ausencia de exportación con registro faltante.
4. **FOB y ceros:** calcular el cociente de sumas, no media simple de precios de operaciones. Cuando kg = 0, el valor unitario no está definido; no rellenarlo automáticamente con cero. Evaluar volumen y valor unitario sobre conjuntos elegibles explícitos.
5. **Métricas:** no sumar errores de kg y USD/kg. Reportar resultados por serie y agregados macro; documentar cualquier ponderación. SMAPE, MAPE y escalados necesitan reglas para ceros y series constantes.
6. **Detectores:** justificar pesos 0,45/0,30/0,25 y umbral 0,65 mediante validación o tratarlos como configuración preliminar. El score no es una probabilidad de fraude. Comprobar cómo la implementación concreta de LOF/ECOD trata datos nuevos y si una muestra futura modifica la puntuación de semanas anteriores.
7. **Referencia de anomalías:** separar errores de dato, cambios esperables por campaña, eventos comerciales documentados y anomalías sintéticas. No entrenar o evaluar con etiquetas derivadas del mismo detector y llamarlas verdad independiente.
8. **Inferencia:** si se usan intervalos o contrastes, respetar dependencia temporal y entre series; no tratar cada semana o cada clic del mismo usuario como participante independiente. No rechazar H0 no demuestra equivalencia.
9. **Explicación:** SHAP explica contribuciones al predictor especificado; no prueba causas comerciales ni necesariamente explica directamente la puntuación de otro detector.
10. **RAG:** evaluar exactitud de las cifras, respaldo de cada afirmación, adecuación temporal de documentos y abstención. Un texto recuperado sobre una plaga no prueba que esa plaga causó una desviación concreta. BLEU/ROUGE no sustituyen fidelidad factual. ALCE aporta un referente para evaluar citas, pero requiere adaptación al caso. [ALCE](https://aclanthology.org/2023.emnlp-main.398/).

La recomendación de separar selección y prueba temporal coincide con las advertencias metodológicas de Hewamalage y colaboradores; el protocolo concreto anterior es una propuesta para esta tesis. [Fuente](https://doi.org/10.1007/s10618-022-00894-5).

## 6. Textos propuestos para incorporar

Los siguientes párrafos son propuestas de redacción, no evidencia de actividades ya realizadas.

### 6.1 Problema principal

¿Qué desempeño predictivo, capacidad de integrar información trazable y utilidad para evaluar escenarios comerciales alcanza un sistema de información y pronóstico de mercados agroexportadores de palta, uva fresca y arándano, y qué limitaciones identifican sus distintos perfiles de usuario al interpretar sus resultados?

### 6.2 Objetivo general

Desarrollar y evaluar un sistema de información y pronóstico de mercados agroexportadores de palta, uva fresca y arándano que integre indicadores comerciales, pronósticos, simulación de escenarios y reportes respaldados por evidencia, para apoyar el análisis de inversión y comercialización de productores, productores–acopiadores, exportadores y vendedores de grandes volúmenes.

### 6.3 Objetivo específico de evaluación humana

Evaluar de manera exploratoria, mediante revisión de casos y tareas de interpretación, la comprensión de los indicadores, pronósticos, escenarios y alertas, así como su utilidad y limitaciones para perfiles de productor, productor–acopiador, exportador y vendedor de grandes volúmenes, diferenciando señales de exportación de precios y condiciones del mercado local.

Conservar los objetivos actuales de datos, pronóstico, detección, explicabilidad y reportes, pero evitar duplicar este objetivo con el cierre actual de OE6. Su inclusión formal exige mantener coherentes viabilidad, instrumentos y calendario.

### 6.4 Usuario y alcance

Los usuarios potenciales de dominio son productores, productores–acopiadores, exportadores y vendedores de grandes volúmenes. Su participación se orienta a valorar la claridad, pertinencia y límites de los resultados y a identificar información adicional requerida para su uso. El sistema puede calcular resultados referenciales bajo supuestos declarados, pero no estima directamente el precio en chacra, garantiza márgenes ni determina cantidades óptimas de compra o venta; sus salidas representan indicadores agregados, pronósticos y simulaciones que requieren interpretación contextual.

### 6.5 Diseño de validación

La evaluación se organizará en cuatro componentes: desempeño técnico fuera de muestra; verificación de la aritmética y transparencia de los escenarios; revisión metodológica por un especialista competente en análisis de datos y sistemas predictivos; y evaluación exploratoria con uno o más perfiles de usuario, incluido el productor–acopiador cuando sea viable. La consulta sectorial examinará pertinencia, comprensión y restricciones de uso mediante un protocolo previamente definido. Sus hallazgos se reportarán como evidencia del caso estudiado y no como validación estadística de toda la población comercial.

Si solo participa el productor–acopiador, no escribir que también hubo revisión metodológica independiente. Registrar ese componente como pendiente o limitar expresamente el alcance.

### 6.6 Antecedentes que necesitan sustitución de texto

**Kadir y colaboradores:** AuditCopilot estudia el uso de modelos de lenguaje para identificar irregularidades en registros de partida doble y compara su funcionamiento con métodos de referencia. Es un antecedente de integración de LLM y análisis de anomalías contables, no evidencia directa de pronóstico agroexportador. Eliminar la reducción de tiempo y la valoración de especialistas hasta localizar mediciones específicas que las respalden; tampoco corresponde afirmar que el trabajo carece de métricas. [Fuente](https://arxiv.org/abs/2512.02726).

**Park:** propone una arquitectura de agentes para investigar y consolidar información sobre anomalías del S&P 500. La demostración sirve como antecedente arquitectónico. La versión consultada no aporta un ensayo comparativo que respalde la afirmación de la tesis sobre una mejora medida de verdaderos positivos frente a un único LLM; reemplazarla por una descripción de la demostración y sus límites. [Texto completo](https://arxiv.org/html/2403.19735v1).

**Sodnomdavaa y Lkhagvadorj:** reemplazar «Mongolia et al.» por los autores. Revisar la composición exacta del ensamble contra el artículo, sin atribuirle CatBoost automáticamente. Sus resultados de clasificación de fraude no demuestran superioridad en regresión temporal agroexportadora. Usar el año de la versión editorial elegida de forma consistente. [Artículo](https://doi.org/10.3390/jrfm19010013).

**PyOD:** el artículo de 2019 describe más de veinte algoritmos; no adjudicarle el número de algoritmos de una versión posterior. Registrar por separado la versión realmente utilizada. [Publicación original](https://www.jmlr.org/papers/v20/19-011.html).

### 6.7 Regla general de escritura

Sustituir «demuestra», «garantiza», «valida» y «optimiza» por formulaciones acordes con la evidencia: «permite examinar», «se evaluará», «se observó en este conjunto» o «se propone». Reservar pasado para implementaciones y pruebas verificables; futuro para trabajo pendiente. Evitar saltos de «datos de exportación» a «producción, inventario, costos y calidad» si esas variables no están efectivamente medidas.

## 7. Formato y organización de archivos

En la estructura nativa se identificaron 286 párrafos Título 1, 14 Título 2 y 12 Título 3. El número por sí solo no prueba error; sí lo prueban ejemplos como la prosa de 3.1.1 y los pies de las figuras 3.1–3.3 marcados como Título 1. Aplicar jerarquía real: capítulo, sección, subsección, texto normal y pie de figura. Después actualizar índices y enlaces internos.

Renumerar «Figura 3.4A» si la norma requiere secuencia única; comprobar que cada figura se mencione en el texto, tenga fuente y corresponda al prototipo real. Revisar tablas, ecuaciones, márgenes, interlineado y saltos en un PDF final. No declarar cumplimiento visual completo con esta extracción textual.

Organización sugerida, **no ejecutada en Drive**:

```text
Tesis/
  00_control/        inventario, decisiones del asesor, registro de versiones
  01_documento/      una tesis maestra y copias fechadas de entrega
  02_anexos/        especialidad; experto; fuentes; cronograma; glosario
  03_bibliografia/   referencias exportables y artículos identificados
  04_evidencias/     métricas, figuras, consultas y trazabilidad
```

Designar una versión maestra. Una exportación DOCX más reciente no debe interpretarse automáticamente como contenido más actualizado. Mantener copias históricas; no borrar los PDF de fraude, pero identificarlos como antecedentes metodológicos y no como centro del dominio agroexportador. No es necesario alterar los nombres actuales de anexos hasta acordar numeración coherente con el enunciado.

## 8. Secuencia de corrección y cierre

1. Confirmar asesor vigente, versión maestra, productos/destinos, perfiles de usuario disponibles y variables para escenarios. Cerrar alcance agroexportador y etiquetar precios locales, cambio de cultivo y optimización como proyecciones si no tienen datos.
2. Corregir referencias mezcladas y antecedentes; alinear problemas, objetivos, factores y evaluación.
3. Congelar datos y calendario experimental. Recalcular muestra, ejecutar controles de disponibilidad y fuga temporal.
4. Ejecutar y guardar resultados técnicos antes de afirmar superioridad. Preparar casos para evaluación humana sin contaminar entrenamiento o prueba.
5. Aplicar consulta y tareas; registrar resultados, desacuerdos y modificaciones. No pedir una firma de conformidad anticipada.
6. Completar capítulo IV, conclusiones y anexos; sincronizar cronograma con avances comprobables.
7. Normalizar formato y bibliografía; exportar y revisar visualmente la versión de entrega antes del 10 de diciembre, según el enunciado.

La tesis estará lista para una revisión final cuando cada resultado tenga datos y configuración identificables, cada referencia problemática esté resuelta o retirada justificadamente, cada sección obligatoria esté desarrollada y la participación del experto se encuentre documentada sin exagerar su alcance.

