# Protocolo de conciliación SUNAT — versión 1.0

Fecha: 31 de octubre de 2026. Alcance: 22 paquetes disponibles, no el universo completo de exportaciones. La entrada se preserva íntegra y cada fila recibe una decisión.

## Fundamento y límite de la clave

SUNAT describe paquetes procesados por fecha de modificación y reemplazo del envío anterior cuando una declaración vuelve a publicarse. Fuente primaria descargada: http://www.aduanet.gob.pe/aduanas/informae/procedimiento.doc (SHA-256: 53e9f1c9a7989099c79d3f98170f0caf031c0891d82cce7580a3ecd198bb065d). Portal: https://www.sunat.gob.pe/operatividadaduanera/index.html. Se conserva el documento original solo localmente en data/fuentes_2026-10-31/documentacion/.

La clave operativa candidata es CADU|FANO|NDCL para declaración y añade NSER para serie. Se comprueban componentes numéricos positivos y concordancia entre DBF y CSV. Se publican únicamente hashes de estas claves. El diccionario estructura_bases.xls no pudo recuperarse (HTTP 404); no se presenta esta revisión como certificación oficial de la clave. Su validación contra un diccionario completo y cualquier cambio de identidad entre declaraciones quedan pendientes.

## Reglas ejecutadas

1. Verificar SHA-256 de los 22 ZIP y estructura de sus DBF; contrastar TODOS los campos retenidos del CSV contra su fila DBF, no solo conteos.
2. Interpretar el último día del periodo del nombre xDDDDMMAA.zip como orden de los paquetes. Es una referencia al periodo del paquete, NO una fecha acreditada de publicación o disponibilidad histórica.
3. Leer todas las filas activas de cada DBF, también las subpartidas fuera del alcance. Obtener para cada declaración el paquete más reciente disponible. Esto evita conservar series antiguas cuando la declaración fue actualizada después.
4. Marcar las filas de paquetes anteriores como sustituidas por el snapshot posterior de la declaración. No sumar importes de revisiones. Si una serie objetivo desaparece del último snapshot, registrarla aparte; se encontraron cero casos en esta ejecución.
5. Comparar todos los campos analíticos originales, incluyendo fechas, destino, FOB y peso. Eliminar únicamente repeticiones idénticas de esa proyección dentro del snapshot vigente. La equivalencia se refiere a campos extraídos, NO a todos los campos privados del DBF. Elegir la menor fila de origen solo como referencia trazable de copias equivalentes, nunca como criterio para resolver valores distintos.
6. Si una serie tiene versiones analíticas diferentes dentro del último paquete, no usar orden de fila, FOB máximo, promedios ni la fecha de regularización para adivinar el valor correcto. Poner toda su declaración en cuarentena para no publicar como completa una declaración parcialmente ambigua.
7. Poner también en cuarentena declaraciones con clave inválida, fecha de embarque inválida/posterior al periodo del paquete o calidad física inválida. No se encontraron casos de esta segunda categoría.
8. Conservar todos los excluidos en decisiones.csv y las filas vigentes bloqueadas en cuarentena.csv. Mantener sin cambios observaciones-sunat.csv y los originales. Una fila conciliada tiene los mismos campos y valores de una fila de origen, con metadatos adicionales.

## Archivos y significados

- vista-conciliada.csv: una fila por clave candidata de serie, sin declaraciones bloqueadas, según el último paquete disponible de cada declaración.
- decisiones.csv: una decisión por cada una de las 110253 filas; identificadores hash, fuente/fila, periodo y huella analítica.
- cuarentena.csv: filas del último snapshot de declaraciones bloqueadas, incluidas las series vecinas sin conflicto propio.
- conflictos-detalle.json: campos y valores contradictorios por serie, sin nombres/RUC/direcciones.
- series_ausentes_snapshot_posterior.csv: series de los envíos antiguos que no aparecen en el último snapshot; archivo vacío salvo cabecera en esta ejecución.
- resumen.json: métricas, hashes de entrada/código y comprobaciones.
- informe.md: lectura de los resultados y pendientes.

## Reproducción y verificación

Desde la raíz del repositorio, con Python 3 y los DBF originales recuperados:

    python -B tools/reconcile_sunat.py .
    python -B tools/verify_sunat_reconciliation.py .

Los dos scripts usan únicamente la biblioteca estándar de Python. En esta sesión se utilizó D:/tesis_yoset/.venv/Scripts/python.exe, sin escribir en el respaldo. Primero debe poder reproducirse la extracción con los scripts Node.js ya incluidos.

El verificador independiente relee los resultados persistidos: comprueba contabilidad, cobertura exacta de referencias de entrada, unicidad, igualdad de valores con la fuente, pertenencia al último snapshot y exclusión de declaraciones bloqueadas. No acredita por sí mismo la semántica oficial de las claves.

## Límites de uso

La vista describe la versión más reciente ENTRE LOS PAQUETES DISPONIBLES. No se presume que sea la versión oficial final, un censo, un panel semanal completo o un dataset listo para entrenar. No se crean semanas, ceros ni datos faltantes. FOB/kg es un cociente observado, no precio del productor ni rentabilidad.

La elección de versiones revisadas puede incorporar información conocida después del embarque. Para backtesting se necesita reconstruir disponibilidad y versiones por origen; esta vista retrospectiva no garantiza ausencia de fuga temporal. Los 22 paquetes no certifican continuidad 2018–2026. Los valores extremos y FOB muy pequeños permanecen visibles: superar controles aritméticos no acredita validez económica.

La cuarentena solo se liberará con evidencia externa de versión correcta, diccionario de claves o rectificación de la fuente. Cualquier regla nueva debe versionarse y regenerar todas las salidas; no se editarán importes manualmente.
