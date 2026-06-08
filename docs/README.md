# Indice Canonico De Documentacion

Este directorio contiene los capitulos, anexos y reportes tecnicos de la tesis. La fuente vigente no es cualquier archivo suelto dentro de `docs/`, sino el conjunto declarado en `SECTION_ORDER` dentro de `scripts/rebuild_tesis_monolith.py`.

El monolito activo se genera en:

```text
docs/02-95-tesis.md
```

Para regenerarlo:

```powershell
py scripts/rebuild_tesis_monolith.py
```

Los borradores historicos y documentos desalineados se conservan en `docs/archive/` y no deben citarse como version vigente.

## Modulos Activos De Tesis

| Bloque | Archivos fuente |
|---|---|
| Front matter | `02-00-portada.md`, `02-01-resumen.md`, `02-02-indices.md`, `02-03-introduccion.md` |
| Capitulo I | `02-10-capitulo1.md` |
| Capitulo II | `02-20-capitulo2-antecedentes.md`, `02-21-capitulo2-estadoarte.md`, `02-22-capitulo2-marcoteorico.md` |
| Capitulo III | `02-30-capitulo3.md` |
| Capitulo IV | `02-40-capitulo4.md`, `02-41-capitulo4-resultados-cuantitativos.md`, `02-42-capitulo4-explicabilidad-reportes.md`, `02-43-capitulo4-usabilidad-trazabilidad.md`, `02-44-capitulo4-discusion.md`, `02-45-capitulo4-limitaciones-sintesis.md` |
| Capitulo V y cierre | `02-50-capitulo5.md`, `02-60-conclusiones.md`, `02-70-recomendaciones.md` |
| Soporte academico | `02-80-glosario.md`, `02-90-referencias.md` |
| Anexos | `05-a1-anexo-usabilidad.md`, `05-a2-anexo-modelcards.md`, `05-a3-anexo-datasheet.md`, `05-a4-anexo-ia.md`, `05-a5-resumen-general.md` |

## Documentos Tecnicos De Soporte

| Archivo | Uso |
|---|---|
| `03-01-variables-operacionalizadas.md` | Definicion formal de VI, VD1-VD5 y variables explicativas. |
| `03-02-recopilacion-de-data.md` | Evidencia de recopilacion multisource. |
| `03-03-informe-detallado-datasets.md` | Catalogo de datasets conocidos y estado metodologico. |
| `03-04-preprocesamiento-data.md` | Reglas de limpieza, transformacion y split temporal. |
| `03-05-resultado-procesamiento.md` | Estado del procesamiento y decisiones por producto. |
| `03-06-informe-de-uso-datos.md` | Uso de datos en anomalias, SHAP y RAG. |
| `03-07-busqueda-datos-y-fuentes.md` | Bitacora de busqueda de fuentes y enlaces tecnicos. |

## Planes Y Gobernanza

Los archivos `01-*` y `04-*` son planes, bitacoras o documentos de gestion. Pueden contener ideas historicas o rutas de trabajo anteriores. Cuando contradigan el enfoque actual, prevalecen:

1. `plan-implementacion-datasets-tesis.md` en la raiz del proyecto.
2. Los capitulos activos `02-*` incluidos en `SECTION_ORDER`.
3. Los anexos activos `05-*`.
4. Los informes tecnicos `03-01` a `03-07`.

## Reglas De Mantenimiento

- No editar manualmente `docs/02-95-tesis.md`; regenerarlo desde los modulos fuente.
- No agregar documentos historicos a `SECTION_ORDER`.
- No presentar datos sinteticos como observaciones oficiales.
- No usar cacao como producto de evaluacion principal.
- No interpretar SISAP como exportaciones; es mercado interno mayorista.
- No reportar metricas finales sin version de dataset, split temporal y reporte reproducible.
