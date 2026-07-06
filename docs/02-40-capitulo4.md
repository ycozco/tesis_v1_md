# CAPÍTULO IV — RESULTADOS Y DISCUSIÓN

## 4.1 Resultados de la implementación del sistema

La revisión del repositorio confirma que el sistema de supervisión agroexportadora se encuentra desarrollado y funcional. La solución integra una interfaz React/Vite, servicios backend en Python, persistencia mediante SQLAlchemy sobre PostgreSQL con pgvector, ejecución local con Docker Compose y un pipeline analítico organizado en capas para predicción, detección de anomalías, explicabilidad, generación de reportes y trazabilidad.

El sistema no se limita a presentar vistas estáticas. Dispone de autenticación, dashboard operativo, listado y detalle de alertas, historial de decisiones, telemetría experimental, métricas de integridad, exploración de datos, administración de documentos RAG, configuración del ensemble y gestión de usuarios. La evidencia de implementación corresponde a código ejecutable, modelos persistentes, datos semilla, rutas REST, relaciones ORM y capturas de las principales pantallas.

### 4.1.1 Componentes funcionales verificados

| Componente | Evidencia del repositorio | Estado |
|---|---|---|
| Interfaz web | `sistema-web-agro/frontend/src/pages/` | Implementado |
| Backend REST | `sistema-web-agro/backend/app.py` | Implementado |
| Persistencia | `sistema-web-agro/backend/models.py` | Implementado |
| Datos de prueba | `sistema-web-agro/backend/init_db.py` | Implementado para validación funcional |
| Configuración analítica | endpoints y vista de configuración | Implementado |
| Pipeline de IA | XGBoost, PyOD, SHAP y RAG | Implementado con evidencia preliminar |
| Trazabilidad | `PipelineRun`, `ArtifactLineage`, UUID y hashes | Implementado parcialmente y sujeto a auditoría final |
| Despliegue | `docker-compose.yml`, Gunicorn/Nginx/PostgreSQL | Implementado para entorno local reproducible |
| Servicios FastAPI/Uvicorn | punto de entrada ASGI y endpoints de salud | Incorporados como consolidación tecnológica |

### 4.1.2 Arquitectura operativa verificada

La arquitectura desplegada mantiene tres niveles principales. El cliente React/Vite presenta los módulos de interacción del auditor. El backend Python expone servicios REST, ejecuta el pipeline analítico y gestiona la persistencia mediante SQLAlchemy. PostgreSQL 15 con pgvector almacena usuarios, alertas, decisiones, explicaciones SHAP, documentos normativos, reportes y registros de trazabilidad.

Docker Compose organiza los servicios de base de datos, backend y frontend. Gunicorn atiende la aplicación Flask heredada y Nginx sirve el cliente React. FastAPI y Uvicorn ya forman parte del repositorio mediante un punto de entrada ASGI, configuración de CORS, ciclo de vida y endpoints de salud. La permanencia temporal de rutas en Flask corresponde a compatibilidad y consolidación progresiva, no a ausencia de implementación.

### 4.1.3 Persistencia y correcciones ORM

El modelo relacional incorpora las entidades `Usuario`, `OperacionAlerta`, `DecisionAuditoria`, `ExplicacionSHAP`, `DocumentoNormativo`, `ConfiguracionPipeline`, `PipelineRun`, `GeneratedReport`, `ArtifactLineage` y `SecurityLog`.

La revisión de los commits recientes confirma la incorporación de una relación uno a uno entre `OperacionAlerta` y `GeneratedReport`. Esta corrección permite que el reporte generado quede vinculado explícitamente con la alerta que lo originó y reduce problemas de orden de inserción durante la carga de datos. También se corrigió la resolución de rutas SQLite para evitar dependencias de la carpeta desde la cual se ejecuta el sistema.

## 4.2 Resultados funcionales de los módulos del sistema

### 4.2.1 Autenticación y condiciones experimentales

El sistema dispone de usuarios con roles `ADMIN` y `AUDITOR`. Durante la autenticación puede asignarse una condición experimental para comparar dos formas de presentación:

- **INTEGRADO:** presenta predicción, scores de anomalía, SHAP, evidencia RAG y reporte trazable.
- **AISLADO:** presenta resultados técnicos sin la capa completa de explicación narrativa.

Esta diferenciación permite capturar tiempo de decisión, comprensión percibida y clasificación emitida por el usuario. La existencia de las condiciones está implementada; la evaluación con participantes reales continúa pendiente.

### 4.2.2 Dashboard, alertas y detalle analítico

El dashboard resume estadísticas globales, alertas prioritarias y estado operativo. La bandeja de alertas permite filtrar operaciones por producto, mercado, estado y nivel de severidad. La vista de detalle concentra el flujo principal del sistema y presenta:

1. datos de la operación;
2. valor FOB declarado y esperado;
3. score combinado de anomalía;
4. contribuciones locales SHAP;
5. curva o visualización de probabilidad;
6. evidencia recuperada por RAG;
7. reporte narrativo estructurado;
8. formulario de decisión del auditor;
9. panel de logs del pipeline.

Los commits recientes muestran mejoras específicas en la vista `Detail.jsx`: modularización de SHAP y RAG, renderizado enriquecido de reportes Markdown, interpretación de negritas y código en línea, incorporación de un gráfico de probabilidad, panel de logs minimizable y rediseño de la distribución en tres columnas. También se adecuó la vista histórica `AuditDetail` para mantener consistencia visual con el detalle principal.

### 4.2.3 Explorador de datos y biblioteca RAG

La vista de datos permite explorar registros y administrar documentos normativos. Los usuarios administradores pueden incorporar nuevas normativas, generar sus embeddings y almacenarlas en pgvector. El backend expone rutas para listar e indexar documentos y utiliza similitud coseno para recuperar los fragmentos más relevantes.

El sistema incluye inicialmente documentos de la FDA, SENASA y el reglamento peruano de inteligencia artificial. Estas fuentes se utilizan como evidencia estructurada durante la generación del reporte. Su presencia en el sistema constituye evidencia funcional; la pertinencia jurídica definitiva debe validarse documentalmente antes de la versión final de la tesis.

### 4.2.4 Configuración del ensemble

La vista de configuración permite consultar y modificar los pesos de Isolation Forest, Local Outlier Factor y ECOD, además del umbral global de alerta. La configuración inicial utiliza ponderaciones de 0.45, 0.30 y 0.25, respectivamente, con un umbral preliminar de 0.65.

Estos valores permiten demostrar el funcionamiento configurable del sistema. No deben interpretarse como hiperparámetros óptimos hasta completar la calibración con el dataset experimental final.

## 4.3 Resultados de datos y ejecución preliminar

### 4.3.1 Auditoría del conjunto de datos

La ejecución registrada en los logs de calidad cargó 40 672 filas y 21 columnas. Después de excluir 379 registros correspondientes a cacao, quedaron 40 293 filas. La validación final clasificó 40 289 registros como válidos y 4 como rechazados.

La distribución registrada fue:

| Producto | Registros válidos |
|---|---:|
| Palta | 17 360 |
| Uva | 15 697 |
| Arándano | 4 633 |
| Espárrago | 2 599 |
| **Total** | **40 289** |

Estos resultados demuestran la ejecución de un proceso de carga y control de calidad. Sin embargo, la tesis mantiene como alcance principal palta, uva fresca y arándano; por ello, el espárrago debe excluirse del conjunto final utilizado para aceptar o rechazar las hipótesis.

### 4.3.2 Datos semilla para validación funcional

`init_db.py` crea usuarios, alertas pendientes, alertas en revisión, decisiones históricas, explicaciones, configuración y documentos normativos. También entrena y serializa modelos de prueba con semilla aleatoria 42 para demostrar la integración de XGBoost, StandardScaler, Isolation Forest, LOF y ECOD.

Los valores generados por este proceso son datos de prueba. Su función es verificar rutas, relaciones, visualizaciones y flujo completo. No constituyen resultados científicos finales.

### 4.3.3 Telemetría preliminar

La documentación del sistema registra ejemplos semilla para las condiciones INTEGRADO y AISLADO. En estos ejemplos, la condición integrada presenta menores tiempos de decisión y mayor comprensión Likert. Esta diferencia es únicamente una hipótesis preliminar derivada de datos semilla y no puede emplearse para aceptar la hipótesis general.

La validación definitiva requiere participantes reales, protocolo de consentimiento, tamaño de muestra justificado, registro automático de tiempos y prueba estadística apropiada.

## 4.4 Discusión de los resultados de implementación

La evidencia del repositorio permite afirmar que el sistema fue desarrollado y que sus módulos principales están integrados. La contribución actual no es solo una interfaz: existe una cadena completa que vincula datos, predicción, detección, explicación, recuperación documental, reporte y decisión humana.

El uso conjunto de SHAP y RAG mejora la capacidad de presentar resultados técnicos de forma comprensible. SHAP muestra la contribución cuantitativa de las variables y RAG incorpora contexto documental. Esta combinación responde a la necesidad de evitar que el modelo de lenguaje genere explicaciones sin evidencia.

La modularización reciente del pipeline en carpetas `pipeline/etl/`, `pipeline/preparation/` y `pipeline/core/` fortalece la reproducibilidad. El orquestador central registra la secuencia de ejecución y relaciona las salidas con el Capítulo IV. Esta organización reduce el acoplamiento y facilita identificar qué archivo produce cada métrica o artefacto.

No obstante, la implementación funcional no equivale todavía a validación científica completa. Permanecen pendientes la congelación del dataset final, la partición temporal, la calibración de detectores, las métricas definitivas de predicción y anomalías, el estudio con usuarios y el análisis estadístico.

## 4.5 Limitaciones y trabajo pendiente

Las principales limitaciones identificadas son:

1. parte de la demostración funcional utiliza datos semilla o sintéticos;
2. las métricas A/B actuales son preliminares;
3. los pesos del ensemble requieren calibración experimental;
4. la autenticación debe consolidarse con JWT y control de roles;
5. deben retirarse secretos del repositorio y reforzarse las variables de entorno;
6. la integridad referencial y el linaje deben auditarse de extremo a extremo;
7. se requieren pruebas automatizadas, de contrato, integración y carga;
8. la equivalencia de rutas FastAPI debe completarse antes de retirar Flask;
9. las capturas finales deben vincularse con commit, fecha y función demostrada.

En consecuencia, el Capítulo IV puede presentar como resultados consolidados la implementación del sistema, la existencia de sus módulos, la arquitectura desplegada, las relaciones de datos y la ejecución funcional. Las métricas de desempeño, efectividad y comprensión deben mantenerse como preliminares hasta completar el protocolo experimental.