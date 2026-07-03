#!/usr/bin/env python3
"""
scripts/sync_individual_chapters.py
===================================
Sincroniza los archivos de capítulos individuales en docs/ a partir
de los nuevos archivos reestructurados en docs/tesis/, para que al compilar
el sitio de GitHub Pages de forma individual, las páginas HTML correspondientes
reflejen los cambios académicos.

Tesis UNSA - Yoset Cozco Mauri (2026).
"""

import os
import re
from pathlib import Path

def sync_chapters():
    base_dir = Path(__file__).resolve().parent.parent
    docs_dir = base_dir / "docs"
    tesis_dir = docs_dir / "tesis"

    print("Sincronizando archivos individuales de capítulos en docs/...")

    # 1. Capítulo I
    cap1_src = tesis_dir / "CAPITULO_I.md"
    cap1_dest = docs_dir / "02-10-capitulo1.md"
    if cap1_src.exists():
        with open(cap1_src, "r", encoding="utf-8") as f:
            content = f.read()
        with open(cap1_dest, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Sincronizado: {cap1_dest.name}")

    # 2. Capítulo II (Dividir en Antecedentes, Estado del arte y Marco teórico)
    cap2_src = tesis_dir / "CAPITULO_II.md"
    if cap2_src.exists():
        with open(cap2_src, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Encontrar las secciones mediante expresiones regulares
        antecedentes_match = re.search(r"## 2\.1 Antecedentes de la Investigación", content)
        estado_arte_match = re.search(r"## 2\.2 Estado del Arte", content)
        marco_conceptual_match = re.search(r"## 2\.3 Marco Conceptual", content)
        
        if antecedentes_match and estado_arte_match and marco_conceptual_match:
            # Extraer secciones
            antecedentes_text = "# CAPÍTULO II: MARCO TEÓRICO\n\n" + content[antecedentes_match.start():estado_arte_match.start()].strip()
            estado_arte_text = "# ESTADO DEL ARTE\n\n" + content[estado_arte_match.start():marco_conceptual_match.start()].strip()
            marco_conceptual_text = "# MARCO CONCEPTUAL\n\n" + content[marco_conceptual_match.start()].strip()
            # Wait, let's get the text for marco conceptual up to the end of the file
            marco_conceptual_text = "# MARCO CONCEPTUAL\n\n" + content[marco_conceptual_match.start():].strip()
            
            # Escribir archivos correspondientes
            with open(docs_dir / "02-20-capitulo2-antecedentes.md", "w", encoding="utf-8") as f:
                f.write(antecedentes_text)
            with open(docs_dir / "02-21-capitulo2-estadoarte.md", "w", encoding="utf-8") as f:
                f.write(estado_arte_text)
            with open(docs_dir / "02-22-capitulo2-marcoteorico.md", "w", encoding="utf-8") as f:
                f.write(marco_conceptual_text)
                
            print("Sincronizado y dividido: 02-20-capitulo2-antecedentes.md, 02-21-capitulo2-estadoarte.md, 02-22-capitulo2-marcoteorico.md")
        else:
            print("No se pudieron identificar las secciones 2.1, 2.2 y 2.3 en CAPITULO_II.md para la división.")

    # 3. Capítulo III
    cap3_src = tesis_dir / "CAPITULO_III_3_1_3_2.md"
    cap3_dest = docs_dir / "02-30-capitulo3.md"
    if cap3_src.exists():
        with open(cap3_src, "r", encoding="utf-8") as f:
            content = f.read()
        with open(cap3_dest, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Sincronizado: {cap3_dest.name}")

if __name__ == "__main__":
    sync_chapters()
