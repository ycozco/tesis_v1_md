# GUÍA DE USO Y EJECUCIÓN
## Sistema Integrado de Supervisión Operativa con IA Explicable
## Tesis UNSA — Yoset Cozco Mauri · Versión 1.0 — 2026-05-17

> Esta guía documenta cómo trabajar en el proyecto: cómo levantar el visor de tesis, cómo regenerar el dataset, cómo ejecutar la purga de referencias, cómo auditar la integridad bibliográfica y cómo entregar nuevos cambios. Está pensada para que cualquier persona (asesor, jurado, colaborador o el propio autor en una nueva máquina) pueda reproducir el entorno en menos de 30 minutos.

---

## 1. Estructura del repositorio

```
tesis_yoset/
├── config/
│   ├── apa.csl                   estilo de citación APA para Pandoc
│   ├── entrypoint.sh             entrada del contenedor Docker
│   ├── refs.bib                  base de referencias (47 entradas, v2.0)
│   └── requirements-docker.txt   dependencias del visor Flask
├── data/                         dataset(s) sintético(s) generado(s)
├── docs/                         19 secciones de la tesis + planes + anexos
│   ├── 00-portada.md … 90-referencias.md
│   ├── A1-anexo-usabilidad.md … A4-anexo-ia.md
│   ├── plan_detallado.md
│   ├── plan-revision-academica-exhaustiva.md
│   ├── plan-siguientes-pasos.md
│   ├── variables-operacionalizadas.md
│   ├── busqueda-sistematica-gap.md
│   └── guia-uso.md               (este archivo)
├── scripts/                      utilidades para purga y auditoría
│   ├── purga_referencias.py
│   ├── limpia_duplicados.py
│   └── auditar_referencias.py
├── src/
│   ├── app.py                    visor Flask con hot-reload
│   ├── convert_md_to_html.py     generación HTML estática
│   ├── serve_thesis.py           servidor alternativo
│   └── generate_synthetic_dataset.py
├── output/                       HTML generado (opcional)
├── requirements.txt              dependencias Python del pipeline ML
├── docker-compose.yml            servicio del visor en localhost:8000
└── Dockerfile
```

---

## 2. Levantar el visor de tesis (lectura interactiva)

### 2.1 Con Docker (recomendado)

```powershell
docker compose up --build
```

Abrir en el navegador:
- http://localhost:8000              → portada
- http://localhost:8000/secciones    → panel de navegación con estado por sección
- http://localhost:8000/seccion/10-capitulo1   → vista de la sección con sidebar TOC

**Hot-reload**: cualquier edición de `docs/XX-*.md` recarga la página automáticamente gracias a `FLASK_DEBUG=1` + `extra_files`.

### 2.2 Sin Docker (entorno local)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r config/requirements-docker.txt
$env:FLASK_DEBUG = "1"
py src/app.py
```

---

## 3. Entorno Python completo (para experimentos ML)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Versión de Python recomendada: **3.11.x**. (3.12 funciona; 3.14 puede requerir ajustes en xgboost/shap.)

---

## 4. Generar el dataset sintético v1.0

```powershell
py src/generate_synthetic_dataset.py --n 2000 --seed 42 --out data/dataset_agro_sintetico_v1.csv
```

**Parámetros opcionales**:
| Flag | Default | Significado |
|---|---|---|
| `--n` | 2000 | número de filas |
| `--seed` | 42 | semilla determinista |
| `--anomaly-rate` | 0.12 | porcentaje de anomalías inyectadas |
| `--missing-rate` | 0.03 | porcentaje de valores faltantes |
| `--out` | `data/dataset_agro_sintetico_v1.csv` | ruta de salida |

**Reproducibilidad**: con la misma semilla y la misma versión del script, el CSV es bit-exact idéntico entre máquinas.

---

## 5. Mantenimiento de referencias bibliográficas

El proyecto evita el formato `[@clave]` en los documentos (que no compila con el visor Flask). En su lugar usa citas APA legibles tipo `(Autor, AAAA)`.

### 5.1 Reemplazo masivo `[@clave]` → `(Autor, AAAA)`

```powershell
py scripts/purga_referencias.py
```

El script:
- Procesa todos los `.md` activos (excluye `tesis.md` y `tesis_v2.md`).
- Maneja citas individuales `[@clave]` y múltiples `(@k1; @k2)`.
- Reporta claves no mapeadas.

### 5.2 Limpieza de duplicaciones tras cita narrativa

Si el texto dice `Lundberg & Lee (2017)`, el reemplazo produce `Lundberg & Lee (2017)` (duplicado). Para corregir:

```powershell
py scripts/limpia_duplicados.py
```

### 5.3 Auditoría de integridad refs.bib ↔ docs

```powershell
py scripts/auditar_referencias.py
```

Salida:
- **Citas APA SIN entrada en refs.bib**: errores de tipeo o referencias faltantes.
- **Entradas en refs.bib NO citadas en docs activos**: huérfanas legítimas (mantener si referencia narrativa) o eliminables.

### 5.4 Agregar una nueva referencia

1. Editar `config/refs.bib` añadiendo la entrada en la categoría correspondiente (A–K).
2. Si va a sustituir un `[@clave]` existente, actualizar `MAPEO_APA` en `scripts/purga_referencias.py` y `MAPEO_INVERSO` en `scripts/auditar_referencias.py`.
3. Citar en el texto en formato APA: `(Apellido, Año)` o narrativo `Apellido (Año) [...]`.

---

## 6. Convenciones de redacción

| Caso | Forma correcta | Ejemplo |
|---|---|---|
| Cita parentética simple | `(Apellido, Año)` | `(Chen & Guestrin, 2016)` |
| Cita parentética múltiple | `(A, Año; B, Año)` | `(Ji et al., 2023; Maynez et al., 2026)` |
| Cita narrativa | `Apellido (Año) ...` | `Lundberg y Lee (2017) introducen SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)...` |
| Tres o más autores | `Apellido et al.` | `(Lim et al., 2021)` |
| Norma o resolución | `(Institución, Año)` | `(SBS, 2023)`, `(PCM, 2025)` |
| Referencia a sección interna | `§N.N` | `según §3.3.2` |
| Referencia a tabla | `Tabla N.N` | `(Tabla 4.1)` |
| Referencia a figura | `Figura N.N` | `(Figura 3.1)` |

**Anti-patrones que evitar**:
- ❌ `[@clave]` (no compila en el visor Flask)
- ❌ Citar nombre de archivo (`según docs/30-capitulo3.md`) — usar `según §3.3`
- ❌ Usar `@autor` suelto en el texto
- ❌ Hipervínculos a archivos relativos en el cuerpo principal (sí en planes y guías)

---

## 7. Flujo de trabajo Git

### 7.1 Antes de empezar a editar

```powershell
git status
git pull --rebase
```

### 7.2 Al cerrar una sesión de trabajo

```powershell
# revisar cambios
git status
git diff

# auditar referencias antes de commitear
py scripts/auditar_referencias.py

# si todo está limpio, agregar y commitear con mensaje descriptivo
git add docs/ config/ src/ scripts/ requirements.txt
git commit -m "tipo: descripción breve

Detalle del cambio:
- Punto 1
- Punto 2"
```

### 7.3 Convención de mensajes

| Prefijo | Significado |
|---|---|
| `tesis:` | cambios al texto de la tesis |
| `refs:` | cambios en `config/refs.bib` |
| `script:` | nuevos scripts en `scripts/` o `src/` |
| `plan:` | actualización de planes/checklists |
| `anexo:` | cambios en anexos A/B/C/D |
| `fix:` | corrección de errata |
| `doc:` | documentación general (guías, README) |

---

## 8. Estructura de un nuevo experimento E_x

```
src/
├── experiments/
│   └── exp_X_<nombre>.py
└── evaluate.py
```

Cada experimento debe:
1. Fijar `np.random.seed(42)`.
2. Cargar `data/dataset_agro_sintetico_v1.csv` con división temporal.
3. Aplicar `optuna` para tuning si hay hiperparámetros.
4. Reportar métricas como `mean ± std` sobre semillas 42–47.
5. Exportar CSV con resultados en `output/experiments/exp_X_results.csv`.
6. Generar tabla Markdown insertable en `docs/40-capitulo4.md`.

---

## 9. Soluciones a problemas comunes

| Problema | Causa probable | Solución |
|---|---|---|
| `py: command not found` | `py.exe` no en PATH | Usar `python` o instalar Python desde python.org |
| `ModuleNotFoundError: numpy` | venv no activado o no instalado | `.\.venv\Scripts\activate; pip install -r requirements.txt` |
| Dataset no se regenera idéntico | Semilla distinta o versión de `numpy` distinta | Fijar `--seed 42` y respetar versiones de `requirements.txt` |
| `[@clave]` aparece literal en el HTML | Olvidó ejecutar `purga_referencias.py` | `py scripts/purga_referencias.py` |
| Citas duplicadas en el texto | Cita narrativa + parentética combinadas | `py scripts/limpia_duplicados.py` |
| Docker falla al recargar | `FLASK_DEBUG` no está en `1` | Revisar `docker-compose.yml` env vars |
| Caracteres no ASCII en refs.bib | Algunos lectores no soportan UTF-8 directo | Mantener solo ASCII en claves; tildes solo en campos `title`/`author` |

---

## 10. Contactos y reconocimientos

- **Autor**: Yoset Cozco Mauri — yodetcozco@gmail.com
- **Asesor**: Dr. Víctor Manuel Cornejo Aparicio (UNSA)
- **Institución**: Escuela Profesional de Ingeniería de Sistemas, Universidad Nacional de San Agustín de Arequipa
- **Repositorio**: privado hasta defensa; público bajo MIT post-defensa
- **Datasets generados**: licencia **CC BY 4.0**

---

*Guía generada 2026-05-17. Actualizar conforme se incorporen nuevos módulos o flujos.*
