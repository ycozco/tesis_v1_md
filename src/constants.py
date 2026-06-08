# constants.py
# ============
# Constantes del orden de secciones de la tesis y metadatos de progreso.

from pathlib import Path

MARKDOWN_DIR = Path("/app/docs")
if not MARKDOWN_DIR.exists():
    MARKDOWN_DIR = Path("docs")
if not MARKDOWN_DIR.exists():
    MARKDOWN_DIR = Path("d:/tesis_yoset/docs")

ENTREGABLE_DIR = Path("/app/entregable")
if not ENTREGABLE_DIR.exists():
    ENTREGABLE_DIR = Path("entregable")

HTML_DIR = Path("/app/output")
if not HTML_DIR.exists():
    HTML_DIR = Path("output")

# Orden canonico de secciones de la tesis
SECTION_ORDER = [
    "02-00-portada",
    "02-01-resumen",
    "02-02-indices",
    "02-03-introduccion",
    "02-10-capitulo1",
    "02-20-capitulo2-antecedentes",
    "02-21-capitulo2-estadoarte",
    "02-22-capitulo2-marcoteorico",
    "02-30-capitulo3",
    "02-40-capitulo4",
    "02-41-capitulo4-resultados-cuantitativos",
    "02-42-capitulo4-explicabilidad-reportes",
    "02-43-capitulo4-usabilidad-trazabilidad",
    "02-44-capitulo4-discusion",
    "02-45-capitulo4-limitaciones-sintesis",
    "02-50-capitulo5",
    "02-60-conclusiones",
    "02-70-recomendaciones",
    "02-80-glosario",
    "02-90-referencias",
    "05-a1-anexo-usabilidad",
    "05-a2-anexo-modelcards",
    "05-a3-anexo-datasheet",
    "05-a4-anexo-ia",
    "05-a5-resumen-general",
]

SECTION_META = {
    "02-00-portada": {"label": "Portada", "cap": None, "status": "done"},
    "02-01-resumen": {"label": "Resumen / Abstract", "cap": None, "status": "done"},
    "02-02-indices": {"label": "Indices", "cap": None, "status": "done"},
    "02-03-introduccion": {"label": "Introduccion", "cap": None, "status": "done"},
    "02-10-capitulo1": {"label": "Capitulo I", "cap": "I", "status": "done"},
    "02-20-capitulo2-antecedentes": {"label": "Cap. II - 2.1", "cap": "II", "status": "done"},
    "02-21-capitulo2-estadoarte": {"label": "Cap. II - 2.2", "cap": "II", "status": "done"},
    "02-22-capitulo2-marcoteorico": {"label": "Cap. II - 2.3", "cap": "II", "status": "done"},
    "02-30-capitulo3": {"label": "Capitulo III", "cap": "III", "status": "done"},
    "02-40-capitulo4": {"label": "Capitulo IV", "cap": "IV", "status": "done"},
    "02-41-capitulo4-resultados-cuantitativos": {
        "label": "Cap. IV - Resultados Cuantitativos",
        "cap": "IV",
        "status": "pending",
    },
    "02-42-capitulo4-explicabilidad-reportes": {
        "label": "Cap. IV - Explicabilidad y Reportes",
        "cap": "IV",
        "status": "pending",
    },
    "02-43-capitulo4-usabilidad-trazabilidad": {
        "label": "Cap. IV - Usabilidad y Trazabilidad",
        "cap": "IV",
        "status": "pending",
    },
    "02-44-capitulo4-discusion": {
        "label": "Cap. IV - Discusion",
        "cap": "IV",
        "status": "pending",
    },
    "02-45-capitulo4-limitaciones-sintesis": {
        "label": "Cap. IV - Limitaciones y Sintesis",
        "cap": "IV",
        "status": "pending",
    },
    "02-50-capitulo5": {"label": "Capitulo V", "cap": "V", "status": "pending"},
    "02-60-conclusiones": {"label": "Conclusiones", "cap": None, "status": "pending"},
    "02-70-recomendaciones": {"label": "Recomendaciones", "cap": None, "status": "done"},
    "02-80-glosario": {"label": "Glosario", "cap": None, "status": "done"},
    "02-90-referencias": {"label": "Referencias", "cap": None, "status": "done"},
    "05-a1-anexo-usabilidad": {"label": "Anexo A", "cap": "A", "status": "pending"},
    "05-a2-anexo-modelcards": {"label": "Anexo B", "cap": "B", "status": "pending"},
    "05-a3-anexo-datasheet": {"label": "Anexo C", "cap": "C", "status": "pending"},
    "05-a4-anexo-ia": {"label": "Anexo D", "cap": "D", "status": "done"},
    "05-a5-resumen-general": {"label": "Anexo E", "cap": "E", "status": "done"},
}
