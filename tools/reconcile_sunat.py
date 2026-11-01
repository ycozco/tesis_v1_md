"""Reconcile available SUNAT declaration snapshots without modifying sources.

Usage: python -B tools/reconcile_sunat.py <repository root>
Uses only the Python standard library. See output/protocolo.md for assumptions.
"""
import csv
import datetime as dt
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import re
import struct
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
BASE = (ROOT / (sys.argv[2] if len(sys.argv) > 2 else "datasets/fuentes/2026-10-31")).resolve()
if not BASE.is_relative_to(ROOT):
    raise ValueError('Collection must be inside repository')
RAW_ROOTS = [ROOT / "data/fuentes_2026-10-31/sunat", ROOT / "data/busqueda_2026-11-01"]
OUT = BASE / "conciliacion"
OUT.mkdir(parents=True, exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def raw_file(name):
    for folder in RAW_ROOTS:
        for candidate in [folder/name, folder/name.replace('.DBF', '.zip.DBF')]:
            if candidate.is_file(): return candidate
    raise FileNotFoundError('Missing exact source: ' + name)


def packet_end(name):
    match = re.fullmatch(r"x\d{2}(\d{2})(\d{2})(\d{2})\.zip", name)
    if not match:
        raise ValueError("Unrecognized packet: " + name)
    day, month, year = map(int, match.groups())
    return dt.date(2000 + year, month, day).isoformat()


def read_csv(file):
    with file.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def write_csv(name, columns, records):
    with (OUT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


input_bytes = (BASE / "observaciones-sunat.csv").read_bytes()
columns, rows = read_csv(BASE / "observaciones-sunat.csv")
manifest = json.loads((BASE / "manifest-sunat.json").read_text(encoding="utf-8"))
assert len(rows) == manifest["filas_seleccionadas"]
references = {(row["archivo_fuente"], int(row["fila_fuente"])): i
              for i, row in enumerate(rows)}
assert len(references) == len(rows)
latest_declaration = {}
row_declaration = {}
row_key_invalid = set()
source_checks = []
# Inspect ALL DBF rows, including products outside the filtered CSV. A newer
# declaration must supersede its older snapshot even if a series changed HS.
for source in manifest["fuentes"]:
    name = source["archivo"]
    end = packet_end(name)
    zipped = raw_file(name).read_bytes()
    assert sha(zipped).upper() == source["sha256"].upper(), name
    dbf_path = raw_file(name.replace(".zip", ".DBF"))
    data = dbf_path.read_bytes()
    count = struct.unpack_from("<I", data, 4)[0]
    header, record_length = struct.unpack_from("<HH", data, 8)
    assert header + count * record_length <= len(data), name
    fields, offset = {}, 1
    for position in range(32, header - 1, 32):
        if data[position] == 13:
            break
        field = data[position:position + 11].split(b"\x00")[0].decode("ascii")
        width = data[position + 16]
        fields[field] = offset, width
        offset += width

    def get(index, field):
        start, width = fields[field]
        start += header + index * record_length
        return data[start:start + width].decode("latin1").strip()

    for i in range(count):
        if data[header + i * record_length] == 42:
            continue
        key_parts = [get(i, field) for field in ("CADU", "FANO", "NDCL")]
        declaration = sha("|".join(key_parts).encode())
        latest_declaration[declaration] = max(
            latest_declaration.get(declaration, ""), end)
        reference = (name, i + 1)
        if reference not in references:
            continue
        index = references[reference]
        row_declaration[index] = declaration
        series = get(i, "NSER")
        assert sha("|".join(key_parts + [series]).encode()) == rows[index][
            "id_declaracion_serie_sha256"]
        if not all(part.isdigit() and int(part) > 0 for part in key_parts + [series]):
            row_key_invalid.add(index)
        # Check every retained source value independently of the CSV parser.
        for raw_field, csv_field in (
            ("PART_NANDI", "subpartida"), ("CPAIDES", "destino"),
            ("FNUM", "fecha_numeracion_raw"), ("FEMB", "fecha_embarque_raw"),
            ("FECH_RECEP", "fecha_recepcion_raw"), ("FREG", "fecha_regularizacion_raw"),
            ("VFOBSERDOL", "valor_fob_usd"), ("VPESNET", "peso_neto_kg"),
        ):
            value = get(i, raw_field)
            if raw_field == "PART_NANDI":
                value = value.split(".")[0].zfill(10)
            assert value == rows[index][csv_field], (name, i + 1, csv_field)
    source_checks.append({"archivo": name, "periodo_paquete_fin": end,
                          "zip_sha256": sha(zipped), "dbf_sha256": sha(data),
                          "registros_dbf": count})

assert len(row_declaration) == len(rows)
analytic = [c for c in columns if c not in (
    "archivo_fuente", "fila_fuente", "valor_unitario_fob_usd_kg", "estado_calidad")]
fingerprints = [sha(json.dumps([row[c] for c in analytic],
                             ensure_ascii=False, separators=(",", ":")).encode())
                for row in rows]
current = defaultdict(list)
for i, row in enumerate(rows):
    if packet_end(row["archivo_fuente"]) == latest_declaration[row_declaration[i]]:
        current[row["id_declaracion_serie_sha256"]].append(i)

conflict_series = {key for key, indexes in current.items()
                   if len({fingerprints[i] for i in indexes}) > 1}
blocked = {row_declaration[i] for key in conflict_series for i in current[key]}
invalid_date = set()
for indexes in current.values():
    for i in indexes:
        try:
            date = dt.datetime.strptime(rows[i]["fecha_embarque_raw"], "%Y%m%d").date()
            assert date.isoformat() <= packet_end(rows[i]["archivo_fuente"])
        except (ValueError, AssertionError):
            invalid_date.add(i)
blocked_quality = {row_declaration[i] for indexes in current.values() for i in indexes
                   if i in row_key_invalid or i in invalid_date
                   or rows[i]["estado_calidad"] != "valido"}

accepted, quarantined, ledger = [], [], []
representative = {}
for indexes in current.values():
    for i in sorted(indexes, key=lambda j: (rows[j]["archivo_fuente"],
                                          int(rows[j]["fila_fuente"]))):
        representative.setdefault((row_declaration[i], fingerprints[i]), i)

for i, row in enumerate(rows):
    declaration = row_declaration[i]
    key = row["id_declaracion_serie_sha256"]
    if packet_end(row["archivo_fuente"]) != latest_declaration[declaration]:
        action = "sustituida_por_paquete_posterior_declaracion"
    elif declaration in blocked:
        action = "cuarentena_declaracion_con_versiones_simultaneas"
    elif declaration in blocked_quality:
        action = "cuarentena_declaracion_por_calidad"
    elif representative[declaration, fingerprints[i]] != i:
        action = "duplicado_analitico_del_snapshot_vigente"
    else:
        action = "incluida_vista_conciliada"
    decision = {"archivo_fuente": row["archivo_fuente"], "fila_fuente": row["fila_fuente"],
                "id_declaracion_sha256": declaration, "id_declaracion_serie_sha256": key,
                "huella_campos_analiticos": fingerprints[i],
                "periodo_paquete_fin": packet_end(row["archivo_fuente"]),
                "ultimo_periodo_declaracion": latest_declaration[declaration],
                "decision": action}
    ledger.append(decision)
    extra = {**row, "id_declaracion_sha256": declaration,
             "periodo_paquete_fin": decision["periodo_paquete_fin"],
             "huella_campos_analiticos": fingerprints[i], "decision": action}
    if action == "incluida_vista_conciliada":
        accepted.append(extra)
    elif action.startswith("cuarentena"):
        quarantined.append(extra)

extra_columns = columns + ["id_declaracion_sha256", "periodo_paquete_fin",
                           "huella_campos_analiticos", "decision"]
write_csv("vista-conciliada.csv", extra_columns, accepted)
write_csv("cuarentena.csv", extra_columns, quarantined)
write_csv("decisiones.csv", list(ledger[0]), ledger)
assert len(ledger) == len(rows)
assert len({r["id_declaracion_serie_sha256"] for r in accepted}) == len(accepted)
assert not {r["id_declaracion_sha256"] for r in accepted} & (blocked | blocked_quality)
assert all(r["periodo_paquete_fin"] == latest_declaration[r["id_declaracion_sha256"]]
           for r in accepted)
assert (BASE / "observaciones-sunat.csv").read_bytes() == input_bytes
input_versions = defaultdict(set)
for i, row in enumerate(rows):
    input_versions[row["id_declaracion_serie_sha256"]].add(fingerprints[i])
initial_multi = {key for key, values in input_versions.items() if len(values) > 1}
accepted_keys = {r["id_declaracion_serie_sha256"] for r in accepted}
quarantine_keys = {r["id_declaracion_serie_sha256"] for r in quarantined}
conflict_details = []
changing_counts = Counter()
for key in sorted(conflict_series):
    indexes = current[key]
    changing = [c for c in analytic if len({rows[i][c] for i in indexes}) > 1]
    changing_counts.update(changing)
    conflict_details.append({
        "id_declaracion_serie_sha256": key,
        "id_declaracion_sha256": row_declaration[indexes[0]],
        "campos_en_conflicto": changing,
        "valores": {c: sorted({rows[i][c] for i in indexes}) for c in changing},
        "fuentes": sorted({rows[i]["archivo_fuente"] for i in indexes}),
    })
details = {
    "claves_multiversion_iniciales": len(initial_multi),
    "multiversion_resueltas_en_vista": len(initial_multi & accepted_keys),
    "multiversion_en_cuarentena": len(initial_multi & quarantine_keys),
    "cuarentena_series_colaterales_sin_conflicto_propio": len(quarantine_keys - conflict_series),
    "campos_cambiantes_cuarentena": dict(changing_counts), "casos": conflict_details,
}
(OUT / "conflictos-detalle.json").write_text(
    json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8")
old_keys = {r["id_declaracion_serie_sha256"] for r in rows}
latest_keys = set(current)
removed_keys = old_keys - latest_keys
write_csv("series_ausentes_snapshot_posterior.csv", ["id_declaracion_serie_sha256"],
          ({"id_declaracion_serie_sha256": k} for k in sorted(removed_keys)))
outcomes = Counter(r["decision"] for r in ledger)
assert sum(outcomes.values()) == len(rows)
summary = {
    "version_reglas": "sunat-conciliacion-1.1", "fecha_corte_coleccion": manifest.get('fecha_recopilacion'),
    "ejecutado_en_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "estado": "vista_conciliada_de_paquetes_disponibles_no_dataset_experimental",
    "entrada_sha256": sha(input_bytes), "script_sha256": sha(Path(__file__).read_bytes()),
    "filas_entrada": len(rows), "claves_serie_entrada": len(old_keys),
    "decisiones": dict(outcomes), "filas_conciliadas": len(accepted),
    "filas_cuarentena": len(quarantined),
    "series_cuarentena": len({r["id_declaracion_serie_sha256"] for r in quarantined}),
    "declaraciones_cuarentena_conflicto": len(blocked),
    "declaraciones_cuarentena_calidad": len(blocked_quality),
    "series_conflicto_ultimo_paquete": len(conflict_series),
    "series_ausentes_snapshot_posterior": len(removed_keys),
    "por_producto": dict(Counter(r["producto"] for r in accepted)),
    "comprobaciones": {"originales_sha256": True, "campos_contra_dbf": True,
                        "una_decision_por_entrada": True, "clave_serie_unica": True,
                        "sin_declaraciones_bloqueadas": True,
                        "observaciones_sin_modificar": True},
    "fuentes": source_checks,
}
(OUT / "resumen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in summary.items() if k != "fuentes"}, ensure_ascii=False))
