"""An explicitly heuristic, reversible selection of observed conflict variants.

Does not change the conservative reconciled view or the quarantine. Stdlib only.
"""
import csv
import datetime as dt
import hashlib
import json
import math
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
import statistics
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
BASE = ROOT / "datasets/fuentes/2026-10-31/conciliacion"
OUT = BASE / "resolucion-analitica"
OUT.mkdir(parents=True, exist_ok=True)
VERSION = "seleccion-heuristica-observada-1.0"
MIN_PEERS = 20
TIE_TOLERANCE = 1e-12


def read(file):
    with file.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def write(name, fields, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def file_hash(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def date(row):
    return dt.datetime.strptime(row["fecha_embarque_raw"], "%Y%m%d").date()


def unit(row):
    return float(row["valor_fob_usd"]) / float(row["peso_neto_kg"])


fields, clean = read(BASE / "vista-conciliada.csv")
_, quarantine = read(BASE / "cuarentena.csv")
input_hashes = {name: file_hash(BASE / name) for name in (
    "vista-conciliada.csv", "cuarentena.csv", "conflictos-detalle.json")}
details = json.loads((BASE / "conflictos-detalle.json").read_text(encoding="utf-8"))
conflicts = {case["id_declaracion_serie_sha256"] for case in details["casos"]}
groups = defaultdict(dict)
for row in quarantine:
    groups[row["id_declaracion_serie_sha256"]].setdefault(
        row["huella_campos_analiticos"], row)
peer_groups = defaultdict(list)
for row in clean:
    if unit(row) > 0:
        peer_groups[row["producto"], row["destino"]].append((date(row), math.log(unit(row))))

choices, candidates, restored = [], [], []
reference_rows = []
chosen_by_key = {}
for key in sorted(groups):
    variants = list(groups[key].values())
    if key not in conflicts:
        assert len(variants) == 1
        selected = variants[0]
        restored.append({**selected, "resolucion_analitica": "sin_conflicto_directo_declaracion_resuelta",
                         "confirmacion_oficial": "no", "version_regla": VERSION})
        chosen_by_key[key] = selected
        continue
    same = variants[0]
    assert all((r["producto"], r["destino"], r["fecha_embarque_raw"]) ==
               (same["producto"], same["destino"], same["fecha_embarque_raw"]) for r in variants)
    target_date = date(same)
    pool = peer_groups[same["producto"], same["destino"]]
    peers, tier = [], "sin_referencia_suficiente"
    # Fixed hierarchy: same product/destination only, never borrow other markets.
    for days in (90, 365):
        available = [value for when, value in pool
                     if 0 <= (target_date - when).days <= days]
        if len(available) >= MIN_PEERS:
            peers, tier = available, "producto_destino_" + str(days) + "_dias"
            break
    center = statistics.median(peers) if peers else None
    scores = []
    for row in variants:
        score = abs(math.log(unit(row)) - center) if center is not None and unit(row) > 0 else None
        scores.append((score, row))
    finite = [(score, row) for score, row in scores if score is not None]
    if finite:
        best = min(score for score, _ in finite)
        tied = [row for score, row in finite if abs(score - best) <= TIE_TOLERANCE]
        selected = min(tied, key=lambda r: r["huella_campos_analiticos"])
        rule = "cercania_mediana_log_valor_unitario" if len(tied) == 1 else "empate_resuelto_por_hash_sin_evidencia_adicional"
    else:
        selected = min(variants, key=lambda r: r["huella_campos_analiticos"])
        rule = "sin_referencia_desempate_hash_no_sustentado_estadisticamente"
    chosen_by_key[key] = selected
    selected_score = next(score for score, row in scores if row is selected)
    choice = {
        "id_declaracion_serie_sha256": key,
        "id_declaracion_sha256": same["id_declaracion_sha256"],
        "producto": same["producto"], "destino": same["destino"],
        "fecha_embarque_raw": same["fecha_embarque_raw"],
        "archivo_elegido": selected["archivo_fuente"], "fila_elegida": selected["fila_fuente"],
        "huella_elegida": selected["huella_campos_analiticos"],
        "valor_fob_elegido": selected["valor_fob_usd"], "peso_neto_elegido": selected["peso_neto_kg"],
        "valor_unitario_elegido": unit(selected), "referencia": tier, "n_referencias": len(peers),
        "mediana_log_valor_unitario": center, "distancia_elegida": selected_score,
        "regla": rule, "confirmacion_oficial": "no", "version_regla": VERSION,
        "sustento_metodologico": "NIST-EDA-1.3.5.1; decision de diseno propia, no validacion aduanera",
    }
    choices.append(choice)
    # Exact references used to construct each peer median are stored by hash.
    window = 90 if tier.endswith("90_dias") else 365
    for row in clean:
        if row["producto"] == same["producto"] and row["destino"] == same["destino"] and unit(row) > 0:
            if peers and 0 <= (target_date - date(row)).days <= window:
                reference_rows.append({"caso_sha256": key,
                                       "serie_referencia_sha256": row["id_declaracion_serie_sha256"],
                                       "huella_referencia": row["huella_campos_analiticos"]})
    for score, row in scores:
        candidates.append({
            "id_declaracion_serie_sha256": key, "huella_variante": row["huella_campos_analiticos"],
            "archivo_fuente": row["archivo_fuente"], "fila_fuente": row["fila_fuente"],
            "valor_fob_usd": row["valor_fob_usd"], "peso_neto_kg": row["peso_neto_kg"],
            "valor_unitario": unit(row), "distancia_referencia": score,
            "elegida": "si" if row is selected else "no", "regla": rule,
        })
    restored.append({**selected, "resolucion_analitica": "variante_observada_elegida_heuristicamente",
                     "confirmacion_oficial": "no", "version_regla": VERSION})

analytical = [{**row, "resolucion_analitica": "base_sin_conflicto_directo",
               "confirmacion_oficial": "no_verificada", "version_regla": VERSION} for row in clean] + restored
assert len(analytical) == len(clean) + len(groups)
assert len({r["id_declaracion_serie_sha256"] for r in analytical}) == len(analytical)
assert len(choices) == len(conflicts)
write("vista-resuelta-analitica.csv", fields + ["resolucion_analitica", "confirmacion_oficial", "version_regla"], analytical)
write("decisiones-resolucion.csv", list(choices[0]), choices)
write("alternativas.csv", list(candidates[0]), candidates)
write("referencias-por-caso.csv", ["caso_sha256", "serie_referencia_sha256", "huella_referencia"], reference_rows)

# Component-wise envelope of observed alternatives; not confidence intervals,
# not a single joint scenario when the FOB and weight extrema use different rows.
sensitivity = []
for product in sorted({r["producto"] for r in analytical}):
    core = [r for r in clean if r["producto"] == product]
    extra = [r for r in restored if r["producto"] == product]
    base_fob = sum(Decimal(r["valor_fob_usd"]) for r in core)
    base_weight = sum(Decimal(r["peso_neto_kg"]) for r in core)
    for variable, base_total in (("valor_fob_usd", base_fob), ("peso_neto_kg", base_weight)):
        selected_total = base_total + sum(Decimal(r[variable]) for r in extra)
        minimum = base_total + sum(min(Decimal(r[variable]) for r in v.values())
                                   for v in groups.values() if next(iter(v.values()))["producto"] == product)
        maximum = base_total + sum(max(Decimal(r[variable]) for r in v.values())
                                   for v in groups.values() if next(iter(v.values()))["producto"] == product)
        sensitivity.append({"producto": product, "variable": variable, "base_conservadora": str(base_total),
                            "seleccion_heuristica": str(selected_total), "minimo_variantes_observadas": str(minimum),
                            "maximo_variantes_observadas": str(maximum),
                            "amplitud_relativa_porcentaje": str(100 * (maximum - minimum) / selected_total)})
write("sensibilidad.csv", list(sensitivity[0]), sensitivity)
assert all(file_hash(BASE / name) == value for name, value in input_hashes.items())
summary = {"version_regla": VERSION, "fecha": "2026-10-31",
           "estado": "resolucion_operativa_heuristica_no_confirmacion_oficial",
           "minimo_referencias": MIN_PEERS, "ventanas_dias": [90, 365],
           "tolerancia_empate": TIE_TOLERANCE, "hashes_entradas": input_hashes,
           "script_sha256": file_hash(Path(__file__)), "filas_base": len(clean),
           "series_reincorporadas": len(restored), "series_elegidas_heuristicamente": len(choices),
           "series_sin_conflicto_directo_reincorporadas": len(restored) - len(choices),
           "filas_vista_resuelta": len(analytical), "reglas_aplicadas": dict(Counter(c["regla"] for c in choices)),
           "referencias_aplicadas": dict(Counter(c["referencia"] for c in choices)),
           "por_producto": dict(Counter(r["producto"] for r in analytical)),
           "cuarentena_original_conservada": True, "sensibilidad": sensitivity}
(OUT / "resumen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in summary.items() if k not in ("sensibilidad", "hashes_entradas")}, ensure_ascii=False))
