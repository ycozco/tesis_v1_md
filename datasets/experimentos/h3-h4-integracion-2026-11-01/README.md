# H3 y H4 — integración y verificación técnica

## H3: ejecutor integrado con entrenamiento previo

`pipeline/research/h3_engine.py` integra escalado ajustado en entrenamiento, Isolation Forest, LOF en modo novelty, una adaptación inductiva de ECOD, percentiles de entrenamiento y combinación con pesos iguales. Los cinco métodos —tres detectores, ensemble y referencia frente a 52 semanas— usan un universo común y el presupuesto por producto de la propuesta. Se conservan las tres sensibilidades de persistencia y q/r/u, límites por indeterminados y solapamientos. No se selecciona un ganador por afinidad con la rúbrica.

Se ejecutaron **189 casos artificiales y nueve ajustes**; hay 63 candidatos por producto y K=4 en cada método. Las variables son residuos hipotéticos de FOB y volumen, cambio relativo frente a 52 semanas y valor unitario. Los residuos son fixtures de pronósticos fuera de ajuste, no salidas de modelos H1 finales. Las inyecciones, magnitudes y semilla 42 quedan separadas del histórico. El escalador, la ventana y los parámetros son una configuración técnica de desarrollo; aún no una selección histórica definitiva.

### Hallazgo ECOD y corrección propuesta

La versión instalada PyOD 3.6.0 concatena el lote nuevo con el entrenamiento al puntuar con ECOD y recalcula su distribución. El [código oficial publicado](https://pyod.readthedocs.io/en/latest/_modules/pyod/models/ecod.html) también muestra ese comportamiento en la documentación consultada, que corresponde a una versión posterior. La constatación del entorno se basa en el código instalado, no en suponer que ambas versiones son idénticas.

La adaptación propuesta fija CDF y signo de asimetría exclusivamente en el entrenamiento, con colas acotadas inferiormente por 1/(n+1). Usa ECDF inclusiva a derecha e izquierda para las dos colas. Se registra como **ECOD adaptado con distribución fija**, no como ejecución sin cambios del ECOD de PyOD. Las pruebas verifican que añadir casos nuevos extremos no cambia la puntuación del caso inicial, tanto en el adaptador como en el ejecutor completo. Esta adaptación debe declararse y fijarse en el protocolo de desarrollo antes de cualquier evaluación histórica final; sus garantías no se atribuyen automáticamente al artículo original.

Los resultados de `h3-artificial-analysis.json` caracterizan únicamente el fixture. El histórico final sigue **sin ejecutar**: el panel no tiene cobertura y publicación certificadas y faltan pronósticos H1 finales elegibles. `historical-h3-gate.json` conserva la huella del panel y ese resultado, sin inventar una muestra histórica K>0.

## H4: ejecución pareada, evaluación y revisión ciega

El ejecutor conserva entradas y parámetros iguales, inicial/correcciones/final, documentos recuperados, errores y fallback cuando está explícitamente configurado y verificado. Las claves de evaluación no se pasan al generador, al recuperador ni al verificador de la aplicación. Cada recorrido puede guardarse mediante checkpoint. Antes de una ejecución real se verifican hashes de casos, claves y calendario; revisión humana registrada; congelamiento del diseño, prompt/corpus y proveedor real.

Se ejercitaron **180 recorridos con un transporte determinista artificial**, sin llamadas a Ollama o DeepSeek. La recuperación del fixture es una consulta por ID, no PostgreSQL/pgvector ni RAG denso. El verificador del fixture solo comprueba el esquema. Estos recorridos prueban las interfaces y los registros; **no son 180 salidas experimentales de un modelo de lenguaje ni respaldan H4**. Los valores correctos del fixture no son una comparación de calidad entre configuraciones.

Se preparó la submuestra técnica de **45 salidas**, semilla 42, seis estratos producto × configuración con 7/8 por estrato. La permutación de IDs ciegos usa aleatoriedad separada y privada; no se reconstruye la condición con la semilla pública del muestreo. El mapeo de condiciones queda en `data/h4-technical-fixture/private-blind-mapping.json`, fuera de la entrega; el paquete público oculta configuración y repetición. La forma o contenido de una respuesta todavía podría sugerir su condición: se oculta la asignación sin afirmar cegamiento perfecto. El paquete está etiquetado como fixture y no debe calificarse como si fuera el experimento final.

La evaluación numérica toma la precisión de la clave, no una tolerancia elegida por el generador. Las afirmaciones factuales requieren una calificación externa de cada átomo. Se rechazan revisiones incompletas; una afirmación contradictoria no se oculta por añadir una abstención. Las tres repeticiones se resumen dentro de cada caso y después los 30 casos con igual peso. El módulo de acuerdo registra salidas y átomos, porcentaje de acuerdo previo a adjudicar y kappa si es calculable; no trata los átomos de una misma salida como muestras independientes. La repetición intraevaluador exige al menos siete días.

### Punto metodológico que debe resolverse antes de generar

Los casos con denominador cero o sin cifras verificables producen una tasa numérica no definida. El evaluador implementa una política primaria conservadora: si un caso queda sin tasa, el macro completo conserva NA y el dictamen resulta no concluyente; además muestra resúmenes condicionales como diagnóstico, sin usarlos para respaldar H4. La clave actual tiene 12 casos sin valor numérico esperado: abstenerse correctamente puede dejar esos denominadores nulos. Por eso hay que revisar **antes** de las salidas cómo se agregan las tasas no aplicables y documentarlo en el protocolo. No se transforman los NA en cero ni se elige una política después de observar resultados.

## Lo que falta para las ejecuciones reales

H3: cerrar H1 y datos elegibles, declarar la adaptación ECOD, fijar variables/ventana en desarrollo y ejecutar los puntajes y la caracterización histórica. H4: revisión humana de 30 claves y de la política de tasas; proveedor real, modelo/versión/parámetros congelados; corpus/embeddings/recuperación verificados; 180 generaciones reales; calificación ciega y segunda revisión. No se marcaron claves como revisadas por una persona ni se simularon sus calificaciones.

La inspección de servicios quedó en `runtime-readiness.json`: no había modelo Ollama disponible y Docker no respondía. Se intentó iniciar Docker Desktop en segundo plano; eso no acredita un PostgreSQL/pgvector operativo. No se usó la credencial antigua ni se realizó gasto de API.

```powershell
./data/runtime-research-clean/Scripts/python.exe -B tools/advance_h3_h4.py
./data/runtime-research-clean/Scripts/python.exe -B tools/verify_h3_h4.py
./data/runtime-research-clean/Scripts/python.exe -B -m pytest tests/unit/test_h3_engine.py tests/unit/test_h4_execution.py -q
```

Los artefactos históricos y el catálogo H4 original permanecen intactos. Los resultados de esta carpeta están separados y se identifican como artificiales en sus manifiestos.

Los motores nuevos todavía no están conectados a las rutas de la UI/API. La interfaz conserva el piloto anterior y no presenta estos fixtures como resultados históricos o informes reales de H4. El verificador independiente recalcula presupuestos, persistencia desde observaciones artificiales guardadas, q/r/u, solapamientos e integridad de los paquetes sin importar el productor.
