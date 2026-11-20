FROM python:3.11-slim@sha256:a3ab0b966bc4e91546a033e22093cb840908979487a9fc0e6e38295747e49ac0
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1 HF_HUB_OFFLINE=1
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir 'torch==2.13.0+cpu' --index-url https://download.pytorch.org/whl/cpu
COPY requirements-observed.lock /opt/training-requirements.lock
RUN pip install --no-cache-dir -r /opt/training-requirements.lock && pip check
WORKDIR /worker
COPY . /worker
RUN useradd --uid 10002 --create-home trainer && mkdir /state && chown trainer:trainer /state
ARG AGRO_SOURCE_REVISION
LABEL org.opencontainers.image.revision=${AGRO_SOURCE_REVISION}
ENV AGRO_SOURCE_REVISION=${AGRO_SOURCE_REVISION}
USER trainer
EXPOSE 8010
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8010", "--workers", "1"]
