#!/usr/bin/env python3
"""
Descarga controlada de fuentes para la revision Codex.

Todo se guarda dentro de codex-revision:
  data_raw/
  metadata/download_manifest.json
  metadata/download_manifest.csv
  metadata/download_report.md

No escribe en data/ ni en otras carpetas del proyecto principal.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urljoin, urlparse

import requests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data_raw"
META = ROOT / "metadata"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}
TIMEOUT = 45
SLEEP_SECONDS = 0.25

PRODUCTS = {
    "palta": "0804400000",
    "uva": "0806100000",
    "arandano": "0810400000",
    "esparrago": "0709200000",
}


@dataclass
class ManifestRow:
    source: str
    dataset: str
    url: str
    output_path: str
    status: str
    http_status: str = ""
    content_type: str = ""
    bytes: int = 0
    sha256: str = ""
    note: str = ""


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v for k, v in attrs}
        if tag.lower() == "a" and attrs_d.get("href"):
            self.links.append((attrs_d["href"] or "", attrs_d.get("title") or attrs_d.get("aria-label") or ""))
        if tag.lower() == "iframe" and attrs_d.get("src"):
            self.links.append((attrs_d["src"] or "", "iframe"))


def safe_name(url: str, fallback: str = "download") -> str:
    path = urlparse(url).path
    name = Path(path).name or fallback
    name = re.sub(r"[^\w.\-()%]+", "_", name, flags=re.UNICODE)
    if len(name) > 170:
        stem = Path(name).stem[:120]
        suffix = Path(name).suffix[:12]
        name = stem + suffix
    return name or fallback


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_bytes(path: Path, content: bytes) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path.stat().st_size, sha256_file(path)


def fetch(url: str, *, source: str, dataset: str, out_dir: Path, filename: str | None = None) -> tuple[ManifestRow, bytes | None]:
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = filename or safe_name(url)
    out_path = out_dir / filename
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        content_type = r.headers.get("content-type", "")
        if r.ok:
            size, digest = write_bytes(out_path, r.content)
            row = ManifestRow(
                source=source,
                dataset=dataset,
                url=url,
                output_path=str(out_path.relative_to(ROOT)),
                status="downloaded",
                http_status=str(r.status_code),
                content_type=content_type,
                bytes=size,
                sha256=digest,
            )
            return row, r.content
        row = ManifestRow(
            source=source,
            dataset=dataset,
            url=url,
            output_path=str(out_path.relative_to(ROOT)),
            status="http_error",
            http_status=str(r.status_code),
            content_type=content_type,
            note=r.text[:300] if r.text else "",
        )
        return row, None
    except Exception as exc:
        row = ManifestRow(
            source=source,
            dataset=dataset,
            url=url,
            output_path=str(out_path.relative_to(ROOT)),
            status="error",
            note=f"{type(exc).__name__}: {exc}",
        )
        return row, None
    finally:
        time.sleep(SLEEP_SECONDS)


def parse_links(base_url: str, html_bytes: bytes, patterns: Iterable[str]) -> list[str]:
    text = html_bytes.decode("utf-8", errors="replace")
    parser = LinkParser()
    parser.feed(text)
    urls: list[str] = []
    for href, title in parser.links:
        fixed_href = href.replace("\\", "/")
        full = urljoin(base_url, fixed_href)
        # Aduanet publishes malformed paths such as /aduanas/informae//aduanas/informae/x.zip
        full = full.replace("/aduanas/informae//aduanas/informae/", "/aduanas/informae/")
        low = (full + " " + title).lower()
        if any(p.lower() in low for p in patterns):
            urls.append(full)
    return list(dict.fromkeys(urls))


def extract_next_json(html_bytes: bytes) -> dict | None:
    text = html_bytes.decode("utf-8", errors="replace")
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', text, re.S)
    if not match:
        return None
    return json.loads(match.group(1))


def save_json(source: str, dataset: str, url: str, out_path: Path, obj: object, rows: list[ManifestRow], note: str = "") -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
    out_path.write_bytes(content)
    rows.append(
        ManifestRow(
            source=source,
            dataset=dataset,
            url=url,
            output_path=str(out_path.relative_to(ROOT)),
            status="generated",
            content_type="application/json",
            bytes=out_path.stat().st_size,
            sha256=sha256_file(out_path),
            note=note,
        )
    )


def download_from_page(
    rows: list[ManifestRow],
    source: str,
    page_url: str,
    page_dataset: str,
    out_dir: Path,
    patterns: list[str],
    max_files: int | None = None,
) -> list[str]:
    row, content = fetch(page_url, source=source, dataset=page_dataset, out_dir=out_dir, filename="index.html")
    rows.append(row)
    if not content:
        return []
    links = parse_links(row.url, content, patterns)
    save_json(source, f"{page_dataset}_links", page_url, out_dir / "extracted_links.json", links, rows, note=f"{len(links)} links")
    selected = links[:max_files] if max_files else links
    for link in selected:
        dataset = Path(urlparse(link).path).suffix.lower().lstrip(".") or "linked_file"
        drow, _ = fetch(link, source=source, dataset=dataset, out_dir=out_dir / "files")
        rows.append(drow)
    return links


def bcrp(rows: list[ManifestRow]) -> None:
    out = RAW / "bcrp"
    url_json = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2018-01/2026-06"
    row, content = fetch(url_json, source="BCRP", dataset="PN01207PM_json", out_dir=out, filename="PN01207PM_2018-01_2026-06.json")
    rows.append(row)
    if content:
        data = json.loads(content.decode("utf-8", errors="replace"))
        csv_path = out / "PN01207PM_2018-01_2026-06.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["periodo_bcrp", "tipo_cambio_pen_usd"])
            for p in data.get("periods", []):
                writer.writerow([p.get("name"), (p.get("values") or [""])[0]])
        rows.append(
            ManifestRow(
                "BCRP",
                "PN01207PM_csv_normalized",
                url_json,
                str(csv_path.relative_to(ROOT)),
                "generated",
                content_type="text/csv",
                bytes=csv_path.stat().st_size,
                sha256=sha256_file(csv_path),
                note=f"{len(data.get('periods', []))} periods",
            )
        )


def promperu(rows: list[ManifestRow]) -> None:
    out = RAW / "promperu_exportemos"
    summary: dict[str, object] = {}
    for product, hs in PRODUCTS.items():
        url = f"https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/{hs}"
        product_dir = out / product
        row, content = fetch(url, source="PROMPERU", dataset=f"{product}_html", out_dir=product_dir, filename="page.html")
        rows.append(row)
        if not content:
            continue
        try:
            next_data = extract_next_json(content)
            if next_data:
                save_json("PROMPERU", f"{product}_next_data", url, product_dir / "next_data.json", next_data, rows)
                data = next_data.get("props", {}).get("pageProps", {}).get("data", {})
                summary[product] = {
                    "hs_code": hs,
                    "keys": list(data.keys()) if isinstance(data, dict) else [],
                    "mercados": len(data.get("principalesMercados", {}).get("anioCerrado", [])) if isinstance(data.get("principalesMercados"), dict) else None,
                    "empresas": len(data.get("empresasExportadoras", {}).get("anioCerrado", [])) if isinstance(data.get("empresasExportadoras"), dict) else None,
                    "precios": len(data.get("preciosReferenciales", [])) if isinstance(data.get("preciosReferenciales"), list) else None,
                }
        except Exception as exc:
            rows.append(ManifestRow("PROMPERU", f"{product}_next_data", url, "", "error", note=f"parse error: {exc}"))
    save_json("PROMPERU", "summary", "product pages", out / "summary.json", summary, rows)


def nasa_power(rows: list[ManifestRow]) -> None:
    out = RAW / "nasa_power"
    coords = {
        "ica": (-14.07, -75.73),
        "la_libertad": (-8.10, -79.03),
        "piura": (-5.20, -80.63),
        "arequipa": (-16.40, -71.54),
        "lima": (-12.05, -77.04),
    }
    params = "T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN"
    for name, (lat, lon) in coords.items():
        url = (
            "https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters={params}&community=AG&longitude={lon}&latitude={lat}"
            "&start=20180101&end=20260607&format=JSON"
        )
        row, _ = fetch(url, source="NASA_POWER", dataset=f"{name}_daily_json", out_dir=out, filename=f"{name}_20180101_20260607.json")
        rows.append(row)


def un_comtrade(rows: list[ManifestRow]) -> None:
    out = RAW / "un_comtrade"
    periods = ",".join(str(y) for y in range(2018, 2027))
    for product, hs10 in PRODUCTS.items():
        hs6 = hs10[:6]
        url = (
            "https://comtradeapi.un.org/data/v1/get/C/A/HS?"
            f"reporterCode=604&period={periods}&cmdCode={hs6}&flowCode=X&partnerCode=0"
        )
        row, _ = fetch(url, source="UN_COMTRADE", dataset=f"{product}_{hs6}_annual_exports", out_dir=out, filename=f"{product}_{hs6}_annual_exports.json")
        if row.status != "downloaded":
            row.note = (row.note + " | API may require subscription key or changed endpoint").strip(" |")
        rows.append(row)


def simple_pages(rows: list[ManifestRow]) -> None:
    pages = [
        ("SUNAT", "operatividadaduanera", "https://www.sunat.gob.pe/operatividadaduanera/"),
        ("SISAP_MIDAGRI", "portal_https", "https://sistemas.midagri.gob.pe/sisap/portal/"),
        ("SISAP_MIDAGRI", "portal_http", "http://sistemas.midagri.gob.pe/sisap/portal/"),
        ("SENASA", "certificado_fitosanitario", "https://www.gob.pe/10093-obtener-certificado-fitosanitario-de-exportacion-o-reexportacion-de-plantas-productos-vegetales-y-otros-articulos-reglamentados"),
        ("SENASA", "requisitos_gobpe", "https://www.gob.pe/10950-consultar-los-requisitos-sanitarios-y-fitosanitarios-para-el-comercio-exterior"),
        ("SENASA", "consulta_requisitos_app", "https://servicios.senasa.gob.pe/consultaRequisitos/consultarRequisitos.action"),
        ("FDA", "import_refusals", "https://www.fda.gov/industry/fda-import-process/import-refusals"),
        ("FDA", "data_sets", "https://www.fda.gov/about-fda/oii-foia-electronic-reading-room/data-sets"),
        ("FDA", "import_refusals_irr", "http://www.accessdata.fda.gov/scripts/ImportRefusals/ir_index.cfm"),
        ("RASFF", "food_safety_page", "https://food.ec.europa.eu/food-safety/rasff_en"),
        ("RASFF", "rasff_window_search", "https://webgate.ec.europa.eu/rasff-window/screen/search"),
        ("FAOSTAT", "portal_es", "https://www.fao.org/faostat/es/"),
        ("FAOSTAT", "api_portal_note", "https://www.fao.org/statistics/highlights-archive/highlights-detail/faostat-launches-a-new-api-developer-portal-to-make-data-access-easier/en"),
        ("ITC", "trade_map", "https://www.intracen.org/resources/tools/trade-map"),
        ("INEI", "microdatos", "https://proyectos.inei.gob.pe/microdatos/"),
        ("INEI", "ena_2024_query", "https://proyectos.inei.gob.pe/microdatos/consulta.asp?cmbTrimestre=62&cmbanno=2024&cmbencuesta=ENCUESTA+NACIONAL+AGROPECUARIA"),
        ("WORLD_BANK", "pink_sheet_page", "https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/world-bank-commodities-price-data-the-pink-sheet"),
        ("WORLD_BANK", "pink_sheet_csv_candidate", "http://pubdocs.worldbank.org/en/561011504107123456/CMO-Historical-Data-Monthly.csv"),
    ]
    for source, dataset, url in pages:
        row, _ = fetch(url, source=source, dataset=dataset, out_dir=RAW / source.lower() / dataset, filename="index.html" if not url.lower().endswith(".csv") else safe_name(url))
        rows.append(row)


def senamhi(rows: list[ManifestRow]) -> None:
    out = RAW / "senamhi"
    download_from_page(rows, "SENAMHI", "https://www.senamhi.gob.pe/site/descarga-datos/", "descarga_datos", out / "descarga_datos", [".php", "descarga", "map_hist_data"])
    station_page = "https://www.senamhi.gob.pe/servicios/?p=estaciones"
    row, content = fetch(station_page, source="SENAMHI", dataset="estaciones_index", out_dir=out / "estaciones", filename="index.html")
    rows.append(row)
    if content:
        links = parse_links(station_page, content, ["dp=ica", "dp=la-libertad", "dp=piura", "dp=arequipa", "dp=lima"])
        save_json("SENAMHI", "estaciones_departamento_links", station_page, out / "estaciones" / "department_links.json", links, rows)
        for link in links:
            dep = re.search(r"dp=([^&]+)", link)
            filename = f"{dep.group(1) if dep else safe_name(link, 'department')}.html"
            drow, _ = fetch(link, source="SENAMHI", dataset="estaciones_departamento", out_dir=out / "estaciones" / "departamentos", filename=filename)
            rows.append(drow)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    RAW.mkdir(parents=True, exist_ok=True)
    META.mkdir(parents=True, exist_ok=True)
    rows: list[ManifestRow] = []

    started = datetime.now(timezone.utc).isoformat()

    # Direct page/file discovery downloads.
    download_from_page(
        rows,
        "ADUANET",
        "http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm",
        "bases_regimenes_definitivos",
        RAW / "aduanet_bases",
        [".zip", ".xls"],
    )
    bcrp(rows)
    promperu(rows)
    download_from_page(
        rows,
        "MIDAGRI",
        "https://www.gob.pe/institucion/midagri/informes-publicaciones/2730438-compendio-anual-de-comercio-exterior-agrario",
        "compendio_comercio_exterior_agrario",
        RAW / "midagri_compendio",
        [".pdf", ".xlsx", ".xls", ".zip"],
    )
    senamhi(rows)
    nasa_power(rows)
    download_from_page(
        rows,
        "APN",
        "https://www.gob.pe/institucion/apn/informes-publicaciones/6573509-estadisticas-apn-2025-trafico-de-carga",
        "trafico_carga_2025",
        RAW / "apn_2025",
        [".pdf", ".xlsx"],
    )
    download_from_page(
        rows,
        "APN",
        "https://www.gob.pe/institucion/apn/informes-publicaciones/5425311-estadisticas-apn-2024-trafico-de-carga",
        "trafico_carga_2024",
        RAW / "apn_2024",
        [".pdf", ".xlsx"],
    )
    ositran_links = download_from_page(
        rows,
        "OSITRAN",
        "https://www.gob.pe/104704-acceder-a-datos-abiertos-de-puertos-del-ositran-en-la-plataforma-nacional-de-datos-abiertos-pnda",
        "gobpe_puertos",
        RAW / "ositran_gobpe",
        ["datosabiertos.gob.pe", "puertos"],
    )
    pnda_url = "https://www.datosabiertos.gob.pe/search/field_tags/puertos-623/type/dataset?query=OSITRAN&sort_by=changed&sort_order=DESC"
    dataset_links = download_from_page(
        rows,
        "OSITRAN_PNDA",
        pnda_url,
        "search_puertos_ositran",
        RAW / "ositran_pnda",
        ["dataset/", "csv", "xlsx"],
    )
    # Follow first layer of dataset pages to capture resources.
    for link in dataset_links:
        if "/dataset/" not in link:
            continue
        slug = safe_name(link, "dataset").replace(".html", "")
        drow, content = fetch(link, source="OSITRAN_PNDA", dataset="dataset_page", out_dir=RAW / "ositran_pnda" / "datasets" / slug, filename="index.html")
        rows.append(drow)
        if not content:
            continue
        resources = parse_links(link, content, [".csv", ".xlsx", ".xls"])
        save_json("OSITRAN_PNDA", "dataset_resources", link, RAW / "ositran_pnda" / "datasets" / slug / "resources.json", resources, rows)
        for res in resources:
            rrow, _ = fetch(res, source="OSITRAN_PNDA", dataset="resource_file", out_dir=RAW / "ositran_pnda" / "datasets" / slug / "files")
            rows.append(rrow)

    simple_pages(rows)
    un_comtrade(rows)

    finished = datetime.now(timezone.utc).isoformat()
    manifest_json = META / "download_manifest.json"
    manifest_csv = META / "download_manifest.csv"
    manifest_json.write_text(json.dumps([asdict(r) for r in rows], ensure_ascii=False, indent=2), encoding="utf-8")
    with manifest_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()) if rows else list(ManifestRow.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    downloaded = [r for r in rows if r.status in {"downloaded", "generated"}]
    errors = [r for r in rows if r.status not in {"downloaded", "generated"}]
    total_bytes = sum(r.bytes for r in downloaded)
    report = META / "download_report.md"
    report.write_text(
        "\n".join(
            [
                "# Reporte de descarga completa de fuentes",
                "",
                f"Inicio UTC: {started}",
                f"Fin UTC: {finished}",
                f"Workspace: `{ROOT}`",
                "",
                "## Resumen",
                "",
                f"- Entradas de manifiesto: {len(rows)}",
                f"- Descargados/generados: {len(downloaded)}",
                f"- Errores/bloqueos HTTP: {len(errors)}",
                f"- Bytes descargados/generados: {total_bytes}",
                "",
                "## Errores o bloqueos",
                "",
                *(f"- `{r.source}` / `{r.dataset}` / `{r.status}` / HTTP `{r.http_status}`: {r.url} :: {r.note[:180]}" for r in errors),
                "",
                "## Archivos de control",
                "",
                "- `metadata/download_manifest.json`",
                "- `metadata/download_manifest.csv`",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Manifest rows: {len(rows)}")
    print(f"Downloaded/generated: {len(downloaded)}")
    print(f"Errors: {len(errors)}")
    print(f"Bytes: {total_bytes}")
    print(f"Report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
