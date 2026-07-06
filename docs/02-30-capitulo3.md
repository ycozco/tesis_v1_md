# CAPÍTULO III: DESARROLLO E IMPLEMENTACIÓN DEL PROTOTIPO FUNCIONAL

## 3.1 Generalidades del prototipo funcional

### 3.1.1 Propósito del prototipo

El prototipo funcional de supervisión agroexportadora fue desarrollado con el propósito de integrar en una sola plataforma el procesamiento de datos de exportación, la estimación semanal del valor unitario FOB y del volumen exportado, la detección multivariable de anomalías, la explicación de resultados mediante SHAP, la recuperación de evidencia documental mediante RAG y el registro trazable de las decisiones realizadas por los usuarios.

El prototipo está orientado a operaciones de palta, uva fresca y arándano registradas en el Perú. La unidad de análisis corresponde a la combinación producto, mercado de destino y semana ISO. El sistema apoya la revisión de comportamientos inusuales, pero no sustituye la decisión del analista ni ejecuta acciones automáticas sobre operaciones reales.

La implementación tiene carácter de prototipo funcional y experimental. Sus módulos principales pueden ejecutarse de manera integrada y permiten demostrar el flujo propuesto; sin embargo, la calibración definitiva de los modelos, la validación con usuarios y el endurecimiento para un entorno productivo permanecen fuera del estado actual del desarrollo.

### 3.1.2 Alcance funcional

El prototipo permite cargar y preparar fuentes agroexportadoras, validar registros, generar datasets por capas, agrupar operaciones semanalmente, construir variables predictivas, estimar valor unitario FOB y volumen, calcular residuos, detectar anomalías mediante Isolation Forest, Local Outlier Factor y ECOD, consolidar puntuaciones, explicar predicciones mediante SHAP, recuperar documentos relevantes mediante RAG, generar reportes, registrar decisiones, conservar trazabilidad y visualizar el proceso mediante una interfaz web.

No forman parte del alcance actual la integración en tiempo real con SUNAT, sistemas ERP, sensores, plataformas empresariales ni decisiones automáticas de bloqueo o intervención.

### 3.1.3 Usuarios y actores

Los actores implementados en el prototipo son el Administrador y el Auditor. El Administrador gestiona usuarios, parámetros del ensemble, documentos RAG y elementos de configuración. El Auditor consulta alertas, revisa predicciones, puntuaciones, explicaciones SHAP, evidencia RAG y reportes, y registra una decisión con su justificación.

Como interesados conceptuales se consideran el analista de datos, responsable de preparar fuentes y revisar calidad; el ingeniero de aprendizaje automático, encargado del entrenamiento y versionamiento de modelos; el supervisor, que revisa decisiones y reportes; y el investigador, que ejecuta y documenta los experimentos.

### 3.1.4 Entradas del prototipo

Las entradas principales son los registros de exportación provenientes de SUNAT o ADUANET, los tipos de cambio publicados por el BCRP, los precios mayoristas de SISAP o MIDAGRI, las variables climáticas de NASA POWER, los documentos normativos de SENASA, FDA y normativa peruana, y los parámetros de ejecución almacenados en archivos de configuración o base de datos.

Estas fuentes presentan diferentes estructuras, formatos y granularidades. Para permitir su integración, los registros se normalizan y agregan a una frecuencia semanal. Las variables contextuales se incorporan únicamente cuando existe correspondencia temporal y metodológica documentada.

### 3.1.5 Salidas del prototipo

Las salidas principales son el dataset semanal producto-mercado-semana, las predicciones de valor unitario FOB y volumen, los scores individuales de Isolation Forest, LOF y ECOD, el score combinado del ensemble, la severidad de cada alerta, las explicaciones SHAP, los fragmentos recuperados mediante RAG, el reporte técnico, la decisión del auditor y el linaje de ejecución basado en identificadores, versiones y hashes.

### 3.1.6 Restricciones

El prototipo opera mediante procesamiento por lotes semanales y no consume telemetría en tiempo real. Algunas variables son proxies agregados y no mediciones directas. Los datos semilla se utilizan para validar visualmente e integrar módulos, pero no sustituyen al dataset experimental final. Flask permanece como componente heredado mientras FastAPI y Uvicorn se incorporan progresivamente. El prototipo no está preparado todavía para un despliegue productivo ni para la toma de decisiones automáticas.

### 3.1.7 Principios de diseño

El diseño se fundamenta en la separación de responsabilidades, la prioridad de la evidencia sobre la narrativa, la intervención humana, la trazabilidad, el control factual, el mínimo privilegio, la reproducibilidad y el desacoplamiento modular. Los cálculos cuantitativos se mantienen separados de la redacción generativa; toda alerta requiere revisión humana; y cada artefacto debe poder relacionarse con los datos, modelos y configuraciones que lo originaron.

## 3.2 Auditoría inicial de datos y componentes

### 3.2.1 Objetivo de la auditoría

La auditoría inicial tuvo como finalidad determinar si los archivos disponibles, los scripts de procesamiento y los componentes del prototipo permitían construir una cadena reproducible desde las fuentes de origen hasta la generación de una alerta trazable.

La revisión comprendió la estructura de los archivos, cobertura temporal, calidad, granularidad, valores nulos, duplicados, productos, mercados, rutas de ejecución, modelos serializados, persistencia, servicios backend, vistas del frontend y mecanismos de trazabilidad.

### 3.2.2 Procedimiento de auditoría

El procedimiento incluyó el inventario de archivos, la inspección de dimensiones y tipos, el análisis de nulos y duplicados, la validación de fechas, códigos arancelarios y unidades, la clasificación de datos como reales, agregados, proxies o sintéticos, el cálculo de hashes, la revisión de scripts y modelos, y la verificación del flujo entre frontend, backend y persistencia.

**Figura 3.1. Flujo de auditoría inicial de datos y componentes del prototipo.**

La figura representa las actividades realizadas para evaluar la disponibilidad, calidad, procedencia y trazabilidad de los datos, así como la correspondencia entre scripts analíticos, modelos, servicios backend y vistas del prototipo. El proceso comienza con el inventario de fuentes y finaliza con el registro de hallazgos y acciones correctivas.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_1_flujo_auditoria.mmd`.

### 3.2.3 Resultados de la auditoría de datos

El conjunto inicial contiene 40 672 registros y 21 columnas. Después de excluir 379 registros de cacao quedaron 40 293 registros evaluados. La validación clasificó 40 289 como válidos y 4 como rechazados. La agregación semanal preliminar produjo 8 340 filas en la capa gold, 139 variables en la matriz predictiva y 170 variables en la matriz utilizada por los detectores de anomalías.

**Figura 3.2. Evolución de registros durante la preparación inicial.**

La figura muestra la cantidad de registros conservados después de excluir productos fuera del alcance, aplicar las reglas de calidad y ejecutar la agregación semanal. Los valores corresponden al estado preliminar y deberán actualizarse cuando se congele el dataset gold definitivo.

**Fuente:** elaboración propia a partir de los reportes de calidad. Diagrama Mermaid: `docs/diagrams/figura_3_2_evolucion_registros.mmd`.

### 3.2.4 Hallazgos y decisiones metodológicas

La auditoría identificó la presencia de cacao y espárrago fuera del núcleo experimental, cuatro registros rechazados, posibles duplicados funcionales, diferencias de granularidad y variables climáticas utilizadas como proxy regional. También evidenció la necesidad de congelar el dataset gold, completar las pruebas de fuga temporal y mantener una separación explícita entre datos reales, datos agregados, proxies y datos semilla.

Como decisiones metodológicas se adoptó la frecuencia semanal, la unidad producto-mercado-semana, la exclusión de cacao, la separación del espárrago de las conclusiones principales, el uso de valor unitario FOB y volumen como objetivos y la organización del procesamiento en capas raw, bronze, silver, gold y features.

## 3.3 Requisitos del prototipo funcional

### 3.3.1 Requisitos funcionales

Los requisitos funcionales comprenden la importación de fuentes, validación y normalización de registros, anonimización, agregación semanal, entrenamiento de modelos, generación de predicciones, detección de anomalías, explicación SHAP, recuperación de documentos, generación y validación de reportes, consulta de trazabilidad, revisión de alertas y exportación de resultados.

Cada requisito se vincula con un actor, una entrada, una salida verificable y un módulo del prototipo. El cumplimiento funcional se evalúa mediante rutas ejecutables, persistencia, registros y evidencia visual.

### 3.3.2 Requisitos no funcionales

Los requisitos no funcionales considerados son reproducibilidad, auditabilidad, modularidad, seguridad, privacidad, usabilidad, portabilidad y disponibilidad experimental. El prototipo debe registrar semillas, versiones y hashes; mantener separados los módulos ETL, predicción, anomalías, SHAP, RAG y servicios; proteger credenciales mediante variables de entorno; anonimizar identificadores; y poder ejecutarse en un entorno local reproducible mediante Docker Compose.

**Figura 3.3. Casos de uso principales del prototipo funcional.**

La figura presenta las funciones disponibles para los actores Administrador y Auditor. El Administrador dispone de operaciones de configuración, usuarios y documentos, mientras que el Auditor concentra las tareas de consulta, análisis y registro de decisiones.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_3_casos_uso.mmd`.

## 3.4 Arquitectura del prototipo funcional

### 3.4.1 Enfoque arquitectónico

El prototipo adopta una arquitectura modular por capas. La separación permite aislar la adquisición y preparación de datos, el procesamiento analítico, la persistencia, los servicios de aplicación y la interfaz de usuario.

El flujo analítico se ejecuta principalmente por lotes, mientras que la aplicación web permite consultar resultados almacenados y registrar decisiones. La arquitectura representa una configuración reproducible para desarrollo, demostración y experimentación, no un despliegue productivo distribuido.

### 3.4.2 Capas de la arquitectura

La capa de fuentes reúne SUNAT o ADUANET, BCRP, SISAP, NASA POWER, SENASA, FDA y archivos de configuración. La capa de datos organiza la información en raw, bronze, silver, gold, prediction features y anomaly features. La capa analítica ejecuta XGBoost, LightGBM, StandardScaler, Isolation Forest, LOF, ECOD y SHAP.

La capa de conocimiento administra documentos, fragmentos, embeddings, recuperación por similitud, generación narrativa y validación factual. La capa de servicios contiene autenticación, alertas, configuración, telemetría, reportes e integridad. La capa de presentación está construida con React y Vite. La persistencia combina PostgreSQL, pgvector, SQLAlchemy, archivos Parquet, modelos serializados y artefactos trazables.

**Figura 3.4. Arquitectura lógica del prototipo funcional de supervisión agroexportadora.**

La figura representa las capas principales de la solución. Las fuentes externas alimentan el proceso de preparación de datos por niveles raw, bronze, silver y gold. El dataset gold permite generar variables para los modelos predictivos y de anomalías. Las predicciones, puntuaciones, explicaciones SHAP y evidencias documentales recuperadas mediante RAG son expuestas por los servicios backend y consumidas desde la interfaz React.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_4_arquitectura_logica.mmd`.

### 3.4.3 Arquitectura de despliegue

Nginx atiende las solicitudes del navegador y sirve la interfaz React. El backend Python expone los servicios de aplicación y accede a PostgreSQL, pgvector, los modelos serializados y los artefactos analíticos. El pipeline procesa las fuentes y actualiza datasets, modelos y resultados.

La coexistencia de Flask y FastAPI representa una transición tecnológica. Flask mantiene rutas funcionales existentes, mientras que FastAPI y Uvicorn se incorporan progresivamente como objetivo de consolidación del backend.

**Figura 3.5. Arquitectura de despliegue del prototipo en entorno local.**

La figura muestra la distribución de los componentes durante la ejecución del prototipo, incluyendo navegador, Nginx, frontend React, backend Python, PostgreSQL, pgvector, pipeline, modelos serializados y artefactos analíticos.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_5_arquitectura_despliegue.mmd`.

### 3.4.4 Arquitectura de datos

La capa raw conserva los archivos originales sin transformación metodológica. Bronze realiza una conversión estructural. Silver aplica reglas de limpieza, normalización, homologación y anonimización. Gold consolida la unidad producto-mercado-semana. A partir de gold se generan matrices especializadas para predicción y detección de anomalías.

**Figura 3.6. Arquitectura de datos por capas.**

La figura representa el proceso de transformación de los archivos desde su estado original hasta los conjuntos utilizados por los modelos. También muestra la derivación de prediction features, anomaly features, predicciones, residuos, scores, explicaciones y reportes.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_6_arquitectura_datos.mmd`.

### 3.4.5 Arquitectura de componentes web

Cada vista del frontend consume servicios especializados del backend. La autenticación se relaciona con el servicio de usuarios y sesiones; el dashboard y la bandeja consultan alertas; la vista de detalle integra predicción, anomalías, SHAP, RAG, reportes y decisión; y las vistas de telemetría, integridad, configuración y usuarios consumen sus servicios correspondientes.

SQLAlchemy actúa como capa de acceso a PostgreSQL, mientras que pgvector almacena y recupera representaciones vectoriales utilizadas por el componente RAG.

**Figura 3.7. Arquitectura de componentes de la aplicación web.**

La figura muestra la correspondencia entre las vistas de la interfaz, los servicios backend y la persistencia. Permite identificar qué componente atiende cada interacción y qué almacenamiento utiliza.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_7_componentes_web.mmd`.

## 3.5 Modelo de datos y persistencia

### 3.5.1 Entidades principales

El modelo relacional incluye Usuario, OperacionAlerta, DecisionAuditoria, ExplicacionSHAP, DocumentoNormativo, ConfiguracionPipeline, PipelineRun, GeneratedReport, ArtifactLineage y SecurityLog.

Usuario almacena credenciales y roles. OperacionAlerta concentra los valores observados y esperados, residuos, puntuaciones y severidad. DecisionAuditoria registra la condición experimental, decisión, justificación, comprensión y tiempo empleado. ExplicacionSHAP almacena contribuciones locales. DocumentoNormativo conserva el corpus utilizado por RAG. GeneratedReport guarda el reporte y sus validaciones. PipelineRun y ArtifactLineage permiten reconstruir la ejecución y sus artefactos.

### 3.5.2 Relaciones y trazabilidad

Un usuario puede registrar varias decisiones. Una alerta puede disponer de una explicación SHAP y un reporte. Una ejecución del pipeline puede producir varias alertas y artefactos. La configuración utilizada se relaciona con la ejecución. Los documentos normativos aportan evidencia al reporte.

**Figura 3.8. Modelo de datos del prototipo funcional.**

La figura representa las principales entidades persistidas, sus relaciones y los campos necesarios para reconstruir datos, modelos, alertas, explicaciones, reportes y decisiones.

**Fuente:** elaboración propia a partir del modelo SQLAlchemy. Diagrama Mermaid: `docs/diagrams/figura_3_8_modelo_datos.mmd`.

## 3.6 Preparación e integración de datos

### 3.6.1 Extracción y conservación de fuentes

Los archivos de origen se conservan en la capa raw sin modificar. Los formatos DBF, CSV, XLS y JSON se transforman a estructuras tabulares, manteniendo fecha de descarga, ruta, dimensiones y hash.

### 3.6.2 Limpieza y normalización

La preparación incluye validación de fechas, tipos, códigos arancelarios, países, pesos y valores FOB. Se eliminan registros fuera del alcance cuando la regla está documentada, se aíslan registros rechazados y se mantienen los duplicados potenciales hasta confirmar si representan operaciones legítimas o repetidas.

### 3.6.3 Agregación semanal

Las operaciones se agrupan por producto, mercado de destino y semana ISO. El valor unitario FOB se calcula dividiendo el FOB total entre el peso neto, mientras que el volumen corresponde a la suma del peso neto semanal.

### 3.6.4 Ingeniería de características y prevención de fuga

Las variables temporales incluyen rezagos, medias móviles, desviaciones, variaciones y componentes cíclicos. Las ventanas se desplazan una semana mediante `shift(1)` para impedir el uso de información perteneciente al periodo objetivo.

## 3.7 Desarrollo del modelamiento predictivo

El prototipo contempla modelos separados para valor unitario FOB y volumen. El procedimiento incluye modelos base, XGBoost y LightGBM, división temporal de entrenamiento, validación y prueba, búsqueda de hiperparámetros, serialización y generación de predicciones fuera de muestra.

Los residuos se calculan comparando el valor observado con el esperado. Estos residuos alimentan posteriormente el módulo de detección de anomalías.

**Figura 3.9. Proceso de entrenamiento de los modelos predictivos.**

La figura presenta el flujo desde el dataset gold y la ingeniería de características hasta la comparación de modelos, selección, predicción fuera de muestra y cálculo de residuos.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_9_entrenamiento_modelos.mmd`.

## 3.8 Detección de anomalías

El módulo utiliza residuos predictivos y variables contextuales como entrada. Isolation Forest, Local Outlier Factor y ECOD generan puntuaciones individuales. Estas puntuaciones se transforman a una escala comparable y se combinan mediante pesos configurables. Cuando el score consolidado supera el umbral, el sistema genera una alerta y asigna una severidad.

Los pesos iniciales del prototipo son 0.45 para Isolation Forest, 0.30 para LOF y 0.25 para ECOD, con un umbral preliminar de 0.65. Estos valores deben calibrarse durante la evaluación experimental.

**Figura 3.10. Flujo del ensemble de detección de anomalías.**

La figura muestra cómo los residuos y variables son evaluados por tres detectores, normalizados, combinados y comparados con el umbral para producir una alerta.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_10_ensemble_anomalias.mmd`.

## 3.9 Explicabilidad mediante SHAP

TreeSHAP se utiliza para estimar la contribución de cada variable sobre las predicciones generadas por los modelos basados en árboles. El prototipo presenta variables que elevan o reducen el valor esperado y permite visualizar su magnitud.

Las explicaciones SHAP complementan la interpretación de la predicción, pero no representan causalidad ni explican directamente todo el score del ensemble. Por ello, la vista de detalle combina SHAP con residuos, valores observados, valores esperados y puntuaciones individuales.

## 3.10 Recuperación documental y reportes RAG

Los documentos se preparan, fragmentan, convierten en embeddings y almacenan en PostgreSQL con pgvector. Ante una alerta, el recuperador selecciona fragmentos relevantes por similitud. La evidencia documental se combina con valores de la operación, predicciones, puntuaciones y explicaciones SHAP.

El generador produce un reporte estructurado. Antes de persistirlo, el validador comprueba cifras y afirmaciones. Cuando el reporte no cumple los controles, se solicita corrección o se utiliza una plantilla determinista.

**Figura 3.11. Secuencia de recuperación de evidencia y generación del reporte.**

La figura presenta la interacción entre alerta, backend, base vectorial, recuperador RAG, generador narrativo, validador y persistencia.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_11_secuencia_rag.mmd`.

## 3.11 Trazabilidad del prototipo

Cada ejecución se identifica mediante un `run_id` y se relaciona con la versión y hash del dataset, hash del modelo y configuración utilizada. Cada alerta dispone de `alert_id`; los reportes y artefactos conservan identificadores y hashes propios.

La trazabilidad conecta dataset, configuración, modelo, alerta, explicación SHAP, evidencia RAG, reporte y decisión humana. ArtifactLineage conserva rutas, tipos y hashes para facilitar la reconstrucción.

**Figura 3.12. Cadena de trazabilidad de una alerta.**

La figura muestra cómo una ejecución se relaciona con el dataset, modelo y configuración, y cómo la alerta resultante se enlaza con explicación, evidencia, reporte y decisión.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_12_trazabilidad_alerta.mmd`.

## 3.12 Implementación de la interfaz web

### 3.12.1 Inicio de sesión

La pantalla de inicio de sesión valida credenciales, rol y condición experimental. Permite diferenciar usuarios Administrador y Auditor y asignar las condiciones INTEGRADO o AISLADO.

**Figura 3.13. Pantalla de inicio de sesión del prototipo funcional.**

La figura debe mostrar los campos de autenticación, la validación del usuario y el acceso según rol.

**Fuente:** elaboración propia a partir del prototipo, versión y fecha por completar.

### 3.12.2 Dashboard

El dashboard presenta indicadores agregados, alertas prioritarias y accesos a los módulos principales.

**Figura 3.14. Panel principal del prototipo funcional.**

La figura debe mostrar los indicadores generales, distribución de alertas y navegación disponible.

**Fuente:** elaboración propia a partir del prototipo, versión y fecha por completar.

### 3.12.3 Bandeja de alertas

La bandeja permite filtrar operaciones por producto, mercado, estado y severidad, y acceder al detalle analítico.

**Figura 3.15. Bandeja de alertas del prototipo funcional.**

La figura debe mostrar filtros, columnas, severidad, estado y acceso al detalle.

**Fuente:** elaboración propia a partir del prototipo, versión y fecha por completar.

### 3.12.4 Detalle de alerta

La vista de detalle integra datos de la operación, valores observados y esperados, score combinado, puntuaciones individuales, curva de probabilidad, explicaciones SHAP, evidencia RAG, reporte, formulario de decisión y logs.

**Figura 3.16. Vista de detalle de una alerta agroexportadora.**

La figura debe demostrar la integración de resultados analíticos, explicación, evidencia documental y decisión humana.

**Fuente:** elaboración propia a partir del prototipo, versión y fecha por completar.

### 3.12.5 Historial, telemetría e integridad

El historial permite consultar decisiones previas. La telemetría registra condición experimental, tiempo de decisión y comprensión. El módulo de integridad presenta identificadores, hashes y artefactos de trazabilidad.

**Figura 3.17. Historial de decisiones y telemetría experimental.**

**Figura 3.18. Módulo de integridad y trazabilidad del prototipo.**

**Fuente:** elaboración propia a partir del prototipo, versión y fecha por completar.

### 3.12.6 Datos, configuración y usuarios

La vista de datos permite explorar registros y administrar documentos normativos. La configuración modifica pesos y umbral del ensemble. La gestión de usuarios permite administrar roles y estados.

**Figura 3.19. Biblioteca documental y administración de datos RAG.**

**Figura 3.20. Configuración de pesos y umbral del ensemble.**

**Figura 3.21. Gestión de usuarios y roles.**

**Fuente:** elaboración propia a partir del prototipo, versión y fecha por completar.

## 3.13 Flujo funcional de revisión de una alerta

El proceso comienza con la autenticación del auditor. Después de seleccionar una alerta, el frontend solicita el detalle al backend. El backend recupera la operación, configuración, predicciones, puntuaciones, explicación SHAP, evidencia RAG y reporte. El auditor revisa la información y registra una decisión, justificación y valoración de comprensión. La decisión y el tiempo se almacenan y se incorporan al linaje.

**Figura 3.22. Secuencia funcional de revisión y decisión sobre una alerta.**

La figura representa el proceso completo desde la autenticación hasta el registro de la decisión y confirmación de trazabilidad.

**Fuente:** elaboración propia. Diagrama Mermaid: `docs/diagrams/figura_3_22_secuencia_revision_alerta.mmd`.

## 3.14 Seguridad y privacidad

El prototipo implementa roles, almacenamiento de contraseñas, variables de entorno, ejecución local y registros de actividad. La autorización granular, JWT, gestión centralizada de secretos, protección avanzada de endpoints y auditoría integral permanecen como componentes parciales.

Para un entorno productivo serían necesarios HTTPS, rotación de secretos, limitación de solicitudes, respaldo, recuperación, monitoreo, pruebas de penetración y gestión centralizada de identidades.

## 3.15 Pruebas funcionales del prototipo

Las pruebas funcionales comprueban inicio de sesión, filtrado de alertas, consulta de detalle, visualización SHAP, recuperación RAG, generación de reportes, registro de decisiones, consulta de historial, modificación de configuración, revisión de integridad y gestión de usuarios.

Para considerar un módulo funcional debe existir una ruta ejecutable, una entrada conocida, una salida verificable, persistencia o registro y evidencia visual. Las pruebas funcionales demuestran integración, pero no sustituyen la evaluación científica ni permiten aceptar las hipótesis sin métricas experimentales definitivas.
