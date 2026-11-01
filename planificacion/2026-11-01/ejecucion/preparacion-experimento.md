# Preparación verificable del experimento final

## Avance de esta entrega

P04: instalado desde cero un entorno científico aislado con Python 3.14.2 dentro del repositorio, sin paquetes de D: ni system-site-packages. Las dependencias exactas resueltas están en `requirements-scientific-clean.txt`; `pip check` no encuentra incompatibilidades. Se verificaron 19 comprobaciones artificiales: ocho configuraciones por cada uno de los dos objetivos con ajuste, predicción finita y aditividad SHAP, más puntuación fuera del ajuste de IF, LOF y ECOD. Esto acredita compatibilidad del núcleo científico en Windows; no una réplica científica ni la instalación completa de API, PostgreSQL/pgvector, embeddings o generador.

P03/P04: reconstruida la vista de características de la colección ampliada en una versión independiente. Se verificaron las 3.845 celdas con operaciones contra sumas Decimal de la fuente; los 16.309 huecos siguen desconocidos. Se preserva el calendario anterior. Las fechas de publicación son desconocidas y ninguna fila se declara elegible para el experimento final.

P06: `pipeline/research/temporal_ledger.py` registra predicciones antes de asociarles observaciones. La calibración solo admite residuos de la misma ejecución/configuración, producto–destino, objetivo y L, de emisiones anteriores y con objetivo ya publicado más el embargo. Se ordenan por semana objetivo, con mínimo 40 y orden `ceil((n+1)*cobertura)`. Las variantes L=0/4/8 nunca comparten residuos por accidente. `run_id` debe identificar la configuración experimental estable a través de sus reajustes semanales; los hashes de cada ajuste y sus datos todavía deben enlazarse en el runner final.

El ledger se guarda sin sobrescribir y se restaura contra una huella conservada en un manifiesto independiente. Se prueban publicación tardía, ausencia del residuo de la semana objetivo en su origen, separación de series/objetivos/configuraciones/L y detección de alteraciones. El hash comprueba integridad, no autenticidad de una publicación. El ledger todavía debe conectarse al runner de selección y al modelo final; no se afirma que el piloto antiguo ya lo use.

## Un comando de preparación

Desde la raíz del repositorio, usando una instalación base de Python 3.14:

```powershell
python -m venv data/runtime-research-clean
./data/runtime-research-clean/Scripts/python.exe -m pip install -r planificacion/2026-11-01/ejecucion/requirements-scientific-clean.txt
./data/runtime-research-clean/Scripts/python.exe -B tools/prepare_final_experiment.py
```

El último comando también puede invocarse mediante rutas absolutas desde otra carpeta: resuelve el repositorio desde su archivo. No instala paquetes, no lee `.env`, no llama a IA, no reajusta con observaciones históricas y no ejecuta el test reservado. Sí ajusta modelos sobre un fixture artificial para comprobar compatibilidad y reconstruye el preprocesamiento retrospectivo. Registra salidas, códigos y hashes del código ejecutado en `preparation-run.json`.

Salida 2 significa que la preparación técnica aprobó pero el diagnóstico científico encontró pendientes; es el resultado esperado actual. Salida 1 indica un fallo técnico. Salida 0 tampoco autoriza automáticamente el test: la revisión del protocolo sigue siendo necesaria. Las librerías quedan fijadas por versión; todavía no existe un almacén de wheels con hashes para reinstalación completamente offline.

## Pendientes que realmente impiden avanzar

`preflight-final.json` enumera siete pendientes actuales:

1. Cobertura semanal completa sin certificados.
2. Publicación histórica y vintages sin certificación.
3. Calendario y protocolo aún sin congelar.
4. Cero filas con elegibilidad as-of verificada para la evaluación final.
5. Selección de desarrollo con la grilla final aún sin ejecutar ni registrar.
6. Claves de los 30 casos H4 pendientes de revisión humana.
7. Generador y recuperación de H4 pendientes de configuración congelada.

El diagnóstico comprueba las fuentes y hashes de artefactos disponibles; es una herramienta de revisión, no un mecanismo suficiente para autorizar la ejecución. No sustituye una política metodológica revisada sobre datos retrospectivos. Resolver la cobertura puede exigir recuperar documentación/periodos o reformular frecuencia y alcance antes del test; no se cambian fechas para buscar mejores errores. La exposición previa a objetivos visualizados permanece declarada.

Próxima dependencia: cerrar P00/P03 y conectar las reglas probadas a un runner de desarrollo con universo común, fechas de publicación verificables, cuatro referencias, selección/desempates y manifiestos de modelos. H4 puede avanzar por separado hacia el runner pareado después de revisar sus claves y fijar generador/corpus. La integridad técnica no se presenta como respaldo empírico de H1–H4.
