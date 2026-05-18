import os
import re
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Please install markdown: pip install markdown")
    exit(1)

def build_site():
    docs_dir = Path("docs")
    out_dir = Path("github_pages")
    ref_dir = out_dir / "referencias"
    
    out_dir.mkdir(parents=True, exist_ok=True)
    ref_dir.mkdir(parents=True, exist_ok=True)

    # Markdown extension setup
    md = markdown.Markdown(extensions=['tables', 'toc', 'fenced_code', 'nl2br'])

    # 1. Read files
    tesis_content = (docs_dir / "tesis.md").read_text(encoding="utf-8")
    ref_content = (docs_dir / "90-referencias.md").read_text(encoding="utf-8")

    # Remove the frontmatter if any (though tesis.md is combined and frontmatter might be at the top)
    if tesis_content.startswith("---"):
        tesis_content = re.sub(r"^---.*?---", "", tesis_content, flags=re.DOTALL)

    # 2. Convert to HTML
    tesis_html = md.convert(tesis_content)
    tesis_toc = md.toc

    md.reset()
    ref_html = md.convert(ref_content)

    # 3. HTML Template
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

@media (max-width: 1024px) {
    .layout { flex-direction: column; }
    .sidebar { width: 100%; height: auto; position: static; }
    .paper { padding: 2rem; }
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
});
"""
    (out_dir / "app.js").write_text(js_content, encoding="utf-8")

    print(f"✅ Github Pages built successfully in {out_dir.absolute()}!")

if __name__ == "__main__":
    build_site()
