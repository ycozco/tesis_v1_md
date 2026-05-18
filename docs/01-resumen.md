# RESUMEN

Esta tesis propone un sistema integrado de supervisión operativa para empresas agroexportadoras peruanas, que combina predicción tabular mediante modelos GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente), detección de anomalías operativas mediante ensemble de algoritmos, explicabilidad mediante SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley), y generación automática de reportes trazables con LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño) en arquitectura RAG (Retrieval-Augmented Generation).

El sistema aborda una brecha identificada en el contexto agroexportador: los procesos de producción, acopio, almacenamiento, control de calidad, logística, cumplimiento fitosanitario y comercialización internacional suelen analizarse mediante fuentes fragmentadas, reportes manuales o tableros aislados. Esta fragmentación dificulta la detección temprana de anomalías y reduce la trazabilidad de las decisiones. La propuesta se evalúa con métricas técnicas (PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad), F1-Score (Medida Armónica de Precisión y Exhaustividad), cobertura de trazabilidad), evaluación de comprensión operativa y datos públicos/sintéticos documentados del dominio agroexportador.

Las contribuciones principales son: (1) arquitectura modular de cuatro capas que separa predicción, detección, explicación y reporte; (2) integración de fuentes públicas oficiales y dataset sintético agroexportador documentado mediante criterios de Datasheets for Datasets (Gebru et al., 2021); (3) uso de SHAP para explicar alertas operativas a nivel de variable; (4) generación de reportes mediante RAG restringido a evidencias estructuradas, reduciendo el riesgo de alucinación; (5) evaluación comparativa del sistema integrado frente a componentes aislados en rendimiento, trazabilidad y tiempo de interpretación. La Resolución SBS N° 053-2023 se considera como referencia nacional de buenas prácticas para gestión de riesgo de modelos, mientras que el D.S. N° 115-2025-PCM se adopta como marco peruano general de gobernanza y supervisión humana en IA.

**Palabras clave**: supervisión operativa, detección de anomalías, agroexportación, explicabilidad IA, modelos de lenguaje, gobernanza, GBDT, reportes automáticos, trazabilidad, inteligencia artificial.

---

# ABSTRACT

This thesis proposes an integrated operational supervision system for Peruvian agro-export companies, combining tabular prediction using Gradient Boosting Decision Trees (GBDT), operational anomaly detection through an ensemble of algorithms, explainability through SHAP (SHapley Additive exPlanations), and traceable automatic report generation with Large Language Models (LLMs) in a RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación) architecture.

The system addresses an identified gap in agro-export operational supervision: production, storage, quality control, logistics, phytosanitary compliance, and international commercialization are commonly analyzed through fragmented sources, manual reports, or isolated dashboards. This fragmentation limits early anomaly detection and weakens decision traceability. The proposal is evaluated using technical metrics (PR-AUC, F1-Score, traceability coverage), operational comprehension assessment, and documented public/synthetic agro-export data.

The main contributions are: (1) a modular four-layer architecture separating prediction, detection, explanation, and reporting; (2) integration of official public sources and a documented synthetic agro-export dataset; (3) SHAP-based explanation of operational alerts; (4) evidence-restricted RAG reporting to reduce hallucination risk; and (5) comparative evaluation of the integrated system against isolated components in terms of detection performance, traceability, and interpretation time. Peruvian Resolution SBS N° 053-2023 is used only as a national reference for model risk management practices, while D.S. N° 115-2025-PCM is adopted as the general Peruvian AI governance framework.

**Keywords**: operational supervision, anomaly detection, agro-export, AI explainability, language models, governance, GBDT, automatic reports, traceability, artificial intelligence.

---

