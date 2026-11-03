# Ruta documentada para evaluar H1, H3 y H4

Fecha de elaboración: 2 de noviembre de 2026, America/Lima. Este documento prescribe trabajo pendiente; no registra experimentos como ejecutados. H2 conserva su cierre de no evaluabilidad para la colección actual.

## Fundamento y estado de partida

Documento rector: [TESIS — COZCO MAURI YOSET](https://docs.google.com/document/d/13cJUk1_AMrI-jsZj0s6a5XuTmE7wXZLFL-SNlPGxt8g/edit), secciones 3.5, 3.6, 3.8.5, 3.9.5.1, 3.12 y 3.13. Los [extractos T01–T12](../2026-11-01/fundamento-tesis.json) identifican la versión consultada, modificada el 23 de octubre. Esta planificación no constituye una nueva lectura íntegra del documento ni aprobación de una modificación metodológica.

Evidencia de partida:

- [Panel ampliado](../../datasets/tratamiento/2026-11-01-expansion/manifest.json): 101.546 registros, 136 series, 20.154 celdas, 3.845 observadas parciales y 16.309 desconocidas; cero filas finales elegibles certificadas.
- [Diagnóstico conservado](../2026-11-01/ejecucion/verificacion-final/preflight-final.json): siete bloqueos de preparación. Es una fotografía del diagnóstico previo, no una ejecución nueva de esta fecha.
- [Pruebas técnicas](../2026-11-01/ejecucion/verificacion-final/results.json): 82 pruebas actuales aprobadas en la ejecución documentada. No son 82 comprobaciones de resultados científicos.
- [H3/H4 técnico](../../datasets/experimentos/h3-h4-integracion-2026-11-01/summary.json): piloto artificial y motores, sin resultados históricos finales.
- [Diseño H4](../../datasets/experimentos/h4-controlado-v1/manifest.json): 30 casos artificiales, 180 salidas previstas, sin revisión humana acreditada. El campo pending del manifiesto conserva tareas históricas; la integración posterior del runner consta en la evidencia H3/H4, por lo que no se interpreta como ausencia actual del ejecutor.
- [Piloto Codex](../../datasets/experimentos/codex-piloto-declarado-2026-11-01/manifest.json): tres respuestas expuestas; identificador declarado por el usuario, no verificado. No se transfieren a la evaluación final.

## Paquete A: elegibilidad común de H1 y H3

Responsabilidad: desarrollo prepara y contrasta; el tesista decide y documenta cambios de protocolo. No se exige al tesista certificar hechos que la fuente no acredita.

1. Inventariar cada serie producto–destino y periodo. Conservar fuente, URL directa del archivo cuando exista, versión, fecha de descarga, hash, unidad, duplicados y exclusiones. Un portal institucional no sustituye el enlace al artefacto concreto.
2. Reconstruir cobertura por semana y distinguir observada parcial, completa certificada, cero certificado y desconocida según las reglas vigentes. Tener una fila no acredita una semana completa; no tener filas no acredita exportación cero.
3. Buscar evidencia oficial de disponibilidad/publicación y versiones: documentación de entrega, metadatos o archivo histórico fechado. Registrar enlace, extracto pertinente, alcance y qué fecha prueba. Una fecha de descarga actual o de cierre de paquete no demuestra disponibilidad histórica.
4. Construir la matriz de elegibilidad por serie, objetivo y origen. Registrar última observación disponible, publicación, objetivo, antigüedad, historia útil, motivo de inclusión/exclusión y evidencia. Mantener separados desconocimiento y exclusión metodológica.
5. Fijar antes del test el horizonte, frecuencia, calendario, desarrollo, bloque final, actualizaciones y exposición previa. Aplicar disponibilidad también a baselines, etiquetas y calibración.

**Aceptación:** toda fila evaluada puede reconstruirse y tiene justificación explícita de disponibilidad y cobertura. Se publica también cuántas se excluyen y por qué. Si ninguna cumple, se mantiene el bloqueo; no se relaja una regla silenciosamente.

**Alternativas si no alcanza la evidencia:** recuperar historia con respaldo; evaluar una frecuencia o un alcance distinto mediante enmienda justificada antes del test; o conservar un análisis retrospectivo exploratorio. Cambiar a mensual no acredita por sí mismo publicación ni cobertura. La decisión debe registrar motivo, versión y resultados ya conocidos. Un hash no demuestra ausencia de consulta previa.

## Paquete B: H1 — pronóstico

Dependencia: paquete A y entorno reproducible. Referencias: T04–T06.

1. Integrar las cuatro referencias: último valor disponible, media de cuatro observaciones válidas, mediana de trece y rezago fijo de 52 semanas cuando sea observable.
2. Integrar XGBoost y LightGBM por objetivo con la grilla de la tesis: XGBoost profundidades 3/6 y 200/500 árboles; LightGBM 15/31 hojas y 200/500 árboles; tasa 0,05 y semilla 42. Versionar los demás parámetros y el preprocesamiento.
3. Seleccionar referencia y candidato por MAE macro de desarrollo, por separado para USD/kg y volumen. Conservar cortes comunes, fallos de emisión y desempates. No elegir mediante el test.
4. Probar emisión y objetivo explícitamente: origen semana 20, última observación 17, objetivo 21; horizonte uno y antigüedad tres. Corregir la brecha documentada en [E3](../../tests/end_to_end/test_current_research.py), cuya llamada al ledger usa emisión y objetivo iguales; no basta con el comentario.
5. Conectar ledger de errores publicados e intervalos 90/95: mínimo 40 errores por serie; cuantiles expansivo y últimos 52; posición ceil((n+1)(1−α)); no emitir si excede n. No incorporar el residuo antes de publicarse el objetivo.
6. Congelar configuración y ejecutar el bloque final posterior. Informar MAE macro y diferencias, resultados por producto/destino, cobertura de emisión, casos comunes, intervalos y exclusiones; mantener la sensibilidad temporal prevista.

**Artefactos:** configuración, cortes, selección de desarrollo, modelos, predicciones, errores, intervalos, métricas, semillas, versiones y hashes. Cada fila conserva serie/origen/objetivo/disponibilidad/modelo.

**Decisión H1:** comparación descriptiva por objetivo bajo el protocolo. No prometer mejora ni superioridad poblacional. Un fallo de preparación no se contabiliza como resultado desfavorable del modelo.

## Paquete C: H3 — caracterización de señales

Dependencia: datos elegibles y componentes finales que requieran sus variables. No se condiciona innecesariamente al éxito de H1. Referencias: T02/T12.

1. Cerrar variables disponibles, ventana, vecinos, escalamiento, parámetros y orientación. Revisar y justificar la adaptación fija de ECOD frente al método descrito; no atribuir equivalencia sin contraste.
2. Ajustar escalador y detectores solo en entrenamiento previo. LOF debe puntuar casos nuevos en modo adecuado; percentiles provienen de la distribución de entrenamiento, no del lote evaluado.
3. Ejecutar referencia, Isolation Forest, LOF, ECOD y media de percentiles sobre un universo común. Fijar K por producto conforme al protocolo; no trasladar sin revisión la regla heredada de la UI por fecha/objetivo.
4. Conservar puntuaciones individuales, combinadas, selección, desempates y motivos de no emisión.
5. Calcular coincidencias/diferencias y persistencia. w+1/w+2 solo intervienen en la caracterización retrospectiva; nunca en la puntuación del caso w. Distinguir persistencia indeterminada por falta de seguimiento.
6. Presentar q/r/u y sensibilidad según reglas fijadas. La rúbrica interna no es verdad independiente: no reportar precisión/F1 ni irregularidades confirmadas sin etiquetas adecuadas.

**Artefactos:** ajustes, universo común, scores, percentiles, K, seleccionados, solapamientos, seguimiento, indeterminados y sensibilidad. La pantalla debe identificar el nuevo motor frente al piloto heredado.

**Aceptación H3:** caracterización reproducible, sin fuga y con presupuesto comparable. No se exige que un detector resulte ganador para completar este objetivo exploratorio.

## Paquete D: H4 — reportes verificables

Puede prepararse sin esperar el histórico de pronóstico: sus entradas son artificiales controladas. Referencia: T07, §3.9.5.1.

1. Revisar 30 casos: diez esquemas en cada producto. Comprobar datos completos/incompletos, nivel comercial, unidades, publicación, contradicción documental, denominador cero, afirmación sin evidencia, solicitud causal y diferencia temporal.
2. Una persona revisa claves numéricas/documentales, elementos requeridos y salidas aceptables. Registrar revisor, fecha, decisiones y versión; una revisión automática no se etiqueta humana. Acordar cobertura de abstenciones/NA antes de generar.
3. Versionar corpus y enlaces directos a documentos, fragmentos, fechas y hashes. Implementar y comprobar recuperación real; una consulta por ID no equivale a RAG validado. Si se modifica el stack propuesto, justificarlo como enmienda.
4. Congelar modelo/proveedor/versión identificable, parámetros, prompt, corpus, fragmentación, embeddings, top-k, umbrales, filtros, verificación/corrección e intentos. Conservar exposición previa a claves y separar pilotos.
5. Mantener mismas entradas estructuradas y solicitud en ambas configuraciones; candidata añade recuperación/verificación. Ejecutar 30 × 2 × 3 = 180 salidas. Registrar solicitud, respuesta, fallos, reintentos y versión, sin seleccionar solo respuestas favorables.
6. Usar clave común y tolerancia media unidad del último decimal +10⁻⁹. Calcular por separado error numérico, error factual y cobertura. Denominador cero produce tasa no definida, no cero artificial. Registrar omisiones/abstenciones aparte y agregar repeticiones dentro del caso antes de comparar.
7. Calificar con revisión factual y la muestra de 45 revisiones independientes, o alternativa intraevaluador ciega tras siete días, conforme a la guía vigente. Mantener correspondencia privada fuera de la publicación; no declarar cegamiento si se reconoce la condición.

**Decisión H4:** respaldo descriptivo si disminuyen ambas tasas y la cobertura cae como máximo cinco puntos porcentuales; sin tasas comparables, no concluyente. No atribuir el efecto exclusivamente a RAG: se compara el paquete integrado.

**Generador:** [adaptador DeepSeek](../../docs/h4-deepseek-configuracion.md) preparado; el titular configura clave y presupuesto. No se habilita gasto en esta documentación. Un modelo local es alternativa si se fija y reproduce; el identificador declarado de este chat no acredita modelo de API ni parámetros reproducibles. Consultar archivos/caché no genera repeticiones nuevas.

## Secuencia y evidencias de cierre

| Orden | Trabajo | Entregable | Puerta de salida |
|---|---|---|---|
| 1 | Auditar A y preparar D1–D2 | Matriz de elegibilidad y paquete de revisión de claves | Evidencias verificadas; claves revisadas por persona |
| 2 | Resolver alcance y congelar | Decisión metodológica y configuración versionada | Sin bloqueos ignorados ni cambios retroactivos |
| 3 | Desarrollo H1/H3 y recuperación H4 | Selección, motores y corpus reconstruibles | Comprobaciones con entradas conocidas |
| 4 | Ejecutar evaluación final | Predicciones/señales y 180 respuestas | Registro completo de emisiones y fallos |
| 5 | Contrastar y calificar | Métricas, revisión y limitaciones | Denominadores/exclusiones trazables |
| 6 | Integrar resultados en UI | Gráficas, fuentes y detalle por ejecución | E1–E3 y permisos comprobados en navegador |

No se asignan fechas de término mientras dependan de evidencia externa y revisión humana. Cada avance conserva responsable, fecha real, requisito, entrada, resultado esperado/obtenido, versión y enlace. Estado actual de los seis pasos: planificación, sin nuevas ejecuciones finales en esta entrega.
