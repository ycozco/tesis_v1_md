"""Independent accounting and source-reference checks for persisted outputs."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
base = root / (sys.argv[2] if len(sys.argv) > 2 else "datasets/fuentes/2026-10-31")
out = base / "conciliacion"


def load(file):
    with file.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def reference(row):
    return row["archivo_fuente"], row["fila_fuente"]


summary = json.loads((out / "resumen.json").read_text(encoding="utf-8"))
source_bytes = (base / "observaciones-sunat.csv").read_bytes()
assert hashlib.sha256(source_bytes).hexdigest() == summary["entrada_sha256"]
source = load(base / "observaciones-sunat.csv")
indexed = {reference(row): row for row in source}
assert len(indexed) == len(source)
decisions = load(out / "decisiones.csv")
assert Counter(map(reference, decisions)) == Counter(map(reference, source))
assert dict(Counter(row["decision"] for row in decisions)) == summary["decisiones"]
ledger = {reference(row): row for row in decisions}
accepted = load(out / "vista-conciliada.csv")
quarantine = load(out / "cuarentena.csv")
blocked = {row["id_declaracion_sha256"] for row in quarantine}
assert len(accepted) == summary["filas_conciliadas"]
assert len(quarantine) == summary["filas_cuarentena"]
assert len({r["id_declaracion_serie_sha256"] for r in accepted}) == len(accepted)
assert {reference(r) for r in accepted} == {
    reference(r) for r in decisions if r["decision"] == "incluida_vista_conciliada"}
assert {reference(r) for r in quarantine} == {
    reference(r) for r in decisions if r["decision"].startswith("cuarentena")}
for row in accepted + quarantine:
    original = indexed[reference(row)]
    assert all(row[field] == value for field, value in original.items())
    item = ledger[reference(row)]
    assert row["decision"] == item["decision"]
    assert row["periodo_paquete_fin"] == item["ultimo_periodo_declaracion"]
    expected = float(row["valor_fob_usd"]) / float(row["peso_neto_kg"])
    assert abs(float(row["valor_unitario_fob_usd_kg"]) - expected) <= 1e-9 * max(1, expected)
    if row["decision"] == "incluida_vista_conciliada":
        assert row["id_declaracion_sha256"] not in blocked
assert dict(Counter(r["producto"] for r in accepted)) == summary["por_producto"]
assert summary["filas_entrada"] == sum(summary["decisiones"].values())
print(json.dumps({"estado": "OK", "entradas_con_decision": len(decisions),
                  "filas_conciliadas": len(accepted), "filas_cuarentena": len(quarantine),
                  "comprobacion": "contabilidad_y_correspondencia_con_fuente"}))
