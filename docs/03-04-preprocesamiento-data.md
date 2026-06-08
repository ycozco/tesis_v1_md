# Informe tecnico: preprocesamiento de datos

El preprocesamiento transforma datos crudos y agregados en un dataset modelable. La version actual separa datos reales observados, reales agregados, proxies y sinteticos controlados.

## 1. Principios

1. Evitar fuga de informacion temporal.
2. Ajustar imputadores, codificadores y escaladores solo con train.
3. Mantener trazabilidad de fuente, archivo y granularidad.
4. Separar datos sinteticos del test real.
5. No unir fuentes agregadas a nivel embarque si no existe llave directa.

## 2. Limpieza comun

| Paso | Regla |
|---|---|
| Productos | Normalizar a palta, uva, arandano y esparrago; excluir cacao. |
| HS | Homologar `080440`, `080610`, `081040`, `070920`. |
| Fechas | Crear `fecha` y `periodo_mes`. |
| Unidades | Convertir toneladas a kg y miles USD a USD cuando corresponda. |
| Duplicados | Remover exactos y funcionales. |
| Nulos | Separar nulos estructurales de errores. |
| Outliers | Reportar antes de decidir excluir o winsorizar. |

## 3. Tratamiento por fuente

| Fuente | Tratamiento |
|---|---|
| SUNAT/ADUANET | Extraer DBF/ZIP, filtrar HS objetivo, deduplicar DUA/serie, calcular precio FOB/kg. |
| Trade Map | Parsear `.xls` HTML, conservar solo `export_*`, normalizar paises y unidades. |
| SISAP | Agregar por producto/mes; no usar para arandano. |
| BCRP | Elegir una serie canonica y unir por `periodo_mes`. |
| Clima/logistica/sanidad | Integrar como proxies agregados por region/mes, puerto/mes o producto/destino/mes. |
| Sinteticos | Usar solo en train o escenarios auxiliares; marcar origen. |

## 4. Split temporal

| Particion | Porcentaje | Uso |
|---|---:|---|
| Train | 70% | Ajuste de modelos y balanceo. |
| Validation | 10% | Hiperparametros y umbrales. |
| Test | 20% | Evaluacion final. |

SMOTE o balanceo sintetico solo puede aplicarse sobre train. El test final debe conservar la distribucion real o documentada.

## 5. Salidas esperadas

- `dataset_train_raw.csv`
- `dataset_train_balanced.csv`
- `dataset_validation.csv`
- `dataset_test.csv`
- `dataset_inference_examples.csv`
- `reporte-calidad-datos.md`

---
