# Ejecución del plan — 1 de noviembre de 2026

Documento rector: [tesis vigente, modificación 23 de octubre](https://docs.google.com/document/d/13cJUk1_AMrI-jsZj0s6a5XuTmE7wXZLFL-SNlPGxt8g/edit). Metadatos reconfirmados durante esta ejecución. Las referencias T01–T12 remiten a `../fundamento-tesis.json`; esta entrega no sustituye la tesis ni declara resultados finales.

## Cambios ejecutados

- P02: incorporados 8.579 registros filtrados de dos paquetes históricos, con SHA-256 comprobados. Colección ampliada: 118.832 entradas de 24 paquetes. Conciliación: 101.546 registros únicos frente a 93.225 anteriores; ganancia neta 8.321. Sustituidas 9.349 versiones y descartados 7.829 duplicados. Permanecen 108 registros en cuarentena, correspondientes a 73 claves. Verificador independiente confirma contabilidad y correspondencia con DBF. No se publican originales con identificadores personales.
- P03: auditoría ejecutable de cobertura y elegibilidad contextual, sin entrenamiento. Los huecos no se convierten en ceros. No hay certificados de cobertura completa ni de publicación histórica; las observaciones recuperadas siguen siendo parciales.
- P04: eliminado el acceso obligatorio a D: en la recuperación BCRP del constructor. Usa el archivo recuperado y versionado en el repositorio. La auditoría y las reglas de referencias funcionan con biblioteca estándar. Esto no acredita todavía la instalación limpia del entorno científico completo.
- P05: implementadas cuatro referencias con observaciones válidas y disponibilidad explícita, escala MASE con mínimo 26 pares estacionales, SMAPE y grilla de ocho candidatos con parámetros explícitos. Aún falta conectarlas al ejecutor final y seleccionar con desarrollo común.
- P06: corregida calibración de intervalos: orden `ceil((n+1)*cobertura)`, mínimo 40 errores anteriores, rango inválido sin intervalo y predicción no negativa. La procedencia temporal de los errores deberá garantizarla el ejecutor; la función por sí sola no la certifica.
- P11: corregida tolerancia numérica a media unidad del último decimal más 1e-9. No se han ejecutado los 180 ensayos H4.

## Matriz de requisitos y divergencias

| Fundamento | Requisito vigente | Evidencia de implementación / verificación | Pendiente |
|---|---|---|---|
| T01–T03 | Seis objetivos; cuatro hipótesis; evaluación técnica documental | Plan y fuente rectora versionados | `docs/02-10-capitulo1.md` conserva H1a–H1e y evaluación de usuarios antigua: requiere alineación editorial; no usar como protocolo rector |
| T04–T05 | Cuatro referencias, grilla exacta, MAE macro por ambos objetivos | `methodology.py`, pruebas de huecos y disponibilidad; `grid-candidatos.json` | Integración del runner, desempates, selección completa en desarrollo |
| T05–T06 | Disponibilidad histórica y calibración previa por serie | Auditoría, intervalos corregidos, pruebas de regresión | Certificados, universo común y residual ledger temporal; calendario congelado |
| T07–T08 | H3 exploratorio y SHAP sin interpretación causal | Pilotos anteriores conservados como pilotos | Percentiles de entrenamiento, presupuesto por producto y rúbrica estacional final |
| T09–T12 | Evidencia verificable, informes y reproducibilidad | Validador corregido; conciliación verificable y auditoría portable | Corpus/pgvector real, casos controlados H4, 180 ejecuciones, revisión ciega y E1–E3 |

La matriz rastrea requisitos de la propuesta, pero no sustituye la matriz antecedente–hallazgo–adaptación: la verificación de los artículos primarios de cada antecedente sigue pendiente en P00.

## Decisiones y límites

1. Conservar intactos los conjuntos y pilotos anteriores. La expansión es una versión nueva; no se actualizan resultados de UI o modelos con un conjunto distinto sin reconstruir su linaje.
2. Mantener la cuarentena. La conciliación de archivos disponibles no equivale a certificación oficial de cobertura ni a validar una resolución heurística.
3. No entrenar ni evaluar el bloque final hasta cerrar cobertura, política de disponibilidad, exposición previa y congelamiento del protocolo. Ya se visualizaron objetivos reales del periodo propuesto: no describirlo como totalmente ciego.
4. BCRP, SISAP, NASA y Comtrade siguen excluidos de H2 histórico hasta resolver las limitaciones registradas en `auditoria-expansion.json`; no se sustituyen por constantes o datos sintéticos.
5. La rotación de la credencial histórica sigue pendiente del titular. No se leen ni reutilizan secretos locales.

## Reproducción de esta entrega

Desde el repositorio, con Python 3.14 y biblioteca estándar:

```
python -B tools/expand_sunat_collection.py
python -B tools/reconcile_sunat.py . datasets/fuentes/2026-11-01-expansion
python -B tools/verify_sunat_reconciliation.py . datasets/fuentes/2026-11-01-expansion
python -B tools/audit_expanded_collection.py
```

Los tres primeros pasos requieren los 24 ZIP originales locales bajo `data/`, excluidos de Git por contener datos personales. Para auditar cobertura desde la vista filtrada publicada basta el último paso. La reproducción sin originales no acredita la comprobación independiente contra DBF.

Pruebas de reglas: `python -B -m pytest tests/unit/test_methodology.py tests/unit/test_research_protocol.py -q`. No son prueba de resultados científicos ni de reproducibilidad integral del experimento. Siguiente dependencia crítica: completar P00/P03 y un ejecutor de desarrollo que aplique estas reglas antes de continuar hacia H1–H4 finales.

## Verificación ejecutada

12 pruebas de reglas e informes y 11 de API aprobadas. API conserva 28 advertencias de deprecación. Auditoría de cobertura repetida con Python 3.14.2 en un entorno nuevo creado sin pip ni paquetes externos. No se acredita aún instalación científica limpia ni experimento final.

## Estado de publicación

Entrega guardada en el repositorio y en la copia local de Drive. La revisión automática rechazó subir el ZIP por datos históricos y visibilidad del destino. Metadatos posteriores confirman que la carpeta pertenece al titular y está compartida con el dominio UNSA y colaboradores. No se modifica su acceso; publicación remota pendiente de aprobación explícita del paquete. No se enviaron originales DBF/ZIP ni secretos.
