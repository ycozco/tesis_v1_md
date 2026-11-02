# DeepSeek para H4: configuración privada y presupuesto

La vía elegida por el titular es DeepSeek, con clave y presupuesto configurados por él. Se preparó un transporte específico para el ejecutor H4; no se habilitó el proveedor de pago en la UI/API anterior ni se reutiliza su clave. **No se ha realizado ninguna llamada real a DeepSeek.** Las pruebas HTTP usan respuestas simuladas.

## Configurar sin compartir la clave

Desde PowerShell, en la raíz del repositorio:

```powershell
$h4BudgetUsd = [decimal](Read-Host 'Tu presupuesto maximo para esta preparacion y H4, en USD')
./tools/configure_h4_deepseek.ps1 -BudgetUsd $h4BudgetUsd
```

El script pide la clave con entrada oculta, la guarda cifrada mediante DPAPI para el usuario actual de Windows bajo `data/h4-deepseek/key.dpapi` y solo la expone al proceso hijo en `H4_DEEPSEEK_API_KEY`. Al terminar restaura el entorno y libera la representación nativa del secreto. No imprime ni escribe la clave en texto plano; `data/` está excluido de Git. No pegues la clave en el chat. `-ReplaceKey` permite sustituirla explícitamente.

Esta orden configura tu límite y hace una comprobación **offline**, sin comprobar la validez de la clave con el servidor ni gastar saldo. La configuración pública de ejemplo permanece deshabilitada y con presupuesto cero; el archivo privado real está en `data/h4-deepseek/config.json`. No se sobrescribe el gasto anterior al cambiar el presupuesto y no se resetea el libro de consumo.

## Calibración explícita, con coste

Cuando decidas autorizar la prueba neutral de conexión dentro de tu presupuesto:

```powershell
./tools/configure_h4_deepseek.ps1 -BudgetUsd $h4BudgetUsd -Action Calibrate
```

Esta orden sí envía **una petición de pago**, independiente de los casos H4, y registra modelo devuelto y `system_fingerprint`. No ejecuta los 180 casos. La calibración usa el mismo libro de presupuesto que el experimento. Antes de consumirlo en H4, esos metadatos deben incorporarse al congelamiento experimental. El alias no acredita por sí solo una versión inmutable; el transporte detiene nuevas peticiones si cambia el modelo devuelto o el fingerprint esperado. Eso verifica consistencia declarada por el proveedor, no el peso binario interno del modelo.

## Modelo, uso y coste reservado

La [documentación oficial de precios](https://api-docs.deepseek.com/quick_start/pricing/), consultada el 1 de noviembre de 2026, identifica `deepseek-flash` como DeepSeek-V4.1-Flash-1017. Se emplean los techos de hora punta sin descuento de caché: **USD 0,30 por millón de tokens de entrada y USD 1,20 de salida**. Son tarifas consultadas, no una promesa permanente del proveedor; revisarlas antes de la ejecución y mantener el contrato versionado.

El [endpoint Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/) permite salida JSON y devuelve `usage`. El transporte fija HTTPS oficial, deshabilita redirecciones, razonamiento y herramientas, y no usa proxies/credenciales ambientales de `requests`. Conserva modelo, fingerprint, ID de respuesta y tokens; nunca cabeceras de autorización.

Configuración inicial: máximo conservador de 16.000 tokens de entrada por petición, salida de 800 tokens, temperatura cero, 180 turnos H4 y una calibración: **181 peticiones como máximo**, sin correcciones adicionales. La reserva máxima calculada es **USD 0,00576 por petición y USD 1,04256 para las 181** con estas tarifas y límites. No es un precio real medido ni un presupuesto elegido por el titular. Las correcciones y las nuevas calibraciones consumen peticiones y presupuesto; requieren ajustar y congelar esos límites antes de generar, sin cambios oportunistas por resultados.

Antes de enviar se reserva el máximo completo de la petición. Después se contabiliza un coste superior calculado con tokens devueltos y tarifas punta sin caché; los descuentos reales pueden reducir la factura. Se limita también el tamaño del texto mediante un techo conservador de bytes UTF-8 más sobrecarga. La reserva presupone los precios y límites declarados: el control local no sustituye un límite de saldo del proveedor ni garantiza una factura si cambian sus tarifas.

Si falta `usage`, hay timeout/error HTTP, una respuesta no permite conocer consumo o quedan reservas sin terminar, se conserva el máximo y se detiene el libro. No hay reintento automático ni reinicio silencioso del gasto. Revisar los cargos del proveedor y el libro antes de reconciliarlo; no borrar el historial para reanudar. El libro usa exclusión entre procesos y escritura atómica. JSON incompleto consume igualmente el uso ya registrado, sin fingir que la petición fue gratis.

## Estado experimental

El transporte está disponible para `pipeline/research/h4_runner.py` como callback con los mismos parámetros de ambos brazos. **No hay todavía un comando que eluda las puertas científicas y lance los 180 casos.** Siguen pendientes revisión humana de claves, política de tasas indefinidas, recuperación documental real y congelamiento del experimento. Configurar una clave o calibrar el transporte no satisface esos requisitos ni produce una conclusión H4.

Comprobación reproducible sin clave ni red:

```powershell
./data/runtime-research-clean/Scripts/python.exe -B tools/h4_deepseek.py --init
./data/runtime-research-clean/Scripts/python.exe -B tools/h4_deepseek.py --check
./data/runtime-research-clean/Scripts/python.exe -B -m pytest tests/unit/test_deepseek_h4.py -q
```
