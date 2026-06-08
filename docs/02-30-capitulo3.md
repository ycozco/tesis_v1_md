<div style="background-color: orange; color: white; padding: 10px; text-align: center; font-weight: bold; margin-bottom: 20px; border-radius: 5px;">EN DESARROLLO</div>

# CAPITULO III: PROPUESTA METODOLOGICA

## 3.1 Arquitectura del sistema integrado

La arquitectura propuesta se divide en cuatro capas secuenciales y trazables:

1. **Capa 1: Prediccion tabular.** Modelos GBDT, principalmente XGBoost y LightGBM, estiman valores esperados de precio o volumen usando variables comerciales, macroeconomicas, climaticas, logisticas y de contexto.
2. **Capa 2: Deteccion de anomalias.** Un ensemble de Isolation Forest, LOF y ECOD produce un score de anomalia. El LLM no detecta anomalias.
3. **Capa 3: Explicabilidad.** SHAP/TreeSHAP identifica las variables con mayor contribucion a la alerta. Las explicaciones son atribuciones del modelo, no causalidad.
4. **Capa 4: Reportes RAG/LLM.** Un LLM restringido por evidencias redacta reportes tecnicos a partir de datos, score, umbral, SHAP, fuente y metadatos.

```
[Dataset agroexportador integrado]
        |
        v
[Capa 1: GBDT] -> valor esperado / residuo
        |
        v
[Capa 2: IF + LOF + ECOD] -> score anomalia
        |
        v
[Capa 3: SHAP] -> top variables explicativas
        |
        v
[Capa 4: RAG/LLM] -> reporte trazable
```

## 3.2 Dataset agroexportador integrado y trazable

La validacion principal no dependera de un dataset sintetico aislado. Se trabajara con un **dataset agroexportador integrado**, construido desde cuatro tipos de informacion:

| Capa de datos | Fuentes | Rol |
|---|---|---|
| Datos reales observados | SUNAT/ADUANET, `data/dataset_real_v1.csv` | Base primaria de exportaciones. |
| Datos reales agregados | Trade Map, SISAP/MIDAGRI, BCRP, MIDAGRI compendios, FAOSTAT | Validacion externa y contexto. |
| Proxies documentados | NASA POWER, SENAMHI, APN, OSITRAN, SENASA/FDA/RASFF | Variables explicativas agregadas. |
| Datos sinteticos controlados | `data/dataset_agro_sintetico_v1.csv` y reglas de inyeccion | Escenarios auxiliares, balanceo y etiquetas experimentales. |

### 3.2.1 Segmentacion de productos

| Producto | HS | Decision |
|---|---|---|
| Palta | `080440` | Producto nucleo. |
| Uva | `080610` | Producto nucleo. |
| Arandano | `081040` | Producto nucleo; sin dependencia de SISAP. |
| Esparrago | `070920` | Producto secundario condicionado. |
| Cacao | Verificar | Excluido del nucleo por baja representatividad. |

### 3.2.2 Uso de fuentes

- **SUNAT/ADUANET:** fuente primaria para volumen, valor FOB, partida, fecha, empresa y destino.
- **Trade Map:** benchmark internacional por producto y mercado destino.
- **SISAP/MIDAGRI:** precio y volumen mayorista interno para palta, uva y esparrago; no mide exportaciones.
- **BCRP:** tipo de cambio mensual.
- **Clima/logistica/sanidad:** proxies agregados cuando no existe llave directa por embarque.
- **Sinteticos:** escenarios controlados y balanceo, siempre etiquetados.

## 3.3 Configuracion experimental y metricas

### 3.3.1 Division temporal

Para evitar fuga de informacion temporal:

- Train: 70% inicial.
- Validation: 10% siguiente.
- Test: 20% final.

El split aleatorio no se usara como evaluacion principal.

### 3.3.2 Metricas por variable dependiente

| VD | Metricas |
|---|---|
| VD1 rendimiento | PR-AUC, ROC-AUC, F1, precision, recall. |
| VD2 explicabilidad | Cobertura top-k SHAP, estabilidad, claridad. |
| VD3 reportes | Rubrica de completitud, consistencia, accionabilidad y evidencia. |
| VD4 decision | Tiempo-a-decision, Likert, decision correcta. |
| VD5 trazabilidad | Porcentaje de alertas con campos completos. |

### 3.3.3 Experimentos E1-E5

| Exp. | Nombre | Condicion experimental | Control | VD |
|---|---|---|---|---|
| E1 | Rendimiento de deteccion | Ensemble IF + LOF + ECOD | Detectores individuales | VD1 |
| E2 | Aporte SHAP | Alertas con SHAP | Alertas solo con score | VD2 |
| E3 | Aporte RAG | Reporte RAG anclado | LLM sin RAG | VD3 |
| E4 | Sistema integrado | Pipeline completo | Componentes aislados | VD4, VD5 |
| E5 | Ablation | Variantes por capas | Pipeline completo | VD1, VD5 |

### 3.3.4 Baselines

- B1: Isolation Forest individual.
- B2: Ensemble IF + LOF.
- B3: XGBoost supervisado si existe etiqueta confiable.
- B4: LLM sin RAG ni evidencia SHAP.

## 3.4 Reproducibilidad

Cada corrida debe registrar:

- Version del dataset.
- Fecha de generacion.
- Fuentes usadas.
- Semilla.
- Particion temporal.
- Modelo y parametros.
- Metricas.
- Reporte de trazabilidad.

---
