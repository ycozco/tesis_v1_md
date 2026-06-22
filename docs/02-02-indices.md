# ÍNDICE DE CONTENIDOS

- DEDICATORIA
- AGRADECIMIENTOS
- PRESENTACIÓN
- RESUMEN
- ABSTRACT
- ÍNDICE DE CONTENIDOS
- ÍNDICE DE FIGURAS
- ÍNDICE DE TABLAS
- ÍNDICE DE FÓRMULAS
- INTRODUCCIÓN
- **CAPÍTULO I: PLANTEAMIENTO DEL PROBLEMA**
  - 1.1 Descripción de la Realidad Problemática
  - 1.2 Problema Principal
  - 1.3 Objetivos
  - 1.4 Hipótesis de la Investigación
  - 1.5 Variables e Indicadores
  - 1.6 Viabilidad de la Investigación
  - 1.7 Justificación e Importancia
  - 1.8 Alcance
  - 1.9 Línea, Tipo y Nivel de la Investigación
  - 1.10 Técnicas e Instrumentos de Recolección de Información
  - 1.11 Cronograma de Actividades
- **CAPÍTULO II: MARCO TEÓRICO**
  - 2.1 Antecedentes de la Investigación
  - 2.2 Estado del Arte
  - 2.3 Marco Conceptual
- **CAPÍTULO III: ELABORACIÓN DE LA PROPUESTA**
  - 3.1 Generalidades de la Propuesta
  - 3.2 Esquema de la Propuesta
  - 3.3 Obtención y Preparación de Datos
  - 3.4 Diseño e Implementación del Prototipo
  - 3.5 Diseño Experimental y Validación
- **CAPÍTULO IV: RESULTADOS Y DISCUSIÓN**
  - 4.1 Estado de Implementación del Prototipo
  - 4.2 Resultados Cuantitativos: Predicción y Detección
  - 4.3 Explicabilidad Local y Reportes Automáticos
  - 4.4 Usabilidad y Trazabilidad
  - 4.5 Discusión y Cruce Comparativo
  - 4.6 Limitaciones de los Resultados
  - 4.7 Síntesis del Capítulo IV
- **CAPÍTULO V: CONCLUSIONES Y TRABAJOS FUTUROS**
  - 5.1 Conclusiones
  - 5.2 Limitaciones
  - 5.3 Trabajos Futuros
- CRONOGRAMA DE ACTIVIDADES
- CONCLUSIONES
- RECOMENDACIONES
- GLOSARIO DE TÉRMINOS
- REFERENCIAS BIBLIOGRÁFICAS
- ANEXOS

---

# ÍNDICE DE FIGURAS

- Figura 3.1 — Arquitectura lógica del sistema integrado
- Figura 3.2 — Flujo temporal de datos, predicción, alerta y reporte
- Figura 3.3 — Modelo lógico de trazabilidad de alerta, explicación y reporte
- Figura 4.1 — Vista de detalle de alerta del prototipo funcional
- Figura 4.2 — Consola de telemetría experimental del prototipo
- Figura 4.3 — Bandeja de gestión de alertas
- Figura 4.4 — Configuración de modelo y umbrales
- Figura 4.5 — Explorador de datos y biblioteca RAG
- Figura 4.6 — Importancia global SHAP para FOB
- Figura 4.7 — Importancia global SHAP para volumen
- Figura 4.8 — Distribución SHAP para FOB
- Figura 4.9 — Distribución SHAP para volumen

---

# ÍNDICE DE TABLAS

- Tabla 1.1 — Variables e Indicadores
- Tabla 1.2 — Cronograma de Actividades
- Tabla 1.3 — Técnicas e Instrumentos de Recolección
- Tabla 2.1 — Comparativa de Sistemas de Supervisión con IA
- Tabla 2.2 — Resumen del Estado del Arte por Bloques Temáticos
- Tabla 3.1 — Mapeo de módulos, rutas, entradas, salidas y evidencia
- Tabla 3.2 — Inventario reproducible de archivos principales
- Tabla 3.3 — Caracterización del dataset semanal gold
- Tabla 3.4 — Controles de calidad temporal y prevención de fuga de información
- Tabla 3.5 — Checklist verificable de cierre del Capítulo III
- Tabla 4.1 — Rendimiento de detección en experimento preliminar
- Tabla 4.2 — Recall por tipo de anomalía
- Tabla 4.3 — Rendimiento predictivo de XGBoost
- Tabla 4.4 — Atribuciones SHAP promedio por variable
- Tabla 4.5 — Rúbrica de calidad de reportes RAG
- Tabla 4.6 — Documentos recuperados por tipo de alerta
- Tabla 4.7 — Telemetría de usabilidad
- Tabla 4.8 — Campos de trazabilidad completos

---

# ÍNDICE DE FÓRMULAS

- Fórmula 1 — Función objetivo GBDT: $F^*(x) = \arg\min_F \mathbb{E}[L(y, F(x))]$
- Fórmula 2 — Iteración GBDT: $F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)$
- Fórmula 3 — Local Outlier Factor: $\text{LOF}_k(p)$
- Fórmula 4 — Score robusto de residuo: $z_r(t)=\frac{r(t)-\text{mediana}(r_{t-13:t-1})}{\text{MAD}(r_{t-13:t-1})}$
- Fórmula 5 — Score ensemble de anomalía: $s=\sum_i w_i p_i$
- Fórmula 6 — Valor SHAP: $\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!}[f(S\cup\{i\})-f(S)]$

---
