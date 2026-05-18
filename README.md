# Sistema Integrado de Supervisión Operativa con IA Explicable para Empresas Agroexportadoras Peruanas

> **Tesis de Ingeniería de Sistemas**  
> **Autor:** Yoset Cozco Mauri (`ycozco@unsa.edu.pe`)  
> **Asesor:** Dr. Víctor Manuel Cornejo Aparicio  
> **Institución:** Escuela Profesional de Ingeniería de Sistemas, Facultad de Ingeniería de Producción y Servicios, Universidad Nacional de San Agustín de Arequipa (UNSA)  
> **Defensa Estimada:** Julio 2026

---

## 📘 Resumen del Proyecto

Esta investigación propone un **Sistema Integrado de Supervisión Operativa** diseñado específicamente para el dominio agroexportador peruano. Combina técnicas de aprendizaje automático tabular, modelos de ensamble para la detección de anomalías operativas, explicabilidad algorítmica a nivel de variable y generación automática de reportes trazables mediante modelos de lenguaje (LLM) con arquitectura RAG (Retrieval-Augmented Generation).

El sistema responde a una brecha clave en los procesos de auditoría y control de calidad en agroexportación (producción, acopio, logística, almacenamiento y cumplimiento fitosanitario), los cuales suelen analizarse mediante fuentes de datos fragmentadas. Al integrar explicabilidad y reportes automáticos trazables, el sistema reduce drásticamente el tiempo de toma de decisiones de los supervisores y garantiza la trazabilidad documental de cada alerta.

### Arquitectura Modular (4 Capas)

```
┌──────────────────────────────────────────────────────┐
│ Capa 4 — Reportes Narrativos LLM + RAG               │ ← Claude / Llama 3 + BM25 Retrieval
│ Generación de reportes trazables anclados en SHAP    │
└──────────────────────────────────────────────────────┘
                          ↑
┌──────────────────────────────────────────────────────┐
│ Capa 3 — Explicabilidad Algorítmica                  │ ← TreeSHAP (SHapley Additive exPlanations)
│ Identificación del top-5 de variables por anomalía    │
└──────────────────────────────────────────────────────┘
                          ↑
┌──────────────────────────────────────────────────────┐
│ Capa 2 — Detección de Anomalías (Ensemble)           │ ← Ensemble de IF + LOF + ECOD (PyOD)
│ Reducción de falsos positivos frente a modelos únicos│
└──────────────────────────────────────────────────────┘
                          ↑
┌──────────────────────────────────────────────────────┐
│ Capa 1 — Predicción Tabular de Series                │ ← GBDT (XGBoost + LightGBM)
│ Justificado para datos tabulares < 50k registros     │
└──────────────────────────────────────────────────────┘
                          ↑
              Dataset Agroexportador Sintético
              (v1.0 - 10,000 registros operativos)
```

---

## 🗂️ Estructura del Repositorio

*   `docs/`: Los 19 archivos numerados que componen los capítulos y anexos de la tesis en formato Markdown activo (fuente única de verdad), además de planes de desarrollo auxiliares.
    *   `docs/tesis.md`: Documento monolítico integrado generado automáticamente a partir de los capítulos activos.
*   `src/`: Código fuente de la aplicación del visor web y utilidades del sistema.
    *   `src/app.py`: Servidor Flask interactivo que levanta la tesis en formato dinámico con soporte de fórmulas matemáticas (MathJax) y hot-reload.
    *   `src/convert_md_to_html.py`: Motor de conversión Markdown a HTML.
    *   `src/generate_synthetic_dataset.py`: Script para generar el conjunto de datos sintéticos transaccionales.
*   `config/`: Archivos de configuración (referencias BibTeX `refs.bib`, estilo de citación APA `apa.csl`, y scripts de arranque de Docker).
*   `formato/`: Plantillas oficiales de la universidad, incluyendo la plantilla oficial de Microsoft Word (`Plantilla - Tesis de Investigación 2026.docx`).
*   `scripts/`: Utilidades de auditoría, purga de referencias y compilación.
    *   `scripts/rebuild_tesis_monolith.py`: Reconstruye `docs/tesis.md` a partir de los 19 capítulos individuales, inyectando saltos de página nativos en OpenXML y HTML.
    *   `scripts/compile_thesis.py`: Compilador integrado que exporta la tesis a formatos DOCX y PDF de calidad editorial.
*   `ia/`: Contexto persistente de desarrollo del agente de Inteligencia Artificial (`memory.md` y `agents.md`).
*   `output/`: Directorio donde se guardan los archivos compilados resultantes (`tesis_v2.docx`, `tesis_v2.pdf` y sus versiones fechadas de control de cambios).

---

## 🐳 Visor de Tesis Interactivo en Docker

La tesis está montada sobre un servidor web local en Flask dentro de un contenedor Docker para facilitar su lectura interactiva, navegación fluida por el índice y la visualización perfecta de fórmulas matemáticas.

### Cómo iniciarlo:
1.  Asegúrate de tener Docker y Docker Compose instalados en tu máquina.
2.  Desde el directorio raíz del proyecto (`D:\tesis_yoset`), levanta el contenedor:
    ```powershell
    docker-compose up --build -d
    ```
3.  Abre tu navegador e ingresa a: **`http://localhost:8000/docs/tesis`**

*Nota: La carpeta `./docs` está montada directamente en caliente. Cualquier edición que realices en los archivos Markdown individuales se verá reflejada en el navegador al instante sin reiniciar el contenedor.*

---

## 🖨️ Guía de Compilación Detallada (Word y PDF)

El proyecto cuenta con un pipeline de compilación profesional en un solo comando que convierte tu tesis en dos formatos de nivel formal listos para entrega:

```
              [Capítulos individuales en docs/]
                              │
               (rebuild_tesis_monolith.py)
                              │
                              ▼
                        [tesis.md]
                  ┌───────────┴───────────┐
                  ▼                       ▼
           (PANDOC en Docker)     (Chrome Headless)
           Con plantilla oficial  Vista de servidor Flask
                  │                       │
                  ▼                       ▼
            [tesis.docx]             [tesis.pdf]
```

### 1. Requisitos Previos en el Host
Antes de compilar, asegúrate de cumplir con los siguientes requisitos en tu máquina Windows (Host):
*   **Docker Desktop:** Corriendo y con el contenedor `tesis-web-viewer` levantado en el puerto 8000 (`docker-compose up -d`).
*   **Python 3.x (o Py Launcher):** Instalado en Windows para ejecutar el script compilador en el host.
*   **Google Chrome o Microsoft Edge:** Instalados en sus rutas por defecto en Windows.

### 2. Flujo de Compilación
El script `scripts/compile_thesis.py` ejecuta las siguientes transformaciones automatizadas:

#### A. Exportación a Word (.DOCX) - *Docker + Pandoc*
El script delega la conversión a Pandoc dentro del contenedor Docker para compilar la tesis monolítica. Esto asegura que la conversión sea multiplataforma:
*   Aplica el estilo y los metadatos de la plantilla de la universidad: `formato/Plantilla - Tesis de Investigación 2026.docx`.
*   Utiliza el motor `--citeproc` mapeado a `config/refs.bib` y el estilo de citación **APA 7** (`config/apa.csl`) para compilar de forma impecable el índice bibliográfico y las citas en el texto.
*   Procesa los **saltos de página nativos en OpenXML** inyectados entre las 19 secciones, asegurando que cada sección física comience en una nueva página dentro de Microsoft Word.

#### B. Exportación a PDF de Calidad Editorial - *Chrome Headless en Host*
En lugar de depender de pesados e inestables compiladores de LaTeX (que suelen fallar por codificación de caracteres UTF-8 o imágenes complejas), el script ejecuta el navegador web en modo *headless* (segundo plano) en el host y realiza una **impresión directa a PDF** de la vista del servidor local (`http://localhost:8000/docs/tesis`). 

Gracias a la inyección de una hoja de estilos de impresión profesional (`@media print` en `src/app.py`), el PDF resultante:
*   **Elimina todo elemento web:** Oculta barras laterales, botones flotantes, menús e indicadores.
*   **Aplica Formato APA 7 Estricto:** Fija la tipografía a **Times New Roman, 12pt**, con interlineado **1.6**, márgenes correctos y texto **justificado**.
*   **Sangría de 1.25 cm:** Sangra automáticamente la primera línea de cada párrafo de acuerdo con el manual APA 7 (con excepciones de sangrado controladas para dedicatorias, agradecimientos, resúmenes y párrafos inmediatamente posteriores a encabezados).
*   **Tablas Académicas:** Diseña las tablas con líneas horizontales formales de color negro, removiendo bordes decorativos innecesarios.
*   **Procesamiento de Fórmulas:** Renders vectoriales y nítidos de las ecuaciones matemáticas procesadas en tiempo real por **MathJax** a **10pt**.
*   **Saltos de Página:** Asegura que cada capítulo comience estrictamente en una nueva página física (`page-break-before: always`).

### 3. Comandos de Ejecución

Para iniciar la compilación (la cual genera tanto las versiones base como copias fechadas de control de cambios dentro de la carpeta `output/`):

1.  Abre una terminal de **PowerShell** en la raíz del proyecto.
2.  Fija la variable de entorno para evitar problemas de codificación de emojis y caracteres especiales en la consola de Windows, y ejecuta el script:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"
    py scripts/compile_thesis.py
    ```

### 4. Resultados Generados (Carpeta `output/`)
Una vez finalizado el proceso de manera exitosa, encontrarás en la carpeta `output/`:
*   `tesis_v2.docx` y `tesis_v2_[AAAA_MM_DD].docx` (Entregable formal en Word para revisiones).
*   `tesis_v2.pdf` y `tesis_v2_[AAAA_MM_DD].pdf` (Lectura de alta calidad tipográfica en Times New Roman para la defensa).

---

## 🎓 Cumplimiento Ético e Integridad Académica

*   **Enfoque Epistemológico:** La presente investigación se enmarca en una postura **post-positivista**, asumiendo que la realidad de los eventos operativos y anomalías puede ser aproximada de forma cuantitativa, pero requiriendo de explicaciones contextuales (SHAP) y supervisión humana (gobernanza) para su correcta validación.
*   **Gobernanza de IA (D.S. N° 115-2025-PCM):** El diseño e implementación del sistema sigue rigurosamente los principios de transparencia algorítmica, equidad y gestión de riesgos establecidos en el Reglamento de la Ley de IA en el Perú.
*   **Gestión de Riesgo de Modelos (Resolución SBS N° 053-2023):** Se adopta esta resolución nacional como marco referencial metodológico de buenas prácticas para garantizar la estabilidad y evitar la degradación del rendimiento de los modelos en producción.
*   **Declaración de uso de IA (Anexo D):** De acuerdo con el manual de ética de la UNSA, el Anexo D (`docs/A4-anexo-ia.md`) detalla formalmente los prompts y el alcance de las herramientas de IA generativa utilizadas únicamente como copiloto en la corrección de estilo, refinamiento bibliográfico y asistencia de formato.
