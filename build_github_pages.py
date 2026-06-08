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
                <li><a href="{relative_root}/planeamiento.html">Planificación</a></li>
                <li class="dropdown">
                    <a href="javascript:void(0)" class="dropbtn" id="dropdownBtn">Avances de Datos e IA ▾</a>
                    <div class="dropdown-content" id="dropdownContent">
                        <a href="{relative_root}/diccionario-fuentes.html">Diccionario de Fuentes</a>
                        <a href="{relative_root}/calidad-datos.html">Calidad de Datos</a>
                        <a href="{relative_root}/entrenamiento-modelos.html">Modelos e IA</a>
                        <a href="{relative_root}/explicabilidad-shap.html">Explicabilidad SHAP</a>
                        <a href="{relative_root}/reformulacion-tesis.html">Reformulación de Tesis</a>
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

    # Write Proposal & Prototype from template file directly
    print("Generando página estática de la propuesta en GitHub Pages...")
    propuesta_tmpl_path = Path("src/templates/propuesta.html")
    if propuesta_tmpl_path.exists():
        propuesta_body = extract_body_from_template(propuesta_tmpl_path)
        # Adapt links & static resources
        propuesta_body = propuesta_body.replace('/seccion/', './index.html#')
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

    print("✅ Github Pages built successfully!")

if __name__ == "__main__":
    build_site()
