#!/usr/bin/env python3
"""
Script para convertir Markdown a HTML con soporte para tablas y referencias.
Genera versiones interactivas y estáticas de documentos Markdown.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

try:
    import markdown
    from markdown.extensions import tables, toc, codehilite, meta
except ImportError:
    print("Error: markdown no instalado. Instalar: pip install markdown")
    sys.exit(1)


class MarkdownToHTML:
    """Conversor Markdown → HTML con templates modernos."""
    
    def __init__(self, output_dir="/app/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.md = markdown.Markdown(
            extensions=[
                'tables',
                'toc',
                'codehilite',
                'meta',
                'fenced_code',
                'attr_list',
                'nl2br'
            ]
        )
    
    def load_file(self, filepath):
        """Carga archivo Markdown."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse_frontmatter(self, content):
        """Extrae YAML frontmatter del Markdown."""
        if not content.startswith('---'):
            return {}, content
        
        lines = content.split('\n')
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].startswith('---'):
                end_idx = i
                break
        
        if end_idx == -1:
            return {}, content
        
        frontmatter = {}
        for line in lines[1:end_idx]:
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')
        
        body = '\n'.join(lines[end_idx+1:])
        return frontmatter, body
    
    def generate_html(self, md_content, title="Tesis", author=""):
        """Convierte Markdown a HTML."""
        html_body = self.md.convert(md_content)
        toc_html = self.md.toc if hasattr(self.md, 'toc') else ""
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
            padding: 20px;
        }}
        
        .sidebar {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-height: 90vh;
            overflow-y: auto;
            position: sticky;
            top: 20px;
        }}
        
        .sidebar h3 {{
            margin-bottom: 15px;
            font-size: 16px;
            color: #2c3e50;
        }}
        
        .sidebar ul {{
            list-style: none;
        }}
        
        .sidebar li {{
            margin: 8px 0;
        }}
        
        .sidebar a {{
            text-decoration: none;
            color: #3498db;
            transition: color 0.3s;
            font-size: 14px;
            display: block;
            padding: 6px;
            border-radius: 4px;
        }}
        
        .sidebar a:hover {{
            background: #ecf0f1;
            color: #2980b9;
        }}
        
        .sidebar ul ul {{
            margin-left: 16px;
            margin-top: 8px;
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
        
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            font-size: 14px;
            color: #7f8c8d;
        }}
        
        h2 {{
            margin-top: 40px;
            margin-bottom: 20px;
            color: #2c3e50;
            border-left: 4px solid #3498db;
            padding-left: 12px;
        }}
        
        h3 {{
            margin-top: 25px;
            margin-bottom: 15px;
            color: #34495e;
        }}
        
        h4, h5, h6 {{
            margin-top: 15px;
            margin-bottom: 10px;
            color: #7f8c8d;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px solid #bdc3c7;
        }}
        
        a:hover {{
            background: #ecf0f1;
        }}
        
        code {{
            background: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
        }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        
        pre code {{
            background: none;
            color: #ecf0f1;
            padding: 0;
        }}
        
        ul, ol {{
            margin: 15px 0;
            margin-left: 30px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        
        table thead {{
            background: #ecf0f1;
        }}
        
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
        
        table tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 15px 0;
            color: #7f8c8d;
            font-style: italic;
        }}
        
        .checklist {{
            list-style: none;
            margin: 15px 0;
        }}
        
        .checklist li {{
            margin: 10px 0;
        }}
        
        .checklist input[type="checkbox"] {{
            margin-right: 10px;
            cursor: pointer;
        }}
        
        .metadata {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 13px;
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
        
        .back-to-top:hover {{
            background: #2980b9;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
            
            .sidebar {{
                position: static;
                max-height: none;
            }}
            
            .main {{
                padding: 20px;
            }}
        }}
        
        @print {{
            body {{
                background: white;
            }}
            
            .sidebar {{
                display: none;
            }}
            
            .container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h3>📑 Índice</h3>
            {toc_html}
        </div>
        
        <div class="main">
            <div class="header">
                <h1>{title}</h1>
                <div class="meta">
                    Autor: {author} | Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
            
            {html_body}
        </div>
    </div>
    
    <div class="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        ↑ Arriba
    </div>
    
    <script>
        // Mostrar botón "Back to Top" al scrollear
        window.addEventListener('scroll', function() {{
            const btn = document.querySelector('.back-to-top');
            if (window.scrollY > 300) {{
                btn.style.display = 'block';
            }} else {{
                btn.style.display = 'none';
            }}
        }});
        
        // Hacer checkboxes interactivos
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => {{
            cb.addEventListener('change', function() {{
                // Guardar estado en localStorage
                const id = Math.random();
                localStorage.setItem('checkbox-' + id, this.checked);
            }});
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def save_html(self, html, filename):
        """Guarda HTML en archivo."""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path
    
    def convert_file(self, md_filepath, html_filename=None):
        """Convierte archivo Markdown a HTML."""
        md_file = Path(md_filepath)
        if not md_file.exists():
            print(f"Error: Archivo no encontrado: {md_filepath}")
            return None
        
        content = self.load_file(md_filepath)
        frontmatter, body = self.parse_frontmatter(content)
        
        title = frontmatter.get('title', md_file.stem.replace('-', ' ').title())
        author = frontmatter.get('author', 'Sistema de Tesis')
        
        html = self.generate_html(body, title, author)
        
        if html_filename is None:
            html_filename = md_file.stem + '.html'
        
        output_path = self.save_html(html, html_filename)
        print(f"✓ Convertido: {md_filepath} → {output_path}")
        
        return output_path


SECTION_ORDER = [
    "00-portada", "01-resumen", "02-indices", "03-introduccion",
    "10-capitulo1",
    "20-capitulo2-antecedentes", "21-capitulo2-estadoarte", "22-capitulo2-marcoteorico",
    "30-capitulo3", "40-capitulo4", "50-capitulo5", "60-conclusiones",
    "70-recomendaciones", "80-glosario", "90-referencias",
    "A1-anexo-usabilidad", "A2-anexo-modelcards", "A3-anexo-datasheet", "A4-anexo-ia",
]


def combine_sections(docs_dir='/app/docs', output_path='/app/output/tesis-completa.html'):
    """Combina todas las secciones numeradas en un único HTML para revisión."""
    converter = MarkdownToHTML()
    combined_md = ""
    for slug in SECTION_ORDER:
        md_path = Path(docs_dir) / f"{slug}.md"
        if md_path.exists():
            content = md_path.read_text(encoding='utf-8')
            if content.startswith('---'):
                lines = content.split('\n')
                end = next((i for i in range(1, len(lines)) if lines[i].startswith('---')), -1)
                content = '\n'.join(lines[end + 1:]) if end != -1 else content
            combined_md += content + "\n\n---\n\n"
    html = converter.generate_html(combined_md, "Tesis Completa — Sistema Integrado Agroexportador", "Yoset Cozco Mauri")
    converter.save_html(html, 'tesis-completa.html')
    print(f"✓ Tesis combinada generada: {output_path}")


def main():
    """Función principal."""
    converter = MarkdownToHTML()

    # Convertir secciones numeradas (nuevo esquema segmentado)
    section_files = [
        (f'/app/docs/{slug}.md', f'{slug}.html')
        for slug in SECTION_ORDER
        if Path(f'/app/docs/{slug}.md').exists()
    ]

    # Compatibilidad: agregar archivos legacy si existen
    legacy_files = [
        ('/app/docs/entregable1.md', 'entregable1.html'),
        ('/app/docs/plan_detallado.md', 'plan_detallado.html'),
        ('/app/docs/mejora-continua-plan.md', 'mejora-continua.html'),
        ('/app/docs/tesis.md', 'tesis.html'),
    ]

    files_to_convert = section_files + [f for f in legacy_files if Path(f[0]).exists()]
    
    print("🚀 Iniciando conversión Markdown → HTML\n")
    
    results = {}
    for md_file, html_file in files_to_convert:
        if Path(md_file).exists():
            result = converter.convert_file(md_file, html_file)
            results[md_file] = result
        else:
            print(f"⚠️  Archivo no encontrado: {md_file}")
    
    # Generar índice HTML
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    index_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visor de Tesis - Índice</title>
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
            max-width: 600px;
            padding: 40px;
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        
        .documents {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        
        .doc-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-decoration: none;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }}
        
        .doc-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .doc-card h3 {{
            margin: 0 0 8px 0;
            font-size: 18px;
        }}
        
        .doc-card p {{
            margin: 0;
            font-size: 13px;
            opacity: 0.9;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-size: 12px;
        }}
        
        .status {{
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Visor de Tesis Interactivo</h1>
        <p class="subtitle">Sistema integrado de supervisión operativa agroexportadora con IA</p>
        
        <div class="status">
            ✓ Conversión completada: {timestamp}
        </div>
        
        <div class="documents">
            <a href="entregable1.html" class="doc-card">
                <h3>📄 Entregable 1</h3>
                <p>Capítulo I (Planteamiento) y Capítulo II (Marco Teórico)</p>
            </a>

            <a href="plan_detallado.html" class="doc-card">
                <h3>🗂 Plan Detallado</h3>
                <p>Estructura completa, avance y checklist actualizado</p>
            </a>
            
            <a href="mejora-continua.html" class="doc-card">
                <h3>🔄 Plan de Mejora Continua</h3>
                <p>Ciclos PDCA, validación iterativa, métricas calidad</p>
            </a>
            
            <a href="agent-review.html" class="doc-card">
                <h3>✓ Agente de Revisión</h3>
                <p>Checklist completo para validación del plan</p>
            </a>
            
            <a href="tesis.html" class="doc-card">
                <h3>📜 Tesis Completa</h3>
                <p>Estructura de 5 capítulos con discusión avanzada</p>
            </a>
        </div>
        
        <div class="footer">
            <p>Generado automáticamente por script de conversión Markdown → HTML</p>
            <p>Compatible con todos los navegadores modernos | Optimizado para lectura</p>
        </div>
    </div>
</body>
</html>"""
    
    index_path = converter.save_html(index_html, 'index.html')
    
    combine_sections()

    print(f"\n✅ Conversión completada:")
    print(f"   - {len(results)} archivos convertidos")
    print(f"   - Tesis combinada: /app/output/tesis-completa.html")
    print(f"   - Acceso web: http://localhost:8000/secciones")

    return results


if __name__ == '__main__':
    main()
