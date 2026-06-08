# Gate Pre-Entrenamiento

Fecha: 2026-06-07  
Generado por: `src/build_dataset_final.py`

## Gate de datos

- [x] `dataset_modelo_v_final_2026-06-07.csv` existe y tiene fecha en el nombre.
- [x] Numero de filas documentado: 40,289 filas.
- [x] Cero filas con `precio_kg_usd` <= 0.
- [x] Cero filas con `volumen_kg` <= 0.
- [x] Columna `origen_dato` presente en cada fila.
- [x] Columna `etiqueta_anomalia` presente sin nulos.
- [x] Cacao completamente ausente del dataset final.
- [x] Split temporal implementado sin mezcla aleatoria.
- [x] Conjunto de prueba no contaminado por SMOTE ni balanceo.
- [x] `reporte-calidad-datos.md` generado y disponible.

## Gate de trazabilidad

- [x] `diccionario-fuentes-canonicas.md` existe y tiene entradas.
- [x] Columna `origen_dato` presente en cada fila.
- [x] Una sola version de tipo de cambio BCRP en el pipeline.

## Gate de modelos

- [ ] Los modelos se entrenan por producto (palta, uva, arandano).
- [ ] Existe un modelo base (baseline trivial: media historica).
- [ ] Optuna tiene presupuesto de trials fijo: n_trials=100, timeout=3600.
- [ ] Semillas fijadas: [42, 123, 456, 789, 2026].

## Resumen de splits

| Partition | Filas | Fecha inicio | Fecha fin |
|---|---|---|---|
| Train (70%) | 28,202 | 2018-06-15 | 2026-04-10 |
| Val (10%) | 4,028 | 2026-04-10 | 2026-04-23 |
| Test (20%) | 8,059 | 2026-04-23 | 2026-05-27 |

## Estado de items Gate de modelos

Los items de Gate de modelos se completaran en Fase 6 (entrenamiento).
El entrenamiento puede iniciarse solo cuando todos los gates de datos y trazabilidad esten marcados [x].
