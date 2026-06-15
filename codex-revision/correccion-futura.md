# Reporte de Correcciones Futuras y Líneas de Trabajo

Fecha: 2026-06-14  
Estado: Planificación de Trabajo Futuro  

---

## 1. Introducción y Propósito

Este documento detalla las correcciones metodológicas de mediano plazo, las optimizaciones de arquitectura y las líneas de investigación futuras identificadas durante las auditorías técnicas del sistema de supervisión operativa agroexportadora. Su propósito es servir como hoja de ruta para la continuidad del proyecto tras la defensa de la tesis, aportando transparencia y delimitando claramente los compromisos actuales frente a los desarrollos subsiguientes.

---

## 2. Inventario de Correcciones Futuras y Trabajos Pendientes

### A. Incremento del Tamaño de Muestra en el Estudio de Usabilidad (VD4)
*   **Contexto Actual:** El estudio de usabilidad con evaluadores humanos se acota a un grupo piloto controlado de $N = 15$ a $27$ participantes con perfiles profesionales en ingeniería o administración para registrar el "tiempo de decisión".
*   **Trabajo Futuro:** Ampliar la cohorte experimental a $N \geq 52$ analistas y auditores aduaneros activos en empresas del sector agroexportador peruano. Esto permitirá realizar pruebas de potencia estadística más robustas (como t-Student de muestras independientes o ANOVA de medidas repetidas) y generalizar los resultados con menor margen de error.

### B. Integración Productiva en Tiempo Real (Capa de Ingesta Dinámica)
*   **Contexto Actual:** El sistema procesa un dataset histórico estático o semiestático en formato DBF y CSV consolidado hasta mayo de 2026.
*   **Trabajo Futuro:** Desarrollar adaptadores de datos basados en WebSockets y Webhooks para conectarse en tiempo real con las APIs de la SUNAT, del SISAP/MIDAGRI y de sensores de temperatura IoT en contenedores. El pipeline operará con procesamiento de flujos (*stream processing*) mediante Apache Kafka o Spark Streaming.

### C. Evaluación Comparativa con Modelos de Deep Learning Tabular (Baselines)
*   **Contexto Actual:** La tesis prioriza modelos GBDT (XGBoost y LightGBM) debido a su óptimo desempeño en datos tabulares y bajo costo en CPU convencional.
*   **Trabajo Futuro:** Implementar, entrenar y comparar sistemáticamente arquitecturas de Deep Learning diseñadas para datos tabulares, tales como *TabNet* y *FT-Transformer*, utilizando tarjetas gráficas dedicadas (GPUs). Esto permitirá realizar un estudio de comparación empírica de rendimiento y coste computacional.

### D. Expansión y Validación del Cultivo Secundario (Espárrago)
*   **Contexto Actual:** El espárrago (*Asparagus officinalis*) está clasificado como producto secundario de validación condicionada (2,599 registros) debido a la menor consistencia temporal en algunas variables aduaneras.
*   **Trabajo Futuro:** Diseñar un pipeline de normalización específico para cultivos de menor densidad, aplicando técnicas avanzadas de imputación por vecinos más cercanos (k-NN) o imputación múltiple por ecuaciones encadenadas (MICE) para estabilizar el comportamiento del espárrago en el dataset de entrenamiento.

### E. Auditorías de Cumplimiento Regulatorio Externo (SBS / PCM)
*   **Contexto Actual:** La tesis adopta los principios de gobernanza del D.S. N° 115-2025-PCM y la Resolución SBS N° 053-2023 únicamente como conformidad de diseño metodológico.
*   **Trabajo Futuro:** Someter el prototipo a una auditoría formal de modelos de inteligencia artificial por una entidad de certificación regulatoria externa para validar el cumplimiento estricto del reglamento de la Ley de IA y auditar los Model Cards y Datasheets en un entorno empresarial de producción real.

---

## 3. Matriz de Priorización de Trabajos Futuros

| Código | Corrección / Trabajo Futuro | Prioridad | Dificultad | Impacto Académico |
| :--- | :--- | :--- | :--- | :--- |
| **CF-01** | Ampliación de muestra de usabilidad a $N \geq 52$ | Alta | Media | Muy Alto |
| **CF-02** | Integración de baselines TabNet / FT-Transformer | Media | Alta | Alto |
| **CF-03** | Pipeline de scraping en tiempo real (APIs SUNAT) | Baja | Alta | Medio |
| **CF-04** | Imputación avanzada MICE para espárrago | Media | Media | Medio-Alto |
| **CF-05** | Certificación regulatoria externa del framework | Baja | Muy Alta | Alto |

---

## 4. Sustentación de la Postergación

Las exclusiones actuales están sustentadas en criterios de viabilidad de recursos y rigor metodológico:
1.  **Presupuesto de Cómputo:** La limitación a modelos GBDT y detectores de PyOD en CPU responde a la necesidad de mantener el prototipo accesible para investigadores y PYMES agrarias sin inversión en infraestructura GPU.
2.  **Delimitación Temporal:** Al estar enfocados en la construcción del dataset histórico integrado (junio 2018 - mayo 2026), la integración en tiempo real representaría una carga operativa ajena a los objetivos académicos primarios.
3.  **Representatividad del Sector:** Priorizar palta, uva y arándano asegura que el framework sea evaluado sobre los cultivos que representan más del 65% de la canasta agroexportadora peruana, postergando otros cultivos menores para futuros trabajos de especialización.
