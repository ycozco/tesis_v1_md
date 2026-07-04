# INFORME DE ENTORNO Y LÍNEA BASE
## Sistema Integrado de Inteligencia Artificial Explicable
### Tesis UNSA — Yoset Cozco Mauri (2026)

Este documento registra los metadatos técnicos y el estado del entorno de desarrollo al iniciar la **Fase 1 (Congelar y auditar el estado actual)** de la rama `refactor/prototipo-tesis-v2`.

---

## 1. Detalles del Entorno Técnico

| Parámetro | Valor Registrado |
| :--- | :--- |
| **Sistema Operativo** | Microsoft Windows 11 Pro (OS Version: 10.0.26200 N/A Build 26200) |
| **Versión de Python** | Python 3.14.2 (Entorno Virtual .venv configurado) |
| **Versión de Node.js**| v26.1.0 |
| **Versión de Docker** | Docker version 29.5.3, build d1c06ef |
| **Fecha de Inicio** | 2026-07-04 (Fecha local) |
| **Rama Git Creada** | `refactor/prototipo-tesis-v2` |

---

## 2. Configuración de Credenciales y Servicios

*   **Credenciales de Demostración**:
    *   **Administrador**: `admin` / `admin`
    *   **Auditor**: `auditor` / `auditor`
*   **Variables de Entorno (.env)**:
    *   `APP_MODE`: `EXPERIMENT`
    *   `ALLOW_MOCK_MODE`: `false`
    *   `OPENAI_API_BASE`: `https://integrate.api.nvidia.com/v1`
    *   `OPENAI_MODEL`: `z-ai/glm-5.2`

---

## 3. Estado de Compilación Inicial

*   **Frontend**: React + Vite.
*   **Backend**: Flask + SQLite.
*   **Contenedores**: Orquestados con `docker-compose.yml`.
