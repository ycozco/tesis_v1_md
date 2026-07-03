#!/usr/bin/env python3
"""
scripts/build_tesis_reestructurada.py
=====================================
Compila la tesis reestructurada consolidada uniendo los preliminares,
los nuevos capítulos I, II y III (3.1-3.2) y conservando las secciones
de resultados (Capítulo IV), conclusiones (Capítulo V), glosario, 
referencias y anexos actualizados por el pipeline.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import os
from pathlib import Path
import re

def compile_thesis():
    base_dir = Path(__file__).resolve().parent.parent
    docs_dir = base_dir / "docs"
    tesis_dir = docs_dir / "tesis"
    tesis_dir.mkdir(parents=True, exist_ok=True)

    original_tesis_path = docs_dir / "02-95-tesis.md"
    chapter1_path = tesis_dir / "CAPITULO_I.md"
    chapter2_path = tesis_dir / "CAPITULO_II.md"
    chapter3_path = tesis_dir / "CAPITULO_III_3_1_3_2.md"
    output_path = tesis_dir / "tesis_reestructurada.md"

    print("Compilando tesis reestructurada...")

    # 1. Leer archivo original de tesis
    if not original_tesis_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo original {original_tesis_path}")
    
    with open(original_tesis_path, "r", encoding="utf-8", errors="replace") as f:
        original_content = f.read()

    # 2. Extraer preliminares (desde el inicio hasta justo antes del CAPITULO I)
    # Buscaremos la línea '# CAPITULO I' o '# CAPÍTULO I'
    cap1_match = re.search(r"\n#\s+CAPITULO\s+I:?", original_content, re.IGNORECASE)
    if not cap1_match:
        cap1_match = re.search(r"\n#\s+CAPÍTULO\s+I:?", original_content, re.IGNORECASE)
        
    if not cap1_match:
        raise ValueError("No se encontró la cabecera del Capítulo I en el archivo original.")

    preliminares = original_content[:cap1_match.start()]

    # 3. Leer los nuevos capítulos I, II y III
    with open(chapter1_path, "r", encoding="utf-8") as f:
        chapter1_content = f.read()

    with open(chapter2_path, "r", encoding="utf-8") as f:
        chapter2_content = f.read()

    with open(chapter3_path, "r", encoding="utf-8") as f:
        chapter3_content = f.read()

    # 4. Extraer el Capítulo IV, V, glosario, referencias y anexos del archivo original
    # Buscaremos la línea del CAPITULO IV
    cap4_match = re.search(r"\n#\s+CAPITULO\s+IV:?", original_content, re.IGNORECASE)
    if not cap4_match:
        cap4_match = re.search(r"\n#\s+CAPÍTULO\s+IV:?", original_content, re.IGNORECASE)

    if not cap4_match:
        raise ValueError("No se encontró la cabecera del Capítulo IV en el archivo original.")

    rest_of_thesis = original_content[cap4_match.start():]

    # 5. Consolidar el contenido
    consolidated = []
    consolidated.append(preliminares.strip())
    consolidated.append("\n\n<div style=\"page-break-before: always;\"></div>\n\n")
    consolidated.append(chapter1_content.strip())
    consolidated.append("\n\n<div style=\"page-break-before: always;\"></div>\n\n")
    consolidated.append(chapter2_content.strip())
    consolidated.append("\n\n<div style=\"page-break-before: always;\"></div>\n\n")
    consolidated.append(chapter3_content.strip())
    consolidated.append("\n\n<div style=\"page-break-before: always;\"></div>\n\n")
    consolidated.append(rest_of_thesis.strip())

    consolidated_content = "\n".join(consolidated)

    # 6. Escribir el resultado
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(consolidated_content)

    print(f"Tesis consolidada reestructurada escrita con éxito en: {output_path}")

if __name__ == "__main__":
    compile_thesis()
