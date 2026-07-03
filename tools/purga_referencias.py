"""
purga_referencias.py
====================
Reemplaza citas tipo [@clave_bib] por formato APA legible en los Markdown de docs/.
Tambien corrige inconsistencias de claves entre documentos y refs.bib.

Uso:
    py scripts/purga_referencias.py
"""

from __future__ import annotations

import re
from pathlib import Path

# ----------------------------------------------------------------------------
# Mapeo clave_bib -> cita APA (en parentesis, formato narrativo final)
# ----------------------------------------------------------------------------

MAPEO_APA = {
    # Predictivos GBDT y tabular
    "chen2016xgboost": "(Chen & Guestrin, 2016)",
    "ke2017lightgbm": "(Ke et al., 2017)",
    "prokhorenkova2018catboost": "(Prokhorenkova et al., 2018)",
    "gorishniy2021ft": "(Gorishniy et al., 2021)",
    "grinsztajn2022trees": "(Grinsztajn et al., 2022)",
    "arik2021tabnet": "(Arik & Pfister, 2021)",
    "friedman2001greedy": "(Friedman, 2001)",
    # Series temporales
    "lim2020tft": "(Lim et al., 2021)",
    "zeng2023dlinear": "(Zeng et al., 2023)",
    "liu2024itransformer": "(Liu et al., 2024)",
    "nie2023patchtst": "(Nie et al., 2023)",
    "nhts2022": "(Challu et al., 2022)",
    "nbeats2019": "(Oreshkin et al., 2020)",
    "chronos2024": "(Ansari et al., 2024)",
    "taylor2018prophet": "(Taylor & Letham, 2017)",
    "hyndman2008forecasting": "(Hyndman & Khandakar, 2008)",
    # Anomalias
    "liu2008isolationforest": "(Liu et al., 2008)",
    "liu2008iforest": "(Liu et al., 2008)",
    "breunig2000lof": "(Breunig et al., 2000)",
    "ruff2018deepsvdd": "(Ruff et al., 2018)",
    "li2022ecod": "(Li et al., 2022)",
    "han2022adbench": "(Han et al., 2022)",
    "zhao2019pyod": "(Zhao et al., 2019)",
    # Explicabilidad
    "lundberg2017shap": "(Lundberg & Lee, 2017)",
    "lundberg2020treeshap": "(Lundberg et al., 2020)",
    "ribeiro2016lime": "(Ribeiro et al., 2016)",
    # LLM, RAG y alucinaciones
    "tabllm2023": "(Hegselmann et al., 2023)",
    "lewis2020rag": "(Lewis et al., 2020)",
    "schneider2025rag": "(Schneider et al., 2025)",
    "park2024llm": "(Park, 2024)",
    "auditcopilot2025": "(Kadir et al., 2025)",
    "kadir2025auditcopilot": "(Kadir et al., 2025)",
    "auditmai2024": "(Waltersdorfer et al., 2024)",
    "tsai2025llmanomaly": "(Tsai et al., 2025)",
    "ji2023survey": "(Ji et al., 2023)",
    "survey2026hallucination": "(Maynez et al., 2026)",
    "barclays2025beyond": "(Barclays Research, 2025)",
    # Fraude / Auditoria
    "mongolia2025fraud": "(JRFM, 2025)",
    "thanathamathee2024shap": "(Thanathamathee et al., 2024)",
    "almalki2025fraud": "(Almalki & Masud, 2025)",
    "patel2024auditing": "(Patel et al., 2024)",
    # Gobernanza, MLOps, documentacion
    "sculley2015hidden": "(Sculley et al., 2015)",
    "kreuzberger2022mlops": "(Kreuzberger et al., 2022)",
    "gebru2021datasheets": "(Gebru et al., 2021)",
    "mitchell2019modelcards": "(Mitchell et al., 2019)",
    "mitchell2019model": "(Mitchell et al., 2019)",
    "nist2023aia": "(NIST, 2023)",
    # Regulacion
    "sbs2023riesgos": "(SBS, 2023)",
    "pcm2025leyia": "(PCM, 2025)",
    "eu2024aiact": "(Parlamento Europeo y Consejo, 2024)",
    "prenio2024managing": "(Prenio & Yong, 2024)",
    # Metodologia
    "creswell2018research": "(Creswell & Creswell, 2018)",
    "page2021prisma": "(Page et al., 2021)",
    "cohen1960kappa": "(Cohen, 1960)",
    "akiba2019optuna": "(Akiba et al., 2019)",
    # Metricas texto
    "papineni2002bleu": "(Papineni et al., 2002)",
    "lin2004rouge": "(Lin, 2004)",
    # Datos / fuentes
    "midagri2026boletin": "(MIDAGRI, 2026)",
    "jesus2022baf": "(Jesus et al., 2022)",
}

# Archivos a procesar (solo activos; NO procesar tesis.md ni tesis-v2.md)
DOCS_DIR = Path("docs")
ACTIVE_DOCS = sorted(
    p for p in DOCS_DIR.glob("*.md")
    if p.name not in {"tesis.md", "tesis-v2.md"}
)

CITE_SINGLE = re.compile(r"\[@([a-zA-Z0-9_-]+)\]")
# Citas multiples separadas por ; o , : "[@k1; @k2]" o "[@k1, @k2]"
CITE_MULTI = re.compile(r"\[(@[a-zA-Z0-9_-]+(?:[;,]\s*@[a-zA-Z0-9_-]+)+)\]")
# Las claves individuales dentro del bloque multi
KEY_IN_MULTI = re.compile(r"@([a-zA-Z0-9_-]+)")


def _apa_from_key(key: str) -> str:
    """Devuelve la cita APA sin parentesis exteriores para combinar en bloque multi."""
    full = MAPEO_APA.get(key)
    if full is None:
        return f"@{key}"  # marcador para detectar faltantes
    return full.strip("()")  # remover parentesis para combinarlas


def replace_citations(text: str) -> tuple[str, set[str]]:
    """Reemplaza [@clave] y [@k1; @k2] por la cita APA correspondiente."""
    not_found: set[str] = set()

    def _sub_multi(match: re.Match[str]) -> str:
        inner = match.group(1)
        keys = KEY_IN_MULTI.findall(inner)
        parts: list[str] = []
        for k in keys:
            apa = MAPEO_APA.get(k)
            if apa is None:
                not_found.add(k)
                parts.append(f"@{k}")
            else:
                parts.append(apa.strip("()"))
        return "(" + "; ".join(parts) + ")"

    def _sub_single(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in MAPEO_APA:
            return MAPEO_APA[key]
        not_found.add(key)
        return match.group(0)

    new_text = CITE_MULTI.sub(_sub_multi, text)
    new_text = CITE_SINGLE.sub(_sub_single, new_text)
    return new_text, not_found


def main() -> None:
    print(f"Procesando {len(ACTIVE_DOCS)} archivos activos en {DOCS_DIR}/")
    total_reemplazos = 0
    todas_no_encontradas: set[str] = set()

    for path in ACTIVE_DOCS:
        original = path.read_text(encoding="utf-8")
        replaced, not_found = replace_citations(original)
        n_repl = original.count("[@") - replaced.count("[@")
        if n_repl > 0:
            path.write_text(replaced, encoding="utf-8")
            print(f"  {path.name}: {n_repl} reemplazos")
            total_reemplazos += n_repl
        todas_no_encontradas.update(not_found)

    print(f"\nTotal reemplazos: {total_reemplazos}")
    if todas_no_encontradas:
        print(f"\nClaves NO mapeadas (revisar):")
        for k in sorted(todas_no_encontradas):
            print(f"  - {k}")
    else:
        print("Todas las claves fueron mapeadas correctamente.")


if __name__ == "__main__":
    main()
