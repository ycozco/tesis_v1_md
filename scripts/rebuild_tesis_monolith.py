#!/usr/bin/env python3
"""
Rebuild the active monolithic thesis file from the source Markdown modules.

Output:
  docs/02-95-tesis.md

The source modules are the canonical thesis files. Historical drafts should live
under docs/archive/ and must not be added to SECTION_ORDER.
"""

import os
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


SECTION_ORDER = [
    "02-00-portada", "02-01-resumen", "02-02-indices", "02-03-introduccion",
    "02-10-capitulo1",
    "02-20-capitulo2-antecedentes", "02-21-capitulo2-estadoarte", "02-22-capitulo2-marcoteorico",
    "02-30-capitulo3",
    "02-40-capitulo4",
    "02-41-capitulo4-resultados-cuantitativos",
    "02-42-capitulo4-explicabilidad-reportes",
    "02-43-capitulo4-usabilidad-trazabilidad",
    "02-44-capitulo4-discusion",
    "02-45-capitulo4-limitaciones-sintesis",
    "02-50-capitulo5", "02-60-conclusiones",
    "02-70-recomendaciones", "02-80-glosario", "02-90-referencias",
    "05-a1-anexo-usabilidad", "05-a2-anexo-modelcards", "05-a3-anexo-datasheet", "05-a4-anexo-ia",
    "05-a5-resumen-general",
]

def main():
    docs_dir = Path("docs")
    output_file = docs_dir / "02-95-tesis.md"
    
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
