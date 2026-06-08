# Reporte de Calidad de Datos

Fecha de generacion: 2026-06-07  
Generado por: `src/eda_calidad.py`  
Documento rector: `plan-implementacion-datasets-tesis.md`

---

## 1. Resumen ejecutivo

| Metrica | Valor |
|---|---|
| Archivo fuente | `data/dataset_real_v1.csv` |
| Filas totales (raw) | 40,293 |
| Filas validas (post-validacion) | 40,289 |
| Filas rechazadas | 4 |
| Pct rechazadas | 0.01% |
| Periodo cubierto | 2018 — 2026 |
| Productos presentes | palta, uva, arandano, esparrago |

---

## 2. Conteo por producto

| Producto | Filas |
|---|---|
| palta | 17,360 |
| uva | 15,697 |
| arandano | 4,633 |
| esparrago | 2,599 |

**Cacao excluido:** ✅ SI (correcto)

---

## 3. Analisis de nulos

| columna | nulos | pct_nulos | tipo_dato |
|---|---|---|---|
| regla_inyeccion | 40293 | 100.00% | float64 |
| empresa_exportadora | 2110 | 5.24% | str |

---

## 4. Duplicados

| Tipo | Cantidad |
|---|---|
| Duplicados exactos | 0 |
| Duplicados funcionales | 4,933 |
| Columnas usadas para dedup funcional | producto, fecha, empresa_exportadora, destino_mercado, volumen_kg, precio_kg_usd |

---

## 5. Outliers (metodo IQR x3)

| columna | min | max | mean | outliers_3iqr | pct_outliers |
|---|---|---|---|---|---|
| id | 1.0000 | 40672.0000 | 20271.9775 | 0 | 0.00% |
| partida_arancelaria | 709200000.0000 | 810400000.0000 | 799611696.8208 | 2599 | 6.45% |
| volumen_kg | 0.7800 | 45497.0000 | 13783.9916 | 0 | 0.00% |
| precio_kg_usd | 0.0001 | 146.2909 | 3.1133 | 1779 | 4.42% |
| dias_logisticos | 0.0000 | 25.0000 | 4.4240 | 383 | 0.95% |
| costo_logistico_usd_kg | 0.1800 | 0.4800 | 0.2331 | 631 | 1.57% |
| cumplimiento_fitosanitario | 1.0000 | 1.0000 | 1.0000 | 0 | 0.00% |
| merma_pct | 1.2000 | 7.4500 | 2.1115 | 58 | 0.14% |
| tipo_cambio_pen_usd | 3.7650 | 3.7650 | 3.7650 | 0 | 0.00% |
| temperatura_max_c | 20.8000 | 32.6000 | 23.8811 | 551 | 1.37% |
| temperatura_min_c | 8.2000 | 24.6000 | 16.8802 | 797 | 1.98% |
| precipitacion_mm | 0.0000 | 5.0000 | 0.0233 | 1108 | 2.75% |
| humedad_pct | 55.0000 | 81.6000 | 73.7690 | 0 | 0.00% |
| etiqueta_anomalia | 0.0000 | 0.0000 | 0.0000 | 0 | 0.00% |
| regla_inyeccion | nan | nan | nan | 0 | 0.00% |

---

## 6. Cobertura temporal por producto

| producto | anio | registros |
|---|---|---|
| arandano | 2022 | 143 |
| arandano | 2024 | 3 |
| arandano | 2025 | 2,021 |
| arandano | 2026 | 2,466 |
| esparrago | 2025 | 148 |
| esparrago | 2026 | 2,451 |
| palta | 2018 | 1 |
| palta | 2019 | 20 |
| palta | 2021 | 1 |
| palta | 2022 | 44 |
| palta | 2025 | 178 |
| palta | 2026 | 17,116 |
| uva | 2021 | 11 |
| uva | 2022 | 21 |
| uva | 2024 | 55 |
| uva | 2025 | 6,434 |
| uva | 2026 | 9,180 |

---

## 7. Estado de fuentes externas integradas

| Fuente | Estado | Filas |
|---|---|---|
| dataset_real_v1.csv | OK Base experimental | 40,293 |
| SUNAT/ADUANET DBFs 2026 | Sin datos SUNAT filtrados (periodo 2026 solo) | - |
| BCRP tipo de cambio | OK 101 periodos mes | 101 |
| SISAP/MIDAGRI | OK 3826 registros | 3826 |
| NASA POWER clima | OK 77000 registros | 77000 |
| APN/OSITRAN logistica | OK 7891 registros | 7891 |
| Trade Map | OK 8 archivos procesados | 16 |

---

## 8. Gate pre-entrenamiento - estado actual

| Item | Estado |
|---|---|
| origen_dato presente | PASS |
| precio_kg_usd mayor 0 en validos | PASS |
| volumen_kg mayor 0 en validos | PASS |
| etiqueta_anomalia sin nulos | PASS |
| Cacao ausente | PASS |

---

## 9. Rechazados

Archivo: codex-revision/data_processed/rejected/rechazados_2026-06-07.csv  
Total rechazados: 4

---

## 10. Notas metodologicas

- El dataset_real_v1.csv es la base experimental principal.
  Contiene variables proxy y potencialmente sinteticas marcadas con regla_inyeccion.
- Los DBFs SUNAT descargados corresponden a ventanas de 2026 (periodos semanales).
  Para cubrir 2018-2025, se necesitan descargar los anualizados de ADUANET.
- El tipo de cambio canonico BCRP PN01207PM cubre 2018-01 a 2026-06 (101 meses).
- El clima proxy NASA POWER tiene 77000 registros cubriendo las zonas productoras.
- Recomendacion: dataset_real_v1.csv es defendible como base si se documenta
  que las variables operativas (merma, dias_logisticos, cumplimiento) son proxies simuladas.
