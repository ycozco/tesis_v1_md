# Informe tecnico: uso de datos en SHAP y RAG

Este documento explica como los datos del dataset agroexportador integrado alimentan las capas 2, 3 y 4 del sistema.

## 1. Flujo de evidencia

```
Dataset integrado
   -> Capa 1: prediccion tabular
   -> Capa 2: score de anomalia
   -> Capa 3: SHAP top-k
   -> Capa 4: reporte RAG trazable
```

Cada alerta debe transportar:

- `id` del registro.
- Version del dataset.
- Fuente y archivo de origen.
- Modelo usado.
- Score y umbral.
- Variables SHAP top-k.
- Evidencia recuperada por RAG.
- Reporte generado.

## 2. Uso en deteccion de anomalias

La Capa 2 consume variables numericas y categoricas procesadas. Los scores de IF, LOF y ECOD se normalizan antes de agregarse. Si la etiqueta de anomalia proviene de reglas o sinteticos, debe documentarse.

## 3. Uso en SHAP

SHAP explica contribuciones del modelo. No establece causalidad. Las variables SHAP deben ser interpretables y tener fuente documentada:

- comercio exterior: SUNAT/ADUANET;
- mercado interno: SISAP;
- macro: BCRP;
- clima/logistica/sanidad: proxies;
- sinteticos: escenarios controlados.

## 4. Uso en RAG/LLM

El RAG debe recuperar evidencia desde:

- metadatos del registro;
- score y umbral;
- top variables SHAP;
- descripcion de fuente;
- documentos de contexto.

El LLM no puede inventar numeros, causas ni recomendaciones. Debe narrar solo lo que aparece en evidencias estructuradas.

## 5. Regla de trazabilidad

Un reporte es valido solo si permite reconstruir:

`dato -> transformacion -> modelo -> score -> SHAP -> fuente recuperada -> reporte`.

---
