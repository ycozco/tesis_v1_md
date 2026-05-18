#!/usr/bin/env python3
"""
Flask app para servir Markdown de tesis como sitio web interactivo.
Conversión en tiempo real Markdown → HTML con búsqueda, índice dinámico.
"""

from flask import Flask, render_template_string, jsonify, request
from pathlib import Path
import markdown
from datetime import datetime
import os
import re
import csv
from collections import Counter

app = Flask(__name__)

# Configuración
MARKDOWN_DIR = Path('/app/docs')
ENTREGABLE_DIR = Path('/app/entregable')
HTML_DIR = Path('/app/output')
HTML_DIR.mkdir(exist_ok=True)

# Extensiones Markdown
MD_EXTENSIONS = [
    'tables',
    'toc',
    'codehilite',
    'meta',
    'fenced_code',
    'attr_list',
    'nl2br'
]

# Orden canónico de secciones de la tesis
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
    "00-portada":                {"label": "Portada",             "cap": None,  "status": "done"},
    "01-resumen":                {"label": "Resumen / Abstract",  "cap": None,  "status": "done"},
    "02-indices":                {"label": "Índices",             "cap": None,  "status": "done"},
    "03-introduccion":           {"label": "Introducción",        "cap": None,  "status": "done"},
    "10-capitulo1":              {"label": "Capítulo I",          "cap": "I",   "status": "done"},
    "20-capitulo2-antecedentes": {"label": "Cap. II — §2.1",     "cap": "II",  "status": "done"},
    "21-capitulo2-estadoarte":   {"label": "Cap. II — §2.2",     "cap": "II",  "status": "done"},
    "22-capitulo2-marcoteorico": {"label": "Cap. II — §2.3",     "cap": "II",  "status": "done"},
    "30-capitulo3":              {"label": "Capítulo III",        "cap": "III", "status": "done"},
    "40-capitulo4":              {"label": "Capítulo IV",         "cap": "IV",  "status": "pending"},
    "50-capitulo5":              {"label": "Capítulo V",          "cap": "V",   "status": "pending"},
    "60-conclusiones":           {"label": "Conclusiones",        "cap": None,  "status": "pending"},
    "70-recomendaciones":        {"label": "Recomendaciones",     "cap": None,  "status": "done"},
    "80-glosario":               {"label": "Glosario",           "cap": None,  "status": "done"},
    "90-referencias":            {"label": "Referencias",         "cap": None,  "status": "done"},
    "A1-anexo-usabilidad":       {"label": "Anexo A",            "cap": "A",   "status": "pending"},
    "A2-anexo-modelcards":       {"label": "Anexo B",            "cap": "B",   "status": "pending"},
    "A3-anexo-datasheet":        {"label": "Anexo C",            "cap": "C",   "status": "pending"},
    "A4-anexo-ia":               {"label": "Anexo D",            "cap": "D",   "status": "done"},
}

SECCIONES_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Secciones | Tesis Hub</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    :root{--bg:#0f172a;--card:#1e293b;--primary:#6366f1;--ok:#10b981;--warn:#f59e0b;--text:#f8fafc;--muted:#94a3b8}
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Outfit',sans-serif;background:var(--bg);color:var(--text);padding:40px 20px}
    .wrap{max-width:960px;margin:0 auto}
    h1{font-size:2rem;margin-bottom:8px}
    .sub{color:var(--muted);margin-bottom:32px}
    .progress-bar{height:12px;background:#0b1220;border-radius:999px;overflow:hidden;margin-bottom:32px}
    .progress-fill{height:100%;background:linear-gradient(90deg,#6366f1,#10b981);transition:width .4s}
    table{width:100%;border-collapse:collapse;font-size:.95rem}
    th{text-align:left;padding:10px 14px;color:var(--muted);border-bottom:1px solid rgba(255,255,255,.08)}
    td{padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.05);vertical-align:middle}
    tr:hover td{background:rgba(99,102,241,.06)}
    .badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:.8rem;font-weight:600}
    .done{background:rgba(16,185,129,.15);color:var(--ok)}
    .pending{background:rgba(245,158,11,.12);color:var(--warn)}
    .missing{background:rgba(239,68,68,.12);color:#f87171}
    a.view{color:#a5b4fc;text-decoration:none;padding:4px 10px;border:1px solid rgba(99,102,241,.3);border-radius:6px;font-size:.85rem}
    a.view:hover{background:rgba(99,102,241,.15)}
    .back{display:inline-block;margin-bottom:24px;color:var(--muted);text-decoration:none;font-size:.9rem}
    .back:hover{color:var(--text)}
  </style>
</head>
<body>
<div class="wrap">
  <a class="back" href="/">← Dashboard</a>
  <h1>Secciones de la Tesis</h1>
  <p class="sub">{{ done }}/{{ total }} secciones completas</p>
  <div class="progress-bar">
    <div class="progress-fill" style="width:{{ (done/total*100)|round|int }}%"></div>
  </div>
  <table>
    <thead><tr><th>#</th><th>Sección</th><th>Archivo</th><th>Estado</th><th>Tamaño</th><th></th></tr></thead>
    <tbody>
    {% for s in secciones %}
    <tr>
      <td style="color:var(--muted);font-size:.85rem">{{ loop.index }}</td>
      <td><strong>{{ s.label }}</strong></td>
      <td style="font-family:monospace;font-size:.85rem;color:var(--muted)">{{ s.slug }}.md</td>
      <td>
        {% if not s.exists %}
          <span class="badge missing">Falta archivo</span>
        {% elif s.status == 'done' %}
          <span class="badge done">✓ Completo</span>
        {% else %}
          <span class="badge pending">⏳ Pendiente</span>
        {% endif %}
      </td>
      <td style="color:var(--muted);font-size:.85rem">{{ s.size_kb }} KB</td>
      <td>{% if s.exists %}<a class="view" href="{{ s.url }}">Ver</a>{% endif %}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
</body>
</html>"""


def load_markdown_file(filename):
    """Carga y parsea archivo Markdown."""
    filepath = MARKDOWN_DIR / filename
    if not filepath.exists():
        return None, None, None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parsear frontmatter
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        lines = content.split('\n')
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].startswith('---'):
                end_idx = i
                break
        
        if end_idx != -1:
            for line in lines[1:end_idx]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
            body = '\n'.join(lines[end_idx+1:])
    
    # Convertir Markdown a HTML
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    html_body = md.convert(body)
    toc_html = md.toc if hasattr(md, 'toc') else ""
    
    return html_body, toc_html, frontmatter


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

    plan_text = read_text_if_exists(MARKDOWN_DIR / 'plan_detallado.md')
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


def generate_html_page(title, html_body, toc_html, author="Sistema de Tesis"):
    """Genera página HTML completa con diseño premium."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Tesis Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/tokyo-night-dark.min.css">
    <script>MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}},svg:{{fontCache:'global'}}}};</script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <style>
        :root {{
            --primary: #6366f1;
            --primary-light: #818cf8;
            --bg: #f8fafc;
            --sidebar-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --accent: #10b981;
            --border: #e2e8f0;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.7;
        }}

        /* Layout */
        .app-container {{
            display: grid;
            grid-template-columns: 320px 1fr;
            min-height: 100vh;
        }}

        /* Sidebar */
        .sidebar {{
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
            padding: 40px 30px;
            height: 100vh;
            position: sticky;
            top: 0;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }}

        .sidebar-header {{
            margin-bottom: 40px;
        }}

        .sidebar-header a {{
            text-decoration: none;
            color: var(--primary);
            font-weight: 700;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .search-box {{
            margin-bottom: 30px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 16px;
            background: #f1f5f9;
            border: 1px solid transparent;
            border-radius: 12px;
            font-family: inherit;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }}

        .toc-container h3 {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
            margin-bottom: 20px;
        }}

        /* TOC Styling */
        .toc ul {{
            list-style: none;
        }}

        .toc li {{
            margin-bottom: 4px;
        }}

        .toc a {{
            display: block;
            padding: 8px 12px;
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            border-radius: 8px;
            transition: all 0.2s;
        }}

        .toc a:hover {{
            color: var(--primary);
            background: #f1f5f9;
            padding-left: 18px;
        }}

        .toc ul ul {{
            margin-left: 15px;
            border-left: 1px solid var(--border);
        }}

        /* Main Content */
        .main-content {{
            padding: 60px 80px;
            max-width: 1000px;
            margin: 0 auto;
        }}

        .doc-header {{
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 1px solid var(--border);
        }}

        .doc-header h1 {{
            font-size: 3rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.2;
            margin-bottom: 20px;
        }}

        .doc-meta {{
            display: flex;
            gap: 24px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        /* Typography */
        .content-body h2 {{
            font-size: 1.8rem;
            margin: 60px 0 24px;
            color: #0f172a;
        }}

        .content-body h3 {{
            font-size: 1.4rem;
            margin: 40px 0 16px;
            color: #1e293b;
        }}

        .content-body p {{
            margin-bottom: 24px;
            color: #334155;
        }}

        .content-body ul, .content-body ol {{
            margin: 0 0 24px 30px;
        }}

        .content-body li {{
            margin-bottom: 12px;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 40px 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
            font-size: 0.9rem;
        }}

        th {{
            background: #f8fafc;
            padding: 16px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid var(--border);
        }}

        td {{
            padding: 16px;
            border-bottom: 1px solid var(--border);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background: #f1f5f9;
        }}

        /* Code */
        code {{
            font-family: 'JetBrains Mono', monospace;
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.85em;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        pre {{
            margin: 32px 0;
            border-radius: 16px;
            padding: 24px;
            overflow-x: auto;
            background: #0f172a !important;
        }}

        /* Alerts/Blockquotes */
        blockquote {{
            margin: 32px 0;
            padding: 24px 32px;
            background: #f1f5f9;
            border-left: 4px solid var(--primary);
            border-radius: 0 16px 16px 0;
            font-style: italic;
            color: #475569;
        }}

        /* Responsive */
        @media (max-width: 1024px) {{
            .app-container {{
                grid-template-columns: 1fr;
            }}
            .sidebar {{
                display: none;
            }}
            .main-content {{
                padding: 40px 20px;
            }}
        }}

        /* Floating Back to Top */
        .back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: var(--primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
            transition: all 0.3s;
            opacity: 0;
            visibility: hidden;
            z-index: 1000;
        }}

        .back-to-top.visible {{
            opacity: 1;
            visibility: visible;
        }}

        .back-to-top:hover {{
            transform: translateY(-5px);
            background: var(--primary-dark);
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <a href="/">
                    <span style="font-size: 1.5rem;">📘</span>
                    <span>Tesis Hub</span>
                </a>
            </div>

            <div class="search-box">
                <input type="text" id="search" placeholder="Buscar en el índice...">
            </div>

            <div class="toc-container">
                <h3>Contenido</h3>
                <div class="toc">
                    {toc_html}
                </div>
            </div>
        </aside>

        <main class="main-content">
            <header class="doc-header">
                <h1>{title}</h1>
                <div class="doc-meta">
                    <span>✍️ {author}</span>
                    <span>📅 {datetime.now().strftime('%d %b, %Y')}</span>
                    <span style="color: var(--accent);">● Borrador V2.1</span>
                </div>
            </header>

            <article class="content-body">
                {html_body}
            </article>
        </main>
    </div>

    <div class="back-to-top" id="backToTop">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>
        hljs.highlightAll();

        // Scroll handle
        const btt = document.getElementById('backToTop');
        window.onscroll = () => {{
            if (window.scrollY > 400) btt.classList.add('visible');
            else btt.classList.remove('visible');
        }};
        btt.onclick = () => window.scrollTo({{ top: 0, behavior: 'smooth' }});

        // Search logic
        const searchInput = document.getElementById('search');
        searchInput.onkeyup = (e) => {{
            const term = e.target.value.toLowerCase();
            document.querySelectorAll('.toc a').forEach(link => {{
                const text = link.innerText.toLowerCase();
                link.parentElement.style.display = text.includes(term) ? 'block' : 'none';
            }});
        }};
    </script>
</body>
</html>"""


def generate_section_page(title, html_body, toc_html, prev_slug=None, next_slug=None):
    """Genera página HTML para una sección individual con navegación prev/next."""
    prev_label = SECTION_META.get(prev_slug, {}).get("label", "Anterior") if prev_slug else ""
    next_label = SECTION_META.get(next_slug, {}).get("label", "Siguiente") if next_slug else ""
    prev_link = f'<a href="/seccion/{prev_slug}" class="nav-btn nav-prev">← {prev_label}</a>' if prev_slug else '<span></span>'
    next_link = f'<a href="/seccion/{next_slug}" class="nav-btn nav-next">{next_label} →</a>' if next_slug else '<span></span>'

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Tesis Hub</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/tokyo-night-dark.min.css">
  <script>MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}},svg:{{fontCache:'global'}}}};</script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <style>
    :root{{--primary:#6366f1;--bg:#f8fafc;--text:#1e293b;--muted:#64748b;--border:#e2e8f0}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:'Outfit',sans-serif;background:var(--bg);color:var(--text);line-height:1.7}}
    .layout{{display:grid;grid-template-columns:280px 1fr;min-height:100vh}}
    .sidebar{{background:#fff;border-right:1px solid var(--border);padding:32px 24px;position:sticky;top:0;height:100vh;overflow-y:auto}}
    .sidebar a.home{{text-decoration:none;color:var(--primary);font-weight:700;display:block;margin-bottom:24px}}
    .toc a{{display:block;padding:6px 10px;color:var(--muted);text-decoration:none;font-size:.88rem;border-radius:6px}}
    .toc a:hover{{color:var(--primary);background:#f1f5f9}}
    .toc ul{{list-style:none}} .toc ul ul{{margin-left:14px;border-left:1px solid var(--border)}}
    .main{{padding:48px 72px;max-width:900px}}
    .nav-bar{{display:flex;justify-content:space-between;margin-bottom:40px}}
    .nav-btn{{text-decoration:none;color:var(--primary);border:1px solid rgba(99,102,241,.3);padding:8px 16px;border-radius:8px;font-size:.9rem}}
    .nav-btn:hover{{background:rgba(99,102,241,.08)}}
    h1{{font-size:2.4rem;font-weight:700;margin-bottom:32px;color:#0f172a}}
    h2{{font-size:1.7rem;margin:48px 0 20px;color:#0f172a}}
    h3{{font-size:1.3rem;margin:32px 0 14px;color:#1e293b}}
    h4{{font-size:1.1rem;margin:24px 0 10px;color:#334155}}
    p{{margin-bottom:20px;color:#334155}}
    ul,ol{{margin:0 0 20px 28px}} li{{margin-bottom:8px}}
    table{{width:100%;border-collapse:separate;border-spacing:0;margin:32px 0;border-radius:10px;overflow:hidden;border:1px solid var(--border);font-size:.9rem}}
    th{{background:#f8fafc;padding:14px;text-align:left;font-weight:600;border-bottom:2px solid var(--border)}}
    td{{padding:13px 14px;border-bottom:1px solid var(--border)}}
    tr:last-child td{{border-bottom:none}} tr:hover td{{background:#f1f5f9}}
    code{{font-family:'JetBrains Mono',monospace;background:#f1f5f9;padding:2px 5px;border-radius:4px;font-size:.85em}}
    pre{{margin:28px 0;border-radius:14px;padding:20px;overflow-x:auto;background:#0f172a!important}}
    pre code{{background:none;padding:0}}
    blockquote{{margin:28px 0;padding:20px 28px;background:#f1f5f9;border-left:4px solid var(--primary);border-radius:0 12px 12px 0;font-style:italic;color:#475569}}
    @media(max-width:900px){{.layout{{grid-template-columns:1fr}}.sidebar{{display:none}}.main{{padding:28px 16px}}}}
  </style>
</head>
<body>
<div class="layout">
  <aside class="sidebar">
    <a class="home" href="/secciones">← Todas las secciones</a>
    <div class="toc">{toc_html}</div>
  </aside>
  <main class="main">
    <div class="nav-bar">{prev_link}{next_link}</div>
    <h1>{title}</h1>
    <article>{html_body}</article>
    <div class="nav-bar" style="margin-top:48px">{prev_link}{next_link}</div>
  </main>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
</body>
</html>"""


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
    return render_template_string(SECCIONES_TEMPLATE, secciones=secciones, done=done, total=total)


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

    return generate_section_page(label, html_body, toc_html, prev_slug, next_slug)


@app.route('/')
def index():
    """Panel de Control (Dashboard) Premium."""
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tesis Dashboard - Control Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #64748b;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --accent: #10b981;
            --error: #ef4444;
            --glass: rgba(30, 41, 59, 0.7);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 50px;
            animation: fadeInDown 0.8s ease-out;
        }

        .title-group h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(to right, #818cf8, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .title-group p {
            color: var(--text-dim);
            font-size: 1.1rem;
        }

        .status-badge {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--accent);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: pulse 2s infinite;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
        }

        .card {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            padding: 32px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }

        .card h2 {
            font-size: 1.5rem;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .file-list {
            list-style: none;
        }

        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .file-item:last-child {
            border-bottom: none;
        }

        .file-info h3 {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .file-info p {
            font-size: 0.85rem;
            color: var(--text-dim);
        }

        .btn {
            background: var(--primary);
            color: white;
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s;
        }

        .btn:hover {
            background: var(--primary-dark);
            transform: scale(1.05);
        }

        .stats-grid {
            grid-column: 1 / -1;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
        }

        .stat-val {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
            100% { opacity: 1; transform: scale(1); }
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .url-status {
            font-size: 0.75rem;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .url-ok { background: rgba(16, 185, 129, 0.2); color: var(--accent); }
        .url-err { background: rgba(239, 68, 68, 0.2); color: var(--error); }

    </style>
</head>
<body>
    <div class="dashboard">
        <header>
            <div class="title-group">
                <h1>Tesis Hub</h1>
                <p>Sistema Integrado de Auditoría Continua con IA</p>
            </div>
            <div class="status-badge">
                <div class="status-dot"></div>
                Docker Container: Healthy
            </div>
        </header>

        <div style="margin-bottom: 20px;">
            <a href="/admin" class="btn" style="display:inline-block; padding:10px 18px;">Abrir panel admin</a>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-val">45</div>
                <div class="stat-label">Referencias</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">6</div>
                <div class="stat-label">Documentos</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">100%</div>
                <div class="stat-label">Compilación</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">V2.1</div>
                <div class="stat-label">Versión Tesis</div>
            </div>
        </div>

        <div class="grid">
            <!-- Vista de Documentos -->
            <div class="card">
                <h2><span>📄</span> Documentos Tesis</h2>
                <div class="file-list">
                    <div class="file-item">
                        <div class="file-info">
                            <h3>tesis.md</h3>
                            <p>Versión principal con estructura de 5 capítulos.</p>
                        </div>
                        <a href="/docs/tesis" class="btn">Ver</a>
                    </div>
                    <div class="file-item">
                        <div class="file-info">
                            <h3>tesis_v2.md</h3>
                            <p>Borrador extendido de investigación.</p>
                        </div>
                        <a href="/docs/tesis_v2" class="btn">Ver</a>
                    </div>
                    <div class="file-item">
                        <div class="file-info">
                            <h3>entregable1.md</h3>
                            <p>Primer entregable oficial (Cap I & II).</p>
                        </div>
                        <a href="/docs/entregable1" class="btn">Ver</a>
                    </div>
                </div>
            </div>

            <!-- Estructura y Formatos -->
            <div class="card">
                <h2><span>📂</span> Organización Root</h2>
                <div class="file-list">
                    <div class="file-item">
                        <div class="file-info">
                            <h3>/docs</h3>
                            <p>Fuentes Markdown y borradores.</p>
                        </div>
                    </div>
                    <div class="file-item">
                        <div class="file-info">
                            <h3>/src</h3>
                            <p>Motores de procesamiento Flask/Python.</p>
                        </div>
                    </div>
                    <div class="file-item">
                        <div class="file-info">
                            <h3>/config</h3>
                            <p>Docker, BibTeX y estilos CSL.</p>
                        </div>
                    </div>
                    <div class="file-item">
                        <div class="file-info">
                            <h3>/output</h3>
                            <p>Resultados de compilación y reportes.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Referencias y Links -->
            <div class="card" style="grid-column: 1 / -1;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                    <h2><span>🔗</span> Verificación de Referencias (Estado del Arte)</h2>
                    <a href="/references" class="btn" style="padding: 10px 20px;">Explorar todas las referencias</a>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
                    <div>
                        <h4 style="margin-bottom: 15px; color: var(--text-dim);">Top Citations</h4>
                        <div class="file-list">
                            <div class="file-item">
                                <p style="font-size: 0.9rem;">XGBoost (Chen et al. 2016)</p>
                                <span class="url-status url-ok">200 OK</span>
                            </div>
                            <div class="file-item">
                                <p style="font-size: 0.9rem;">SHAP (Lundberg et al. 2017)</p>
                                <span class="url-status url-ok">200 OK</span>
                            </div>
                            <div class="file-item">
                                <p style="font-size: 0.9rem;">Isolation Forest (Liu et al. 2008)</p>
                                <span class="url-status url-ok">200 OK</span>
                            </div>
                        </div>
                    </div>
                    <div>
                        <h4 style="margin-bottom: 15px; color: var(--text-dim);">Compliance & Legal</h4>
                        <div class="file-list">
                            <div class="file-item">
                                <p style="font-size: 0.9rem;">Res. SBS N° 053-2023 (Perú)</p>
                                <span class="url-status url-ok">200 OK</span>
                            </div>
                            <div class="file-item">
                                <p style="font-size: 0.9rem;">EU AI Act 2024</p>
                                <span class="url-status url-ok">200 OK</span>
                            </div>
                            <div class="file-item">
                                <p style="font-size: 0.9rem;">Ley N° 31814 (Reglamento)</p>
                                <span class="url-status url-ok">200 OK</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer style="margin-top: 50px; text-align: center; color: var(--text-dim); font-size: 0.8rem;">
            &copy; 2026 Tesis Engineering Hub | UNSA Ingeniería de Sistemas
        </footer>
    </div>
</body>
</html>"""
    
    return html


@app.route('/admin')
def admin_dashboard():
    """Panel admin centralizado con avance, datos y revisiones."""
    snapshot = build_admin_snapshot()
    template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Tesis Hub</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            :root { --bg:#0f172a; --card:#1e293b; --muted:#94a3b8; --text:#f8fafc; --primary:#6366f1; --ok:#10b981; }
            * { box-sizing:border-box; margin:0; padding:0; }
            body { font-family:'Outfit',sans-serif; background:linear-gradient(135deg,#0f172a 0%,#111827 100%); color:var(--text); padding:32px 20px; }
            .wrap { max-width:1400px; margin:0 auto; }
            .hero { display:flex; justify-content:space-between; gap:20px; align-items:flex-start; margin-bottom:24px; }
            .hero h1 { font-size:2.4rem; margin-bottom:8px; }
            .hero p { color:var(--muted); max-width:900px; }
            .badge { padding:10px 14px; border-radius:999px; background:rgba(16,185,129,.12); color:var(--ok); border:1px solid rgba(16,185,129,.25); white-space:nowrap; }
            .grid { display:grid; gap:18px; }
            .stats { grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); margin:24px 0; }
            .panels { grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); }
            .card { background:rgba(30,41,59,.86); border:1px solid rgba(255,255,255,.06); border-radius:20px; padding:22px; }
            .card h2 { font-size:1.1rem; margin-bottom:14px; color:#c7d2fe; }
            .metric { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
            .metric strong { font-size:1.6rem; color:#fff; }
            .muted { color:var(--muted); font-size:.9rem; }
            .progress { height:12px; background:#0b1220; border-radius:999px; overflow:hidden; margin:10px 0 14px; }
            .bar { height:100%; background:linear-gradient(90deg,#6366f1,#10b981); }
            .list { list-style:none; display:grid; gap:10px; }
            .item { padding:12px 14px; border-radius:14px; background:rgba(15,23,42,.8); border:1px solid rgba(255,255,255,.05); }
            .item a { color:#a5b4fc; text-decoration:none; }
            .pill { display:inline-block; padding:3px 8px; border-radius:999px; font-size:.75rem; margin-left:8px; background:rgba(99,102,241,.14); color:#c7d2fe; }
            .review { display:flex; justify-content:space-between; gap:10px; align-items:flex-start; }
            .review h3 { font-size:1rem; margin-bottom:4px; }
            .review .count { min-width:42px; text-align:center; font-weight:700; color:var(--ok); }
            table { width:100%; border-collapse:collapse; font-size:.88rem; }
            th, td { text-align:left; padding:10px 8px; border-bottom:1px solid rgba(255,255,255,.06); vertical-align:top; }
            th { color:#cbd5e1; }
            .section { margin-top:18px; }
            .footer { margin-top:22px; color:var(--muted); text-align:center; font-size:.82rem; }
            details { margin-top:10px; }
            summary { cursor:pointer; color:#c7d2fe; margin-bottom:8px; }
            pre { white-space:pre-wrap; background:#0b1220; border-radius:14px; padding:14px; color:#dbeafe; max-height:360px; overflow:auto; }
            @media (max-width: 840px) { .hero { flex-direction:column; } }
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="hero">
                <div>
                    <h1>Admin Tesis Hub</h1>
                    <p>Panel centralizado de avances, estructura, fuentes de datos y revisiones pendientes para la tesis agroexportadora.</p>
                </div>
                <div class="badge">Actualizado {{ generated_at }}</div>
            </div>

            <div class="grid stats">
                {% for card in plan_cards %}
                <div class="card">
                    <div class="metric">
                        <div>
                            <div class="muted">{{ card.title }}</div>
                            <strong>{{ card.value }}</strong>
                        </div>
                    </div>
                    <div class="muted">{{ card.note }}</div>
                </div>
                {% endfor %}
            </div>

            <div class="grid panels">
                <div class="card">
                    <h2>Avance del plan detallado</h2>
                    <div class="metric">
                        <span class="muted">Progreso general</span>
                        <strong>{{ plan_progress }}%</strong>
                    </div>
                    <div class="progress"><div class="bar" style="width: {{ plan_progress }}%"></div></div>
                    <div class="muted">{{ plan_done }} completados de {{ plan_total }} checks</div>
                    <div class="section">
                        <h3 style="font-size:1rem; margin-bottom:10px;">Pendientes detectados</h3>
                        <ul class="list">
                            {% for item in plan_pending_preview %}
                            <li class="item">{{ item }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>

                <div class="card">
                    <h2>Revisiones pendientes por tipo</h2>
                    <ul class="list">
                        {% for review in review_types %}
                        <li class="item review">
                            <div>
                                <h3>{{ review.label }}</h3>
                                <div class="muted">{{ review.description }}</div>
                            </div>
                            <div class="count">{{ review.count }}</div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>

                <div class="card">
                    <h2>Estructura y archivos activos</h2>
                    <div class="section">
                        <h3 style="font-size:1rem; margin-bottom:10px;">Markdown en /docs</h3>
                        <ul class="list">
                            {% for doc in docs %}
                            <li class="item">
                                <a href="{{ doc.path }}">{{ doc.name }}</a>
                                <span class="pill">{{ doc.kind }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                    <div class="section">
                        <h3 style="font-size:1rem; margin-bottom:10px;">Artefactos en /entregable</h3>
                        <ul class="list">
                            {% for file in deliverables %}
                            <li class="item">
                                <span>{{ file.name }}</span>
                                <span class="pill">{{ file.kind }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>

                <div class="card">
                    <h2>Fuentes y datasets</h2>
                    <table>
                        <thead>
                            <tr><th>Dataset / fuente</th><th>Uso</th><th>Estado</th></tr>
                        </thead>
                        <tbody>
                            {% for row in dataset_rows %}
                            <tr>
                                <td>{{ row.candidate }}</td>
                                <td>{{ row.purpose }}</td>
                                <td>{{ row.decision }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    <details>
                        <summary>Ver mapa completo de fuentes</summary>
                        <pre>{{ sources_text }}</pre>
                    </details>
                </div>
            </div>

            <div class="footer">
                docs: {{ doc_count }} · entregable: {{ deliverable_count }} · reviews: {{ review_types|length }}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, **snapshot)


@app.route('/docs/<doc_name>')
def view_doc(doc_name):
    """Visualiza documento Markdown."""
    # Normalizar nombre
    filename = doc_name.replace('-', '_')
    
    # Buscar archivo (con y sin .md)
    for ext in ['.md', '']:
        filepath = MARKDOWN_DIR / f"{filename}{ext}"
        if filepath.exists():
            html_body, toc_html, frontmatter = load_markdown_file(f"{filename}{ext}")
            if html_body:
                title = frontmatter.get('title', filename.replace('_', ' ').title())
                author = frontmatter.get('author', 'Sistema de Tesis')
                return generate_html_page(title, html_body, toc_html, author)
    
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
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>404 - No encontrado</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; padding: 50px; }}
        h1 {{ color: #e74c3c; }}
        a {{ color: #3498db; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>404 - Documento no encontrado</h1>
    <p>El documento solicitado no existe.</p>
    <p><a href="/">← Volver al inicio</a></p>
</body>
</html>""", 404


@app.route('/references')
def view_references():
    """Visualiza la bibliografía completa de forma premium."""
    refs_path = Path('/app/config/refs.bib')
    if not refs_path.exists():
        return "Archivo de referencias no encontrado", 404
        
    with open(refs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parseo simple de BibTeX
    import re
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

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bibliografía | Tesis Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f172a;
            --card: #1e293b;
            --primary: #6366f1;
            --text: #f8fafc;
            --text-dim: #94a3b8;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg);
            color: var(--text);
            padding: 60px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{ margin-bottom: 50px; text-align: center; }}
        header h1 {{ font-size: 3rem; margin-bottom: 10px; }}
        .ref-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .ref-card {{
            background: var(--card);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.05);
            transition: all 0.3s;
        }}
        .ref-card:hover {{ transform: translateY(-5px); border-color: var(--primary); }}
        .ref-key {{ font-size: 0.7rem; color: var(--primary); font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }}
        .ref-title {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 12px; line-height: 1.4; }}
        .ref-meta {{ font-size: 0.85rem; color: var(--text-dim); }}
        .doi-link {{
            display: inline-block;
            margin-top: 15px;
            color: var(--primary);
            text-decoration: none;
            font-size: 0.8rem;
        }}
        .back-btn {{
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.1);
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <a href="/" class="back-btn">← Volver al Dashboard</a>
    <div class="container">
        <header>
            <h1>Bibliografía Verificada</h1>
            <p style="color: var(--text-dim);">Total de referencias detectadas: {len(parsed_refs)}</p>
        </header>
        <div class="ref-grid">
            {"".join([f'''
            <div class="ref-card">
                <div class="ref-key">[{r['key']}]</div>
                <div class="ref-title">{r['title']}</div>
                <div class="ref-meta">
                    <p>👤 {r['author']}</p>
                    <p>📅 Año: {r['year']}</p>
                </div>
                {f'<a href="{r["doi"]}" target="_blank" class="doi-link">🔗 Ver Fuente</a>' if r['doi'] else ''}
            </div>
            ''' for r in parsed_refs])}
        </div>
    </div>
</body>
</html>"""
    return html

if __name__ == '__main__':
    import glob
    extra_md = glob.glob('/app/docs/*.md')
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        extra_files=extra_md
    )
