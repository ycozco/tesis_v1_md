# CAPÍTULO IV: RESULTADOS Y DISCUSIÓN

> **Pendiente:** Capítulo IV — requiere dataset sintético y experimentos (Fases 1-3)


## 4.1 Resultados Cuantitativos (Predicción y Detección)

*(Sección reservada para la inserción de métricas resultantes: PR-AUC del ensemble GBDT, comparativa detector único vs. ensemble, velocidad de inferencia de LightGBM respecto a XGBoost, y comparativas de forecasting entre TFT y DLinear [@zeng2023dlinear] como baseline).*

## 4.2 Resultados Cualitativos (Generación de Reportes LLM-RAG)

*(Sección reservada para ilustrar cómo el módulo LLM+RAG transforma los vectores SHAP crudos en explicaciones narrativas auditables, con ejemplos de reportes generados y evaluación ROUGE-1 vs. referencia humana).*

## 4.3 Discusión de Resultados

La arquitectura propuesta se evaluará frente a enfoques basados en componentes aislados, considerando rendimiento técnico, trazabilidad documental y utilidad para la supervisión operativa agroexportadora.

### 4.3.1 Superioridad de GBDT sobre Deep Learning en Datos Tabulares

Los hallazgos se discutirán a la luz del benchmark de Grinsztajn et al. [-@grinsztajn2022trees], que respalda el uso de modelos basados en árboles para datos tabulares. En el contexto agroexportador, esta elección se justifica por la heterogeneidad de variables como precio, volumen, clima, producto, zona, destino y cumplimiento fitosanitario. Los trabajos de fraude financiero y auditoría se conservarán solo como antecedentes metodológicos sobre datos tabulares desbalanceados y explicabilidad, no como evidencia principal del dominio.

### 4.3.2 Restricción Determinista de LLMs frente al Riesgo de Alucinación

En contraste con arquitecturas donde el LLM actúa como agente autónomo de toma de decisiones [@park2024llm], este sistema relega al LLM estrictamente a la capa de traducción narrativa mediante RAG [@schneider2025rag]. Esta decisión reduce el riesgo documentado de alucinaciones [@survey2026hallucination]. Al restringir al LLM a interpretar scores, umbrales, variables SHAP y contexto recuperado, el sistema mantiene fidelidad a las evidencias operativas.

### 4.3.3 Cumplimiento Regulatorio y Gobernanza

La interpretabilidad post-hoc (SHAP) implementada en el sistema responde a principios modernos de gobernanza de IA: transparencia, documentación, supervisión humana y trazabilidad. En el contexto nacional, el D.S. N° 115-2025-PCM [@pcm2025leyia] proporciona el marco general de IA responsable. La Resolución SBS N° 053-2023 [@sbs2023riesgos] se utiliza como referencia nacional de buenas prácticas para gestión de riesgo de modelos, sin asumir obligación directa para empresas agroexportadoras. A nivel internacional, el EU AI Act [@eu2024aiact] y NIST AI RMF [@nist2023aia] refuerzan la necesidad de documentar decisiones y riesgos de sistemas de IA.

---

