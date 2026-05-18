# RESUMEN EJECUTIVO: BÚSQUEDA AMPLIADA Y VALIDACIÓN DE REVISIONES
## Tesis — Sistema Integrado de Predicción, Detección de Anomalías y Generación de Reportes

**Versión**: 1.0  
**Fecha**: 2025  
**Alcance**: Validación mediante búsqueda web de estándares académicos e internacionales  
**Conclusión**: Las 6 categorías originales son sólidas pero **incompletas**; se amplían a **8 categorías** con justificación académica.

---

## PROBLEMA INICIAL

Se había definido un plan de revisiones con 6 categorías:
1. Estructural
2. Coherencia académica
3. Metodológica
4. Bibliográfica
5. Gobernanza
6. Web/Publicación

**Interrogante**: ¿Están estas categorías completas y bien encaminadas según estándares internacionales?

---

## BÚSQUEDA REALIZADA

Se consultaron 9+ marcos académicos reconocidos:

| Marco | Fuente | Año | Relevancia |
|-------|--------|------|-----------|
| **Model Cards** | Mitchell et al. | 2018 | Documentación estándar para modelos ML |
| **Datasheets for Datasets** | Gebru et al. | 2018 | Documentación estándar para datasets |
| **Interpretability Mythos** | Lipton | 2016 | Definiciones de explicabilidad vs transparencia |
| **Uncertainty Quantification** | Postels et al. | 2021 | Incertidumbre epistémica en modelos |
| **FAO Standards** | FAO | 2022 | Calidad de datos agroalimentarios |
| **NIST AI RMF** | NIST | 2023 | Marco de gobernanza de IA (oficial EE.UU.) |
| **ACM Code of Ethics** | ACM | Vigente | Fairness, transparency, accountability |
| **EU AI Act 2024** | Parlamento Europeo | 2024 | Regulación de IA de alto riesgo |
| **Perú DS-115-2025** | PCM | 2025 | Reglamento IA nacional |

---

## HALLAZGOS CLAVE

### ✅ VALIDADO: Las 6 categorías originales son fundamentadas
Cada una mapea a un estándar reconocido:
- Estructural → Estándares académicos UNSA/APA ✓
- Coherencia académica → NIST Map + ACM Transparency ✓
- Metodológica → Model Cards + Datasheets ✓
- Bibliográfica → APA + actualidad de fuentes ✓
- Gobernanza → NIST Govern + regulaciones ✓
- Web/Publicación → NIST Manage + usabilidad ✓

### ⚠️ INCOMPLETO: Faltan 2 dimensiones críticas

#### 1. **Explicabilidad e Interpretabilidad** (NUEVA)
**Fundamento académico**: Lipton (2016), Mitchell et al. (2018)  
**Razón falta**: La tesis usa SHAP + LLMs; necesita validar que explicaciones sean:
- Entendibles por supervisores sin ML
- Consistentes entre SHAP y generación de reportes
- Limitadas por anti-alucinación (RAG)
- Cuantificadas en usabilidad (% supervisores que entienden)

**Indicadores a evaluar**:
- Validación SHAP (top features interpretables)
- Incertidumbre explícita en reportes (epistémica vs aleatoria)
- Limitaciones documentadas ("Este sistema NO se debe usar en X")

#### 2. **Ética y Sesgo** (NUEVA)
**Fundamento académico**: ACM Code of Ethics, NIST AI RMF, EU AI Act Arts. 5-6  
**Razón falta**: Sistema de IA operativo en empresas agroexportadoras; impacta decisiones sobre:
- Quién recibe auditorías frecuentes
- Qué operaciones se flagean como "anómalas"
- Equidad entre PYME y grandes exportadores

**Indicadores a evaluar**:
- Desempeño del modelo por subgrupos (región, tamaño empresa)
- Sesgos identificados en dataset
- Trade-offs explícitos (si mejorar equidad degrada precisión global)
- Documentación de impacto potencial en poblaciones vulnerables

---

## CATEGORÍAS PROPUESTAS (VERSIÓN FINAL)

### ANTES (6 categorías)
1. Estructural
2. Coherencia académica
3. Metodológica
4. Bibliográfica
5. Gobernanza
6. Web/Publicación

### DESPUÉS (8 categorías con mejoras)
1. **Estructural** (sin cambios — es sólida)
2. **Rigor Científico** (renombre para mayor precisión)
3. **Metodológica + Documentación de Modelos** (expansión)
4. **Documentación de Datos y Referencias** (renombre + Datasheets)
5. **Gobernanza + Conformidad Regulatoria** (expansión SBS/DS-115/EU)
6. **Explicabilidad e Interpretabilidad** 🆕
7. **Ética y Sesgo** 🆕
8. **Web/Publicación + Usabilidad** (sin cambios)

---

## IMPACTO EN EL PROYECTO

### Documentos entregables creados hoy:
1. **`sustentacion-revisiones-ampliada.md`** — Justificación académica de las 8 categorías
2. **`matriz-revisiones-8categorias.md`** — 49 indicadores de logro con tracking

### Cambios en el panel administrativo:
- De 6 secciones de revisión → 8 secciones
- 5 indicadores completados ✅
- 14 indicadores en revisión ⏳
- 30 indicadores pendientes ⏳
- **Avance global: 38%**

### Orden de trabajo recomendado:
**Fase 1 (Inmediata)**: Operacionalizar variables + Datasheets + decisiones metodológicas  
**Fase 2 (Semana 2-3)**: Gobernanza + Fairness + SHAP  
**Fase 3 (Semana 4+)**: Web + Integración + cierre regulatorio

---

## CONCLUSIÓN

✅ **Las categorías de revisión de la tesis NO están mal encaminadas; están INCOMPLETAS.**

**Recomendación**: Adoptar el modelo de 8 categorías antes de redactar versión final de tesis. Esto garantiza:
- Conformidad con estándares internacionales (NIST, EU AI Act, ACM)
- Auditoría regulatoria clara (SBS N° 053-2023, DS-115-2025-PCM)
- Explicabilidad validada por usuarios reales
- Evaluación de fairness explícita en subgrupos

**Próximas acciones**:
1. Revisar y validar Matriz de 49 indicadores
2. Integrar en dashboard administrativo centralizado
3. Priorizar Fase 1 de trabajo
4. Documentar decisiones en trazabilidad regulatoria

---

**Responsable**: Yoset Cozco Mauri + Copilot  
**Referencias completas**: Ver `sustentacion-revisiones-ampliada.md`  
**Matriz de trabajo**: Ver `matriz-revisiones-8categorias.md`
