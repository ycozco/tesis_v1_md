# Preprocesamiento de la colección ampliada

Versión independiente de los pilotos previos. Fuente: la vista conservadora de 101.546 registros conciliados de 24 paquetes. Las sumas y razones por producto, destino y semana se reconstruyeron y comprobaron contra la fuente con aritmética Decimal independiente.

Contiene 136 series y 20.154 posiciones semanales: 3.845 con operaciones recuperadas y 16.309 desconocidas. Una posición observada es parcial: no se afirma cobertura completa. Los huecos conservan NA y no se imputan a cero. No existen fechas certificadas de publicación histórica, por lo que `eligible_for_final_experiment` es falso para todas las filas. Son características retrospectivas para preparar el sistema, no datos declarados elegibles para una evaluación operativa.

Se conservan L=0/4/8 y el calendario provisional previo sin cambios. No se ajustaron modelos con estos datos ni se evaluaron errores del bloque final. El piloto de sensibilidad anterior pertenece a otra versión y no se mezcla con esta colección. Las columnas de rezagos conservan las reglas del piloto; las cuatro referencias y la selección final aún deben integrarse en el ejecutor científico.

```
python -B tools/build_expanded_research_data.py
python -B tools/verify_expanded_research_data.py
```

`manifest.json` identifica la fuente y las huellas de los cinco artefactos de datos. No se modifica la versión de datos servida actualmente por la UI sin reconstruir también su linaje.
