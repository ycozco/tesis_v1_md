# Arranque de investigación y conexión IA

1 de noviembre de 2026. Hay dos modalidades: revisión aislada y uso con servicios reales. Los controles de IA están en `/dashboard?view=ia`; la comprobación de archivos, en `/dashboard?view=proceso`.

## Revisión aislada ya comprobada

Desde E:/tesis-yoset/github, con las librerías auditadas disponibles:

```powershell
& 'D:/tesis_yoset/.venv/Scripts/python.exe' -B tools/serve_research_preview.py
```

En otra terminal:

```powershell
Set-Location 'E:/tesis-yoset/github/sistema-web-agro/frontend'
$env:AGRO_API_TARGET = 'http://127.0.0.1:5002'
npm run dev -- --host 127.0.0.1
```

UI: http://127.0.0.1:8050. Cuenta exclusiva de QA en SQLite aislado: usuario `revision-ui`, contraseña `SoloRevisionLocal2026!`. El helper nunca apunta a la base de producción y fuerza deshabilitada la IA local/de pago. Si estos procesos ya están activos, se puede usar la pestaña abierta sin lanzar duplicados.

## Backend con servicios reales

Se requieren una base y usuarios reales, dependencias del backend, clave de sesión privada persistente y la configuración del proveedor. No se provisionaron cuentas externas ni se migró PostgreSQL en esta revisión.

Defina las variables de `backend/research-ai.env.example` en el entorno o en el `.env` privado de la raíz. Reinicie el backend después de cambiarlas. No se escribe ese archivo desde la UI.

```powershell
Set-Location 'E:/tesis-yoset/github'
$env:PYTHONPATH = 'E:/tesis-yoset/github/data/runtime-api;E:/tesis-yoset/github/sistema-web-agro/backend'
& 'D:/tesis_yoset/.venv/Scripts/python.exe' -B -m uvicorn app_fastapi.main:app --host 127.0.0.1 --port 5001
```

En esta modalidad Vite usa su destino predeterminado 5001: quite la variable AGRO_API_TARGET de esa terminal o asígnele el puerto correspondiente. No ejecute `serve_research_preview.py` para intentar habilitar IA: ese helper conserva el bloqueo por diseño.

**Ollama:** instale y ejecute el servicio oficial, seleccione un modelo adecuado al equipo y compruebe su presencia local. Defina `RESEARCH_ALLOW_LOCAL_AI=true` y `RESEARCH_OLLAMA_MODEL` con su nombre exacto. No se recomienda un modelo ni se inicia una descarga de varios GB sin conocer recursos disponibles. La UI consulta disponibilidad; los modelos cloud no se admiten como inferencia local.

**DeepSeek:** defina una clave privada en `RESEARCH_DEEPSEEK_API_KEY`, `RESEARCH_ALLOW_PAID_AI=true` y el modelo, inicialmente `deepseek-flash`. Entre con ADMIN, revise el caso y acepte el envío de hechos agregados y el consumo antes de solicitar un borrador. No se probaron facturación ni conexión real de pago. Documentación: [DeepSeek](https://api-docs.deepseek.com/quick_start), [Ollama](https://docs.ollama.com/api/openai-compatibility).

Los borradores se archivan localmente con evidencia y hashes. Verificación numérica no significa validación factual completa; cada texto exige revisión humana. No son salidas de la evaluación H4. Nunca coloque claves en VITE_*, en el navegador o en archivos versionados.
