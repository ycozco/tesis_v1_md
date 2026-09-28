# Auditoría bibliográfica de la tesis

Fecha: 25 de septiembre de 2026 · Inventario de las 73 entradas presentes en la sección Referencias.

**Título de trabajo adoptado:** *Sistema de información y pronóstico de mercados agroexportadores para la evaluación de escenarios comerciales de palta, uva fresca y arándano.*

La auditoría se reinterpreta bajo este alcance: las referencias deben sostener información de mercados, pronósticos, escenarios/sensibilidad, trazabilidad y evaluación de uso. El productor–acopiador es un perfil de usuario junto con productores, exportadores y vendedores de grandes volúmenes; ninguna referencia debe utilizarse para atribuirle por sí sola decisiones de inversión, rentabilidad o representatividad sectorial.

## 1. Qué se comprobó y qué no

Se contrastaron referencias problemáticas con publicaciones originales, repositorios oficiales y metadatos depositados por los editores en Crossref. La matriz distingue referencias corroboradas, correcciones identificadas y entradas pendientes. **Inventariar 73 entradas no significa haber validado exhaustivamente el contenido de las 73 publicaciones.** Tampoco demuestra calidad metodológica, ausencia de retractaciones o que cada cita del cuerpo respalde su afirmación.

No se debe llamar «falsa» a una referencia solo porque falte DOI, haya un error HTTP o no se encuentre inmediatamente. Algunos accesos a MDPI devolvieron HTTP 429; se contrastaron metadatos y resultados editoriales disponibles. Crossref tampoco contiene necesariamente todos los identificadores de otros registradores. Un DOI que apunta a otra obra es un problema diferente y más preciso que un enlace inaccesible.

## 1.1 Qué debe añadirse para el enfoque de escenarios

Además de corregir las referencias rotas, la tesis necesita separar cinco familias de evidencia: (a) estadísticas oficiales de comercio y mercados; (b) métodos de pronóstico y validación temporal; (c) simulación determinística, análisis de sensibilidad e incertidumbre; (d) costos, merma, margen y punto de equilibrio como conceptos de escenario; y (e) evaluación de reportes, trazabilidad y comprensión de usuarios. Una fuente que estudia fraude contable o una arquitectura LLM puede conservarse como antecedente metodológico, pero no debe presentarse como evidencia directa de precios de compra, ganancias, decisiones de cultivo o desempeño agroexportador.

La prioridad bibliográfica para el nuevo título es: integrar el antecedente peruano de arándano; documentar la procedencia y fecha de los datos MIDAGRI, SUNAT y BCRP; añadir, si se implementan, fuentes oficiales de precios mayoristas/locales; y respaldar el módulo de escenarios con bibliografía de sensibilidad y evaluación de pronósticos. Los precios introducidos por el usuario deben rotularse como supuestos, no como hechos respaldados por una referencia.

## 2. Errores de mayor riesgo

| Entrada | Problema confirmado | Sustitución o acción |
|---|---|---|
| Lewis et al., RAG | DOI `10.18653/v1/2020.emnlp-main.727` pertenece a Xia, Xuan y Yu, sobre rumores en redes sociales; autores y congreso de RAG también están mezclados. | Reconstruir la referencia desde NeurIPS 2020. [Obra equivocada](https://aclanthology.org/2020.emnlp-main.727/) · [RAG correcto](https://proceedings.neurips.cc/paper/2020/hash/6b493230-Abstract.html). |
| Thanathamathee et al. | DOI terminado en `-024` corresponde a *SlowFast-TCN*, sobre reconocimiento visual del habla, no fraude financiero. | DOI correcto terminado en `-016`; título dice «Weighted», no «Weighting»; completar cuatro autores y páginas 2404–2430. [Editorial](https://www.ijournalse.org/index.php/ESJ/article/view/2653). |
| Lim et al., TFT | Se atribuye a ICLR y se pone arXiv `1912.09300`, que corresponde a un artículo de matrices aleatorias. | Usar publicación en *International Journal of Forecasting* 37(4), 1748–1764, DOI `10.1016/j.ijforecast.2021.03.012`. Preprint correcto: `1912.09363`. [Editorial](https://doi.org/10.1016/j.ijforecast.2021.03.012) · [identificador equivocado](https://arxiv.org/abs/1912.09300). |
| NIST, AI RMF 1.0 | `NIST.AI.600-1` corresponde al perfil de IA generativa de 2024. | Para AI RMF 1.0 de 2023 usar `NIST.AI.100-1`; si se usan ambos documentos, crear dos referencias distintas. [NIST](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10). |
| Kreuzberger et al. | Inicial Hirschl G., título abreviado, año, volumen, páginas y DOI no corresponden a la publicación final de MLOps. | Hirschl S.; 2023; *IEEE Access*, 11, 31866–31879; DOI `10.1109/ACCESS.2023.3262138`. El preprint de 2022 es otra versión legítima, no debe mezclarse. [Repositorio institucional](https://epub.uni-bayreuth.de/id/eprint/7577/1/Machine_Learning_Operations_MLOps_Overview_Definition_and_Architecture.pdf). |
| «Schneider et al.» | El DOI de RAG en BISE pertenece a Michael Klesel y H. Felix Wittmann. | Corregir autores en bibliografía y en todas las citas del texto. [Editorial](https://link.springer.com/article/10.1007/s12599-025-00945-3). |
| «Mongolia et al.» / «Varios autores» | Mongolia es el país, no un autor. La entrada carece de autores identificados. | Sodnomdavaa y Lkhagvadorj. La editorial cita la entrega 2026; Crossref registra publicación online el 24/12/2025. Normalizar por versión, no llamar inventado al artículo. [Cita editorial](https://www.mdpi.com/1911-8074/19/1/13). |
| Prenio y Yong | La obra existe, pero no es de 2024 ni tiene solo esos dos autores. | Pérez-Cruz, Prenio, Restoy y Yong; septiembre de 2025; FSI Occasional Papers 24. [BIS](https://www.bis.org/fsi/fsipapers24.pdf). |
| Ruff et al. | La lista de autores de *Deep One-Class Classification* no coincide con la publicación. | Reemplazar lista completa desde PMLR; no mezclarla con autores de otras revisiones sobre anomalías. [PMLR](https://proceedings.mlr.press/v80/ruff18a.html). |
| Hyndman–Khandakar | Solo queda «t package for R…». | Restaurar autores, año 2008 y título completo. [Journal of Statistical Software](https://www.jstatsoft.org/index.php/jss/article/view/v027i03). |
| Patel et al. (2024) | No se localizó una coincidencia verificable de la combinación de título y cuatro autores consignada. | Solicitar el PDF original o registro editorial. Mientras no se identifique, no usarla como soporte de afirmaciones. «No localizada» no equivale a «demostrada falsa». |

## 3. Matriz de las 73 entradas

Numeración de auditoría: orden de aparición en la tesis, no numeración APA. Estados: **V** = identidad/metadatos básicos corroborados, no validación de todas sus afirmaciones; **C** = corrección o complemento concreto identificado; **P** = revisión editorial/versionado aún pendiente; **NL** = no localizada con los datos suministrados. Las observaciones limitan el alcance de cada estado.

| N.º | Entrada identificable | Estado | Acción o evidencia |
|---|---|---|---|
| 1 | Chen y Guestrin, XGBoost, 2016 | V | DOI, autores, congreso y páginas corroborados en Crossref. [DOI](https://doi.org/10.1145/2939672.2939785). |
| 2 | Gebru et al., Datasheets, 2021 | V | Metadatos y siete autores corroborados. [DOI](https://doi.org/10.1145/3458723). |
| 3 | «t package for R…» | C | Restaurar Hyndman y Khandakar (2008); ficha corregida abajo. |
| 4 | Jesus et al., Turning the Tables, 2022 | C | Autores y preprint reales, aceptación NeurIPS confirmada; elegir versión y eliminar rótulo suelto «[NeurIPS 2022]». [arXiv](https://arxiv.org/abs/2211.13358). |
| 5 | Kadir et al., AuditCopilot, 2025 | C | Referencia real; el problema principal está en el resumen del antecedente: título diferente, tiempo de revisión y valoración experta no sustentados allí. [arXiv](https://arxiv.org/abs/2512.02726). |
| 6 | Ke et al., LightGBM, 2017 | P | Completar enlace editorial y cotejo final de ficha. No se marca inexistente. |
| 7 | Kreuzberger et al., MLOps | C | Corregir autor, título y publicación final a 2023, volumen 11, 31866–31879. |
| 8 | Lewis et al., RAG | C | DOI de otra obra, autores y sede erróneos. |
| 9 | Li et al., ECOD | C | DOI y autores válidos; combinar volumen 35(12) con año final 2023, no 2022 online. [Repositorio de coautor](https://publications.pik-potsdam.de/pubman/item/item_26927_5). |
| 10 | Lim et al., TFT | C | Revista y arXiv incorrectos; ficha abajo. |
| 11 | Lin, ROUGE, 2004 | P | Añadir enlace primario y cotejar título formal del taller. Su uso no prueba fidelidad factual. |
| 12 | Liu et al., Isolation Forest, 2008 | V | Identidad, tres autores y páginas corroborados. [DOI](https://doi.org/10.1109/ICDM.2008.17). |
| 13 | Liu et al., iTransformer, 2024 | P | Añadir registro ICLR y cotejar lista de autores/versiones. |
| 14 | Lundberg y Lee, SHAP, 2017 | P | Completar enlace editorial y cotejo final de ficha; distinguir explicación de predicción y causalidad. |
| 15 | Mitchell et al., Model Cards, 2019 | V | DOI, autores y páginas corroborados. Normalizar nombre del congreso de esa edición. [DOI](https://doi.org/10.1145/3287560.3287596). |
| 16 | NIST, AI RMF 1.0, 2023 | C | DOI corresponde a otro informe; ver autoría recomendada en ficha oficial. |
| 17 | Nie et al., PatchTST, 2023 | P | Añadir registro ICLR y confirmar metadatos completos. |
| 18 | Oreshkin et al., N-BEATS, 2020 | C | Es ICLR, no ICML. Sustituir sede, páginas e identificador mezclados por registro oficial. [ICLR](https://openreview.net/forum?id=r1ecqn4YwB). |
| 19 | Papineni et al., BLEU, 2002 | P | DOI identifica BLEU; Crossref presenta fecha inconsistente con ACL '02. Cotejar ficha/PDF de ACL antes de alterar el año 2002. No usar como verificador de hechos. |
| 20 | Park, agentes LLM, 2024 | C | Preprint real; retirar o respaldar cuantitativamente la superioridad TPR/FPR afirmada en el cuerpo. [Texto](https://arxiv.org/html/2403.19735v1). |
| 21 | Patel et al., 2024 | NL | Pendiente PDF o registro primario exacto; no reemplazar por una obra parecida de otros autores. |
| 22 | Reglamento UE 2024/1689 | P | Enlace oficial consignado; revisar artículo y ámbito realmente invocados, no asumir aplicación directa a todo prototipo peruano. [Texto normativo](https://eur-lex.europa.eu/eli/reg/2024/1689). |
| 23 | Prenio y Yong, Managing explanations | C | Cuatro autores y año 2025. Antecedente regulatorio financiero, no validación agrícola. |
| 24 | PCM, DS 115-2025-PCM | C | Reemplazar portada genérica de El Peruano por ficha/documento específico, con fecha precisa y artículo citado. [PCM](https://www.gob.pe/institucion/pcm/normas-legales/7133522-115-2025-). |
| 25 | Prokhorenkova et al., CatBoost, 2018 | C | Obra real; el identificador 10.5555 no se recuperó en Crossref, lo cual no prueba inexistencia. Preferir enlace verificable a NeurIPS. [Editorial](https://proceedings.neurips.cc/paper/2018/hash/14491b756b3a51daac41c24863285549-Abstract.html). |
| 26 | Ribeiro et al., LIME, 2016 | V | DOI, autores y páginas corroborados. [DOI](https://doi.org/10.1145/2939672.2939778). |
| 27 | Ruff et al., Deep One-Class, 2018 | C | Lista de autores mezclada. Ficha correcta abajo. |
| 28 | Schneider et al., RAG, 2025 | C | Sustituir por Klesel y Wittmann. |
| 29 | Sculley et al., deuda técnica, 2015 | C | No es solo «Workshop»; faltan Crespo y Dennison. [NIPS 28](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html). |
| 30 | SBS, Resolución 053-2023 | C | Norma real; falta enlace específico al texto. Comunicado confirma alcance financiero/seguros, no obligación automática de productores, acopiadores, exportadores o vendedores de grandes volúmenes. [SBS](https://www.sbs.gob.pe/noticia/detallenoticia/idnoticia/2647). |
| 31 | Taylor y Letham, 2017 | V | Preprint real con DOI válido. Puede conservarse si es la versión usada; no mezclarlo con la posterior publicación en revista. [DOI](https://doi.org/10.7287/peerj.preprints.3190v2). |
| 32 | Thanathamathee et al., 2024 | C | DOI de otra obra; completar título, cuatro autores y páginas. |
| 33 | Pesaranghader y Li, 2026 | V | Preprint identificado; no presentarlo como publicación arbitrada confirmada. [arXiv](https://arxiv.org/abs/2601.09929). |
| 34 | Varios autores, fraude financiero | C | Sodnomdavaa y Lkhagvadorj. Controlar diferencia online 2025 / entrega editorial 2026. |
| 35 | Varios autores, SHAP/LIME forense | C | Hermosilla, Berríos y Allende-Cid (2025); DOI válido. [DOI](https://doi.org/10.3390/app15137329). |
| 36 | Waltersdorfer et al., AuditMAI, 2024 | V | Título, cuatro autores y preprint corroborados. [arXiv](https://arxiv.org/abs/2406.14243). |
| 37 | Zeng et al., Transformers, 2023 | V | Metadatos de AAAI y DOI corroborados. [DOI](https://doi.org/10.1609/aaai.v37i9.26317). |
| 38 | Zhao et al., PyOD, 2019 | C | Ficha real; añadir enlace JMLR y corregir «más de 40» en antecedente: artículo original dice más de 20. [JMLR](https://www.jmlr.org/papers/v20/19-011.html). |
| 39 | Apache Parquet, documentación | P | URL oficial consignada; registrar versión/consulta y uso efectivo. |
| 40 | Docker, documentación | P | Confirmar configuración y versión realmente usadas, no confundir propuesta con ejecución. |
| 41 | FastAPI, documentación | P | Diferenciar migración prevista de componente efectivamente evaluado. |
| 42 | NGINX, documentación | P | Registrar versión y función de despliegue. |
| 43 | React, documentación | P | Conservar si se usa; completar versión reproducible. |
| 44 | Flask, documentación | P | Identificar como heredado si ese es su estado real. |
| 45 | pgvector, repositorio | P | Precisar versión/tag/commit; la página principal cambia. |
| 46 | PostgreSQL, documentación | P | Vincular documentación de la versión utilizada. |
| 47 | SQLAlchemy, documentación | P | Confirmar rama de versión y API utilizada. |
| 48 | Uvicorn, documentación | P | Confirmar uso efectivo y versión. |
| 49 | Vite, documentación | P | Confirmar uso efectivo y versión. |
| 50 | MIDAGRI, 9 febrero 2026 | C | Resolver sufijo a/b con la entrada de enero y actualizar citas del cuerpo; contrastar cifras con tabla o nota específica. |
| 51 | MIDAGRI, 6 enero 2026 | C | En el cuerpo aparece MIDAGRI 2026 sin distinguir noticia. Vincular cada afirmación a la nota correspondiente. |
| 52 | SUNAT, régimen definitivo | C | Página institucional no identifica por sí sola los archivos exactos usados. Añadir fuente de extracción, cobertura, fecha, filtros y versión. |
| 53 | Hyndman y Athanasopoulos, FPP3 | P | Referencia reconocible; comprobar edición/fecha frente a libro web actualizado y capítulos utilizados. |
| 54 | Montero-Manso y Hyndman, 2021 | V | DOI, revista, volumen y páginas corroborados. [DOI](https://doi.org/10.1016/j.ijforecast.2021.03.004). |
| 55 | Alufaisan et al., 2021 | V | DOI y ficha corroborados. No inferir que toda explicación mejora toda decisión. [DOI](https://doi.org/10.1609/aaai.v35i8.16819). |
| 56 | Han et al., ADBench, 2022 | C | Reparar URL con sufijo `Abstract-Datasets_and_Benchmarks.html`. [Enlace editorial](https://papers.neurips.cc/paper_files/paper/2022/hash/cf93972b116ca5268827d575f2cc226b-Abstract-Datasets_and_Benchmarks.html). |
| 57 | BCRP, Memoria 2025 | C | Documento identificado; anotar tabla/página que respalda cada cifra. No mezclar sin explicación categorías estadísticas de BCRP y MIDAGRI. [PDF](https://www.bcrp.gob.pe/docs/Publicaciones/Memoria/2025/memoria-bcrp-2025.pdf). |
| 58 | Grinsztajn et al., 2022 | P | Completar cotejo editorial; evitar convertir resultados de datasets tabulares en prueba universal para series agroexportadoras. |
| 59 | Breunig et al., LOF, 2000 | V | DOI y páginas corroborados. Revisar inicial de Raymond T. Ng: corresponde R. T., no solo R. [DOI](https://doi.org/10.1145/342009.335388). |
| 60 | Hewamalage et al., 2023 | C | Añadir DOI `10.1007/s10618-022-00894-5`; retirar nota de trabajo entre corchetes. [Editorial](https://doi.org/10.1007/s10618-022-00894-5). |
| 61 | Gneiting y Raftery, 2007 | P | Completar cotejo y enlace editorial; retirar «[Reglas de puntuación]». |
| 62 | Hansen et al., 2011 | P | Completar cotejo y enlace; usar MCS solo si realmente se implementa y justifica. |
| 63 | Croston, 1972 | P | Completar cotejo y enlace; justificar pertinencia a series intermitentes seleccionadas. |
| 64 | Wickramasuriya et al., 2019 | P | Completar cotejo; no afirmar reconciliación jerárquica si no se ejecuta. |
| 65 | Tatbul et al., 2018 | P | Completar enlace; definir eventos y tolerancias antes de usar métricas de rango. |
| 66 | Wu y Keogh, 2021 | C | Distinguir online 2021 de entrega final 2023, 35(3); completar páginas desde editorial. [IEEE](https://ieeexplore.ieee.org/document/9537291/). |
| 67 | Li, Zhu y Van Leeuwen, survey | C | DOI `10.1145/3609333`, artículo 23, 54 páginas; online septiembre 2023 y entrega enero 2024. No declarar falso el año 2023 sin precisar versión. [Editorial](https://doi.org/10.1145/3609333). |
| 68 | Gao et al., ALCE, 2023 | C | Añadir páginas 6465–6488 y DOI; retirar anotación entre corchetes. [ACL](https://aclanthology.org/2023.emnlp-main.398/). |
| 69 | Min et al., FActScore, 2023 | C | Añadir páginas 12076–12100 y DOI; normalizar autores con el PDF y retirar anotación. [ACL](https://aclanthology.org/2023.emnlp-main.741/). |
| 70 | Wilkinson et al., FAIR, 2016 | P | Exportar ficha completa desde editorial y aplicar regla APA para más de 20 autores; «et al.» no es sustituto automático de la lista bibliográfica. |
| 71 | W3C, PROV-DM, 2013 | P | Añadir URL específica de recomendación, fecha y autoría/editorship según ficha oficial. |
| 72 | Pineau et al., reproducibilidad, 2021 | C | Completar ocho autores, enlace JMLR y retirar nota entre corchetes. [JMLR](https://www.jmlr.org/beta/papers/v22/20-303.html). |
| 73 | Carrión Mezones et al., arándano, 2026 | C | Añadir DOI, conservar apellidos editoriales con guion e integrar antecedente al capítulo II. [Editorial](https://doi.org/10.3390/su18094529). |

## 4. Fichas corregidas para las sustituciones principales

Formato autor–fecha compatible con APA; aplicar después cursivas, sangría francesa y orden definitivo en la tesis. Los enlaces siguientes identifican las fuentes. No sustituir la bibliografía completa por esta selección.

**Hyndman y Khandakar:** Hyndman, R. J., & Khandakar, Y. (2008). Automatic time series forecasting: The forecast package for R. *Journal of Statistical Software, 27*(3), 1–22. [DOI](https://doi.org/10.18637/jss.v027.i03).

**MLOps:** Kreuzberger, D., Kühl, N., & Hirschl, S. (2023). Machine learning operations (MLOps): Overview, definition, and architecture. *IEEE Access, 11*, 31866–31879. [DOI](https://doi.org/10.1109/ACCESS.2023.3262138).

**RAG original:** Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*. [Registro editorial](https://proceedings.neurips.cc/paper/2020/hash/6b493230-Abstract.html). Completar paginación desde la exportación editorial si el formato institucional la exige; no conservar las páginas mezcladas de EMNLP.

**ECOD, versión final:** Li, Z., Zhao, Y., Hu, X., Botta, N., Ionescu, C., & Chen, G. H. (2023). ECOD: Unsupervised outlier detection using empirical cumulative distribution functions. *IEEE Transactions on Knowledge and Data Engineering, 35*(12), 12181–12193. [DOI](https://doi.org/10.1109/TKDE.2022.3159580).

**TFT:** Lim, B., Arık, S. Ö., Loeff, N., & Pfister, T. (2021). Temporal fusion transformers for interpretable multi-horizon time series forecasting. *International Journal of Forecasting, 37*(4), 1748–1764. [DOI](https://doi.org/10.1016/j.ijforecast.2021.03.012).

## 5. Matriz de cobertura que debe cerrarse antes de la versión final

| Componente del título | Evidencia mínima que debe quedar identificada | Riesgo si falta |
|---|---|---|
| Información de mercados | Fuente, fecha de actualización, unidad, cobertura por producto/destino y regla de extracción. | Presentar datos antiguos o no comparables como información actual. |
| Pronóstico | Método, horizonte, partición temporal, baseline, métrica y periodo de prueba. | Confundir una proyección con una cifra observada o seleccionar el modelo con datos futuros. |
| Escenarios comerciales | Definición de volumen, precio, costos, merma, moneda, periodo y fórmula. | Presentar una ganancia simulada como resultado real o recomendación. |
| Sensibilidad e incertidumbre | Escenarios bajo/central/alto, intervalos o advertencia explícita cuando no existan. | Dar falsa precisión a decisiones de compra, venta o inversión. |
| Usuarios | Instrumento y perfil real de cada participante: productor, acopiador, exportador o vendedor de volumen. | Generalizar la opinión de un participante a todo el sector. |
| Trazabilidad | Vínculo entre cifra, fuente, fecha, transformación, supuesto y reporte. | Imposibilidad de verificar o corregir una conclusión. |

La bibliografía quedará cerrada solo cuando cada componente tenga una fuente o una declaración metodológica suficiente y cada referencia problemática esté corregida, retirada o marcada como pendiente sin inventar datos.

**NIST:** Tabassi, E. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). National Institute of Standards and Technology. [DOI](https://doi.org/10.6028/NIST.AI.100-1). Esta autoría sigue la ficha de NIST; si se adopta, cambiar también las citas del cuerpo de NIST (2023) a Tabassi (2023). El documento es un marco voluntario, no una obligación universal del productor.

**N-BEATS:** Oreshkin, B. N., Carpov, D., Chapados, N., & Bengio, Y. (2020). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. *International Conference on Learning Representations*. [Registro ICLR](https://openreview.net/forum?id=r1ecqn4YwB).

**BIS:** Pérez-Cruz, F., Prenio, J., Restoy, F., & Yong, J. (2025). *Managing explanations: How regulators can address AI explainability* (FSI Occasional Papers No. 24). Bank for International Settlements. [Documento](https://www.bis.org/fsi/fsipapers24.pdf).

**Deep One-Class:** Ruff, L., Vandermeulen, R., Goernitz, N., Deecke, L., Siddiqui, S. A., Binder, A., Müller, E., & Kloft, M. (2018). Deep one-class classification. *Proceedings of Machine Learning Research, 80*, 4393–4402. [Registro PMLR](https://proceedings.mlr.press/v80/ruff18a.html).

**RAG en BISE:** Klesel, M., & Wittmann, H. F. (2025). Retrieval-augmented generation (RAG). *Business & Information Systems Engineering, 67*, 551–561. [DOI](https://doi.org/10.1007/s12599-025-00945-3).

**Deuda técnica:** Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F., & Dennison, D. (2015). Hidden technical debt in machine learning systems. *Advances in Neural Information Processing Systems, 28*. [Registro editorial](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html).

**SHAP-Instance:** Thanathamathee, P., Sawangarreerak, S., Chantamunee, S., & Mohd Nizam, D. N. (2024). SHAP-instance weighted and anchor explainable AI: Enhancing XGBoost for financial fraud detection. *Emerging Science Journal, 8*(6), 2404–2430. [DOI](https://doi.org/10.28991/ESJ-2024-08-06-016).

**Fraude financiero, versión de la entrega editorial:** Sodnomdavaa, T., & Lkhagvadorj, G. (2026). Financial statement fraud detection through an integrated machine learning and explainable AI framework. *Journal of Risk and Financial Management, 19*(1), Article 13. [DOI](https://doi.org/10.3390/jrfm19010013). Nota de control: publicado online en 2025, citado por la editorial como 2026. Usar una sola convención de versión en texto y bibliografía.

**SHAP/LIME forense:** Hermosilla, P., Berríos, S., & Allende-Cid, H. (2025). Explainable AI for forensic analysis: A comparative study of SHAP and LIME in intrusion detection models. *Applied Sciences, 15*(13), Article 7329. [DOI](https://doi.org/10.3390/app15137329).

**Evaluación temporal:** Hewamalage, H., Ackermann, K., & Bergmeir, C. (2023). Forecast evaluation for data scientists: Common pitfalls and best practices. *Data Mining and Knowledge Discovery, 37*, 788–832. [DOI](https://doi.org/10.1007/s10618-022-00894-5).

**ALCE:** Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. En *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 6465–6488). Association for Computational Linguistics. [DOI](https://doi.org/10.18653/v1/2023.emnlp-main.398).

**FActScore:** Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-t., Koh, P., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. En *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 12076–12100). Association for Computational Linguistics. [DOI](https://doi.org/10.18653/v1/2023.emnlp-main.741). Inicial de Koh conforme a la exportación de ACL; comprobar contra la versión del PDF citada al importar al gestor.

**Reproducibilidad:** Pineau, J., Vincent-Lamarre, P., Sinha, K., Larivière, V., Beygelzimer, A., d'Alché-Buc, F., Fox, E., & Larochelle, H. (2021). Improving reproducibility in machine learning research (A report from the NeurIPS 2019 reproducibility program). *Journal of Machine Learning Research, 22*(164), 1–20. [Artículo](https://www.jmlr.org/beta/papers/v22/20-303.html).

**Antecedente peruano:** Carrión-Mezones, J. M., Cúneo-Fernández, F. E., & Morán-Santamaría, R. O. (2026). Forecasting Peruvian blueberry exports for sustainable agricultural trade management: Markov chains, SARIMA, and log-linear growth. *Sustainability, 18*(9), Article 4529. [DOI](https://doi.org/10.3390/su18094529).

## 5. Reparar citas en el cuerpo, no solo la lista final

1. Buscar «Mongolia», «Varios autores», «Schneider», «Hirschl», «Prenio», «2022» asociado a ECOD/MLOps y el título incorrecto de AuditCopilot. Sustituir solo coincidencias que correspondan a estas obras.
2. En MIDAGRI, distinguir la noticia de enero sobre productos/mercados de la de febrero sobre ventas. Una propuesta coherente es enero = 2026a y febrero = 2026b; actualizar todas las citas conjuntamente con el orden bibliográfico final. No dejar MIDAGRI (2026) ambiguo.
3. Separar «la obra existe» de «esta afirmación está en la obra»: tiempo ahorrado, expertos favorables y mejora de precisión requieren resultado o tabla identificable. No inferirlos de un abstract promocional.
4. Eliminar anotaciones de trabajo como «[Antecedente peruano]» y «[Fidelidad factual]» de la bibliografía entregable. Mantenerlas, si sirven, en fichas de lectura separadas.
5. Añadir referencias primarias para FT-Transformer, TabNet o TabLLM si se mantienen afirmaciones específicas sobre esos métodos. Su mención en una comparación no demuestra que se implementaron.
6. Verificar correspondencia bidireccional: cada cita del cuerpo tiene una entrada y cada entrada de la lista se utiliza de manera pertinente. Este cruce completo sigue pendiente; la presente matriz no lo certifica.
7. Distinguir referencias académicas, normativa, documentación de software y procedencia de datos. Una URL institucional genérica no documenta un dataset reproducible.

## 6. Criterio de cierre bibliográfico

Una referencia queda cerrada cuando su identidad y versión son inequívocas, su enlace lleva a la obra correcta, la ficha coincide con la fuente primaria y las afirmaciones para las que se usa están efectivamente respaldadas. Resolver primero las obras mezcladas de §2; después las entradas incompletas; finalmente el cotejo pendiente y el estilo global. No completar años, páginas, autores o DOI por semejanza con otro artículo.

