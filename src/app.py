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
    "a1-anexo-usabilidad",
    "a2-anexo-modelcards",
    "a3-anexo-datasheet",
    "a4-anexo-ia",
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
    "a1-anexo-usabilidad":       {"label": "Anexo A",            "cap": "A",   "status": "pending"},
    "a2-anexo-modelcards":       {"label": "Anexo B",            "cap": "B",   "status": "pending"},
    "a3-anexo-datasheet":        {"label": "Anexo C",            "cap": "C",   "status": "pending"},
    "a4-anexo-ia":               {"label": "Anexo D",            "cap": "D",   "status": "done"},
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
    
    /* Navigation Bar Styles */
    .main-navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(30, 41, 59, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 12px 24px;
      margin-bottom: 30px;
    }
    .nav-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      font-size: 1.15rem;
      color: #fff;
    }
    .logo-dot {
      width: 8px;
      height: 8px;
      background: var(--ok);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--ok);
      animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
      0% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.2); opacity: 0.7; }
      100% { transform: scale(1); opacity: 1; }
    }
    .nav-menu {
      display: flex;
      gap: 8px;
    }
    .nav-item {
      color: var(--muted);
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 0.9rem;
      font-weight: 600;
      transition: all 0.2s ease;
    }
    .nav-item:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.04);
    }
    .nav-item.active {
      color: #fff;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.25);
    }

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
  </style>
</head>
<body>
<div class="wrap">
  <!-- Main Navbar -->
  <nav class="main-navbar">
    <div class="nav-logo">
      <span class="logo-dot"></span>
      <span class="logo-text">Tesis Hub</span>
    </div>
    <div class="nav-menu">
      <a href="/" class="nav-item">🏠 Inicio</a>
      <a href="/secciones" class="nav-item active">📖 Secciones</a>
      <a href="/datos" class="nav-item">🗃️ Datos</a>
      <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
      <a href="/admin" class="nav-item">⚙️ Administración</a>
    </div>
  </nav>

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

        /* ==================================================
           ESTILOS ACADÉMICOS PARA IMPRESIÓN Y EXPORTACIÓN PDF
           ================================================== */
        @media print {{
            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            
            body {{
                background: white !important;
                color: #000000 !important;
                font-family: 'Times New Roman', Times, serif !important;
                font-size: 12pt !important;
                line-height: 1.6 !important;
            }}
            
            .sidebar, .back-to-top, .doc-header, .search-box {{
                display: none !important;
            }}
            
            .app-container {{
                display: block !important;
                width: 100% !important;
            }}
            
            .main-content {{
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
                width: 100% !important;
                box-shadow: none !important;
            }}
            
            h1, h2, h3, h4, h5, h6 {{
                color: #000000 !important;
                font-family: 'Times New Roman', Times, serif !important;
                page-break-after: avoid;
            }}
            
            h1 {{
                page-break-before: always;
                font-size: 16pt !important;
                text-align: center;
                margin-top: 0 !important;
                margin-bottom: 24pt !important;
                font-weight: bold;
            }}
            
            h2 {{
                page-break-before: always;
                font-size: 14pt !important;
                margin-top: 24pt !important;
                margin-bottom: 12pt !important;
                font-weight: bold;
            }}
            
            h3 {{
                font-size: 12pt !important;
                margin-top: 18pt !important;
                margin-bottom: 6pt !important;
                font-weight: bold;
            }}
            
            p {{
                margin-bottom: 12pt !important;
                text-align: justify;
                text-indent: 1.25cm; /* Sangría de primera línea estilo APA 7 */
            }}
            
            /* Excepciones a la sangría en dedicatorias, agradecimientos, resumen y títulos */
            .doc-header h1, h1 + p, h2 + p, h3 + p, blockquote p, .center-text p {{
                text-indent: 0 !important;
            }}
            
            table {{
                page-break-inside: avoid;
                font-size: 10pt !important;
                width: 100% !important;
                border: 1px solid #000000 !important;
                border-collapse: collapse !important;
                margin: 20px 0 !important;
            }}
            
            th, td {{
                border: 1px solid #000000 !important;
                padding: 8px 12px !important;
                color: #000000 !important;
                background: none !important;
            }}
            
            th {{
                background-color: #f2f2f2 !important;
                font-weight: bold !important;
                border-bottom: 2px solid #000000 !important;
            }}
            
            tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}
            
            blockquote {{
                border-left: 3px solid #000 !important;
                background: none !important;
                margin: 1.5cm !important;
                padding: 0 0 0 0.5cm !important;
                font-size: 11pt !important;
                font-style: italic;
            }}
            
            /* Render de fórmulas matemáticas */
            .MathJax {{
                font-size: 10pt !important;
            }}
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
    
    /* Navigation Bar Styles */
    .main-navbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(30, 41, 59, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 12px 24px;
      margin-bottom: 30px;
    }}
    .nav-logo {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      font-size: 1.15rem;
      color: #fff;
    }}
    .logo-dot {{
      width: 8px;
      height: 8px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 10px #10b981;
      animation: pulse-dot 2s infinite;
    }}
    @keyframes pulse-dot {{
      0% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.2); opacity: 0.7; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}
    .nav-menu {{
      display: flex;
      gap: 8px;
    }}
    .nav-item {{
      color: var(--muted);
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 0.9rem;
      font-weight: 600;
      transition: all 0.2s ease;
    }}
    .nav-item:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.04);
    }}
    .nav-item.active {{
      color: #fff;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.25);
    }}

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
    <!-- Main Navbar -->
    <nav class="main-navbar" style="background: #1e293b; border-color: rgba(255, 255, 255, 0.1);">
      <div class="nav-logo">
        <span class="logo-dot"></span>
        <span class="logo-text">Tesis Hub</span>
      </div>
      <div class="nav-menu">
        <a href="/" class="nav-item">🏠 Inicio</a>
        <a href="/secciones" class="nav-item active">📖 Secciones</a>
        <a href="/datos" class="nav-item">🗃️ Datos</a>
        <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
        <a href="/admin" class="nav-item">⚙️ Administración</a>
      </div>
    </nav>

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



def count_bib_references():
    """Cuenta dinámicamente las entradas del archivo refs.bib."""
    for path_str in ['/app/config/refs.bib', 'config/refs.bib', 'd:/tesis_yoset/config/refs.bib']:
        path = Path(path_str)
        if path.exists():
            try:
                content = path.read_text(encoding='utf-8')
                entries = re.findall(r'@[a-zA-Z]+\s*\{', content)
                return len(entries)
            except Exception:
                pass
    return 45  # fallback

def count_written_words():
    """Cuenta el total de palabras en los archivos Markdown individuales."""
    words = 0
    try:
        # Intentar con ruta relativa y absoluta
        dirs = [MARKDOWN_DIR, Path('docs'), Path('d:/tesis_yoset/docs')]
        for d in dirs:
            if d.exists():
                for md_file in d.glob('*.md'):
                    if md_file.name in ['tesis.md', 'tesis-v2.md', 'README.md']:
                        continue
                    content = md_file.read_text(encoding='utf-8')
                    words += len(re.findall(r'\w+', content))
                break
    except Exception:
        pass
    return words if words > 0 else 24850

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
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tesis Dashboard - Control Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            securityLevel: 'loose',
            themeVariables: {{
                background: '#1e293b',
                primaryColor: '#6366f1',
                primaryTextColor: '#fff',
                lineColor: '#cbd5e1'
            }}
        }});
    </script>
    <script>MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}},svg:{{fontCache:'global'}}}};</script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <style>
        :root {{
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
            --border: rgba(255, 255, 255, 0.08);
        }}

        /* Navigation Bar Styles */
        .main-navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 12px 24px;
            margin-bottom: 30px;
        }}
        .nav-logo {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 1.15rem;
            color: #fff;
        }}
        .logo-dot {{
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: pulse-dot 2s infinite;
        }}
        @keyframes pulse-dot {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.2); opacity: 0.7; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        .nav-menu {{
            display: flex;
            gap: 8px;
        }}
        .nav-item {{
            color: var(--text-dim);
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .nav-item:hover {{
            color: #fff;
            background: rgba(255, 255, 255, 0.04);
        }}
        .nav-item.active {{
            color: #fff;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.25);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 40px 20px;
        }}

        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            animation: fadeInDown 0.8s ease-out;
        }}

        .title-group h1 {{
            font-size: 2.3rem;
            font-weight: 700;
            background: linear-gradient(to right, #818cf8, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }}

        .title-group p {{
            color: var(--text-dim);
            font-size: 1.05rem;
        }}

        .status-badge {{
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--accent);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .status-dot {{
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: pulse 2s infinite;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: var(--glass);
            border: 1px solid var(--border);
            padding: 24px;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(12px);
        }}

        .stat-val {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-light);
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 4px;
        }}

        .stat-label {{
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}

        .grid-dashboard {{
            display: grid;
            grid-template-columns: 7fr 6fr;
            gap: 24px;
            margin-bottom: 30px;
        }}

        .card-dash {{
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 28px;
        }}

        .card-dash h2 {{
            font-size: 1.35rem;
            margin-bottom: 20px;
            color: #c7d2fe;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
        }}

        /* Table Matrix Style */
        .matrix-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}

        .matrix-table th {{
            text-align: left;
            padding: 10px 12px;
            color: var(--text-dim);
            border-bottom: 1px solid var(--border);
            font-size: 0.8rem;
            text-transform: uppercase;
        }}

        .matrix-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            vertical-align: middle;
        }}

        .matrix-table tr:hover td {{
            background: rgba(99, 102, 241, 0.05);
        }}

        .badge-status {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .badge-done {{ background: rgba(16, 185, 129, 0.15); color: var(--accent); }}
        .badge-pending {{ background: rgba(245, 158, 11, 0.12); color: var(--text-dim); }}
        .badge-missing {{ background: rgba(239, 68, 68, 0.12); color: var(--error); }}

        .btn-sm {{
            display: inline-block;
            background: rgba(99, 102, 241, 0.15);
            color: #fff;
            text-decoration: none;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: all 0.2s;
            cursor: pointer;
        }}

        .btn-sm:hover {{
            background: var(--primary);
            border-color: var(--primary);
        }}

        .sidebar-right {{
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}

        .mermaid-container {{
            background: #1e293b;
            border-radius: 16px;
            padding: 16px;
            overflow-x: auto;
            border: 1px solid var(--border);
        }}

        /* Sliding Preview Panel Drawer */
        .drawer-overlay {{
            position: fixed;
            top: 0;
            right: -620px;
            width: 600px;
            height: 100vh;
            background: #111827;
            border-left: 1px solid var(--border);
            box-shadow: -10px 0 35px rgba(0,0,0,0.6);
            z-index: 2000;
            transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding: 30px;
            overflow-y: auto;
        }}
        .drawer-overlay.active {{
            right: 0;
        }}
        .drawer-close-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            color: #fff;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin-bottom: 25px;
            font-family: inherit;
            transition: all 0.2s;
        }}
        .drawer-close-btn:hover {{
            background: var(--error);
            border-color: var(--error);
        }}
        .drawer-content-body {{
            color: #f3f4f6;
            font-size: 0.95rem;
            line-height: 1.7;
        }}
        .drawer-content-body table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.85rem;
            border: 1px solid var(--border);
        }}
        .drawer-content-body th, .drawer-content-body td {{
            padding: 8px 12px;
            border: 1px solid var(--border);
        }}
        .drawer-content-body th {{
            background: rgba(255,255,255,0.03);
            text-align: left;
        }}

        @keyframes pulse {{
            0% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.1); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}

        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <!-- Main Navbar -->
        <nav class="main-navbar">
            <div class="nav-logo">
                <span class="logo-dot"></span>
                <span class="logo-text">Tesis Hub</span>
            </div>
            <div class="nav-menu">
                <a href="/" class="nav-item active">🏠 Inicio</a>
                <a href="/secciones" class="nav-item">📖 Secciones</a>
                <a href="/datos" class="nav-item">🗃️ Datos</a>
                <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
                <a href="/admin" class="nav-item">⚙️ Administración</a>
            </div>
        </nav>

        <header>
            <div class="title-group">
                <h1>Tesis Dashboard</h1>
                <p>Sistema Inteligente de Supervisión Operativa con IA Explicable, RAG y LLM en Agroexportación</p>
            </div>
            <div class="status-badge">
                <div class="status-dot"></div>
                Docker Container: Active (Hot-Reload)
            </div>
        </header>

        <!-- Metrics Row -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-val">{progress_pct}%</div>
                <div class="stat-label">Progreso Redacción</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">{total_words:,}</div>
                <div class="stat-label">Palabras Escritas</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">{total_refs}</div>
                <div class="stat-label">Referencias (refs.bib)</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">Fase 2</div>
                <div class="stat-label">Fase Actual</div>
            </div>
        </div>

        <div class="grid-dashboard">
            <!-- Left: Sections Progress Matrix -->
            <div class="card-dash">
                <h2><span>📖</span> Matriz de Avance - Tesis Completa</h2>
                <div style="max-height: 980px; overflow-y: auto;">
                    <table class="matrix-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Sección / Capítulo</th>
                                <th>Estado</th>
                                <th>Tamaño</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            """
    for i, s in enumerate(secciones, 1):
        if not s["exists"]:
            status_html = '<span class="badge-status badge-missing">Falta archivo</span>'
            btn_html = ""
        else:
            if s["status"] == "done":
                status_html = '<span class="badge-status badge-done">✓ Completo</span>'
            else:
                status_html = '<span class="badge-status badge-pending">⏳ Pendiente</span>'
            btn_html = f'<button onclick="openSectionPreview(\'{s["slug"]}\')" class="btn-sm">Vista Previa</button>'

        html += f"""
                            <tr>
                                <td style="color:var(--text-dim); font-size:0.8rem;">{i:02d}</td>
                                <td><strong>{s["label"]}</strong><div style="font-size:0.75rem; color:var(--text-dim); font-family:monospace;">{s["slug"]}.md</div></td>
                                <td>{status_html}</td>
                                <td style="color:var(--text-dim); font-family:monospace; font-size:0.8rem;">{s["size_kb"]} KB</td>
                                <td style="text-align:right;">{btn_html}</td>
                            </tr>
        """
    html += """
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Right Sidebar: Gantt & Complete Dataflow -->
            <div class="sidebar-right">
                <!-- Gantt container -->
                <div class="card-dash" style="padding: 20px;">
                    <h2><span>📅</span> Cronograma (Mayo - Diciembre)</h2>
                    <div class="mermaid-container">
                        <div class="mermaid">
                            gantt
                                title Cronograma de Tesis 2026
                                dateFormat  YYYY-MM
                                section Desarrollo
                                F1: Datos (Mayo)           :active, a1, 2026-05, 1m
                                F2: Backend (Jun-Jul)      : a2, 2026-06, 2m
                                F3: RAG/SHAP (Agosto)      : a3, 2026-08, 1m
                                F4: UI & Pipeline (Sept)   : a4, 2026-09, 1m
                                section Validación
                                F5: Usabilidad (Oct)       : a5, 2026-10, 1m
                                F6: Robustez (Nov)         : a6, 2026-11, 1m
                                section Cierre
                                F7: Redacción (Nov)        : a7, after a5, 1m
                                F8: Defensa (Dic)          : a8, 2026-12, 1w
                        </div>
                    </div>
                </div>

                <!-- Complete 6-stage Dataflow Diagram -->
                <div class="card-dash" style="padding: 20px;">
                    <h2><span>⚙️</span> Flujo de Datos del Sistema (Capas 1-6)</h2>
                    <div class="mermaid-container">
                        <div class="mermaid">
                            graph TD
                                classDef step fill:#1e293b,stroke:#6366f1,stroke-width:2px,color:#fff;
                                classDef data fill:#0f172a,stroke:#38bdf8,stroke-width:1px,color:#38bdf8;
                                classDef accent fill:#312e81,stroke:#10b981,stroke-width:2px,color:#d1fae5;

                                subgraph S1 [1. Tratamiento de Datos]
                                    A[Datos Transaccionales]:::data --> B[Limpieza y Normalización]:::step
                                    B --> C[KNN Imputation / Mediana]:::step
                                    C --> D[Transformación e Ingeniería Variables]:::step
                                end
                                
                                subgraph S2 [2. Ensemble Inteligente]
                                    D --> E1[XGBoost & LightGBM]:::step
                                    D --> E2[Isolation Forest & LOF]:::step
                                    E1 --> F[Predicción Consolidada]:::step
                                    E2 --> F
                                end
                                
                                subgraph S3 [3. Explicabilidad TreeSHAP]
                                    F --> G[Cálculo de Aportes SHAP]:::step
                                    G --> H[Top-5 Variables Relevantes]:::accent
                                end
                                
                                subgraph S4 [4. Recuperación Semántica RAG]
                                    H --> I[Consulta Semántica Vectorial]:::step
                                    J[(Base de Regulaciones)]:::data --> J_doc[Refs. Legales]:::data
                                    J_doc --> I
                                    I --> K[Fragmentos de Evidencia]:::step
                                end
                                
                                subgraph S5 [5. Generación Narrativa LLM]
                                    K --> L[Entrada Estructurada]:::step
                                    H --> L
                                    L --> M[LLM Orquestador Narrativo]:::step
                                end
                                
                                subgraph S6 [6. Presentación de Informes]
                                    M --> N[Dashboard Jerárquico]:::step
                                    N --> O[Reporte Explicable PDF/DOCX]:::accent
                                end
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sliding Drawer for Section Previews -->
        <div id="section-drawer" class="drawer-overlay">
            <button class="drawer-close-btn" onclick="closeSectionPreview()">✕ Cerrar Vista Previa</button>
            <div id="drawer-body" class="drawer-content-body">
                <!-- Loaded dynamically by JavaScript -->
            </div>
        </div>

        <script>
            function openSectionPreview(slug) {
                const drawer = document.getElementById('section-drawer');
                const body = document.getElementById('drawer-body');
                body.innerHTML = '<div style="text-align:center; padding:50px; color:var(--text-dim);">Cargando sección interactiva...</div>';
                drawer.classList.add('active');
                
                fetch('/api/seccion/' + slug)
                    .then(res => res.json())
                    .then(data => {
                        if (data.error) {
                            body.innerHTML = '<div style="color:var(--error); padding:20px;">Error al cargar la sección.</div>';
                        } else {
                            body.innerHTML = `
                                <h1 style="font-size:1.8rem; margin-bottom:15px; color:#fff; border-bottom: 2px solid var(--primary); padding-bottom:10px;">${data.title}</h1>
                                <div style="font-size:0.95rem; line-height:1.7; color:#e2e8f0;">${data.html}</div>
                            `;
                            // Re-trigger MathJax to process LaTeX formulas in the drawer
                            if (window.MathJax && window.MathJax.typeset) {
                                window.MathJax.typeset();
                            }
                        }
                    })
                    .catch(err => {
                        body.innerHTML = '<div style="color:var(--error); padding:20px;">Error de comunicación con el servidor.</div>';
                    });
            }

            function closeSectionPreview() {
                document.getElementById('section-drawer').classList.remove('active');
            }
        </script>

        <footer style="text-align: center; color: var(--text-dim); font-size: 0.8rem; padding: 20px 0; border-top: 1px solid var(--border);">
            &copy; 2026 Tesis Engineering Hub | Universidad Nacional de San Agustín (UNSA)
        </footer>
    </div>
</body>
</html>"""
    return html




PROPUESTA_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plataforma de Validación de Usabilidad e IA Explicable | Tesis Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'dark',
            securityLevel: 'loose',
            themeVariables: {
                background: '#1e293b',
                primaryColor: '#6366f1',
                primaryTextColor: '#fff',
                lineColor: '#cbd5e1'
            }
        });
    </script>
    <style>
        :root {
            --primary: #6366f1;
            --primary-light: #818cf8;
            --accent: #10b981;
            --accent-dark: #059669;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --error: #ef4444;
            --border: rgba(255, 255, 255, 0.08);
            --glass: rgba(30, 41, 59, 0.7);
        }

        /* Navigation Bar Styles */
        .main-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 12px 24px;
            margin-bottom: 30px;
        }
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 1.15rem;
            color: #fff;
        }
        .logo-dot {
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: pulse-dot 2s infinite;
        }
        @keyframes pulse-dot {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        .nav-menu {
            display: flex;
            gap: 8px;
        }
        .nav-item {
            color: var(--text-dim);
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .nav-item:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.04);
        }
        .nav-item.active {
            color: #fff;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.25);
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
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
        }

        .title-group h1 {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(to right, #818cf8, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }

        .title-group p {
            color: var(--text-dim);
            font-size: 1.05rem;
        }

        .nav-links {
            display: flex;
            gap: 12px;
        }

        .btn {
            background: var(--glass);
            border: 1px solid var(--border);
            color: var(--text-main);
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn:hover {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.15);
            transform: translateY(-2px);
        }

        .btn-accent {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            border: none;
        }

        .btn-accent:hover {
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
            filter: brightness(1.1);
        }

        /* Tabs Layout */
        .tabs-nav {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.03);
            padding: 6px;
            border-radius: 16px;
            width: fit-content;
            border: 1px solid var(--border);
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-dim);
            padding: 12px 24px;
            border-radius: 12px;
            font-family: inherit;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }

        .tab-btn.active {
            color: white;
            background: var(--primary);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.4s ease-out;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Card styles */
        .card {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 24px;
        }

        .card h2 {
            font-size: 1.4rem;
            margin-bottom: 20px;
            color: #c7d2fe;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
        }

        /* Tab 1: Architecture layout */
        .arch-grid {
            display: grid;
            grid-template-columns: 2fr 3fr;
            gap: 24px;
        }

        .mermaid-container {
            background: #1e293b;
            border-radius: 16px;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: auto;
            border: 1px solid var(--border);
        }

        .layers-desc {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .layer-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .layer-card:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: var(--primary);
        }

        .layer-card.active {
            background: rgba(99, 102, 241, 0.06);
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.25);
        }

        .layer-badge {
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 8px;
        }

        .badge-l1 { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
        .badge-l2 { background: rgba(16, 185, 129, 0.15); color: #34d399; }
        .badge-l3 { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
        .badge-l4 { background: rgba(239, 68, 68, 0.15); color: #f87171; }

        .layer-card h3 {
            font-size: 1.1rem;
            margin-bottom: 6px;
            color: #fff;
        }

        .layer-card p {
            color: var(--text-dim);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Tab 2: Development Plan Accordions */
        .plan-phase {
            margin-bottom: 16px;
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }

        .phase-header {
            background: rgba(255, 255, 255, 0.02);
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .phase-header:hover {
            background: rgba(255, 255, 255, 0.04);
        }

        .phase-title {
            font-weight: 600;
            font-size: 1.1rem;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .phase-progress {
            font-size: 0.85rem;
            color: var(--accent);
            font-weight: 700;
            background: rgba(16, 185, 129, 0.1);
            padding: 4px 10px;
            border-radius: 20px;
        }

        .phase-content {
            padding: 20px;
            border-top: 1px solid var(--border);
            background: rgba(0, 0, 0, 0.1);
        }

        .plan-checklist {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .checklist-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            font-size: 0.95rem;
            color: var(--text-main);
        }

        .checklist-item.done {
            color: var(--text-dim);
            text-decoration: line-through;
        }

        .checklist-item input[type="checkbox"] {
            margin-top: 4px;
            accent-color: var(--primary);
            width: 16px;
            height: 16px;
        }

        .plan-notes {
            margin-top: 15px;
            font-size: 0.85rem;
            color: var(--text-dim);
            border-left: 3px solid var(--primary);
            padding-left: 10px;
            font-style: italic;
        }

        /* Tab 3: Sandbox / Prototype styles */
        .sandbox-layout {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 24px;
            min-height: 600px;
        }

        /* Sidebar - Alert queue */
        .alert-queue {
            border-right: 1px solid var(--border);
            padding-right: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 650px;
            overflow-y: auto;
        }

        .queue-header {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-dim);
            margin-bottom: 8px;
            font-weight: 700;
        }

        .alert-item {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }

        .alert-item:hover {
            background: rgba(255,255,255,0.05);
            border-color: var(--primary);
        }

        .alert-item.active {
            background: rgba(99, 102, 241, 0.08);
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.1);
        }

        .alert-item-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            align-items: center;
        }

        .alert-id {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 0.9rem;
            color: #818cf8;
        }

        .alert-badge {
            font-size: 0.7rem;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .badge-pending { background: rgba(245, 158, 11, 0.12); color: var(--warn); }
        .badge-approved { background: rgba(16, 185, 129, 0.12); color: var(--accent); }
        .badge-rejected { background: rgba(239, 68, 68, 0.12); color: var(--error); }

        .alert-desc {
            font-size: 0.85rem;
            color: var(--text-dim);
            margin-bottom: 4px;
        }

        .alert-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-dim);
        }

        /* Detail panel */
        .detail-panel {
            min-height: 500px;
            display: flex;
            flex-direction: column;
        }

        .empty-detail {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            color: var(--text-dim);
            text-align: center;
            padding: 40px;
        }

        .empty-detail svg {
            width: 64px;
            height: 64px;
            color: rgba(255,255,255,0.05);
            margin-bottom: 16px;
        }

        .detail-header {
            border-bottom: 1px solid var(--border);
            padding-bottom: 16px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .detail-title h3 {
            font-size: 1.4rem;
            color: #fff;
            margin-bottom: 4px;
        }

        .detail-title p {
            color: var(--text-dim);
            font-size: 0.85rem;
        }

        .condition-switch {
            display: flex;
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            padding: 4px;
            border-radius: 10px;
        }

        .cond-btn {
            border: none;
            background: transparent;
            color: var(--text-dim);
            font-size: 0.8rem;
            font-weight: 600;
            padding: 6px 12px;
            border-radius: 8px;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.2s;
        }

        .cond-btn.active {
            color: #fff;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        .detail-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }

        .metadata-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }

        .metadata-table td {
            padding: 8px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }

        .metadata-table td.label {
            color: var(--text-dim);
            font-weight: 600;
            width: 45%;
        }

        .metadata-table td.val {
            font-family: 'JetBrains Mono', monospace;
            color: #fff;
        }

        /* Score Gauge */
        .score-box {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }

        .score-val {
            font-size: 2.2rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 4px;
        }

        .score-label {
            font-size: 0.8rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .score-bar-outer {
            height: 6px;
            background: rgba(255,255,255,0.05);
            border-radius: 99px;
            margin-top: 10px;
            overflow: hidden;
        }

        .score-bar-inner {
            height: 100%;
            background: linear-gradient(90deg, var(--accent) 0%, var(--error) 100%);
            width: 0%;
            transition: width 0.5s ease-in-out;
        }

        /* Tab view details */
        .view-cond-a, .view-cond-b {
            display: none;
        }

        .view-cond-a.active, .view-cond-b.active {
            display: block;
        }

        /* LLM Report Display */
        .llm-report {
            background: #0b1220;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            line-height: 1.6;
            color: #e2e8f0;
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 24px;
        }

        /* Actions form */
        .action-box {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            margin-top: auto;
        }

        .action-box h4 {
            font-size: 1rem;
            margin-bottom: 12px;
            color: #fff;
        }

        .form-row {
            display: flex;
            gap: 12px;
            margin-bottom: 12px;
        }

        .action-btn-choice {
            flex: 1;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.02);
            color: var(--text-dim);
            cursor: pointer;
            font-family: inherit;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s;
        }

        .action-btn-choice:hover {
            color: #fff;
            border-color: var(--text-dim);
        }

        .action-btn-choice.active[data-action="approve"] {
            background: rgba(239, 68, 68, 0.15);
            color: var(--error);
            border-color: var(--error);
        }

        .action-btn-choice.active[data-action="reject"] {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent);
            border-color: var(--accent);
        }

        .justification-area {
            width: 100%;
            height: 70px;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #fff;
            padding: 10px;
            font-family: inherit;
            font-size: 0.85rem;
            resize: none;
            margin-bottom: 12px;
            outline: none;
        }

        .justification-area:focus {
            border-color: var(--primary);
        }

        /* Top KPIs Row */
        .kpis-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .kpi-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px;
            text-align: center;
        }

        .kpi-card strong {
            display: block;
            font-size: 1.4rem;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 2px;
        }

        .kpi-card span {
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Toast notification */
        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #10b981;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2);
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s;
            z-index: 2000;
        }

        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }

        /* Live Timer display */
        .timer-badge {
            font-size: 0.8rem;
            color: var(--text-dim);
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            padding: 4px 8px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .timer-dot {
            width: 6px;
            height: 6px;
            background: var(--accent);
            border-radius: 50%;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Main Navbar -->
        <nav class="main-navbar">
            <div class="nav-logo">
                <span class="logo-dot"></span>
                <span class="logo-text">Tesis Hub</span>
            </div>
            <div class="nav-menu">
                <a href="/" class="nav-item">🏠 Inicio</a>
                <a href="/secciones" class="nav-item">📖 Secciones</a>
                <a href="/datos" class="nav-item">🗃️ Datos</a>
                <a href="/propuesta" class="nav-item active">📊 Propuesta y Prototipo</a>
                <a href="/admin" class="nav-item">⚙️ Administración</a>
            </div>
        </nav>

        <header>
            <div class="title-group">
                <h1>Sistema Integrado de Supervisión Operativa con IA Explicable (Prototipo Tesis)</h1>
                <p>Validación de la Eficiencia (Tiempo-a-Decisión, H1d), Comprensión (SHAP, H1b) y Calidad de Reportes (RAG, H1c) en Agroexportación</p>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="tabs-nav">
            <button class="tab-btn active" onclick="switchTab('tab-architecture', this)">📊 Arquitectura y Capas</button>
            <button class="tab-btn" onclick="switchTab('tab-plan', this)">📅 Plan de Desarrollo de Vistas</button>
            <button class="tab-btn" onclick="switchTab('tab-experiments', this)">🧪 Plan de Pruebas y Experimentos</button>
            <button class="tab-btn" onclick="switchTab('tab-prototype', this)">💻 Sandbox de Usabilidad (Simulador A/B)</button>
        </div>

        <!-- Tab 1: Architecture -->
        <div id="tab-architecture" class="tab-content active">
            <div class="arch-grid">
                <div class="layers-desc">
                    <div class="card" style="margin-bottom:0;">
                        <h2>Arquitectura del Sistema</h2>
                        <div class="layer-card" id="arch-card-1" onclick="selectArchLayer(1, this)">
                            <span class="layer-badge badge-l1">Capa 1: Predicción Tabular</span>
                            <h3>GBDT: XGBoost & LightGBM</h3>
                            <p>Esta capa estima valores esperados y comportamientos normales de variables clave de la cadena agroexportadora (precios, volúmenes de envío, mermas). Justificado para datos tabulares y transaccionales pequeños, sirviendo de línea base.</p>
                        </div>
                        <div class="layer-card" id="arch-card-2" style="margin-top: 12px;" onclick="selectArchLayer(2, this)">
                            <span class="layer-badge badge-l2">Capa 2: Detección de Anomalías</span>
                            <h3>Ensemble PyOD: IF + LOF + ECOD</h3>
                            <p>Combina Isolation Forest, Local Outlier Factor y ECOD en un ensamble robusto para identificar lotes operativos anómalos o sospechosos, reduciendo drásticamente la tasa de falsos positivos en comparación con detectores únicos.</p>
                        </div>
                        <div class="layer-card" id="arch-card-3" style="margin-top: 12px;" onclick="selectArchLayer(3, this)">
                            <span class="layer-badge badge-l3">Capa 3: Explicabilidad</span>
                            <h3>Explicabilidad Local con TreeSHAP</h3>
                            <p>Calcula la contribución marginal de cada variable de entrada (clima, logística, destino) sobre el score de anomalía de la alerta, identificando qué factores específicos (top-5 variables) provocaron la desviación.</p>
                        </div>
                        <div class="layer-card" id="arch-card-4" style="margin-top: 12px;" onclick="selectArchLayer(4, this)">
                            <span class="layer-badge badge-l4">Capa 4: Reportes Automáticos</span>
                            <h3>Narrativa de IA + RAG</h3>
                            <p>Un LLM con arquitectura de Recuperación Aumentada (RAG) redacta borradores de informes trazables en lenguaje natural. El modelo se ancla estrictamente a los vectores SHAP y a una base de regulaciones (resoluciones de la SBS, SENASA y FDA) para evitar alucinaciones.</p>
                        </div>
                    </div>
                </div>

                <div style="display:flex; flex-direction:column; gap:24px;">
                    <div class="mermaid-container">
                        <div class="mermaid">
                            graph TD
                                classDef layer1 fill:#312e81,stroke:#6366f1,stroke-width:2px,color:#dbeafe;
                                classDef layer2 fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#d1fae5;
                                classDef layer3 fill:#78350f,stroke:#fbbf24,stroke-width:2px,color:#fef3c7;
                                classDef layer4 fill:#7f1d1d,stroke:#f87171,stroke-width:2px,color:#fee2e2;
                                classDef db fill:#334155,stroke:#475569,stroke-width:2px,color:#f8fafc;
                                
                                D1[(Dataset Sintético v1.0)] --> L1[Capa 1: XGBoost & LightGBM]:::layer1
                                D2[(SENASA / MIDAGRI / SUNAT)] --> L1
                                L1 --> L1_out[Predicciones Normalidad]:::layer1
                                L1_out --> L2[Capa 2: Ensemble IF+LOF+ECOD]:::layer2
                                L2 --> L2_out[Score Anomalía Consolidado]:::layer2
                                L2_out -->|Score > 0.75| L3[Capa 3: Explicabilidad SHAP]:::layer3
                                L3 --> L3_out[Top-5 Variables Contribución]:::layer3
                                L3_out --> L4[Capa 4: Reportes RAG + LLM]:::layer4
                                L4 --> L4_out[Reporte Técnico Trazable PDF]:::layer4
                                
                                class D1,D2 db;
                        </div>
                    </div>

                    <div class="card" id="layer-inspector-card" style="margin-bottom:0;">
                        <h2 style="font-size:1.2rem; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:12px; color:#c7d2fe;">
                            🔍 Inspector de Flujo y Datos de Capa
                        </h2>
                        <div id="inspector-placeholder" style="color:var(--text-dim); text-align:center; padding:30px 10px; font-size:0.9rem;">
                            Haga clic en una de las capas de la izquierda para navegar por las entradas, salidas, fórmulas matemáticas y documentos de tesis asociados a ese diagrama.
                        </div>
                        <div id="inspector-content" style="display:none;">
                            <!-- Rendered dynamically by JS -->
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 2: Development Plan -->
        <div id="tab-plan" class="tab-content">
            <div class="card">
                <h2>Cronograma y Plan de Desarrollo de Tesis (Mayo - Diciembre 2026)</h2>
                <p style="font-size: 0.95rem; color: var(--text-dim); margin-bottom: 20px; line-height: 1.6;">
                    Plan de trabajo reestructurado para la tesis de Yoset Cozco Mauri. Detalla las 8 fases fundamentales abarcando la ingeniería de datos, el modelado backend con explicabilidad local, la interfaz del supervisor, el estudio piloto de usabilidad con 10 testers especializados, y el cierre académico de redacción.
                </p>

                <!-- Gantt Chart View -->
                <div class="mermaid-container" style="margin-bottom: 30px; background: rgba(15, 23, 42, 0.4);">
                    <div class="mermaid">
                        gantt
                            title Cronograma de Desarrollo e Implementación 2026
                            dateFormat  YYYY-MM
                            section Software y Datos
                            F1: Datos & Prep (Mayo)           :active, a1, 2026-05, 1m
                            F2: Modelos Predictivos (Jun-Jul)  : a2, 2026-06, 2m
                            F3: TreeSHAP & RAG (Agosto)       : a3, 2026-08, 1m
                            F4: UI & Pipeline (Septiembre)    : a4, 2026-09, 1m
                            section Experimentos
                            F5: Usabilidad & 10 Testers (Oct) : a5, 2026-10, 1m
                            F6: Robustez y Refinamientos (Nov): a6, 2026-11, 1m
                            section Tesis
                            F7: Redacción Cap. IV-V (Nov)      : a7, after a5, 1m
                            F8: Compilación & Defensa (Dic)   : a8, 2026-12, 1w
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase1')">
                        <span class="phase-title"><span>📂</span> Fase 1: Preparación de Datos e Ingeniería de Variables (Mayo)</span>
                        <span class="phase-progress">Completado</span>
                    </div>
                    <div id="phase1" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item done"><input type="checkbox" checked disabled> Operacionalización de variables clave en formato tabular de agroexportación.</li>
                            <li class="checklist-item done"><input type="checkbox" checked disabled> Generación del conjunto de datos sintético transaccional (2,000 registros).</li>
                            <li class="checklist-item done"><input type="checkbox" checked disabled> Pipeline de preprocesamiento de datos (`preprocess_data.py`) aplicando RobustScaler, KNNImputer y balanceo de clases SMOTE.</li>
                        </ul>
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase2')">
                        <span class="phase-title"><span>🤖</span> Fase 2: Desarrollo del Backend Predictivo y de Anomalías (Junio - Julio)</span>
                        <span class="phase-progress" style="background: rgba(99, 102, 241, 0.15); color: var(--primary-light);">En Desarrollo</span>
                    </div>
                    <div id="phase2" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item"><input type="checkbox" disabled> Creación de estimadores predictivos de GBDT (LightGBM y XGBoost) para el comportamiento base de las variables.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Calibración automática de hiperparámetros con Optuna (50 trials) para el Módulo 1.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Implementación del Módulo 2 de Detección de Anomalías no supervisadas utilizando un Ensemble de PyOD (Isolation Forest + LOF + ECOD).</li>
                        </ul>
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase3')">
                        <span class="phase-title"><span>🧠</span> Fase 3: Motor de Explicabilidad Local y Reportes RAG (Agosto)</span>
                        <span class="phase-progress" style="background: rgba(255, 255, 255, 0.05); color: var(--text-dim); border: 1px solid var(--border);">Planificado</span>
                    </div>
                    <div id="phase3" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item"><input type="checkbox" disabled> Integración de TreeSHAP para la extracción local del top-5 de variables que explican las alertas.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Construcción de la base de conocimiento vectorial RAG para regulaciones de exportación (SENASA, SBS y FDA).</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Orquestación de prompts con el LLM para generar reportes narrativos anclados estrictamente en SHAP.</li>
                        </ul>
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase4')">
                        <span class="phase-title"><span>💻</span> Fase 4: Frontend y Dashboard de Supervisión Operativa (Septiembre)</span>
                        <span class="phase-progress" style="background: rgba(255, 255, 255, 0.05); color: var(--text-dim); border: 1px solid var(--border);">Planificado</span>
                    </div>
                    <div id="phase4" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item"><input type="checkbox" disabled> UI interactiva en Flask con visualización de la cola de alertas y priorización.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Desarrollo de gráficos interactivos SHAP en la vista de detalle de la alerta.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Panel de exportación formal de reportes trazables en DOCX/PDF.</li>
                        </ul>
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase5')">
                        <span class="phase-title"><span>🧪</span> Fase 5: Protocolo de Usabilidad con Testers Especializados (Octubre)</span>
                        <span class="phase-progress" style="background: rgba(255, 255, 255, 0.05); color: var(--text-dim); border: 1px solid var(--border);">Planificado</span>
                    </div>
                    <div id="phase5" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item"><input type="checkbox" disabled> Reclutamiento de un grupo especializado de 10 testers (supervisores y analistas técnicos).</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Ejecución de las sesiones de usabilidad within-subjects (Condición A vs. Condición B) en la plataforma.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Registro de telemetría de interacción (tiempo-a-decisión, veredicto, etc.) en caliente.</li>
                        </ul>
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase6')">
                        <span class="phase-title"><span>⚙️</span> Fase 6: Robustez, Calidad y Cierre del Software (Noviembre)</span>
                        <span class="phase-progress" style="background: rgba(255, 255, 255, 0.05); color: var(--text-dim); border: 1px solid var(--border);">Planificado</span>
                    </div>
                    <div id="phase6" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item"><input type="checkbox" disabled> Pruebas estadísticas (t-test / Wilcoxon) sobre la telemetría recolectada para contrastar hipótesis.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Refinamiento de hiperparámetros y optimización de latencia en la generación RAG.</li>
                        </ul>
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase7')">
                        <span class="phase-title"><span>✍️</span> Fase 7: Redacción y Cierre de Capítulos IV y V (Noviembre)</span>
                        <span class="phase-progress" style="background: rgba(255, 255, 255, 0.05); color: var(--text-dim); border: 1px solid var(--border);">Planificado</span>
                    </div>
                    <div id="phase7" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item"><input type="checkbox" disabled> Redacción del Capítulo IV (Análisis de Resultados de Detección, Explicabilidad y Usabilidad).</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Redacción del Capítulo V (Discusión, Conclusiones y Recomendaciones de Gobernanza de IA).</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Completitud de Model Cards (Anexo B) y Datasheet de Datos (Anexo C).</li>
                        </ul>
                    </div>
                </div>

                <div class="plan-phase">
                    <div class="phase-header" onclick="toggleAccordion('phase8')">
                        <span class="phase-title"><span>🎓</span> Fase 8: Revisiones Finales, Compilación y Defensa (Diciembre)</span>
                        <span class="phase-progress" style="background: rgba(255, 255, 255, 0.05); color: var(--text-dim); border: 1px solid var(--border);">Planificado</span>
                    </div>
                    <div id="phase8" class="phase-content">
                        <ul class="plan-checklist">
                            <li class="checklist-item"><input type="checkbox" disabled> Purga bibliográfica y auditoría final de citas del repositorio.</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Compilación automatizada en Word (.docx) y PDF (normas APA 7, Times New Roman).</li>
                            <li class="checklist-item"><input type="checkbox" disabled> Sustentación y defensa de tesis ante la Escuela de Ingeniería de Sistemas de la UNSA (Semana 1).</li>
                        </ul>
                    </div>
                </div>
                
                <p class="plan-notes">
                    Nota: Las fases 1 y 2 están actualmente activas en el repositorio. Los siguientes pasos inmediatos se centrarán en la implementación del Módulo 1 (XGBoost/LightGBM + Optuna) y Módulo 2 (Ensemble de Anomalías con PyOD).
                </p>
            </div>
        </div>

        <!-- Tab 3: Plan de Pruebas y Experimentos -->
        <div id="tab-experiments" class="tab-content">
            <div class="card">
                <h2>🧪 Plan de Pruebas, Experimentos y Comparaciones</h2>
                <p style="font-size:0.95rem; color:var(--text-dim); margin-bottom:20px; line-height:1.6;">
                    Este panel detalla el protocolo experimental de la investigación metodológica para validar la eficiencia temporal, la explicabilidad local y la fidelidad del anclaje documental.
                </p>

                <!-- Section 1: Data split -->
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
                    <h3 style="color:#818cf8; margin-bottom:10px; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
                        <span>📊</span> Tratamiento de Datos, División Temporal y Semillas
                    </h3>
                    <p style="font-size:0.9rem; color:var(--text-main); line-height:1.5; margin-bottom:12px;">
                        Para prevenir la fuga de información debido al <em>concept drift</em> y la estacionalidad en variables del sector agroexportador, se ejecuta una <strong>división cronológica</strong> del dataset en lugar de una partición aleatoria:
                    </p>
                    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-bottom:16px; text-align:center;">
                        <div style="background:rgba(0,0,0,0.2); padding:12px; border-radius:8px; border:1px solid rgba(99, 102, 241, 0.15);">
                            <div style="font-size:0.8rem; color:#818cf8; font-weight:700;">Entrenamiento (Train)</div>
                            <strong style="font-size:1.4rem; color:#fff;">70%</strong>
                            <div style="font-size:0.75rem; color:var(--text-dim); margin-top:4px;">Primeros registros ordenados cronológicamente</div>
                        </div>
                        <div style="background:rgba(0,0,0,0.2); padding:12px; border-radius:8px; border:1px solid rgba(245, 158, 11, 0.15);">
                            <div style="font-size:0.8rem; color:#fbbf24; font-weight:700;">Validación (Validation)</div>
                            <strong style="font-size:1.4rem; color:#fff;">10%</strong>
                            <div style="font-size:0.75rem; color:var(--text-dim); margin-top:4px;">Ajuste de hiperparámetros (Optuna, 50 trials)</div>
                        </div>
                        <div style="background:rgba(0,0,0,0.2); padding:12px; border-radius:8px; border:1px solid rgba(16, 185, 129, 0.15);">
                            <div style="font-size:0.8rem; color:var(--accent); font-weight:700;">Pruebas (Test)</div>
                            <strong style="font-size:1.4rem; color:#fff;">20%</strong>
                            <div style="font-size:0.75rem; color:var(--text-dim); margin-top:4px;">Evaluación final libre de contaminación temporal</div>
                        </div>
                    </div>
                    <p style="font-size:0.85rem; color:var(--text-dim); font-style:italic;">
                        * Reproducibilidad: Las ejecuciones experimentales fijan la semilla principal en 42 y se repiten con 5 semillas adicionales (43, 44, 45, 46, 47) para reportar resultados en formato media ± desviación estándar.
                    </p>
                </div>

                <!-- Section 2: Experiments table -->
                <div style="margin-bottom: 24px;">
                    <h3 style="color:#c7d2fe; margin-bottom:12px; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
                        <span>🧪</span> Diseño Experimental: Experimentos E1–E5
                    </h3>
                    <div style="overflow-x:auto;">
                        <table style="width:100%; border-collapse:collapse; font-size:0.85rem; text-align:left; border: 1px solid var(--border);">
                            <thead>
                                <tr style="background:rgba(255,255,255,0.03); color:var(--text-dim); border-bottom: 1px solid var(--border);">
                                    <th style="padding:10px 12px; font-weight:700;">Exp.</th>
                                    <th style="padding:10px 12px; font-weight:700;">Nombre del Experimento</th>
                                    <th style="padding:10px 12px; font-weight:700;">Condición Experimental</th>
                                    <th style="padding:10px 12px; font-weight:700;">Grupo de Control</th>
                                    <th style="padding:10px 12px; font-weight:700;">Var. Observada (VD)</th>
                                    <th style="padding:10px 12px; font-weight:700;">Hipótesis</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:10px 12px; font-weight:bold; color:#818cf8;">E1</td>
                                    <td style="padding:10px 12px; font-weight:600; color:#fff;">Rendimiento de Detección</td>
                                    <td style="padding:10px 12px;">Ensemble IF + LOF + ECOD (PyOD)</td>
                                    <td style="padding:10px 12px;">Isolation Forest Individual</td>
                                    <td style="padding:10px 12px; font-family:monospace; color:var(--accent);">VD1: PR-AUC, F1-Score</td>
                                    <td style="padding:10px 12px; font-weight:bold; color:var(--accent);">H1a</td>
                                </tr>
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:10px 12px; font-weight:bold; color:#818cf8;">E2</td>
                                    <td style="padding:10px 12px; font-weight:600; color:#fff;">Aporte de Explicabilidad</td>
                                    <td style="padding:10px 12px;">Sistema con vectores SHAP</td>
                                    <td style="padding:10px 12px;">Sistema sin SHAP (solo scores)</td>
                                    <td style="padding:10px 12px; font-family:monospace; color:var(--accent);">VD2: Cobertura Top-K, Likert</td>
                                    <td style="padding:10px 12px; font-weight:bold; color:var(--accent);">H1b</td>
                                </tr>
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:10px 12px; font-weight:bold; color:#818cf8;">E3</td>
                                    <td style="padding:10px 12px; font-weight:600; color:#fff;">Aporte de Anclaje RAG</td>
                                    <td style="padding:10px 12px;">LLM + RAG (anclado en SHAP)</td>
                                    <td style="padding:10px 12px;">LLM libre (sin RAG)</td>
                                    <td style="padding:10px 12px; font-family:monospace; color:var(--accent);">VD3: Rúbrica 5D, ROUGE-L</td>
                                    <td style="padding:10px 12px; font-weight:bold; color:var(--accent);">H1c</td>
                                </tr>
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:10px 12px; font-weight:bold; color:#818cf8;">E4</td>
                                    <td style="padding:10px 12px; font-weight:600; color:#fff;">Evaluación del Sistema Integrado</td>
                                    <td style="padding:10px 12px;">Pipeline completo de 4 capas</td>
                                    <td style="padding:10px 12px;">Salidas técnicas aisladas</td>
                                    <td style="padding:10px 12px; font-family:monospace; color:var(--accent);">VD4: Tiempo de decisión, Likert</td>
                                    <td style="padding:10px 12px; font-weight:bold; color:var(--accent);">H1d</td>
                                </tr>
                                <tr>
                                    <td style="padding:10px 12px; font-weight:bold; color:#818cf8;">E5</td>
                                    <td style="padding:10px 12px; font-weight:600; color:#fff;">Ablation Study (E5a a E5d)</td>
                                    <td style="padding:10px 12px;">Configuraciones parciales (ver notas)</td>
                                    <td style="padding:10px 12px;">—</td>
                                    <td style="padding:10px 12px; font-family:monospace; color:var(--accent);">VD1 y VD5: Trazabilidad</td>
                                    <td style="padding:10px 12px; color:var(--text-dim);">Aporte Capa</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <p style="font-size:0.8rem; color:var(--text-dim); margin-top:8px; font-style:italic;">
                        Nota de Ablación: E5a (Solo Capa 2), E5b (Capas 1+2+4 sin SHAP), E5c (Capas 1+2+3 sin RAG), E5d (Pipeline completo).
                    </p>
                </div>

                <!-- Section 3: Statistical validation & baselines -->
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:24px;">
                    <div>
                        <h3 style="color:#fbbf24; margin-bottom:12px; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
                            <span>📊</span> Contraste de Hipótesis y Pruebas Estadísticas
                        </h3>
                        <div style="overflow-x:auto;">
                            <table style="width:100%; border-collapse:collapse; font-size:0.8rem; text-align:left; border: 1px solid var(--border);">
                                <thead>
                                    <tr style="background:rgba(255,255,255,0.03); color:var(--text-dim); border-bottom: 1px solid var(--border);">
                                        <th style="padding:8px 10px;">Sub-hipótesis</th>
                                        <th style="padding:8px 10px;">Comparación Clave</th>
                                        <th style="padding:8px 10px;">Prueba Estadística</th>
                                        <th style="padding:8px 10px;">α</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr style="border-bottom:1px solid var(--border);">
                                        <td style="padding:8px 10px; font-weight:bold; color:var(--accent);">H1a</td>
                                        <td style="padding:8px 10px;">Ensemble vs Detector Único</td>
                                        <td style="padding:8px 10px; font-family:monospace;">Wilcoxon Signed-Rank</td>
                                        <td style="padding:8px 10px;">0.05</td>
                                    </tr>
                                    <tr style="border-bottom:1px solid var(--border);">
                                        <td style="padding:8px 10px; font-weight:bold; color:var(--accent);">H1b</td>
                                        <td style="padding:8px 10px;">Vectores SHAP vs Sin SHAP</td>
                                        <td style="padding:8px 10px; font-family:monospace;">Mann-Whitney U</td>
                                        <td style="padding:8px 10px;">0.05</td>
                                    </tr>
                                    <tr style="border-bottom:1px solid var(--border);">
                                        <td style="padding:8px 10px; font-weight:bold; color:var(--accent);">H1c</td>
                                        <td style="padding:8px 10px;">Anclaje RAG vs LLM libre</td>
                                        <td style="padding:8px 10px; font-family:monospace;">t-Student apareada / Wilcoxon</td>
                                        <td style="padding:8px 10px;">0.05</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:8px 10px; font-weight:bold; color:var(--accent);">H1d</td>
                                        <td style="padding:8px 10px;">Integrado vs Aislado (Tiempo)</td>
                                        <td style="padding:8px 10px; font-family:monospace;">t-Student apareada (N=15)</td>
                                        <td style="padding:8px 10px;">0.05</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div>
                        <h3 style="color:#f87171; margin-bottom:12px; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
                            <span>🎯</span> Comparación de Modelos con Baselines
                        </h3>
                        <div style="overflow-x:auto;">
                            <table style="width:100%; border-collapse:collapse; font-size:0.8rem; text-align:left; border: 1px solid var(--border);">
                                <thead>
                                    <tr style="background:rgba(255,255,255,0.03); color:var(--text-dim); border-bottom: 1px solid var(--border);">
                                        <th style="padding:8px 10px;">Ref.</th>
                                        <th style="padding:8px 10px;">Baseline Utilizado</th>
                                        <th style="padding:8px 10px;">Justificación Teórica</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr style="border-bottom:1px solid var(--border);">
                                        <td style="padding:8px 10px; font-weight:bold; color:#f87171;">B1</td>
                                        <td style="padding:8px 10px; font-weight:600;">Isolation Forest individual</td>
                                        <td style="padding:8px 10px;">Detector más simple y ampliamente adoptado en la industria.</td>
                                    </tr>
                                    <tr style="border-bottom:1px solid var(--border);">
                                        <td style="padding:8px 10px; font-weight:bold; color:#f87171;">B2</td>
                                        <td style="padding:8px 10px; font-weight:600;">Ensemble IF + LOF (sin ECOD)</td>
                                        <td style="padding:8px 10px;">Aísla y mide la contribución específica de ECOD al ensemble.</td>
                                    </tr>
                                    <tr style="border-bottom:1px solid var(--border);">
                                        <td style="padding:8px 10px; font-weight:bold; color:#f87171;">B3</td>
                                        <td style="padding:8px 10px; font-weight:600;">XGBoost Supervisado</td>
                                        <td style="padding:8px 10px;">Límite superior (upper bound) teórico del rendimiento supervisado.</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:8px 10px; font-weight:bold; color:#f87171;">B4</td>
                                        <td style="padding:8px 10px; font-weight:600;">LLM sin RAG y sin SHAP</td>
                                        <td style="padding:8px 10px;">Línea base del reporte automático para evaluar alucinación.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 4: Interactive Sandbox / Prototype -->
        <div id="tab-prototype" class="tab-content">
            <div class="card" style="margin-bottom:20px; background:rgba(99, 102, 241, 0.05); border:1px solid rgba(99,102,241,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h3 style="color:#c7d2fe; margin-bottom:4px; font-size:1.15rem;">Simulación del Experimento Within-Subjects (Anexo A)</h3>
                        <p style="font-size:0.85rem; color:var(--text-dim);">Evalúe el impacto de la explicabilidad sobre el tiempo de decisión. Al alternar de condición, cambian las herramientas de análisis del auditor.</p>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.75rem; color:var(--text-dim); text-transform:uppercase; display:block;">Prueba de Hipótesis</span>
                        <strong style="color:var(--accent); font-size:0.95rem;">H1d (Eficiencia) & H1b (Comprensión)</strong>
                    </div>
                </div>
            </div>

            <div class="kpis-row">
                <div class="kpi-card">
                    <strong id="kpi-lotes">2,450</strong>
                    <span>Lotes Auditados</span>
                </div>
                <div class="kpi-card">
                    <strong id="kpi-anom">148</strong>
                    <span>Anomalías Detectadas</span>
                </div>
                <div class="kpi-card">
                    <strong id="kpi-fp">1.19%</strong>
                    <span>Tasa Falsos Positivos</span>
                </div>
                <div class="kpi-card">
                    <strong id="kpi-tiempo">12.4s</strong>
                    <span>Tiempo Medio de Decisión</span>
                </div>
            </div>

            <div class="sandbox-layout">
                <!-- Alert list column -->
                <div class="alert-queue">
                    <div class="queue-header">Cola de Alertas Recientes</div>
                    <div id="alerts-list-container">
                        <!-- Rendered by JS -->
                    </div>
                </div>

                <!-- Alert Detail column -->
                <div class="card" style="margin-bottom: 0;">
                    <div id="alert-detail-container" class="detail-panel">
                        <div class="empty-detail">
                            <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"></path>
                            </svg>
                            <h3>Ninguna alerta seleccionada</h3>
                            <p>Haga clic en una alerta de la lista izquierda para iniciar el análisis del lote y auditar las decisiones.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Session log table for statistical analysis -->
            <div class="card" style="margin-top: 24px;">
                <h2 style="font-size:1.2rem; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:12px; color:#c7d2fe;">
                    📊 Telemetría y Registro de Sesión (Datos para Pruebas Estadísticas - Wilcoxon / t-Student)
                </h2>
                <p style="font-size:0.85rem; color:var(--text-dim); margin-bottom:12px;">
                    Cada decisión que registras en el simulador superior se guarda en esta tabla de telemetría, emulando la recolección automática de variables dependientes descrita en el **Anexo A** para contrastar las hipótesis H1b (comprensión) y H1d (eficiencia temporal).
                </p>
                <div style="overflow-x: auto;">
                    <table style="width:100%; border-collapse:collapse; font-size:0.85rem; text-align:left;" id="session-log-table">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border); color:var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px;">
                                <th style="padding:12px;">ID Alerta</th>
                                <th style="padding:12px;">Lote</th>
                                <th style="padding:12px;">Condición</th>
                                <th style="padding:12px;">Veredicto</th>
                                <th style="padding:12px;">Tiempo (s)</th>
                                <th style="padding:12px;">Justificación</th>
                                <th style="padding:12px;">Trazabilidad (VD5)</th>
                            </tr>
                        </thead>
                        <tbody id="session-log-body">
                            <tr id="empty-session-row">
                                <td colspan="7" style="padding:20px; text-align:center; color:var(--text-dim); font-style:italic;">
                                    Aún no se han registrado decisiones en esta sesión. Seleccione una alerta arriba y envíe su veredicto.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast -->
    <div id="toast-success" class="toast">Decisión registrada con éxito. Archivo de telemetría de tesis actualizado.</div>

    <script>
        // JS Data
        const alertsData = [
            {
                id: "AL-1042",
                lote: "L-2026-084",
                fecha: "2026-05-18",
                producto: "Palta Hass",
                zona: "La Libertad",
                destino: "Unión Europea",
                volumen_kg: 24500,
                precio_usd_kg: 2.65,
                temperatura_max: 23.5,
                humedad_pct: 78,
                dias_logisticos: 41,
                costo_logistico_usd_kg: 0.95,
                cumplimiento_fitosanitario: "Sí",
                merma_pct: 3.8,
                tipo_cambio_pen_usd: 3.76,
                score_ECOD: 0.924,
                score_IF: 0.812,
                score_LOF: 0.745,
                ensemble_score: 0.827,
                status: "pending",
                tipo_anomalia: "logistica",
                shap_data: [
                    { name: "Días Logísticos (41 días)", val: 12.4, is_positive: true },
                    { name: "Costo Logístico (0.95 USD/kg)", val: 4.8, is_positive: true },
                    { name: "Temperatura Max (23.5°C)", val: -1.2, is_positive: false },
                    { name: "Humedad (78%)", val: -0.8, is_positive: false },
                    { name: "Cumplimiento Fitosanitario", val: -0.5, is_positive: false }
                ],
                report: `### Reporte de Alerta: Anomalía en Cadena Logística (Palta Hass a UE)
**Identificador:** AL-1042 | **Fecha:** 2026-05-18

#### 1. Resumen de la Alerta
El sistema de supervisión ha detectado un comportamiento anómalo en el tránsito logístico del Lote L-2026-084 (Palta Hass con destino a la Unión Europea). El score de anomalía consolidado por el ensemble es de **0.827**, superando el umbral de alerta configurado de **0.750**.

#### 2. Justificación Técnica (Explicabilidad SHAP)
Las variables que más contribuyeron a la clasificación de anomalía son:
* **Días Logísticos (41 días)**: Aporta un +12.4% a la anomalía, situándose significativamente por encima del promedio habitual de tránsito a la UE (22-26 días).
* **Costo Logístico (0.95 USD/kg)**: Aporta un +4.8% debido al aumento inesperado en fletes y cargos de demora.

#### 3. Contexto Regulatorio y Fitosanitario (Anclaje RAG)
Según la **Resolución SBS N° 053-2023** sobre gestión del riesgo de modelos y continuidad operativa, y de acuerdo a los requerimientos de la Unión Europea para productos perecederos (Reglamento CE N° 852/2004), los tránsitos superiores a 35 días en palta Hass incrementan exponencialmente el riesgo de sobre-maduración en puerto y rechazo comercial.
* **Nota Meteorológica:** SENAMHI reporta congestión en puertos de salida debido a oleaje anómalo durante la semana del embarque.`
            },
            {
                id: "AL-1043",
                lote: "L-2026-089",
                fecha: "2026-05-20",
                producto: "Espárrago Fresco",
                zona: "Ica",
                destino: "Estados Unidos",
                volumen_kg: 8200,
                precio_usd_kg: 3.40,
                temperatura_max: 37.2,
                humedad_pct: 42,
                dias_logisticos: 5,
                costo_logistico_usd_kg: 0.42,
                cumplimiento_fitosanitario: "Sí",
                merma_pct: 2.1,
                tipo_cambio_pen_usd: 3.75,
                score_ECOD: 0.895,
                score_IF: 0.790,
                score_LOF: 0.710,
                ensemble_score: 0.798,
                status: "pending",
                tipo_anomalia: "clima",
                shap_data: [
                    { name: "Temperatura Máx (37.2°C)", val: 14.2, is_positive: true },
                    { name: "Humedad (42%)", val: 5.1, is_positive: true },
                    { name: "Días Logísticos (5 días)", val: -2.3, is_positive: false },
                    { name: "Merma (2.1%)", val: -1.2, is_positive: false },
                    { name: "Precio (3.40 USD/kg)", val: 0.2, is_positive: true }
                ],
                report: `### Reporte de Alerta: Estrés Térmico por Clima Extremo (Espárrago de Ica a EEUU)
**Identificador:** AL-1043 | **Fecha:** 2026-05-20

#### 1. Resumen de la Alerta
Se detectó estrés térmico extremo en la zona de acopio de Ica para el Lote L-2026-089 (Espárrago Fresco). El score de anomalía consolidado es de **0.798** (umbral: 0.750).

#### 2. Justificación Técnica (Explicabilidad SHAP)
Las variables dominantes son:
* **Temperatura Máxima (37.2°C)**: Aporta un +14.2% al riesgo de anomalía. Representa un desvío de +3.2 sigmas respecto a la media histórica de Ica para este mes.
* **Humedad Relativa (42%)**: Aporta un +5.1% de contribución por sequedad extrema.

#### 3. Contexto Regulatorio y Fitosanitario (Anclaje RAG)
El manual fitosanitario de **SENASA** indica que temperaturas mayores a 35°C durante el acopio de espárragos aceleran la apertura de cabezas (florecimiento) y lignificación del tallo, reduciendo la calidad a Categoría II.
* **Mitigación Recomendada:** Activar el protocolo de pre-enfriado rápido (hydrocooling) de inmediato y reducir el tiempo de almacenamiento temporal a menos de 4 horas.`
            },
            {
                id: "AL-1044",
                lote: "L-2026-092",
                fecha: "2026-05-21",
                producto: "Arándano Orgánico",
                zona: "Arequipa",
                destino: "Asia",
                volumen_kg: 15400,
                precio_usd_kg: 11.80,
                temperatura_max: 21.0,
                humedad_pct: 60,
                dias_logisticos: 28,
                costo_logistico_usd_kg: 1.15,
                cumplimiento_fitosanitario: "Sí",
                merma_pct: 28.5,
                tipo_cambio_pen_usd: 3.77,
                score_ECOD: 0.941,
                score_IF: 0.885,
                score_LOF: 0.820,
                ensemble_score: 0.882,
                status: "pending",
                tipo_anomalia: "calidad",
                shap_data: [
                    { name: "Merma de Calidad (28.5%)", val: 18.5, is_positive: true },
                    { name: "Precio Exclusivo (11.80 USD/kg)", val: 6.2, is_positive: true },
                    { name: "Temperatura (21.0°C)", val: -0.5, is_positive: false },
                    { name: "Días Logísticos (28 días)", val: 1.1, is_positive: true },
                    { name: "Zona (Arequipa)", val: -0.3, is_positive: false }
                ],
                report: `### Reporte de Alerta: Merma de Calidad Excesiva en Arándano Orgánico (Destino Asia)
**Identificador:** AL-1044 | **Fecha:** 2026-05-21

#### 1. Resumen de la Alerta
Detección de pérdida crítica por calidad (merma física del 28.5%) en el Lote L-2026-092 de arándano orgánico de Arequipa con destino a Asia. El score consolidado es de **0.882** (crítico).

#### 2. Justificación Técnica (Explicabilidad SHAP)
Las variables dominantes son:
* **Merma (28.5%)**: Aporta +18.5% al score de anomalía. La merma tolerada contractualmente para Asia es de máximo 8.0%.
* **Precio (11.80 USD/kg)**: Aporta +6.2% de peso. Al ser un producto premium (orgánico), el impacto financiero de la merma se multiplica.

#### 3. Contexto Regulatorio y Fitosanitario (Anclaje RAG)
De acuerdo a las regulaciones de la FDA y estándares asiáticos de importación de berries, mermas superiores al 15% indican descomposición fúngica activa u hongos fitopatógenos, lo cual gatilla rechazo total del contenedor en destino y alerta sanitaria para la empresa exportadora.`
            },
            {
                id: "AL-1045",
                lote: "L-2026-095",
                fecha: "2026-05-22",
                producto: "Uva de Mesa",
                zona: "Piura",
                destino: "Estados Unidos",
                volumen_kg: 18000,
                precio_usd_kg: 3.10,
                temperatura_max: 29.5,
                humedad_pct: 65,
                dias_logisticos: 15,
                costo_logistico_usd_kg: 0.35,
                cumplimiento_fitosanitario: "Sí",
                merma_pct: 1.5,
                tipo_cambio_pen_usd: 3.76,
                score_ECOD: 0.120,
                score_IF: 0.145,
                score_LOF: 0.110,
                ensemble_score: 0.125,
                status: "pending",
                tipo_anomalia: "none",
                shap_data: [
                    { name: "Días Logísticos (15 días)", val: -2.8, is_positive: false },
                    { name: "Merma (1.5%)", val: -2.1, is_positive: false },
                    { name: "Precio (3.10 USD/kg)", val: -1.5, is_positive: false },
                    { name: "Temperatura (29.5°C)", val: -0.4, is_positive: false },
                    { name: "Humedad (65%)", val: -0.2, is_positive: false }
                ],
                report: `### Reporte de Alerta: Transacción Operativa Regular (Uva de Piura a EEUU)
**Identificador:** AL-1045 | **Fecha:** 2026-05-22

#### 1. Resumen de la Alerta
La operación del Lote L-2026-095 se clasifica como **Normal**. El score consolidado del ensemble es de **0.125**, muy por debajo del umbral de alerta (0.750).

#### 2. Justificación Técnica (Explicabilidad SHAP)
Todas las variables principales muestran aportes negativos, indicando estabilidad y consistencia estadística:
* **Días Logísticos (15 días)** y **Merma (1.5%)** corroboran la eficiencia y el excelente control de la cadena de frío de este despacho.

#### 3. Contexto Regulatorio y Fitosanitario (Anclaje RAG)
Operación alineada 100% con los acuerdos de pre-embarque SENASA-USDA para uva de mesa de Piura. No se requieren acciones correctivas.`
            }
        ];

        let selectedAlertId = null;
        let selectedCondition = 'A'; // 'A' or 'B'
        let timerInterval = null;
        let secondsElapsed = 0;
        let decisionTimes = [];

        // Tab selection (FIXED: reliable tab activation using btn reference)
        function switchTab(tabId, btn) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            if (btn) {
                btn.classList.add('active');
            } else {
                // Fallback selector matching tabId in onclick
                const activeBtn = document.querySelector(`button[onclick*="${tabId}"]`);
                if (activeBtn) activeBtn.classList.add('active');
            }
            
            const targetContent = document.getElementById(tabId);
            if (targetContent) {
                targetContent.classList.add('active');
            }

            if (tabId === 'tab-prototype') {
                renderAlertsList();
            }
        }

        // Accordion toggle
        function toggleAccordion(id) {
            const el = document.getElementById(id);
            if (el.style.display === "none" || !el.style.display) {
                el.style.display = "block";
            } else {
                el.style.display = "none";
            }
        }

        // Render sidebar list
        function renderAlertsList() {
            const container = document.getElementById('alerts-list-container');
            let html = '';
            alertsData.forEach(alert => {
                const activeClass = alert.id === selectedAlertId ? 'active' : '';
                const badgeClass = `badge-${alert.status}`;
                const badgeLabel = alert.status === 'pending' ? 'Pendiente' : (alert.status === 'approved' ? 'Anomalía Ok' : 'Falso Pos.');
                html += `
                    <div class="alert-item ${activeClass}" onclick="selectAlert('${alert.id}')">
                        <div class="alert-item-header">
                            <span class="alert-id">${alert.id}</span>
                            <span class="alert-badge ${badgeClass}">${badgeLabel}</span>
                        </div>
                        <div class="alert-desc">${alert.producto} · Lote ${alert.lote}</div>
                        <div class="alert-meta">
                            <span>Destino: ${alert.destino}</span>
                            <span style="font-weight:bold; color: ${alert.ensemble_score > 0.75 ? 'var(--error)' : 'var(--accent)'}">Score: ${alert.ensemble_score}</span>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        // Select alert to load details
        function selectAlert(id) {
            selectedAlertId = id;
            renderAlertsList();
            startTimer();
            renderAlertDetails();
        }

        // Switch Condition A vs B
        function setCondition(cond) {
            selectedCondition = cond;
            renderAlertDetails();
        }

        // Timer
        function startTimer() {
            clearInterval(timerInterval);
            secondsElapsed = 0;
            updateTimerDisplay();
            timerInterval = setInterval(() => {
                secondsElapsed++;
                updateTimerDisplay();
            }, 1000);
        }

        function updateTimerDisplay() {
            const el = document.getElementById('decision-timer-val');
            if (el) {
                el.innerText = `${secondsElapsed}s`;
            }
        }

        // Parse markdown text simple
        function parseMarkdown(text) {
            return text
                .replace(/^### (.*$)/gim, '<h3 style="color:#c7d2fe; margin-top:16px; margin-bottom:8px;">$1</h3>')
                .replace(/^#### (.*$)/gim, '<h4 style="color:#818cf8; margin-top:12px; margin-bottom:6px;">$1</h4>')
                .replace(/^\*\*([^*]+)\*\*/gim, '<strong>$1</strong>')
                .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
                .replace(/^\* (.*$)/gim, '<li style="margin-left: 20px; margin-bottom:4px; font-size:0.9rem;">$1</li>')
                .replace(/\\n/g, '<br>');
        }

        // Render SHAP graph
        function renderShap(shapData) {
            let html = '';
            shapData.forEach(item => {
                const valPercent = Math.min(Math.abs(item.val) * 6, 100);
                const color = item.is_positive ? 'var(--error)' : 'var(--accent)';
                const sign = item.is_positive ? '+' : '';
                html += `
                    <div style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
                            <span>${item.name}</span>
                            <span style="color: ${color}; font-weight: bold;">${sign}${item.val}%</span>
                        </div>
                        <div style="height: 8px; background: rgba(255,255,255,0.05); border-radius: 99px; overflow: hidden; position: relative;">
                            <div style="height: 100%; width: ${valPercent}%; background: ${color}; border-radius: 99px;"></div>
                        </div>
                    </div>
                `;
            });
            return html;
        }

        // Render detailed panel
        function renderAlertDetails() {
            const container = document.getElementById('alert-detail-container');
            const alertObj = alertsData.find(a => a.id === selectedAlertId);
            if (!alertObj) return;

            const isAnomalous = alertObj.ensemble_score > 0.75;
            const bannerColor = isAnomalous ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)';
            const bannerBorder = isAnomalous ? '1px solid rgba(239, 68, 68, 0.2)' : '1px solid rgba(16, 185, 129, 0.2)';
            const bannerText = isAnomalous ? 'Operación Atípica Detectada (Alerta de Anomalía)' : 'Operación dentro del Rango Normal';
            const bannerBadge = isAnomalous ? 'Critico' : 'Normal';
            const badgeColor = isAnomalous ? 'var(--error)' : 'var(--accent)';

            const isActionChosen = alertObj.status !== 'pending';
            const approveActive = alertObj.status === 'approved' ? 'active' : '';
            const rejectActive = alertObj.status === 'rejected' ? 'active' : '';

            let conditionHtml = '';

            if (selectedCondition === 'A') {
                // Condición A - Explicable y Reporte RAG
                conditionHtml = `
                    <div class="view-cond-a active">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
                            <div>
                                <h4 style="color:#c7d2fe; margin-bottom:12px; font-size:1rem;">Contribución de Variables (TreeSHAP)</h4>
                                <div style="background: rgba(255,255,255,0.01); border: 1px solid var(--border); padding:16px; border-radius:12px;">
                                    ${renderShap(alertObj.shap_data)}
                                </div>
                            </div>
                            <div>
                                <h4 style="color:#c7d2fe; margin-bottom:12px; font-size:1rem;">Reporte Narrativo Generado (LLM + RAG)</h4>
                                <div class="llm-report">
                                    ${parseMarkdown(alertObj.report)}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                // Condición B - Aislada (Solo Score)
                conditionHtml = `
                    <div class="view-cond-b active">
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius:12px; padding:20px; margin-bottom: 24px;">
                            <h4 style="color:#818cf8; margin-bottom:14px; font-size:1rem;">Scores de Modelos Técnicos</h4>
                            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 15px; text-align:center;">
                                <div style="background:rgba(0,0,0,0.2); padding:12px; border-radius:8px;">
                                    <div style="font-size:0.8rem; color:var(--text-dim);">ECOD (Empirical Cumulative)</div>
                                    <strong style="font-size:1.2rem; font-family:monospace; color:#fff;">${alertObj.score_ECOD}</strong>
                                </div>
                                <div style="background:rgba(0,0,0,0.2); padding:12px; border-radius:8px;">
                                    <div style="font-size:0.8rem; color:var(--text-dim);">Isolation Forest</div>
                                    <strong style="font-size:1.2rem; font-family:monospace; color:#fff;">${alertObj.score_IF}</strong>
                                </div>
                                <div style="background:rgba(0,0,0,0.2); padding:12px; border-radius:8px;">
                                    <div style="font-size:0.8rem; color:var(--text-dim);">LOF (Local Outlier Factor)</div>
                                    <strong style="font-size:1.2rem; font-family:monospace; color:#fff;">${alertObj.score_LOF}</strong>
                                </div>
                            </div>
                            <div style="margin-top:20px; color:var(--text-dim); font-size:0.85rem; font-style:italic;">
                                * Nota de usabilidad: En la Condición B, el auditor no dispone de vectores SHAP ni reporte de síntesis contextualizada.
                            </div>
                        </div>
                    </div>
                `;
            }

            container.innerHTML = `
                <!-- Detail Header -->
                <div class="detail-header">
                    <div class="detail-title">
                        <h3>Lote ${alertObj.lote}</h3>
                        <p>ID Alerta: ${alertObj.id} · Generado el ${alertObj.fecha}</p>
                    </div>
                    <div style="display:flex; flex-direction:column; align-items:flex-end; gap:8px;">
                        <div class="condition-switch">
                            <button class="cond-btn ${selectedCondition === 'A' ? 'active' : ''}" onclick="setCondition('A')">Condición A (Explicable)</button>
                            <button class="cond-btn ${selectedCondition === 'B' ? 'active' : ''}" onclick="setCondition('B')">Condición B (Aislado)</button>
                        </div>
                        <div class="timer-badge">
                            <div class="timer-dot"></div>
                            <span>Tiempo de análisis: </span>
                            <strong id="decision-timer-val" style="font-family:monospace;">${secondsElapsed}s</strong>
                        </div>
                    </div>
                </div>

                <!-- Alert status banner -->
                <div style="background: ${bannerColor}; border: ${bannerBorder}; padding: 12px 18px; border-radius: 10px; margin-bottom: 20px; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; font-size:0.95rem; color:#fff;">${bannerText}</span>
                    <span style="background: ${isAnomalous ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)'}; color: ${badgeColor}; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">${bannerBadge}</span>
                </div>

                <div class="detail-grid">
                    <!-- Column 1: Details Table -->
                    <div>
                        <table class="metadata-table">
                            <tbody>
                                <tr><td class="label">Producto</td><td class="val">${alertObj.producto}</td></tr>
                                <tr><td class="label">Zona de origen</td><td class="val">${alertObj.zona}</td></tr>
                                <tr><td class="label">Mercado Destino</td><td class="val">${alertObj.destino}</td></tr>
                                <tr><td class="label">Volumen Neto</td><td class="val">${alertObj.volumen_kg.toLocaleString()} kg</td></tr>
                                <tr><td class="label">Precio Unitario</td><td class="val">${alertObj.precio_usd_kg.toFixed(2)} USD/kg</td></tr>
                                <tr><td class="label">Días en Tránsito</td><td class="val">${alertObj.dias_logisticos} días</td></tr>
                                <tr><td class="label">Merma Física</td><td class="val">${alertObj.merma_pct}%</td></tr>
                                <tr><td class="label">Fitosanitario (SENASA)</td><td class="val">${alertObj.cumplimiento_fitosanitario}</td></tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Column 2: Score card -->
                    <div style="display:flex; flex-direction:column; justify-content:center;">
                        <div class="score-box">
                            <span class="score-label">Consolidated Ensemble Score</span>
                            <div class="score-val" style="color: ${alertObj.ensemble_score > 0.75 ? 'var(--error)' : 'var(--accent)'}">${alertObj.ensemble_score}</div>
                            <div class="score-bar-outer">
                                <div class="score-bar-inner" style="width: ${alertObj.ensemble_score * 100}%"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Active Condition View -->
                ${conditionHtml}

                <!-- Action form -->
                <div class="action-box">
                    <h4>Vedicto Operativo del Auditor</h4>
                    <div class="form-row">
                        <button class="action-btn-choice ${approveActive}" data-action="approve" onclick="selectAction('approved')">Confirmar Anomalía Crítica</button>
                        <button class="action-btn-choice ${rejectActive}" data-action="reject" onclick="selectAction('rejected')">Marcar Falso Positivo</button>
                    </div>
                    <textarea id="justification" class="justification-area" placeholder="Escriba la justificación basada en las variables explicadas (máx. 200 caracteres)..." ${isActionChosen ? 'disabled' : ''}>${alertObj.justification || ''}</textarea>
                    <button class="btn btn-accent" style="width:100%;" onclick="submitDecision()" ${isActionChosen ? 'disabled' : ''}>Registrar Decisión y Actualizar Trazabilidad</button>
                </div>
            `;
        }

        // Toggle button states in decision form
        let currentChoice = null;
        function selectAction(choice) {
            const alertObj = alertsData.find(a => a.id === selectedAlertId);
            if (alertObj && alertObj.status !== 'pending') return; // Cannot edit historical decisions

            currentChoice = choice;
            document.querySelectorAll('.action-btn-choice').forEach(btn => {
                btn.classList.remove('active');
                if (btn.getAttribute('data-action') === (choice === 'approved' ? 'approve' : 'reject')) {
                    btn.classList.add('active');
                }
            });
        }

        // Submit decision (FIXED: removed global alert shadowing and window.alert fallback)
        function submitDecision() {
            if (!selectedAlertId) return;
            const alertObj = alertsData.find(a => a.id === selectedAlertId);
            if (alertObj.status !== 'pending') return;

            if (!currentChoice) {
                window.alert("Por favor, seleccione un veredicto (Confirmar o Descartar) antes de enviar.");
                return;
            }

            const justVal = document.getElementById('justification').value.trim();
            if (justVal.length === 0) {
                window.alert("Por favor, escriba una justificación textual.");
                return;
            }

            // Stop timer
            clearInterval(timerInterval);
            decisionTimes.push(secondsElapsed);

            // Update local object
            alertObj.status = currentChoice;
            alertObj.justification = justVal;

            // Recalculate KPIs
            let pendingCount = alertsData.filter(a => a.status === 'pending').length;
            let approvedCount = alertsData.filter(a => a.status === 'approved').length;
            let rejectedCount = alertsData.filter(a => a.status === 'rejected').length;
            
            // Simulated additions to metrics
            document.getElementById('kpi-anom').innerText = 148 + approvedCount;
            // Update false positive rate: rejected decisions / total audits
            let totalAudited = 148 + approvedCount + rejectedCount;
            let fpRate = (rejectedCount / totalAudited) * 100;
            document.getElementById('kpi-fp').innerText = fpRate > 0 ? `${fpRate.toFixed(2)}%` : "1.19%";

            // Average decision time
            let sumTimes = decisionTimes.reduce((a, b) => a + b, 0);
            let avgTime = (12.4 * 148 + sumTimes) / (148 + decisionTimes.length);
            document.getElementById('kpi-tiempo').innerText = `${avgTime.toFixed(1)}s`;

            // Add row to session log (Telemetría de Tesis)
            const logBody = document.getElementById('session-log-body');
            const emptyRow = document.getElementById('empty-session-row');
            if (emptyRow) emptyRow.remove();

            const condLabel = selectedCondition === 'A' ? 
                '<span style="color:#818cf8; font-weight:bold;">Condición A (Integrado)</span>' : 
                '<span style="color:var(--text-dim);">Condición B (Aislado)</span>';
            const veredictoLabel = currentChoice === 'approved' ? 
                '<span style="color:var(--error); font-weight:bold;">Anomalía Confirmada</span>' : 
                '<span style="color:var(--accent); font-weight:bold;">Falso Positivo</span>';
            const trazabilidadLabel = selectedCondition === 'A' ? 
                '<span style="color:var(--accent); font-weight:bold;">100% (Completa)</span>' : 
                '<span style="color:var(--error);">30% (Sin SHAP/RAG)</span>';

            const newRow = document.createElement('tr');
            newRow.style.borderBottom = '1px solid var(--border)';
            newRow.innerHTML = `
                <td style="padding:12px; font-family:monospace;">${alertObj.id}</td>
                <td style="padding:12px;">${alertObj.lote}</td>
                <td style="padding:12px;">${condLabel}</td>
                <td style="padding:12px;">${veredictoLabel}</td>
                <td style="padding:12px; font-family:monospace; font-weight:bold;">${secondsElapsed}s</td>
                <td style="padding:12px; color:var(--text-dim); font-size:0.8rem; max-width:250px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${justVal}">${justVal}</td>
                <td style="padding:12px;">${trazabilidadLabel}</td>
            `;
            logBody.appendChild(newRow);

            // Show Toast
            const toast = document.getElementById('toast-success');
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);

            // Refresh view
            renderAlertsList();
            renderAlertDetails();
        }

        // Metadata de las capas de la arquitectura
        const layersMetadata = {
            1: {
                title: "Capa 1: Predicción Tabular de Series",
                subtitle: "XGBoost & LightGBM",
                badgeClass: "badge-l1",
                inputs: "Variables transaccionales históricas de agroexportación (Precios MIDAGRI, Volúmenes SUNAT, Clima SENAMHI, Fitosanitario SENASA, Días Logísticos).",
                outputs: "Valores esperados y umbrales de normalidad estadística para cada registro operativo.",
                logic: "Algoritmos Gradient Boosting que optimizan la función de pérdida regularizada mediante divisiones sucesivas de árboles de decisión.",
                formula: "F_m(x) = F_{m-1}(x) + \\\\gamma_m h_m(x)",
                metrics: "RMSE (Root Mean Squared Error), MAE (Mean Absolute Error), R² (Coeficiente de Determinación).",
                links: [
                    { name: "Metodología: §3.1", path: "/seccion/30-capitulo3" },
                    { name: "Anexo B: Model Cards", path: "/seccion/a2-anexo-modelcards" }
                ]
            },
            2: {
                title: "Capa 2: Detección de Anomalías (Ensemble)",
                subtitle: "Isolation Forest + LOF + ECOD",
                badgeClass: "badge-l2",
                inputs: "Desvíos de variables observadas versus valores predichos (de Capa 1) y dataset transaccional.",
                outputs: "Score consolidado de anomalía (0.0 a 1.0) y bandera de alerta si el score supera el umbral (0.75).",
                logic: "Ensemble no supervisado orquestado por PyOD que promedia o maximiza las predicciones de Isolation Forest, Local Outlier Factor y ECOD.",
                formula: "Score_{cons} = \\\\frac{1}{3}(Score_{IF} + Score_{LOF} + Score_{ECOD})",
                metrics: "PR-AUC (Área bajo la curva Precisión-Exhaustividad), ROC-AUC, F1-Score (umbral óptimo).",
                links: [
                    { name: "Metodología: §3.1 y §3.3", path: "/seccion/30-capitulo3" },
                    { name: "Anexo C: Datasheet de Datasets", path: "/seccion/a3-anexo-datasheet" }
                ]
            },
            3: {
                title: "Capa 3: Explicabilidad Algorítmica",
                subtitle: "TreeSHAP (Shapley Values)",
                badgeClass: "badge-l3",
                inputs: "Registros de alertas clasificadas como anomalías (de Capa 2), la estructura de pesos y caminos de los árboles de decisión.",
                outputs: "Vectores SHAP de contribución local indicando el peso (+ o -) de cada una de las top-5 variables en la alerta.",
                logic: "Algoritmo TreeSHAP optimizado para árboles de decisión que calcula las atribuciones locales exactas basadas en la teoría de juegos cooperativos.",
                formula: "\\\\phi_i = \\\\sum_{S \\\\subseteq F \\\\setminus \\\\{i\\\\}} \\\\frac{|S|!(|F| - |S| - 1)!}{|F|!} [f_x(S \\\\cup \\\\{i\\\\}) - f_x(S)]",
                metrics: "Cobertura Top-K (porcentaje de alertas donde el top-5 explica ≥80% del score absoluto), Índice de Estabilidad SHAP.",
                links: [
                    { name: "Metodología: §3.1", path: "/seccion/30-capitulo3" },
                    { name: "Anexo A: Usabilidad y Explicabilidad", path: "/seccion/a1-anexo-usabilidad" }
                ]
            },
            4: {
                title: "Capa 4: Reportes Narrativos Generativos",
                subtitle: "LLM + RAG",
                badgeClass: "badge-l4",
                inputs: "Vectores SHAP (de Capa 3), metadatos del lote operativo, Base de Conocimientos regulatorios (Resolución SBS N° 053-2023, manual fitosanitario SENASA).",
                outputs: "Borrador de reporte en lenguaje natural con anclaje técnico y legal en formato Markdown/PDF.",
                logic: "Recuperación semántica (RAG) de directivas asociadas y generación estructurada por LLM mediante prompts que impiden la alucinación de datos numéricos.",
                formula: "\\\\text{Reporte} = \\\\text{LLM}(\\\\text{Query}, \\\\text{SHAP}, \\\\text{Contexto}_{\\\\text{RAG}})",
                metrics: "Rúbrica 5D (Completitud, Coherencia, Accionabilidad, Consistencia numérica, Evidencias), ROUGE-L.",
                links: [
                    { name: "Metodología: §3.1 y §3.3", path: "/seccion/30-capitulo3" },
                    { name: "Anexo D: Declaración de uso de IA", path: "/seccion/a4-anexo-ia" }
                ]
            }
        };

        // Función para seleccionar e inspeccionar una capa de la arquitectura (FIXED: LaTeX markup in MathJax)
        function selectArchLayer(id, el) {
            // Quitar clase active de todas las layer-cards
            document.querySelectorAll('.layer-card').forEach(card => card.classList.remove('active'));
            
            // Agregar clase active a la card clickeada
            if (el) el.classList.add('active');
            
            // Ocultar placeholder
            const placeholder = document.getElementById('inspector-placeholder');
            if (placeholder) placeholder.style.display = 'none';
            
            // Mostrar y rellenar inspector
            const content = document.getElementById('inspector-content');
            if (content) {
                content.style.display = 'block';
                
                const meta = layersMetadata[id];
                
                content.innerHTML = `
                    <div style="margin-bottom:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span class="layer-badge ${meta.badgeClass}" style="margin-bottom:0;">${meta.title}</span>
                            <span style="font-size:0.85rem; color:var(--text-dim); font-family:'JetBrains Mono', monospace; font-weight:700;">${meta.subtitle}</span>
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
                        <div style="background:rgba(0,0,0,0.15); padding:12px; border-radius:8px; border:1px solid var(--border);">
                            <h4 style="font-size:0.85rem; color:#818cf8; margin-bottom:6px; font-weight:700;">📥 Entradas (Inputs)</h4>
                            <p style="font-size:0.85rem; line-height:1.4; color:var(--text-main);">${meta.inputs}</p>
                        </div>
                        <div style="background:rgba(0,0,0,0.15); padding:12px; border-radius:8px; border:1px solid var(--border);">
                            <h4 style="font-size:0.85rem; color:var(--accent); margin-bottom:6px; font-weight:700;">📤 Salidas (Outputs)</h4>
                            <p style="font-size:0.85rem; line-height:1.4; color:var(--text-main);">${meta.outputs}</p>
                        </div>
                    </div>

                    <div style="background:rgba(0,0,0,0.15); padding:12px; border-radius:8px; border:1px solid var(--border); margin-bottom:16px;">
                        <h4 style="font-size:0.85rem; color:#fbbf24; margin-bottom:6px; font-weight:700;">⚙️ Lógica y Formulación Matemática</h4>
                        <p style="font-size:0.85rem; line-height:1.4; margin-bottom:8px; color:var(--text-dim);">${meta.logic}</p>
                        <div style="display:flex; justify-content:center; background:rgba(0,0,0,0.2); padding:12px; border-radius:6px; font-family:'JetBrains Mono', monospace; font-size:0.95rem; color:#fff; overflow-x:auto;">
                            $$${meta.formula}$$
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns:1.2fr 1fr; gap:16px;">
                        <div style="background:rgba(0,0,0,0.15); padding:12px; border-radius:8px; border:1px solid var(--border);">
                            <h4 style="font-size:0.85rem; color:#f87171; margin-bottom:6px; font-weight:700;">📈 Métricas de Evaluación</h4>
                            <p style="font-size:0.85rem; line-height:1.4; color:var(--text-main);">${meta.metrics}</p>
                        </div>
                        <div style="background:rgba(0,0,0,0.15); padding:12px; border-radius:8px; border:1px solid var(--border);">
                            <h4 style="font-size:0.85rem; color:#a5b4fc; margin-bottom:6px; font-weight:700;">📘 Trazabilidad en Documento Tesis</h4>
                            <div style="display:flex; flex-direction:column; gap:6px; margin-top:4px;">
                                ${meta.links.map(l => `<a href="${l.path}" class="btn" style="padding:4px 8px; font-size:0.75rem; text-align:center; display:block;">${l.name}</a>`).join('')}
                            </div>
                        </div>
                    </div>
                `;
                
                // Re-renderizar las fórmulas matemáticas LaTeX agregadas dinámicamente con MathJax
                if (window.MathJax && MathJax.typesetPromise) {
                    MathJax.typesetPromise([content]);
                }
            }
        }

        // Seleccionar la Capa 1 por defecto al cargar la página (FIXED: reliable trigger)
        const activeCard = document.getElementById('arch-card-1');
        if (activeCard) {
            selectArchLayer(1, activeCard);
        }
    </script>
</body>
</html>"""

@app.route('/propuesta')
def propuesta_solucion():
    """Sirve la página interactiva de la propuesta tecnológica y prototipo."""
    return render_template_string(PROPUESTA_TEMPLATE)




@app.route('/datos')
def view_data_explorer():
    """Sirve la vista del Explorador de Datasets interactivo."""
    return render_template_string(DATOS_TEMPLATE)


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
    
    import csv
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

            /* Navigation Bar Styles */
            .main-navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(30, 41, 59, 0.7);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 12px 24px;
                margin-bottom: 30px;
            }
            .nav-logo {
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: 700;
                font-size: 1.15rem;
                color: #fff;
            }
            .logo-dot {
                width: 8px;
                height: 8px;
                background: var(--ok);
                border-radius: 50%;
                box-shadow: 0 0 10px var(--ok);
                animation: pulse-dot 2s infinite;
            }
            @keyframes pulse-dot {
                0% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.2); opacity: 0.7; }
                100% { transform: scale(1); opacity: 1; }
            }
            .nav-menu {
                display: flex;
                gap: 8px;
            }
            .nav-item {
                color: var(--muted);
                text-decoration: none;
                padding: 8px 16px;
                border-radius: 10px;
                font-size: 0.9rem;
                font-weight: 600;
                transition: all 0.2s ease;
            }
            .nav-item:hover {
                color: #fff;
                background: rgba(255, 255, 255, 0.04);
            }
            .nav-item.active {
                color: #fff;
                background: rgba(99, 102, 241, 0.15);
                border: 1px solid rgba(99, 102, 241, 0.25);
            }
        </style>
    </head>
    <body>
        <div class="wrap">
            <!-- Main Navbar -->
            <nav class="main-navbar">
                <div class="nav-logo">
                    <span class="logo-dot"></span>
                    <span class="logo-text">Tesis Hub</span>
                </div>
                <div class="nav-menu">
                    <a href="/" class="nav-item">🏠 Inicio</a>
                    <a href="/secciones" class="nav-item">📖 Secciones</a>
                    <a href="/datos" class="nav-item">🗃️ Datos</a>
                    <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
                    <a href="/admin" class="nav-item active">⚙️ Administración</a>
                </div>
            </nav>

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


# =============================================================================
# EXPLORADOR DE DATOS INTERACTIVO
# =============================================================================

DATOS_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explorador de Datasets | Tesis Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --primary: #6366f1;
            --accent: #10b981;
            --warn: #f59e0b;
            --error: #ef4444;
            --text: #f8fafc;
            --muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.08);
            --glass: rgba(30, 41, 59, 0.7);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
            color: var(--text);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* Navigation Bar Styles */
        .main-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 12px 24px;
            margin-bottom: 30px;
        }
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 1.15rem;
            color: #fff;
        }
        .logo-dot {
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: pulse-dot 2s infinite;
        }
        @keyframes pulse-dot {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        .nav-menu {
            display: flex;
            gap: 8px;
        }
        .nav-item {
            color: var(--muted);
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .nav-item:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.04);
        }
        .nav-item.active {
            color: #fff;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.25);
        }

        header { margin-bottom: 30px; }
        h1 { font-size: 2.2rem; margin-bottom: 6px; background: linear-gradient(to right, #818cf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: var(--muted); font-size: 1rem; }

        .explorer-layout {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 24px;
        }
        .card {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .card h2 { font-size: 1.25rem; color: #c7d2fe; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }

        /* Dataset list styling */
        .dataset-list { display: flex; flex-direction: column; gap: 8px; }
        .dataset-btn {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            color: var(--muted);
            padding: 12px 16px;
            border-radius: 12px;
            cursor: pointer;
            text-align: left;
            font-family: inherit;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        .dataset-btn:hover { color: #fff; border-color: var(--primary); background: rgba(99, 102, 241, 0.05); }
        .dataset-btn.active { color: #fff; border-color: var(--primary); background: var(--primary); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); }

        /* Table & Controls */
        .controls-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 16px; }
        .search-input {
            background: rgba(0,0,0,0.2);
            border: 1px solid var(--border);
            padding: 10px 16px;
            border-radius: 10px;
            color: #fff;
            font-family: inherit;
            font-size: 0.9rem;
            width: 250px;
            outline: none;
        }
        .search-input:focus { border-color: var(--primary); }
        .limit-select {
            background: #1e293b;
            border: 1px solid var(--border);
            padding: 8px 12px;
            border-radius: 8px;
            color: #fff;
            font-family: inherit;
            font-size: 0.85rem;
            outline: none;
        }

        .table-wrap { overflow-x: auto; max-height: 500px; border: 1px solid var(--border); border-radius: 12px; background: rgba(0,0,0,0.15); }
        table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
        th { background: #1e293b; padding: 12px 14px; font-weight: 600; border-bottom: 2px solid var(--border); color: #cbd5e1; cursor: pointer; user-select: none; }
        th:hover { color: #fff; background: rgba(99, 102, 241, 0.2); }
        td { padding: 10px 14px; border-bottom: 1px solid var(--border); color: #e2e8f0; }
        tr:hover td { background: rgba(255,255,255,0.03); }

        .pagination { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
        .page-btn {
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border);
            color: #fff;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-family: inherit;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .page-btn:hover { background: rgba(99, 102, 241, 0.15); }
        .page-btn:disabled { opacity: 0.3; cursor: not-allowed; }

        .metadata-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
        .meta-card { background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid var(--border); }
        .meta-val { font-size: 1.3rem; font-weight: 700; color: var(--primary); font-family: 'JetBrains Mono', monospace; }
        .meta-lbl { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; }

        .chart-container { width: 100%; height: 260px; display: flex; justify-content: center; align-items: center; position: relative; }
        
        .loading-overlay { text-align: center; padding: 60px; color: var(--muted); }
        .spinner { width: 40px; height: 40px; border: 4px solid rgba(255,255,255,0.1); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
<div class="container">
    <!-- Main Navbar -->
    <nav class="main-navbar">
        <div class="nav-logo">
            <span class="logo-dot"></span>
            <span class="logo-text">Tesis Hub</span>
        </div>
        <div class="nav-menu">
            <a href="/" class="nav-item">🏠 Inicio</a>
            <a href="/secciones" class="nav-item">📖 Secciones</a>
            <a href="/datos" class="nav-item active">🗃️ Datos</a>
            <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
            <a href="/admin" class="nav-item">⚙️ Administración</a>
        </div>
    </nav>

    <header>
        <h1>Explorador de Datasets de Tesis</h1>
        <p class="sub">Visualice, ordene, filtre y analice las estadísticas de las fuentes reales e hipotéticas del sistema.</p>
    </header>

    <div class="explorer-layout">
        <!-- Sidebar -->
        <aside>
            <div class="card">
                <h2>Fuentes de Datos</h2>
                <div class="dataset-list">
                    <button class="dataset-btn active" onclick="loadDataset('synthetic_agro', this)">🤖 Dataset Sintético v1.0</button>
                    <button class="dataset-btn" onclick="loadDataset('train_raw', this)">📊 Train Preprocesado (Sin Bal.)</button>
                    <button class="dataset-btn" onclick="loadDataset('train_balanced', this)">⚖️ Train Balanceado (SMOTE)</button>
                    <button class="dataset-btn" onclick="loadDataset('test_processed', this)">🧪 Test Preprocesado (2025)</button>
                    <button class="dataset-btn" onclick="loadDataset('bcrp_exchange', this)">💵 Tipo de Cambio (BCRP)</button>
                    <button class="dataset-btn" onclick="loadDataset('faostat_prod', this)">🌾 Producción Agro (FAOSTAT)</button>
                    <button class="dataset-btn" onclick="loadDataset('sunat_export', this)">🚢 Exportaciones (SUNAT)</button>
                    <button class="dataset-btn" onclick="loadDataset('validated_refs', this)">📋 Datasets Validados (CSV)</button>
                </div>
            </div>
            
            <div class="card">
                <h2>Resumen Técnico</h2>
                <div id="metadata-container">
                    <!-- Loaded dynamically -->
                    <p style="color:var(--muted); font-size:0.9rem; text-align:center;">Cargando metadatos...</p>
                </div>
            </div>
        </aside>

        <!-- Main Panel -->
        <main>
            <div class="card" id="chart-card">
                <h2>Análisis Gráfico</h2>
                <div class="chart-container">
                    <canvas id="dataset-chart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>Registros de Datos</h2>
                <div class="controls-row">
                    <div>
                        <span style="font-size:0.85rem; color:var(--muted)">Mostrar</span>
                        <select class="limit-select" id="page-size-select" onchange="changePageSize(this.value)">
                            <option value="10">10 filas</option>
                            <option value="25">25 filas</option>
                            <option value="50">50 filas</option>
                        </select>
                    </div>
                    <input type="text" class="search-input" id="search-box" placeholder="Buscar registros..." onkeyup="filterRows(this.value)">
                </div>

                <div id="table-loading-container" class="loading-overlay">
                    <div class="spinner"></div>
                    <p>Cargando datos del archivo CSV...</p>
                </div>

                <div id="table-display-container" style="display:none;">
                    <div class="table-wrap">
                        <table id="data-table">
                            <thead id="table-head"></thead>
                            <tbody id="table-body"></tbody>
                        </table>
                    </div>

                    <div class="pagination">
                        <span style="font-size:0.85rem; color:var(--muted)" id="page-indicator">Mostrando 1-10 de 100</span>
                        <div>
                            <button class="page-btn" id="prev-btn" onclick="prevPage()">Anterior</button>
                            <button class="page-btn" id="next-btn" onclick="nextPage()" style="margin-left:8px;">Siguiente</button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>

<script>
    let currentData = { columns: [], rows: [] };
    let filteredRows = [];
    let currentPage = 1;
    let pageSize = 10;
    let activeDataset = 'synthetic_agro';
    let chartInstance = null;

    async function loadDataset(key, btn) {
        if (btn) {
            document.querySelectorAll('.dataset-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }
        activeDataset = key;
        
        // Reset view
        document.getElementById('table-loading-container').style.display = 'block';
        document.getElementById('table-display-container').style.display = 'none';
        document.getElementById('search-box').value = '';
        
        try {
            const res = await fetch(`/api/data/${key}`);
            const payload = await res.json();
            if (payload.error) {
                alert(payload.error);
                return;
            }
            currentData = payload;
            filteredRows = [...currentData.rows];
            currentPage = 1;
            
            renderMetadata(payload.stats);
            renderChart(key, payload);
            renderTable();
        } catch (e) {
            alert("Error cargando el dataset: " + e.message);
        }
    }

    function renderMetadata(stats) {
        const container = document.getElementById('metadata-container');
        container.innerHTML = `
            <div class="metadata-grid">
                <div class="meta-card">
                    <div class="meta-val">${stats.num_rows.toLocaleString()}</div>
                    <div class="meta-lbl">Registros</div>
                </div>
                <div class="meta-card">
                    <div class="meta-val">${stats.num_cols}</div>
                    <div class="meta-lbl">Columnas</div>
                </div>
            </div>
            <p style="font-size:0.85rem; margin-bottom:4px; color:var(--muted);">Archivo: <span style="color:#fff; font-family:monospace;">${stats.filename}</span></p>
        `;
    }

    function renderChart(key, data) {
        const ctx = document.getElementById('dataset-chart').getContext('2d');
        if (chartInstance) {
            chartInstance.destroy();
        }
        
        const chartCard = document.getElementById('chart-card');
        chartCard.style.display = 'block';

        let chartConfig = {};

        if (key === 'synthetic_agro') {
            // Pie chart of anomaly types
            const anomalies = data.rows.filter(r => r.etiqueta_anomalia === '1' || r.etiqueta_anomalia === 1);
            const counts = {};
            anomalies.forEach(r => {
                const t = r.tipo_anomalia || 'Desconocido';
                counts[t] = (counts[t] || 0) + 1;
            });
            chartConfig = {
                type: 'pie',
                data: {
                    labels: Object.keys(counts),
                    datasets: [{
                        data: Object.values(counts),
                        backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'],
                        borderWidth: 1,
                        borderColor: '#1e293b'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#f8fafc', font: { family: 'Outfit' } } }
                    }
                }
            };
        }
        else if (key === 'train_raw' || key === 'train_balanced' || key === 'test_processed') {
            // Pie chart of label distribution (Normal vs Anomaly)
            const counts = { 'Normal (0)': 0, 'Anomalía (1)': 0 };
            data.rows.forEach(r => {
                const label = parseInt(r.etiqueta_anomalia) === 1 ? 'Anomalía (1)' : 'Normal (0)';
                counts[label]++;
            });
            chartConfig = {
                type: 'pie',
                data: {
                    labels: Object.keys(counts),
                    datasets: [{
                        data: Object.values(counts),
                        backgroundColor: ['#10b981', '#ef4444'],
                        borderWidth: 1,
                        borderColor: '#1e293b'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#f8fafc', font: { family: 'Outfit' } } }
                    }
                }
            };
        } 
        else if (key === 'bcrp_exchange') {
            // Line chart of exchange rate over time
            // Columns: "", "PN01205PM", "PN01206PM", "PN01207PM", etc.
            // Row has: Col_0 (mes like "May24"), "PN01207PM" (Promedio rate)
            const labels = [];
            const values = [];
            
            // BCRP columns: Col_0 is month, Col_3 (PN01207PM) is interbank average
            data.rows.forEach(r => {
                const month = r.Col_0 || r[''] || 'N/A';
                const rate = parseFloat(r['PN01207PM'] || r['Col_3']);
                if (month !== 'N/A' && !isNaN(rate)) {
                    labels.push(month);
                    values.push(rate);
                }
            });
            
            chartConfig = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tipo de cambio promedio interbancario (S/ por USD)',
                        data: values,
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: {
                        legend: { labels: { color: '#f8fafc' } }
                    }
                }
            };
        } 
        else if (key === 'faostat_prod') {
            // Bar chart of area harvested for top 8 crops
            const crops = {};
            data.rows.forEach(r => {
                const cropName = r.Item || 'N/A';
                const area = parseFloat(r.Value);
                if (cropName !== 'N/A' && r.Element === 'Area harvested' && !isNaN(area)) {
                    crops[cropName] = area;
                }
            });
            const sortedCrops = Object.entries(crops).sort((a, b) => b[1] - a[1]).slice(0, 8);
            chartConfig = {
                type: 'bar',
                data: {
                    labels: sortedCrops.map(c => c[0]),
                    datasets: [{
                        label: 'Área cosechada (Hectáreas) - 2024',
                        data: sortedCrops.map(c => c[1]),
                        backgroundColor: '#10b981',
                        borderWidth: 0,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 9 } } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            };
        } 
        else if (key === 'sunat_export') {
            // Bar chart comparing sectors
            // Look for non-traditional sectors
            const labels = ['Agropecuario', 'Textil', 'Quimico', 'Pesquero no trad.'];
            const values = [];
            
            data.rows.forEach(r => {
                const sector = (r.Col_0 || r[''] || '').toLowerCase();
                const totalVal = parseFloat((r.Total || '').replace(/,/g, ''));
                if (sector.includes('agropecuario') && !isNaN(totalVal)) values[0] = totalVal / 1000; // in millions
                if (sector.includes('textil') && !isNaN(totalVal)) values[1] = totalVal / 1000;
                if (sector.includes('quimico') && !isNaN(totalVal)) values[2] = totalVal / 1000;
                if (sector.includes('pesquero no tradicional') && !isNaN(totalVal)) values[3] = totalVal / 1000;
            });
            
            chartConfig = {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Exportaciones FOB Trimestre 2026 (Millones USD)',
                        data: values,
                        backgroundColor: '#fbbf24',
                        borderWidth: 0,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            };
        }
        else {
            // Default / hide chart for validated refs
            chartCard.style.display = 'none';
            return;
        }

        chartInstance = new Chart(ctx, chartConfig);
    }

    function renderTable() {
        document.getElementById('table-loading-container').style.display = 'none';
        document.getElementById('table-display-container').style.display = 'block';

        const head = document.getElementById('table-head');
        const body = document.getElementById('table-body');
        
        // 1. Render Header
        let headHtml = '<tr>';
        currentData.columns.forEach(col => {
            headHtml += `<th onclick="sortTable('${col}')">${col} ↕</th>`;
        });
        headHtml += '</tr>';
        head.innerHTML = headHtml;

        // 2. Paginate Rows
        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = Math.min(startIndex + pageSize, filteredRows.length);
        const paginatedRows = filteredRows.slice(startIndex, endIndex);

        // 3. Render Body
        let bodyHtml = '';
        if (paginatedRows.length === 0) {
            bodyHtml = `<tr><td colspan="${currentData.columns.length}" style="text-align:center; color:var(--muted); font-style:italic; padding:30px;">No se encontraron registros que coincidan con la búsqueda.</td></tr>`;
        } else {
            paginatedRows.forEach(row => {
                bodyHtml += '<tr>';
                currentData.columns.forEach(col => {
                    const val = row[col] !== undefined && row[col] !== null ? row[col] : '';
                    bodyHtml += `<td>${val}</td>`;
                });
                bodyHtml += '</tr>';
            });
        }
        body.innerHTML = bodyHtml;

        // 4. Update Pagination Controls
        const total = filteredRows.length;
        document.getElementById('page-indicator').innerText = total > 0 ? 
            `Mostrando ${startIndex + 1}-${endIndex} de ${total}` : 
            'Mostrando 0-0 de 0';

        document.getElementById('prev-btn').disabled = currentPage === 1;
        document.getElementById('next-btn').disabled = endIndex >= total;
    }

    function filterRows(term) {
        term = term.toLowerCase().trim();
        if (term === '') {
            filteredRows = [...currentData.rows];
        } else {
            filteredRows = currentData.rows.filter(row => {
                return currentData.columns.some(col => {
                    const val = String(row[col]).toLowerCase();
                    return val.includes(term);
                });
            });
        }
        currentPage = 1;
        renderTable();
    }

    let sortAsc = true;
    let lastSortedCol = '';
    function sortTable(col) {
        if (lastSortedCol === col) {
            sortAsc = !sortAsc;
        } else {
            sortAsc = true;
            lastSortedCol = col;
        }
        
        filteredRows.sort((a, b) => {
            let valA = a[col];
            let valB = b[col];
            
            // Check if they are numeric
            const numA = parseFloat(valA);
            const numB = parseFloat(valB);
            
            if (!isNaN(numA) && !isNaN(numB)) {
                return sortAsc ? numA - numB : numB - numA;
            }
            
            valA = String(valA).toLowerCase();
            valB = String(valB).toLowerCase();
            if (valA < valB) return sortAsc ? -1 : 1;
            if (valA > valB) return sortAsc ? 1 : -1;
            return 0;
        });
        
        currentPage = 1;
        renderTable();
    }

    function changePageSize(val) {
        pageSize = parseInt(val);
        currentPage = 1;
        renderTable();
    }

    function prevPage() {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    }

    function nextPage() {
        const total = filteredRows.length;
        if (currentPage * pageSize < total) {
            currentPage++;
            renderTable();
        }
    }

    // Load initial dataset on load
    window.onload = () => {
        loadDataset('synthetic_agro');
    };
</script>
</body>
</html>
"""

if __name__ == '__main__':
    import glob
    extra_md = glob.glob('/app/docs/*.md')
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        extra_files=extra_md
    )
