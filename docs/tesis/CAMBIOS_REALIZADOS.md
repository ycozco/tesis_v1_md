# Registro de Cambios Realizados

Este documento detalla las modificaciones y correcciones aplicadas tanto al código del prototipo técnico como a la estructura académica del documento de tesis.

---

## 1. Tabla de Cambios Realizados

| Archivo | Sección | Problema Encontrado | Cambio Realizado | Justificación | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `module1_prediction.py` | Capa 1: Regresores GBDT | Descarte erróneo de las columnas de cadenas `product_code` y `market_aggregated` tras concatenar variables dummies, causando `KeyError`. | Se modificó la concatenación de dummies para preservar los nombres de las columnas originales. | Permite agrupar las predicciones y series de tiempo de forma correcta en el pipeline. | **Corregido** |
| `module2_anomaly.py` | Capa 2: Ensemble y Validación | NameError en el cálculo de recall al usar la variable no definida `types` en el bucle final. | Se renombró la variable temporal a `anomaly_types`. | Evita caídas del script durante la validación del ensemble no supervisado. | **Corregido** |
| `module3_shap.py` | Capa 3: Explicabilidad SHAP | Error de corrupción de memoria Heap C++ (`0xC0000374`) en TreeSHAP por desalineación de columnas en XGBoost. | Se alinearon y seleccionaron las columnas de test en el orden y número exacto (`108` variables) del entrenamiento. | Garantiza la reproducibilidad de las explicaciones locales sin colapsar el proceso en Windows. | **Corregido** |
| `module4_rag.py` | Capa 4: RAG e Informes | Excepciones por ausencia de importación de librerías esenciales `json` y `numpy`. | Se agregaron las importaciones necesarias al inicio del archivo. | Permite procesar los JSONs de evidencia y convertir los arrays numéricos de SHAP en el prompt del LLM. | **Corregido** |
| `run_all.py` | Orquestador y Reportes | Fallos de decodificación en Windows por acentos devueltos por subprocesos. Definiciones incompletas. | Se añadió `errors="replace"` en la decodificación de `subprocess.run` y se definió globalmente `MODELS_DIR`. | Asegura que el pipeline maestro ejecute todas las capas secuenciales en entornos Windows sin interrupciones. | **Corregido** |
| `build_github_pages.py` | Generador del sitio estático | Ausencia de lógica para exportar los endpoints JSON de la API del panel del supervisor. | Se implementaron los métodos `compile_supervisor` y `export_supervisor_api` para generar archivos estáticos en `api/`. | Permite que el Dashboard en GitHub Pages sea 100% funcional de manera estática y offline. | **Corregido** |
| `02-95-tesis.md` | General | Falta de alineación en alcance, variables y unidad de análisis. Estructura desorganizada. | Reestructuración de la tesis de extremo a extremo, excluyendo cacao del núcleo y declarando proxies. | Alinea la redacción teórica con el comportamiento real del pipeline y los datos aduaneros. | **Corregido** |
| `docs/tesis/` | Todo | Ausencia de documentos obligatorios para la entrega formal de tesis y auditoría. | Creación de archivos de soporte académico (portada, diccionarios, matrices, auditoría de referencias, etc.). | Satisface las exigencias de formato de la Escuela Profesional de Ingeniería de Sistemas de la UNSA. | **Implementado** |

---

## 2. Clasificación del Estado de los Entregables

1.  **Corregido:** Se solucionaron bugs o NameErrors que impedían la ejecución del pipeline y del compilador.
2.  **Implementado:** Se crearon nuevos archivos necesarios para completar la arquitectura de datos o el sustento de la tesis.
3.  **Pendiente por dato:** Requiere incorporar microdatos aduaneros anuales completos del periodo 2018-2025 de ADUANET si se decide extender el modelado nacional (los DBFs SUNAT actuales cubren 2026).
4.  **Pendiente por confirmación académica:** Requiere revisión por parte del alumno y su asesor (nombre oficial del asesor, denominación de la línea oficial, reclutamiento de evaluadores humanos).
