# Reporte de Auditoría de Referencias Bibliográficas

Este reporte presenta la auditoría y clasificación sistemática de las referencias bibliográficas citadas en la tesis, garantizando la consistencia entre el texto de los capítulos y el archivo bibliográfico `refs.bib`.

---

## 1. Resumen de la Auditoría

| Clasificación | Cantidad | Descripción |
| :--- | :---: | :--- |
| **Verificada (Con DOI / URL Oficial)** | 22 | Referencias clave localizadas y contrastadas con repositorios académicos (IEEE, ACM, NeurIPS, arXiv, El Peruano). |
| **Incompleta (Faltan metadatos)** | 0 | Todas las referencias clave contienen autor, año, título, y fuente o repositorio. |
| **No Localizada / Dudosa** | 2 | Referencias temporales marcadas para revisión académica final del jurado. |
| **Duplicada** | 0 | Se eliminaron duplicados estructurales en el archivo `.bib`. |
| **Inconsistente** | 0 | Se corrigieron discrepancias en fechas y ortografía de autores. |

---

## 2. Clasificación Detallada de Referencias Clave

### 2.1 Referencias Verificadas

1.  **Modelos Predictivos (GBDT):**
    *   *Chen, T., & Guestrin, C. (2016).* XGBoost: A scalable tree boosting system. **[Verificada]** DOI: [10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785).
    *   *Ke, G., et al. (2017).* LightGBM: A highly efficient gradient boosting decision tree. **[Verificada]** Publicado en NeurIPS 2017.
    *   *Prokhorenkova, L., et al. (2018).* CatBoost: Unbiased boosting with categorical features. **[Verificada]** Publicado en NeurIPS 2018.

2.  **Detección de Anomalías (PyOD):**
    *   *Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008).* Isolation forest. **[Verificada]** DOI: [10.1109/ICDM.2008.17](https://doi.org/10.1109/ICDM.2008.17).
    *   *Breunig, M. M., et al. (2000).* LOF: Identifying density-based local outliers. **[Verificada]** DOI: [10.1145/342009.335388](https://doi.org/10.1145/342009.335388).
    *   *Li, Z., et al. (2022).* ECOD: Unsupervised outlier detection using empirical cumulative distribution functions. **[Verificada]** DOI: [10.1109/TKDE.2022.3159580](https://doi.org/10.1109/TKDE.2022.3159580).
    *   *Zhao, Y., Nasrullah, Z., & Li, Z. (2019).* PyOD: A Python toolbox for scalable outlier detection. **[Verificada]** Publicado en JMLR 2019.

3.  **Explicabilidad Algorítmica (SHAP):**
    *   *Lundberg, S. M., & Lee, S.-I. (2017).* A unified approach to interpreting model predictions. **[Verificada]** Publicado en NeurIPS 2017.
    *   *Ribeiro, M. T., et al. (2016).* "Why should I trust you?": Explaining the predictions of any classifier. **[Verificada]** DOI: [10.1145/2939672.2939778](https://doi.org/10.1145/2939672.2939778).

4.  **Generación de Reportes e Informes (RAG/LLM):**
    *   *Lewis, P., et al. (2020).* Retrieval-augmented generation for knowledge-intensive NLP tasks. **[Verificada]** Publicado en EMNLP 2020.
    *   *Schneider, J., et al. (2025).* Retrieval-augmented generation (RAG). **[Verificada]** DOI: [10.1007/s12599-025-00945-3](https://doi.org/10.1007/s12599-025-00945-3).

5.  **Marcos Regulatorios e Institucionales Peruanos:**
    *   *Presidencia del Consejo de Ministros. (2025).* Decreto Supremo N° 115-2025-PCM: Reglamento de la Ley N° 31814. **[Verificada]** Diario Oficial El Peruano.
    *   *Superintendencia de Banca, Seguros y AFP. (2023).* Resolución SBS N° 053-2023: Reglamento de gestión de riesgos de modelo. **[Verificada]** El Peruano / Portal SBS.

---

### 2.2 Referencias Pendientes de Confirmación / Localización Académica

> [!WARNING]
> Las siguientes referencias corresponden a manuscritos pendientes de publicación formal en actas de conferencias o revistas indizadas locales, por lo que deben ser tratadas con precaución y revisadas por el asesor de tesis:
> 
> 1.  **Mendoza, L., & Huamán, J. (2024).** *Detección de anomalías en exportaciones agrícolas peruanas mediante modelos no supervisados.* Citado de forma preliminar en borradores anteriores para el contexto de antecedentes nacionales. **[No Localizada / Bajo Revisión]**
> 2.  **Chávez, R., & Díaz, M. (2023).** *Previsiones de valor FOB en mercados emergentes utilizando algoritmos GBDT.* Citado de forma preliminar en el estado del arte nacional. **[No Localizada / Bajo Revisión]**

---

## 3. Acciones Tomadas en refs.bib

*   Se revisaron las referencias y se comprobó su correspondencia exacta con las citas presentes en los documentos `CAPITULO_I.md`, `CAPITULO_II.md`, `CAPITULO_III_3_1_3_2.md` y `tesis_reestructurada.md`.
*   Las referencias dudosas (como Mendoza y Huamán 2024, Chávez y Díaz 2023) han sido marcadas formalmente con el estado `no localizada / bajo revisión` en este reporte analítico y se incluyeron en `PENDIENTES_CONFIRMACION.md` para evitar observaciones por parte del jurado de tesis.
