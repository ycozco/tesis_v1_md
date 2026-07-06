# Inventario de figuras, capturas y diagramas de la tesis

Este documento centraliza las imágenes requeridas por la tesis, su tipo, nombre, ubicación dentro del documento y ruta propuesta dentro del repositorio. Debe utilizarse como lista de control para producir, insertar y versionar cada recurso visual.

## Convención de archivos

- Los diagramas editables se guardan en formato Mermaid (`.mmd`).
- Cada diagrama Mermaid debe exportarse también a SVG y PNG.
- Las capturas de pantalla se guardan en PNG.
- Los gráficos generados mediante scripts se guardan en PNG y, cuando sea posible, también en SVG.
- Los nombres de archivo deben mantenerse en minúsculas, sin tildes y separados por guiones.
- Las capturas finales deben registrar en su pie de figura la versión o commit, fecha y dataset utilizado.

## Estructura propuesta

```text
docs/figures/
├── capitulo3/
│   ├── mermaid/
│   ├── graficos/
│   └── capturas/
└── capitulo4/
    ├── mermaid/
    ├── graficos/
    └── capturas/
```

# Capítulo III: Desarrollo e implementación del prototipo funcional

## A. Diagramas Mermaid y diagramas técnicos

| Figura | Nombre oficial | Sección de la tesis | Tipo | Archivo fuente propuesto | Archivo exportado propuesto | Estado |
|---|---|---|---|---|---|---|
| 3.1 | Flujo de auditoría inicial de datos y componentes del prototipo | 3.2.1 Objetivo y procedimiento | Diagrama de flujo Mermaid | `docs/figures/capitulo3/mermaid/figura-3-01-flujo-auditoria.mmd` | `docs/figures/capitulo3/mermaid/figura-3-01-flujo-auditoria.svg` | Pendiente |
| 3.3 | Casos de uso principales del prototipo funcional | 3.3 Requisitos del prototipo funcional | Diagrama de casos de uso | `docs/figures/capitulo3/mermaid/figura-3-03-casos-uso.mmd` | `docs/figures/capitulo3/mermaid/figura-3-03-casos-uso.svg` | Pendiente |
| 3.4 | Arquitectura lógica del prototipo funcional de supervisión agroexportadora | 3.4.2 Arquitectura lógica | Diagrama de arquitectura Mermaid | `docs/figures/capitulo3/mermaid/figura-3-04-arquitectura-logica.mmd` | `docs/figures/capitulo3/mermaid/figura-3-04-arquitectura-logica.svg` | Pendiente |
| 3.5 | Arquitectura de despliegue del prototipo en entorno local | 3.4.3 Arquitectura de despliegue | Diagrama de despliegue Mermaid | `docs/figures/capitulo3/mermaid/figura-3-05-arquitectura-despliegue.mmd` | `docs/figures/capitulo3/mermaid/figura-3-05-arquitectura-despliegue.svg` | Pendiente |
| 3.6 | Arquitectura de datos por capas | 3.4.4 Arquitectura de datos | Diagrama de flujo de datos Mermaid | `docs/figures/capitulo3/mermaid/figura-3-06-arquitectura-datos.mmd` | `docs/figures/capitulo3/mermaid/figura-3-06-arquitectura-datos.svg` | Pendiente |
| 3.7 | Arquitectura de componentes de la aplicación web | 3.4.5 Arquitectura de componentes web | Diagrama de componentes Mermaid | `docs/figures/capitulo3/mermaid/figura-3-07-componentes-web.mmd` | `docs/figures/capitulo3/mermaid/figura-3-07-componentes-web.svg` | Pendiente |
| 3.8 | Modelo de datos del prototipo funcional | 3.5 Modelo de datos y persistencia | Diagrama entidad-relación Mermaid | `docs/figures/capitulo3/mermaid/figura-3-08-modelo-datos.mmd` | `docs/figures/capitulo3/mermaid/figura-3-08-modelo-datos.svg` | Pendiente |
| 3.9 | Proceso de entrenamiento de los modelos predictivos | 3.7 Desarrollo del modelamiento predictivo | Diagrama de pipeline Mermaid | `docs/figures/capitulo3/mermaid/figura-3-09-entrenamiento-modelos.mmd` | `docs/figures/capitulo3/mermaid/figura-3-09-entrenamiento-modelos.svg` | Pendiente |
| 3.10 | Flujo del ensemble de detección de anomalías | 3.8 Detección multivariable de anomalías | Diagrama de pipeline Mermaid | `docs/figures/capitulo3/mermaid/figura-3-10-ensemble-anomalias.mmd` | `docs/figures/capitulo3/mermaid/figura-3-10-ensemble-anomalias.svg` | Pendiente |
| 3.11 | Flujo de generación y presentación de explicaciones SHAP | 3.9 Explicabilidad mediante SHAP | Diagrama de flujo Mermaid | `docs/figures/capitulo3/mermaid/figura-3-11-flujo-shap.mmd` | `docs/figures/capitulo3/mermaid/figura-3-11-flujo-shap.svg` | Pendiente |
| 3.12 | Secuencia de recuperación de evidencia y generación controlada del reporte | 3.10 Recuperación documental y generación de reportes RAG | Diagrama de flujo Mermaid | `docs/figures/capitulo3/mermaid/figura-3-12-flujo-rag.mmd` | `docs/figures/capitulo3/mermaid/figura-3-12-flujo-rag.svg` | Pendiente |
| 3.13 | Cadena de trazabilidad de una alerta | 3.11 Trazabilidad del prototipo | Diagrama de linaje Mermaid | `docs/figures/capitulo3/mermaid/figura-3-13-cadena-trazabilidad.mmd` | `docs/figures/capitulo3/mermaid/figura-3-13-cadena-trazabilidad.svg` | Pendiente |
| 3.23 | Secuencia funcional de revisión y decisión sobre una alerta | 3.13 Flujo funcional de revisión de una alerta | Diagrama de secuencia Mermaid | `docs/figures/capitulo3/mermaid/figura-3-23-secuencia-revision-alerta.mmd` | `docs/figures/capitulo3/mermaid/figura-3-23-secuencia-revision-alerta.svg` | Pendiente |

## B. Gráficos generados a partir de datos

| Figura | Nombre oficial | Sección de la tesis | Tipo | Script o fuente propuesta | Archivo propuesto | Estado |
|---|---|---|---|---|---|---|
| 3.2 | Evolución de registros durante la preparación inicial | 3.2.2 Resultados de la auditoría de datos | Gráfico de barras o embudo | `scripts/figures/generar_figura_3_02.py` | `docs/figures/capitulo3/graficos/figura-3-02-evolucion-registros.png` | Pendiente |

### Datos que debe mostrar la Figura 3.2

- Registros iniciales: 40 672.
- Exclusión de cacao: 379.
- Registros evaluados: 40 293.
- Registros válidos: 40 289.
- Registros rechazados: 4.
- Debe aclararse que el espárrago se excluye del conjunto experimental principal.

## C. Capturas de pantalla del prototipo

| Figura | Nombre oficial | Sección de la tesis | Pantalla o módulo | Archivo propuesto | Evidencia mínima requerida | Estado |
|---|---|---|---|---|---|---|
| 3.14 | Pantalla de inicio de sesión del prototipo funcional | 3.12.1 Inicio de sesión | Login | `docs/figures/capitulo3/capturas/figura-3-14-inicio-sesion.png` | Campos de autenticación, rol y condición experimental | Pendiente |
| 3.15 | Panel principal del prototipo funcional | 3.12.2 Dashboard | Dashboard | `docs/figures/capitulo3/capturas/figura-3-15-dashboard.png` | Indicadores, severidades, alertas prioritarias y navegación | Pendiente |
| 3.16 | Bandeja de alertas del prototipo funcional | 3.12.3 Bandeja de alertas | Alertas | `docs/figures/capitulo3/capturas/figura-3-16-bandeja-alertas.png` | Filtros, columnas, estado, severidad y acceso a detalle | Pendiente |
| 3.17 | Vista de detalle de una alerta agroexportadora | 3.12.4 Detalle de alerta | Detalle analítico | `docs/figures/capitulo3/capturas/figura-3-17-detalle-alerta.png` | Predicción, residuos, scores, SHAP, RAG, reporte y decisión | Pendiente |
| 3.18 | Historial de decisiones y telemetría experimental | 3.12.5 Historial, telemetría e integridad | Historial y telemetría | `docs/figures/capitulo3/capturas/figura-3-18-historial-telemetria.png` | Decisiones, condición experimental, tiempo y comprensión | Pendiente |
| 3.19 | Módulo de integridad y trazabilidad del prototipo | 3.12.5 Historial, telemetría e integridad | Integridad | `docs/figures/capitulo3/capturas/figura-3-19-integridad-trazabilidad.png` | `run_id`, `alert_id`, hashes, versiones y artefactos | Pendiente |
| 3.20 | Biblioteca documental y administración de datos RAG | 3.12.6 Datos, configuración y usuarios | Datos / documentos RAG | `docs/figures/capitulo3/capturas/figura-3-20-biblioteca-rag.png` | Listado documental, metadatos, indexación y estado | Pendiente |
| 3.21 | Configuración de pesos y umbral del ensemble | 3.12.6 Datos, configuración y usuarios | Configuración | `docs/figures/capitulo3/capturas/figura-3-21-configuracion-ensemble.png` | Pesos IF/LOF/ECOD, umbral y validación de suma | Pendiente |
| 3.22 | Gestión de usuarios y roles | 3.12.6 Datos, configuración y usuarios | Usuarios | `docs/figures/capitulo3/capturas/figura-3-22-usuarios-roles.png` | Usuarios, roles, estado y acciones administrativas | Pendiente |

## Requisitos para las capturas

Cada captura incorporada a la tesis debe cumplir lo siguiente:

1. Utilizar el prototipo en una versión identificable mediante commit o etiqueta.
2. Registrar la fecha de captura.
3. Indicar si los datos mostrados son reales, preliminares o datos semilla.
4. Ocultar o anonimizar credenciales, RUC, nombres comerciales y claves.
5. Mantener una resolución legible en el documento final.
6. Evitar capturas parciales sin contexto o con datos que contradigan el texto de la tesis.
7. Conservar el archivo original sin compresión destructiva.

# Capítulo IV: Resultados y discusión

## Diagramas identificados

| Figura | Nombre | Ubicación actual | Tipo | Archivo fuente propuesto | Archivo exportado propuesto | Observación |
|---|---|---|---|---|---|---|
| 4.7 | Secuencia funcional de revisión de una alerta | Bloque de resultados funcionales, después de la explicación del flujo Auditor → Frontend → API → PostgreSQL/pgvector → modelos/RAG → decisión | Diagrama de secuencia Mermaid | `docs/figures/capitulo4/mermaid/figura-4-07-secuencia-funcional.mmd` | `docs/figures/capitulo4/mermaid/figura-4-07-secuencia-funcional.svg` | Revisar si duplica la Figura 3.23. Si muestra el mismo flujo, reutilizar la figura del Capítulo III o convertirla en evidencia de resultado con datos reales. |

## Figuras que deberá producir el Capítulo IV cuando se cierre la evaluación

Estas figuras aún no tienen numeración definitiva. Deben numerarse después de consolidar los resultados y evitar asignar números antes de cerrar el capítulo.

| Nombre provisional | Tipo | Ruta propuesta | Fuente de datos |
|---|---|---|---|
| Comparación de modelos para valor unitario FOB | Gráfico de barras o tabla gráfica | `docs/figures/capitulo4/graficos/comparacion-modelos-fob.png` | Métricas de modelos base, XGBoost y LightGBM |
| Comparación de modelos para volumen exportado | Gráfico de barras o tabla gráfica | `docs/figures/capitulo4/graficos/comparacion-modelos-volumen.png` | RMSLE, MAE, RMSE, SMAPE y R² |
| Desempeño de detectores individuales y ensemble | Gráfico comparativo | `docs/figures/capitulo4/graficos/comparacion-detectores-anomalias.png` | Precision, Recall, F1, PR-AUC y Precision@k |
| Matriz o distribución de anomalías controladas | Heatmap o barras | `docs/figures/capitulo4/graficos/anomalias-controladas.png` | Resultados por tipo y magnitud de anomalía |
| Importancia global SHAP | Beeswarm o barras | `docs/figures/capitulo4/graficos/shap-global.png` | Valores SHAP del modelo final |
| Ejemplo de explicación local SHAP | Waterfall | `docs/figures/capitulo4/graficos/shap-local-alerta.png` | Alerta seleccionada y modelo versionado |
| Validación factual de reportes | Barras o matriz de cumplimiento | `docs/figures/capitulo4/graficos/validacion-reportes.png` | Exactitud numérica, completitud y fidelidad factual |
| Comparación AISLADO vs. INTEGRADO | Barras o boxplot | `docs/figures/capitulo4/graficos/comparacion-condiciones.png` | Tiempo de análisis, comprensión y respuestas correctas |
| Reconstrucción trazable de una alerta | Diagrama de evidencia | `docs/figures/capitulo4/mermaid/reconstruccion-alerta-final.mmd` | Artefactos reales, hashes y versiones finales |

# Control de consistencia

Antes de insertar una figura en Google Docs se debe comprobar:

- [ ] La figura está mencionada antes o después de su inserción.
- [ ] El número coincide con el texto y el índice de figuras.
- [ ] El título coincide con este inventario.
- [ ] El archivo existe en la ruta indicada.
- [ ] La fuente editable existe cuando se trata de Mermaid.
- [ ] La imagen exportada es legible en tamaño de página.
- [ ] La fuente de elaboración está indicada.
- [ ] La captura contiene fecha, versión o commit y naturaleza de los datos.
- [ ] No existen datos personales ni secretos visibles.
- [ ] La figura no duplica otra figura sin una justificación metodológica.

# Prioridad de producción

1. Figura 3.4: arquitectura lógica.
2. Figura 3.5: arquitectura de despliegue.
3. Figura 3.6: arquitectura de datos.
4. Figura 3.8: modelo de datos.
5. Figura 3.9: pipeline predictivo.
6. Figura 3.10: ensemble de anomalías.
7. Figura 3.11: SHAP.
8. Figura 3.12: RAG.
9. Figura 3.13: trazabilidad.
10. Figura 3.23: secuencia funcional.
11. Figuras 3.14 a 3.22: capturas finales del prototipo.
12. Figura 3.2: gráfico de evolución de registros.
13. Figura 3.1 y Figura 3.3: auditoría y casos de uso.

# Regla de actualización

Cada vez que se agregue, elimine o renumere una figura en la tesis, este inventario debe actualizarse en el mismo commit que modifica el capítulo correspondiente.
