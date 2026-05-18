# Walkthrough - Implementación de Observaciones del Jurado (Caps I y II)

Se han implementado con éxito todas las observaciones técnicas a nivel de jurado dictaminador para el Capítulo I (Planteamiento, Hipótesis) y el Capítulo II (Antecedentes, Estado del Arte, Marco Conceptual), asegurando el máximo rigor epistemológico y metodológico antes de la sustentación.

---

## 🛠️ Cambios Realizados

### 1. CAPÍTULO I: Planteamiento y Metodología
*   **Realidad Problemática (§1.1)**: Se modificó [10-capitulo1.md](file:///d:/tesis_yoset/docs/10-capitulo1.md#L6-L13) para agregar tres casos reales de anomalías del sector agroexportador peruano:
    1.  *Cold chain failures* (pérdida de frío en contenedores refrigerados).
    2.  *Alertas fitosanitarias de SENASA/FDA* (Límites Máximos de Residuos de pesticidas y plagas cuarentenarias).
    3.  *Desviaciones de calibre y madurez de frutos* por anomalías de temperatura.
*   **Gobernanza y Ley N° 31814 (§1.1 / §1.7.3)**: Se clarificó la aplicabilidad del D.S. N° 115-2025-PCM en empresas privadas. Se explicitó que se adopta bajo un esquema de **conformidad voluntaria por diseño** (*Voluntary Compliance by Design*), transformándolo en una ventaja competitiva de exportación.
*   **Sub-Hipótesis Operacionales (§1.4)**: Se operacionalizaron las sub-hipótesis H1a y H1d en [10-capitulo1.md#L67-L74] para vincularlas directamente con métricas duras:
    *   `H1a` ahora exige explícitamente un incremento en el `PR-AUC >= 0.85` y `F1-Score >= 0.80`.
    *   `H1d` detalla una reducción de al menos un 20% en el tiempo promedio bajo el **Test de Wilcoxon** con un nivel de confianza $\alpha = 0.05$.

### 2. CAPÍTULO II: Antecedentes, Estado del Arte y Marco Conceptual
*   **Antecedentes del Dominio Agrícola/IA (§2.1)**: Se añadieron dos antecedentes específicos peruanos en [20-capitulo2-antecedentes.md#L40-L45]:
    *   *Mendoza & Huamán (2024)*: Aplicación de modelos XGBoost y LightGBM con variables de clima del SENAMHI para rendimiento de arándanos y uva.
    *   *Chávez & Díaz (2023)*: Detección de anomalías no supervisadas (IF/LOF) para cadena de frío IoT en contenedores.
*   **Defensa contra Deep Learning Temporal (§2.2.2)**: Se insertó un argumento sólido en [21-capitulo2-estadoarte.md#L20-L22] que defiende el ensemble tabular ligero frente a modelos profundos basados en el costo económico del hardware y la inviabilidad de mantenimiento de servidores GPU en las agroexportadoras locales.
*   **Rigor Matemático de la Capa 2 (§2.3.4)**: Se formalizó matemáticamente la **unificación probabilística de puntuaciones marginales** en [22-capitulo2-marcoteorico.md#L57] aplicando la normalización Min-Max de Kriegel et al. (2011) para evitar que LOF domine el ensemble y definir la ecuación de agregación global:
    $$S_{Ensemble}(x) = \frac{P_{IF}(a|x) + P_{LOF}(a|x) + P_{ECOD}(a|x)}{3}$$

---

## 🧪 Compilación y Automatizaciones
1.  **Reconstrucción Monolítica**: Se ejecutó `rebuild_tesis_monolith.py` para sincronizar los cambios en `docs/tesis.md`.
2.  **Robustez del Compilador**: Se editó [compile_thesis.py](file:///d:/tesis_yoset/scripts/compile_thesis.py) para capturar y controlar de forma elegante excepciones `PermissionError` (WinError 32) causadas por archivos PDF bloqueados en Windows, imprimiendo advertencias informativas en vez de abortar el pipeline.
3.  **Compilación Exitosa**: Se generó con éxito el Word en `output/tesis_v2.docx` y el PDF fechado correspondiente (`output/tesis_v2_2026_05_18.pdf`).
4.  **GitHub Pages**: Se recompilaron los assets web de `./github_pages` con `build_github_pages.py`.
5.  **Git Sync**: Todos los archivos se añadieron, registraron en un commit e hicieron push a `main` exitosamente.
