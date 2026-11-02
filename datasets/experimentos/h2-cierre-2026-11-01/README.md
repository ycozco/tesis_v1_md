# Cierre de H2 para la colección auditada

**Dictamen: H2 no pudo evaluarse con la colección actual. El análisis de elegibilidad queda cerrado; la hipótesis no queda confirmada ni refutada.** No hay una ablación ejecutada ni métricas de mejora que reportar.

## Fundamento rector

La propuesta vigente, sección 1.4.3 H2, establece: «Si no existen variables compatibles o su disponibilidad temporal no puede verificarse, se documentará que la hipótesis no pudo evaluarse». La fuente se identifica en `decision.json` y en `planificacion/2026-11-01/fundamento-tesis.json`, ancla T02. Durante este cierre se reconfirmó que la tesis de Drive mantiene su modificación de 23 de octubre de 2026. No se cambió la hipótesis ni se retiraron sus condiciones para obtener un resultado favorable.

## Auditoría terminada

Se revisaron las cuatro familias contextuales, la cobertura y publicación del panel ampliado y los 52 orígenes del calendario provisional, para ambos objetivos y L=0/4/8. La matriz contiene **1.248 combinaciones origen × L × objetivo × fuente**, no 1.248 muestras independientes ni predicciones. Todas tienen cero casos pareados elegibles con evidencia temporal y de cobertura verificada.

| Fuente | Material disponible | Resultado de elegibilidad |
|---|---|---|
| BCRP | 102 meses locales; 32 cotejos documentales de 16 meses, todos coincidentes al redondeo | Originales y disponibilidad histórica no verificados; no se habilitan las transcripciones indexadas |
| SISAP | 3.074 celdas, 1.890 con precio numérico | Publicación histórica y unidades específicas sin verificar; interpretación del proxy pendiente |
| NASA POWER | 3.217 días por cada uno de cuatro parámetros en un punto de Arequipa | Sin vinculación territorial o justificación verificable del proxy y sin vintages de publicación |
| Comtrade | Una observación de muestra | No constituye una serie contextual suficiente ni tiene historial de disponibilidad reconstruido |

El panel SUNAT conserva 20.154 posiciones semanales, de las cuales 3.845 contienen operaciones recuperadas y 16.309 permanecen desconocidas. No hay certificados de cobertura completa ni fechas de publicación histórica verificadas; por ello ninguna fila está habilitada como objetivo final as-of. Los valores observados no se convierten en cero ni se interpretan como semanas completas.

**Corrección de criterio:** una covariable no necesita tener la misma unidad ni el mismo nivel comercial que FOB. El precio interno podría ser un proxy, la frecuencia mensual puede alinearse hacia atrás y el clima puede incorporarse con una vinculación justificada. El impedimento actual es la falta de evidencia de interpretación, unidades cuando corresponde, cobertura y disponibilidad; no una exigencia de igualdad con FOB. Basta una fuente elegible, no las cuatro.

## Comparación y conclusión

Se ejecutaron la conciliación numérica BCRP, el contraste independiente, la auditoría temporal y la verificación de la matriz. El universo común elegible para la comparación de modelos está vacío. Por ello no se ajustaron dos configuraciones para producir cifras sin sustento, no se imputaron fechas y no se abrieron los errores del test reservado. Las métricas, el respaldo y la refutación se guardan como `null`, no como error cero ni mejora cero.

Texto utilizable en resultados y limitaciones:

> H2 no pudo evaluarse con las fuentes auditadas. Aunque se recuperaron observaciones contextuales y se corroboraron valores de tipo de cambio a la precisión publicada, no fue posible verificar conjuntamente su disponibilidad histórica, su alineación con los orígenes del pronóstico y la cobertura de los objetivos del panel. El universo pareado elegible resultó vacío. En consecuencia, no se ejecutó la ablación historial frente a historial más contexto y no se obtuvo evidencia para respaldar ni refutar H2. Esta limitación se refiere a la colección y al protocolo auditados; no demuestra que el contexto carezca de utilidad predictiva.

## Evidencias y reproducción

- `source-inventory.json`: cantidades, restricciones y papel de cada fuente.
- `origin-eligibility.csv`: comprobación completa del calendario propuesto, sin valores imputados.
- `decision.json`: dictamen, regla de decisión y hashes de las entradas.
- `verification.json`: contraste independiente de hashes, matriz y conclusión.
- `one-pass-run.json`: ejecución continua, pruebas y huellas del código.

Comando completo, con el entorno científico/API ya instalado y las dependencias frontend disponibles:

```powershell
./data/runtime-research-clean/Scripts/python.exe -B tools/finish_h2.py
```

La opción `--legacy-gold-dir` permite comprobar aparte los artefactos antiguos. No hace falta para cerrar H2. La ejecución continua incluye la conciliación independiente, el cierre, su contraste, las regresiones temporales y la suite técnica actual de componentes, API, compatibilidad, datos y compilación.

Comandos individuales para inspección:
```
python -B tools/verify_h2_bcrp.py
python -B tools/close_h2.py
python -B tools/verify_h2_closure.py
python -B -m pytest tests/unit/test_h2_bcrp.py tests/unit/test_h2_closure.py -q
```

El comando de cierre falla explícitamente si las entradas ya no cumplen las condiciones auditadas: no sustituye una reevaluación de nuevas fuentes por ceros prefijados. El diagnóstico general valida las huellas antes de reconocer este cierre y lo marca obsoleto si cambia la evidencia. El cierre solo se reabre con nuevas fuentes verificadas o una modificación metodológica revisada que altere la elegibilidad. Recuperar originales y vintages es una posible ampliación, no un resultado fingido para declarar H2 aprobada. H1/H3/H4 conservan sus propios pendientes.
