# Dictamen de preparación del prototipo — 2026-11-01

## Decisión

**Apto como prototipo para pruebas técnicas controladas y revisión formativa de presentación.** La evidencia disponible no permite declararlo prototipo integral terminado conforme a todas las funciones de la tesis, ni ejecutar y presentar H1/H3/H4 como experimentos finales. No se acredita usabilidad con usuarios mediante pruebas funcionales.

Versión examinada: commit 7f1b103476b2451fd66d6f23ae481ec2a3d3d885. Documento rector conectado consultado en esta revisión: [TESIS - COZCO MAURI YOSET](https://docs.google.com/document/d/13cJUk1_AMrI-jsZj0s6a5XuTmE7wXZLFL-SNlPGxt8g/edit). Modificación comunicada por Drive: 2026-10-23T13:27:20.453Z; texto recuperado: 240011 caracteres. Los requisitos se corresponden con los extractos T01–T12 de fundamento-tesis.json; no se modifica la tesis ni se presume una revisión inmutable.

## Contraste con la tesis

| Requisito | Evidencia contrastada | Estado y prueba admisible |
|---|---|---|
| Fuentes, normalización y trazabilidad (T01/T03) | 24 paquetes; conciliación con 101.546 registros; 108 en cuarentena; manifiestos y hashes | Implementado para la colección auditada. Probar importación/contabilidad e integridad; no confundirlo con cobertura histórica completa. |
| Panel semanal y faltantes (T03/T05) | 20.154 posiciones; 3.845 observadas parciales y 16.309 desconocidas; 136 series | Preparación retrospectiva disponible. Cero filas elegibles finales; no transformar desconocidos en cero ni entrenar como si estuvieran certificadas. |
| Pronóstico H1 y bandas (T04/T05/T06) | Reglas, referencias, grilla, intervalos y ledger con pruebas; preflight mantiene selección y calendario pendientes | Parcial. Se prueban componentes con entradas conocidas; falta selección integrada, artefactos finales y comparación histórica admisible. |
| Contexto H2 (T02) | Dictamen reproducible de no evaluabilidad de la colección actual | Cierre metodológico permitido expresamente por la tesis; no es confirmación ni refutación ni resultado de ablación. |
| Señales H3 (T12) | Motor de cinco métodos; 189 casos artificiales, nueve ajustes y CDF de entrenamiento | Piloto técnico. Faltan datos históricos elegibles, revisión de ECOD adaptado y cadena completa de UI/linaje. |
| Explicaciones SHAP (T01/T08) | P09 continúa pendiente; no se aporta aquí explicación sobre modelo final | No cubierto para aceptación final. Exigir reconstrucción aditiva y enlace a versión de modelo/datos antes de acreditarlo. |
| Evidencia documental y recuperación (T07/T08) | Fixture por ID y transporte preparados; sin reconstrucción real acreditada de PostgreSQL/pgvector/embeddings | Parcial. No presentar fixture como RAG validado. |
| Generación y validación H4 (T07) | 30 casos artificiales; ejecutor pareado; tres respuestas Codex archivadas; cero salidas finales | Piloto expuesto. GPT 6.1 Sol Light es identificación declarada, no verificada. Falta revisión humana de 30 claves, política NA, congelar generador/corpus/recuperación y producir/calificar 180 salidas. |
| Consulta, proceso y exportación (T03/T08) | UI/API del archivo Codex, descarga SHA-256 y siete artefactos de progreso; capturas escritorio/móvil | Cubierto para estos recorridos. Gráficos conservan piloto de 93.225 registros; no representan silenciosamente el panel ampliado. |
| Autenticación, perfil y permisos (T08/T09) | Pruebas API con usuarios QA aislados y acceso autenticado | Acceso básico probado. Perfil/persistencia de consultas, denegación entre dos cuentas/roles y revocación persistente de JWT no quedan acreditados. |
| E1–E3 completos (T08/T11) | Integraciones de componentes y pruebas API; navegador del piloto Codex/proceso | Parcial. No equivale a recorrer E1–E3 de extremo a extremo en navegador con modelos finales. |
| Reproducibilidad (T09) | 82 pruebas actuales aprobadas, 19 comprobaciones de compatibilidad, build y snapshot; tres checks históricos aparte | Verificación técnica reproducible documentada; falta reconstrucción completa en segunda instalación con stack documental/modelos y datos finales. |

## Evidencia y límites de esta revisión

Se contrastaron nuevamente 18 huellas de los manifiestos de progreso, salidas del panel ampliado y preflight: 18 coinciden, cero discrepancias. Los hashes acreditan identidad de bytes, no verdad factual, fecha de publicación ni ausencia de exposición previa. No se repitió toda la suite porque el código no cambió: se revisó results.json de la última ejecución completa, con 82 pruebas, cero fallos/errores/omisiones, 62 núcleo y 20 API. Los tres checks históricos y 19 de compatibilidad se contabilizan aparte. Persisten 44 advertencias API y aviso de tamaño de bundle. La evidencia visual existente es de QA local con SQLite; no prueba PostgreSQL ni usabilidad.

Referencias locales:
- ejecucion/verificacion-final/results.json y preflight-final.json.
- ../../datasets/tratamiento/2026-11-01-expansion/manifest.json.
- ../../datasets/experimentos/h2-cierre-2026-11-01/decision.json.
- ../../datasets/experimentos/h3-h4-integracion-2026-11-01/summary.json.
- ../../datasets/experimentos/codex-piloto-declarado-2026-11-01/verification.json.
- ../../docs/ui-codex-piloto-2026-11-01/README.md.

## Campaña de pruebas que ya puede comenzar

1. Usar cuenta QA y fijar versión de datos en cada caso. Probar autenticación, navegación, filtros y errores sin credenciales reales.
2. Contrastar cálculos conocidos y faltantes: 800/300 = 2,666666… USD/kg; segunda semana 3 USD/kg y cambio 12,5 %; cero denominador no aplicable. Acreditar por separado lo calculado por componentes y lo recorrido realmente por UI.
3. Consultar las tres respuestas archivadas, comprobar abstenciones y procedencia y verificar descarga por SHA-256. Registrar que consultar no crea inferencias ni repeticiones.
4. Contrastar siete artefactos en proceso y mantener identificada la diferencia entre gráficos antiguos y colección ampliada.
5. Registrar por caso: requisito, precondición, entrada, pasos, esperado, obtenido, aprobación/fallo, fecha, versión y captura. Observaciones de claridad son formativas; no una medición de usabilidad.

## Condiciones para aceptar el prototipo integral

Prioridad inmediata: cerrar recorridos E1–E3 completos, dos cuentas/roles, historial reproducible de consulta y exportación. Después integrar pronóstico/señal/SHAP/evidencia con versiones reales y reconstruir recuperación documental. Para H1/H3 resolver certificados de cobertura/publicación y congelar calendario/selección; para H4 revisar claves y congelar protocolo antes de las 180 salidas. Mantener cualquier piloto previamente expuesto separado del experimento final. La clave DeepSeek solo es necesaria si se elige ese transporte para generar, no para estas pruebas funcionales del archivo.

