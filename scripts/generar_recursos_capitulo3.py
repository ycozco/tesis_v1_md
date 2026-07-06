from __future__ import annotations

import shutil
import subprocess
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "docs" / "images" / "capitulo3"
MERMAID_DIR = IMAGES_DIR / "mermaid"
GRAFICOS_DIR = IMAGES_DIR / "graficos"
CAPTURAS_DIR = IMAGES_DIR / "capturas"


MERMAID_SOURCES = {
    "figura-3-01-flujo-auditoria.mmd": """
    flowchart TD
        A[Inventario de fuentes y artefactos] --> B[Revision de estructura y cobertura]
        B --> C[Validacion de calidad\nnulos duplicados fechas codigos]
        C --> D[Clasificacion de datos\nreales proxies semilla]
        D --> E[Calculo de hashes y trazabilidad]
        E --> F[Revision de scripts ETL y modelos]
        F --> G[Verificacion de backend frontend y persistencia]
        G --> H[Registro de hallazgos]
        H --> I[Acciones correctivas y decisiones metodologicas]
    """,
    "figura-3-03-casos-uso.mmd": """
    flowchart LR
        admin[(Administrador)]
        auditor[(Auditor)]

        subgraph sistema[Prototipo funcional]
            u1[Gestionar usuarios y roles]
            u2[Configurar pesos y umbral]
            u3[Administrar documentos RAG]
            u4[Consultar dashboard y alertas]
            u5[Revisar detalle analitico]
            u6[Registrar decision y justificacion]
            u7[Consultar telemetria e integridad]
        end

        admin --> u1
        admin --> u2
        admin --> u3
        admin --> u7
        auditor --> u4
        auditor --> u5
        auditor --> u6
        auditor --> u7
    """,
    "figura-3-04-arquitectura-logica.mmd": """
    flowchart TB
        subgraph fuentes[Fuentes externas]
            sunat[SUNAT o ADUANET]
            bcrp[BCRP]
            sisap[SISAP MIDAGRI]
            nasa[NASA POWER]
            normas[SENASA FDA normas]
        end

        subgraph datos[Capa de datos]
            raw[raw]
            bronze[bronze]
            silver[silver]
            gold[gold]
            pred[prediction features]
            anom[anomaly features]
        end

        subgraph analitica[Capa analitica]
            modelos[XGBoost y LightGBM]
            detectores[Isolation Forest LOF ECOD]
            shap[Explicaciones SHAP]
        end

        subgraph conocimiento[Capa de conocimiento]
            rag[RAG y validador factual]
        end

        subgraph servicios[Servicios backend]
            api[Autenticacion alertas reportes telemetria integridad]
        end

        ui[Frontend React]
        db[(PostgreSQL y pgvector)]
        artefactos[(Parquet modelos y reportes)]

        fuentes --> raw --> bronze --> silver --> gold
        gold --> pred --> modelos
        gold --> anom --> detectores
        modelos --> shap
        modelos --> api
        detectores --> api
        shap --> api
        rag --> api
        api --> ui
        api --> db
        gold --> artefactos
        modelos --> artefactos
        detectores --> artefactos
        normas --> rag
    """,
    "figura-3-05-arquitectura-despliegue.mmd": """
    flowchart LR
        browser[Navegador del usuario] --> nginx[Nginx]
        nginx --> react[Frontend React Vite]
        nginx --> backend[Backend Python\nFlask y FastAPI]
        backend --> postgres[(PostgreSQL)]
        backend --> pgvector[(pgvector)]
        backend --> models[(Modelos serializados)]
        backend --> reports[(Reportes y artefactos)]
        pipeline[Pipeline por lotes] --> postgres
        pipeline --> pgvector
        pipeline --> models
        pipeline --> reports
        pipeline --> data[(Datasets raw bronze silver gold)]
        backend --> data
    """,
    "figura-3-06-arquitectura-datos.mmd": """
    flowchart TB
        raw[raw\narchivos originales] --> bronze[bronze\nconversion estructural]
        bronze --> silver[silver\nlimpieza homologacion anonimización]
        silver --> gold[gold\nproducto mercado semana]
        gold --> feat1[prediction features]
        gold --> feat2[anomaly features]
        feat1 --> pred[Predicciones FOB y volumen]
        pred --> residuos[Residuos]
        feat2 --> detect[Scores IF LOF ECOD]
        residuos --> detect
        detect --> alertas[Alertas y severidad]
        pred --> shap[Explicaciones SHAP]
        alertas --> rag[Reporte RAG]
        shap --> vista[Vista de detalle]
        rag --> vista
    """,
    "figura-3-07-componentes-web.mmd": """
    flowchart LR
        subgraph frontend[Frontend React]
            login[Login]
            dash[Dashboard]
            inbox[Bandeja de alertas]
            detail[Detalle de alerta]
            telemetry[Telemetria e integridad]
            admin[Datos configuracion usuarios]
        end

        subgraph backend[Servicios backend]
            auth[Auth y sesiones]
            alerts[Alertas]
            explain[Prediccion anomalias SHAP RAG]
            monitor[Telemetria e integridad]
            config[Configuracion y usuarios]
        end

        db[(PostgreSQL)]
        vectors[(pgvector)]
        files[(Modelos y artefactos)]

        login --> auth
        dash --> alerts
        inbox --> alerts
        detail --> explain
        telemetry --> monitor
        admin --> config
        auth --> db
        alerts --> db
        explain --> db
        explain --> vectors
        explain --> files
        monitor --> db
        config --> db
    """,
    "figura-3-08-modelo-datos.mmd": """
    erDiagram
        USUARIO ||--o{ DECISION_AUDITORIA : registra
        PIPELINE_RUN ||--o{ OPERACION_ALERTA : produce
        CONFIGURACION_PIPELINE ||--o{ PIPELINE_RUN : parametriza
        OPERACION_ALERTA ||--|| EXPLICACION_SHAP : explica
        OPERACION_ALERTA ||--|| GENERATED_REPORT : resume
        OPERACION_ALERTA ||--o{ DECISION_AUDITORIA : recibe
        GENERATED_REPORT }o--o{ DOCUMENTO_NORMATIVO : cita
        PIPELINE_RUN ||--o{ ARTIFACT_LINEAGE : documenta
        OPERACION_ALERTA ||--o{ ARTIFACT_LINEAGE : enlaza
        USUARIO ||--o{ SECURITY_LOG : genera

        USUARIO {
            int id
            string username
            string rol
        }
        OPERACION_ALERTA {
            string alert_id
            string producto
            string mercado
            float score_ensemble
            string severidad
        }
        DECISION_AUDITORIA {
            int id
            string decision
            string condicion
            float tiempo_segundos
        }
        EXPLICACION_SHAP {
            int id
            string top_features
        }
        DOCUMENTO_NORMATIVO {
            int id
            string titulo
            string fuente
        }
        CONFIGURACION_PIPELINE {
            int id
            float peso_if
            float peso_lof
            float peso_ecod
            float umbral
        }
        PIPELINE_RUN {
            string run_id
            string dataset_hash
            string model_hash
        }
        GENERATED_REPORT {
            int id
            string estado_validacion
        }
        ARTIFACT_LINEAGE {
            int id
            string tipo
            string hash
        }
        SECURITY_LOG {
            int id
            string accion
            string created_at
        }
    """,
    "figura-3-09-entrenamiento-modelos.mmd": """
    flowchart LR
        gold[Dataset gold] --> prep[Ingenieria de caracteristicas]
        prep --> split[Split temporal train valid test]
        split --> base[Modelos base]
        split --> xgb[XGBoost]
        split --> lgbm[LightGBM]
        base --> compare[Comparacion de metricas]
        xgb --> compare
        lgbm --> compare
        compare --> select[Seleccion de modelo final]
        select --> serialize[Serializacion y versionado]
        serialize --> infer[Prediccion fuera de muestra]
        infer --> residuos[Calculo de residuos]
    """,
    "figura-3-10-ensemble-anomalias.mmd": """
    flowchart LR
        entradas[Residuos y variables contextuales] --> scale[Escalado y normalizacion]
        scale --> iforest[Isolation Forest]
        scale --> lof[Local Outlier Factor]
        scale --> ecod[ECOD]
        iforest --> norm[Homologacion de scores]
        lof --> norm
        ecod --> norm
        norm --> weights[Pesos IF 0.45 LOF 0.30 ECOD 0.25]
        weights --> score[Score ensemble]
        score --> threshold{Score >= umbral 0.65}
        threshold -->|Si| alerta[Generar alerta y severidad]
        threshold -->|No| normal[Operacion dentro de rango]
    """,
    "figura-3-11-flujo-shap.mmd": """
    flowchart LR
        modelo[Modelo predictivo final] --> alerta[Operacion o alerta seleccionada]
        alerta --> features[Vector de caracteristicas]
        features --> treeshap[TreeSHAP]
        treeshap --> contrib[Contribuciones positivas y negativas]
        contrib --> resumen[Resumen global y explicacion local]
        resumen --> ui[Vista de detalle del auditor]
        ui --> decision[Apoyo a la decision humana]
    """,
    "figura-3-12-flujo-rag.mmd": """
    sequenceDiagram
        participant A as Alerta
        participant B as Backend
        participant V as pgvector
        participant R as Recuperador RAG
        participant G as Generador
        participant F as Validador factual
        participant P as Persistencia

        A->>B: Solicitar reporte contextual
        B->>V: Buscar embeddings relevantes
        V-->>B: Fragmentos candidatos
        B->>R: Ranquear y filtrar evidencia
        R-->>B: Evidencia priorizada
        B->>G: Generar borrador con datos y evidencia
        G-->>B: Reporte preliminar
        B->>F: Verificar cifras y afirmaciones
        F-->>B: Aprobado o correccion
        B->>P: Guardar reporte validado
        P-->>B: Identificador y trazabilidad
    """,
    "figura-3-13-cadena-trazabilidad.mmd": """
    flowchart LR
        run[run_id] --> dataset[Dataset hash]
        run --> config[Configuracion versionada]
        run --> model[Modelo hash]
        dataset --> alert[alert_id]
        config --> alert
        model --> alert
        alert --> shap[Explicacion SHAP]
        alert --> evid[Evidencia RAG]
        alert --> report[Reporte generado]
        alert --> decision[Decision humana]
        shap --> lineage[ArtifactLineage]
        evid --> lineage
        report --> lineage
        decision --> lineage
    """,
    "figura-3-23-secuencia-revision-alerta.mmd": """
    sequenceDiagram
        actor U as Auditor
        participant F as Frontend
        participant API as Backend API
        participant DB as PostgreSQL
        participant M as Modelos y SHAP
        participant R as RAG

        U->>F: Inicia sesion y abre una alerta
        F->>API: Solicitar detalle(alert_id)
        API->>DB: Recuperar operacion y configuracion
        DB-->>API: Datos de alerta
        API->>M: Obtener prediccion scores SHAP
        M-->>API: Resultado analitico
        API->>R: Recuperar evidencia y reporte
        R-->>API: Fragmentos y reporte validado
        API-->>F: Respuesta consolidada
        U->>F: Registrar decision y justificacion
        F->>API: Guardar decision
        API->>DB: Persistir decision y telemetria
        DB-->>API: Confirmacion y trazabilidad
        API-->>F: Estado actualizado
    """,
}


CAPTURA_MAP = {
    "figura-3-14-inicio-sesion.png": ROOT / "sistema-web-agro" / "login_del_auditor_esp" / "screen.png",
    "figura-3-15-dashboard.png": ROOT / "sistema-web-agro" / "auditor_dashboard_final" / "screen.png",
    "figura-3-16-bandeja-alertas.png": ROOT / "sistema-web-agro" / "alerts_management_inbox" / "screen.png",
    "figura-3-17-detalle-alerta.png": ROOT / "sistema-web-agro" / "detalle_de_operaci_n_ia_explicable_esp" / "screen.png",
    "figura-3-18-historial-telemetria.png": ROOT / "sistema-web-agro" / "experimental_telemetry_console" / "screen.png",
    "figura-3-19-integridad-trazabilidad.png": ROOT / "sistema-web-agro" / "integrity_fairness_monitor" / "screen.png",
    "figura-3-20-biblioteca-rag.png": ROOT / "sistema-web-agro" / "explorador_de_datos_y_centro_de_carga" / "screen.png",
    "figura-3-21-configuracion-ensemble.png": ROOT / "sistema-web-agro" / "model_configuration_terminal" / "screen.png",
    "figura-3-22-usuarios-roles.png": ROOT / "sistema-web-agro" / "user_control_security_log" / "screen.png",
}


def ensure_dirs() -> None:
    for path in (MERMAID_DIR, GRAFICOS_DIR, CAPTURAS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def write_mermaid_sources() -> None:
    for filename, content in MERMAID_SOURCES.items():
        (MERMAID_DIR / filename).write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def render_mermaid() -> None:
    npx_cmd = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
    for source in sorted(MERMAID_DIR.glob("*.mmd")):
        svg_target = source.with_suffix(".svg")
        png_target = source.with_suffix(".png")
        for target in (svg_target, png_target):
            subprocess.run(
                [
                    npx_cmd,
                    "-y",
                    "@mermaid-js/mermaid-cli",
                    "-i",
                    str(source),
                    "-o",
                    str(target),
                    "-b",
                    "transparent",
                ],
                check=True,
                cwd=ROOT,
            )


def generate_chart() -> None:
    labels = [
        "Registros iniciales",
        "Exclusion cacao",
        "Registros evaluados",
        "Registros validos",
        "Registros rechazados",
    ]
    values = [40672, 379, 40293, 40289, 4]
    colors = ["#245c73", "#c96f31", "#4b8f8c", "#2f7d4a", "#b23a48"]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Figura 3.2. Evolucion de registros durante la preparacion inicial")
    ax.set_ylabel("Cantidad de registros")
    ax.set_ylim(0, 43000)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.text(
        0.99,
        0.95,
        "Nota: el esparrago se excluye del conjunto experimental principal.",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.3"},
    )
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 600, f"{value:,}".replace(",", " "), ha="center", va="bottom", fontsize=9)
    fig.autofmt_xdate(rotation=15, ha="right")
    fig.tight_layout()
    fig.savefig(GRAFICOS_DIR / "figura-3-02-evolucion-registros.png", dpi=200)
    fig.savefig(GRAFICOS_DIR / "figura-3-02-evolucion-registros.svg")
    plt.close(fig)


def copy_captures() -> None:
    for target_name, source in CAPTURA_MAP.items():
        shutil.copy2(source, CAPTURAS_DIR / target_name)


def main() -> None:
    ensure_dirs()
    write_mermaid_sources()
    render_mermaid()
    generate_chart()
    copy_captures()


if __name__ == "__main__":
    main()
