# ANEXOS

## Anexo A — Protocolo de Evaluación de Usabilidad

> **Versión 1.0 — 2026-05-17.** Aprobar antes de iniciar reclutamiento de participantes.

### A.1 Objetivo del experimento

El experimento de usabilidad mide el impacto del sistema integrado de supervisión operativa en la **eficiencia (VD4 — tiempo-a-decisión)**, **comprensión (VD4 — Likert)** y **trazabilidad documental (VD5)** frente al uso de componentes aislados. Constituye la fuente principal de evidencia para contrastar las sub-hipótesis H1b y H1d (Capítulo I §1.4).

### A.2 Diseño experimental

**Tipo**: Cuasi-experimental con diseño within-subjects (apareado) y orden contrabalanceado.

Cada participante ejecuta las mismas tareas en dos condiciones:
- **Condición A — Sistema integrado**: pipeline de 4 capas con alerta + score + vector SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley) top-5 + reporte LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)+RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación).
- **Condición B — Componentes aislados**: alerta + score crudo del detector, sin SHAP, sin reporte narrativo (solo tabla y visualización técnica).

La mitad de los participantes inicia con A y la otra mitad con B, asignación aleatorizada con `np.random.seed(42)`. Entre ambas condiciones se intercala un descanso de 5 minutos y una tarea distractora (sopa de letras) para reducir efectos de arrastre.

### A.3 Tareas evaluadas

Cada condición presenta el mismo bloque de 10 alertas (5 positivas reales, 3 negativas reales, 2 ambiguas) extraídas del conjunto de test del dataset sintético. Para cada alerta, el participante:

1. **Tarea T1 — Clasificación**: decide si la alerta corresponde a una anomalía operativa real (sí/no/dudoso).
2. **Tarea T2 — Justificación**: en una oración (máx. 200 caracteres) indica la variable que justifica la decisión.
3. **Tarea T3 — Comprensión**: responde Likert 1–5 sobre cuán comprensible resultó la alerta.

Al finalizar el bloque de 10 alertas, completa un cuestionario post-bloque (SUS adaptado + preguntas abiertas).

### A.4 Métricas registradas automáticamente

| Métrica | Fuente | Resolución |
|---|---|---|
| Tiempo apertura alerta → decisión | Log JavaScript de la plataforma | milisegundos |
| Tiempo total bloque | Log JavaScript | segundos |
| Clasificación del participante | Formulario | sí / no / dudoso |
| Justificación textual | Formulario | texto libre |
| Likert comprensión | Formulario | 1–5 |
| Versión del sistema | Variable de configuración | string |
| Identificador de alerta | Variable | string |

### A.5 Criterios de inclusión y exclusión de participantes

**Inclusión**:
- (a) Estudiantes de últimos ciclos (≥ 9° semestre) o egresados de Ingeniería de Sistemas, Ingeniería Industrial o Agronomía con formación comprobada en logística, control de calidad o auditoría de sistemas; o
- (b) Profesionales y técnicos con experiencia en supervisión de operaciones, control de calidad, auditoría de sistemas o gestión logística en el sector agroexportador.
- Mayores de 18 años.
- Aceptación de consentimiento informado firmado.

**Exclusión**:
- Participación previa en el diseño, desarrollo o entrenamiento de cualquier capa del sistema evaluado.
- Conflicto de interés directo declarado.
- Discapacidad visual no corregible que impida la lectura del dashboard.

### A.6 Tamaño de muestra y reclutamiento

**Tamaño meta**: N = 10 participantes (documentar formalmente como un estudio piloto especializado de usabilidad). Un tamaño N = 10 permite una evaluación detallada de la eficiencia temporal y cualitativa sin pretensiones de generalización estadística a gran escala, pero con alta representatividad técnica.

**Reclutamiento**: El estudio se limita a **grupos cerrados de testers con conocimiento especializado en el área** bajo invitación directa (no abierta al público general). La convocatoria se realiza por invitación formal a través de la Escuela de Ingeniería de Sistemas de la UNSA y contactos en empresas agroexportadoras de Arequipa, Ica y La Libertad coordinadas por el asesor, garantizando el perfil técnico de los evaluadores.

### A.7 Procedimiento detallado (sesión por participante, ~45 minutos)

| Paso | Duración | Contenido |
|---|---|---|
| 1 | 5 min | Bienvenida + consentimiento informado firmado |
| 2 | 5 min | Tutorial guiado de la plataforma (alerta de ejemplo) |
| 3 | 12 min | Bloque 1 — Condición A o B (según contrabalanceo) |
| 4 | 5 min | Descanso + tarea distractora |
| 5 | 12 min | Bloque 2 — Condición contraria |
| 6 | 5 min | Cuestionario final SUS + preguntas abiertas |
| 7 | 1 min | Cierre + agradecimiento |

### A.8 Consentimiento informado (texto base)

```
Por la presente confirmo que:
1. He sido informado sobre el propósito del estudio: evaluar la usabilidad de
   un sistema de supervisión operativa con IA explicable.
2. Comprendo que mi participación es voluntaria y puedo retirarme en cualquier
   momento sin justificación ni consecuencia.
3. Comprendo que mis respuestas son anónimas. Solo el investigador principal
   accederá a los datos, que se almacenarán cifrados y se eliminarán al
   finalizar la tesis (julio 2027).
4. Acepto que se registre el tiempo de mis respuestas y las opciones
   seleccionadas para análisis estadístico agregado.
5. Comprendo que no recibiré evaluación individual ni se compartirán mis
   resultados con terceros.
6. Acepto participar en una sesión de aproximadamente 45 minutos.

Nombre: ____________________  Fecha: __________  Firma: __________
```

### A.9 Cuestionario post-bloque

**Bloque I — Comprensión percibida (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Entendí claramente por qué el sistema marcó cada alerta | | | | | |
| 2 | La información presentada me ayudó a tomar una decisión | | | | | |
| 3 | Las variables explicativas fueron suficientes | | | | | |
| 4 | El reporte generado fue útil para justificar mi decisión | | | | | |
| 5 | Confío en la decisión del sistema | | | | | |

**Bloque II — Tiempo y carga cognitiva (Likert 1–5)**

| # | Ítem | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 6 | Me tomó mucho tiempo entender cada alerta (1) — Fui rápido (5) | | | | | |
| 7 | Tuve que esforzarme mucho mentalmente | | | | | |
| 8 | Me sentí seguro al decidir | | | | | |

**Bloque III — Adaptación SUS (10 ítems Likert 1–5)**

```
1. Creo que me gustaría usar este sistema frecuentemente.
2. Encontré el sistema innecesariamente complejo.
3. Pensé que el sistema fue fácil de usar.
4. Necesitaría el apoyo de un experto técnico para usar este sistema.
5. Las funciones del sistema están bien integradas.
6. Hay demasiada inconsistencia en este sistema.
7. La mayoría aprendería a usar este sistema rápidamente.
8. Encontré el sistema muy engorroso.
9. Me sentí muy confiado al usar el sistema.
10. Necesitaría aprender muchas cosas antes de usar el sistema.
```

**Bloque IV — Preguntas abiertas**

1. ¿Qué fue lo más útil del sistema en esta sesión?
2. ¿Qué información agregaría o quitaría?
3. ¿En qué situación operativa real este sistema sería más valioso?

### A.10 Variables registradas para análisis

| Variable | Tipo | Origen |
|---|---|---|
| `participant_id` | string anónimo | Generado |
| `order` | {AB, BA} | Aleatorización |
| `condition` | {integrated, isolated} | Variable independiente |
| `alert_id` | string | Dataset |
| `gt_label` | {0, 1} | Dataset (oculto al participante) |
| `user_decision` | {yes, no, dunno} | Formulario |
| `time_to_decision_ms` | int | Log JavaScript |
| `likert_comprehension` | 1–5 | Cuestionario |
| `justification_text` | string | Formulario |
| `sus_score` | 0–100 | Cálculo SUS |

### A.11 Plan de análisis estadístico

1. **Tiempo-a-decisión (VD4-a)**: t de Student apareado integrado vs. aislado; Wilcoxon si Shapiro-Wilk rechaza normalidad. Reportar media ± DE, IC95%, Cohen's dz.
2. **Comprensión Likert (VD4-b)**: Wilcoxon signed-rank apareado.
3. **Decisión correcta (VD4-c)**: McNemar sobre pares concordantes/discordantes.
4. **SUS**: comparación de medias con Mann-Whitney U.
5. **Análisis cualitativo de respuestas abiertas**: análisis temático con doble codificación independiente.

### A.12 Almacenamiento y privacidad de datos

- Datos almacenados en archivo CSV cifrado con clave conocida solo por el investigador.
- Identificadores anónimos, sin nombre, correo ni datos demográficos sensibles.
- Backup en disco duro institucional UNSA.
- Eliminación de datos crudos al cierre del proyecto (julio 2027).
- Resultados agregados publicados en la tesis y en el repositorio GitHub.

### A.13 Aprobación ética

El protocolo se somete a revisión del asesor de tesis (Dr. Víctor Manuel Cornejo Aparicio) y, si la Escuela de Ingeniería de Sistemas dispone de comité de ética, a su aprobación formal antes del reclutamiento.

---

*Anexo A — versión 1.0 — 2026-05-17. Sometido a revisión final antes de ejecutar el estudio.*
