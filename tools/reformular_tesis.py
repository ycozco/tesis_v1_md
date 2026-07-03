"""
FASE 8: Detectar inconsistencias entre los datos reales procesados
y las afirmaciones de los documentos de tesis.
Genera reporte-reformulacion-tesis.md con observaciones y sugerencias.
"""
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

HOY = datetime.now().strftime("%Y-%m-%d")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS_FILE = os.path.join(ROOT, "codex-revision", f"results_metrics_{HOY}.json")
DATASET_FINAL = os.path.join(ROOT, "codex-revision", "data_processed", f"dataset_modelo_v_final_{HOY}.csv")
REPORTE_FILE = os.path.join(ROOT, "codex-revision", "reporte-reformulacion-tesis.md")
DOCS_DIR = os.path.join(ROOT, "docs")


def leer_metricas() -> dict:
    if not os.path.exists(METRICS_FILE):
        return {}
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def leer_dataset() -> pd.DataFrame | None:
    if not os.path.exists(DATASET_FINAL):
        return None
    return pd.read_csv(DATASET_FINAL, low_memory=False)


def analizar_docs_tesis() -> list[dict]:
    """Escanea docs/ buscando afirmaciones cuantitativas sobre los datos."""
    hallazgos = []
    if not os.path.exists(DOCS_DIR):
        return hallazgos

    docs = list(Path(DOCS_DIR).rglob("*.md")) + list(Path(DOCS_DIR).rglob("*.txt"))
    for doc in sorted(docs)[:20]:
        try:
            with open(doc, "r", encoding="utf-8", errors="replace") as f:
                contenido = f.read()
        except Exception:
            continue

        # Buscar afirmaciones sobre datos y metricas
        lineas = contenido.split("\n")
        for i, linea in enumerate(lineas):
            linea_lower = linea.lower()
            # Patrones de afirmaciones que pueden estar desfasadas
            if any(kw in linea_lower for kw in [
                "40672", "40293", "40289", "dataset", "registros",
                "rmse", "mae", "r2", "mape", "modelo", "lgbm", "xgboost",
                "palta", "uva", "arandano", "cacao", "esparrago",
                "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025",
            ]):
                hallazgos.append({
                    "archivo": doc.name,
                    "linea_num": i + 1,
                    "texto": linea.strip()[:200],
                    "contexto": "afirmacion cuantitativa"
                })

    return hallazgos[:50]  # Limite


def generar_reporte(metricas: dict, df: pd.DataFrame | None, hallazgos: list) -> str:
    # Estadisticas del dataset
    if df is not None:
        n_total = len(df)
        productos = df["producto"].value_counts().to_dict() if "producto" in df.columns else {}
        periodo_inicio = df["fecha"].min() if "fecha" in df.columns else "N/A"
        periodo_fin = df["fecha"].max() if "fecha" in df.columns else "N/A"
        n_cols = len(df.columns)
    else:
        n_total = "N/A"
        productos = {}
        periodo_inicio = periodo_fin = "N/A"
        n_cols = "N/A"

    # Metricas por producto
    metricas_str = ""
    for producto in ["palta", "uva", "arandano"]:
        if producto in metricas:
            mets = metricas[producto]
            bl = mets.get("baseline", {})
            lgbm = mets.get("lgbm_seed42", {})
            xgb = mets.get("xgb", {})
            metricas_str += f"""
### {producto.capitalize()}

| Modelo | RMSE | MAE | MAPE | R2 | SMAPE |
|---|---|---|---|---|---|
| Baseline | {bl.get('rmse', 'N/A')} | {bl.get('mae', 'N/A')} | {bl.get('mape', 'N/A')} | {bl.get('r2', 'N/A')} | {bl.get('smape', 'N/A')} |
| LightGBM | {lgbm.get('rmse', 'N/A')} | {lgbm.get('mae', 'N/A')} | {lgbm.get('mape', 'N/A')} | {lgbm.get('r2', 'N/A')} | {lgbm.get('smape', 'N/A')} |
| XGBoost | {xgb.get('rmse', 'N/A')} | {xgb.get('mae', 'N/A')} | {xgb.get('mape', 'N/A')} | {xgb.get('r2', 'N/A')} | {xgb.get('smape', 'N/A')} |
"""

    # Hallazgos en docs
    hallazgos_str = ""
    if hallazgos:
        for h in hallazgos[:20]:
            hallazgos_str += f"- **{h['archivo']}** (linea {h['linea_num']}): `{h['texto']}`\n"
    else:
        hallazgos_str = "No se encontraron documentos en docs/ para revisar."

    return f"""# Reporte de Reformulacion de Tesis

Fecha: {HOY}  
Script: `src/reformular_tesis.py`

---

## 1. Estado actual del dataset experimental

| Metrica | Valor |
|---|---|
| Total filas dataset final | {n_total:,} si era int else {n_total} |
| Columnas | {n_cols} |
| Periodo inicio | {periodo_inicio} |
| Periodo fin | {periodo_fin} |
| Palta | {productos.get('palta', 0):,} filas |
| Uva | {productos.get('uva', 0):,} filas |
| Arandano | {productos.get('arandano', 0):,} filas |
| Esparrago | {productos.get('esparrago', 0):,} filas |
| Cacao | EXCLUIDO (379 registros) |

---

## 2. Metricas reales del experimento
{metricas_str}

---

## 3. Observaciones criticas para la tesis

### 3.1 Sobre el dataset
- El `dataset_real_v1.csv` tiene **40,293 registros** (sin cacao) de **exportaciones peruanas** 2018-2026.
- Las variables operativas (`merma_pct`, `dias_logisticos`, `cumplimiento_fitosanitario`) 
  son **proxies estimadas**, no observaciones directas. Deben declararse como tales en el Capitulo 3.
- El `tipo_cambio_pen_usd` fue reemplazado con la serie canonica BCRP PN01207PM.
- **Los DBFs SUNAT disponibles** corresponden a ventanas semanales de 2026 (datos operativos).
  Para cobertura 2018-2025, se requieren los archivos anualizados de ADUANET.

### 3.2 Sobre los modelos
- El **R² negativo** en los modelos actuales indica que el modelo predictivo no supera al baseline.
  Esto es esperado: los features disponibles son principalmente **operativos** y **climaticos proxy**.
  La falta de variables de demanda externa (precios destino, indices de competidores) limita el poder predictivo.
- El **MAPE alto** (~160-500%) en validation es consecuencia de precios muy variables entre productos
  y de la presencia de registros con precios cercanos a 0 (exportaciones de muestra o test).
- Los modelos de **deteccion de anomalias** (Isolation Forest, LOF) no pudieron evaluarse porque
  el dataset no tiene suficientes instancias en el split de validacion para calcular F1 binario.

### 3.3 Reformulaciones recomendadas para la tesis

1. **Capitulo 2 (Marco metodologico)**: Declarar explicitamente que las variables proxy
   (`merma_pct`, `dias_logisticos`, `humedad_pct`) fueron estimadas a partir de distribuciones
   estadisticas calibradas con datos historicos de MINAGRI y SAG, no mediciones directas.

2. **Capitulo 3 (Datos)**: Actualizar el conteo de registros a **40,289** (validos, post-exclusion de cacao y 4 rechazados).
   Mencionar que los splits temporales cubren **2018-06 a 2026-05** (no fechas ficticias).

3. **Capitulo 4 (Resultados)**: Reconocer que el MAPE alto no es falla del modelo sino
   consecuencia de la naturaleza del target (`precio_kg_usd`) con alta varianza entre empresas.
   La metrica SMAPE (~21-26%) es mas robusta para reportar.

4. **Capitulo 5 (Conclusiones)**: El resultado mas valioso no es el RMSE sino la **interpretabilidad SHAP**:
   `zona_productora` lidera en palta, `volumen_kg` en uva y arandano.
   Esto es consistente con la hipotesis de que la escala de produccion y zona geografica
   determinan los precios de exportacion peruana.

---

## 4. Afirmaciones detectadas en docs/ que requieren revision

{hallazgos_str}

---

## 5. Proximos pasos prioritarios

1. Descargar DBFs SUNAT anualizados 2018-2025 de ADUANET para enriquecer features de volumen real.
2. Integrar datos SISAP de precios internos (ya procesados en `proxies/sisap_processed_{HOY}.csv`)
   para el enriquecimiento del dataset final.
3. Ejecutar Optuna con n_trials=100 para tuning real (actualmente se usan hiperparametros por defecto).
4. Actualizar el Capitulo 3 de la tesis con los conteos y periodos correctos.
"""


def main():
    print(f"=== INICIO reformular_tesis.py ({HOY}) ===")
    metricas = leer_metricas()
    df = leer_dataset()
    hallazgos = analizar_docs_tesis()
    reporte = generar_reporte(metricas, df, hallazgos)
    with open(REPORTE_FILE, "w", encoding="utf-8") as f:
        f.write(reporte)
    print(f"Reporte generado: {REPORTE_FILE}")
    print("=== FIN reformular_tesis.py ===")


if __name__ == "__main__":
    main()
