# Revisión narrativa: sistema desarrollado

**Fecha:** 5 de julio de 2026

Se revisó la tesis completa desde el Capítulo I para identificar expresiones que presentan el software como propuesta, prototipo, vista o trabajo futuro, pese a que el repositorio ya contiene interfaz, backend, modelos, persistencia, endpoints, reportes y trazabilidad implementados.

## Criterio de redacción

La tesis debe describir el artefacto como **sistema desarrollado y funcional**. Las expresiones de futuro deben reservarse únicamente para validaciones científicas, pruebas con usuarios, métricas finales y endurecimiento productivo.

## Sustituciones obligatorias

- `prototipo` → `sistema desarrollado` o `sistema funcional`, según el contexto.
- `propuesta` → `solución desarrollada` cuando se refiere al artefacto.
- `se implementará` → `se implementó` o `está implementado`.
- `será desarrollado` → `fue desarrollado`.
- `arquitectura objetivo` → `arquitectura implementada` cuando el componente existe en el repositorio.
- `plan de migración` → `arquitectura de servicios desarrollada` si la tecnología ya forma parte del sistema.
- `vistas` → `módulos funcionales de la interfaz`.
- `prototipo funcional` → `sistema funcional desarrollado`.

## Capítulos afectados

### Capítulo I

Debe presentar el sistema como construido. Los objetivos pueden conservarse en infinitivo porque forman parte de la estructura metodológica, pero la descripción de viabilidad, alcance y solución debe escribirse en presente o pasado.

### Capítulo II

Las frases como `la propuesta de esta tesis plantea` deben cambiarse por `el sistema desarrollado integra` cuando describen la solución propia.

### Capítulo III

El título debe ser `Desarrollo e implementación del sistema`. La arquitectura, requisitos, entradas, salidas, persistencia y servicios deben describirse como componentes implementados.

### Capítulo IV

Debe titularse y redactarse como resultados de la implementación del sistema. Las limitaciones deben referirse a validación experimental o preparación productiva, no a inexistencia del software.

## Diferencia necesaria

- **Sistema desarrollado:** interfaz, servicios, modelos, base de datos, alertas, reportes y trazabilidad existen en código.
- **Validación experimental pendiente:** métricas finales, estudio con usuarios, intervalos de confianza o pruebas estadísticas.
- **Endurecimiento productivo pendiente:** gestión de secretos, TLS, observabilidad, escalamiento y despliegue final.

No se debe volver a describir el sistema como una simple propuesta o conjunto de vistas.
