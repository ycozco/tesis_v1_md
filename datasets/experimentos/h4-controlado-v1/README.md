# H4: casos controlados artificiales, versión 1

Implementa los diez esquemas por producto de la sección 3.9.5.1 de la propuesta vigente: datos completos, cobertura incompleta, nivel comercial incompatible, unidades incompatibles, dato no publicado, versión contradictoria, denominador cero, afirmación sin evidencia, solicitud causal y diferencias entre periodos.

Estos números son **fixtures artificiales** para comprobar informes. No son observaciones SUNAT, no amplían la historia, no entran en H1–H3 y no certifican cobertura de exportaciones. Los documentos incluidos son definiciones artificiales etiquetadas, no fuentes externas ni antecedentes bibliográficos. Las claves se calculan antes de recuperar o generar; ninguna clave se incluye en el payload entregado al generador.

- `cases.json`: 30 solicitudes con sus entradas y huellas.
- `keys.json`: claves numéricas y documentales, elementos requeridos, abstenciones aceptables y advertencias.
- `documents.json`: corpus artificial de definiciones, incluida una versión retirada para los casos contradictorios.
- `schedule.json`: 180 turnos: 30 casos × 2 configuraciones × 3 repeticiones. Todos sin ejecutar.
- `manifest.json`: límites, huella del diseño y estado del congelamiento.

La candidata y la referencia reciben la misma solicitud y datos estructurados. Solo la candidata incorpora recuperación y verificación. El modelo y sus parámetros deben coincidir. No se atribuirá cualquier diferencia exclusivamente a RAG.

Las claves están pendientes de revisión humana. Una abstención explícita y correcta satisface el elemento para el cual la clave exige abstenerse; la omisión no. Esta regla se declara antes de ejecutar y requiere revisión. Los valores del caso entre periodos conservan precisión interna: 800/300, 900/300, diferencia 1/3 USD/kg y cambio 12,5 %.

El diseño no es todavía un experimento listo: faltan congelar modelo/versión/parámetros, prompt, corpus, fragmentación, embeddings, recuperación, filtros temporales e intentos; integrar el ejecutor; preparar revisión ciega; ejecutar y evaluar. `require_execution_ready` rechaza claves sin revisar, configuración incompleta o diseño alterado respecto al congelamiento. Este guard está probado, pero aún no está conectado a un runner experimental. La API de informes existente no ejecuta este catálogo.

Reproducción sin dependencias externas, desde el repositorio:

```
python -B tools/build_h4_controlled_design.py
```

No ejecuta modelos locales ni proveedores de pago. El catálogo anterior de agregados reales se conserva como piloto y no se presenta como los 30 escenarios finales.
