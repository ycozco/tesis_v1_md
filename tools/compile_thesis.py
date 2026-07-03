#!/usr/bin/env python3
"""
Compilador de Tesis Integrado (PDF y DOCX)
------------------------------------------
Este script compila la tesis del proyecto en dos formatos estándar:
1. DOCX: Usando Pandoc dentro del contenedor Docker para asegurar formato APA 7
   con la plantilla oficial de la tesis.
2. PDF: Usando Google Chrome / Microsoft Edge headless en el host para imprimir
   la vista interactiva del servidor local (http://localhost:8000/docs/02-95-tesis)
   con tipografía moderna, tablas estilizadas y diseño prémium.

Uso:
  python scripts/compile_thesis.py [--date]
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def run_command(cmd, shell=False):
    """Ejecuta un comando del sistema y captura la salida."""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr or e.stdout or str(e)}"

def compile_docx(project_dir, output_path):
    """Compila la tesis a DOCX usando Pandoc en el contenedor Docker."""
    print("✨ Iniciando compilación de formato DOCX en Docker...")
    
    cmd = [
        "docker", "exec", "tesis-web-viewer",
        "pandoc", "/app/docs/02-95-tesis.md",
        "-o", "/app/output/tesis.docx",
        "--reference-doc=/app/formato/Plantilla - Tesis de Investigación 2026.docx",
        "--citeproc",
        "--bibliography=/app/config/refs.bib",
        "--csl=/app/config/apa.csl",
        "--toc",
        "--toc-depth=3"
    ]
    
    success, output = run_command(cmd)
    if success:
        print("✅ Formato DOCX compilado exitosamente.")
        # Copiar de output/tesis.docx al output_path si difieren
        src_path = project_dir / "output" / "tesis.docx"
        if src_path.exists() and src_path != output_path:
            import shutil
            shutil.copy2(src_path, output_path)
            print(f"📁 Copia DOCX guardada en: {output_path}")
        return True
    else:
        print(f"❌ Error al compilar DOCX: {output}")
        return False

def compile_pdf(project_dir, output_path):
    """Compila la tesis a PDF usando Chrome/Edge headless desde el host."""
    print("✨ Iniciando compilación de formato PDF desde el navegador del host...")
    
    # Rutas comunes del navegador
    chrome_paths = [
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
        Path(os.environ.get("USERPROFILE", "")) / "AppData/Local/Google/Chrome/Application/chrome.exe"
    ]
    
    edge_paths = [
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe")
    ]
    
    browser_exe = None
    # Priorizar Chrome
    for path in chrome_paths:
        if path.exists():
            browser_exe = path
            break
            
    # Caída a Edge si Chrome no se encuentra
    if not browser_exe:
        for path in edge_paths:
            if path.exists():
                browser_exe = path
                break
                
    if not browser_exe:
        print("❌ Error: No se encontró Google Chrome o Microsoft Edge en las rutas por defecto del host.")
        return False
        
    print(f"🌐 Usando navegador: {browser_exe}")
    
    # Creamos un PDF temporal local en output
    temp_pdf = project_dir / "output" / "tesis.pdf"
    
    cmd = [
        str(browser_exe),
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={temp_pdf}",
        "http://localhost:8000/docs/02-95-tesis"
    ]
    
    success, output = run_command(cmd)
    if success and temp_pdf.exists():
        print("✅ Formato PDF compilado exitosamente.")
        if temp_pdf != output_path:
            import shutil
            try:
                shutil.copy2(temp_pdf, output_path)
                print(f"📁 Copia PDF guardada en: {output_path}")
            except PermissionError:
                print(f"⚠️ El archivo de salida '{output_path.name}' está bloqueado por otro proceso (e.g. Acrobat/Chrome).")
                print(f"   Se conserva el archivo PDF recién compilado en: {temp_pdf}")
        return True
    else:
        print(f"❌ Error al compilar PDF: {output}")
        return False

def main():
    project_dir = Path("D:/tesis_yoset")
    output_dir = project_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Obtener fecha para el nombrado opcional
    today_str = datetime.now().strftime("%Y_%m_%d")
    
    # Nombres de salida por defecto
    default_docx = output_dir / "tesis-v2.docx"
    default_pdf = output_dir / "tesis-v2.pdf"
    
    # Nombres de salida con fecha
    dated_docx = output_dir / f"tesis-v2_{today_str}.docx"
    dated_pdf = output_dir / f"tesis-v2_{today_str}.pdf"
    
    print("==================================================")
    print("🚀 COMPILADOR INTEGRADO DE TESIS (PDF y DOCX)")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==================================================")
    
    # 1. Compilar DOCX
    docx_success = compile_docx(project_dir, default_docx)
    if docx_success:
        import shutil
        shutil.copy2(default_docx, dated_docx)
        print(f"✨ Archivo fechado creado: {dated_docx.name}")
        
    print("-" * 50)
    
    # 2. Compilar PDF (requiere que el servidor local Docker esté levantado en el puerto 8000)
    pdf_success = compile_pdf(project_dir, default_pdf)
    if pdf_success:
        import shutil
        temp_pdf = project_dir / "output" / "tesis.pdf"
        try:
            shutil.copy2(temp_pdf, dated_pdf)
            print(f"✨ Archivo fechado creado: {dated_pdf.name}")
        except PermissionError:
            print(f"⚠️ El archivo fechado '{dated_pdf.name}' está bloqueado y no se pudo sobreescribir.")
        
    print("==================================================")
    if docx_success and pdf_success:
        print("🎉 ¡PROCESO DE COMPILACIÓN COMPLETADO EXITOSAMENTE!")
        print(f"📄 DOCX: {default_docx.name} y {dated_docx.name}")
        print(f"📄 PDF: tesis.pdf (compilado fresco) y {dated_pdf.name}")
    else:
        print("⚠️ Compilación finalizada con advertencias.")
    print("==================================================")

if __name__ == "__main__":
    main()
