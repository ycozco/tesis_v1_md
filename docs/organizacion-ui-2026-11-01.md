# Organización del dashboard y revisión de diseño

## Skills consultadas

Se consultó skill-installer y el catálogo oficial de [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated). Disponibles: figma, figma-generate-design, figma-create-design-system-rules y figma-implement-design. Son candidatas si se adopta un archivo Figma; no se instalaron porque no hay referencia Figma y el repositorio ya impone DESIGN.md. Se aplicaron sus reglas locales: tonos verdes, Outfit/Inter, paneles glass y grillas responsivas.

## Cambios aplicados

- Resumen como entrada por defecto, con seis accesos por intención y alcance de los datos.
- Navegación distingue series/destinos, modelos piloto, protocolo y reportes IA.
- Mantiene enlaces de vistas anteriores y filtros existentes.
- Corrige fuentes: los paquetes adicionales sí están conciliados en la versión ampliada; gráficos siguen en el snapshot anterior.
- Evaluación piloto no se presenta como una emisión futura; prueba final marcada no ejecutada.
- Transición breve de 180 ms al cambiar vista, conservando preferencia de movimiento reducido y foco visible existentes. No se anima un progreso de cómputo inexistente.

## Verificación

npm run build aprobado tras el cambio; persiste aviso de bundle principal de unos 598 kB. No se ejecutó de nuevo la suite de backend porque no se modificaron sus módulos. La comprobación visual actual quedó bloqueada: el controlador de la pestaña respondió browser.user is unavailable incluso al recuperar su ID. No hay nueva captura ni aprobación de escritorio/móvil para esta reorganización.

## Pendientes de UI

1. Verificar resumen y navegación en escritorio/móvil, foco, movimiento reducido y retorno entre vistas.
2. Verificar visualmente el bloque actualizado Protocolo de reportes: ya distingue 30 casos artificiales, 180 salidas previstas y piloto Codex separado.
3. Vista de mercados con agregaciones por país y participaciones solo sobre registros disponibles; agrupación regional documentada. No atribuir aduana a región productiva.
4. Integrar una sola versión de datos aprobada o mantener avisos explícitos al comparar ampliada/piloto.
5. E1–E3 navegables con entrada conocida, cálculos, exportación y linaje; corregir la brecha de horizonte E3.
6. Estados de trabajo reales para pronóstico/señales/SHAP; detalle ejecutable cuando existan artefactos válidos.
7. Perfiles, permisos entre cuentas e historial de consultas reproducibles.
8. Enlaces directos por artefacto/documento además de portales institucionales.
9. Dividir bundle y revisar contraste/accesibilidad; no afirmar WCAG ni usabilidad acreditadas sin evaluación.

Esta entrega organiza la interfaz y corrige contenido puntual; no declara resueltos todos los pendientes científicos o de UI.

## Corrección aplicada posteriormente

Navegación móvil en grilla de dos columnas (cuatro en ancho intermedio), evitando depender de una tira horizontal para descubrir secciones. Selector de objetivo adaptable a ancho móvil; tablas desplazables enfocables por teclado y etiquetadas. País de destino aclara que conserva el código de la fuente. Protocolo H4 actualizado y enlace directo a la tesis. Build aprobado; diff sin errores de espacios. La recuperación de la pestaña volvió a fallar con browser.user is unavailable: validación visual pendiente, sin nueva captura.
