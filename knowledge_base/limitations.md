# Limitaciones Metodológicas y Declaración de Proxies

Este documento establece el alcance científico, las suposiciones y las limitaciones de validez del sistema de supervisión.

## Declaración de Variables Proxy
Debido a que cierta información operativa no se encuentra disponible públicamente con granularidad transaccional (por contenedor o embarque), el sistema adopta las siguientes variables proxy:
1. **Días Logísticos**: Calculados a partir de los registros de la SUNAT mediante la diferencia en días entre la fecha de numeración de la DUA y la fecha de embarque efectivo.
2. **Costo Logístico**: Estimado a partir de tarifas portuarias de OSITRAN y APN ponderadas por el peso del embarque.
3. **Mermas**: Modeladas mediante distribuciones de probabilidad basadas en la perecibilidad teórica del cultivo, la temperatura promedio del trayecto y el tiempo en puerto.
4. **Cumplimiento Fitosanitario**: Proxy binario derivado de alertas históricas de rechazo por mercado de destino en bases de datos sanitarias (FDA, RASFF).

## Limitaciones de los Modelos y Alcance
* **No Causalidad**: El modelo TreeSHAP cuantifica la importancia de las variables en la predicción del modelo GBDT. No debe interpretarse como causalidad física ni económica real en el mercado.
* **Exclusión de Cultivos**: El cacao fue formalmente excluido de todo modelamiento y agregación debido a su baja representatividad transaccional (menos del 1% del volumen acumulado del histórico real).
* **Uso de Datos Sintéticos**: Las alertas reales se generan a partir del dataset real observador. La validación cuantitativa de la detección (PR-AUC, Recall) se realiza mediante un subconjunto experimental donde se inyectan anomalías sintéticas controladas, lo cual debe declararse explícitamente en la sustentación de la tesis para evitar la falsa afirmación de detección de anomalías 100% reales en el entrenamiento no supervisado.
* **Tolerancia en Reportes**: La validación factual de reportes opera con un margen de tolerancia del 0.5% para diferencias de redondeo matemático.
