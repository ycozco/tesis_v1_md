# AgroScope Perú: despliegue local

Desde `sistema-web-agro`:

```powershell
docker compose up -d --build --wait
docker compose ps
docker compose logs --tail 50 backend
```

Abrir http://localhost:8050. Cuenta de revisión local: `revision-ui`, contraseña
`SoloRevisionLocal2026!`. Al migrar desde Vite, cerrar la sesión anterior y entrar
de nuevo; sus tokens fueron emitidos por otro backend.

La imagen Python instala las versiones verificadas de `backend/requirements-local.lock`;
el frontend utiliza `npm ci` y `package-lock.json`.

Nginx sirve el frontend compilado y envía `/api/` a FastAPI. PostgreSQL/pgvector
queda en la red interna. Los volúmenes `postgres_data` y `research_state` conservan
cuentas, registros, reportes y la clave de sesión entre reinicios. La extensión
vector se crea al arrancar; esto no acredita evaluación de recuperación semántica.
Las llamadas a proveedores de IA permanecen deshabilitadas por defecto.

El Compose de la raíz corresponde al visor de tesis y es independiente. Este
Compose reemplaza la combinación anterior de Flask y FastAPI para el prototipo.

Opcional: crear un `.env` local (ignorado por Git) con `AGRO_WEB_PORT`,
`AGRO_LOCAL_USERNAME`, `AGRO_LOCAL_PASSWORD` y `AGRO_DB_PASSWORD`. Cambiar la
contraseña de PostgreSQL con un volumen existente requiere actualizar también el
usuario en la base; la variable de inicialización no cambia usuarios existentes.

Para detener sin perder datos: `docker compose stop`. Para reconstruir cambios:
`docker compose up -d --build --wait`. No usar `down -v` salvo que se desee eliminar
los datos locales. No es necesario instalar Python o Node en Windows.

Los gráficos utilizan el corte documentado de `public/research/snapshot.json`.
La consulta de fuentes externas informa su disponibilidad y contexto; no cambia
automáticamente el conjunto de investigación ni los resultados de la tesis.

## Verificación realizada

Tres servicios saludables; acceso mediante Nginx; integridad de 44 archivos y siete
artefactos de avance; 30 casos disponibles; sesión válida después de reiniciar el
backend; 18 pruebas de API y fuentes aprobadas. Vista de escritorio y menú móvil
verificados en navegador. `pip check` no encuentra dependencias incompatibles.

Las fuentes se consultan cada 15 minutos mientras el panel está abierto, con caché
del servidor por 15 minutos. SUNAT, SISAP y NASA muestran accesibilidad del enlace;
BCRP también devuelve la última observación numérica de PN01207PM. El periodo de
la observación y la hora de consulta se presentan por separado.

Pendientes técnicos: la instalación del frontend reportó diez avisos de seguridad
en su árbol npm y el build advierte un bundle de más de 500 kB. La migración de
versiones mayores y la optimización del bundle requieren trabajo adicional.
