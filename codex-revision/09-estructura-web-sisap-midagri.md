# Estructura web SISAP/MIDAGRI

Fecha: 2026-06-07  
URL revisada:

```text
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/
```

## 1. Confirmación principal

La web SISAP/MIDAGRI no requiere inicio de sesión para la consulta revisada. La versión funcional es `http`, no `https`.

La versión:

```text
https://sistemas.midagri.gob.pe/sisap/portal/
```

falló por SSL, pero la ruta directa:

```text
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/
```

respondió HTTP 200 y permitió reproducir consultas por POST.

## 2. Archivos guardados

Se guardaron dentro de `codex-revision`:

```text
data_raw/sisap_midagri/portal2_mayorista_resumenes_consultar/index.html
data_raw/sisap_midagri/assets/asset_00.js
data_raw/sisap_midagri/assets/asset_01.css
data_raw/sisap_midagri/post_matrix/*.html
metadata/sisap_assets_manifest.json
metadata/sisap_post_matrix_summary.txt
metadata/sisap_selectores_confirmados.json
```

## 3. Formularios detectados

### Consulta

```text
form id="consulta"
method="post"
action="#"
```

El formulario no se envía directamente al `#`; el JavaScript intercepta el submit y llama por AJAX a:

```text
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar
```

### Exportar Excel

```text
form id="exportarExcel"
action="http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/exportarAExcel/"
method="post"
target="_blank"
```

El exportador toma el HTML ya generado en el div de reporte y lo coloca en:

```text
datos_a_enviar
```

Luego envía ese HTML al endpoint `exportarAExcel`. Esto significa que primero debe generarse el reporte; no basta con llamar al exportador sin tabla.

## 4. JavaScript y endpoints internos

El HTML carga un JS principal:

```text
data_raw/sisap_midagri/assets/asset_00.js
```

Endpoints encontrados en ese JS:

```text
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/generos/filtrarPorMercado
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/variedades/filtrarPorGenero
http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrarVolumenPorProcedencias
```

Función JS clave:

```text
elementosDependientes(...)
```

Esta función arma solicitudes AJAX agregando:

```text
ajax=true
```

## 5. Endpoint de consulta confirmado

Endpoint operativo:

```text
POST http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar
```

Parámetros mínimos confirmados:

```text
mercado
variables[]
productos[]
producto
periodicidad
fecha
desde
hasta
anios[]
meses[]
semanas[]
__ajax_carga_final
ajax
```

Ejemplo de consulta mensual:

```text
mercado=15011502
variables[]=precio_prom
productos[]=0626
producto=NA
periodicidad=mensual
fecha=07/06/2026
desde=01/06/2026
hasta=07/06/2026
anios[]=2025
meses[]=06
__ajax_carga_final=consulta
ajax=true
```

## 6. Mercados confirmados por producto

La prueba mostró que no todos los productos están en el mismo mercado.

### Palta

Mercado con resultados:

```text
15011502 = Mercado mayorista nro 2-frutas
```

Producto:

```text
0626 = Palta
```

Resultados confirmados:

```text
dia + precio_prom
dia + volumen
mensual + precio_prom
mensual + volumen
anual + precio_prom
anual + volumen
```

### Uva

Mercado con resultados:

```text
15011502 = Mercado mayorista nro 2-frutas
```

Producto:

```text
0637 = Uva
```

Resultados confirmados:

```text
dia + precio_prom
mensual + precio_prom
mensual + volumen
anual + precio_prom
anual + volumen
```

El caso:

```text
dia + volumen
```

devolvió sin resultados para la fecha probada `07/06/2026`.

### Espárrago

Mercado con resultados:

```text
15011501 = Gran mercado mayorista de lima
```

Producto:

```text
0216 = Esparrago
```

Resultados confirmados:

```text
mensual + precio_prom
mensual + volumen
anual + precio_prom
anual + volumen
```

No devolvió resultados diarios para la fecha probada `07/06/2026`.

### Arándano

No aparece como producto directo en el HTML inicial.

Posible ruta:

```text
0638 = Otros fruticolas
```

Pendiente: expandir el árbol de productos o buscar por interacción en navegador para confirmar si arándano existe como variedad hija.

## 7. Mercados probados

```text
15011501 = Gran mercado mayorista de lima
15011503 = Mcdo mod. de frutas
15011502 = Mercado mayorista nro 2-frutas
15013704 = Mcdo prod. santa anita
```

Hallazgo:

- Palta y uva sí devuelven resultados en `15011502`.
- Espárrago sí devuelve resultados en `15011501`.
- `15011503` y `15013704` no devolvieron resultados para las combinaciones probadas.

## 8. Variables probadas

```text
precio_prom = Precio Promedio
volumen = Volumen
```

También están disponibles, pero todavía no se probaron exhaustivamente:

```text
precio_max = Precio Máximo
precio_min = Precio Mínimo
```

## 9. Data SISAP ya confirmada

Se confirmó descarga de tablas HTML, no Excel, para:

```text
Palta mensual 2025-06 precio_prom
Palta mensual 2025-06 volumen
Palta anual 2025 precio_prom
Palta anual 2025 volumen
Uva mensual 2025-06 precio_prom
Uva mensual 2025-06 volumen
Uva anual 2025 precio_prom
Uva anual 2025 volumen
Espárrago mensual 2025-06 precio_prom
Espárrago mensual 2025-06 volumen
Espárrago anual 2025 precio_prom
Espárrago anual 2025 volumen
```

Además, se confirmaron algunas consultas diarias para `07/06/2026`:

```text
Palta diaria precio_prom
Palta diaria volumen
Uva diaria precio_prom
```

## 10. Data SISAP pendiente

Pendiente para convertir esto en dataset usable:

```text
1. Ejecutar extracción masiva mensual 2018-2026.
2. Incluir precio_prom, precio_min, precio_max y volumen.
3. Parsear las tablas HTML descargadas a CSV.
4. Confirmar arándano en "Otros fruticolas" o declarar no disponible en SISAP.
5. Si se requiere Excel, generar primero el HTML de reporte y luego enviar datos_a_enviar a exportarAExcel.
```

## 11. Recomendación de extracción

Prioridad para tesis:

```yaml
palta:
  mercado: "15011502"
  producto: "0626"
uva:
  mercado: "15011502"
  producto: "0637"
esparrago:
  mercado: "15011501"
  producto: "0216"
variables:
  - precio_prom
  - volumen
periodicidad: "mensual"
periodo: "2018-01 a 2026-06"
```

Arándano:

```yaml
estado: "pendiente"
accion: "buscar dentro de Otros fruticolas / validar manualmente si SISAP lo registra"
```

