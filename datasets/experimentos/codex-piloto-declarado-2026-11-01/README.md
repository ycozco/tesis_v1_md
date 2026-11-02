# Piloto Codex: identificador declarado y exposición previa

Se redactaron tres respuestas originales de Codex en este chat para casos artificiales: cálculo de razón de sumas de palta, abstención por denominador cero de uva y abstención causal de arándano. Son tres respuestas, una por caso, no treinta casos completos ni 180 repeticiones.

Identificador solicitado por el usuario: **GPT 6.1 Sol Light**. Se registra como declaración del usuario y **no como identificador de API o versión del modelo técnicamente comprobados**. El origen es `codex_chat_authored`. La redacción comparte este chat y exposición previa a las claves; no se presenta como generación ciega o independiente. No hay uso real de DeepSeek u Ollama ni gasto de esas API; no se mide aquí el consumo de inferencia de la plataforma Codex.

El campo `external_api_call=false` se refiere a llamadas a proveedores desde la aplicación de la tesis. No significa que Codex no haya generado el texto mediante su propia plataforma. No se inventan tokens o metadatos internos: `usage` permanece nulo.

## Flujo implementado

- `responses.json`: texto y afirmaciones estructuradas redactadas por Codex, sin plantillas de sustitución de proveedor.
- `manifest.json`: procedencia, exposición previa, modelo declarado, fuentes y huellas. Ninguna salida cuenta como H4 final.
- `progress-evidence.json`: etapas actuales y huellas de siete artefactos. El panel ampliado es una versión distinta del piloto usado en los gráficos.
- API autenticada de solo lectura: catálogo, detalle y descarga del piloto; y estado actual del proyecto. El POST de generación no acepta `codex_archive`.
- La vista IA abre el archivo, indica modelo no verificado, piloto expuesto y revisión factual pendiente. Las consultas repetidas conservan ID y hash; no invocan un modelo ni incrementan repeticiones.

Se comprueban las huellas de respuestas, casos y claves numéricas antes de servirlas. La verificación numérica solo cubre los campos estructurados: dos respuestas coinciden con la referencia, y el caso sin denominador tiene estado no aplicable, no un cero de error inventado. La prosa y las afirmaciones factuales siguen pendientes de revisión humana.

## UI y evidencia

Se verificaron en el navegador los tres casos, descarga con SHA-256, selección entre proveedores y vista de proceso. La descarga real de arándano coincidió con la huella del backend. Se probó ancho móvil de 390 px sin desbordamiento horizontal de página y se restauró el tamaño normal. Las capturas están en `docs/ui-codex-piloto-2026-11-01`.

El proceso ya muestra 24 paquetes y 101.546 registros conciliados, en vez de mantener los candidatos como pendientes. Declara que los gráficos conservan el piloto anterior y que H2 se cerró como no evaluable. El botón de integridad contrasta los siete artefactos actuales, no los archivos del piloto antiguo.

La UI conserva plantilla, Ollama y DeepSeek como opciones independientes; sus claves y habilitación no se alteraron. El preview usa SQLite y cuenta QA aislados, sin leer el `.env` del usuario ni habilitar generación externa. No es una integración con un servicio de inferencia Codex ni un archivo de toda la conversación: solo estas tres respuestas seleccionadas.

## Alcance científico

No se recalificó H4 como ejecutada y no se sustituyó el experimento por caché. H3 histórica, generación final H4, RAG completo y revisión ciega mantienen sus condiciones previamente documentadas. Cambiar el generador del experimento requiere un protocolo previo y un entorno sin exposición a las claves; este piloto se informa aparte.
