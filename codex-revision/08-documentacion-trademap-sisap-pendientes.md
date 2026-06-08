# Documentación de Trade Map y SISAP/MIDAGRI

Fecha: 2026-06-07  
Ámbito de revisión: descargas manuales Trade Map en `D:\tesis_yoset\data-trademap` y recolección SISAP/MIDAGRI guardada en `codex-revision`.

## 1. Trade Map

### Carpeta revisada

```text
D:\tesis_yoset\data-trademap
```

### Estado

Se revisaron y renombraron 14 archivos `.xls` descargados desde ITC Trade Map. Se encontró que 8 archivos corresponden al flujo correcto para la tesis:

```text
Exportaciones de Perú por producto y mercado destino
```

También se detectaron 6 archivos colados de importación:

```text
Importaciones de Perú / proveedores externos
```

Estos últimos no deben usarse como benchmark principal de exportaciones, pero fueron conservados con prefijo `import_colado_` por trazabilidad.

### Archivos útiles para tesis

Usar estos 8 archivos:

```text
export_indicadores_2025_hs070920_esparrago.xls
export_indicadores_2025_hs080440_palta.xls
export_indicadores_2025_hs080610_uva.xls
export_indicadores_2025_hs081040_arandano.xls
export_serie_anual_2021_2025_hs070920_esparrago.xls
export_serie_anual_2021_2025_hs080440_palta.xls
export_serie_anual_2021_2025_hs080610_uva.xls
export_serie_anual_2021_2025_hs081040_arandano.xls
```

### Archivos colados de importación

No usar como base experimental:

```text
import_colado_indicadores_2025_hs080440_palta.xls
import_colado_indicadores_2025_hs080610_uva.xls
import_colado_indicadores_2025_hs081040_arandano.xls
import_colado_serie_anual_2021_2025_hs080440_palta.xls
import_colado_serie_anual_2021_2025_hs080610_uva.xls
import_colado_serie_anual_2021_2025_hs080610_uva_duplicado2.xls
```

Observación: `import_colado_serie_anual_2021_2025_hs080610_uva_duplicado2.xls` es duplicado de la serie anual importada de uva.

### Documentos generados en la carpeta Trade Map

```text
D:\tesis_yoset\data-trademap\README_renombrado.md
D:\tesis_yoset\data-trademap\rename_manifest_trademap.json
```

### Uso metodológico correcto

Trade Map debe usarse como benchmark internacional agregado:

```text
valor_unitario_trademap = valor_exportado / cantidad_exportada
```

Cruce recomendado con SUNAT:

```text
producto/HS + país destino + año
```

No reemplaza los microdatos SUNAT/Aduanet.

## 2. SISAP / MIDAGRI

### URL funcional confirmada

La URL que sí respondió fue:

```text
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/
```

La versión `https://sistemas.midagri.gob.pe/sisap/portal/` falló con:

```text
SSLV3_ALERT_HANDSHAKE_FAILURE
```

### Archivos guardados

Dentro de `codex-revision` se guardaron:

```text
data_raw/sisap_midagri/portal2_mayorista_resumenes_consultar/index.html
data_raw/sisap_midagri/portal_http/index.html
metadata/sisap_selectores_confirmados.json
```

### Confirmado

La página SISAP/MIDAGRI sí expone selectores y formulario para consultar precios/volúmenes por fecha, mercado, producto y variable.

Formularios detectados:

```text
form id="consulta"
method="post"
action="#"

form id="exportarExcel"
action="http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/exportarAExcel/"
method="post"
target="_blank"
```

Campos de fecha:

```text
fecha
desde
hasta
```

Periodicidades detectadas:

```text
dia
intervalo
semanal
mensual
anual
```

Años disponibles:

```text
1997 a 2026
```

Meses disponibles:

```text
01 enero
02 febrero
03 marzo
04 abril
05 mayo
06 junio
07 julio
08 agosto
09 septiembre
10 octubre
11 noviembre
12 diciembre
```

Mercado recomendado:

```text
15011501 = Gran mercado mayorista de lima
```

Variables disponibles:

```text
precio_max  = Precio Máximo
precio_prom = Precio Promedio
precio_min  = Precio Mínimo
volumen     = Volumen
```

Productos confirmados:

```text
0216 = Esparrago
0626 = Palta
0637 = Uva
0638 = Otros fruticolas
```

Arándano no aparece como producto directo en el HTML inicial. Puede estar dentro de `0638 = Otros fruticolas`, pero requiere expandir el árbol de productos con JavaScript/AJAX o navegador automatizado.

### Data SISAP pendiente

Actualización posterior: se confirmó que el endpoint `resumenes/filtrar` sí devuelve tablas HTML por POST sin login. La descarga en Excel aún no se ejecutó como archivo final porque el exportador requiere primero generar el HTML de reporte y luego enviar `datos_a_enviar`.

Todavía falta convertir a dataset CSV/XLS consolidado:

```text
Palta - precio_prom, precio_min, precio_max, volumen
Uva - precio_prom, precio_min, precio_max, volumen
Espárrago - precio_prom, precio_min, precio_max, volumen
Arándano - pendiente de confirmar producto/variedad
```

También está pendiente definir la granularidad final:

```text
diaria
mensual
anual
intervalo de tiempo
```

Para la tesis se recomienda priorizar:

```text
mensual 2018-2026
mercado 15011502 para palta y uva
mercado 15011501 para espárrago
variables precio_prom y volumen
productos 0626, 0637, 0216
```

Luego intentar arándano vía `Otros fruticolas` o descarga manual si el árbol no se deja automatizar.

### Parámetros sugeridos para próxima extracción SISAP

```yaml
base_url: "http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/"
excel_url: "http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/exportarAExcel/"
mercado: "15011501"
periodicidad: "mensual"
anios: ["2018","2019","2020","2021","2022","2023","2024","2025","2026"]
meses: ["01","02","03","04","05","06","07","08","09","10","11","12"]
variables: ["precio_prom","volumen"]
productos:
  palta: "0626"
  uva: "0637"
  esparrago: "0216"
  arandano: "pendiente_en_otros_fruticolas_0638"
```

### Nota técnica

El HTML inicial contiene el formulario y el enlace de exportación a Excel, pero no basta con hacer un POST simple si el servidor espera estado de sesión, `postID` o datos serializados en `datos_a_enviar`. Por eso el siguiente paso debe ser uno de estos:

1. Automatización con Playwright/Selenium sobre el formulario real.
2. Inspección de red del navegador al pulsar `Consultar` y `Exportar Excel`.
3. Descarga manual controlada por producto/periodo, documentando parámetros.

## 3. Estado pendiente consolidado

| Fuente | Data pendiente | Motivo |
|---|---|---|
| SISAP/MIDAGRI | Tablas de precios y volumen por producto/mes/año | Confirmados selectores; falta automatizar consulta/exportación. |
| SISAP/MIDAGRI | Arándano | No aparece directo; revisar `Otros fruticolas` o descarga manual. |
| UN Comtrade | Exportaciones Perú por HS 080440, 080610, 081040, 070920 | API requiere subscription key. |
| ITC Trade Map | Nada crítico para los 4 productos exportados | Ya hay 8 archivos útiles; quedaron 6 importaciones coladas documentadas. |
| ITC Trade Map | Posible ampliación mensual/trimestral | Solo si se necesita granularidad menor que anual. |
