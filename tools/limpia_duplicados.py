"""
limpia_duplicados.py
=====================
Limpia duplicaciones de citas tras la purga.

Detecta y corrige patrones como:
- "Autor (Anio) (Autor, Anio)"  -> "Autor (Anio)"
- "(Autor, Anio) (Autor, Anio)" -> "(Autor, Anio)"
"""

from __future__ import annotations

import re
from pathlib import Path

DOCS_DIR = Path("docs")
ACTIVE_DOCS = sorted(
    p for p in DOCS_DIR.glob("*.md")
    if p.name not in {"tesis.md", "tesis-v2.md"}
)

# Patron 1: "Autor (YYYY) (Autor, YYYY)" -> "Autor (YYYY)"
# El "Autor" puede tener "et al.", "&", varios apellidos
# Capturamos: nombre/apellido + (YYYY) seguido de espacios + (mismo autor abreviado, YYYY)
PAT_NARRATIVE_DUP = re.compile(
    r"([A-ZÁ-Ú][\wÁ-Úá-úñÑ.&\s,]*?)\s+\((\d{4}[a-z]?)\)\s+\(([^)]+),\s*\2\)"
)

# Patron 2: doble parentetica "(Autor, YYYY) (Autor, YYYY)"
PAT_PARENS_DUP = re.compile(
    r"\(([^)]+),\s*(\d{4}[a-z]?)\)\s+\(\1,\s*\2\)"
)


def limpiar(text: str) -> tuple[str, int]:
    n = 0
    # Primero limpia duplicados parenteticos consecutivos
    nuevo, m = PAT_PARENS_DUP.subn(r"(\1, \2)", text)
    n += m
    # Luego limpia narrativo + parentetico redundante
    nuevo, m = PAT_NARRATIVE_DUP.subn(r"\1 (\2)", nuevo)
    n += m
    return nuevo, n


def main() -> None:
    total = 0
    for path in ACTIVE_DOCS:
        original = path.read_text(encoding="utf-8")
        nuevo, n = limpiar(original)
        if n > 0:
            path.write_text(nuevo, encoding="utf-8")
            print(f"  {path.name}: {n} duplicados corregidos")
            total += n
    print(f"\nTotal duplicados corregidos: {total}")


if __name__ == "__main__":
    main()
