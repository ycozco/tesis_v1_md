# Riesgos y correcciones prioritarias

## Prioridad alta

### 1. Excluir cacao del pipeline experimental

Evidencia:

- `data/dataset_real_v1.csv` tiene solo 379 registros de cacao.
- Scripts actuales aún lo incluyen.
- Dataset sintético también lo incluye con 554 registros, sobrerrepresentándolo respecto al real.

Corrección:

1. Crear configuración central de productos.
2. Filtrar cacao en ETL, segmentación, sintético y experimentos.
3. Regenerar resultados y tablas del Capítulo IV.
4. Añadir justificación metodológica:

```text
El cacao fue excluido del modelamiento experimental debido a su baja representatividad muestral en el dataset real consolidado. Esta decisión reduce el riesgo de estimaciones inestables y evita conclusiones no generalizables.
```

### 2. Separar real, proxy y sintético

Riesgo: presentar como real variables que no están disponibles públicamente por DUA.

Variables críticas:

```text
merma_pct
costo_logistico_usd_kg
cumplimiento_fitosanitario
dias_logisticos
temperatura/humedad/precipitación si fueron simuladas
etiqueta_anomalia
```

Corrección:

- Agregar columna `fuente_variable` o documentar a nivel de datasheet.
- Usar `*_simulado` en nombres cuando corresponda.
- Incluir matriz real/proxy/sintético en Capítulo III.

### 3. Tratar duplicados del dataset real

Evidencia:

- `verify_integrity.py` detectó 4,684 duplicados en `data/dataset_real_v1.csv`.

Corrección:

1. Definir clave de deduplicación.
2. Usar `dua_key` cuando esté disponible.
3. Si el dataset final no conserva `dua_key`, agregarlo o documentar la razón.
4. Generar reporte antes/después:

```text
registros_antes
registros_despues
duplicados_removidos
criterio_deduplicacion
```

### 4. Generar segmento de espárrago o excluirlo operacionalmente

Evidencia:

- Hay 2,599 registros de espárrago en el maestro.
- No existe `data/real_processed/esparrago/dataset_esparrago_raw.csv`.

Corrección:

- Si se mantiene como secundario, incluirlo en `src/segment_datasets.py`.
- Si no se usa, moverlo a análisis contextual.

## Prioridad media

### 5. Corregir nombres ambiguos de scripts/datasets

`src/build_real_dataset.py` genera `dataset_agro_sintetico_v1.csv`, por lo que el nombre puede confundir al jurado.

Corrección recomendada:

- Documentar como dataset sintético calibrado.
- Renombrar en una fase posterior a algo como:

```text
build_synthetic_calibrated_dataset.py
```

### 6. Ajustar fechas futuras del sintético

`data/dataset_agro_sintetico_v1.csv` llega hasta 2026-12-28, fecha futura respecto al 2026-06-07.

Corrección:

- Declarar como escenario prospectivo, o
- Recortar a `<= 2026-06-07` para evaluación histórica.

### 7. Reforzar fuentes climáticas reales

El código `src/etl_real_data.py` contiene `simulate_weather`, con clima realista por zona pero no necesariamente observado.

Corrección:

- Añadir `fuente_clima`.
- Reemplazar con SENAMHI/NASA POWER cuando se implemente.
- Mantener simulación solo como calibración sintética.

### 8. Documentar scraping con bitácora

Riesgo: no poder reproducir qué se descargó, cuándo y desde dónde.

Corrección:

Crear:

```text
codex-revision/log-scraping.md
metadata/data_lineage.yml
```

## Prioridad baja

### 9. Revisar codificación de textos

Varios archivos muestran mojibake en salidas de consola o contenidos (`Ã³`, `Ã±`). No necesariamente rompe el pipeline, pero afecta presentación.

Corrección:

- Normalizar lectura/escritura a UTF-8.
- Evitar que PowerShell muestre textos sin `PYTHONIOENCODING=utf-8`.

### 10. Fortalecer métricas para datos reales sin etiqueta

Riesgo: usar PR-AUC/F1 como si fueran métricas reales si las etiquetas son sintéticas o reglas inyectadas.

Corrección:

- En real: usar ranking top-k, inspección experta, estabilidad temporal, SHAP y reglas auditables.
- En sintético calibrado: PR-AUC, ROC-AUC, F1, precisión y recall sí son válidos como evaluación controlada.

## Redacción recomendada para tesis

```text
La investigación utiliza una estrategia híbrida de datos. Las dimensiones comerciales y aduaneras se sustentan en microdatos reales públicos de SUNAT/Aduanet, complementados con tipo de cambio BCRP y fuentes externas oficiales o institucionales. Sin embargo, variables internas como merma, calidad de lote, temperatura de contenedor, costo logístico unitario y cumplimiento fitosanitario por embarque no están disponibles públicamente a nivel de DUA. Por ello, estas dimensiones se modelan mediante datos sintéticos calibrados y reglas trazables, evitando presentarlas como observaciones reales.
```

## Checklist de cierre antes de defensa

- [ ] Dataset real sin cacao generado.
- [ ] Segmento espárrago creado o exclusión documentada.
- [ ] Reporte de deduplicación del dataset real.
- [ ] Datasheet actualizado con real/proxy/sintético.
- [ ] Capítulo III corregido con matriz de fuentes.
- [ ] Capítulo IV regenerado sin cacao.
- [ ] Métricas reales separadas de métricas sintéticas.
- [ ] Bitácora de scraping y data lineage creada.
- [ ] Fuentes web citadas con fecha de consulta.
- [ ] Variables privadas renombradas o documentadas como sintéticas/calibradas.

