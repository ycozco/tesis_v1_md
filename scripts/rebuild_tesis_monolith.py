#!/usr/bin/env python3
"""
Script to rebuild the monolithic docs/tesis.md from the active individual chapter files.
This ensures that the unified document served at http://localhost:8000/docs/tesis
is fully synchronized with the academic edits (Hitos 1 to 4).
"""

import os
from pathlib import Path

SECTION_ORDER = [
    "00-portada", "01-resumen", "02-indices", "03-introduccion",
    "10-capitulo1",
    "20-capitulo2-antecedentes", "21-capitulo2-estadoarte", "22-capitulo2-marcoteorico",
    "30-capitulo3", "40-capitulo4", "50-capitulo5", "60-conclusiones",
    "70-recomendaciones", "80-glosario", "90-referencias",
    "A1-anexo-usabilidad", "A2-anexo-modelcards", "A3-anexo-datasheet", "A4-anexo-ia",
]

def main():
    docs_dir = Path("docs")
    output_file = docs_dir / "tesis.md"
    
    print(f"🔄 Rebuilding monolithic {output_file} from active chapters...")
    
    combined_content = []
    
    for idx, slug in enumerate(SECTION_ORDER):
        file_path = docs_dir / f"{slug}.md"
        if not file_path.exists():
            print(f"⚠️ Warning: {file_path} not found!")
            continue
            
        print(f"  + Adding {file_path}")
        content = file_path.read_text(encoding="utf-8")
        
        # If it's not the first file, strip any YAML frontmatter if present
        if idx > 0 and content.startswith("---"):
            lines = content.split("\n")
            end_idx = -1
            for i in range(1, len(lines)):
                if lines[i].startswith("---"):
                    end_idx = i
                    break
            if end_idx != -1:
                content = "\n".join(lines[end_idx+1:])
                
        combined_content.append(content.strip())
        
    # Join sections with standard academic page breaks (OpenXML for Word and HTML for PDF)
    page_break = (
        "\n\n"
        "<div style=\"page-break-before: always;\"></div>\n\n"
        "```{=openxml}\n"
        "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n"
        "```\n\n"
    )
    final_md = page_break.join(combined_content) + "\n"
    
    # Save output file
    output_file.write_text(final_md, encoding="utf-8")
    print(f"✅ Rebuild complete! Saved as {output_file} ({len(final_md)} bytes).")

if __name__ == "__main__":
    main()
