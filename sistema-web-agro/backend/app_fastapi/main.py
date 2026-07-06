from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_tables
from app_fastapi.api.v1.router import api_router
from app_fastapi.core.config import settings

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_tables()
    yield

app = FastAPI(
    title="Sistema de Supervisión Agroexportadora",
    version="0.2.0-migration",
    description=(
        "Punto de entrada ASGI para la migración gradual del backend Flask. "
        "Las rutas se trasladarán por módulos y se validarán antes de retirar la aplicación heredada."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["operación"])
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "framework": "FastAPI",
        "server": "Uvicorn",
        "migration": "in_progress",
    }

@app.get("/api/migration/status", tags=["operación"])
def migration_status() -> dict[str, object]:
    return {
        "legacy_backend": "Flask/Gunicorn",
        "target_backend": "FastAPI/Uvicorn",
        "database": "PostgreSQL/pgvector via SQLAlchemy",
        "completed_routes": [
            "GET /health",
            "GET /api/migration/status",
            "POST /api/auth/login",
            "POST /api/auth/logout",
            "GET /api/dashboard/stats"
        ],
        "pending_groups": [
            "alerts",
            "reports",
            "telemetry",
            "configuration",
        ],
    }
