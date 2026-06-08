from __future__ import annotations

import csv
import html
import json
import re
import time
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data_raw" / "sisap_midagri" / "massive"
OUT_DIR = BASE_DIR / "data_processed" / "sisap_midagri"
META_DIR = BASE_DIR / "metadata"

ENDPOINT = "http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar"

RUN_DATE = datetime.now().strftime("%Y-%m-%d")
YEARS = list(range(2018, 2027))
MONTHS = list(range(1, 13))

PRODUCTS = [
    {
        "producto": "palta",
        "producto_id": "0626",
        "mercado": "15011502",
        "mercado_nombre": "Mercado mayorista nro 2-frutas",
    },
    {
        "producto": "uva",
        "producto_id": "0637",
        "mercado": "15011502",
        "mercado_nombre": "Mercado mayorista nro 2-frutas",
    },
    {
        "producto": "esparrago",
        "producto_id": "0216",
        "mercado": "15011501",
        "mercado_nombre": "Gran mercado mayorista de lima",
    },
]

VARIABLES = [
    ("precio_prom", "Precio Promedio"),
    ("volumen", "Volumen"),
]


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def numeric_or_text(value: str) -> str:
    value = clean_text(value)
    value = value.replace(",", "")
    return value


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.in_cell = False
        self.current_cell: list[str] = []
        self.current_row: list[dict[str, str]] = []
        self.rows: list[list[dict[str, str]]] = []
        self.current_attrs: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self.in_table = True
        elif self.in_table and tag == "tr":
            self.current_row = []
        elif self.in_table and tag in {"td", "th"}:
            self.in_cell = True
            self.current_cell = []
            self.current_attrs = {k: v or "" for k, v in attrs}
        elif self.in_cell and tag == "br":
            self.current_cell.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if self.in_table and tag in {"td", "th"} and self.in_cell:
            self.current_row.append(
                {
                    "text": clean_text(html.unescape("".join(self.current_cell))),
                    "colspan": self.current_attrs.get("colspan", "1"),
                    "rowspan": self.current_attrs.get("rowspan", "1"),
                }
            )
            self.in_cell = False
        elif self.in_table and tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data)


def extract_headings(html_text: str) -> str:
    headings = re.findall(r"<h1[^>]*>(.*?)</h1>", html_text, flags=re.I | re.S)
    return " | ".join(clean_text(html.unescape(re.sub(r"<[^>]+>", " ", h))) for h in headings)


def parse_sisap_html(html: str) -> tuple[list[dict[str, str]], str]:
    error_match = re.search(r"<p[^>]*mensajeDeError[^>]*>(.*?)</p>", html, flags=re.I | re.S)
    if error_match:
        message = re.sub(r"<[^>]+>", " ", error_match.group(1))
        return [], clean_text(html_module_unescape(message))

    parser = TableParser()
    parser.feed(html)
    table_rows = parser.rows
    if len(table_rows) < 3:
        return [], "sin_tabla"

    heading = extract_headings(html)
    first_header = table_rows[0]
    varieties: list[str] = []
    for cell in first_header[1:]:
        colspan = int(cell.get("colspan") or "1")
        varieties.extend([cell["text"]] * colspan)

    rows: list[dict[str, str]] = []
    for tr in table_rows[2:]:
        if len(tr) < 2:
            continue
        fecha = tr[0]["text"]
        for idx, cell in enumerate(tr[1:]):
            variedad = varieties[idx] if idx < len(varieties) else f"variedad_{idx + 1}"
            value = numeric_or_text(cell["text"])
            if value == "":
                continue
            rows.append(
                {
                    "periodo_sisap": fecha,
                    "variedad": variedad,
                    "valor": value,
                    "titulo_reporte": heading,
                }
            )
    if not rows:
        return [], "sin_filas_parseables"
    return rows, heading[:300]


def html_module_unescape(value: str) -> str:
    return html.unescape(value)


def make_payload(product: dict[str, str], variable: str, year: int, month: int) -> list[tuple[str, str]]:
    return [
        ("mercado", product["mercado"]),
        ("variables[]", variable),
        ("productos[]", product["producto_id"]),
        ("producto", product["producto_id"]),
        ("periodicidad", "mensual"),
        ("fecha", ""),
        ("desde", ""),
        ("hasta", ""),
        ("anios[]", str(year)),
        ("meses[]", f"{month:02d}"),
        ("__ajax_carga_final", "true"),
        ("ajax", "true"),
    ]


def main() -> int:
    ensure_dirs()
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 tesis-yoset codex-revision",
            "Referer": "http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/",
            "X-Requested-With": "XMLHttpRequest",
        }
    )

    out_csv = OUT_DIR / f"sisap_midagri_mensual_2018_2026_{RUN_DATE}.csv"
    manifest_csv = META_DIR / f"sisap_midagri_mensual_manifest_{RUN_DATE}.csv"
    manifest_json = META_DIR / f"sisap_midagri_mensual_manifest_{RUN_DATE}.json"

    all_rows: list[dict[str, str]] = []
    manifest: list[dict[str, str | int]] = []

    total = len(PRODUCTS) * len(VARIABLES) * len(YEARS) * len(MONTHS)
    done = 0
    for product in PRODUCTS:
        for variable, variable_label in VARIABLES:
            for year in YEARS:
                for month in MONTHS:
                    done += 1
                    raw_subdir = RAW_DIR / product["producto"] / variable / str(year)
                    raw_subdir.mkdir(parents=True, exist_ok=True)
                    raw_file = raw_subdir / f"{year}-{month:02d}.html"
                    status = "error"
                    note = ""
                    row_count = 0
                    try:
                        response = session.post(
                            ENDPOINT,
                            data=make_payload(product, variable, year, month),
                            timeout=45,
                        )
                        raw_file.write_bytes(response.content)
                        if response.status_code != 200:
                            status = f"http_{response.status_code}"
                            note = response.text[:200]
                        else:
                            parsed_rows, note = parse_sisap_html(response.text)
                            row_count = len(parsed_rows)
                            status = "ok" if row_count else "sin_datos"
                            for parsed in parsed_rows:
                                flat = {
                                    "fuente": "MIDAGRI SISAP",
                                    "endpoint": ENDPOINT,
                                    "fecha_descarga": RUN_DATE,
                                    "periodicidad": "mensual",
                                    "anio": str(year),
                                    "mes": f"{month:02d}",
                                    "producto": product["producto"],
                                    "producto_id": product["producto_id"],
                                    "mercado": product["mercado"],
                                    "mercado_nombre": product["mercado_nombre"],
                                    "variable": variable,
                                    "variable_label": variable_label,
                                    "raw_file": str(raw_file.relative_to(BASE_DIR)),
                                }
                                flat.update(parsed)
                                all_rows.append(flat)
                    except Exception as exc:
                        note = repr(exc)

                    manifest.append(
                        {
                            "producto": product["producto"],
                            "producto_id": product["producto_id"],
                            "mercado": product["mercado"],
                            "variable": variable,
                            "anio": year,
                            "mes": f"{month:02d}",
                            "status": status,
                            "rows": row_count,
                            "raw_file": str(raw_file.relative_to(BASE_DIR)),
                            "note": clean_text(str(note))[:500],
                        }
                    )
                    print(f"[{done}/{total}] {product['producto']} {variable} {year}-{month:02d}: {status} ({row_count})")
                    time.sleep(0.2)

    fieldnames = sorted({key for row in all_rows for key in row.keys()})
    preferred = [
        "fuente",
        "endpoint",
        "fecha_descarga",
        "periodicidad",
        "anio",
        "mes",
        "producto",
        "producto_id",
        "mercado",
        "mercado_nombre",
        "variable",
        "variable_label",
        "periodo_sisap",
        "variedad",
        "valor",
        "titulo_reporte",
        "raw_file",
    ]
    ordered = [f for f in preferred if f in fieldnames] + [f for f in fieldnames if f not in preferred]
    with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=ordered)
        writer.writeheader()
        writer.writerows(all_rows)

    with manifest_csv.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)

    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "run_date": RUN_DATE,
        "endpoint": ENDPOINT,
        "queries": len(manifest),
        "rows": len(all_rows),
        "ok_queries": sum(1 for item in manifest if item["status"] == "ok"),
        "sin_datos_queries": sum(1 for item in manifest if item["status"] == "sin_datos"),
        "error_queries": sum(1 for item in manifest if item["status"] not in {"ok", "sin_datos"}),
        "csv": str(out_csv.relative_to(BASE_DIR)),
        "manifest_csv": str(manifest_csv.relative_to(BASE_DIR)),
        "manifest_json": str(manifest_json.relative_to(BASE_DIR)),
    }
    (META_DIR / f"sisap_midagri_mensual_summary_{RUN_DATE}.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
