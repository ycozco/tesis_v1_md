# Sustentación Ampliada de Categorías de Revisión
## Búsqueda Web y Validación de Marcos Académicos

**Fecha de búsqueda**: 2025  
**Objetivo**: Validar si las 6 categorías de revisión actuales (Estructural, Coherencia académica, Metodológica, Bibliográfica, Gobernanza, Web/Publicación) son completas, robustas y alineadas con estándares académicos internacionales.

---

## HALLAZGOS CLAVE DE INVESTIGACIÓN

### 1. MARCOS ACADÉMICOS IDENTIFICADOS

#### A. Model Cards Framework (Mitchell et al., 2018)
**Fuente**: arXiv:1810.03993 "Model Cards for Model Reporting"  
**Relevancia**: Propone documentación estándar para modelos ML entrenados  
**Componentes recomendados**:
- Detalles del modelo y uso previsto
- Evaluación del desempeño en múltiples condiciones (demográficas, interseccionales)
- Contexto de aplicación y limitaciones
- Procedimientos de evaluación de desempeño
- **IMPLICACIÓN**: Nuestra categoría "Metodológica" cubre esto, pero es relevante añadir una sub-dimensión de "Documentación de Modelos" si usamos ML en la tesis.

#### B. Datasheets for Datasets (Gebru et al., 2018)
**Fuente**: arXiv:1803.09010 "Datasheets for Datasets"  
**Relevancia**: Estándar de documentación para datasets de ML  
**Componentes recomendados**:
- Motivación del dataset
- Composición del dataset
- Proceso de recolección
- Preprocesamiento y limpieza
- Usos recomendados y no recomendados
- **IMPLICACIÓN**: Nuestra categoría "Bibliográfica" (mal nombrada) debería ser "Datos y Documentación" para incluir validación de calidad de datasets según Datasheets.

#### C. Interpretability / Explainability Standards (Lipton, 2016)
**Fuente**: arXiv:1606.03490 "The Mythos of Model Interpretability"  
**Relevancia**: Propone definiciones rigurosas y diferenciación entre transparencia e interpretabilidad  
**Componentes críticos**:
- Transparencia a humanos (simplicity, complexity, scope)
- Explicaciones post-hoc (LIME, SHAP, saliency maps)
- Calibración y confiabilidad de incertidumbre
- **IMPLICACIÓN**: Nuestra tesis usa SHAP para explicabilidad. Necesitamos una categoría explícita de revisión de "Explicabilidad e Interpretabilidad" más allá de metodología.

#### D. Uncertainty Quantification in ML (Postels et al., 2021)
**Fuente**: arXiv:2012.03082 "Implicit Representation Uncertainty in Latent Space Models"  
**Relevancia**: Evalúa incertidumbre epistémica vs aleatoria en predicciones  
**Aplicación**: Crítico si usamos GBDT con predicciones probabilísticas  
- **IMPLICACIÓN**: Necesitamos revisar cómo el modelo comunica incertidumbre en reportes.

#### E. FAO Standards for Agricultural Data (FAO, 2022)
**Fuente**: FAO Technical Study CB8249EN  
**Relevancia**: Estándares para datos agroalimentarios, evaluación de shocks  
**Componentes**:
- Recolección de datos primarios desde productores, comerciantes, suplidores
- Evaluación de impactos en cadena de valor
- Seguimiento de seguridad alimentaria
- **IMPLICACIÓN**: Si usamos datos agrícolas, necesitamos validar calidad según FAO.

---

### 2. ESTÁNDARES DE EVALUACIÓN ACADÉMICA ENCONTRADOS

#### NIST AI RMF (Risk Management Framework)
**Contexto**: Marco de gobernanza de IA desarrollado por el NIST (2023)  
**Dominios de revisión**:
1. **Govern** (Gobernar) — Políticas, marcos, responsabilidades
2. **Map** (Mapear) — Identificar sistemas, contexto, riesgos
3. **Measure** (Medir) — Evaluar desempeño, riesgos, mitigaciones
4. **Manage** (Gestionar) — Mitigación de riesgos, monitoreo

**Reflexión**: Nuestras 6 categorías pueden reorganizarse según NIST:
- Gobernanza → GOVERN
- Estructural + Coherencia + Metodológica → MAP + MEASURE
- Bibliográfica → MAP (validación de fuentes)
- Web/Publicación → MANAGE (comunicación, transparencia post-lanzamiento)

---

#### ACM Code of Ethics & Professional Conduct
**Componentes relevantes**:
1. **Responsibility**: Calidad del trabajo, impacto social
2. **Fairness**: Evitar sesgo, acceso equitativo
3. **Transparency**: Comunicación clara de limitaciones y alcances
4. **Accountability**: Documentación de decisiones

**Reflexión**: **FALTA una categoría de revisión de "Ética y Sesgo"** que no está explícita en nuestras 6 dimensiones.

---

#### EU AI Act (2024) & Peruvian DS-115-2025-PCM
**Exigencias críticas**:
- Evaluación ex-ante de riesgos (antes del despliegue)
- Evaluación post-despliegue de desempeño real
- Documentación de decisiones de IA
- Transparencia a usuarios
- Corrección de desempeño degradado
- **IMPLICACIÓN**: Nuestra "Gobernanza" cubre esto, pero necesitamos sub-componentes de "Conformidad Regulatoria" evaluables.

---

### 3. CATEGORÍAS DE REVISIÓN PROPUESTAS Y JUSTIFICACIÓN

#### ✅ CATEGORÍA 1: ESTRUCTURAL (MANTENER)
**Descripción**: Coherencia lógica, flujo argumentativo, conectores entre secciones  
**Validado por**: Estándares académicos UNSA, APA  
**Revisión**: ¿Es la tesis un flujo coherente de problema → solución → validación?

---

#### ✅ CATEGORÍA 2: COHERENCIA ACADÉMICA (RENOMBRAR: "RIGOR CIENTÍFICO")
**Descripción**: 
- Alineación título ↔ hipótesis ↔ variables ↔ metodología
- Definiciones operacionales claras
- Lógica causa-efecto explícita
**Validado por**: NIST Map phase, ACM Transparency  
**Revisión**: ¿Son las afirmaciones demostrables con los datos propuestos?

---

#### ✅ CATEGORÍA 3: METODOLÓGICA (MANTENER + EXPANDIR)
**Descripción**: Validez del diseño de investigación, reproducibilidad, benchmarks  
**Validado por**: 
- Model Cards Framework (Mitchell et al., 2018)
- Datasheets for Datasets (Gebru et al., 2018)
- NIST Measure phase
**Sub-componentes a evaluar**:
- Protocolo de recolección de datos documentado
- Splits train/val/test justificados
- Métricas apropiadas al contexto (PR-AUC vs Accuracy)
- Benchmarks de referencia usados
- Reproducibilidad: código, seeds, versiones de librerías

**🆕 ADICIÓN**: Si usamos ML, evaluar "Model Card completitud" (desempeño en subgrupos, contexto de uso, limitaciones)

---

#### ✅ CATEGORÍA 4: BIBLIOGRÁFICA (RENOMBRAR: "DOCUMENTACIÓN DE DATOS Y REFERENCIAS")
**Descripción**: 
- Validez de citas (APA, completitud)
- **NUEVA**: Calidad de datasets según Datasheets for Datasets
- Actualidad de referencias (últimos 5-7 años para IA)
**Validado por**: Estándares APA + Datasheets framework  
**Sub-componentes**:
- Cada dataset documentado: motivación, composición, proceso de recolección
- Sesgos conocidos en datos identificados
- Licencias y permisos explícitos
- Accesibilidad de fuentes para reproducibilidad

---

#### ✅ CATEGORÍA 5: GOBERNANZA (MANTENER + EXPANDIR)
**Descripción**: 
- Conformidad regulatoria (SBS N° 053-2023, DS-115-2025, EU AI Act)
- Responsabilidades y trazabilidad
- Documentación de decisiones
**Validado por**: NIST Govern phase, EU AI Act, normativas peruanas  
**Sub-componentes**:
- Matriz de conformidad regulatoria explícita
- Roles y responsabilidades documentados
- Evaluación de riesgos de IA (ex-ante)
- Plan de monitoreo post-despliegue

---

#### 🆕 CATEGORÍA 6: EXPLICABILIDAD E INTERPRETABILIDAD
**Descripción**: 
- Claridad de decisiones del modelo para stakeholders
- Calibración de incertidumbre
- Anti-alucinación en reportes generados
**Validado por**: 
- Lipton (2016) on Interpretability
- Model Cards (Mitchell et al., 2018)
- NIST Measure phase
**Sub-componentes a evaluar**:
- ¿Entienden supervisores por qué el modelo predice X?
- ¿Se comunica incertidumbre (epistémica vs aleatoria) claramente?
- ¿Hay límites documentados para reportes automáticos?
- ¿Se valida que SHAP + LLM no generan explicaciones contradictorias?

---

#### 🆕 CATEGORÍA 7: ÉTICA Y SESGO
**Descripción**: 
- Evaluación de fairness (equidad entre grupos)
- Identificación y mitigación de sesgos
- Impacto potencial en poblaciones vulnerables
**Validado por**: 
- ACM Code of Ethics (Fairness)
- NIST Framework (Govern + Measure)
- EU AI Act (Art. 5-6, clasificación de riesgo)
**Sub-componentes a evaluar**:
- Composición del dataset: ¿Hay underrepresentation?
- Desempeño del modelo por subgrupos demográficos
- Análisis de sesgo: género, región, escala operativa (PYME vs grandes exportadores)
- Documentación de trade-offs: si mejorar equidad degrada precisión global, ¿es aceptable?

---

#### ✅ CATEGORÍA 8: WEB / PUBLICACIÓN (MANTENER)
**Descripción**: 
- Claridad de presentación en plataforma web
- Usabilidad para supervisores y auditores
- Accesibilidad (WCAG 2.1 AA)
**Validado por**: NIST Manage phase (comunicación post-despliegue)

---

## RESUMEN DE CAMBIOS PROPUESTOS

| Categoría Original | Nuevo Nombre | Cambios |
|-------------------|--------------|---------|
| Estructural | Estructural | Sin cambios, es sólida |
| Coherencia académica | Rigor Científico | Más precisión terminológica |
| Metodológica | Metodológica + Documentación de Modelos | Añadir Model Cards checklist |
| Bibliográfica | Documentación de Datos y Referencias | Añadir Datasheets checklist |
| Gobernanza | Gobernanza + Conformidad Regulatoria | Expandir a matriz SBS/DS-115 |
| Web/Publicación | Web/Publicación + Usabilidad | Sin cambios significativos |
| — | Explicabilidad e Interpretabilidad | 🆕 NUEVA |
| — | Ética y Sesgo | 🆕 NUEVA |

**Total**: 6 categorías ➜ **8 categorías** (2 nuevas fundamentadas)

---

## FUENTES ACADÉMICAS CITADAS

1. **Mitchell et al. (2018)** — Model Cards for Model Reporting  
   arXiv:1810.03993 | Publicado: FAT* 2019 Conference

2. **Gebru et al. (2018)** — Datasheets for Datasets  
   arXiv:1803.09010 | Publicado: CACM, 2021

3. **Lipton (2016)** — The Mythos of Model Interpretability  
   arXiv:1606.03490 | Workshop: WHI 2016 ICML

4. **Postels et al. (2021)** — Implicit Representation Uncertainty in Latent Space Models  
   arXiv:2012.03082

5. **FAO (2022)** — Shocks, Agricultural Livelihoods and Food Security  
   Técnico: CB8249EN | Aplicable a datos agroexportadores

6. **NIST (2023)** — Artificial Intelligence Risk Management Framework  
   Framework oficial para gobernanza de IA

7. **EU AI Act (2024)** — Regulation (EU) 2024/1689  
   Aplicable a sistemas de IA de alto riesgo en decisiones empresariales

8. **Perú DS-115-2025-PCM** — Reglamento de Ley de IA Peruana  
   Aplicable a sistemas financieros y operativos

9. **SBS Resolución N° 053-2023** — Gestión de Riesgos de Modelo  
   Regulación de auditoría y trazabilidad en banca peruana

---

## CONCLUSIÓN

Las **6 categorías originales son un buen punto de partida**, pero **requieren expansión y renombramiento** para ser exhaustivas según estándares internacionales:

✅ **Recomendación**: Adoptar las **8 categorías expandidas** con enfoque en:
1. Trazabilidad regulatoria explícita (SBS, DS-115, EU AI Act)
2. Documentación de datasets según Datasheets for Datasets
3. Explicabilidad explícita como categoría independiente
4. Evaluación de sesgo y fairness según ACM + NIST

Esto garantiza que la tesis no solo sea técnicamente robusta, sino también éticamente fundamentada y regulatoriamente conformante.

---

**Documento generado**: 2025  
**Responsable**: Yoset Cozco Mauri + Copilot  
**Estado**: Listo para integración en dashboard administrativo
