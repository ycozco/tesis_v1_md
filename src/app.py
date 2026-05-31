#!/usr/bin/env python3
"""
Flask app para servir Markdown de tesis como sitio web interactivo.
Conversión en tiempo real Markdown → HTML con búsqueda, índice dinámico.
"""

from flask import Flask, render_template, jsonify, request
from pathlib import Path
from datetime import datetime
import re
import csv
from collections import Counter

# Importar configuraciones y helpers del proyecto
from constants import (
    MARKDOWN_DIR,
    ENTREGABLE_DIR,
    HTML_DIR,
    SECTION_ORDER,
    SECTION_META
)
from helpers import (
    load_markdown_file,
    count_bib_references,
    count_written_words
)

app = Flask(__name__)

def read_text_if_exists(path):
    """Lee un archivo de texto si existe."""
    path = Path(path)
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding='utf-8')


def parse_checklist_items(text):
    """Extrae items marcados como pendientes y completados."""
    pending = re.findall(r'^\s*-\s*\[\s\]\s*(.+)$', text, re.MULTILINE)
    done = re.findall(r'^\s*-\s*\[[xX]\]\s*(.+)$', text, re.MULTILINE)
    return pending, done


def categorize_review_item(item):
    """Clasifica un item pendiente por tipo de revisión."""
    text = item.lower()
    groups = [
        ("Estructural y capítulos", [
            "capítulo", "capitulo", "anexo", "índice", "indice", "portada",
            "presentación", "presentacion", "glosario", "referencias", "tabla de contenidos"
        ]),
        ("Coherencia académica", [
            "coherencia", "hipótesis", "hipotesis", "objetivo", "variable", "alcance",
            "título", "titulo", "resumen", "abstract"
        ]),
        ("Metodológica y datos", [
            "dataset", "datos", "fuente", "fuentes", "midagri", "senasa", "senamhi",
            "inei", "sunat", "faostat", "comtrade", "método", "metod", "experimento"
        ]),
        ("Bibliográfica y citas", [
            "referencia", "cita", "bib", "doi", "bibliografía", "bibliografia", "paper"
        ]),
        ("Gobernanza y regulación", [
            "sbs", "nist", "regulator", "ley", "ai act", "ds ", "decreto", "cumplimiento",
            "auditor", "ética", "etica"
        ]),
        ("Web y publicación", [
            "web", "html", "docx", "docker", "panel", "dashboard", "publicación", "publicacion"
        ]),
    ]
    for label, keywords in groups:
        if any(keyword in text for keyword in keywords):
            return label
    return "Otros"


def build_admin_snapshot():
    """Construye el estado centralizado del proyecto para el panel admin."""
    md_files = []
    if MARKDOWN_DIR.exists():
        for md_file in sorted(MARKDOWN_DIR.glob('*.md')):
            md_files.append({
                "name": md_file.name,
                "stem": md_file.stem,
                "path": f"/docs/{md_file.stem}",
                "kind": "Markdown",
            })

    extra_files = []
    if ENTREGABLE_DIR.exists():
        for file in sorted(ENTREGABLE_DIR.iterdir()):
            if file.is_file() and not file.name.startswith('.'):
                extra_files.append({
                    "name": file.name,
                    "path": str(file),
                    "kind": file.suffix.lower().lstrip('.') or "file",
                })

    plan_text = read_text_if_exists(MARKDOWN_DIR / 'plan-detallado.md')
    pending_items, done_items = parse_checklist_items(plan_text)
    plan_total = len(pending_items) + len(done_items)
    plan_done = len(done_items)
    plan_pending = len(pending_items)
    plan_progress = round((plan_done / plan_total) * 100, 1) if plan_total else 0.0
    plan_pending_preview = pending_items[:8]

    review_counts = Counter(categorize_review_item(item) for item in pending_items)
    review_types = []
    review_catalog = [
        ("Estructural y capítulos", "Portada, capítulos, anexos, índice y cierre documental."),
        ("Coherencia académica", "Problema, objetivos, hipótesis, alcance y variables."),
        ("Metodológica y datos", "Datasets, fuentes, variables y diseño experimental."),
        ("Bibliográfica y citas", "Citas, bibliografía, DOI y consistencia APA."),
        ("Gobernanza y regulación", "NIST, SBS, DS, ética y trazabilidad."),
        ("Web y publicación", "Panel, HTML, Docker y entrega final."),
        ("Otros", "Pendientes que no encajan en las categorías principales."),
    ]
    for label, description in review_catalog:
        review_types.append({
            "label": label,
            "description": description,
            "count": review_counts.get(label, 0),
        })

    sources_text = read_text_if_exists(ENTREGABLE_DIR / 'fuentes-datos-agroexport.txt')
    dataset_matrix_path = ENTREGABLE_DIR / 'dataset-matrix.csv'
    dataset_rows = []
    if dataset_matrix_path.exists():
        with open(dataset_matrix_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            dataset_rows = list(reader)

    plan_cards = [
        {
            "title": "Estructura completa",
            "value": "22 piezas",
            "note": "Cap. I-V + anexos ya definidos"
        },
        {
            "title": "Checklist en plan detallado",
            "value": f"{plan_done}/{plan_total}",
            "note": f"{plan_progress}% completado"
        },
        {
            "title": "Revisiones pendientes",
            "value": str(plan_pending),
            "note": "Pendientes detectados en el avance"
        },
        {
            "title": "Archivos de entregable",
            "value": str(len(extra_files)),
            "note": "Plan, matriz, decisión y fuentes"
        },
    ]

    return {
        "docs": md_files,
        "deliverables": extra_files,
        "plan_cards": plan_cards,
        "plan_progress": plan_progress,
        "plan_done": plan_done,
        "plan_total": plan_total,
        "plan_pending_preview": plan_pending_preview,
        "review_types": review_types,
        "sources_text": sources_text,
        "dataset_rows": dataset_rows,
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "doc_count": len(md_files),
        "deliverable_count": len(extra_files),
    }


@app.route('/')
def index():
    """Panel de Control (Dashboard) Premium Dinámico."""
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
    progress_pct = round((done / total) * 100) if total else 0
    
    total_refs = count_bib_references()
    total_words = count_written_words()
    
    return render_template(
        'index.html',
        secciones=secciones,
        done=done,
        total=total,
        progress_pct=progress_pct,
        total_refs=total_refs,
        total_words=total_words,
        active_page='inicio'
    )


@app.route('/secciones')
def secciones_index():
    """Panel de progreso por sección."""
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
    return render_template(
        'secciones.html',
        secciones=secciones,
        done=done,
        total=total,
        active_page='secciones'
    )


@app.route('/seccion/<slug>')
def ver_seccion(slug):
    """Sirve una sección individual con navegación prev/next."""
    md_path = MARKDOWN_DIR / f"{slug}.md"
    if not md_path.exists():
        return f"<h2 style='font-family:sans-serif;padding:40px'>Sección <code>{slug}</code> no encontrada — el archivo <code>docs/{slug}.md</code> aún no existe.</h2>", 404

    html_body, toc_html, frontmatter = load_markdown_file(f"{slug}.md")
    meta = SECTION_META.get(slug, {})
    label = meta.get("label", slug.replace("-", " ").title())

    idx = SECTION_ORDER.index(slug) if slug in SECTION_ORDER else -1
    prev_slug = SECTION_ORDER[idx - 1] if idx > 0 else None
    next_slug = SECTION_ORDER[idx + 1] if idx >= 0 and idx < len(SECTION_ORDER) - 1 else None

    prev_label = SECTION_META.get(prev_slug, {}).get("label", "Anterior") if prev_slug else ""
    next_label = SECTION_META.get(next_slug, {}).get("label", "Siguiente") if next_slug else ""

    return render_template(
        'seccion.html',
        title=label,
        html_body=html_body,
        toc_html=toc_html,
        prev_slug=prev_slug,
        next_slug=next_slug,
        prev_label=prev_label,
        next_label=next_label,
        active_page='secciones'
    )


@app.route('/api/seccion/<slug>')
def api_ver_seccion(slug):
    """Retorna el contenido JSON de una sección para previsualización."""
    md_path = MARKDOWN_DIR / f"{slug}.md"
    if not md_path.exists():
        return jsonify({"error": "No encontrado"}), 404
    html_body, toc_html, frontmatter = load_markdown_file(f"{slug}.md")
    meta = SECTION_META.get(slug, {})
    return jsonify({
        "title": meta.get("label", slug),
        "html": html_body,
        "toc": toc_html
    })


@app.route('/propuesta')
def propuesta_solucion():
    """Sirve la página interactiva de la propuesta tecnológica y prototipo."""
    return render_template('propuesta.html', active_page='propuesta')


@app.route('/datos')
def view_data_explorer():
    """Sirve la vista del Explorador de Datasets interactivo."""
    return render_template('datos.html', active_page='datos')


@app.route('/api/data/<key>')
def api_data_explorer(key):
    """Servicio API para leer y estructurar archivos CSV del proyecto."""
    DATA_FILES = {
        "bcrp_exchange": Path('/app/data/bcrp/bcrp-tipo-cambio-mensual.csv'),
        "faostat_prod": Path('/app/data/faostat/faostat-produccion-peru-2024.csv'),
        "sunat_export": Path('/app/data/sunat/sunat-exportacion-sectorial-2026.csv'),
        "synthetic_agro": Path('/app/data/dataset_agro_sintetico_v1.csv'),
        "validated_refs": Path('/app/entregable/referencias-datasets-validadas.csv'),
        "train_raw": Path('/app/data/dataset_processed_train_raw.csv'),
        "train_balanced": Path('/app/data/dataset_processed_train_balanced.csv'),
        "test_processed": Path('/app/data/dataset_processed_test.csv')
    }
    
    if key not in DATA_FILES:
        return jsonify({"error": "Dataset no registrado"}), 404
        
    filepath = DATA_FILES[key]
    if not filepath.exists():
        return jsonify({"error": f"Archivo físico {filepath.name} no encontrado en el servidor. Asegúrese de haberlo generado."}), 404
        
    content = ""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except Exception:
            continue
            
    if not content:
        return jsonify({"error": "No se pudo leer el archivo con ninguna codificación"}), 500
        
    lines = content.split('\n')
    lines = [l for l in lines if l.strip()]
    
    start_index = 0
    if "sunat-exportacion-sectorial" in filepath.name:
        for idx, line in enumerate(lines):
            if "Sector" in line:
                start_index = idx
                break
                
    csv_data = "\n".join(lines[start_index:])
    
    import io
    reader = csv.reader(io.StringIO(csv_data))
    rows = []
    columns = []
    
    try:
        header = next(reader)
        columns = [h.strip() if h.strip() else f"Col_{i}" for i, h in enumerate(header)]
        for r in reader:
            if len(r) == 0:
                continue
            if len(r) < len(columns):
                r = r + [""] * (len(columns) - len(r))
            else:
                r = r[:len(columns)]
            rows.append(dict(zip(columns, r)))
    except Exception as e:
        return jsonify({"error": f"Error parseando CSV: {str(e)}"}), 500
        
    num_rows = len(rows)
    num_cols = len(columns)
    
    null_counts = {}
    for col in columns:
        null_counts[col] = 0
        
    for r in rows:
        for col in columns:
            val = str(r[col]).strip().lower()
            if val in ["", "n.d.", "n/d", "null", "none", "n.a.", "n/a"]:
                null_counts[col] += 1
                
    stats = {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "null_counts": null_counts,
        "filename": filepath.name
    }
    
    return jsonify({
        "columns": columns,
        "rows": rows,
        "stats": stats
    })


@app.route('/admin')
def admin_dashboard():
    """Panel admin centralizado con avance, datos y revisiones."""
    snapshot = build_admin_snapshot()
    return render_template('admin.html', active_page='admin', **snapshot)


@app.route('/docs/<doc_name>')
def view_doc(doc_name):
    """Visualiza documento Markdown."""
    # Buscar archivo (intentando con guiones y guiones bajos para máxima compatibilidad)
    filenames = [doc_name, doc_name.replace('-', '_'), doc_name.replace('_', '-')]
    for filename in filenames:
        for ext in ['.md', '']:
            filepath = MARKDOWN_DIR / f"{filename}{ext}"
            if filepath.exists():
                html_body, toc_html, frontmatter = load_markdown_file(f"{filename}{ext}")
                if html_body:
                    title = frontmatter.get('title', filename.replace('_', ' ').replace('-', ' ').title())
                    author = frontmatter.get('author', 'Sistema de Tesis')
                    # format date
                    current_date = datetime.now().strftime('%d %b, %Y')
                    return render_template(
                        'doc.html',
                        title=title,
                        html_body=html_body,
                        toc_html=toc_html,
                        author=author,
                        date=current_date
                    )
    
    return "Documento no encontrado", 404


@app.route('/health')
def health():
    """Health check para Docker."""
    return jsonify({"status": "healthy"}), 200


@app.route('/api/docs')
def list_docs():
    """Lista documentos y artefactos disponibles."""
    documents = [
        {
            "name": md_file.stem,
            "path": f"/docs/{md_file.stem}"
        }
        for md_file in sorted(MARKDOWN_DIR.glob('*.md'))
    ]
    artifacts = []
    if ENTREGABLE_DIR.exists():
        artifacts = [
            {
                "name": file.name,
                "path": str(file)
            }
            for file in sorted(ENTREGABLE_DIR.iterdir())
            if file.is_file() and not file.name.startswith('.')
        ]
    payload = {"documents": documents, "artifacts": artifacts}
    return jsonify(payload)


@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404."""
    return render_template('404.html'), 404


@app.route('/references')
def view_references():
    """Visualiza la bibliografía completa de forma premium."""
    refs_path = Path('/app/config/refs.bib')
    if not refs_path.exists():
        refs_path = Path('config/refs.bib')
    if not refs_path.exists():
        refs_path = Path('d:/tesis_yoset/config/refs.bib')
        
    if not refs_path.exists():
        return "Archivo de referencias no encontrado", 404
        
    with open(refs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parseo simple de BibTeX
    entries = re.findall(r'@(\w+)\{([^,]+),\s*([^@]+)\}', content, re.DOTALL)
    
    parsed_refs = []
    for type, key, fields_str in entries:
        fields = {}
        for field in re.findall(r'(\w+)\s*=\s*\{([^}]+)\}', fields_str):
            fields[field[0].lower()] = field[1]
        
        parsed_refs.append({
            'key': key,
            'type': type,
            'title': fields.get('title', 'Sin título'),
            'author': fields.get('author', 'Anónimo'),
            'year': fields.get('year', 'N/A'),
            'doi': fields.get('doi', fields.get('url', ''))
        })

    return render_template(
        'references.html',
        parsed_refs=parsed_refs,
        active_page='inicio'
    )


if __name__ == '__main__':
    import glob
    extra_md = glob.glob('/app/docs/*.md')
    if not extra_md:
        extra_md = glob.glob('docs/*.md')
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        extra_files=extra_md
    )
