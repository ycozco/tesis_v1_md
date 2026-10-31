"""Verify saved heuristic choices, peer references and unchanged source values."""
import csv
import datetime as dt
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
base = root / "datasets/fuentes/2026-10-31/conciliacion"
out = base / "resolucion-analitica"


def read(p):
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def date(r):
    return dt.datetime.strptime(r["fecha_embarque_raw"], "%Y%m%d").date()


def unit(r):
    return float(r["valor_fob_usd"]) / float(r["peso_neto_kg"])


summary = json.loads((out / "resumen.json").read_text(encoding="utf-8"))
for name, sha in summary["hashes_entradas"].items():
    assert hashlib.sha256((base / name).read_bytes()).hexdigest() == sha
clean, q = read(base / "vista-conciliada.csv"), read(base / "cuarentena.csv")
resolved = read(out / "vista-resuelta-analitica.csv")
choices = read(out / "decisiones-resolucion.csv")
refs = read(out / "referencias-por-caso.csv")
variants = read(out / "alternativas.csv")
reference_map = {r["id_declaracion_serie_sha256"]: r for r in clean}
all_sources = {(r["archivo_fuente"], r["fila_fuente"]): r for r in clean + q}
assert len(resolved) == summary["filas_vista_resuelta"] == len(clean) + len({r["id_declaracion_serie_sha256"] for r in q})
assert len({r["id_declaracion_serie_sha256"] for r in resolved}) == len(resolved)
for row in resolved:
    original = all_sources[row["archivo_fuente"], row["fila_fuente"]]
    assert all(row[k] == v for k, v in original.items())
    assert row["confirmacion_oficial"] != "si"
for case in choices:
    key = case["id_declaracion_serie_sha256"]
    case_refs = [r for r in refs if r["caso_sha256"] == key]
    assert len({r["serie_referencia_sha256"] for r in case_refs}) == len(case_refs)
    peers = [reference_map[r["serie_referencia_sha256"]] for r in case_refs]
    selected = all_sources[case["archivo_elegido"], case["fila_elegida"]]
    window = 90 if case["referencia"].endswith("90_dias") else 365
    assert len(peers) == int(case["n_referencias"]) >= summary["minimo_referencias"]
    for r, peer in zip(case_refs, peers):
        assert r["huella_referencia"] == peer["huella_campos_analiticos"]
        assert (peer["producto"], peer["destino"]) == (selected["producto"], selected["destino"])
        assert 0 <= (date(selected) - date(peer)).days <= window
    center = statistics.median(math.log(unit(r)) for r in peers)
    assert abs(center - float(case["mediana_log_valor_unitario"])) < 1e-12
    options = [r for r in variants if r["id_declaracion_serie_sha256"] == key]
    scores = [abs(math.log(unit(r)) - center) for r in options]
    chosen = [r for r in options if r["elegida"] == "si"]
    assert len(chosen) == 1
    assert chosen[0]["huella_variante"] == case["huella_elegida"]
    assert abs(math.log(unit(selected)) - center) <= min(scores) + summary["tolerancia_empate"]
for r in read(out / "sensibilidad.csv"):
    total = sum(Decimal(x[r["variable"]]) for x in resolved if x["producto"] == r["producto"])
    assert total == Decimal(r["seleccion_heuristica"])
    assert Decimal(r["minimo_variantes_observadas"]) <= total <= Decimal(r["maximo_variantes_observadas"])
print(json.dumps({"estado": "OK", "casos_heuristicos_verificados": len(choices),
                  "filas_resueltas_verificadas": len(resolved), "entradas_originales_preservadas": True}))
