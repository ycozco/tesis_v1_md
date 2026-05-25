"""
auditar_referencias.py
=======================
Verifica que cada cita APA en los docs activos tenga su entrada en refs.bib,
y reporta entradas de refs.bib que no esten citadas (huerfanas).
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

DOCS_DIR = Path("docs")
BIB_FILE = Path("config/refs.bib")
ACTIVE_DOCS = sorted(
    p for p in DOCS_DIR.glob("*.md")
    if p.name not in {"tesis.md", "tesis-v2.md"}
)

# Mapeo inverso: cita APA principal -> clave_bib
# (Se sincroniza con el MAPEO_APA del script purga_referencias.py)
MAPEO_INVERSO = {
    "(Chen & Guestrin, 2016)": "chen2016xgboost",
    "(Ke et al., 2017)": "ke2017lightgbm",
    "(Prokhorenkova et al., 2018)": "prokhorenkova2018catboost",
    "(Gorishniy et al., 2021)": "gorishniy2021ft",
    "(Grinsztajn et al., 2022)": "grinsztajn2022trees",
    "(Arik & Pfister, 2021)": "arik2021tabnet",
    "(Friedman, 2001)": "friedman2001greedy",
    "(Lim et al., 2021)": "lim2020tft",
    "(Zeng et al., 2023)": "zeng2023dlinear",
    "(Liu et al., 2024)": "liu2024itransformer",
    "(Nie et al., 2023)": "nie2023patchtst",
    "(Challu et al., 2022)": "nhts2022",
    "(Ansari et al., 2024)": "chronos2024",
    "(Liu et al., 2008)": "liu2008isolationforest",
    "(Breunig et al., 2000)": "breunig2000lof",
    "(Ruff et al., 2018)": "ruff2018deepsvdd",
    "(Li et al., 2022)": "li2022ecod",
    "(Han et al., 2022)": "han2022adbench",
    "(Zhao et al., 2019)": "zhao2019pyod",
    "(Lundberg & Lee, 2017)": "lundberg2017shap",
    "(Lundberg et al., 2020)": "lundberg2020treeshap",
    "(Ribeiro et al., 2016)": "ribeiro2016lime",
    "(Hegselmann et al., 2023)": "tabllm2023",
    "(Lewis et al., 2020)": "lewis2020rag",
    "(Schneider et al., 2025)": "schneider2025rag",
    "(Park, 2024)": "park2024llm",
    "(Kadir et al., 2025)": "auditcopilot2025",
    "(Waltersdorfer et al., 2024)": "auditmai2024",
    "(Tsai et al., 2025)": "tsai2025llmanomaly",
    "(Ji et al., 2023)": "ji2023survey",
    "(Maynez et al., 2026)": "survey2026hallucination",
    "(Barclays Research, 2025)": "barclays2025beyond",
    "(JRFM, 2025)": "mongolia2025fraud",
    "(Thanathamathee et al., 2024)": "thanathamathee2024shap",
    "(Almalki & Masud, 2025)": "almalki2025fraud",
    "(Patel et al., 2024)": "patel2024auditing",
    "(Sculley et al., 2015)": "sculley2015hidden",
    "(Kreuzberger et al., 2022)": "kreuzberger2022mlops",
    "(Gebru et al., 2021)": "gebru2021datasheets",
    "(Mitchell et al., 2019)": "mitchell2019modelcards",
    "(NIST, 2023)": "nist2023aia",
    "(SBS, 2023)": "sbs2023riesgos",
    "(PCM, 2025)": "pcm2025leyia",
    "(Parlamento Europeo y Consejo, 2024)": "eu2024aiact",
    "(Prenio & Yong, 2024)": "prenio2024managing",
    "(Creswell & Creswell, 2018)": "creswell2018research",
    "(Page et al., 2021)": "page2021prisma",
    "(Cohen, 1960)": "cohen1960kappa",
    "(Akiba et al., 2019)": "akiba2019optuna",
    "(Papineni et al., 2002)": "papineni2002bleu",
    "(Lin, 2004)": "lin2004rouge",
    "(MIDAGRI, 2026)": "midagri2026boletin",
    "(Jesus et al., 2022)": "jesus2022baf",
}


def claves_en_bib() -> set[str]:
    text = BIB_FILE.read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{([a-zA-Z0-9_-]+),", text))


def citas_en_docs() -> Counter:
    counter: Counter[str] = Counter()
    # Captura patrones (Apellido, AAAA) y (Apellido & Apellido, AAAA) y multi
    pat = re.compile(r"\(([^()]+?,\s*\d{4}[a-z]?)\)")
    for path in ACTIVE_DOCS:
        text = path.read_text(encoding="utf-8")
        for m in pat.finditer(text):
            cita = m.group(0)
            # Si es bloque multi separado por ; lo dividimos
            inner = m.group(1)
            if ";" in inner:
                for sub in inner.split(";"):
                    sub = sub.strip()
                    if sub:
                        counter[f"({sub})"] += 1
            else:
                counter[cita] += 1
    return counter


def main() -> None:
    bib_keys = claves_en_bib()
    print(f"refs.bib contiene {len(bib_keys)} entradas\n")

    docs_citations = citas_en_docs()
    print(f"Citas detectadas en docs activos: {sum(docs_citations.values())} ocurrencias, {len(docs_citations)} unicas\n")

    # Mapear citas a claves bib
    citas_huerfanas: list[str] = []
    claves_usadas: set[str] = set()
    for cita, count in docs_citations.most_common():
        key = MAPEO_INVERSO.get(cita)
        if key is None:
            citas_huerfanas.append(f"{cita} ({count} usos)")
        else:
            claves_usadas.add(key)

    bib_huerfanas = bib_keys - claves_usadas

    print("=== Citas APA SIN entrada en refs.bib (revisar manualmente) ===")
    if citas_huerfanas:
        for c in citas_huerfanas[:50]:
            print(f"  - {c}")
        if len(citas_huerfanas) > 50:
            print(f"  ... y {len(citas_huerfanas) - 50} mas")
    else:
        print("  Ninguna.")

    print("\n=== Entradas en refs.bib NO citadas en docs activos ===")
    if bib_huerfanas:
        for k in sorted(bib_huerfanas):
            print(f"  - {k}")
    else:
        print("  Ninguna.")

    print(f"\nResumen: {len(claves_usadas)}/{len(bib_keys)} entradas usadas. "
          f"{len(citas_huerfanas)} citas sin mapeo. "
          f"{len(bib_huerfanas)} entradas huerfanas.")


if __name__ == "__main__":
    main()
