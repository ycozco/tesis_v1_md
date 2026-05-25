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

## 4. Verificación Realizada

1. **Compilación de Código sin Errores**:
   - `py -m py_compile src/app.py` ejecutado en el host finaliza con éxito (exit code: 0).

2. **Respuestas HTTP del Servidor**:
   - El servidor Flask en Docker recargó en caliente tras detectar la edición.
   - Una batería de pruebas con scripts de Python en el host confirma código `200 OK` en:
     - `/` (Inicio)
     - `/secciones` (Lista de capítulos)
     - `/propuesta` (Arquitectura, Experimentos y Simulador A/B)
     - `/admin` (Panel administrativo)

3. **Verificación de Compilación de la Tesis**:
   - `py -X utf8 scripts/compile_thesis.py` se ejecutó con éxito en el host, generando los entregables finales:
     - `output/tesis-v2.pdf` y `output/tesis-v2.docx`
