# Plan de migración del backend Flask a FastAPI para producción

**Proyecto:** Sistema inteligente de supervisión agroexportadora  
**Repositorio:** `ycozco/tesis_v1_md`  
**Fecha de elaboración:** 5 de julio de 2026  
**Estado:** En ejecución  
**Arquitectura actual:** React/Vite + Flask/Gunicorn + SQLAlchemy + PostgreSQL/pgvector  
**Arquitectura objetivo:** React/Vite + FastAPI/Uvicorn + SQLAlchemy + PostgreSQL/pgvector

---

## 1. Propósito

El objetivo de este documento es establecer una guía verificable para migrar progresivamente el backend actual implementado con Flask hacia FastAPI, sin interrumpir el prototipo existente y sin presentar como finalizada una migración que todavía se encuentra en desarrollo.

La migración mantiene el ecosistema Python y los componentes analíticos existentes: XGBoost, PyOD, SHAP, Sentence-Transformers, pgvector y SQLAlchemy. El cambio se concentra en la capa de exposición de servicios, validación de esquemas, documentación de API, seguridad, observabilidad y despliegue.

## 2. Justificación técnica

FastAPI se selecciona porque el sistema funciona principalmente como una API REST para un cliente React y porque requiere validar entradas estructuradas, devolver respuestas tipadas, documentar contratos OpenAPI y exponer servicios de predicción y auditoría. Uvicorn se utilizará como servidor ASGI.

Flask no se considera inválido para producción. La implementación existente puede ejecutarse mediante Gunicorn; sin embargo, FastAPI ofrece una base más adecuada para contratos tipados, validación automática, documentación interactiva y evolución modular de servicios analíticos.

## 3. Estado verificado al 5 de julio de 2026

### 3.1 Componentes existentes

- Cliente web React/Vite.
- Backend monolítico en `sistema-web-agro/backend/app.py`.
- Modelos SQLAlchemy y sesiones de base de datos.
- PostgreSQL con extensión pgvector.
- Endpoints de autenticación, dashboard, alertas, decisiones, reportes, telemetría y configuración.
- Carga de artefactos XGBoost, Isolation Forest, LOF, ECOD y SHAP.
- Recuperación semántica mediante embeddings.
- Despliegue local mediante Docker Compose.

### 3.2 Componentes de migración ya creados

- `sistema-web-agro/backend/requirements-fastapi.txt`.
- `sistema-web-agro/backend/main_fastapi.py`.
- Endpoint `GET /health`.
- Endpoint `GET /api/migration/status`.
- Configuración inicial de CORS.
- Inicialización de tablas mediante ciclo de vida de FastAPI.

### 3.3 Estado real

La aplicación FastAPI todavía no reemplaza al backend Flask. Solo existe un punto de entrada ASGI inicial. Las rutas funcionales del sistema continúan en Flask y deben migrarse y probarse por grupos.

## 4. Arquitectura objetivo

```text
Usuario
  ↓
React / Vite
  ↓ HTTPS
Proxy inverso Nginx o Traefik
  ↓
FastAPI ejecutado con Uvicorn
  ├── API de autenticación y autorización
  ├── API de alertas y decisiones
  ├── API de predicción y anomalías
  ├── API de explicabilidad SHAP
  ├── API de reportes RAG
  ├── API de telemetría y auditoría
  └── Health, readiness y métricas
       ↓
SQLAlchemy
       ↓
PostgreSQL 15 + pgvector

Servicios complementarios:
- almacenamiento versionado de modelos;
- almacenamiento de artefactos y reportes;
- proveedor de modelos de lenguaje;
- monitoreo y registro centralizado;
- CI/CD y pruebas automatizadas.
```

## 5. Estructura objetivo del backend

```text
sistema-web-agro/backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── dashboard.py
│   │           ├── alerts.py
│   │           ├── decisions.py
│   │           ├── reports.py
│   │           ├── telemetry.py
│   │           └── configuration.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   └── migrations/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   │   ├── prediction.py
│   │   ├── anomaly.py
│   │   ├── explainability.py
│   │   ├── rag.py
│   │   └── reporting.py
│   └── observability/
│       ├── metrics.py
│       └── tracing.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── performance/
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

## 6. Fases de implementación

### Fase 0. Línea base y congelamiento del contrato actual

**Objetivo:** evitar que la migración cambie silenciosamente el comportamiento consumido por React.

**Tareas:**

- Inventariar todos los endpoints Flask.
- Registrar método, ruta, parámetros, cuerpo, respuesta y códigos HTTP.
- Capturar ejemplos reales de solicitudes y respuestas.
- Crear pruebas de contrato para el comportamiento actual.
- Registrar dependencias del frontend respecto de cada endpoint.

**Entregables:**

- `docs/api/contrato-flask-actual.md`.
- Colección Postman o archivo OpenAPI provisional.
- Pruebas de contrato ejecutables.

**Criterio de aceptación:** el comportamiento actual puede reproducirse automáticamente antes de migrar una ruta.

### Fase 1. Configuración, seguridad y base transversal

**Tareas:**

- Crear configuración tipada mediante `pydantic-settings`.
- Retirar secretos definidos directamente en código o `docker-compose.yml`.
- Gestionar `DATABASE_URL`, `SECRET_KEY`, claves del proveedor LLM y orígenes CORS mediante variables de entorno.
- Implementar gestión centralizada de errores.
- Implementar sesiones SQLAlchemy mediante dependencias de FastAPI.
- Crear endpoints `/health`, `/ready` y `/version`.
- Configurar logs JSON con identificador de solicitud.

**Criterio de aceptación:** la aplicación arranca sin secretos codificados y puede informar salud, preparación y versión.

### Fase 2. Autenticación y autorización

**Tareas:**

- Reemplazar el token simulado por JWT de acceso y, si corresponde, token de renovación.
- Definir esquemas Pydantic para login, usuario y sesión.
- Mantener verificación segura de contraseñas.
- Implementar autorización por roles: administrador, auditor y analista.
- Registrar eventos de seguridad y fallos de autenticación.
- Definir expiración, rotación y revocación.

**Criterio de aceptación:** ninguna ruta protegida puede ejecutarse sin token válido y rol autorizado.

### Fase 3. Migración de consultas de lectura

Orden recomendado:

1. dashboard;
2. listado de alertas;
3. detalle de alerta;
4. historial;
5. telemetría;
6. configuración de solo lectura.

**Tareas:**

- Crear routers separados.
- Crear esquemas de respuesta.
- Evitar serialización manual con `to_dict()` cuando pueda usarse `from_attributes`.
- Eliminar mutaciones y cálculos aleatorios dentro de operaciones GET.
- Añadir paginación, filtros, ordenamiento y límites máximos.

**Criterio de aceptación:** las respuestas FastAPI coinciden con el contrato usado por React y no alteran datos durante consultas GET.

### Fase 4. Migración de operaciones de escritura

Incluye:

- registro de decisiones;
- actualización de estados;
- configuración del pipeline;
- generación y persistencia de reportes;
- administración de usuarios.

**Tareas:**

- Validar cuerpos mediante Pydantic.
- Gestionar transacciones y rollback.
- Implementar idempotencia donde una repetición pueda duplicar decisiones o reportes.
- Añadir control de concurrencia optimista o versiones en operaciones sensibles.
- Registrar auditoría antes y después del cambio.

**Criterio de aceptación:** no existen escrituras parciales y cada cambio puede rastrearse al usuario, solicitud y versión.

### Fase 5. Separación de servicios analíticos

**Tareas:**

- Extraer carga de modelos fuera de los controladores HTTP.
- Crear servicios independientes para predicción, anomalías, SHAP y RAG.
- Cargar modelos una sola vez durante el inicio del proceso.
- Verificar hash y versión de cada artefacto antes de utilizarlo.
- Eliminar variables aleatorias usadas para construir características demostrativas.
- Prohibir datos simulados en modo de producción.
- Definir timeout para generación de reportes y llamadas al proveedor LLM.

**Criterio de aceptación:** cada resultado registra versión del modelo, hash del artefacto, dataset y configuración utilizada.

### Fase 6. Persistencia y migraciones de base de datos

**Tareas:**

- Incorporar Alembic.
- Crear migraciones versionadas.
- Añadir clave foránea entre `OperacionAlerta.run_id` y `PipelineRun.run_id`.
- Revisar índices para filtros y ordenamiento.
- Definir políticas de retención de logs y reportes.
- Completar la anonimización de RUC y razón social.
- Definir estrategia de respaldo y restauración.

**Criterio de aceptación:** una base nueva puede crearse desde migraciones y una base existente puede actualizarse sin ejecutar `init_tables()` como mecanismo principal.

### Fase 7. Contenedores y proxy inverso

**Tareas:**

- Crear Dockerfile de producción multi-stage.
- Ejecutar Uvicorn sin modo reload.
- Incorporar usuario no root.
- Añadir health check del contenedor.
- Configurar Nginx o Traefik como terminación TLS y proxy inverso.
- Limitar tamaño de solicitudes y tiempos de espera.
- Definir red interna para PostgreSQL.
- No publicar el puerto 5432 fuera de la red del despliegue.

**Criterio de aceptación:** solo el proxy inverso queda expuesto públicamente y el backend y la base de datos permanecen en red privada.

### Fase 8. Pruebas automatizadas

**Cobertura mínima:**

- pruebas unitarias de servicios;
- pruebas de integración con PostgreSQL/pgvector;
- pruebas de contrato API;
- pruebas de autenticación y roles;
- pruebas de carga de artefactos;
- pruebas de ausencia de fuga temporal;
- pruebas de fidelidad numérica de reportes;
- pruebas end-to-end con React;
- pruebas de carga con tiempos y concurrencia definidos.

**Herramientas propuestas:** pytest, HTTPX/TestClient, Testcontainers o una base PostgreSQL de pruebas, Locust o k6.

**Criterio de aceptación:** CI bloquea el merge si fallan pruebas críticas, seguridad o migraciones.

### Fase 9. Observabilidad

**Tareas:**

- Logs estructurados.
- Métricas de latencia, tasa de error, solicitudes y consumo de recursos.
- Métricas de inferencia por modelo.
- Registro de versión de modelos y dataset.
- Trazas distribuidas si se separan servicios.
- Alertas operativas por fallos, latencia o indisponibilidad.

**Opciones:** Prometheus, Grafana, OpenTelemetry y Loki, o servicios equivalentes.

**Criterio de aceptación:** un error puede rastrearse desde la solicitud HTTP hasta la consulta, modelo y reporte relacionado.

### Fase 10. CI/CD y despliegue

**Tareas:**

- Pipeline de lint, tipos, pruebas, seguridad y construcción de imagen.
- Escaneo de dependencias e imagen.
- Etiquetado de imágenes por commit y versión.
- Despliegue a entorno de pruebas antes de producción.
- Migraciones controladas antes de activar la nueva versión.
- Estrategia de rollback.
- Prueba de humo posterior al despliegue.

**Criterio de aceptación:** cualquier versión desplegada puede identificarse, reproducirse y revertirse.

### Fase 11. Retiro de Flask

Flask solo podrá retirarse cuando:

- todas las rutas hayan sido migradas;
- React consuma únicamente FastAPI;
- las pruebas de contrato sean equivalentes;
- exista evidencia de rendimiento y estabilidad;
- no haya imports activos de Flask o Flask-Cors;
- Docker Compose y documentación apunten al nuevo punto de entrada;
- el despliegue FastAPI haya superado un periodo de validación.

## 7. Aspectos que todavía faltan

### Prioridad crítica

- Migrar todos los endpoints funcionales; actualmente solo existen endpoints de salud y estado.
- Sustituir tokens simulados por autenticación real.
- Retirar credenciales y secretos codificados.
- Eliminar datos aleatorios y simulaciones de rutas productivas.
- Incorporar Alembic y corregir integridad referencial.
- Proteger datos identificables de exportadores.
- Crear pruebas automáticas y contratos API.
- Actualizar Docker Compose para arrancar FastAPI/Uvicorn.

### Prioridad alta

- Dividir el archivo monolítico `app.py` en routers, servicios, repositorios y esquemas.
- Implementar manejo centralizado de errores.
- Añadir paginación y límites en consultas.
- Registrar versión y hash de modelos en cada inferencia.
- Añadir timeout, reintentos controlados y circuit breaker para el proveedor LLM.
- Configurar health/readiness checks reales.
- Configurar proxy inverso y TLS.
- Crear respaldo y restauración de PostgreSQL.

### Prioridad media

- Observabilidad con métricas y trazas.
- Caché para consultas o embeddings frecuentes.
- Cola de trabajo para reportes largos o tareas de inferencia pesada.
- Rate limiting.
- Pruebas de carga y definición de SLO.
- Documentación operativa y manual de incidentes.

## 8. Riesgos de la migración

| Riesgo | Consecuencia | Mitigación |
|---|---|---|
| Cambiar respuestas consumidas por React | Fallo del frontend | Pruebas de contrato y migración por rutas |
| Mantener dos backends demasiado tiempo | Duplicidad y divergencia | Fecha de corte y matriz de rutas |
| Ejecutar inferencia pesada en el proceso HTTP | Bloqueos y alta latencia | Servicios desacoplados o cola de trabajo |
| Cargar modelos por worker | Consumo elevado de memoria | Medir memoria y ajustar número de workers |
| Migrar autenticación sin pruebas | Acceso no autorizado | Pruebas de roles, expiración y revocación |
| Publicar PostgreSQL | Exposición de datos | Red privada y reglas de firewall |
| Documentar FastAPI como terminado antes de estarlo | Inconsistencia de tesis | Clasificar estado como objetivo o en migración |

## 9. Matriz de avance

| Componente | Flask actual | FastAPI objetivo | Estado al 05/07/2026 |
|---|---|---|---|
| Punto de entrada | `app.py` | `app/main.py` o `main_fastapi.py` | Inicial creado |
| Health check | Parcial/no normalizado | `/health`, `/ready`, `/version` | `/health` creado |
| Autenticación | Token simulado | JWT y roles | Pendiente |
| Dashboard | Implementado | Router tipado | Pendiente |
| Alertas | Implementado | Router tipado y paginado | Pendiente |
| Decisiones | Implementado | Transaccional e idempotente | Pendiente |
| SHAP | Integrado en controlador | Servicio independiente | Pendiente |
| RAG/reportes | Integrado en controlador | Servicio con timeout y validación | Pendiente |
| Base de datos | SQLAlchemy + `init_tables()` | SQLAlchemy + Alembic | Pendiente |
| CORS | Global y permisivo | Lista por entorno | Inicial |
| Despliegue | Gunicorn/Flask | Uvicorn detrás de proxy | Pendiente |
| Pruebas | Insuficientes | Unitarias, integración, contrato y carga | Pendiente |
| Observabilidad | Logs básicos | Logs JSON, métricas y trazas | Pendiente |

## 10. Definición de terminado

La migración se considerará finalizada cuando:

1. todas las rutas utilizadas por React estén disponibles en FastAPI;
2. las pruebas de contrato demuestren compatibilidad;
3. los secretos estén fuera del repositorio;
4. PostgreSQL use migraciones Alembic y restricciones de integridad;
5. JWT y roles reemplacen al token simulado;
6. no existan datos aleatorios en rutas productivas;
7. los modelos se carguen y versionen de forma verificable;
8. Docker Compose arranque FastAPI/Uvicorn;
9. CI ejecute pruebas y escaneos obligatorios;
10. existan métricas, logs y estrategia de rollback;
11. Flask y Flask-Cors hayan sido retirados de dependencias y código;
12. la tesis describa FastAPI como implementación verificada y no únicamente como arquitectura objetivo.

## 11. Próximo incremento recomendado

El siguiente incremento debe migrar exclusivamente autenticación y dashboard. Antes de migrar alertas o reportes debe crearse la base transversal de configuración, seguridad, sesiones SQLAlchemy, errores y pruebas de contrato.

Orden inmediato:

1. crear paquete `app/`;
2. configurar `pydantic-settings`;
3. implementar dependencia `get_db()`;
4. crear esquemas de usuario y login;
5. implementar JWT y roles;
6. migrar `/api/auth/login`, `/api/auth/logout` y `/api/dashboard/stats`;
7. añadir pruebas de integración;
8. actualizar React solo después de validar equivalencia;
9. actualizar Docker Compose para disponer de un perfil FastAPI de pruebas;
10. registrar evidencia de ejecución y resultados.

---

**Responsable de actualización:** Yoset Cozco Mauri  
**Regla de mantenimiento:** actualizar este documento en cada incremento indicando commit, rutas migradas, pruebas ejecutadas y riesgos pendientes.
