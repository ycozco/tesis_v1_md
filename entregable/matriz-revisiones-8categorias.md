# MATRIZ DE REVISIONES AMPLIADA (8 CATEGORÍAS)
## Sistema Integrado de Predicción y Anomalías — Agroexportación Peruana

**Fecha de validación**: 2025  
**Base académica**: Búsqueda ampliada de estándares (NIST AI RMF, Model Cards, Datasheets, ACM Ethics, EU AI Act)

---

## 1. REVISIÓN ESTRUCTURAL

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| Flujo lógico cap. a cap. | Cada sección inicia con pregunta y cierra con respuesta | ⏳ En revisión | Yoset |
| Introducción coherente | Introduce problema, contexto, brecha identificada | ⏳ En revisión | Yoset |
| Transiciones entre secciones | Conectores y resúmenes que cierren cap. N y abran cap. N+1 | ⏳ En revisión | Yoset |
| Índices completos | Tabla de contenidos, figuras, tablas, fórmulas actualizados | ⏳ En revisión | Yoset |
| Formato visual | Márgenes, tipografía, espaciado UNSA | ⏳ Pendiente | Yoset |

**Criterio de aprobación**: Lector sin conocimiento previo sigue argumentación de inicio a fin sin saltos.

---

## 2. REVISIÓN DE RIGOR CIENTÍFICO

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| Alineación título ↔ hipótesis | Título específico, hipótesis cuantificable y derivada del título | ✅ Completo | Yoset |
| Objetivos SMART | General + 3-4 específicos medibles | ✅ Completo | Yoset |
| Variables operacionalizadas | Cada variable con definición conceptual y operacional | ⏳ Parcial | Yoset |
| Hipótesis nula vs alternativa | Formulación explícita para pruebas estadísticas | ⏳ Pendiente | Yoset |
| Lógica causal documentada | Diagrama de relaciones: X → Y, mediadores/moderadores | ⏳ Pendiente | Yoset |

**Criterio de aprobación**: Jurado puede explicar qué se está probando y cómo se probará sin ambigüedad.

---

## 3. REVISIÓN METODOLÓGICA + DOCUMENTACIÓN DE MODELOS

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| **3.1 Protocolo de datos** | Fuente, período, frecuencia, número de registros documentados | ⏳ En revisión | Yoset |
| **3.2 Data quality** | Valores faltantes, outliers, transformaciones descritas | ⏳ En revisión | Yoset |
| **3.3 Splits train/val/test** | Método (temporal, estratificado, aleatorio), tamaños justificados | ⏳ Pendiente | Yoset |
| **3.4 Reproducibilidad** | Seeds fijas, versiones de librerías, código disponible | ⏳ En revisión | Yoset |
| **3.5 Métricas apropiadas** | PR-AUC para imbalance, F1 para equilibrio, ROUGE para NLG | ✅ Completo | Yoset |
| **3.6 Benchmarks** | Comparación con baseline y estado del arte (si aplica) | ⏳ En revisión | Yoset |
| **3.7 Model Card completo** | Desempeño por subgrupos, uso recomendado, limitaciones | ⏳ **NUEVA** | Yoset |
| **3.8 Ablation studies** | ¿Aporta cada componente (GBDT, ensemble, SHAP)? | ⏳ Pendiente | Yoset |

**Criterio de aprobación**: Otro investigador puede replicar resultados con información aquí contenida.

---

## 4. REVISIÓN DE DOCUMENTACIÓN DE DATOS Y REFERENCIAS

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| **4.1 Datasheets for Datasets** | Para CADA dataset: motivación, composición, proceso recolección | ⏳ **NUEVA** | Yoset |
| **4.2 Sesgos conocidos** | Identificados en dataset (ej. sesgo de cobertura, temporal) | ⏳ **NUEVA** | Yoset |
| **4.3 Licencias y permisos** | CC-BY, proprietary, anónimo — explícitamente documentado | ⏳ Pendiente | Yoset |
| **4.4 Citas APA completas** | Autor, año, título, editorial, DOI o URL | ✅ Completo | Yoset |
| **4.5 Actualidad** | >70% referencias últimos 5 años (IA), 7 años (agricultura) | ✅ Completo | Yoset |
| **4.6 Cobertura temática** | Antecedentes, estado del arte, bases teóricas, normativa | ✅ Completo | Yoset |
| **4.7 Fuentes primarias** | Acceso a papers originales, no solo abstracts | ✅ Completo | Yoset |

**Criterio de aprobación**: Cada dataset tiene "datasheet" anexado; toda cita es verificable y reciente.

---

## 5. REVISIÓN DE GOBERNANZA + CONFORMIDAD REGULATORIA

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| **5.1 Matriz SBS N° 053-2023** | Trazabilidad: modelo documentado con versión, validación, aprobación | ⏳ **NUEVA** | Yoset |
| **5.2 Matriz DS-115-2025-PCM** | Ley IA Perú: clasificación riesgo, análisis ex-ante, monitoreo | ⏳ **NUEVA** | Yoset |
| **5.3 Conformidad EU AI Act** | Si aplica: Annex III risk, Art. 13 transparencia | ⏳ **NUEVA** | Yoset |
| **5.4 Roles explícitos** | Quién desarrolla, quién valida, quién autoriza despliegue | ⏳ Pendiente | Yoset |
| **5.5 Decisiones documentadas** | Por qué se eligió GBDT vs XGBoost, Isolation Forest vs LOF | ⏳ En revisión | Yoset |
| **5.6 Plan de monitoreo** | Métricas de desempeño post-despliegue, alertas de degradación | ⏳ Pendiente | Yoset |

**Criterio de aprobación**: Un regulador (SBS, PCM) puede auditar trazabilidad completa de decisiones.

---

## 6. REVISIÓN DE EXPLICABILIDAD E INTERPRETABILIDAD

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| **6.1 Explicaciones SHAP** | Gráficos SHAP para top features, interpretables por supervisor sin IA | ⏳ **NUEVA** | Yoset |
| **6.2 Incertidumbre explícita** | Diferencia epistémica (modelo desconoce) vs aleatoria (ruido) | ⏳ **NUEVA** | Yoset |
| **6.3 Anti-alucinación en reportes** | Límites de LLM documentados: NO fabrica datos, cita fuentes | ⏳ **NUEVA** | Yoset |
| **6.4 Validación SHAP+LLM** | ¿Las explicaciones de SHAP y LLM son consistentes? | ⏳ **NUEVA** | Yoset |
| **6.5 Transparencia limitaciones** | Reportes indican: "Este modelo no se ha validado en X escenario" | ⏳ Pendiente | Yoset |
| **6.6 Usabilidad para supervisores** | 80%+ supervisores entienden por qué modelo flagea anomalía | ⏳ Pendiente | Yoset |

**Criterio de aprobación**: Un supervisor sin ML background entiende decisiones del sistema sin experto.

---

## 7. REVISIÓN DE ÉTICA Y SESGO

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| **7.1 Análisis de composición** | Dataset incluye PYME, medianas, grandes exportadores equitativamente | ⏳ **NUEVA** | Yoset |
| **7.2 Desempeño por subgrupos** | Métrica principal (PR-AUC) calculada por región, tamaño empresa | ⏳ **NUEVA** | Yoset |
| **7.3 Identificación de sesgos** | ¿El modelo predice mejor para ciertos grupos? ¿Aceptable? | ⏳ **NUEVA** | Yoset |
| **7.4 Trade-offs documentados** | Si mejorar equidad degrada precisión global, ¿cuál prioriza? | ⏳ **NUEVA** | Yoset |
| **7.5 Impacto potencial** | ¿Qué pasa si modelo falla? ¿Perjudicados? ¿Mitigación? | ⏳ **NUEVA** | Yoset |
| **7.6 Acceso equitativo** | Sistema accesible para PYME sin costos prohibitivos | ⏳ Pendiente | Yoset |

**Criterio de aprobación**: Matriz de fairness por subgrupo; trade-offs explícitos entre precisión ↔ equidad.

---

## 8. REVISIÓN WEB / PUBLICACIÓN + USABILIDAD

| Aspecto | Indicador de Logro | Estado | Responsable |
|--------|-------------------|--------|-------------|
| **8.1 Interfaz clara** | Dashboard muestra anomalías, predicciones, explicaciones sin sobrecarga | ⏳ En revisión | Yoset |
| **8.2 Documentación on-site** | Glosario, FAQ, tutorialés para supervisores integrados | ⏳ Pendiente | Yoset |
| **8.3 Accesibilidad WCAG 2.1 AA** | Colores, contraste, navegación teclado, alt-text en imágenes | ⏳ Pendiente | Yoset |
| **8.4 Limitaciones visibles** | Página explica: "Este sistema NO debe usarse en X situación" | ⏳ Pendiente | Yoset |
| **8.5 Formulario de feedback** | Usuario puede reportar predicciones incorrectas | ⏳ Pendiente | Yoset |
| **8.6 Rendimiento** | Carga <3 seg, responsive en móvil (si aplica) | ⏳ Pendiente | Yoset |

**Criterio de aprobación**: Supervisor accede a reportes, entiende recomendaciones y puede actuar en <2 minutos.

---

## RESUMEN DE ESTADO GENERAL

| Categoría | Total Indicadores | ✅ Completo | ⏳ En revisión | ⏳ Pendiente | % Avance |
|-----------|-------------------|-----------|-------------|-----------|----------|
| 1. Estructural | 5 | 0 | 4 | 1 | 80% |
| 2. Rigor Científico | 5 | 1 | 2 | 2 | 60% |
| 3. Metodológica | 8 | 1 | 4 | 3 | 62% |
| 4. Datos y Referencias | 7 | 3 | 1 | 3 | 57% |
| 5. Gobernanza | 6 | 0 | 1 | 5 | 17% |
| 6. Explicabilidad | 6 | 0 | 0 | 6 | 0% |
| 7. Ética y Sesgo | 6 | 0 | 0 | 6 | 0% |
| 8. Web/Usabilidad | 6 | 0 | 2 | 4 | 33% |
| **TOTAL** | **49** | **5** | **14** | **30** | **38%** |

---

## RECOMENDACIÓN DE ORDEN DE TRABAJO

### **Fase 1 (Inmediata)**: Rigor Científico + Datos
1. Operacionalizar variables (Rigor 3, 4)
2. Crear Datasheets para cada dataset (Datos 1, 2, 3)
3. Documentar decisiones metodológicas (Metodología 2, 5)

### **Fase 2 (Semana 2-3)**: Gobernanza + Explicabilidad
1. Matriz SBS N° 053-2023 (Gobernanza 1)
2. Matrices de fairness por subgrupo (Ética 2, 3)
3. Validación SHAP (Explicabilidad 1, 4)

### **Fase 3 (Semana 4+)**: Web + Integración
1. Dashboard con limitaciones explícitas (Web 4)
2. Usabilidad con supervisores (Explicabilidad 6)
3. Cierre normativo (Gobernanza 6)

---

**Documento generado**: 2025  
**Responsable**: Yoset Cozco Mauri  
**Próxima revisión**: Después de completar Fase 1  
**Integración**: Panel administrativo centralizado
