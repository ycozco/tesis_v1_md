# Verificación funcional, diseño, IA y trazabilidad

1 de noviembre de 2026. Propuesta vigente: análisis comparativo y pronóstico semanal de exportaciones peruanas de palta, uva fresca y arándano. Esta entrega amplía la aplicación; no cierra la evaluación científica ni certifica todas las funciones históricas.

## Alcance comprobado e inventario

`ui-ia-auditoria-2026-11-01/inventario-funcional.json` registra **10 operaciones FastAPI**, **28 rutas históricas Flask**, **12 rutas SPA** y **7 vistas científicas**. El inventario Flask se obtiene por análisis de código, sin disparar importaciones, modificaciones de datos, modelos ni llamadas a proveedores antiguos. Registro de ruta no equivale a prueba de un flujo completo.

| Función | Resultado de esta revisión | Pendiente / prioridad |
|---|---|---|
| Login y sesión | Login real contra FastAPI/SQLite aislado; pruebas de contraseña incorrecta y JWT obligatorio | Revocación persistente de tokens al salir y evaluación del despliegue real |
| Cierre de sesión | Corregido envío de Authorization; borra sesión de cliente y registra salida | El JWT previo no se revoca en un almacén persistente: no afirmar revocación inmediata |
| Recuperación de sesión local | JSON de sesión inválido deja de romper la aplicación | Estrategia final de almacenamiento de tokens y expiración de UI |
| Series, comparación y fechas | Corte real, dos destinos, objetivos separados, faltantes explícitos; fuente comprobada con verificador independiente | Publicación de nuevos cortes y API de consulta histórica dinámica |
| Exportación | CSV completo del rango, sin redondeo de datos fuente, huecos vacíos y SHA256 de procedencia | Formato verificado con 53 semanas, 23 faltantes y un cero observado; no se acredita materialización final del CSV en Descargas |
| Pronóstico | MAE macro emparejado; test reservado e intervalos no evaluables visibles | Grilla, elegibilidad, historia de calibración y evaluación final |
| Señales | Se conserva carácter exploratorio y K común del piloto | Referencia estacional, persistencia e indeterminados H3 |
| Reportes H4 | Continúa explícitamente sin ejecutar las 180 salidas | Generación y evaluación emparejada a ciegas; no sustituida por borradores de UI |
| Proceso visual | Cinco etapas seleccionables, pendientes y evidencia por etapa | Orquestación de ETL/entrenamiento como trabajos con progreso real; no se simula su ejecución |
| Integridad en vivo | Backend compara **44 de 44 archivos**; resultado comprobado en navegador | Hashes no certifican verdad económica, cobertura ni fecha de publicación |
| Plantilla de borrador | Generación real, verificación atómica, archivo y evento; descarga por SHA256 comprobada en navegador y en disco | Revisión factual humana del texto, incluso cuando las cifras coinciden |
| Ollama | Adaptador implementado y probado con transporte simulado | Servicio no disponible en este equipo; falta modelo local instalado y una prueba real de inferencia |
| DeepSeek | Adaptador implementado, JSON y modelo configurables; simulación sin gasto | Clave específica, habilitación del servidor, cuenta ADMIN y aceptación del envío; no se ejecutó llamada de pago |
| Auditoría de borradores | ID, actor, hora UTC, proveedor/modelo, prompt, hashes de fuente/evidencia/informe, tokens cuando son devueltos y errores sanitizados | Persistencia transaccional, retención y controles de producción; el journal local no es un registro firmado e inmutable |
| Dashboard API heredado | Se activó autenticación y se sustituyeron tendencias aleatorias por recuentos reales de 14 días | No representa la evaluación actual de tesis; solo corrección del endpoint de compatibilidad |
| Rutas heredadas | Mantienen advertencia y carga diferida; 28 rutas Flask inventariadas | Migrar o retirar alertas/decisiones, historial, configuración, usuarios, integridad e inventario; revisar permisos y métricas ficticias restantes |
| PostgreSQL/pgvector y RAG | No se declara integración concluida; el nuevo generador usa hechos estructurados | Conexión real, recuperación densa, corpus versionado y reconstrucción end-to-end |
| Datos pendientes | Se mantienen separados los 8.579 registros históricos candidatos y sus 8.321 claves nuevas | Conciliación completa, nueva cobertura y versión del panel antes del test |

No se activó el RAG fiscal heredado, que incluye inferencias normativas y de fraude ajenas al alcance actual. El generador nuevo no envía nombres de exportadores, RUC, DAM ni originales; recibe tres hechos agregados de un caso conocido.

## Diseño, habilidades consultadas y animaciones

Se consultó el catálogo oficial con **skill-installer**: Playwright, Playwright Interactive, Figma y Security Best Practices figuran como opciones relacionadas. Se revisaron sus límites de uso. No se instaló un conjunto de habilidades indiscriminado: las de Figma producen artefactos Figma, mientras el entregable actual es una aplicación React existente. Las de visualización en conversación tampoco sustituyen la implementación del proceso dentro de la aplicación. La comprobación del navegador utiliza la capacidad ya disponible.

Se aplicó el DESIGN.md obligatorio del proyecto: paneles glass, paleta forestal, tipografía y tamaños coherentes. El proceso añade tarjetas seleccionables y detalles con evidencia; las animaciones duran 140–180 ms y comunican interacción, no ejecución del pipeline. `prefers-reduced-motion` desactiva movimiento CSS y el hook correspondiente desactiva también animaciones JavaScript de Recharts. Se añadió foco visible, salto al contenido, estados de carga/error, etiquetas y selección accesible.

Se comprobó el proceso en escritorio y a 390×844: documento de 384 px, sin desbordamiento horizontal global. No se cambió la preferencia de movimiento del sistema ni se certificó una auditoría WCAG completa con lector de pantalla. Las capturas están en `ui-ia-auditoria-2026-11-01`.

Las pantallas históricas ahora se cargan bajo demanda. El bundle principal bajó de aproximadamente 776 kB a **592,50 kB** minificado; permanece la advertencia de Vite por superar 500 kB. Falta separar la biblioteca de gráficos o diferir más vistas según medición real.

## IA: qué se implementó y qué se probó

El router `/api/research` requiere un JWT y usuario existente. Ofrece integridad, proveedores, casos, generación de borradores y descarga del original. La generación de pago exige ADMIN. El navegador no decide URLs, modelos arbitrarios ni claves. El servidor permite solamente Ollama por loopback y el endpoint oficial de DeepSeek, con redirecciones HTTP desactivadas.

Ollama usa compatibilidad de chat en `http://127.0.0.1:11434/v1/chat/completions`. Solo se admite el modelo configurado entre modelos locales enumerados; se filtran referencias cloud. No se descargan modelos ni se instaló un daemon durante esta entrega. Referencia: [documentación oficial de Ollama](https://docs.ollama.com/api/openai-compatibility).

DeepSeek usa `https://api.deepseek.com/chat/completions`, con `deepseek-flash` como valor inicial según la documentación comprobada. Para este borrador se pide JSON, modo sin thinking, temperatura cero y máximo 800 tokens. Un alias no garantiza inmovilidad de la versión subyacente: se registra el modelo que devuelve el proveedor. No se estimó una tarifa ni se consumió saldo. Referencias: [inicio oficial](https://api-docs.deepseek.com/quick_start) y [Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/).

Cada borrador contiene hechos identificados, fuente y unidad. La comprobación fija dos decimales y tolerancia absoluta 0,005; el modelo no puede ampliar esa tolerancia. Se rechazan como verificados los hechos faltantes, duplicados, desconocidos, unidades incorrectas o cifras fuera del margen. El texto libre sigue requiriendo juicio humano: **no es validación semántica completa ni RAG documental**. No hay fallback silencioso hacia otro proveedor ni plantilla si falla una llamada IA.

El archivo original se conserva en `data/research_reports`, junto con `events.jsonl`, fuera de Git y de los paquetes públicos. La descarga autenticada verifica propietario o ADMIN y compara el archivo con el hash registrado. El cliente verifica el mismo hash antes de guardarlo. Los hashes de archivos locales no equivalen a firma digital ni protegen frente a un administrador que modifique simultáneamente archivo y journal.

Los borradores de UI son ad hoc y llevan `h4_experiment_output=false`. No incrementan ni sustituyen la evaluación científica de 30 casos × 2 configuraciones × 3 repeticiones.

## Configuración para uso real

`backend/research-ai.env.example` y `.env.example` contienen nombres y valores vacíos de referencia, nunca credenciales. Con FastAPI arrancado desde la raíz, se pueden definir variables en el entorno o en el `.env` privado y reiniciar:

- Local: `RESEARCH_ALLOW_LOCAL_AI=true` y `RESEARCH_OLLAMA_MODEL` igual al nombre exacto de un modelo local ya instalado. Ollama debe estar escuchando en 11434.
- DeepSeek: `RESEARCH_ALLOW_PAID_AI=true`, `RESEARCH_DEEPSEEK_API_KEY` privada y `RESEARCH_DEEPSEEK_MODEL`. El usuario ADMIN elige el caso y acepta el envío agregado antes de cada solicitud.
- No reutilizar automáticamente `OPENAI_API_KEY` para otro proveedor. No poner claves en `VITE_*`, almacenamiento del navegador, documentos o chat.
- Definir una SECRET_KEY privada persistente para un despliegue. Si falta o está vacía, FastAPI genera una clave temporal segura y las sesiones dejan de validar tras reiniciar el proceso.

Para la revisión se utiliza `tools/serve_research_preview.py`: FastAPI real en 127.0.0.1:5002 y SQLite aislado en data/research_preview, con una cuenta exclusiva de QA. Ese script fuerza deshabilitada toda IA externa/local: no es el comando de despliegue real. Vite se arranca con `AGRO_API_TARGET=http://127.0.0.1:5002`; el valor predeterminado sigue apuntando al backend existente en 5001. Esta configuración se documenta para no confundir el preview con PostgreSQL de producción.

## Pruebas y límites de la comprobación

**20 pruebas Python pasaron:** 11 de integración API, JWT, SQLite y proveedores simulados; nueve del protocolo y validador. Casos: autenticación, validación de peticiones, integridad de fuentes, generación sin IA, descarga por hash, deshabilitación y rol de pago, consentimiento, Ollama/DeepSeek simulados, números/unidades/duplicados, timeout sin exponer claves, manipulación del archivo y tendencias reales del dashboard.

Pasaron también el verificador independiente del corte UI (14.683 celdas, 3.268 observadas, 11.415 desconocidas y 12 comparaciones emparejadas), el comprobador del formateador CSV y la compilación de producción. Se mantienen avisos de deprecación de Starlette/httpx, SQLAlchemy y fechas UTC heredadas. No se afirma una instalación limpia de dependencias ni que la configuración histórica de lint esté resuelta.

En navegador se ejecutó login real con la cuenta QA, integridad 44/44, selección de etapa, generación de plantilla, visualización del resultado y descarga original. El JSON descargado se comprobó además en disco y su SHA256 coincide. La descarga CSV se solicitó, pero no se materializó en el directorio inspeccionado; el contenido del formateador sí quedó validado independientemente. No se efectuó inferencia real local, llamada real DeepSeek, fact-checking humano, carga de PostgreSQL ni ejecución destructiva de las 28 rutas Flask antiguas.

Movimiento reducido: [técnica oficial W3C C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39). Esto sustenta la implementación del control de movimiento, no una certificación integral de accesibilidad.

## Incidencia de credenciales encontrada

El `.env` raíz estaba rastreado por Git y tenía un campo de clave no vacío. Se retiró del seguimiento **sin borrar la copia local**, se añadieron exclusiones y ejemplos vacíos. La credencial no se utilizó ni se reprodujo en la documentación. El historial anterior conserva el archivo: **la rotación de la credencial en su proveedor queda pendiente del titular**. No se reescribió historia remota ni se cambiaron credenciales de una cuenta externa.

## Próximas decisiones

Primero: rotar la credencial antigua y cerrar la versión de datos antes de abrir el test. Después: habilitar un modelo local o una cuenta DeepSeek con una prueba acotada autorizada, completar recuperación documental y PostgreSQL, y ejecutar H4 con evaluación humana. Migrar/retirar los flujos heredados con pruebas de permisos y procedencia; no habilitarlos como resultados científicos por el solo hecho de que exista una pantalla.
