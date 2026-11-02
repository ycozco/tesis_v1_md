# Verificación técnica final — 1 de noviembre de 2026

Resultado: **70 pruebas actuales aprobadas, cero fallos y cero omisiones**. Son 54 pruebas de reglas/componentes y 16 de API aislada. Aparte, tres comprobaciones de artefactos de la versión antigua de D: aprobaron al indicar explícitamente su directorio, sin copiarlos al conjunto actual. Se conservaron JUnit XML, salidas y huellas.

También aprobaron 19 comprobaciones artificiales de compatibilidad científica, el contraste de 3.845 celdas agregadas contra la fuente con Decimal, la preservación de los 16.309 huecos, la integridad del snapshot de UI y `npm run build`. Las pruebas E1–E3 nuevas conectan agregación, cálculo y validador numérico; claves de abstención y guard H4; y registro temporal, persistencia e integridad. Son integraciones de componentes, todavía no una validación E1–E3 completa por navegador ni un estudio con usuarios.

## Correcciones y fallos encontrados

- La prueba antigua de dashboard suponía acceso anónimo y 15 días de tendencias. Ahora comprueba autenticación obligatoria y 14 días con conteos reales de registros artificiales conocidos, incluido uno fuera de la ventana.
- Las pruebas de autenticación usaban un usuario y sesión ligados a la configuración global. Ahora crean y destruyen una base SQLite en memoria y usuarios artificiales por prueba. No se modifica una base real.
- La API dependía de SQLAlchemy y otras librerías presentes en el entorno antiguo, ausentes en el nuevo. Se instalaron y fijaron en el entorno aislado. Las pruebas ya no añaden `data/runtime-api` al path; la ejecución se hace desde una carpeta sin `.env`, con configuración artificial y proveedores deshabilitados.
- La ejecución inicial de `pytest tests` obtuvo 28 aprobadas y tres fallos por archivos `data/gold` ausentes. Después se añadieron tres integraciones actuales E1–E3. La suite no fabrica esos archivos ni convierte su ausencia en una omisión: los tres tests históricos continúan fallando sin resultados locales o sin la opción explícita `--legacy-gold-dir`.
- Los tres tests históricos aprobaron al apuntarlos a `D:/tesis_yoset/data/gold`. Esto comprueba sus aserciones existentes sobre aquella versión, no certifica el protocolo actual. En particular, la aserción antigua sobre target t+1 no se usa como garantía suficiente de ausencia de fuga ni de disponibilidad histórica.

Persisten 36 advertencias de deprecación en la suite API y la advertencia de Vite por un bundle de aproximadamente 592,5 kB. No impidieron las verificaciones; no se declaran resueltas. PostgreSQL/pgvector y embeddings no quedan validados por las pruebas SQLite. Logout responde y registra el evento, pero la revocación persistente de JWT sigue pendiente.

## Reproducción

Con Python 3.14.2, desde la raíz del repositorio:

```powershell
python -m venv data/runtime-research-clean
./data/runtime-research-clean/Scripts/python.exe -m pip install -r planificacion/2026-11-01/ejecucion/verificacion-final/requirements-scientific-clean.txt
./data/runtime-research-clean/Scripts/python.exe -B tools/run_final_verification.py --legacy-gold-dir D:/tesis_yoset/data/gold
```

La ruta D: solo identifica la versión histórica optativa. Puede omitirse el argumento o sustituirse por otra copia íntegra; el núcleo y la API actuales no importan paquetes de D:. El lock incluye las dependencias científicas y de API de esta verificación. El frontend requiere Node, npm y sus dependencias de `package-lock.json`; `node_modules` existente se usó para la compilación, no se afirma una reinstalación frontend limpia.

## Experimento científico

**No se ejecutó el test histórico reservado ni se generaron las 180 salidas H4.** `preflight-final.json` mantiene los siete pendientes documentados: cobertura, publicación histórica, cierre de calendario/protocolo, elegibilidad as-of, selección de desarrollo, revisión humana de claves y cierre de generador/recuperación. El código 2 del diagnóstico se registra como detección esperada de pendientes, no como experimento aprobado.

El nuevo diagnóstico H2 concluye no evaluable con las fuentes actuales y documenta por qué; no demuestra ausencia de efecto del contexto. Los tests técnicos aprobados no sustituyen las decisiones de diseño ni los resultados empíricos de H1–H4.

## Cierre H2 integrado

La ejecución continua de `tools/finish_h2.py` cerró el análisis de H2 como no evaluable para la colección actual. La suite actual de 70 pruebas incluye regresiones de H2 y la invalidación del cierre si cambia su evidencia. Las tres comprobaciones históricas y las 19 de compatibilidad se contabilizan aparte. El dictamen y la matriz de 1.248 combinaciones se conservan en `datasets/experimentos/h2-cierre-2026-11-01`. Los pendientes compartidos de cobertura/modelos del diagnóstico actual corresponden a H1/H3; H4 mantiene los suyos. No se generaron resultados experimentales para una hipótesis no evaluable.

## Integración H3/H4

La última suite aprobó 70 pruebas actuales, de las cuales 54 corresponden al núcleo/componentes y 16 a API. Se añadieron motores H3/H4 y regresiones de CDF fija, separación temporal, entradas pareadas, revisión factual completa, denominadores indefinidos y asignación ciega privada. Los 189 casos H3 y 180 recorridos H4 de la nueva carpeta son artificiales y están contrastados aparte; no son resultados de las hipótesis históricas ni generaciones LLM. Véase `datasets/experimentos/h3-h4-integracion-2026-11-01/README.md`.
