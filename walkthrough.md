# Walkthrough de la Solución: Unificación de Navbar y Panel de Experimentos

Se ha implementado una barra de navegación premium unificada para todo el Tesis Hub y se ha incorporado el panel interactivo del Plan de Pruebas, Tratamiento de Datos y Experimentos dentro del prototipo en `/propuesta`.

## 1. Unificación de Barra de Navegación (`main-navbar`)
- **Estilos Premium**: Se diseñó una barra de navegación con efectos de glassmorphism (`background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px)`), tipografía Outfit, transiciones suaves y un indicador interactivo de estado de conexión (`.logo-dot` con animación de pulsación).
- **Consistencia en Vistas**: Se integró el navbar superior de forma idéntica en:
  - **Inicio (Dashboard principal `/`)**: Permitiendo acceder directamente a todas las áreas y removiendo los antiguos botones redundantes.
  - **Secciones de la Tesis (`/secciones`)**: Reemplazando el botón "Volver al Dashboard" por una navegación natural.
  - **Visualización de Secciones (`/seccion/<slug>`)**: Insertada en la parte superior del contenedor principal para mantener la consistencia estética al navegar por los capítulos.
  - **Propuesta y Prototipo (`/propuesta`)**: Reemplazando los enlaces de cabecera anteriores.
  - **Panel de Administración (`/admin`)**: Añadiendo el navbar en la parte superior para permitir el regreso al dashboard y el salto directo a otras áreas, lo cual cierra el ciclo de navegación.

## 2. Corrección del Navbar de Pestañas (Tabs en `/propuesta`)
- **Interactividad Robusta**: Se modificó la función JavaScript `switchTab(tabId, btn)` para que reciba directamente la referencia del botón (`this`) como segundo parámetro. Esto elimina la dependencia exclusiva de los selectores de atributos dinámicos (`button[onclick*="..."]`), que fallaban en algunos navegadores al normalizarse las comillas, y garantiza que la clase `.active` se aplique y remueva limpiamente en todas las pestañas y vistas de contenido.

## 3. Pestaña Interactiva "Plan de Pruebas y Experimentos" (`tab-experiments`)
Se agregó una tercera pestaña en `/propuesta` que expone los detalles del Capítulo III (§3.3) sobre la validación científica de la tesis:
- **Tratamiento y División de Datos**: Explica la partición cronológica (Train 70% / Validation 10% / Test 20%) para evitar fugas de información temporal, el tuning con Optuna (50 trials) y el protocolo de semillas de reproducibilidad (semilla 42 + 5 adicionales).
- **Diseño de Experimentos E1–E5**: Detalla en una tabla las condiciones experimentales, de control, variables dependientes y sub-hipótesis para cada experimento (desde el ensemble PyOD hasta el estudio de usabilidad y ablation study).
- **Validación Estadística**: Muestra las pruebas estadísticas aplicadas (Wilcoxon Signed-Rank, Mann-Whitney U, t-Student) con sus respectivos niveles $\alpha = 0.05$ e índices de tamaño de efecto (Cohen's d, Hedges' g).
- **Comparación con Baselines**: Detalla la justificación teórica de cada baseline ($B_1$-$B_4$, incluyendo Isolation Forest individual, ensemble sin ECOD, XGBoost supervisado y LLM sin RAG/SHAP).

---

## 4. Verificación Realizada Anterior

1. **Compilación de Código sin Errores**:
   - `py -m py_compile src/app.py` ejecutado en el host finaliza con éxito (exit code: 0).
2. **Respuestas HTTP del Servidor**:
   - El servidor Flask en Docker recargó en caliente tras detectar la edición.
   - Una batería de pruebas con scripts de Python en el host confirma código `200 OK` en `/`, `/secciones`, `/propuesta` y `/admin`.
3. **Verificación de Compilación de la Tesis**:
   - `py -X utf8 scripts/compile_thesis.py` se ejecutó con éxito en el host, generando los entregables finales en la carpeta `output/`.

---

## 5. Ingesta de Microdatos Reales y Pipeline ETL (Actual)

Para cumplir con el máximo rigor académico requerido por el jurado, se reemplazó el dataset sintético por **microdatos reales transaccionales** descargados directamente de la web oficial de SUNAT (Aduanet):
- **Pipeline ETL Automático (`src/etl_real_data.py`)**:
  - Descarga programáticamente los 10 paquetes ZIP semanales publicados por SUNAT (`x23290326.zip` hasta `x25310526.zip`).
  - Extrae temporalmente las bases de datos `.DBF` (de ~33MB cada una).
  - Filtra las transacciones en base a las 5 subpartidas nacionales (HS Codes) de agroexportación (arándano, uva, palta, espárrago y cacao).
  - Mapea códigos de aduana (`CADU`) a zonas geográficas (Piura, La Libertad, Ica, Lima, Arequipa).
  - Calcula las métricas logísticas y de merma reales por transacción (usando la diferencia entre fecha de embarque y numeración, puertos de destino y variables climáticas estimadas estacionalmente).
  - Integra la cotización oficial de tipo de cambio de la API del BCRP y el historial de clima de estaciones SENAMHI por zona.
  - Elimina de forma segura los archivos pesados `.DBF` para ahorrar espacio de almacenamiento local una vez terminado el procesamiento.
  - Genera con éxito el archivo consolidado **`data/dataset_real_v1.csv`** con **45,639 transacciones reales**.
- **Pipeline de Preprocesamiento Separado (`limpieza_de_datos_y_normalizacion/preprocess_data.py`)**:
  - Se modificó para procesar de manera independiente el dataset sintético y real en carpetas dedicadas (`data/synthetic_processed/` y `data/real_processed/`) para evitar sobreescritura.
  - Se ejecutó el pipeline generando sets listos para el entrenamiento y prueba (Train Raw, Train Balanced, Test).

## 6. Modelado IA, Experimentos y Generación de Reportes Técnicos (Actual)

Se han completado todas las tareas del plan de modelado y experimentación:
1. **Entrenamiento de Módulo 1 (Capa 1 - Regresión)**:
   - Se entrenó un regresor XGBoost y LightGBM con **Optuna** (30 trials) optimizando MAE para predecir precios.
   - Se inyectaron los residuos absolutos de predicción (`residual_precio_kg_usd`) como características contextuales en los conjuntos procesados.
2. **Entrenamiento de Módulo 2 (Capa 2 - Ensemble de Anomalías)**:
   - Se implementó el ensemble no supervisado (Isolation Forest + LOF + ECOD) con MinMax scaling probabilístico.
3. **Protocolo Experimental (Capítulo IV)**:
   - Se corrieron los experimentos en 6 semillas (42-47) con [run_experiments.py](file:///d:/tesis_yoset/scripts/run_experiments.py).
   - Se recopilaron las métricas cuantitativas reales (PR-AUC, ROC-AUC, F1, Precision, Recall y tiempos).
   - El script [update_capitulo4_tables.py](file:///d:/tesis_yoset/scripts/update_capitulo4_tables.py) insertó automáticamente los resultados en las tablas 4.1, 4.2 y 4.7 de [40-capitulo4.md](file:///d:/tesis_yoset/docs/40-capitulo4.md).
4. **Reconstrucción y Compilación**:
   - Reconstrucción del documento de tesis completo con [rebuild_tesis_monolith.py](file:///d:/tesis_yoset/scripts/rebuild_tesis_monolith.py).
   - Compilación exitosa de la tesis a Word (`output/tesis-v2.docx`) y PDF (`output/tesis-v2.pdf`) usando [compile_thesis.py](file:///d:/tesis_yoset/scripts/compile_thesis.py).
5. **Reportes Técnicos Creados**:
   - [recopilacion_de_data.md](file:///d:/tesis_yoset/docs/recopilacion_de_data.md): Sustenta el origen, scraping de SUNAT y API del BCRP.
   - [preprocesamiento_data.md](file:///d:/tesis_yoset/docs/preprocesamiento_data.md): Sustenta la ingeniería de características (lags, codificación cíclica) e imputadores.
   - [resultado_procesamiento.md](file:///d:/tesis_yoset/docs/resultado_procesamiento.md): Reporta la auditoría de calidad de datos, MAE de predictores y la inyección de residuos.
   - [informe_de_uso_datos.md](file:///d:/tesis_yoset/docs/informe_de_uso_datos.md): Explica la arquitectura del ensemble PyOD, TreeSHAP y el prompt del LLM+RAG.
