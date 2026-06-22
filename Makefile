# =============================================================================
# Makefile — Sistema Integrado de Supervisión Operativa Agroexportadora
# Tesis UNSA — Yoset Cozco Mauri (2026)
# =============================================================================

.PHONY: install test lint ingest data train anomalies explain reports experiments thesis-artifacts api dashboard all

PYTHON = .\.venv\Scripts\python
PIP = .\.venv\Scripts\pip

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -c "import sys, glob; print('Chequeando sintaxis de archivos Python...'); [compile(open(f, encoding='utf-8').read(), f, 'exec') for f in glob.glob('src/**/*.py', recursive=True)]; print('Sintaxis OK.')"

ingest:
	$(PYTHON) src/prepare_weekly_dataset.py

data:
	$(PYTHON) src/prepare_weekly_dataset.py
	$(PYTHON) src/feature_engineering.py

train:
	$(PYTHON) src/module1_prediction.py

anomalies:
	$(PYTHON) src/module2_anomaly.py

explain:
	$(PYTHON) src/module3_shap.py

reports:
	$(PYTHON) src/module4_rag.py

experiments:
	$(PYTHON) src/run_all.py

thesis-artifacts:
	$(PYTHON) scripts/compile_tesis.py

api:
	$(PYTHON) build_github_pages.py

dashboard:
	$(PYTHON) src/app.py

all: data train anomalies explain reports experiments thesis-artifacts api
