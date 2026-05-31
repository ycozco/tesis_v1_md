# constants.py
# ============
# Constantes del orden de secciones de la tesis y metadatos de progreso.

from pathlib import Path

MARKDOWN_DIR = Path('/app/docs')
if not MARKDOWN_DIR.exists():
    MARKDOWN_DIR = Path('docs')
if not MARKDOWN_DIR.exists():
    MARKDOWN_DIR = Path('d:/tesis_yoset/docs')

ENTREGABLE_DIR = Path('/app/entregable')
if not ENTREGABLE_DIR.exists():
    ENTREGABLE_DIR = Path('entregable')

HTML_DIR = Path('/app/output')
if not HTML_DIR.exists():
    HTML_DIR = Path('output')

# Orden canónico de secciones de la tesis
SECTION_ORDER = [
    "00-portada",
    "01-resumen",
    "02-indices",
    "03-introduccion",
    "10-capitulo1",
    "20-capitulo2-antecedentes",
    "21-capitulo2-estadoarte",
    "22-capitulo2-marcoteorico",
    "30-capitulo3",
    "40-capitulo4",
    "50-capitulo5",
    "60-conclusiones",
    "70-recomendaciones",
    "80-glosario",
    "90-referencias",
    "a1-anexo-usabilidad",
    "a2-anexo-modelcards",
    "a3-anexo-datasheet",
    "a4-anexo-ia",
]

SECTION_META = {
    "00-portada":                {"label": "Portada",             "cap": None,  "status": "done"},
    "01-resumen":                {"label": "Resumen / Abstract",  "cap": None,  "status": "done"},
    "02-indices":                {"label": "Índices",             "cap": None,  "status": "done"},
    "03-introduccion":           {"label": "Introducción",        "cap": None,  "status": "done"},
    "10-capitulo1":              {"label": "Capítulo I",          "cap": "I",   "status": "done"},
    "20-capitulo2-antecedentes": {"label": "Cap. II — §2.1",     "cap": "II",  "status": "done"},
    "21-capitulo2-estadoarte":   {"label": "Cap. II — §2.2",     "cap": "II",  "status": "done"},
    "22-capitulo2-marcoteorico": {"label": "Cap. II — §2.3",     "cap": "II",  "status": "done"},
    "30-capitulo3":              {"label": "Capítulo III",        "cap": "III", "status": "done"},
    "40-capitulo4":              {"label": "Capítulo IV",         "cap": "IV",  "status": "pending"},
    "50-capitulo5":              {"label": "Capítulo V",          "cap": "V",   "status": "pending"},
    "60-conclusiones":           {"label": "Conclusiones",        "cap": None,  "status": "pending"},
    "70-recomendaciones":        {"label": "Recomendaciones",     "cap": None,  "status": "done"},
    "80-glosario":               {"label": "Glosario",           "cap": None,  "status": "done"},
    "90-referencias":            {"label": "Referencias",         "cap": None,  "status": "done"},
    "a1-anexo-usabilidad":       {"label": "Anexo A",            "cap": "A",   "status": "pending"},
    "a2-anexo-modelcards":       {"label": "Anexo B",            "cap": "B",   "status": "pending"},
    "a3-anexo-datasheet":        {"label": "Anexo C",            "cap": "C",   "status": "pending"},
    "a4-anexo-ia":               {"label": "Anexo D",            "cap": "D",   "status": "done"},
}
