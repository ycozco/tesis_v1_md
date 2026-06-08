## Anexo E - Resumen general del sistema

Este anexo resume la investigacion bajo la version metodologica actual: sistema integrado de supervision operativa con IA explicable y dataset agroexportador integrado.

## 1. Arquitectura modular

| Capa | Funcion |
|---|---|
| Capa 1 | Prediccion tabular con XGBoost/LightGBM. |
| Capa 2 | Deteccion de anomalias con IF + LOF + ECOD. |
| Capa 3 | Explicabilidad con SHAP/TreeSHAP. |
| Capa 4 | Reportes trazables con RAG/LLM. |

## 2. Base de datos

La evaluacion final debe basarse en un dataset agroexportador integrado:

- SUNAT/ADUANET y dataset real local como base observada.
- Trade Map como benchmark externo.
- SISAP/MIDAGRI como mercado interno para palta, uva y esparrago.
- BCRP como control macro.
- Clima, logistica y sanidad como proxies.
- Sinteticos solo como apoyo experimental.

## 3. Productos

| Producto | Estado |
|---|---|
| Palta | Nucleo. |
| Uva | Nucleo. |
| Arandano | Nucleo. |
| Esparrago | Secundario condicionado. |
| Cacao | Excluido. |

## 4. Estado de resultados

Los resultados obtenidos sobre versiones sinteticas o corridas previas deben considerarse preliminares hasta ejecutar el entrenamiento final sobre el dataset integrado. No se deben presentar como conclusiones finales si no cuentan con reporte de entrenamiento, version de dataset y trazabilidad.

## 5. Gobernanza y trazabilidad

Cada alerta valida debe incluir:

- dato de origen;
- version del dataset;
- modelo y parametros;
- score y umbral;
- variables SHAP;
- fuente recuperada por RAG;
- reporte generado.

---
