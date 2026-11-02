# H2 — conciliación documental BCRP

Se preservó la serie local de **102 meses** sin modificar sus valores ni completar fechas de publicación. Se contrastaron **16 meses, enero de 2025–abril de 2026**, contra el promedio interbancario del cuadro 36 de dos publicaciones oficiales:

- [Nota Semanal 18, 14 de mayo de 2026](https://www.bcrp.gob.pe/docs/Publicaciones/Nota-Semanal/2026/ns-18-2026.pdf).
- [Nota Semanal 19, 21 de mayo de 2026](https://www.bcrp.gob.pe/docs/Publicaciones/Nota-Semanal/2026/ns-19-2026.pdf).

Resultado: **32 comparaciones coinciden con la precisión impresa de tres decimales; cero conflictos**. La regla es diferencia absoluta ≤0,0005 + 1e-9 PEN/USD. No se sustituyen las cifras locales más precisas por las redondeadas del documento. La correspondencia del concepto con PN01207PM se mantiene como candidata hasta revisar el original.

## Alcance de la extracción

Las tablas y fechas se consultaron mediante el texto indexado de documentos oficiales. Los valores se transcribieron manualmente, se separaron como candidatos documentales y se conciliaron mediante un script reproducible. No se presentan como extracción automática del PDF. Los promedios del mes en curso y filas anuales intercaladas del texto aplanado no se incorporaron. Se limitó la extracción al bloque mensual inequívoco indicado.

Las solicitudes directas de API y PDF devolvieron HTML, aunque HTTP respondiera 200. No se evitó el control de acceso ni se consideraron válidos esos cuerpos. `retrieval-manifest.json` conserva URL, fecha de consulta, tipo, tamaño y SHA-256; los cuerpos de respuesta se conservan localmente bajo `data/`, excluidos de Git. Obtener el PDF real permitirá revisar tabla, columnas y fechas y conservar una huella del original; la huella de HTML no certifica el PDF.

## Disponibilidad histórica y H2

Los **32 candidatos siguen excluidos** del join experimental. `document_date` no se copia a `verified_available_at`; esa fecha permanece vacía. Además, que una nota de mayo de 2026 muestre enero de 2025 no demuestra que esa misma versión estuviera disponible en enero de 2025. No se retropropagan valores a los orígenes de entrenamiento o desarrollo.

Se implementó y probó un filtro que exige original verificado, fecha de disponibilidad con zona horaria no posterior al origen y mes ya terminado. Es infraestructura de comprobación; una bandera `original_verified` puesta por software no sustituye evidencia y revisión. Aun con documentos de mayo verificados, faltaría recuperar versiones fechadas anteriores al desarrollo y suficientes para el calendario completo.

**H2 sigue no evaluable con esta entrega.** Se avanzó en la corroboración de los valores y en localizar vintages candidatos; no se ejecutó ablación ni se modificaron los datos o resultados de pronóstico. Los siguientes pasos son conseguir originales válidos, revisar su correspondencia conceptual y cobertura temporal, documentar disponibilidad, resolver cobertura SUNAT y fijar la comparación pareada antes del test.

## Reproducción

```
python -B tools/reconcile_h2_bcrp.py
python -B tools/reconcile_h2_bcrp.py --retrieve
python -B -m pytest tests/unit/test_h2_bcrp.py -q
```

La primera orden reproduce la conciliación de las transcripciones contra la copia local. La segunda realiza nuevas solicitudes normales y requiere `requests`; no asegura que el servidor entregue PDFs. La transcripción documental debe verificarse contra originales antes de habilitar el uso experimental.

## Verificación y contraste independiente posterior

`python -B tools/verify_h2_bcrp.py` recalcula desde los archivos guardados sin importar el productor de la conciliación: claves únicas, 16 meses por cada documento, diferencias Decimal, coherencia de fechas/estados, fuente local inmutable y huellas de los cinco cuerpos descargados. Resultado: 32 coincidencias, diferencia máxima 0,00049 PEN/USD, cero fallos de integridad, cero originales PDF verificados y cero filas elegibles. Son 16 meses repetidos en dos notas, no 32 meses independientes ni 32 PDFs revisados. La consulta web posterior volvió a localizar el cuadro 36 indexado de ambas notas; la evidencia sigue siendo transcripción indexada.

Se corrigió un hueco potencial del selector: una fila marcada como verificada podía declarar una disponibilidad anterior a su propio documento. Ahora exige fecha documental y rechaza esa contradicción. No se detectó un caso así habilitado en esta colección, pues todos los candidatos permanecían excluidos. Cuatro pruebas del módulo aprobaron, incluida la regresión de este caso. Una marca de verificación sigue requiriendo evidencia externa y revisión, no constituye por sí sola certificación.

No se amplió el conjunto elegible ni se ejecutó H2. Los datos concuerdan al redondeo publicado; la disponibilidad histórica sigue sin demostrarse. `independent-audit.json` conserva el resultado del verificador.
