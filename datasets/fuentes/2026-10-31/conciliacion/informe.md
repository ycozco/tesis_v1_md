# Resultado de la conciliación documentada

31 de octubre de 2026 — reglas sunat-conciliacion-1.0.

## Balance de las 110253 filas originales

| Decisión | Filas |
|---|---:|
| Incluidas en vista conciliada | 93225 |
| Sustituidas por paquete posterior de su declaración | 9307 |
| Duplicados analíticos del snapshot vigente | 7613 |
| Cuarentena por contradicción simultánea | 108 |
| Total | 110253 |

Estas categorías son excluyentes. No deben sumarse a los 9811 duplicados y 7019 claves multiversión del inventario anterior: esos diagnósticos se solapan con las decisiones actuales.

## Vista obtenida

93225 claves candidatas de serie: palta 38543, uva 27279 y arándano 27403. No se imputaron importes, fechas ni destinos. Cada fila proviene de un registro identificable del CSV y del DBF.

De las 7019 claves inicialmente multiversión, 6981 quedaron incluidas tras aplicar el paquete vigente; 38 permanecen bloqueadas dentro de las declaraciones en cuarentena. Hay 28 series con contradicción propia en su último paquete: las 28 discrepan en FOB y 18 también en peso. Al bloquear las 25 declaraciones afectadas, se excluyen 73 series en total (45 sin contradicción propia) representadas por 108 filas. No equivale a 108 operaciones independientes.

No hubo series objetivo ausentes en el snapshot posterior ni declaraciones bloqueadas por las comprobaciones físicas/de clave/fecha añadidas. Esto no acredita cobertura integral ni elimina la necesidad de revisar extremos.

## Evidencia y controles

- SHA-256 original verificado para los 22 ZIP.
- Todas las referencias del CSV contrastadas con campos de sus DBF.
- Una decisión por cada fila original y una fila por clave de serie en la vista.
- Ninguna declaración en cuarentena entra en la vista.
- Contabilidad cerrada y valores FOB/peso conservados; input original sin modificación.
- Verificador independiente ejecutado con resultado OK.

Entrada SHA-256: 63b7fb27162d43b155648fa3af92c24fcfb073b597e7bd12eb80fa5b77b4ea3d.
Código SHA-256: a4f92f92fb4bff44e23f88bd6eb00b057121309a811c7ee6331c27697adde3ca.

## Pendientes concretos

1. Resolver 25 declaraciones con fuentes o diccionario oficial; no elegir el mayor FOB ni la última fila como sustituto de evidencia.
2. Confirmar la clave CADU|FANO|NDCL|NSER contra el diccionario vigente y considerar posibles cambios de identidad.
3. Auditar continuidad por producto/destino y fechas de disponibilidad. Conservar el carácter retrospectivo de la vista al diseñar el backtest.
4. Revisar calidad económica, valores extremos y correspondencia temporal antes de generar el panel semanal final.

Reglas completas: [protocolo.md](protocolo.md). Decisiones fila a fila: [decisiones.csv](decisiones.csv). Casos contradictorios: [conflictos-detalle.json](conflictos-detalle.json).
