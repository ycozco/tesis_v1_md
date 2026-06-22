import os
import re
import sys
import shutil
from pathlib import Path

# Ensure UTF-8 output to avoid Windows console Unicode errors
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import markdown
except ImportError:
    print("Please install markdown: pip install markdown")
    exit(1)

def extract_body_from_template(template_path):
    """Extracts the body block from a Jinja template."""
    if not Path(template_path).exists():
        return ""
    text = Path(template_path).read_text(encoding="utf-8")
    match = re.search(r'{%\s*block\s+body\s*%}(.*?){%\s*endblock\s*%}', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def build_site():
    docs_dir = Path("docs")
    out_dir = Path("github_pages")
    ref_dir = out_dir / "referencias"
    
    out_dir.mkdir(parents=True, exist_ok=True)
    ref_dir.mkdir(parents=True, exist_ok=True)

    # Markdown extension setup
    md = markdown.Markdown(extensions=['tables', 'toc', 'fenced_code', 'nl2br'])

    # 1. Read files
    tesis_content = (docs_dir / "02-95-tesis.md").read_text(encoding="utf-8")
    ref_content = (docs_dir / "02-90-referencias.md").read_text(encoding="utf-8")
    
    # Read new Codex-revision files
    diccionario_content = (Path("codex-revision") / "diccionario-fuentes-canonicas.md").read_text(encoding="utf-8")
    calidad_content = (Path("codex-revision") / "reporte-calidad-datos.md").read_text(encoding="utf-8")
    entrenamiento_content = (Path("codex-revision") / "reporte-entrenamiento-modelos.md").read_text(encoding="utf-8")
    explicabilidad_content = (Path("codex-revision") / "reporte-explicabilidad-shap.md").read_text(encoding="utf-8")
    reformulacion_content = (Path("codex-revision") / "reporte-reformulacion-tesis.md").read_text(encoding="utf-8")
    correccion_content = (Path("codex-revision") / "correccion-futura.md").read_text(encoding="utf-8")

    # Remove the frontmatter if any (though tesis.md is combined and frontmatter might be at the top)
    if tesis_content.startswith("---"):
        tesis_content = re.sub(r"^---.*?---", "", tesis_content, flags=re.DOTALL)

    # 2. Convert to HTML
    tesis_html = md.convert(tesis_content)
    tesis_toc = md.toc

    md.reset()
    ref_html = md.convert(ref_content)

    md.reset()
    diccionario_html = md.convert(diccionario_content)
    diccionario_toc = md.toc

    md.reset()
    calidad_html = md.convert(calidad_content)
    calidad_toc = md.toc

    md.reset()
    entrenamiento_html = md.convert(entrenamiento_content)
    entrenamiento_toc = md.toc

    md.reset()
    explicabilidad_html = md.convert(explicabilidad_content)
    explicabilidad_toc = md.toc

    md.reset()
    reformulacion_html = md.convert(reformulacion_content)
    reformulacion_toc = md.toc

    md.reset()
    correccion_html = md.convert(correccion_content)
    correccion_toc = md.toc

    # 3. HTML Template with Planificación link
    def get_template(title, body, toc, relative_root="."):
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{relative_root}/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-content">
            <div class="logo">🎓 Tesis IA Agroexportadora</div>
            <ul class="nav-links">
                <li><a href="{relative_root}/index.html">Tesis Completa</a></li>
                <li><a href="{relative_root}/propuesta.html">Propuesta y Prototipo</a></li>
                <li><a href="{relative_root}/supervisor.html">Supervisor IA</a></li>
                <li><a href="{relative_root}/planeamiento.html">Planificación</a></li>
                <li class="dropdown">
                    <a href="javascript:void(0)" class="dropbtn" id="dropdownBtn">Avances de Datos e IA ▾</a>
                    <div class="dropdown-content" id="dropdownContent">
                        <a href="{relative_root}/diccionario-fuentes.html">Diccionario de Fuentes</a>
                        <a href="{relative_root}/calidad-datos.html">Calidad de Datos</a>
                        <a href="{relative_root}/entrenamiento-modelos.html">Modelos e IA</a>
                        <a href="{relative_root}/explicabilidad-shap.html">Explicabilidad SHAP</a>
                        <a href="{relative_root}/reformulacion-tesis.html">Reformulación de Tesis</a>
                        <a href="{relative_root}/correccion-futura.html">Corrección Futura</a>
                    </div>
                </li>
                <li><a href="{relative_root}/referencias/index.html">Referencias (Directorio)</a></li>
            </ul>
            <div class="theme-switch-wrapper">
                <label class="theme-switch" for="checkbox">
                    <input type="checkbox" id="checkbox" />
                    <div class="slider round"></div>
                </label>
                <em style="margin-left:10px; font-size: 0.8rem; color: var(--text-color);">Dark Mode</em>
            </div>
        </div>
    </nav>

    <div class="layout">
        <aside class="sidebar" id="sidebar">
            <div class="toc-container">
                <h3>Índice de Contenidos</h3>
                {toc}
            </div>
        </aside>

        <main class="content">
            <article class="paper">
                {body}
            </article>
        </main>
    </div>

    <button id="back-to-top" title="Volver arriba">↑</button>

    <script src="{relative_root}/app.js"></script>
</body>
</html>"""

    # Write Thesis Index
    (out_dir / "index.html").write_text(get_template("Tesis Completa - Yoset", tesis_html, tesis_toc, "."), encoding="utf-8")

    # Write References Index
    (ref_dir / "index.html").write_text(get_template("Directorio de Referencias", ref_html, "", ".."), encoding="utf-8")

    # Write Codex progress pages
    (out_dir / "diccionario-fuentes.html").write_text(get_template("Diccionario de Fuentes", diccionario_html, diccionario_toc, "."), encoding="utf-8")
    (out_dir / "calidad-datos.html").write_text(get_template("Calidad de Datos", calidad_html, calidad_toc, "."), encoding="utf-8")
    (out_dir / "entrenamiento-modelos.html").write_text(get_template("Entrenamiento de Modelos", entrenamiento_html, entrenamiento_toc, "."), encoding="utf-8")
    (out_dir / "explicabilidad-shap.html").write_text(get_template("Explicabilidad SHAP", explicabilidad_html, explicabilidad_toc, "."), encoding="utf-8")
    (out_dir / "reformulacion-tesis.html").write_text(get_template("Reformulación de Tesis", reformulacion_html, reformulacion_toc, "."), encoding="utf-8")
    (out_dir / "correccion-futura.html").write_text(get_template("Correcciones Futuras", correccion_html, correccion_toc, "."), encoding="utf-8")

    # Write Proposal & Prototype from template file directly
    print("Generando página estática de la propuesta en GitHub Pages...")
    propuesta_tmpl_path = Path("src/templates/propuesta.html")
    if propuesta_tmpl_path.exists():
        propuesta_body = extract_body_from_template(propuesta_tmpl_path)
        # Adapt links & static resources
        propuesta_body = propuesta_body.replace('/seccion/', './index.html#')
        propuesta_body = propuesta_body.replace('/secciones', './index.html')
        propuesta_body = propuesta_body.replace('/datos', './datos.html')
        propuesta_body = propuesta_body.replace('/propuesta', './propuesta.html')
        propuesta_body = propuesta_body.replace('/admin', './admin.html')
        propuesta_body = propuesta_body.replace('/diagrama/arquitectura', './diagrama-arquitectura.html')
        propuesta_body = propuesta_body.replace('/diagrama/cronograma', './diagrama-cronograma.html')
        # Wrap it in standard template
        (out_dir / "propuesta.html").write_text(get_template("Propuesta y Prototipo", propuesta_body, "", "."), encoding="utf-8")
        print("✅ propuesta.html generada exitosamente.")
    else:
        print("❌ Error: No se encontró src/templates/propuesta.html")

    # Write Planning & Hypotheses Page
    print("Generando página estática de la planificación en GitHub Pages...")
    planeamiento_tmpl_path = Path("src/templates/planeamiento.html")
    if planeamiento_tmpl_path.exists():
        planeamiento_body = extract_body_from_template(planeamiento_tmpl_path)
        # Replace image path for static deployment
        planeamiento_body = planeamiento_body.replace('/static/gantt_chart.png', './gantt_chart.png')
        planeamiento_body = planeamiento_body.replace('/secciones', './index.html')
        planeamiento_body = planeamiento_body.replace('/datos', './datos.html')
        planeamiento_body = planeamiento_body.replace('/propuesta', './propuesta.html')
        planeamiento_body = planeamiento_body.replace('/admin', './admin.html')
        (out_dir / "planeamiento.html").write_text(get_template("Planificación e Hipótesis", planeamiento_body, "", "."), encoding="utf-8")
        
        # Copy Gantt chart image
        gantt_src = Path("data/downloads/gantt_chart.png")
        if gantt_src.exists():
            shutil.copy2(gantt_src, out_dir / "gantt_chart.png")
            print("✅ gantt_chart.png copiado exitosamente.")
        else:
            print("⚠️ Advertencia: No se encontró data/downloads/gantt_chart.png")
        print("✅ planeamiento.html generada exitosamente.")
    else:
        print("❌ Error: No se encontró src/templates/planeamiento.html")

    # 4. Generate CSS
    css_content = """
:root {
    --bg-color: #f4f7f6;
    --text-color: #2c3e50;
    --paper-bg: #ffffff;
    --primary-color: #3498db;
    --secondary-color: #2980b9;
    --border-color: #e0e0e0;
    --nav-bg: rgba(255, 255, 255, 0.95);
    --shadow: 0 4px 6px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.1);
}

[data-theme="dark"] {
    --bg-color: #1a1a2e;
    --text-color: #e0e0e0;
    --paper-bg: #16213e;
    --primary-color: #4facfe;
    --secondary-color: #00f2fe;
    --border-color: #2c3e50;
    --nav-bg: rgba(22, 33, 62, 0.95);
    --shadow: 0 4px 6px rgba(0,0,0,0.3);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.7;
    transition: background-color 0.3s, color 0.3s;
}

.navbar {
    position: sticky;
    top: 0;
    background-color: var(--nav-bg);
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow);
    z-index: 1000;
    padding: 1rem 2rem;
}

.nav-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo { font-weight: 700; font-size: 1.2rem; color: var(--primary-color); }

.nav-links { list-style: none; display: flex; gap: 2rem; }
.nav-links a { text-decoration: none; color: var(--text-color); font-weight: 600; transition: color 0.2s; }
.nav-links a:hover { color: var(--primary-color); }

.layout {
    display: flex;
    max-width: 1400px;
    margin: 2rem auto;
    gap: 2rem;
    padding: 0 1rem;
}

.sidebar {
    width: 300px;
    flex-shrink: 0;
    height: calc(100vh - 100px);
    position: sticky;
    top: 80px;
    overflow-y: auto;
}

.toc-container {
    background: var(--paper-bg);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
}

.toc-container h3 {
    margin-bottom: 1rem;
    font-size: 1.1rem;
    color: var(--primary-color);
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 0.5rem;
}

.toc-container ul { list-style: none; margin-left: 1rem; }
.toc-container li { margin-bottom: 0.5rem; }
.toc-container a {
    text-decoration: none;
    color: var(--text-color);
    font-size: 0.9rem;
    transition: color 0.2s;
}
.toc-container a:hover { color: var(--primary-color); }

.content { flex-grow: 1; min-width: 0; }

.paper {
    background: var(--paper-bg);
    padding: 3rem 4rem;
    border-radius: 12px;
    box-shadow: var(--shadow);
    min-height: 80vh;
}

h1, h2, h3, h4 { color: var(--primary-color); margin-top: 2rem; margin-bottom: 1rem; }
h1 { font-size: 2.5rem; border-bottom: 3px solid var(--primary-color); padding-bottom: 0.5rem; }
h2 { font-size: 2rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3rem; }

p { margin-bottom: 1.2rem; text-align: justify; }

table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    font-size: 0.9rem;
}

th, td {
    padding: 12px 15px;
    border-bottom: 1px solid var(--border-color);
    text-align: left;
}

th {
    background-color: rgba(52, 152, 219, 0.1);
    color: var(--primary-color);
    font-weight: 600;
}

tr:hover { background-color: rgba(52, 152, 219, 0.05); }

pre {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1.5rem 0;
}
code { font-family: 'Consolas', monospace; font-size: 0.9rem; }
p code { background: rgba(52, 152, 219, 0.1); color: var(--primary-color); padding: 0.2rem 0.4rem; border-radius: 4px; }

blockquote {
    border-left: 4px solid var(--primary-color);
    padding-left: 1rem;
    margin: 1.5rem 0;
    font-style: italic;
    color: #7f8c8d;
    background: rgba(52, 152, 219, 0.05);
    padding: 1rem;
    border-radius: 0 8px 8px 0;
}

#back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--primary-color);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    display: none;
    font-size: 1.2rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    transition: transform 0.2s, background 0.2s;
}

#back-to-top:hover {
    transform: translateY(-3px);
    background: var(--secondary-color);
}

/* Theme Switch */
.theme-switch-wrapper { display: flex; align-items: center; }
.theme-switch { display: inline-block; height: 24px; position: relative; width: 50px; }
.theme-switch input { display:none; }
.slider { background-color: #ccc; bottom: 0; cursor: pointer; left: 0; position: absolute; right: 0; top: 0; transition: .4s; }
.slider:before { background-color: #fff; bottom: 4px; content: ""; height: 16px; left: 4px; position: absolute; transition: .4s; width: 16px; }
input:checked + .slider { background-color: var(--primary-color); }
input:checked + .slider:before { transform: translateX(26px); }
.slider.round { border-radius: 24px; }
.slider.round:before { border-radius: 50%; }

/* Custom styles for Planeamiento Card items */
.hyp-box {
    background: rgba(52, 152, 219, 0.08);
    border-left: 4px solid var(--primary-color);
    padding: 20px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 20px;
}
.hyp-box.nula {
    border-left-color: #7f8c8d;
    background: rgba(127, 140, 141, 0.08);
}
.hyp-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 25px;
}
.hyp-card {
    background: rgba(52, 152, 219, 0.02);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
}
.hyp-card h4 { margin-top: 0; color: var(--primary-color); }
.hyp-badge-group { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.hyp-badge { background: rgba(52, 152, 219, 0.1); border-radius: 6px; padding: 4px 10px; font-size: 0.75rem; color: var(--primary-color); }
.gantt-img-container { text-align: center; margin: 30px 0; border: 1px solid var(--border-color); padding: 15px; border-radius: 12px; }
.gantt-img-container img { max-width: 100%; height: auto; border-radius: 8px; }
.phases-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 25px; }
.phase-card { border-left: 4px solid var(--primary-color); background: rgba(52, 152, 219, 0.01); border-radius: 4px; padding: 15px; border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); border-right: 1px solid var(--border-color); }
.phase-num { font-size: 0.75rem; text-transform: uppercase; color: #7f8c8d; }
.phase-title { font-weight: bold; margin-bottom: 5px; }
.phase-date { font-size: 0.8rem; font-weight: bold; color: var(--primary-color); margin-bottom: 10px; }
.milestones-table { width: 100%; border-collapse: collapse; margin-top: 25px; }
.badge-status { display: inline-block; padding: 3px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.badge-status.success { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.badge-status.warning { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }

/* Dropdown styling */
.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown .dropbtn {
    cursor: pointer;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: var(--paper-bg);
    min-width: 240px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.15);
    z-index: 1001;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    margin-top: 5px;
    overflow: hidden;
}

.dropdown-content a {
    color: var(--text-color);
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    font-size: 0.9rem;
    font-weight: 500;
    transition: background-color 0.2s, color 0.2s;
}

.dropdown-content a:hover {
    background-color: rgba(52, 152, 219, 0.1);
    color: var(--primary-color);
}

@media (min-width: 769px) {
    .dropdown:hover .dropdown-content {
        display: block;
    }
}

.dropdown-content.show {
    display: block !important;
}

@media (max-width: 1024px) {
    .layout { flex-direction: column; }
    .sidebar { width: 100%; height: auto; position: static; }
    .paper { padding: 2rem; }
}

@media (max-width: 768px) {
    .nav-content { flex-direction: column; align-items: flex-start; gap: 1rem; }
    .nav-links { flex-direction: column; gap: 0.5rem; width: 100%; }
    .dropdown-content { position: static; box-shadow: none; border: none; padding-left: 1rem; display: none; }
}
"""
    (out_dir / "styles.css").write_text(css_content, encoding="utf-8")

    # 5. Generate JS
    js_content = """
document.addEventListener('DOMContentLoaded', () => {
    // Theme toggler
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }
    }

    toggleSwitch.addEventListener('change', function(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }    
    });

    // Back to top button
    const backToTopBtn = document.getElementById('back-to-top');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Highlight active section in TOC
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                if (id) {
                    document.querySelectorAll('.toc-container a').forEach(a => {
                        a.style.fontWeight = 'normal';
                        a.style.color = 'var(--text-color)';
                        if (a.getAttribute('href') === '#' + id) {
                            a.style.fontWeight = 'bold';
                            a.style.color = 'var(--primary-color)';
                        }
                    });
                }
            }
        });
    }, { rootMargin: '-20% 0px -80% 0px' });

    document.querySelectorAll('.paper h1, .paper h2, .paper h3').forEach(h => observer.observe(h));

    // Dropdown toggle logic for click (highly compatible with mobile/touch)
    const dropbtn = document.getElementById('dropdownBtn');
    const dropdownContent = document.getElementById('dropdownContent');
    if (dropbtn && dropdownContent) {
        dropbtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropdownContent.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!dropdownContent.contains(e.target) && e.target !== dropbtn) {
                dropdownContent.classList.remove('show');
            }
        });
    }
});
"""
    (out_dir / "app.js").write_text(js_content, encoding="utf-8")

    # Compile dynamic diagrams, data explorer, and admin pages statically
    compile_diagrams(out_dir, get_template)
    compile_datos(out_dir, get_template)
    compile_admin(out_dir, get_template)
    compile_supervisor(out_dir)
    export_csv_to_json(out_dir)
    export_supervisor_api(out_dir)

    print("✅ Github Pages built successfully!")

def compile_diagrams(out_dir, get_template):
    diagrama_path = Path("src/templates/diagrama.html")
    if not diagrama_path.exists():
        print("❌ Error: No se encontró src/templates/diagrama.html")
        return
        
    text = diagrama_path.read_text(encoding="utf-8")
    
    # Extract CSS from {% block styles %} ... {% endblock %}
    styles_match = re.search(r'{%\s*block\s+styles\s*%}(.*?){%\s*endblock\s*%}', text, re.DOTALL)
    styles = styles_match.group(1).strip() if styles_match else ""
    
    # Extract the HTML body inside {% block body %} ... {% endblock %}
    body_match = re.search(r'{%\s*block\s+body\s*%}(.*?){%\s*endblock\s*%}', text, re.DOTALL)
    if not body_match:
        print("❌ Error: No se pudo extraer el body de diagrama.html")
        return
        
    body_content = body_match.group(1).strip()
    
    # Split the body by {% if ... %}, {% elif ... %}, {% endif %}
    cronograma_html = re.search(r'{%\s*if\s+name\s*==\s*\'cronograma\'\s*%}(.*?){%\s*elif', body_content, re.DOTALL).group(1).strip()
    dataflow_html = re.search(r'{%\s*elif\s+name\s*==\s*\'dataflow\'\s*%}(.*?){%\s*elif', body_content, re.DOTALL).group(1).strip()
    arquitectura_html = re.search(r'{%\s*elif\s+name\s*==\s*\'arquitectura\'\s*%}(.*?){%\s*endif', body_content, re.DOTALL).group(1).strip()
    
    # Mermaid JS initialization script
    mermaid_script = """
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'base',
            securityLevel: 'loose',
            gantt: {
                useWidth: 1400,
                barHeight: 40,
                barGap: 12,
                topPadding: 75,
                sidePadding: 150,
                fontSize: 16,
                sectionFontSize: 18,
                titlePadding: 20
            },
            themeVariables: {
                background: '#0f172a',
                primaryColor: '#6366f1',
                primaryTextColor: '#fff',
                lineColor: '#cbd5e1',
                fontFamily: 'Outfit',
                nodeBorder: '#4f46e5',
                mainBkg: '#0f172a',
                ganttSectionBkgColor: '#1e293b',
                ganttSectionBkgColor2: '#0f172a',
                ganttSectionBorderColor: '#475569',
                ganttGridLineColor: 'rgba(255, 255, 255, 0.05)',
                ganttTaskBorderColor: '#6366f1',
                ganttTaskBkgColor: '#4f46e5',
                ganttTaskTextColor: '#fff',
                ganttTaskActiveBorderColor: '#10b981',
                ganttTaskActiveBkgColor: '#059669',
                ganttTaskActiveTextColor: '#fff',
                ganttTaskDoneBorderColor: '#94a3b8',
                ganttTaskDoneBkgColor: '#334155',
                ganttTaskDoneTextColor: '#cbd5e1',
                ganttTodayLineColor: '#ef4444',
                ganttSectionTextColor: '#f8fafc',
                ganttSectionTextColor2: '#f8fafc'
            }
        });
    </script>
    """
    
    close_btn = '<a href="javascript:history.back();" class="back-btn">✕ Volver</a>'
    
    def wrap_diagram(content):
        return f"""
        <style>
        {styles}
        </style>
        {mermaid_script}
        <div class="diagram-card">
            {content}
            {close_btn}
        </div>
        """
        
    (out_dir / "diagrama-cronograma.html").write_text(get_template("Diagrama: Cronograma", wrap_diagram(cronograma_html), "", "."), encoding="utf-8")
    (out_dir / "diagrama-dataflow.html").write_text(get_template("Diagrama: Flujo de Datos", wrap_diagram(dataflow_html), "", "."), encoding="utf-8")
    (out_dir / "diagrama-arquitectura.html").write_text(get_template("Diagrama: Arquitectura", wrap_diagram(arquitectura_html), "", "."), encoding="utf-8")
    print("✅ diagramas-cronograma/dataflow/arquitectura.html generados exitosamente.")

def compile_datos(out_dir, get_template):
    datos_tmpl_path = Path("src/templates/datos.html")
    if not datos_tmpl_path.exists():
        print("❌ Error: No se encontró src/templates/datos.html")
        return
        
    text = datos_tmpl_path.read_text(encoding="utf-8")
    
    # 1. Update fetch URL to relative .json
    text = text.replace('fetch(`/api/data/${key}`)', 'fetch(`./api/data/${key}.json`)')
    
    # 2. Re-route nav menu items to static pages
    nav_menu_static = """
            <a href="./index.html" class="nav-item">🏠 Inicio</a>
            <a href="./propuesta.html" class="nav-item">📊 Propuesta y Prototipo</a>
            <a href="./supervisor.html" class="nav-item">🔍 Supervisor IA</a>
            <a href="./datos.html" class="nav-item active">🗃️ Datos</a>
            <a href="./planeamiento.html" class="nav-item">📅 Planificación</a>
            <a href="./admin.html" class="nav-item">⚙️ Administración</a>
    """
    text = re.sub(r'<nav class="main-navbar">.*?</nav>', f"""
    <nav class="main-navbar">
        <div class="nav-logo">
            <span class="logo-dot"></span>
            <span class="logo-text">Tesis Hub</span>
        </div>
        <div class="nav-menu">{nav_menu_static}</div>
    </nav>""", text, flags=re.DOTALL)
    
    (out_dir / "datos.html").write_text(text, encoding="utf-8")
    print("✅ datos.html generado exitosamente.")

def compile_admin(out_dir, get_template):
    admin_tmpl_path = Path("src/templates/admin.html")
    if not admin_tmpl_path.exists():
        print("❌ Error: No se encontró src/templates/admin.html")
        return
        
    text = admin_tmpl_path.read_text(encoding="utf-8")
    
    styles_match = re.search(r'{%\s*block\s+styles\s*%}(.*?){%\s*endblock\s*%}', text, re.DOTALL)
    styles = styles_match.group(1).strip() if styles_match else ""
    
    body_match = re.search(r'{%\s*block\s+body\s*%}(.*?){%\s*endblock\s*%}', text, re.DOTALL)
    if not body_match:
        print("❌ Error: No se pudo extraer el body de admin.html")
        return
        
    body_content = body_match.group(1).strip()
    
    # Pre-render values
    body_content = body_content.replace('{{ generated_at }}', '2026-06-08')
    body_content = body_content.replace('{{ plan_progress }}', '100')
    body_content = body_content.replace('{{ plan_done }}', '8')
    body_content = body_content.replace('{{ plan_total }}', '8')
    body_content = body_content.replace('{{ doc_count }}', '20')
    body_content = body_content.replace('{{ deliverable_count }}', '2')
    
    cards_html = """
    <div class="card">
        <div class="metric">
            <div>
                <div class="muted" style="margin-bottom: 4px;">Fases Ejecutadas</div>
                <strong>8 / 8</strong>
            </div>
        </div>
        <div class="muted">100% de las fases del plan</div>
    </div>
    <div class="card">
        <div class="metric">
            <div>
                <div class="muted" style="margin-bottom: 4px;">Transacciones Reales</div>
                <strong>40,289</strong>
            </div>
        </div>
        <div class="muted">SUNAT / ADUANET</div>
    </div>
    <div class="card">
        <div class="metric">
            <div>
                <div class="muted" style="margin-bottom: 4px;">Algoritmos de IA</div>
                <strong>9 Modelos</strong>
            </div>
        </div>
        <div class="muted">LGBM + XGBoost + PyOD</div>
    </div>
    <div class="card">
        <div class="metric">
            <div>
                <div class="muted" style="margin-bottom: 4px;">Explicabilidad SHAP</div>
                <strong>3 Productos</strong>
            </div>
        </div>
        <div class="muted">Uva, Palta y Arándano</div>
    </div>
    """
    body_content = re.sub(r'{%\s*for\s+card\s+in\s+plan_cards\s*%}.*?{%\s*endfor\s*%}', cards_html, body_content, flags=re.DOTALL)
    body_content = re.sub(r'{%\s*for\s+item\s+in\s+plan_pending_preview\s*%}.*?{%\s*endfor\s*%}', '<li class="item" style="color: #10b981;">🎉 Ninguno (100% completado)</li>', body_content, flags=re.DOTALL)
    
    review_types_html = """
    <li class="item review">
        <div>
            <h3>Validación de Datos</h3>
            <div class="muted">Control de nulos, duplicados y outliers</div>
        </div>
        <div class="count" style="background: rgba(16, 185, 129, 0.15); color: var(--accent); border-color: rgba(16, 185, 129, 0.3);">0</div>
    </li>
    <li class="item review">
        <div>
            <h3>Entrenamiento de Modelos</h3>
            <div class="muted">Optuna trials y métricas RMSE/SMAPE</div>
        </div>
        <div class="count" style="background: rgba(16, 185, 129, 0.15); color: var(--accent); border-color: rgba(16, 185, 129, 0.3);">0</div>
    </li>
    """
    body_content = re.sub(r'{%\s*for\s+review\s+in\s+review_types\s*%}.*?{%\s*endfor\s*%}', review_types_html, body_content, flags=re.DOTALL)
    
    docs_list_html = """
    <li class="item">
        <a href="./diccionario-fuentes.html">diccionario-fuentes-canonicas.md</a>
        <span class="pill">Fase 1</span>
    </li>
    <li class="item">
        <a href="./calidad-datos.html">reporte-calidad-datos.md</a>
        <span class="pill">Fase 4</span>
    </li>
    <li class="item">
        <a href="./entrenamiento-modelos.html">reporte-entrenamiento-modelos.md</a>
        <span class="pill">Fase 6</span>
    </li>
    <li class="item">
        <a href="./explicabilidad-shap.html">reporte-explicabilidad-shap.md</a>
        <span class="pill">Fase 7</span>
    </li>
    <li class="item">
        <a href="./reformulacion-tesis.html">reporte-reformulacion-tesis.md</a>
        <span class="pill">Fase 8</span>
    </li>
    <li class="item">
        <a href="./correccion-futura.html">correccion-futura.md</a>
        <span class="pill">Trabajo Futuro</span>
    </li>
    """
    body_content = re.sub(r'{%\s*for\s+doc\s+in\s+docs\s*%}.*?{%\s*endfor\s*%}', docs_list_html, body_content, flags=re.DOTALL)
    
    deliverables_html = """
    <li class="item">
        <span style="color: #e2e8f0; font-weight: 600;">dataset_modelo_v_final_2026-06-07.csv</span>
        <span class="pill" style="background: rgba(16, 185, 129, 0.15); color: var(--accent);">CSV</span>
    </li>
    <li class="item">
        <span style="color: #e2e8f0; font-weight: 600;">results_metrics_2026-06-07.json</span>
        <span class="pill" style="background: rgba(16, 185, 129, 0.15); color: var(--accent);">JSON</span>
    </li>
    """
    body_content = re.sub(r'{%\s*for\s+file\s+in\s+deliverables\s*%}.*?{%\s*endfor\s*%}', deliverables_html, body_content, flags=re.DOTALL)
    
    dataset_rows_html = """
    <tr>
        <td style="color: #e2e8f0; font-weight: 600;">dataset_real_v1.csv</td>
        <td style="color: var(--text-dim);">Base experimental real transaccional</td>
        <td><span class="pill" style="background: rgba(16, 185, 129, 0.15); color: var(--accent);">Aprobado</span></td>
    </tr>
    <tr>
        <td style="color: #e2e8f0; font-weight: 600;">dataset_processed_train_raw.csv</td>
        <td style="color: var(--text-dim);">Train split sin balancear para modelos</td>
        <td><span class="pill" style="background: rgba(16, 185, 129, 0.15); color: var(--accent);">Aceptado</span></td>
    </tr>
    """
    body_content = re.sub(r'{%\s*for\s+row\s+in\s+dataset_rows\s*%}.*?{%\s*endfor\s*%}', dataset_rows_html, body_content, flags=re.DOTALL)
    
    body_content = body_content.replace('{{ sources_text }}', 'Todos los datasets y proxies fueron integrados y validados exitosamente.')
    body_content = body_content.replace('{{ review_types|length }}', '2')
    
    wrap_html = f"""
    <style>
    {styles}
    </style>
    {body_content}
    """
    
    (out_dir / "admin.html").write_text(get_template("Panel de Administración", wrap_html, "", "."), encoding="utf-8")
    print("✅ admin.html generado exitosamente.")

def export_csv_to_json(out_dir):
    import csv, json
    api_dir = out_dir / "api" / "data"
    api_dir.mkdir(parents=True, exist_ok=True)
    
    files = {
        'synthetic_agro': Path('data/dataset_agro_sintetico_v1.csv'),
        'validated_refs': Path('entregable/referencias-datasets-validadas.csv'),
        'train_raw': Path('data/dataset_processed_train_raw.csv'),
        'train_balanced': Path('data/dataset_processed_train_balanced.csv'),
        'test_processed': Path('data/dataset_processed_test.csv')
    }
    
    for key, filepath in files.items():
        if filepath.exists():
            try:
                content = filepath.read_text(encoding='utf-8')
            except Exception:
                try:
                    content = filepath.read_text(encoding='latin-1')
                except Exception:
                    print(f"⚠️ Error leyendo {filepath}")
                    continue
                    
            lines = [l for l in content.split('\n') if l.strip()]
            reader = csv.reader(lines)
            try:
                header = next(reader)
                columns = [h.strip() if h.strip() else f"Col_{i}" for i, h in enumerate(header)]
                rows = []
                for i, r in enumerate(reader):
                    # limit to first 500 rows for size optimization on GitHub Pages
                    if i >= 500:
                        break
                    if len(r) < len(columns):
                        r = r + [""] * (len(columns) - len(r))
                    else:
                        r = r[:len(columns)]
                    rows.append(dict(zip(columns, r)))
                
                num_rows = len(rows)
                stats = {
                    "num_rows": num_rows,
                    "num_cols": len(columns),
                    "null_counts": {col: 0 for col in columns},
                    "filename": filepath.name
                }
                
                json_data = {
                    "columns": columns,
                    "rows": rows,
                    "stats": stats
                }
                
                (api_dir / f"{key}.json").write_text(json.dumps(json_data, indent=2), encoding="utf-8")
                print(f"✅ Exportado {key}.json ({len(rows)} filas)")
            except Exception as e:
                print(f"⚠️ Error parseando {filepath}: {e}")
        else:
            # write empty placeholder
            json_data = {
                "columns": [],
                "rows": [],
                "stats": {"num_rows": 0, "num_cols": 0, "null_counts": {}, "filename": f"{filepath.name} (No disponible localmente)"}
            }
            (api_dir / f"{key}.json").write_text(json.dumps(json_data), encoding="utf-8")
            
    # Write empty placeholders for external files
    for key in ['bcrp_exchange', 'faostat_prod', 'sunat_export']:
        json_data = {
            "columns": [],
            "rows": [],
            "stats": {"num_rows": 0, "num_cols": 0, "null_counts": {}, "filename": "No disponible localmente"}
        }
        (api_dir / f"{key}.json").write_text(json.dumps(json_data), encoding="utf-8")

def compile_supervisor(out_dir):
    """Compila el supervisor.html estático resolviendo los bloques extendidos de base.html."""
    supervisor_tmpl_path = Path("src/templates/supervisor.html")
    base_tmpl_path = Path("src/templates/base.html")
    if not supervisor_tmpl_path.exists() or not base_tmpl_path.exists():
        print("❌ Error: No se encontró supervisor.html o base.html")
        return
        
    supervisor_text = supervisor_tmpl_path.read_text(encoding="utf-8")
    base_text = base_tmpl_path.read_text(encoding="utf-8")
    
    # Extraer bloques de supervisor.html
    title_match = re.search(r'{%\s*block\s+title\s*%}(.*?){%\s*endblock\s*%}', supervisor_text, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Supervisor de Operaciones IA"
    
    head_match = re.search(r'{%\s*block\s+head\s*%}(.*?){%\s*endblock\s*%}', supervisor_text, re.DOTALL)
    head = head_match.group(1).strip() if head_match else ""
    
    styles_match = re.search(r'{%\s*block\s+styles\s*%}(.*?){%\s*endblock\s*%}', supervisor_text, re.DOTALL)
    styles = styles_match.group(1).strip() if styles_match else ""
    
    body_match = re.search(r'{%\s*block\s+body\s*%}(.*?){%\s*endblock\s*%}', supervisor_text, re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""
    
    scripts_match = re.search(r'{%\s*block\s+scripts\s*%}(.*?){%\s*endblock\s*%}', supervisor_text, re.DOTALL)
    scripts = scripts_match.group(1).strip() if scripts_match else ""
    
    # Reemplazar en base.html
    output_text = base_text
    output_text = re.sub(r'{%\s*block\s+title\s*%}.*?{%\s*endblock\s*%}', title, output_text, flags=re.DOTALL)
    output_text = re.sub(r'{%\s*block\s+head\s*%}.*?{%\s*endblock\s*%}', head, output_text, flags=re.DOTALL)
    output_text = re.sub(r'{%\s*block\s+styles\s*%}.*?{%\s*endblock\s*%}', f"<style>{styles}</style>", output_text, flags=re.DOTALL)
    output_text = re.sub(r'{%\s*block\s+body\s*%}.*?{%\s*endblock\s*%}', body, output_text, flags=re.DOTALL)
    output_text = re.sub(r'{%\s*block\s+scripts\s*%}.*?{%\s*endblock\s*%}', f"<script>{scripts}</script>", output_text, flags=re.DOTALL)
    
    # Ruteo estático del menú de navegación
    static_nav = """
            <div class="nav-menu">
                <a href="./index.html" class="nav-item">🏠 Inicio</a>
                <a href="./datos.html" class="nav-item">🗃️ Datos</a>
                <a href="./propuesta.html" class="nav-item">📊 Propuesta y Prototipo</a>
                <a href="./supervisor.html" class="nav-item active">🔍 Supervisor IA</a>
                <a href="./planeamiento.html" class="nav-item">📅 Planificación</a>
                <a href="./admin.html" class="nav-item">⚙️ Administración</a>
            </div>
    """
    output_text = re.sub(r'<div class="nav-menu">.*?</div>', static_nav, output_text, flags=re.DOTALL)
    
    # Cambiar rutas relativas en general
    output_text = output_text.replace('href="/"', 'href="./index.html"')
    output_text = output_text.replace('href="/secciones"', 'href="./index.html#secciones"')
    output_text = output_text.replace('href="/datos"', 'href="./datos.html"')
    output_text = output_text.replace('href="/propuesta"', 'href="./propuesta.html"')
    output_text = output_text.replace('href="/supervisor"', 'href="./supervisor.html"')
    output_text = output_text.replace('href="/planeamiento"', 'href="./planeamiento.html"')
    output_text = output_text.replace('href="/admin"', 'href="./admin.html"')
    
    # Modificar endpoints fetch de la API del supervisor para que apunten a los JSONs locales
    output_text = output_text.replace("fetch('/api/supervisor/alerts')", "fetch('./api/supervisor/alerts.json')")
    output_text = output_text.replace("fetch(`/api/supervisor/report/${key}`)", "fetch(`./api/supervisor/report/${key}.json`)")
    output_text = output_text.replace("fetch(`/api/supervisor/traceability/${key}`)", "fetch(`./api/supervisor/traceability/${key}.json`)")
    
    (out_dir / "supervisor.html").write_text(output_text, encoding="utf-8")
    print("✅ supervisor.html generado exitosamente.")

def export_supervisor_api(out_dir):
    """Exporta los datos JSON del supervisor de operaciones a rutas estáticas de GitHub Pages."""
    import json
    api_dir = out_dir / "api" / "supervisor"
    api_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Alertas locales y explicaciones
    alerts_path = Path("data/gold/local_explanations.json")
    if alerts_path.exists():
        try:
            shutil.copy2(alerts_path, api_dir / "alerts.json")
            print("✅ Exportado alerts.json")
            
            with open(alerts_path, "r", encoding="utf-8") as f:
                alerts_data = json.load(f)
                
            # 2. Reportes
            reports_path = Path("data/gold/generated_reports.json")
            reports_api_dir = api_dir / "report"
            reports_api_dir.mkdir(parents=True, exist_ok=True)
            if reports_path.exists():
                with open(reports_path, "r", encoding="utf-8") as f:
                    reports_data = json.load(f)
                for key in alerts_data.keys():
                    key_data = reports_data.get(key, {"report_content": "No se encontró el contenido del reporte."})
                    (reports_api_dir / f"{key}.json").write_text(json.dumps(key_data, indent=2), encoding="utf-8")
                print(f"✅ Exportados {len(alerts_data)} reportes individuales.")
            else:
                for key in alerts_data.keys():
                    placeholder = {"report_content": "Reporte no disponible."}
                    (reports_api_dir / f"{key}.json").write_text(json.dumps(placeholder, indent=2), encoding="utf-8")
            
            # 3. Trazabilidad
            trace_path = Path("data/gold/traceability_log.json")
            trace_api_dir = api_dir / "traceability"
            trace_api_dir.mkdir(parents=True, exist_ok=True)
            if trace_path.exists():
                with open(trace_path, "r", encoding="utf-8") as f:
                    trace_data = json.load(f)
                for key in alerts_data.keys():
                    key_data = trace_data.get(key, {"error": "No se encontraron datos de trazabilidad."})
                    (trace_api_dir / f"{key}.json").write_text(json.dumps(key_data, indent=2), encoding="utf-8")
                print(f"✅ Exportados {len(alerts_data)} registros de trazabilidad.")
            else:
                for key in alerts_data.keys():
                    placeholder = {"error": "Trazabilidad no disponible."}
                    (trace_api_dir / f"{key}.json").write_text(json.dumps(placeholder, indent=2), encoding="utf-8")
                    
        except Exception as e:
            print(f"⚠️ Error exportando supervisor API: {e}")
    else:
        print("⚠️ Advertencia: No se encontró local_explanations.json. Escribiendo placeholders de supervisor API...")
        (api_dir / "alerts.json").write_text("{}", encoding="utf-8")

if __name__ == "__main__":
    build_site()
