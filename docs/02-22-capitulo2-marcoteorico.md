# MARCO CONCEPTUAL

## 2.3 Marco Conceptual

### 2.3.1 Operación Agroexportadora
Transacción comercial de exportación de bienes agrícolas perecederos, regulada por la SUNAT, que abarca variables de volumen (peso neto, peso bruto), valor comercial aduanero (FOB), subpartida arancelaria a 10 dígitos (HS code), país de destino y exportador (RUC).

### 2.3.2 Supervisión Analítica
Proceso de auditoría interna y monitoreo de las operaciones de comercio exterior orientado a identificar desviaciones operativas, comerciales o aduaneras, comparando los registros reales contra líneas base o comportamientos esperados.

### 2.3.3 Valor Unitario FOB de Exportación
Indicador comercial derivado que mide el valor promedio obtenido por kilogramo de producto FOB declarado en la aduana de salida:
$$\text{fob\_unit\_value\_usd\_kg} = \frac{\text{total\_fob\_usd}}{\text{total\_net\_weight\_kg}}$$
No equivale conceptualmente al precio internacional de venta minorista en destino, puesto que incorpora costos locales, empaque y contratos aduaneros prefijados.

### 2.3.4 Granularidad Temporal Semanal
Nivel de agregación cronológica adoptado en el dataset analítico, estructurado a nivel de producto × mercado × semana ISO (lunes a domingo), garantizando que las micro-transacciones individuales de SUNAT se acumulen semanalmente para coincidir con la frecuencia de actualización de variables de mercado y climáticas.

### 2.3.5 Data Leakage (Fuga de Información)
Fallo metodológico en el entrenamiento de modelos de series temporales en el cual información del futuro ($t+1$ o posterior) se filtra hacia el conjunto de características del pasado ($t$). Se previene implementando un desplazamiento temporal estricto (`shift(1)`) en todas las rolling windows e imputaciones exógenas.

### 2.3.6 Gradient Boosting Decision Trees (GBDT)
Familia de algoritmos de aprendizaje automático supervisado que optimizan de forma secuencial una función de pérdida agregando árboles de decisión para corregir los residuos de predicción previos mediante descenso de gradiente. Algoritmos principales: XGBoost y LightGBM.

### 2.3.7 Residuo Predictivo Robust-Z
Desviación del valor real observado en $t+1$ respecto de la estimación del modelo predictivo, normalizado de forma robusta utilizando la mediana y la MAD (Desviación Absoluta de la Mediana) de una ventana móvil de 13 semanas por serie temporal para capturar anomalías genuinas aisladas del ruido estacional.

### 2.3.8 Ensemble no Supervisado PyOD
Modelo unificado compuesto por Isolation Forest, Local Outlier Factor (LOF) y ECOD (Empirical Cumulative Distribution Outlier Detection). Sus scores individuales se unifican mediante escalamiento Min-Max calibrado en entrenamiento, calculando el score final del ensemble como el promedio simple de los percentiles de anomalía.

### 2.3.9 Explicabilidad Local Post-Hoc con SHAP
Método de atribución local basado en la teoría de juegos cooperativos que calcula los valores de Shapley para medir el impacto marginal cuantitativo (atribución) de cada variable predictora en la desviación de la estimación del modelo respecto de su valor esperado promedio.

### 2.3.10 Retrieval-Augmented Generation (RAG)
Arquitectura de procesamiento de lenguaje natural que inyecta contexto documental e histórico verificado (recuperado de una base de conocimiento mediante búsqueda híbrida BM25 y embeddings) directamente en el prompt del LLM para restringir la redacción narrativa del reporte y evitar alucinaciones extrínsecas.

### 2.3.11 Trazabilidad de Modelos y Linaje de Datos
Capacidad de documentar y reconstruir de extremo a extremo el flujo de procesamiento de una alerta. Se garantiza mediante el registro inmutable de metadatos de configuración, identificadores UUIDv4 para cada fase y hashes SHA-256 de los datasets y modelos entrenados.