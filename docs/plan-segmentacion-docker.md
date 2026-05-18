# PLAN DE SEGMENTACIÓN — TESIS EN SECCIONES NUMERADAS CON DOCKER HOT-RELOAD

**Fecha:** 2026-05-17  
**Autor:** Yoset Cozco Mauri  
**Objetivo:** Reemplazar el monolito `docs/tesis.md` (1018 líneas) por archivos numerados independientes que el servidor Flask sirva por sección, con recarga automática al editar cualquier segmento.

---

## 1. Por qué segmentar

| Problema del monolito | Solución segmentada |
|-----------------------|---------------------|
| Editar Cap IV requiere abrir 1 000 líneas | Editar solo `40-capitulo4.md` (~100 líneas) |
| Flask recarga TODO cuando cambia un párrafo | Flask recarga solo el segmento modificado |
| Git diff ilegible — un commit toca todo | Commits atómicos por sección |
| No se puede trabajar en paralelo (2 personas) | Cada sección es un archivo independiente |
| Panel admin muestra un solo archivo | Panel muestra progreso por sección con estado |

---

## 2. Estructura de archivos objetivo

```
docs/
├── 00-portada.md              ← Portada, dedicatoria, agradecimientos, presentación
├── 01-resumen.md              ← Resumen (ES) + Abstract (EN)
├── 02-indices.md              ← Índices de contenidos, figuras, tablas, fórmulas
├── 03-introduccion.md         ← Introducción
├── 10-capitulo1.md            ← Cap I completo §1.1-§1.11
├── 20-capitulo2-antecedentes.md   ← §2.1 (7 antecedentes)
├── 21-capitulo2-estadoarte.md     ← §2.2 (5 batallas + Tablas 2.1 y 2.2)
├── 22-capitulo2-marcoteorico.md   ← §2.3 (§2.3.1-§2.3.9)
├── 30-capitulo3.md            ← Cap III §3.1-§3.3
├── 40-capitulo4.md            ← Cap IV §4.1-§4.3  🔴 PENDIENTE
├── 50-capitulo5.md            ← Cap V §5.1-§5.3   🔴 PENDIENTE
├── 60-conclusiones.md         ← Conclusiones (ES) + Conclusions (EN)  🔴 PENDIENTE
├── 70-recomendaciones.md      ← Recomendaciones
├── 80-glosario.md             ← Glosario de términos
├── 90-referencias.md          ← Referencias bibliográficas (lista APA)
├── A1-anexo-usabilidad.md     ← Anexo A — Protocolo de usabilidad  🔴 PENDIENTE
├── A2-anexo-modelcards.md     ← Anexo B — Model Cards              🔴 PENDIENTE
├── A3-anexo-datasheet.md      ← Anexo C — Datasheet del dataset    🔴 PENDIENTE
└── A4-anexo-ia.md             ← Anexo D — Registro uso IA
```

**Convención de nombres:**
- `NN-nombre.md` — prefijo numérico de 2 dígitos (00–90) para secciones principales
- `AN-nombre.md` — prefijo alfanumérico para anexos (A1, A2, A3, A4)
- Los gaps en la numeración (00, 01, 10, 20, 21...) permiten insertar nuevas secciones sin renombrar las existentes

---

## 3. Mapa de migración — líneas de `tesis.md` → archivo destino

| Archivo destino | Contenido | Líneas aprox. en tesis.md | Estado |
|----------------|-----------|--------------------------|--------|
| `00-portada.md` | Portada, dedicatoria, agradecimientos, presentación | 1–60 | ✅ Listo para extraer |
| `01-resumen.md` | Resumen + Abstract | 63–84 | ✅ Listo para extraer |
| `02-indices.md` | Índice contenidos, figuras, tablas, fórmulas | 87–159 | ✅ Listo para extraer |
| `03-introduccion.md` | Introducción completa | 161–173 | ✅ Listo para extraer |
| `10-capitulo1.md` | Cap I §1.1-§1.11 | 175–389 | ✅ Listo para extraer |
| `20-capitulo2-antecedentes.md` | §2.1 completo | 391–440 | ✅ Listo para extraer |
| `21-capitulo2-estadoarte.md` | §2.2 completo + tablas | 441–531 | ✅ Listo para extraer |
| `22-capitulo2-marcoteorico.md` | §2.3.1-§2.3.9 | 532–656 | ✅ Listo para extraer |
| `30-capitulo3.md` | Cap III §3.1-§3.3 | 658–712 | ✅ Listo para extraer |
| `40-capitulo4.md` | Cap IV §4.1-§4.3 | 714–740 | 🔴 Solo placeholder — requiere resultados experimentales |
| `50-capitulo5.md` | Cap V §5.1-§5.3 | 742–756 | 🔴 Solo placeholder — depende de Cap IV |
| `60-conclusiones.md` | Conclusiones ES + EN | 764–791 | 🔴 Solo plantilla — depende de Cap IV |
| `70-recomendaciones.md` | Recomendaciones 1–5 | 794–805 | ✅ Listo para extraer |
| `80-glosario.md` | Glosario completo | 808–861 | ✅ Listo para extraer |
| `90-referencias.md` | Lista bibliográfica APA | 864–967 | ✅ Listo para extraer |
| `A1-anexo-usabilidad.md` | Protocolo usabilidad | 972–990 | 🔴 Skeleton — completar |
| `A2-anexo-modelcards.md` | Model Cards | 993–999 | 🔴 Skeleton — completar |
| `A3-anexo-datasheet.md` | Datasheet dataset | 1003–1006 | 🔴 Skeleton — completar |
| `A4-anexo-ia.md` | Registro uso IA | 1009–1014 | ✅ Listo para extraer |

---

## 4. Cambios al servidor Flask (`src/app.py`)

### 4.1 Nueva constante: orden de secciones

Agregar en la parte superior del archivo, después de `MARKDOWN_DIR`:

```python
# Orden canónico de secciones para ensamblado y navegación
SECTION_ORDER = [
    "00-portada",
    "01-resumen",
    "02-indices",
    "03-introduccion",
    "10-capitulo1",
    "20-capitulo2-antecedentes",
    "21-capitulo2-estadoarte",
    "22-capitulo2-marcoteorico",
    "30-capitulo3",
    "40-capitulo4",
    "50-capitulo5",
    "60-conclusiones",
    "70-recomendaciones",
    "80-glosario",
    "90-referencias",
    "A1-anexo-usabilidad",
    "A2-anexo-modelcards",
    "A3-anexo-datasheet",
    "A4-anexo-ia",
]

SECTION_META = {
    "00-portada":                  {"label": "Portada",              "cap": None,  "status": "done"},
    "01-resumen":                  {"label": "Resumen / Abstract",   "cap": None,  "status": "done"},
    "02-indices":                  {"label": "Índices",              "cap": None,  "status": "done"},
    "03-introduccion":             {"label": "Introducción",         "cap": None,  "status": "done"},
    "10-capitulo1":                {"label": "Capítulo I",           "cap": "I",   "status": "done"},
    "20-capitulo2-antecedentes":   {"label": "Cap. II — §2.1",      "cap": "II",  "status": "done"},
    "21-capitulo2-estadoarte":     {"label": "Cap. II — §2.2",      "cap": "II",  "status": "done"},
    "22-capitulo2-marcoteorico":   {"label": "Cap. II — §2.3",      "cap": "II",  "status": "done"},
    "30-capitulo3":                {"label": "Capítulo III",         "cap": "III", "status": "done"},
    "40-capitulo4":                {"label": "Capítulo IV",          "cap": "IV",  "status": "pending"},
    "50-capitulo5":                {"label": "Capítulo V",           "cap": "V",   "status": "pending"},
    "60-conclusiones":             {"label": "Conclusiones",         "cap": None,  "status": "pending"},
    "70-recomendaciones":          {"label": "Recomendaciones",      "cap": None,  "status": "done"},
    "80-glosario":                 {"label": "Glosario",             "cap": None,  "status": "done"},
    "90-referencias":              {"label": "Referencias",          "cap": None,  "status": "done"},
    "A1-anexo-usabilidad":        {"label": "Anexo A",              "cap": "A",   "status": "pending"},
    "A2-anexo-modelcards":        {"label": "Anexo B",              "cap": "B",   "status": "pending"},
    "A3-anexo-datasheet":         {"label": "Anexo C",              "cap": "C",   "status": "pending"},
    "A4-anexo-ia":                {"label": "Anexo D",              "cap": "D",   "status": "done"},
}
```

### 4.2 Nueva ruta: índice de secciones con progreso

```python
@app.route('/secciones')
def secciones_index():
    """Lista todas las secciones con estado de avance."""
    secciones = []
    for slug in SECTION_ORDER:
        meta = SECTION_META.get(slug, {})
        md_path = MARKDOWN_DIR / f"{slug}.md"
        exists = md_path.exists()
        size = md_path.stat().st_size if exists else 0
        secciones.append({
            "slug": slug,
            "label": meta.get("label", slug),
            "status": meta.get("status", "unknown"),
            "exists": exists,
            "size_kb": round(size / 1024, 1),
            "url": f"/seccion/{slug}",
        })
    done = sum(1 for s in secciones if s["status"] == "done" and s["exists"])
    total = len(secciones)
    return render_template_string(SECCIONES_TEMPLATE, secciones=secciones, done=done, total=total)
```

### 4.3 Nueva ruta: vista de sección individual con navegación anterior/siguiente

```python
@app.route('/seccion/<slug>')
def ver_seccion(slug):
    """Sirve una sección individual con navegación prev/next."""
    md_path = MARKDOWN_DIR / f"{slug}.md"
    if not md_path.exists():
        return f"Sección '{slug}' no encontrada — el archivo {slug}.md no existe aún.", 404

    html_body, toc_html, frontmatter = load_markdown_file(f"{slug}.md")
    meta = SECTION_META.get(slug, {})
    label = meta.get("label", slug)

    # Navegación prev/next
    idx = SECTION_ORDER.index(slug) if slug in SECTION_ORDER else -1
    prev_slug = SECTION_ORDER[idx - 1] if idx > 0 else None
    next_slug = SECTION_ORDER[idx + 1] if idx >= 0 and idx < len(SECTION_ORDER) - 1 else None

    return generate_section_page(label, html_body, toc_html, prev_slug, next_slug)
```

### 4.4 Función `generate_section_page` con barra de navegación

```python
def generate_section_page(title, html_body, toc_html, prev_slug=None, next_slug=None):
    prev_link = f'<a href="/seccion/{prev_slug}" class="nav-btn">← {SECTION_META.get(prev_slug,{}).get("label","Anterior")}</a>' if prev_slug else ""
    next_link = f'<a href="/seccion/{next_slug}" class="nav-btn">{SECTION_META.get(next_slug,{}).get("label","Siguiente")} →</a>' if next_slug else ""
    # ... retorna HTML con la barra prev/next + TOC sidebar
```

### 4.5 Watcher de archivos para hot-reload por sección

Agregar en `entrypoint.sh`, antes de iniciar Flask:

```bash
# Instalar watchdog si no está instalado
pip install -q watchdog

# Iniciar Flask con reloader activo (detecta cambios en /app/docs/*.md)
export FLASK_ENV=development
exec python3 -u /app/src/app.py
```

En `app.py`, al final, usar `extra_files` de Flask para vigilar todos los MD:

```python
if __name__ == '__main__':
    import glob
    extra_md = glob.glob('/app/docs/*.md')
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        extra_files=extra_md   # Flask recarga al editar cualquier .md
    )
```

---

## 5. Cambios a `convert_md_to_html.py`

Reemplazar la lista fija `files_to_convert` por generación dinámica basada en `SECTION_ORDER`:

```python
# En main():
files_to_convert = [
    (f'/app/docs/{slug}.md', f'{slug}.html')
    for slug in SECTION_ORDER
    if Path(f'/app/docs/{slug}.md').exists()
]
```

Agregar función para generar HTML combinado (tesis completa en un solo HTML):

```python
def convert_all_to_combined(output_path='/app/output/tesis-completa.html'):
    """Combina todas las secciones en un único HTML para revisión o impresión."""
    combined_md = ""
    for slug in SECTION_ORDER:
        md_path = Path(f'/app/docs/{slug}.md')
        if md_path.exists():
            content = md_path.read_text(encoding='utf-8')
            # Saltar frontmatter YAML del primer archivo
            if content.startswith('---'):
                lines = content.split('\n')
                end = next((i for i in range(1, len(lines)) if lines[i].startswith('---')), -1)
                content = '\n'.join(lines[end + 1:]) if end != -1 else content
            combined_md += content + "\n\n---\n\n"
    # ... convertir combined_md a HTML
```

---

## 6. Cambios al `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y pandoc && rm -rf /var/lib/apt/lists/*

COPY config/requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Montar docs/ como volumen (no COPY) para hot-reload
# Los archivos se leen en tiempo real desde el volumen

COPY src/ /app/src/
COPY config/ /app/config/
RUN chmod +x /app/src/entrypoint.sh

EXPOSE 8000

CMD ["/app/src/entrypoint.sh"]
```

En `config/requirements-docker.txt`, agregar:

```
watchdog>=3.0.0
```

---

## 7. Cambios al `docker-compose.yml`

```yaml
services:
  thesis-viewer:
    build: .
    container_name: tesis-web-viewer
    ports:
      - "8000:8000"
    volumes:
      - ./docs:/app/docs          # Hot-reload: editar .md → Flask lo detecta
      - ./entregable:/app/entregable
      - ./config/refs.bib:/app/config/refs.bib
      - ./config/apa.csl:/app/config/apa.csl
      - ./output:/app/output
      - ./formato:/app/formato
    environment:
      - FLASK_ENV=development     # Cambiar a development para hot-reload
      - FLASK_APP=/app/src/app.py
      - FLASK_DEBUG=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Resultado:** Al editar cualquier archivo en `docs/`, Flask detecta el cambio y recarga. El volumen montado garantiza que los cambios del host se reflejan instantáneamente dentro del contenedor.

---

## 8. Panel de progreso por sección (nueva ruta `/secciones`)

La ruta `/secciones` mostrará una tabla tipo kanban con:

| Sección | Archivo | Estado | Tamaño | Acciones |
|---------|---------|--------|--------|----------|
| Portada | 00-portada.md | ✅ Completo | 3.2 KB | Ver |
| Resumen | 01-resumen.md | ✅ Completo | 1.8 KB | Ver |
| Cap IV | 40-capitulo4.md | 🔴 Pendiente | 0.8 KB | Ver / Editar |
| Anexo A | A1-anexo-usabilidad.md | 🔴 Pendiente | 0.6 KB | Ver / Editar |

Progreso global: `11/19 secciones completas (58%)`

---

## 9. Tareas de migración — paso a paso

### Tarea 9.1 — Extraer secciones completadas de `tesis.md` (prioridad alta)

Estas secciones solo necesitan ser copiadas del monolito al archivo correspondiente:

| Paso | Comando Git recomendado | Verificación |
|------|------------------------|--------------|
| 9.1.1 | Crear `docs/00-portada.md` con líneas 1–60 de `tesis.md` | `docker-compose up` → visitar `/seccion/00-portada` |
| 9.1.2 | Crear `docs/01-resumen.md` con líneas 63–84 | Verificar que resumen y abstract aparecen completos |
| 9.1.3 | Crear `docs/02-indices.md` con líneas 87–159 | Tablas de índices renderizan correctamente |
| 9.1.4 | Crear `docs/03-introduccion.md` con líneas 161–173 | Citas bibliográficas visibles |
| 9.1.5 | Crear `docs/10-capitulo1.md` con líneas 175–389 | Tabla cronograma y tabla de instrumentos correctas |
| 9.1.6 | Crear `docs/20-capitulo2-antecedentes.md` con líneas 391–440 | 7 antecedentes presentes |
| 9.1.7 | Crear `docs/21-capitulo2-estadoarte.md` con líneas 441–531 | Tablas 2.1 y 2.2 con formato correcto |
| 9.1.8 | Crear `docs/22-capitulo2-marcoteorico.md` con líneas 532–656 | Fórmulas LaTeX renderizan (ver nota abajo) |
| 9.1.9 | Crear `docs/30-capitulo3.md` con líneas 658–712 | Diagrama ASCII del pipeline visible |
| 9.1.10 | Crear `docs/70-recomendaciones.md` con líneas 794–805 | 5 recomendaciones numeradas |
| 9.1.11 | Crear `docs/80-glosario.md` con líneas 808–861 | Términos en negrita + definición |
| 9.1.12 | Crear `docs/90-referencias.md` con líneas 864–967 | Lista bibliográfica APA completa |
| 9.1.13 | Crear `docs/A4-anexo-ia.md` con líneas 1009–1014 | Texto de uso de IA presente |

> **Nota sobre fórmulas LaTeX:** El servidor actual usa Python `markdown` que no renderiza LaTeX. Para mostrar fórmulas matemáticas (`$...$`), agregar `markdown-katex` o usar MathJax vía CDN en el template HTML de `app.py`. Ver Tarea 9.3.

### Tarea 9.2 — Crear secciones pendientes (esqueletos mínimos)

Crear archivos con estructura mínima para que el servidor no devuelva 404:

**`docs/40-capitulo4.md`** — placeholder hasta tener resultados experimentales:

```markdown
# CAPÍTULO IV: RESULTADOS Y DISCUSIÓN

> **Estado:** Pendiente — requiere dataset sintético + experimentos (Fases 1-3 del plan de implementación)

## 4.1 Resultados Cuantitativos (Predicción y Detección)

*(Se completará con: tabla E1 — GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente) vs. baseline, tabla E2 — detector único vs. ensemble)*

## 4.2 Resultados Cualitativos (Generación de Reportes LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)-RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación))

*(Se completará con: 2-3 reportes generados + evaluación ROUGE-1)*

## 4.3 Discusión de Resultados

*(Se completará con: análisis de H1a-H1d, comparativa con literatura)*
```

**`docs/50-capitulo5.md`**, **`docs/60-conclusiones.md`** — mismo patrón de placeholder.

**`docs/A1-anexo-usabilidad.md`**, **`docs/A2-anexo-modelcards.md`**, **`docs/A3-anexo-datasheet.md`** — completar con contenido definitivo en Fase 4 del plan de implementación.

### Tarea 9.3 — Habilitar renderizado de fórmulas matemáticas

En `app.py`, en la función `generate_html_page`, agregar MathJax en el `<head>`:

```python
# Agregar al template HTML del <head>:
MATHJAX_SCRIPT = """
<script>
  MathJax = {
    tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
    svg: { fontCache: 'global' }
  };
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
"""
```

### Tarea 9.4 — Verificar que `tesis.md` monolítico puede eliminarse

Una vez que los 19 archivos de sección existan y sean verificados vía Docker, `docs/tesis.md` puede archivarse (mover a `docs/archive/tesis-monolito.md`) o eliminarse. El servidor Flask usará las secciones individuales.

---

## 10. Checklist de implementación

### Fase A — Infraestructura (completar antes de migrar contenido)

- [ ] A1: Agregar `SECTION_ORDER` y `SECTION_META` a `src/app.py`
- [ ] A2: Crear ruta `/secciones` con panel de progreso
- [ ] A3: Crear ruta `/seccion/<slug>` con navegación prev/next
- [ ] A4: Actualizar `extra_files` en `app.run()` para hot-reload
- [ ] A5: Cambiar `FLASK_ENV=development` en `docker-compose.yml`
- [ ] A6: Agregar MathJax al template HTML (para fórmulas de §2.3)
- [ ] A7: Actualizar `convert_md_to_html.py` para usar `SECTION_ORDER`
- [ ] A8: `docker-compose build && docker-compose up` — verificar que servidor inicia
- [ ] A9: Visitar `http://localhost:8000/secciones` — debe mostrar tabla vacía

### Fase B — Migración de secciones completadas (sin cambiar contenido)

- [ ] B01: Crear `docs/00-portada.md` — verificar en `/seccion/00-portada`
- [ ] B02: Crear `docs/01-resumen.md` — verificar en `/seccion/01-resumen`
- [ ] B03: Crear `docs/02-indices.md` — verificar en `/seccion/02-indices`
- [ ] B04: Crear `docs/03-introduccion.md` — verificar en `/seccion/03-introduccion`
- [ ] B05: Crear `docs/10-capitulo1.md` — verificar tabla cronograma
- [ ] B06: Crear `docs/20-capitulo2-antecedentes.md` — 7 antecedentes OK
- [ ] B07: Crear `docs/21-capitulo2-estadoarte.md` — 2 tablas comparativas OK
- [ ] B08: Crear `docs/22-capitulo2-marcoteorico.md` — fórmulas con MathJax OK
- [ ] B09: Crear `docs/30-capitulo3.md` — diagrama ASCII + tabla datasets OK
- [ ] B10: Crear `docs/70-recomendaciones.md`
- [ ] B11: Crear `docs/80-glosario.md`
- [ ] B12: Crear `docs/90-referencias.md`
- [ ] B13: Crear `docs/A4-anexo-ia.md`

### Fase C — Placeholders para secciones pendientes

- [ ] C1: Crear `docs/40-capitulo4.md` con placeholder claro
- [ ] C2: Crear `docs/50-capitulo5.md` con placeholder claro
- [ ] C3: Crear `docs/60-conclusiones.md` con plantilla
- [ ] C4: Crear `docs/A1-anexo-usabilidad.md` con skeleton
- [ ] C5: Crear `docs/A2-anexo-modelcards.md` con skeleton
- [ ] C6: Crear `docs/A3-anexo-datasheet.md` con skeleton

### Fase D — Verificación final

- [ ] D1: `http://localhost:8000/secciones` muestra 19/19 archivos, 13 verdes y 6 rojos
- [ ] D2: Navegación prev/next funciona en todas las secciones
- [ ] D3: Editar cualquier `docs/XX-*.md` → el servidor recarga sin reiniciar Docker
- [ ] D4: `/seccion/22-capitulo2-marcoteorico` muestra fórmulas matemáticas renderizadas
- [ ] D5: `docs/tesis.md` archivado en `docs/archive/` — ya no es el archivo activo

---

## 11. Flujo de trabajo cotidiano (después de la segmentación)

```
1. docker-compose up -d          # inicia el servidor en background
2. Abrir http://localhost:8000/secciones   # ver estado de secciones
3. Editar docs/40-capitulo4.md   # escribir resultados del experimento
4. Guardar el archivo             # Flask detecta el cambio automáticamente
5. Recargar http://localhost:8000/seccion/40-capitulo4   # ver los cambios
6. git add docs/40-capitulo4.md && git commit -m "cap4: agregar tabla E1 GBDT vs baseline"
```

No es necesario reiniciar Docker ni correr scripts de compilación. El servidor sirve el archivo actualizado en el próximo request.

---

## 12. Sección de pendientes agrupados por prioridad

### Prioridad 1 — Bloqueantes (necesarios para que el sistema funcione)

| ID | Tarea | Archivo a modificar |
|----|-------|---------------------|
| P1.1 | Agregar `SECTION_ORDER` + `SECTION_META` | `src/app.py` |
| P1.2 | Agregar ruta `/seccion/<slug>` | `src/app.py` |
| P1.3 | Agregar `extra_files` en `app.run()` | `src/app.py` |
| P1.4 | Cambiar `FLASK_ENV=development` | `docker-compose.yml` |

### Prioridad 2 — Migración de contenido existente

| ID | Tarea | Fuente | Destino |
|----|-------|--------|---------|
| P2.1 | Extraer Cap I | `tesis.md` líneas 175–389 | `docs/10-capitulo1.md` |
| P2.2 | Extraer §2.1 | `tesis.md` líneas 391–440 | `docs/20-capitulo2-antecedentes.md` |
| P2.3 | Extraer §2.2 | `tesis.md` líneas 441–531 | `docs/21-capitulo2-estadoarte.md` |
| P2.4 | Extraer §2.3 | `tesis.md` líneas 532–656 | `docs/22-capitulo2-marcoteorico.md` |
| P2.5 | Extraer Cap III | `tesis.md` líneas 658–712 | `docs/30-capitulo3.md` |

### Prioridad 3 — Contenido nuevo (requiere experimentos)

| ID | Tarea | Descripción | Depende de |
|----|-------|-------------|------------|
| P3.1 | Escribir Cap IV §4.1 | Tablas E1 y E2 con resultados reales | Dataset sintético + código |
| P3.2 | Escribir Cap IV §4.2 | Reportes de ejemplo generados por RAG | Módulo 4 implementado |
| P3.3 | Escribir Cap IV §4.3 | Discusión de H1a-H1d | P3.1 + P3.2 |
| P3.4 | Escribir Cap V | Conclusiones, limitaciones, trabajos futuros | P3.3 |
| P3.5 | Completar Conclusiones | ES + EN con métricas reales | P3.4 |

### Prioridad 4 — Completar Anexos

| ID | Tarea | Descripción |
|----|-------|-------------|
| P4.1 | Anexo A — Protocolo usabilidad | Cuestionario final + tareas cronometradas |
| P4.2 | Anexo B — Model Cards XGBoost | Especificaciones, limitaciones, usos |
| P4.3 | Anexo B — Model Cards Ensemble | Umbrales, sensibilidad, comparativa |
| P4.4 | Anexo B — Model Cards LLM+RAG | Modelo base, restricciones, ROUGE |
| P4.5 | Anexo C — Datasheet sintético | Motivación, composición, sesgos, licencias |

---

*Plan generado 2026-05-17. Actualizar el checklist en las secciones 10 y 12 a medida que se completan las tareas.*
