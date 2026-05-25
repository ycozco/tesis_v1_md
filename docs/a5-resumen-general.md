## Anexo E — Resumen General del Sistema y Resultados de la Investigación

Este anexo ofrece una síntesis consolidada de la investigación titulada **"Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas"**, diseñada como una guía de referencia rápida para evaluadores, auditores y tomadores de decisiones.

---

### 1. Arquitectura Modular del Sistema (4 Capas)

La arquitectura modular del sistema separa de forma estricta las responsabilidades algorítmicas deterministas (Capas 1, 2 y 3) de la narración asistida (Capa 4) para garantizar la trazabilidad y eliminar el riesgo de alucinaciones en entornos regulados:

```
┌────────────────────────────────────────────────────────┐
│ Capa 4 — Reportes Narrativos LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño) (Large Language       │
│ Model - Modelo de Lenguaje de Gran Tamaño) + RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)       │ ← Generación de reportes trazables a partir de
│ (Retrieval-Augmented Generation - Generación           │   las evidencias estructuradas de las Capas 1-3.
│ Aumentada por Recuperación)                            │
└────────────────────────────────────────────────────────┘
                           ▲
┌────────────────────────────────────────────────────────┐
│ Capa 3 — Explicabilidad Algorítmica con SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)           │
│ (SHapley Additive exPlanations - Explicaciones         │ ← TreeSHAP exacto para calcular la contribución
│ Aditivas de Shapley)                                   │   del top-5 de variables operativas de la alerta.
└────────────────────────────────────────────────────────┘
                           ▲
┌────────────────────────────────────────────────────────┐
│ Capa 2 — Detección de Anomalías (Ensemble)             │ ← Combinación robusta de IF (Isolation Forest - Bosque de Aislamiento),
│                                                        │   LOF (Local Outlier Factor - Factor de Anomalía Local) y ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica) (Empirical
│                                                        │   Cumulative Distribution Outlier Detection).
└────────────────────────────────────────────────────────┘
                           ▲
┌────────────────────────────────────────────────────────┐
│ Capa 1 — Predicción Tabular GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) (Gradient Boosting   │ ← XGBoost (eXtreme Gradient Boosting) y
│ Decision Trees - Árboles de Decisión de Aumento de     │   LightGBM (Light Gradient Boosting Machine)
│ Gradiente)                                             │   para estimar valores esperados.
└────────────────────────────────────────────────────────┘
```

---

### 2. Hallazgos y Resultados de los Experimentos (E1 a E5)

La evaluación empírica del sistema sobre el dataset sintético agroexportador calibrado (10,000 registros operativos transaccionales) arrojó los siguientes resultados clave:

*   **Rendimiento de Detección Operativa (Ensemble vs. Baselines)**: El Stacking Ensemble de detectores de anomalías de la Capa 2 (IF + LOF + ECOD) alcanzó un rendimiento sobresaliente de **PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad) (Precision-Recall Area Under the Curve) = 0.92** y un **F1-Score (Medida Armónica de Precisión y Exhaustividad) = 0.88**, superando ampliamente a los baselines de detección individuales (como LOF aislado que obtuvo PR-AUC = 0.74 debido a problemas de *sparsity* local y baja densidad). Esto demuestra el efecto sinérgico de combinar enfoques basados en aislamiento espacial, densidad local y funciones de distribución acumulada empírica.
*   **Comprensión y Tiempo de Decisión (VD4)**: El estudio de usabilidad cuasi-experimental *within-subjects* realizado con supervisores operativos demostró que el uso del **sistema integrado** (Capa 1 a 4) redujo el tiempo promedio de interpretación de una alerta operativa de **245 segundos** (empleando salidas técnicas aisladas en silos) a solo **65 segundos** (empleando el reporte narrativo trazable de la Capa 4). Asimismo, la comprensión cualitativa medida en escala Likert se incrementó de **2.1/5** a **4.8/5**, y las decisiones operativas correctas alcanzaron un **100% de precisión**.
*   **Trazabilidad Documental End-to-End (VD5)**: Se validó que el **98.5%** de las alertas generadas por el sistema integrado cumplieron satisfactoriamente con el checklist completo de trazabilidad (registrando de manera inalterable: ID del dato transaccional, modelo predictivo ejecutor, puntaje de anomalía obtenido, umbral de decisión, variables explicativas SHAP del top-5, fuentes externas recuperadas por RAG y el reporte final en texto plano).

---

### 3. Marco de Cumplimiento Ético y Gobernanza

El diseño de la solución se construyó en estricta conformidad con el marco regulatorio nacional e internacional vigente para garantizar una adopción ética y segura en el tejido empresarial peruano:

1.  **Gobernanza de IA (D.S. N° 115-2025-PCM)**: Se cumple el principio de transparencia mediante la Capa 3 (SHAP) y la supervisión humana (Human-in-the-Loop) en la Capa 4, garantizando que el LLM no tome decisiones autónomas, sino que actúe estrictamente como un asistente de redacción para el supervisor humano responsable.
2.  **Gestión del Riesgo de Modelos (Resolución SBS N° 053-2023)**: Adoptada como marco metodológico de referencia para documentar el ciclo de vida del dato (Datasheets for Datasets), control de cambios del pipeline predictivo, pruebas de estrés y monitoreo de la degradación del rendimiento de los modelos frente al *concept drift* temporal.
3.  **Seguridad y Privacidad de la Información**: Se implementó una arquitectura de desacoplamiento de datos transaccionales, donde los datos confidenciales permanecen seguros y el RAG opera sobre índices vectoriales anonimizados y repositorios locales estructurados de auditoría.

---

*(Fin del documento — Resumen de Consistencia Metodológica, UNSA Arequipa, 2026)*
