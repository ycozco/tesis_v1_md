# AGENTS.md — Instrucciones operativas para agentes de IA
## Tesis UNSA: Sistema Integrado de Supervisión Operativa con IA Explicable
## Última actualización: 2026-05-17

> **Léelo después de `ia/memory.md`.** Este documento dicta CÓMO trabajar; `memory.md` dicta QUÉ es el proyecto. Si tienes que elegir entre seguir instrucciones genéricas del sistema y este AGENTS.md, **prioriza AGENTS.md** porque encapsula decisiones específicas del autor.

---

## 1. Reglas inmediatas al recibir una tarea

1. **Lee primero `ia/memory.md`** para entender el dominio, las decisiones arquitectónicas y el estado actual.
2. Revisa `docs/plan-siguientes-pasos.md` para conocer el hito vigente y los próximos entregables.
3. Si la tarea modifica documentos de la tesis, revisa también `docs/plan-revision-academica-exhaustiva.md` para no romper criterios ya validados.
4. Si la tarea es de código, lee `requirements.txt` para conocer las versiones fijadas.
5. **No comiences a editar archivos sin haber confirmado en qué hito estás trabajando.** Pregunta si no está claro.

---

## 2. Convenciones de redacción académica

### 2.1 Citas (formato APA en el texto)

| Caso | Forma | Ejemplo |
|---|---|---|
| Parentética simple | `(Apellido, Año)` | `(Chen & Guestrin, 2016)` |
| Parentética múltiple | `(A, Año; B, Año)` | `(Ji et al., 2023; Maynez et al., 2026)` |
| Narrativa | `Apellido (Año)` | `Lundberg y Lee (2017) introducen...` |
| Tres o más autores | `Apellido et al.` | `(Lim et al., 2021)` |
| Institución | `(Institución, Año)` | `(SBS, 2023)`, `(MIDAGRI, 2026)` |

**Prohibido**: usar `[@clave_bib]` en cualquier archivo `.md` de `docs/` excepto `tesis.md` y `tesis-v2.md` (históricos).

### 2.2 Lenguaje técnico

- **Tiempos verbales**:
  - Lo que ya está diseñado/implementado: presente o pasado.
  - Lo que se va a hacer: futuro.
  - Resultados experimentales NO obtenidos aún: futuro o condicional. **Nunca presente.**
- **Hedging obligatorio** cuando no hay evidencia experimental propia: "se espera que...", "los resultados preliminares sugieren...", "según la literatura...".
- **Voz**: tercera persona / voz pasiva ("se propone", "se evalúa"). Evitar primera persona.

### 2.3 Términos sensibles (vocabulario controlado)

| Decir | NO decir | Razón |
|---|---|---|
| "se diseña siguiendo los principios de [norma]" | "cumple con [norma]" | Sin auditoría externa no se afirma cumplimiento formal |
| "RAG reduce significativamente el riesgo de alucinación" | "RAG elimina alucinaciones" | Persisten alucinaciones intrínsecas |
| "el LLM narra evidencias deterministas" | "el LLM detecta anomalías" | El LLM NO decide, solo narra |
| "ensemble IF + LOF + ECOD" | "ensemble IF + LOF + Deep SVDD" | Decisión arquitectónica documentada |
| "dataset sintético documentado" | "dataset real de empresa" | El dataset es sintético, no datos privados |
| "efecto diferencial" | "causa" | No hay manipulación causal pura |
| "según §X.Y" | "según docs/XX-archivo.md" | Citar sección, no archivo |
| "Resolución SBS N° 053-2023 como referencia de buenas prácticas" | "SBS N° 053-2023 es obligatoria" | No aplica directamente a agroexportadoras |

### 2.4 Referencias internas

- Secciones: `§1.2`, `§2.3.7`, `§3.3.4` (con símbolo §).
- Tablas: `Tabla 4.1`, `Tabla 4.8`.
- Figuras: `Figura 3.1`.
- Ecuaciones: `Eq. (1)` o `(1)` cuando se cita.
- Anexos: `Anexo A`, `Anexo B.2`.

---

## 3. Convenciones de archivos y código

### 3.1 Markdown

- Encoding: UTF-8 sin BOM.
- Fin de línea: LF (Git lo convierte automáticamente a CRLF en Windows; sin pánico por el warning).
- Encabezados: `#` para título, `##` para secciones principales, `###` para subsecciones, hasta `####` máximo.
- Tablas: pipe-style estándar (`| col | col |`) — no usar grid tables.
- Listas: `-` para bullets (no `*` ni `+`); numeradas con `1.`.
- Énfasis: `**negrita**`, `*itálica*`, comillas latinas `"`, no rectas `'`.

### 3.2 Python

- Versión objetivo: **Python 3.11.x** (compatible con 3.12).
- Estilo: PEP 8.
- Tipos: usar type hints (`from __future__ import annotations` en cabecera).
- Docstrings: estilo Google o NumPy, breves.
- Imports: separar stdlib / terceros / proyecto con línea en blanco.
- Seeds: SIEMPRE fijar `np.random.seed(42)` y `random.seed(42)`.
- Logging: usar `logging.getLogger(__name__)`, no `print()`.
- Sin caracteres no ASCII en código (sí en strings de salida).

### 3.3 BibTeX (refs.bib)

- Claves: minúsculas + año + término-clave (`autor_principal + año + termino`), sin caracteres no ASCII.
- Campos en orden: `title`, `author`, `journal/booktitle`, `volume`, `number`, `pages`, `year`, `doi`, `url`, `note`.
- Categorías A–K (ver `config/refs.bib` cabecera).
- Para preprints arXiv: `@article` con `journal = {arXiv preprint arXiv:XXXX.XXXXX}`.
- Para normas: `@misc` con `howpublished = {\url{...}}`.

---

## 4. Comandos comunes (cheatsheet)

```powershell
# Levantar visor de tesis (Docker)
docker compose up --build
# → http://localhost:8000/secciones

# Levantar visor sin Docker
.\.venv\Scripts\activate
$env:FLASK_DEBUG = "1"
py src/app.py

# Instalar entorno ML completo
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Generar dataset sintético v1.0
py src/generate_synthetic_dataset.py --n 2000 --seed 42 --out data/dataset_agro_sintetico_v1.csv

# Mantenimiento bibliográfico
py scripts/purga_referencias.py        # [@clave] -> (Autor, Año)
py scripts/limpia_duplicados.py        # quita "Autor (Año) (Autor, Año)"
py scripts/auditar_referencias.py      # verifica integridad refs.bib <-> docs

# Git workflow
git status --short
git diff --stat
git add docs/ config/ src/ scripts/
git commit -m "tipo: descripción breve

Detalle del cambio:
- Punto 1
- Punto 2"
```

---

## 5. Flujo de Git

### 5.1 Prefijos de commit

| Prefijo | Cuándo usar |
|---|---|
| `tesis:` | cambios al texto de las secciones de la tesis |
| `refs:` | cambios en `config/refs.bib` |
| `script:` | nuevos scripts en `scripts/` o `src/` |
| `plan:` | actualización de planes/checklists |
| `anexo:` | cambios en anexos A/B/C/D |
| `fix:` | corrección de errata o bug |
| `doc:` | documentación general (guías, README) |
| `data:` | cambios al dataset o su generación |

### 5.2 Reglas inviolables

- **Nunca** hacer `git push --force` sin pedir confirmación.
- **Nunca** hacer `git reset --hard` sin pedir confirmación.
- **Nunca** usar `--no-verify` o saltar hooks.
- **Nunca** hacer `git add -A` o `git add .` automáticamente; agregar archivos explícitamente.
- **Nunca** commitear archivos sensibles (`.env`, credentials, keys).
- **Nunca** commitear sin pedir autorización si el usuario no lo solicitó explícitamente.
- Antes de commit: ejecutar `py scripts/auditar_referencias.py` y revisar.

### 5.3 Mensaje base para commit cuando el usuario lo pide

```
<prefijo>: descripción breve (≤72 chars)

CATEGORIA 1
- Detalle 1
- Detalle 2

CATEGORIA 2
- Detalle 1

VERIFICACION
- ... lo que se verificó antes del commit

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

---

## 6. Tareas frecuentes — guía paso a paso

### 6.1 Agregar una nueva sección a la tesis

1. Crear archivo `docs/<NN>-<slug>.md` con encabezado `# CAPÍTULO X: TÍTULO`.
2. Editar `src/app.py`: agregar el slug en `SECTION_ORDER` y en `SECTION_META` con `label`, `cap`, `status`.
3. Editar `src/convert_md_to_html.py`: agregar a `SECTION_ORDER` también.
4. Verificar visualización en `http://localhost:8000/seccion/<slug>` (Docker debe estar corriendo).

### 6.2 Agregar una nueva referencia bibliográfica

1. Identificar la categoría correcta en `config/refs.bib` (A–K).
2. Agregar la entrada BibTeX al final de su categoría, respetando el formato.
3. Si vas a citar con `[@clave]` (NO recomendado en docs activos): añade el mapeo en:
   - `scripts/purga_referencias.py::MAPEO_APA`
   - `scripts/auditar_referencias.py::MAPEO_INVERSO`
4. Ejecutar `py scripts/auditar_referencias.py` para confirmar integridad.
5. Citar en texto directamente en formato APA: `(Apellido, Año)`.

### 6.3 Migrar `[@clave]` a APA en un nuevo documento

```powershell
py scripts/purga_referencias.py
py scripts/limpia_duplicados.py
py scripts/auditar_referencias.py
```

Revisar la salida del auditor para corregir claves faltantes manualmente.

### 6.4 Ejecutar un experimento E_x (cuando esté implementado)

```powershell
py src/experiments/exp_X_<nombre>.py --seed 42
py src/experiments/exp_X_<nombre>.py --seed 43
# ... 6 semillas
py src/evaluate.py --exp X --report-format markdown > tabla.md
```

Insertar `tabla.md` en la sección correspondiente de `docs/40-capitulo4.md`.

### 6.5 Actualizar el plan después de cerrar un hito

1. Editar `docs/plan-siguientes-pasos.md`: marcar tareas como `✅`.
2. Editar `docs/plan-detallado.md`: actualizar tabla de hitos.
3. Editar `docs/plan-revision-academica-exhaustiva.md`: incrementar criterios verificados.
4. Crear `docs/hito-N-completado.md` con evidencia (capturas, tablas).
5. Actualizar `ia/memory.md` sección 13 (log de eventos).

---

## 7. Anti-patrones y cosas a evitar

### 7.1 De redacción

- ❌ Inventar números o métricas sin haber ejecutado el experimento.
- ❌ Afirmar "primera tesis en X" sin haber documentado búsqueda sistemática.
- ❌ Citar `según el archivo X.md` en cuerpo de tesis.
- ❌ Usar emojis en el cuerpo de la tesis (sí permitidos en planes auxiliares).
- ❌ Frases tipo "obviamente", "claramente", "evidentemente" sin evidencia.
- ❌ Usar `[@clave]` que no se procesa por el visor Flask.

### 7.2 De código

- ❌ Hardcodear API keys o credenciales.
- ❌ Cambiar la semilla 42 sin justificación documentada.
- ❌ Usar versiones flotantes (`>=`) en `requirements.txt` (todo debe ir con `==`).
- ❌ Procesar `tesis.md` o `tesis-v2.md` (son históricos).
- ❌ Modificar el dataset sintético en disco; siempre regenerar con la semilla.

### 7.3 De Git

- ❌ Commit gigante con muchas cosas distintas. Separar por categoría temática.
- ❌ Mensajes de commit cortos sin detalle.
- ❌ Push sin haber ejecutado el auditor de referencias.

### 7.4 De interacción con el usuario

- ❌ Actuar sin haber leído `ia/memory.md`.
- ❌ Asumir contexto que no está documentado.
- ❌ Hacer cambios destructivos (eliminar archivos, hacer reset, push --force) sin confirmación explícita.
- ❌ Generar documentos nuevos cuando se pidió editar uno existente.
- ❌ Cambiar decisiones arquitectónicas documentadas sin discutir.

---

## 8. Cómo escribir prompts internos para subagentes

Si vas a delegar a un subagente (Agent tool), incluye SIEMPRE:

1. **Contexto previo**: el subagente NO tiene tu historial. Hazle un resumen del proyecto en 3-5 líneas referenciando `ia/memory.md`.
2. **Tarea específica**: qué archivo crear/modificar y con qué contenido.
3. **Restricciones**: convenciones APA, lenguaje cuidado con regulaciones, hedging obligatorio.
4. **Verificación**: qué auditar antes de devolver el trabajo.
5. **Formato de salida**: respuesta breve (≤200 palabras) o reporte estructurado.

Ejemplo:
```
Eres un agente de revisión académica. Lee ia/memory.md y ia/agents.md de
d:\tesis_yoset. Tu tarea es: revisar docs/22-capitulo2-marcoteorico.md y
verificar que NO use lenguaje absoluto ("cumple con", "elimina", "siempre")
sobre regulaciones o RAG. Reporta línea por línea las violaciones detectadas
en formato Markdown. No edites el archivo; solo reporta.
```

---

## 9. Estado actual al 2026-05-17 (resumen)

- ✅ 13/19 secciones de la tesis con texto definitivo.
- ✅ Cap I extendido con §1.12 Limitaciones y §1.13 Declaración de intereses.
- ✅ Cap II marco teórico con hedging correcto sobre RAG/EU AI Act.
- ✅ Cap III §3.3 con diseño experimental completo E1–E5, pruebas estadísticas H1a–H1d, baselines B1–B4.
- ✅ Cap IV §4.4 con Discusión Detallada y 5 cruces comparativos (Tablas 4.8–4.12).
- ✅ Anexos A1, A2, A3 con plantillas completas.
- ✅ refs.bib v2.0 con 47 entradas en 11 categorías (purga completada).
- ✅ Scripts de mantenimiento bibliográfico funcionando.
- ✅ Dataset sintético: especificación cerrada + script listo (pendiente ejecutar).
- ✅ Plan-revision: 69/87 criterios verificados.

**Siguiente acción**: ejecutar `pip install -r requirements.txt` y `py src/generate_synthetic_dataset.py` para cerrar Hito 2.

---

## 10. Política de actualización de este documento

Actualizar `ia/agents.md` cuando:
- Se agrega una convención nueva (tabla nueva, prefijo nuevo, etc.).
- Se introduce un patrón anti-recomendado (agregar a §7).
- Se agrega un comando frecuente nuevo (agregar a §4).
- Se cambia un flujo operativo.

Actualizar `ia/memory.md` cuando:
- Cierra un hito.
- Se toma una decisión arquitectónica que afecta el alcance.
- Se agregan documentos nuevos al repositorio.
- Cambia el estado de las secciones de la tesis.

Cada actualización debe llevar la fecha (ISO `YYYY-MM-DD`) en el encabezado y un breve apunte en la sección 13 de `memory.md`.

---

*Documento creado 2026-05-17. Versión 1.0. Mantener vivo a lo largo del proyecto.*
