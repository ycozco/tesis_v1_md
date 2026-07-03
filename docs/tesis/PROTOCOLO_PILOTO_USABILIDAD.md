# Anexo A: Protocolo Metodológico del Piloto de Usabilidad (HCI)

Este documento describe el diseño experimental, la guía de tareas y los cuestionarios estandarizados de usabilidad para el experimento intra-sujetos (*within-subjects*) del prototipo **Agro-Intelligence Oversight**.

---

## 1. Diseño de la Investigación Experimental

El objetivo del experimento es contrastar las métricas cognitivas y operativas de los auditores bajo dos condiciones de interfaz diferenciadas:

*   **Condición A (INTEGRADO):** Visualización de la DAM aduanera + score del ensemble + explicaciones locales (TreeSHAP) + reporte narrativo asistido (LLM-RAG).
*   **Condición B (AISLADO):** Visualización únicamente de los datos numéricos tabulares crudos de la DAM aduanera y el score del ensemble, sin explicaciones locales ni reporte RAG.

### 1.1. Variables de Estudio
*   **Variables Independientes (VI):** Nivel de explicabilidad de la interfaz (INTEGRADO vs. AISLADO).
*   **Variables Dependientes (VD):**
    *   **Latencia Cognitiva ($VD_1$):** Tiempo total empleado por transacción hasta emitir el veredicto final (`time_to_decision_ms`).
    *   **Comprensión Subjetiva ($VD_2$):** Escala Likert de 1 a 5 estrellas reportada al final de cada decisión (`likert_comprehension`).
    *   **Exactitud Decisional ($VD_3$):** Correspondencia entre la decisión del auditor (0=Falsa alarma, 1=Anomalía, 2=Inspección) y la etiqueta real de anomalía (FPR, Recall).

### 1.2. Muestra Experimental
*   **Sujetos de Estudio:** $N = 10$ evaluadores seleccionados con perfil técnico (Ingeniería de Sistemas, Logística o Comercio Exterior).
*   **Control del Efecto de Aprendizaje (Contrabalanceo):** Para evitar que el auditor recuerde las alertas al cambiar de interfaz, el orden de las sesiones se asigna aleatoriamente en el inicio de sesión (`Login.jsx`).

---

## 2. Guía de Ejecución de Tareas del Piloto

Cada auditor completará la prueba siguiendo este procedimiento:

```
[Inicio de Sesión] ──▶ [Asignación de Condición] ──▶ [Adjudicación de 5 Alertas] ──▶ [Llenar Cuestionario SUS]
```

### Paso 1: Introducción y Consentimiento
El moderador explica el propósito de la herramienta (asistente de detección de desvíos financieros aduaneros). Se solicita al participante leer y autorizar el registro anónimo de sus tiempos de respuesta.

### Paso 2: Fase de Familiarización
El participante realiza una prueba rápida con una alerta de entrenamiento para familiarizarse con la navegación y los botones de adjudicación.

### Paso 3: Sesión Experimental
El participante ingresa con sus credenciales semilla y evalúa la lista de alertas. Para cada alerta prioritaria:
1.  Inspecciona los parámetros operativos declarados de la DAM.
2.  Evalúa los factores de desvío (explicabilidad SHAP y citas normativas RAG si está en **Condición A**; o datos tabulares secos si está en **Condición B**).
3.  Registra su adjudicación: *Falsa Alarma*, *Anomalía Confirmada* o *Requiere Inspección*.
4.  Escribe una justificación breve (máximo 250 caracteres).
5.  Califica su nivel de comprensión de la alerta de 1 a 5 estrellas.

---

## 3. Cuestionario Estandarizado SUS (System Usability Scale)

Al finalizar la sesión, el auditor evaluador responderá el cuestionario **SUS (ISO 9241-11)** compuesto por 10 ítems calificados en una escala Likert de 1 (Totalmente en desacuerdo) a 5 (Totalmente de acuerdo):

| Ítem | Declaración Cuestionario SUS | Escala (1 - 5) |
| :---: | :--- | :---: |
| **S1** | Creo que me gustaría utilizar este sistema con frecuencia en mi labor diaria. | `[1] [2] [3] [4] [5]` |
| **S2** | Encontré el sistema innecesariamente complejo. | `[1] [2] [3] [4] [5]` |
| **S3** | Pensé que el sistema era fácil de usar. | `[1] [2] [3] [4] [5]` |
| **S4** | Creo que necesitaría el soporte de un analista técnico para poder usar este sistema. | `[1] [2] [3] [4] [5]` |
| **S5** | Encontré que las diversas funciones de este sistema estaban bien integradas. | `[1] [2] [3] [4] [5]` |
| **S6** | Pensé que había demasiada inconsistencia en este sistema. | `[1] [2] [3] [4] [5]` |
| **S7** | Imagino que la mayoría de los auditores aprenderían a usar este sistema muy rápidamente. | `[1] [2] [3] [4] [5]` |
| **S8** | Encontré el sistema muy engorroso/incómodo de usar. | `[1] [2] [3] [4] [5]` |
| **S9** | Me sentí muy seguro al utilizar el sistema en mis decisiones. | `[1] [2] [3] [4] [5]` |
| **S10** | Necesité aprender muchas cosas antes de poder seguir adelante con este sistema. | `[1] [2] [3] [4] [5]` |

### Fórmula de Puntuación SUS:
Para obtener el Score Final SUS (escala 0 a 100):
1.  Para preguntas impares (positivas: S1, S3, S5, S7, S9), restar 1 del puntaje de respuesta: $x_i = R_i - 1$.
2.  Para preguntas pares (negativas: S2, S4, S6, S8, S10), restar el puntaje de respuesta de 5: $x_i = 5 - R_i$.
3.  Sumar los 10 valores resultantes y multiplicar por 2.5:

$$\text{Puntuación SUS} = 2.5 \times \sum_{i=1}^{10} x_i$$

*Criterio de Aceptación Académica:* Un puntaje promedio de **SUS > 70** califica al sistema como usable y aceptable para su despliegue operativo en la administración aduanera.

---

## 4. Script de Análisis Estadístico para Contraste de Hipótesis

Una vez finalizado el experimento con los 10 auditores, se puede ejecutar el siguiente bloque de código en Python para verificar si las diferencias observadas son estadísticamente significativas:

```python
import sqlite3
import pandas as pd
import numpy as np
from scipy.stats import shapiro, ttest_rel, wilcoxon

# 1. Cargar la telemetría grabada de usabilidad
conn = sqlite3.connect('sistema-web-agro/agro_audit.db')
query = """
SELECT id_alerta, condicion_experimento, time_to_decision_ms, likert_comprehension 
FROM DecisionesAuditoria
"""
df = pd.read_csv(conn, sql=query)
conn.close()

# 2. Pivotar por alerta para obtener diferencias de pares
df_pivot = df.pivot(index='id_alerta', columns='condicion_experimento', values=['time_to_decision_ms', 'likert_comprehension'])
df_pivot = df_pivot.dropna()

tiempos_a = df_pivot['time_to_decision_ms']['INTEGRADO'] / 1000.0 # en segundos
tiempos_b = df_pivot['time_to_decision_ms']['AISLADO'] / 1000.0

# 3. Validar normalidad de las diferencias de tiempos logarítmicos
diff_log_time = np.log(tiempos_a) - np.log(tiempos_b)
w_stat, p_norm = shapiro(diff_log_time)

print(f"Normalidad de Shapiro-Wilk (p): {p_norm:.4f}")

if p_norm > 0.05:
    # 4. Prueba paramétrica t-Student Relacionada
    t_stat, p_value = ttest_rel(np.log(tiempos_a), np.log(tiempos_b))
    print(f"Prueba t-Student apareada sobre tiempos logarítmicos:")
    print(f"  t-estadístico: {t_stat:.4f}, p-valor: {p_value:.6f}")
else:
    # 4. Prueba no paramétrica de rangos de Wilcoxon
    stat, p_value = wilcoxon(tiempos_a, tiempos_b)
    print(f"Prueba de Wilcoxon apareada sobre tiempos:")
    print(f"  Estadístico W: {stat:.4f}, p-valor: {p_value:.6f}")

if p_value < 0.05:
    print("Resultado: Diferencia ESTADÍSTICAMENTE SIGNIFICATIVA (Se rechaza H0)")
else:
    print("Resultado: Diferencia NO SIGNIFICATIVA (No se rechaza H0)")
```
