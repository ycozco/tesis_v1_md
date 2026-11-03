# Revisión de carga del corte — 2026-11-02

El error comunicado no se reprodujo en una nueva carga. GET /research/snapshot.json respondió HTTP 200, application/json, 893.793 bytes, schema_version 1 y 14.683 filas. Señales recargó en navegador sin error; Palta/US/USD-kg/rango inicial no presenta selecciones del piloto. No se interpreta esto como ausencia de anomalías.

Se separó el cargador, se evita caché HTTP y se reintenta una sola vez ante error de red o HTTP 5xx. No se reintenta 404, JSON inválido ni esquema incompatible. Cancelaciones no actualizan un componente desmontado. La UI informa causa específica y enlaza el archivo; nunca fabrica reemplazos.

Cuatro comprobaciones con fetch simulado aprobaron: recuperación tras red transitoria, HTTP 404, esquema inválido y cancelación. Build aprobado; captura senales-carga-2026-11-02.png después de recarga completa. No se atribuye una causa demostrada al error inicial ni se modifican los datos del snapshot.
