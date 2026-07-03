import pypdf
from pathlib import Path

pdf_path = Path("Plantilla - Tesis de Investigación 2026 (1).docx.pdf")
out_path = Path("output/plantilla_pdf_content.txt")

print(f"Reading PDF: {pdf_path.absolute()}")
reader = pypdf.PdfReader(pdf_path)
lines = []

lines.append("=========================================")
lines.append(f"Documento: {pdf_path.name}")
lines.append(f"Total paginas: {len(reader.pages)}")
lines.append("=========================================\n")

for idx, page in enumerate(reader.pages):
    lines.append(f"--- PAGINA {idx + 1} ---")
    text = page.extract_text()
    if text:
        lines.append(text)
    lines.append("\n")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Contenido del PDF guardado en: {out_path.absolute()}")
