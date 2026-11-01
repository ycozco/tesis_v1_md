# Orientación de la UI a la propuesta actual

1 de noviembre de 2026. Referencia: documento nativo «TESIS - COZCO MAURI YOSET», modificado el 23 de octubre de 2026 a las 13:27:20 UTC; metadatos comprobados otra vez antes de los cambios. Alcance actual: sistema de información y pronóstico para el análisis comparativo de las exportaciones peruanas de palta, uva fresca y arándano. Unidad producto–destino–semana ISO, evaluación técnica H1–H4.

## Hallazgos y cambios aplicados

| Antes | Cambio actual | Motivo |
|---|---|---|
| Terminal del auditor, supervisión fiscal y vigilancia en tiempo real | Series, comparación y pronóstico; estado retrospectivo visible | El estudio no acredita fiscalización ni una operación en vivo |
| F1 fijo 0,92, simulaciones verificadas y variaciones porcentuales decorativas | Métricas MAE emparejadas cargadas de artefactos del piloto; sin F1 ni éxitos inventados | No hay etiquetas reales ni evaluación H4 concluida |
| Notificaciones estáticas de mango y retrasos logísticos | Navegación centrada en los tres productos; sin notificaciones ficticias | Mantener alcance y procedencia |
| Conteo de alertas presentado como operaciones analizadas | Registros aduaneros, combinaciones y celdas observadas/desconocidas diferenciados | No confundir unidades de análisis |
| Precio declarado frente a esperado como eje único | Series de FOB unitario y volumen con filtros comunes y comparación entre dos destinos | Corresponder a los dos objetivos y unidad semanal |
| Estado de sistema o cifrado no comprobado | Corte documentado, cobertura parcial y evaluación técnica | Evitar garantías sin evidencia |
| Validación factual y RAG presentadas como ya verificadas | 30 casos preparados, 180 ejecuciones planificadas, cero reportes generados | Separar preparación de resultados |

Se respetaron los tokens y paneles glass de DESIGN.md. El encabezado, navegación y login actuales usan el nuevo alcance. `ResearchLayout.jsx` y `ResearchDashboard.jsx` sustituyen las importaciones de la entrada activa sin borrar las pantallas históricas.

## Flujo principal disponible

1. **Series y comparación:** producto, destino, segundo destino opcional, variable y fechas. Gráfico y tabla final de 12 semanas; faltantes como «Sin dato», líneas interrumpidas. Se generan todos los lunes del rango, sin completar valores. Se mantienen los códigos de destino de la fuente; códigos especiales no se convierten a países inventados.
2. **Pronóstico:** dos objetivos, MAE macro sobre los mismos casos por modelo/referencia y tamaño del emparejamiento. Se muestra la falta de calibración de intervalos y la reserva del test. No se generan pronósticos futuros ficticios.
3. **Señales exploratorias:** selecciones del ensemble de rangos del piloto filtradas por serie, objetivo y fechas; tamaño de población y K explícitos. Ausencia de selecciones no equivale a ausencia de anomalía. No hay confirmación de fraude.
4. **Reportes y evidencia:** estado real de H4 y criterios de enlace de hechos/fuentes/unidades/tolerancia. Generación y evaluación siguen pendientes.
5. **Fuentes y cobertura:** panel conservador, covariables recuperadas y nuevos históricos todavía candidatos, enlaces institucionales y descarga del corte con hashes.

## Contrato de datos y límites

`tools/export_research_ui.py` genera `frontend/public/research/snapshot.json`, con esquema versionado y hashes de los artefactos fuente. Incluye únicamente series agregadas, métricas de desarrollo y señales exploratorias del piloto. No copia identificadores personales ni variables del dotenv. Los 8.579 registros históricos nuevos figuran como recuperación pendiente; no entran en gráficos ni métricas.

Es una **consulta de corte local**, sin promesa de sincronización automática con Google Drive, base de datos ni APIs de modelos. Si el archivo no carga, aparece un error con reintento y no se muestran cifras de reemplazo. La regeneración del JSON es explícita; los datos no se actualizan por el simple hecho de cambiar el panel científico.

Las rutas antiguas de alertas, decisiones, historial, configuración, integridad, usuarios, telemetría e inventario siguen disponibles por compatibilidad, con una advertencia visible y sin enlaces desde la navegación científica principal. **No se migraron sus acciones ni se certificaron sus métricas**. Los archivos antiguos Dashboard.jsx y Layout.jsx se conservan como prototipo, pero la entrada activa ya no los importa. La autenticación real y los permisos del backend no se modificaron.

## Comprobaciones

- Compilación de producción Vite completada. Advertencia existente de bundle mayor a 500 kB; falta separar cargas de módulos históricos y revisar rendimiento con datos de mayor tamaño.
- Revisión visual en vista estrecha y escritorio de 1360×900; ancho del documento 1354, sin desbordamiento horizontal global en escritorio. Las tablas disponen de scroll propio.
- Navegación verificada entre series, pronóstico, reportes y fuentes; cambio de producto y objetivo, interpretación de faltantes y aviso de prueba reservada. Señales y manejo de rangos se comprobaron en la misma revisión.
- Se usó un servidor **aislado de prueba de login**, solo loopback, sin conectar la base de producción ni usar credenciales reales. La sesión identifica «Revisión local de UI». Esto verifica frontend, no autenticación/roles de producción.
- Consola del navegador sin errores en las pantallas examinadas. Capturas en `ui-revision-2026-11-01`.

## Trabajo que continúa pendiente

Conciliar y versionar la expansión histórica antes de regenerar el panel; cerrar disponibilidad de covariables, calendario y evaluación final; conectar lectura de cortes versionados a un backend real; sustituir o retirar las rutas heredadas cuando exista contrato equivalente; completar H3/H4 y PostgreSQL/pgvector. Los controles de generación y administración no se presentan como funciones terminadas.

La búsqueda y su evidencia quedan en `datasets/busqueda/2026-11-01/README.md`. Esta orientación es una primera adaptación funcional de la navegación y las consultas científicas, no el cierre de toda la aplicación.
