#!/usr/bin/env python3
"""
Visor de tesis - Servidor HTTP simple para Markdown
Genera HTML a partir de Markdown y lo sirve en navegador
Sin requerimientos Docker - solo Python 3.9+
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

try:
    import markdown
    from markdown.extensions import tables, toc, codehilite, meta, fenced_code, attr_list, nl2br
except ImportError:
    print("❌ Error: markdown no instalado")
    print("   Instala: pip install markdown pymdown-extensions")
    sys.exit(1)


class MarkdownConverter:
    """Convierte Markdown a HTML."""
    
    def __init__(self, output_dir="html"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.md = markdown.Markdown(
            extensions=[
                'tables', 'toc', 'codehilite', 'meta', 
                'fenced_code', 'attr_list', 'nl2br'
            ]
        )
    
    def load_markdown(self, filepath):
        """Carga archivo Markdown."""
        if not Path(filepath).exists():
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
                        key, val = line.split(':', 1)
                        frontmatter[key.strip()] = val.strip().strip('"\'')
                body = '\n'.join(lines[end_idx+1:])
        
        # Convertir
        html_body = self.md.convert(body)
        toc_html = self.md.toc if hasattr(self.md, 'toc') else ""
        
        return html_body, toc_html, frontmatter
    
    def generate_html(self, title, html_body, toc_html, author=""):
        """Genera página HTML completa."""
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        
        .navbar {{
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 15px 20px;
        }}
        
        .navbar-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .navbar h2 {{ color: #2c3e50; font-size: 20px; }}
        
        .navbar-links {{
            display: flex;
            gap: 20px;
        }}
        
        .navbar-links a {{
            color: #3498db;
            text-decoration: none;
            font-size: 14px;
        }}
        
        .navbar-links a:hover {{ text-decoration: underline; }}
        
        .container {{
            max-width: 1400px;
            margin: 20px auto;
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
            padding: 0 20px;
        }}
        
        .sidebar {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-height: 85vh;
            overflow-y: auto;
            position: sticky;
            top: 80px;
        }}
        
        .sidebar h3 {{
            margin-bottom: 15px;
            font-size: 16px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .sidebar ul {{ list-style: none; }}
        .sidebar li {{ margin: 6px 0; }}
        
        .sidebar a {{
            text-decoration: none;
            color: #3498db;
            font-size: 13px;
            display: block;
            padding: 6px;
            border-radius: 4px;
        }}
        
        .sidebar a:hover {{
            background: #ecf0f1;
            padding-left: 10px;
        }}
        
        .sidebar ul ul {{
            margin-left: 12px;
            margin-top: 4px;
        }}
        
        .main {{
            background: white;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .header {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{ color: #2c3e50; margin-bottom: 10px; font-size: 32px; }}
        .header .meta {{ font-size: 13px; color: #7f8c8d; }}
        
        h2 {{
            margin-top: 40px;
            margin-bottom: 20px;
            color: #2c3e50;
            border-left: 4px solid #3498db;
            padding-left: 12px;
            font-size: 24px;
        }}
        
        h3 {{ margin-top: 25px; margin-bottom: 15px; color: #34495e; font-size: 20px; }}
        
        p {{ margin-bottom: 15px; text-align: justify; }}
        
        a {{ color: #3498db; text-decoration: none; border-bottom: 1px solid #bdc3c7; }}
        a:hover {{ background: #ecf0f1; }}
        
        code {{ background: #ecf0f1; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 13px; }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        
        pre code {{ background: none; color: #ecf0f1; padding: 0; }}
        
        ul, ol {{ margin: 15px 0; margin-left: 30px; }}
        li {{ margin-bottom: 8px; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 13px;
        }}
        
        table thead {{ background: #ecf0f1; }}
        table th {{
            padding: 12px;
            text-align: left;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 2px solid #bdc3c7;
        }}
        
        table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #bdc3c7;
        }}
        
        table tbody tr:hover {{ background: #f8f9fa; }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 15px 0;
            color: #7f8c8d;
            font-style: italic;
        }}
        
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #3498db;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            display: none;
            z-index: 1000;
        }}
        
        .back-to-top:hover {{ background: #2980b9; }}
        
        .search-box {{
            margin-bottom: 20px;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 8px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            font-size: 13px;
        }}
        
        @media (max-width: 768px) {{
            .container {{ grid-template-columns: 1fr; }}
            .sidebar {{ position: static; max-height: none; }}
            .main {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="navbar-content">
            <h2>📚 Tesis - Sistema Integrado de Auditoría</h2>
            <div class="navbar-links">
                <a href="index.html">Inicio</a>
                <a href="entregable-1.html">Entregable 1</a>
                <a href="mejora-continua.html">Mejora Continua</a>
                <a href="agent.html">Agente</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="sidebar">
            <div class="search-box">
                <input type="text" id="search" placeholder="🔍 Buscar...">
            </div>
            <h3>📑 Índice</h3>
            {toc_html}
        </div>
        
        <div class="main">
            <div class="header">
                <h1>{title}</h1>
                <div class="meta">
                    ✍️ Autor: {author} | 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
            {html_body}
        </div>
    </div>
    
    <div class="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        ↑ Top
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>
        hljs.highlightAll();
        window.addEventListener('scroll', function() {{
            const btn = document.querySelector('.back-to-top');
            if (window.scrollY > 300) btn.style.display = 'block';
            else btn.style.display = 'none';
        }});
        
        const search = document.getElementById('search');
        if (search) {{
            search.addEventListener('keyup', function(e) {{
                const query = e.target.value.toLowerCase();
                document.querySelectorAll('.sidebar a').forEach(link => {{
                    link.style.display = link.textContent.toLowerCase().includes(query) ? 'block' : 'none';
                }});
            }});
        }}
    </script>
</body>
</html>"""
    
    def convert_file(self, md_filepath, html_filename=None):
        """Convierte un archivo Markdown a HTML."""
        md_file = Path(md_filepath)
        if not md_file.exists():
            return None
        
        html_body, toc_html, frontmatter = self.load_markdown(md_filepath)
        if not html_body:
            return None
        
        title = frontmatter.get('title', md_file.stem.replace('_', ' ').title())
        author = frontmatter.get('author', 'Sistema de Tesis')
        
        html = self.generate_html(title, html_body, toc_html, author)
        
        if html_filename is None:
            html_filename = md_file.stem + '.html'
        
        output_path = self.output_dir / html_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path


def create_index_page(output_dir="html"):
    """Crea página índice."""
    index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visor de Tesis - Inicio</title>
    <style>
        body {{
            font-family: 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            max-width: 700px;
            padding: 50px;
            text-align: center;
        }}
        
        h1 {{ color: #2c3e50; margin-bottom: 10px; font-size: 32px; }}
        .subtitle {{ color: #7f8c8d; margin-bottom: 40px; font-size: 16px; }}
        
        .documents {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .doc-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 8px;
            text-decoration: none;
            transition: transform 0.3s;
            cursor: pointer;
        }}
        
        .doc-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .doc-card h3 {{ margin: 10px 0; font-size: 20px; }}
        .doc-card p {{ margin: 0; font-size: 13px; opacity: 0.9; }}
        
        .status {{
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        
        .footer {{ margin-top: 40px; color: #7f8c8d; font-size: 12px; }}
        
        @media (max-width: 600px) {{
            .documents {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Visor de Tesis</h1>
        <p class="subtitle">Sistema integrado de supervisión operativa agroexportadora con IA</p>
        
        <div class="status">
            ✅ Servidor en ejecución | Fecha: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """
        </div>
        
        <div class="documents">
            <a href="entregable-1.html" class="doc-card">
                <div style="font-size: 32px;">📄</div>
                <h3>Entregable 1</h3>
                <p>Capítulo I & II</p>
            </a>

            <a href="plan-detallado.html" class="doc-card">
                <div style="font-size: 32px;">🗂</div>
                <h3>Plan Detallado</h3>
                <p>Estructura completa y checklist</p>
            </a>
            
            <a href="mejora-continua.html" class="doc-card">
                <div style="font-size: 32px;">🔄</div>
                <h3>Mejora Continua</h3>
                <p>Ciclos PDCA</p>
            </a>
            
            <a href="agent.html" class="doc-card">
                <div style="font-size: 32px;">✓</div>
                <h3>Agente Revisión</h3>
                <p>Validación</p>
            </a>
        </div>
        
        <div class="footer">
            <p>📍 http://localhost:8000</p>
            <p>Markdown → HTML en tiempo real</p>
        </div>
    </div>
</body>
</html>"""
    
    Path(output_dir).mkdir(exist_ok=True)
    with open(Path(output_dir) / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)


def main():
    """Función principal."""
    print("\n🚀 Generador de Visor de Tesis")
    print("=" * 50)
    
    converter = MarkdownConverter()
    
    # Convertir archivos
    files = [
        ('entregable-1.md', 'entregable-1.html'),
        ('plan-detallado.md', 'plan-detallado.html'),
        ('mejora-continua-plan.md', 'mejora-continua.html'),
        ('.agent.md', 'agent.html'),
    ]
    
    print("\n📖 Convirtiendo archivos Markdown → HTML...\n")
    
    for md_file, html_file in files:
        if Path(md_file).exists():
            result = converter.convert_file(md_file, html_file)
            if result:
                print(f"   ✅ {md_file:30} → {html_file}")
            else:
                print(f"   ❌ Error convirtiendo {md_file}")
        else:
            print(f"   ⚠️  No encontrado: {md_file}")
    
    # Crear índice
    create_index_page()
    print(f"   ✅ {'index.html':30} → Página de inicio")
    
    print("\n" + "=" * 50)
    print("✅ Conversión completada")
    print(f"📁 Archivos generados en: ./html/")
    print("=" * 50)
    
    # Abrir en navegador
    try:
        import webbrowser
        print("\n🌐 Abriendo navegador...")
        webbrowser.open('file://' + str(Path('html/index.html').absolute()))
    except:
        print("   (No se pudo abrir navegador automáticamente)")
    
    print("\n📍 Acceso manual: Abre ./html/index.html en tu navegador")
    print("\nOpcional: Servir con servidor HTTP:")
    print("   python3 -m http.server 8000 --directory html")
    print("   Luego accede a: http://localhost:8000")


if __name__ == '__main__':
    main()
