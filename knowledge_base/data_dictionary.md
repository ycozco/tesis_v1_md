# Diccionario de Datos del Sistema de Supervisión Agroexportadora

Este documento define las variables operacionales, macroeconómicas, climáticas y logísticas utilizadas en el pipeline de análisis de exportaciones.

## Variables de Comercio Exterior (SUNAT)
* **fob_unit_value_usd_kg**: Valor Unitario FOB en dólares americanos por kilogramo. Se calcula como el valor FOB total de la exportación dividido por el peso neto en kilogramos.
* **total_net_weight_kg**: Peso neto total en kilogramos de los envíos realizados en la semana para el producto y mercado indicados.
* **total_fob_usd**: Valor total FOB en dólares de los envíos realizados en la semana para el producto y mercado indicados.
* **shipment_count**: Cantidad de embarques (declaraciones de exportación) realizados en la semana.
* **exporter_count**: Cantidad de empresas exportadoras únicas que registraron envíos en la semana.
* **weeks_since_last_export**: Número de semanas transcurridas desde el último envío registrado para la combinación de producto y mercado de destino.

## Variables de Mercado Mayorista (SISAP/MIDAGRI)
* **precio_mayorista_interno**: Precio promedio mayorista interno en soles por kilogramo (PEN/kg) del producto en el mercado nacional mayorista (ej. GMML). Funciona como proxy de la oferta interna y el costo local.

## Variables Macroeconómicas (BCRP)
* **tipo_cambio_pen_usd**: Tipo de cambio promedio mensual del sol peruano frente al dólar estadounidense, obtenido del Banco Central de Reserva del Perú (BCRP). Afecta directamente la competitividad y los márgenes de exportación.

## Variables Climatológicas (NASA POWER / SENAMHI)
* **temperatura_max_c**: Temperatura máxima promedio registrada en la zona de cultivo durante la semana.
* **temperatura_min_c**: Temperatura mínima promedio registrada en la zona de cultivo durante la semana.
* **precipitacion_mm**: Lluvia acumulada semanal en la zona de cultivo expresada en milímetros.
* **humedad_pct**: Humedad relativa promedio semanal expresada en porcentaje.

## Variables Logísticas y de Calidad (Proxies OSITRAN / SENASA)
* **dias_logisticos**: Tiempo transcurrido en días desde la numeración de la DUA hasta el embarque efectivo del contenedor en el puerto.
* **costo_logistico_usd_kg**: Estimación del costo logístico de transporte y puerto por kilogramo exportado.
* **cumplimiento_fitosanitario**: Indicador binario (1 si cumple, 0 si no) sobre la ausencia de rechazos fitosanitarios por parte de autoridades en destino (ej. FDA, RASFF).
* **merma_pct**: Porcentaje de pérdida física estimada del producto durante el tránsito logístico y cadena de frío, modelado mediante la perecibilidad del cultivo y las condiciones climáticas.
