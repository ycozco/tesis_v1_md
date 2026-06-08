# RESUMEN

Esta tesis propone un sistema integrado de supervision operativa para empresas agroexportadoras peruanas, basado en un dataset agroexportador integrado y trazable. La arquitectura combina prediccion tabular mediante modelos GBDT (Gradient Boosting Decision Trees), deteccion de anomalias operativas mediante ensemble de algoritmos, explicabilidad mediante SHAP (SHapley Additive exPlanations) y generacion automatica de reportes tecnicos con LLMs en arquitectura RAG (Retrieval-Augmented Generation).

El problema abordado es la fragmentacion de datos agroexportadores y la baja trazabilidad entre fuentes de comercio exterior, mercado interno, variables macroeconomicas, clima, logistica y sanidad. En este contexto, la investigacion se orienta a productos priorizados de agroexportacion peruana: palta, uva y arandano como nucleo; esparrago como producto secundario condicionado a cobertura suficiente; y cacao como producto excluido de la evaluacion principal por baja representatividad en el dataset real auditado.

La propuesta utiliza SUNAT/ADUANET como fuente primaria de exportaciones reales, Trade Map como benchmark externo, SISAP/MIDAGRI como contexto de mercado interno mayorista, BCRP para variables macroeconomicas, y fuentes climaticas, logisticas y sanitarias como proxies documentados. Los datos sinteticos controlados se restringen a escenarios experimentales, balanceo de clases, simulacion de alertas o vacios no observables con fuentes publicas, siempre identificados mediante etiquetas metodologicas.

Las contribuciones principales son: (1) una arquitectura modular de cuatro capas que separa prediccion, deteccion, explicacion y reporte; (2) un enfoque de dataset agroexportador integrado con datos reales observados, datos reales agregados, proxies y sinteticos controlados; (3) uso de SHAP para explicar la contribucion de variables en alertas operativas; (4) reportes RAG restringidos a evidencia estructurada, score, metadatos y version de dataset; y (5) una metodologia de evaluacion que compara rendimiento tecnico, trazabilidad, comprension operativa y tiempo-a-decision. La Resolucion SBS N. 053-2023 se considera como referencia nacional de buenas practicas para gestion de riesgo de modelos, mientras que el D.S. N. 115-2025-PCM se adopta como marco peruano general de gobernanza y supervision humana en IA.

**Palabras clave**: supervision operativa, agroexportacion, dataset integrado, deteccion de anomalias, explicabilidad IA, SHAP, RAG, GBDT, trazabilidad, inteligencia artificial.

---

# ABSTRACT

This thesis proposes an integrated operational supervision system for Peruvian agro-export companies, based on a traceable integrated agro-export dataset. The architecture combines tabular prediction with Gradient Boosting Decision Trees (GBDT), operational anomaly detection through an algorithmic ensemble, explainability with SHAP (SHapley Additive exPlanations), and automatic technical report generation with Large Language Models (LLMs) in a Retrieval-Augmented Generation (RAG) architecture.

The research addresses the fragmentation of agro-export data and the weak traceability between foreign trade, domestic market, macroeconomic, climate, logistics, and sanitary sources. The study focuses on avocado, grape, and blueberry as core products; asparagus as a secondary product subject to coverage validation; and cocoa as excluded from the main evaluation due to low representativeness in the audited real dataset.

The proposal uses SUNAT/ADUANET as the primary source for real export data, Trade Map as an external benchmark, SISAP/MIDAGRI as domestic wholesale market context, BCRP for macroeconomic variables, and climate, logistics, and sanitary sources as documented proxies. Controlled synthetic data are limited to experimental scenarios, class balancing, alert simulation, or non-public data gaps, and must always be explicitly labeled.

The main contributions are: (1) a modular four-layer architecture separating prediction, detection, explanation, and reporting; (2) an integrated agro-export dataset approach combining observed real data, aggregated real data, proxies, and controlled synthetic data; (3) SHAP-based attribution of variables in operational alerts; (4) evidence-restricted RAG reports using structured evidence, scores, metadata, and dataset versions; and (5) an evaluation methodology covering technical performance, traceability, operational comprehension, and time-to-decision.

**Keywords**: operational supervision, agro-export, integrated dataset, anomaly detection, AI explainability, SHAP, RAG, GBDT, traceability, artificial intelligence.
