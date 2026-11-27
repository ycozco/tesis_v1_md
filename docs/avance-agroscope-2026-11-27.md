# AgroScope — avance del 27 de noviembre de 2026

AgroScope permite consultar y comparar exportaciones de palta, uva fresca y arándano. El avance incluye un módulo de planificación del productor, fichas de mercados con fuentes verificables y una propuesta de evaluación para feria universitaria.

## Desarrollado y probado en la instalación local

| Área | Entrega |
| --- | --- |
| Inicio del productor | Con oferta registrada, el inicio prioriza cultivo, producción, acopio y borradores. En ausencia de una oferta, muestra referencias públicas de mercado y permite registrar un cultivo. |
| Oferta y borradores | Registro de producto, origen y capacidad semanal. Los borradores permiten ingresar volumen, cotización de compra y costos propios, guardar escenarios y compararlos. |
| Ranking y comparación | Tarjetas y tabla para comparar precio FOB observado, volumen y cobertura. Los cálculos de costos y punto de equilibrio usan los valores ingresados por el productor. Los pronósticos piloto se identifican por la semana objetivo. |
| Ficha independiente por destino | Estados Unidos, España y Países Bajos conservan sus propias métricas al alternar la selección. La ficha reúne requisitos oficiales y políticas públicas de abastecimiento del comprador potencial. |
| Restricciones y evidencia | Las fichas muestran un resumen antes de abrir el modal. El detalle indica el alcance y la fecha de consulta o vigencia. Al final, cada enlace identifica el documento o comunicado y la afirmación que respalda. |
| Especificaciones comerciales | El productor puede registrar versiones con fechas de emisión y vigencia, documento y huella SHA-256 opcional. La evaluación de un lote queda pendiente hasta contar con evidencia propia. |
| Exportaciones simuladas | Siete operaciones de ejemplo usan pesos simulados y el FOB observado del cultivo, destino y semana correspondiente. El monto de ejemplo es peso por FOB observado. Se retiraron compradores, costos y controles de lote ficticios de los seis borradores activos de prueba. Los archivos históricos de demostración quedaron identificados como tales. |

La instalación local se levantó con Nginx, FastAPI y PostgreSQL en el puerto 8050. Se comprobó el acceso, la persistencia de ofertas y borradores, la selección de destinos, la consulta por fecha, el orden de las fuentes y la navegación en Chrome de escritorio y móvil. Las nueve pruebas de lógica de planificación pasaron. Estas comprobaciones acreditan funcionamiento técnico. El piloto con usuarios y los experimentos finales siguen pendientes.

Las capturas de la revisión técnica se guardaron localmente en **sistema-web-agro/docs/planificacion-2026-11-27/**. Las capturas 10 a 12 muestran el modal de comprador, el documento oficial y la vista móvil.

## Fuentes y tratamiento de datos

El corte de embarques y de publicaciones incluidas en el catálogo es el **22 de octubre de 2026**. La aplicación usa la fecha de consulta para distinguir una publicación de su fecha de aplicación. El catálogo regulatorio es parcial y requiere evidencia del lote para declarar cumplimiento.

El archivo semanal de la app contiene **14 683 filas** de producto, destino y semana ISO. En **11 415** figuran como desconocidos el FOB unitario, el peso neto y el FOB total. Al filtrar los tres destinos de la planificación quedan **2 258 filas**, de las que **1 470** tienen esos campos vacíos. Los huecos se conservan como valores desconocidos y las comparaciones informan su cobertura. La semana iniciada el **19 de octubre** fue la última observada del corte y quedó parcial. El FOB es una referencia de exportación en USD/kg. Los precios mayoristas, las cotizaciones de compra y el precio recibido por el productor corresponden a niveles comerciales distintos.

Los compradores que aparecen en la app son minoristas potenciales identificados mediante documentación corporativa pública. La vinculación de una empresa con una venta requiere la especificación comercial de esa operación.

- **Estados Unidos — Whole Foods Market.** Manejo integrado de plagas para productores de fruta fresca incluidos en la política, con exclusión de mayoristas. [Política de salud de polinizadores](https://assets.wholefoodsmarket.com/www/missions-values/Pollinator-Health-Policy-for-Fresh-Produce-and-Floral_121523.pdf)
- **España — Lidl España.** Criterios publicados de residuos en frutas y verduras. [Revista de sostenibilidad, pp. 14–15](https://empresa.lidl.es/content/download/137527/file/Informe_de_sostenibilidad_Lidl_Espa%C3%B1a_2024.pdf#page=15)
- **Países Bajos — Albert Heijn.** Trazabilidad de marca propia hasta la finca y condiciones logísticas para fruta sin procesar. [Estándar de marca propia](https://static.ah.nl/binaries/ah/content/assets/ah-nl/permanent/over-ah/policy---exhibit-e-b-duurzaamheid_nov2025.pdf#page=9) · [Comunicado sobre transporte](https://nieuws.ah.nl/albert-heijn-stopt-met-invliegen-groente-en-fruit-/)

## Cotejo con la tesis en Google Drive

La tesis vigente de Drive registra una modificación el **27 de noviembre de 2026 a las 00:56, hora de Lima**. Se verificó el contenido de las siguientes incorporaciones:

| Parte de la tesis | Contenido verificado |
| --- | --- |
| Capítulo II, § 2.2.6 | Marco comparativo de soluciones y fuentes oficiales de mercado y regulación. Distingue los precios mayoristas peruanos, los reportes de mercados estadounidenses y los catálogos regulatorios. |
| Capítulo III, § 3.2.4 | Las referencias externas deben conservar fuente, fecha, moneda, unidad y nivel comercial. Las consultas regulatorias se tratan como referencias fechadas. |
| Referencias | Constan fuentes oficiales de MIDAGRI/SISAP, USDA-AMS, la Comisión Europea y USDA-APHIS. |
| Estado experimental | H2 figura como no evaluable con la colección auditada. H1, la caracterización histórica de H3 y el experimento LLM de H4 siguen sin resultados finales. |

La formulación de Drive mantiene el alcance de evaluación técnica de la tesis. La planificación comercial, las fichas de compradores potenciales y las exportaciones simuladas se registran aquí como desarrollos del prototipo. La evaluación con participantes para la feria se plantea como un piloto aparte.

## Feria universitaria y siguiente evidencia

**Pregunta propuesta:** ¿AgroScope reduce el tiempo para preseleccionar un destino de exportación sin aumentar la omisión de requisitos críticos?

1. Comparar la app con una hoja de cálculo y las mismas fuentes. Medir tiempo, aciertos y requisitos omitidos usando tareas equivalentes en distinto orden. Si participa una sola persona, reportar un estudio de caso.
2. Revisar tres casos de referencia con respuesta esperada: capacidad insuficiente, cambio de vigencia y evidencia del lote pendiente. Documentar por qué cambia la preselección y qué documento respalda la decisión.
3. Completar la evaluación temporal de los pronósticos por cultivo, destino y horizonte con datos congelados. En el piloto de desarrollo, el último valor ya superó a XGBoost y LightGBM en WAPE de volumen para los tres cultivos.
4. Demostrar un caso de arándano, tres destinos y dos fechas. Mostrar el volumen simulado, el FOB observado, la vigencia del requisito y la cita directa. Priorizar en la interfaz una explicación breve de la posición del destino y de la evidencia que falta.

La Escuela de Ingeniería de Sistemas de la UNSA publicó el cierre de inscripción el **30 de noviembre**, la entrega del artículo el **7 de diciembre a las 23:59** y la presentación el **11 de diciembre de 2026**. La elegibilidad de la modalidad de tesis debe confirmarse con la organización. [Convocatoria de la Feria de Proyectos de Investigación 2026](https://fips.unsa.edu.pe/ingenieriadesistemas/feria-de-proyectos-2026/)
