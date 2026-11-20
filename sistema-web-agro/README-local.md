# AgroScope Perú: despliegue local

Desde `sistema-web-agro`:

```powershell
docker compose up -d --build --wait
docker compose ps
docker compose logs --tail 50 backend
```

Abrir http://localhost:8050. Cuenta de revisión local: `revision-ui`, contraseña
`SoloRevisionLocal2026!`. Al migrar desde Vite, cerrar la sesión anterior y entrar
de nuevo; sus tokens fueron emitidos por otro backend.

La imagen Python instala las versiones verificadas de `backend/requirements-local.lock`;
el frontend utiliza `npm ci` y `package-lock.json`.

Nginx sirve el frontend compilado y envía `/api/` a FastAPI. PostgreSQL/pgvector
queda en la red interna. Los volúmenes `postgres_data` y `research_state` conservan
cuentas, registros, reportes y la clave de sesión entre reinicios. La extensión
vector se crea al arrancar; esto no acredita evaluación de recuperación semántica.
Las llamadas a proveedores de IA permanecen deshabilitadas por defecto.

El Compose de la raíz corresponde al visor de tesis y es independiente. Este
Compose reemplaza la combinación anterior de Flask y FastAPI para el prototipo.

Opcional: crear un `.env` local (ignorado por Git) con `AGRO_WEB_PORT`,
`AGRO_LOCAL_USERNAME`, `AGRO_LOCAL_PASSWORD` y `AGRO_DB_PASSWORD`. Cambiar la
contraseña de PostgreSQL con un volumen existente requiere actualizar también el
usuario en la base; la variable de inicialización no cambia usuarios existentes.

Para detener sin perder datos: `docker compose stop`. Para reconstruir cambios:
`docker compose up -d --build --wait`. No usar `down -v` salvo que se desee eliminar
los datos locales. No es necesario instalar Python o Node en Windows.

Los gráficos utilizan el corte documentado de `public/research/snapshot.json`.
La consulta de fuentes externas informa su disponibilidad y contexto; no cambia
automáticamente el conjunto de investigación ni los resultados de la tesis.

## Verificación realizada

Tres servicios saludables; acceso mediante Nginx; integridad de 44 archivos y siete
artefactos de avance; 30 casos disponibles; sesión válida después de reiniciar el
backend; 18 pruebas de API y fuentes aprobadas. Vista de escritorio y menú móvil
verificados en navegador. `pip check` no encuentra dependencias incompatibles.

Las fuentes se consultan cada 15 minutos mientras el panel está abierto, con caché
del servidor por 15 minutos. SUNAT, SISAP y NASA muestran accesibilidad del enlace;
BCRP también devuelve la última observación numérica de PN01207PM. El periodo de
la observación y la hora de consulta se presentan por separado.

Pendientes técnicos: la instalación del frontend reportó diez avisos de seguridad
en su árbol npm y el build advierte un bundle de más de 500 kB. La migración de
versiones mayores y la optimización del bundle requieren trabajo adicional.

## Upgrade visual del 20 de noviembre de 2026

Dirección: observatorio agroexportador sobrio, superficies neutras, verde institucional y color concentrado en los datos. Se unificaron los tokens claros de Tailwind y las superficies ui-card/ui-panel/ui-input, retirando la capa oscura de investigación y efectos de cristal. La navegación usa Lucide; el acceso comparte el botón reutilizable. Panorama incorpora pestañas Radix con el patrón de composición de shadcn/ui y Recharts incorpora accessibilityLayer. Las bibliotecas de gráficos y primitivas se separan en chunks de producción.

La metodología de revisión procede de [Unslop por Damir Sokolovsky](https://github.com/heydamir/unslop), CC BY 4.0. Se conserva la skill y su atribución en `design-tools/unslop`; esta copia local no se registra automáticamente como skill global de Codex. Los patrones de Button/Tabs están adaptados de shadcn/ui (MIT) a Tailwind 3, sin ejecutar su CLI sobre el proyecto existente.

Verificación: compilación de producción y cinco verificadores existentes de filtros temporales, precios, pronósticos, comparación e interpretación. Las ocho vistas abren y el recorrido no registra errores de consola. Navegación real en Panorama, Pronósticos y Explorar; acceso con la cuenta local; menú móvil a 390 px y ausencia de desbordamiento horizontal en Pronósticos. El rediseño no constituye validación científica ni una evaluación de usabilidad con participantes. Se comprobó la generación del reporte de selección y el cambio de pestaña mediante teclado. Queda pendiente una auditoría automatizada completa de accesibilidad, revisar los avisos npm y la migración mayor de Recharts. Las demás vistas reciben los estilos compartidos; su validación funcional se registra por separado.

Prueba local: `docker compose up -d --build --wait frontend backend db`. Abrir http://localhost:8050. No es un despliegue público ni una publicación en GitHub Pages. Para volver a compilar después de cambios, repetir ese comando; los volúmenes se conservan.

### Segunda revisión: composición del observatorio

Se reemplazó el shell por una columna fija de navegación con dos grupos, cuenta y estado del corte; cabecera de contexto y navegación móvil con fondo superpuesto. Panorama ahora presenta filtros compactos, indicadores y gráficos antes de los detalles. Los precios y la exploración completa de destinos se conservan abajo; las tablas semanales/mensuales quedan desplegables. Pronósticos mantiene los cuatro selectores principales visibles y agrupa calendario, destinos rápidos y alcance en Configurar. Fuentes utiliza un catálogo de dos columnas, Trazabilidad una secuencia conectada y Asistente un espacio de proveedores y lectura en dos columnas. Evidencia agrupa indicadores y pasos del protocolo.

Pruebas de esta revisión: build Docker, verificadores temporales/precios/pronósticos, recorrido de las ocho vistas sin errores de consola, cambio de producto con actualización de indicadores, apertura del calendario y menú móvil a 390 px sin desbordamiento horizontal. Capturas: `docs/upgrade-frontend-revision2-2026-11-20.jpg` y `docs/upgrade-frontend-revision2-mobile-2026-11-20.jpg`. El servicio continúa en http://localhost:8050.

### Mercado al día: tarjetas y franja continua

La franja superior repite precios mayoristas SISAP, dólar interbancario diario BCRP (PD04638PD) y clima de modelo Open-Meteo para Ica, Trujillo y Arequipa. No contiene controles de movimiento; respeta la preferencia del sistema de movimiento reducido. Las tarjetas del Panorama muestran la misma información con fecha, fuente y estado. El selector regional modifica únicamente la tarjeta de clima. Los detalles conservan todas las variedades recuperadas; no hay precio de arándano verificado.

El backend inicia un recolector al arrancar FastAPI, consulta cada 3600 segundos incluso con el navegador cerrado y conserva `market-context.json` en el volumen research_state. El frontend consulta ese estado cada 30 segundos mediante GET /api/research/market-context con autenticación. No se hacen llamadas a las fuentes desde cada navegador. Si una fuente falla, su último dato queda marcado como guardado; si nunca hubo respuesta, se informa no disponible. El corte científico y los pronósticos permanecen separados del contexto actual.

SISAP: consulta pública de lectura a resumenes/filtrar, mercado 15011502, productos 0626 y 0637, precio_prom y fecha de Lima. Se valida fecha, encabezado y continuidad de las variedades en filas con rowspan. El encabezado mezcla S/ por kg, litro o unidad: no se asume una unidad específica ni se convierten los precios. BCRP muestra venta y fecha del último dato publicado, no una cotización intradía. Open-Meteo presenta puntos regionales de modelo, no estaciones ni parcelas verificadas. No se presentan promociones comerciales ni descuentos inventados.

Validación del recolector: seis pruebas en backend/tests/test_market_context.py y consulta real de las tres fuentes. Para reproducir las pruebas sin red: establecer PYTHONPATH=sistema-web-agro/backend y ejecutar `python -m unittest discover -s sistema-web-agro/backend/tests -p test_market_context.py -v`. Despliegue: `docker compose up -d --build --wait frontend backend db`.

Comprobación del despliegue: health 200; market-context sin sesión 401; nueve observaciones persistidas; seis pruebas aprobadas dentro del contenedor. Navegador: cuatro tarjetas con datos, selector regional operativo, dos grupos de cinta de igual ancho y animación infinita sin controles, ausencia de errores de consola y ausencia de desbordamiento a 390 px. Evidencia visual: docs/mercado-al-dia-dashboard-2026-11-20.jpg y docs/mercado-al-dia-mobile-2026-11-20.jpg.

### Barra persistente, fichas de mercado e interpretación visual

La franja queda sticky en top:0 en todas las vistas y la cabecera de contexto queda debajo (40 px escritorio / 36 px móvil). Cada dato seleccionable de la cinta y cada tarjeta abre un dialog nativo con foco contenido, Escape, cierre, comparación, fechas de recuperación, descarga JSON y enlace directo a la fuente. Los controles de la franja seleccionan datos; no controlan el movimiento.

La interpretación compartida de Panorama, Pronósticos y entrenamiento incorpora cinco pestañas: Resumen, Clima, Dólar y precios, Tabla de datos y Fuentes y alcance. Resumen presenta indicadores y serie de precio/peso/FOB, o MAE por método cuando corresponde. Clima utiliza medias semanales de máximas/mínimas y lluvia disponible con sus días de cobertura. Dólar conserva los meses sin respaldo como desconocidos; precios locales se filtran por variedad y se tabulan sin comparaciones gráficas de unidades no validadas. Los párrafos descriptivos se conservan como tabla de hallazgos. La descarga incluye series y métricas representadas.

Verificación de esta revisión: compilación Docker y cinco verificadores de datos aprobados. Scroll en ocho vistas: cinta en y=0 y cabecera en y=40; en móvil cinta y=0 y cabecera y=36, sin desbordamiento horizontal a 390 px. Modal probado desde la cinta fija y tarjeta de Palta Fuerte: enlace oficial, tabla de variedades, bloqueo de scroll, cierre por Escape y restauración del foco. Interpretación: serie de volumen, gráficos climáticos, filtro de variedad, tabla semanal y MAE de pronósticos comprobados; sin errores de consola. Evidencia: docs/mercado-modal-detalle-2026-11-20.jpg y docs/interpretacion-visual-tabs-2026-11-20.jpg.

## Pendientes del despliegue local (auditoría del 20 de noviembre de 2026)

- **Calendario y E3.** El archivo de pronósticos v2 separa semana de origen, emisión simulada, semana objetivo y última observación usada. La API y la descarga JSON sirven el mismo archivo, y el CSV incluye los campos de calendario. La emisión simulada indica el límite entre las semanas de origen y objetivo. E3 comprueba en el registro temporal un horizonte de una semana, una antigüedad de tres y cero residuos del objetivo disponibles al emitir, además de detectar una alteración.
- **Entorno del entrenador.** El Dockerfile consume el lock de dependencias con StatsForecast 2.0.3, AutoGluon 1.6.3 y PyTorch CPU 2.13.0+cpu. El manifiesto conserva la revisión de origen si se indica al construir y las huellas del lock, la entrada y el corte de datos. El [procedimiento del entrenador](training/README.md) indica cómo obtener el ID de imagen.
- **Frontend.** React Router pasa a 7.18.6 y ESLint se ejecuta con `npm run lint`. El alcance del saneamiento corresponde a la auditoría de producción. Las alertas de herramientas de desarrollo y la migración de Recharts se revisan por separado.
- **Evidencia funcional pendiente.** E1–E3 cuentan con pruebas de componentes. Falta reproducir los tres escenarios controlados completos en navegador, con entradas, resultados, versiones, exportaciones y capturas enlazadas. Este trabajo no usa el bloque final.
- **H4 preparado para revisión.** El [registro de 30 revisiones](../planificacion/2026-11-02/ejecucion/h4-revision-humana-pendiente.json) identifica por SHA-256 cada clave. El ejecutor exige la revisión numérica, documental y de abstención, y comprueba los documentos devueltos contra el corpus congelado antes de llamar al generador. Las pruebas técnicas reproducen los 180 turnos con transporte simulado. Siguen pendientes la revisión humana, el congelamiento experimental, la validación del recuperador real, las 180 salidas reales y su evaluación ciega. H4 sigue sin evidencia experimental que la respalde.
- **H1–H3.** H1/H3 requieren elegibilidad y calendario congelado. H2 sigue cerrada como no evaluable para la colección auditada.
