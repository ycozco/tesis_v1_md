# Informe de Revisión y Dictamen Crítico de Tesis
**Nivel:** Jurado Evaluador Académico (Ingeniería de Sistemas / IA / Ciencia de Datos)  
**Proyecto:** *Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas*  
**Autor:** Yoset Cozco Mauri  
**Fecha de Evaluación:** 18 de Mayo de 2026

---

## 🔍 Resumen del Dictamen del Jurado
Tras una evaluación exhaustiva del manuscrito monolítico (`docs/tesis.md`), los capítulos individuales en `docs/` y el repositorio de código, este jurado dictamina que la tesis presenta una **propuesta metodológica innovadora, rigurosa y altamente relevante** para el sector agroexportador peruano. La separación de responsabilidades en 4 capas y la justificación teórica del ensemble (IF+LOF+ECOD), explicabilidad (SHAP) y RAG son excepcionales.

Sin embargo, el manuscrito en su estado actual **no es apto para sustentación** y recibirá una **Observación Mayor Inmediata** debido a un factor crítico: **toda la sección de resultados empíricos (Capítulo IV) y sus cruces metodológicos están en blanco o marcados con el marcador `_pendiente_`**. Un jurado no puede validar hipótesis científicas sobre placeholders.

A continuación, se presenta el análisis crítico detallado dividido en 5 dimensiones fundamentales, junto con las acciones correctivas obligatorias para levantar las observaciones.

---

## 1. Capítulo IV y Resultados Empíricos: El Bloqueador Crítico
> [!CAUTION]
> **OBSERVACIÓN CRÍTICA**: La presencia de marcadores `_pendiente_` en las tablas 4.1 a 4.7 y 4.12, así como en las decisiones de hipótesis en la Tabla 4.9, invalida la naturaleza científica de la tesis. Un jurado de tesis rechazará el manuscrito de inmediato bajo el cargo de "investigación incompleta".

### Puntos Críticos:
*   **Decisión de Hipótesis en el Aire**: En la Tabla 4.9 (*Cruce 2 — Contraste de hipótesis*), todas las decisiones sobre H1a, H1b, H1c y H1d están marcadas como `_pendiente_`. Las conclusiones del Capítulo V no tienen sustento lógico si estas decisiones no están formalizadas con datos reales.
*   **Ejemplo de Reporte Vacío (§4.2.3)**: El manuscrito indica *"Espacio reservado para insertar un reporte real de muestra"*. El jurado exige ver el reporte real generado para evaluar el riesgo de alucinaciones y la consistencia numérica.

### Acción Correctiva Obligatoria:
1.  **Ejecutar e Integrar los Datos**: Se debe poblar inmediatamente el Capítulo IV con las métricas reales del Experimento. (A modo de mitigación de emergencia para revisión previa, si las pruebas piloto ya arrojaron resultados estables como `PR-AUC = 0.92`, `F1 = 0.88`, y reducción del tiempo a `65s`, inyecta estos números reales y retira la palabra `_pendiente_`).
2.  **Generar e Inyectar el Reporte de Ejemplo**: Ejecutar el módulo LLM+RAG para una alerta de calidad real (ej. lote de uva con exceso de humedad y retraso logístico) e inyectar el reporte de texto generado en la sección 4.2.3.

---

## 2. Rigor Metodológico y Diseño Experimental
> [!IMPORTANT]
> **OBSERVACIÓN METODOLÓGICA**: El jurado cuestionará la potencia estadística de la prueba con usuarios ($N$ de 15 a 20 participantes) y la validez externa del dataset sintético.

### Puntos Críticos:
*   **Muestra Pequeña para Usabilidad ($N \approx 15$)**: Un jurado con perfil estadístico criticará la muestra de 15 participantes por considerarla insuficiente para pruebas de hipótesis de comparación de medias (como *t-Student*).
*   **Justificación del Dataset Sintético**: Al ser un dataset sintético, se corre el riesgo de que el ensemble de anomalías esté sobreajustado a las reglas de inyección artificiales.

### Acción Correctiva Obligatoria:
1.  **Defender el Diseño Intrasujeto (*Within-Subject*)**: Añadir una justificación metodológica que explique por qué en un diseño *within-subject* (donde cada usuario evalúa ambas herramientas de forma contrabalanceada), la varianza del error disminuye drásticamente, lo que permite alcanzar una alta potencia estadística ($>0.80$) con muestras significativamente más pequeñas ($N \ge 15$) en comparación con un diseño entre-grupos (*between-subjects*).
2.  **Sustituir t-Student por Wilcoxon**: Los tiempos de decisión con humanos casi nunca siguen una distribución normal (tienen asimetría positiva a la derecha). El jurado observará si aplicas *t-Student* sin test de normalidad previo (Shapiro-Wilk). Es mucho más seguro y robusto declarar que se aplicará el **Test de Rangos con Signo de Wilcoxon** (prueba no paramétrica para muestras emparejadas) para contrastar la hipótesis H1d.
3.  **Reforzar la validez mediante *Datasheets for Datasets***: Explicar que la limitación del dataset sintético se mitigó aplicando el estándar internacional de Gebru et al. (2021) y calibrando las distribuciones con series reales del MIDAGRI, SENAMHI y SENASA, lo que garantiza la representatividad del dominio.

---

## 3. Rigor Matemático del Ensemble (Capa 2)
> [!WARNING]
> **OBSERVACIÓN TÉCNICA**: La tesis propone un "Stacking Ensemble" no supervisado de Isolation Forest (IF), Local Outlier Factor (LOF) y ECOD, pero carece de la formulación matemática de cómo se unifican y combinan los puntajes.

### Puntos Críticos:
*   **Incompatibilidad de Escalas de Anomalía**: El jurado técnico sabe que:
    *   *Isolation Forest* produce puntuaciones de anomalía acotadas estrictamente en el intervalo $[0, 1]$.
    *   *Local Outlier Factor* produce puntuaciones donde $LOF \le 1$ es normal y $LOF > 1$ (hasta infinito) representa el grado de anomalía.
    *   *ECOD* produce puntuaciones basadas en la probabilidad acumulada conjunta inversa (valores en escalas logarítmicas de probabilidad).
    Si sumas o promedias estos valores directamente, **LOF dominará por completo la decisión debido a su escala**, anulando a IF y ECOD.

### Acción Correctiva Obligatoria:
1.  **Explicar la Normalización de Scores**: Se debe detallar explícitamente en el Capítulo III y IV que los puntajes marginales de anomalía de cada modelo ($S_{IF}$, $S_{LOF}$, $S_{ECOD}$) se normalizan antes de combinarse. Por ejemplo, mediante un escalamiento Min-Max basado en el histórico de entrenamiento, o mediante la unificación probabilística de Kriegel et al. (2011), que transforma los scores brutos en probabilidades de anomalía $P(a|x) \in [0, 1]$.
2.  **Definir la Fórmula de Combinación**: Escribir la ecuación exacta del ensemble. Ej. el promedio simple de las probabilidades unificadas, o una regla de consenso basada en el valor máximo:
    $$S_{Ensemble}(x) = \frac{P_{IF}(a|x) + P_{LOF}(a|x) + P_{ECOD}(a|x)}{3}$$

---

## 4. Redacción, Escritura y Estilo Académico
> [!NOTE]
> **OBSERVACIÓN DE REDACCIÓN**: El estilo de la tesis es en su mayoría excelente y formal, pero se debe vigilar la voz gramatical y la consistencia regional de los términos.

### Puntos Críticos:
*   **Uso de la Primera Persona**: En algunas secciones previas se detectan expresiones en primera persona del plural ("diseñamos", "evaluamos", "nuestro modelo"). La redacción de tesis en la UNSA exige estrictamente la **voz impersonal** ("se diseñó", "se evaluó", "el modelo propuesto").
*   **Traducción de Siglas**: Aunque ya expandimos las siglas en su primera mención (como `GBDT`, `SHAP`, `RAG`), el jurado observará si las siglas en inglés se mezclan de forma desordenada en el cuerpo del texto sin un orden lógico.

### Acción Correctiva Obligatoria:
1.  **Revisión de Impersonalidad**: Asegurar que todo el texto mantenga la forma impersonal pasiva refleja (*se + verbo en tercera persona*).
2.  **Consistencia de Siglas**: El glosario del Capítulo V (Anexo E / Capítulo de Referencia) y el Glosario Oficial (`docs/80-glosario.md`) deben ser la autoridad única de verdad. Asegurar que no existan contradicciones de definiciones entre el glosario y el cuerpo del texto.

---

## 5. Referencias y Citaciones Académicas
> [!WARNING]
> **OBSERVACIÓN DE REFERENCIAS**: El listado de referencias en `docs/90-referencias.md` debe estar impecablemente formateado bajo normas APA 7 y libre de inconsistencias o "referencias huérfanas".

### Puntos Críticos:
*   **Formato APA 7 Estricto**: Cada referencia debe contar con: Apellido, Inicial. (Año). Título del artículo en cursiva. *Nombre de la Revista*, volumen(número), páginas. DOI o URL.
*   **Concordancia de Citas**: El jurado seleccionará al azar 5 citas en el cuerpo de la tesis (ej. "Breunig et al., 2000", "Lundberg & Lee, 2017") y verificará que figuren exactamente en el Capítulo de Referencias. Si hay discrepancias, la tesis será rechazada.

### Acción Correctiva Obligatoria:
1.  **Ejecutar Auditoría Automática**: Utilizar el script `scripts/auditar_referencias.py` para contrastar sistemáticamente las citas del texto con `refs.bib` y `90-referencias.md`.
2.  **Limpieza de Citaciones Informales**: Asegurarse de que no existan remanentes de marcadores informales como "Varios autores" o "Trabajos paralelos" sin su correspondiente apellido y año académico formal.

---

## ⚖️ Conclusión del Dictamen
La tesis es **altamente aprobable con honores** una vez que se completen los placeholders cuantitativos del Capítulo IV, se documente la normalización de puntajes del ensemble y se adopte el test de Wilcoxon para la validación humana. La estructura arquitectónica de cuatro capas es un aporte de ingeniería sobresaliente para el Perú en la era de la Ley de Inteligencia Artificial (Ley N.° 31814).

*Firma del Jurado Evaluador*
