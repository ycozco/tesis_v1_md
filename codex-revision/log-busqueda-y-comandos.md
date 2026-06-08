# Log de búsqueda y comandos

Fecha: 2026-06-07  
Ruta de ejecución: `d:\tesis_yoset`

## Búsqueda local

Se inspeccionó:

```text
README.md
src/constants.py
src/scrape_sunat_all.py
src/etl_real_data.py
src/download_context_data.py
src/build_real_dataset.py
src/segment_datasets.py
src/verify_integrity.py
limpieza_de_datos_y_normalizacion/preprocess_data.py
src/generate_synthetic_dataset.py
docs/03-08-trabajo-de-recopilacion-2026-06-07.md
data/results_metrics.json
```

Se ejecutaron auditorías de archivos, CSV y ZIP con Python local. El alias `python` no estaba disponible; se usó `py` para lectura estándar de CSV/ZIP y luego el Python del `.venv` para la verificación con `pandas`.

## Comandos relevantes

```powershell
Get-ChildItem -LiteralPath 'd:\tesis_yoset' -Force
rg --files
py <script de auditoría CSV/ZIP>
& 'd:\tesis_yoset\.venv\Scripts\python.exe' src\verify_integrity.py
Select-String -Path 'd:\tesis_yoset\src\*.py','d:\tesis_yoset\limpieza_de_datos_y_normalizacion\*.py' -Pattern 'cacao|CULTIVOS|PRODUCTOS|esparrago|1801001900'
Get-ChildItem -LiteralPath 'd:\tesis_yoset\data' -Recurse -File | Group-Object Extension
```

## Búsqueda web documental

Consultas realizadas:

```text
SUNAT operatividad aduanera bases regimenes definitivos exportacion definitiva DBF ZIP
BCRP API PN01207PM tipo de cambio promedio mensual
MIDAGRI SISAP precios mayoristas frutas portal descarga
SENAMHI descarga datos meteorologicos estaciones Peru
APN estadisticas trafico de carga 2025 xlsx Peru puertos
OSITRAN datos abiertos puertos movimiento carga contenedores csv Peru
FDA Import Refusals data dashboard download dataset Peru avocado grapes blueberries
RASFF Window public database Peru fruits alerts
```

## Contenido encontrado/documentado

- SENAMHI mantiene página oficial de descarga de datos meteorológicos y Gob.pe confirma descarga diaria en TXT con año, mes, día, precipitación, temperatura máxima y mínima, con registro requerido.
- BCRP expone series estadísticas y API; se mantiene PN01207PM como serie recomendada para tipo de cambio promedio mensual.
- APN publica reportes de tráfico de carga 2024/2025 con archivos PDF/XLSX, incluyendo movimiento de carga y contenedores.
- OSITRAN informa datos abiertos de puertos en PNDA con movimiento de carga, contenedores, naves atendidas, ingresos regulados e indicadores operativos.
- FDA mantiene página de Import Refusals y datasets ORA/Data Dashboard.
- RASFF indica que RASFF Window ofrece base pública consultable de notificaciones desde 2020 en adelante.

## Zips locales

Se encontraron 50 zips bajo `data/sunat/`, todos inspeccionados con Python. Ejemplo: `data/sunat/raw_downloads/x23290326.zip` contiene `x23290326.DBF`.

