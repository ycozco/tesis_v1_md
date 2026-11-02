# Preparación H4 con DeepSeek

Proveedor elegido por el titular: DeepSeek; la clave y el presupuesto los configura él. Se implementaron transporte HTTPS oficial, salida JSON, verificación del congelamiento y fingerprint, libro persistente con reservas conservadoras, registro de tokens, bloqueo de concurrencia y detención ante gasto incierto. No se habilitó el proveedor de pago en la UI/API anterior.

La configuración inicial privada está deshabilitada y con presupuesto cero; no se leyó la clave histórica ni se invocó una API real. Se verificó la sintaxis del script PowerShell sin ejecutarlo. Sus pruebas de transporte usan respuestas simuladas, no una conexión autenticada con DeepSeek ni salidas experimentales H4.

**8 pruebas específicas y 78 pruebas actuales de la suite aprobaron**, además de las verificaciones de datos, compatibilidad, snapshot y compilación. Queda pendiente que el titular configure su clave y límite, y decida cuándo ejecutar la calibración explícita de pago. La calibración se cobra dentro del mismo libro y no equivale al experimento H4.

[Instrucciones de configuración y uso](../../../docs/h4-deepseek-configuracion.md). El script `tools/configure_h4_deepseek.ps1` solicita la clave de forma oculta, la guarda cifrada con DPAPI bajo `data/` y por defecto solo comprueba la configuración sin red. El transporte usa `H4_DEEPSEEK_API_KEY`, independiente de otras claves del proyecto. La entrega no incluye configuración privada, clave cifrada, clave en texto plano ni libro de gasto real.

Las claves H4, política de tasas indefinidas, recuperación documental y configuración experimental siguen pendientes de revisión/congelamiento. No se han producido las 180 respuestas reales ni calificaciones humanas. El control local presupone tarifas revisadas y tokens/límites declarados; no sustituye un límite de saldo en la cuenta del proveedor.
