# Criterios de Severidad de Alertas y Gobernanza Algorítmica

Este documento detalla las reglas de gobernanza y la determinación de la severidad de las alertas de anomalías en el sistema.

## Niveles de Severidad de Alertas
La severidad de una alerta se determina dinámicamente según la puntuación consolidada del ensemble de anomalías ($S_{Ensemble}$):

1. **Severidad Alta (Crítica)**: 
   * Se activa cuando la puntuación del ensemble es $\ge 0.99$.
   * Indica una desviación multivariable extrema en el 1% superior del histórico de observaciones.
   * Requiere auditoría operativa inmediata y revisión del lote por parte del supervisor de exportación.

2. **Severidad Media (Advertencia)**:
   * Se activa cuando la puntuación del ensemble se encuentra en el rango $[0.975, 0.99)$.
   * Indica desviaciones moderadas pero consistentes en variables críticas (ej. caída simultánea de volumen y precios atípicos).
   * Requiere seguimiento semanal y control preventivo.

3. **Severidad Baja (Informativa)**:
   * Se activa cuando la puntuación del ensemble está en el rango $[0.95, 0.975)$ o cuando se cumple la regla de votos $\ge 2$.
   * Indica una desviación leve en alguna variable contextual o climática que no compromete críticamente la operación.
   * Sirve para el registro histórico y análisis de tendencias.

## Principios de Gobernanza (D.S. N.° 115-2025-PCM y NIST AI RMF)
* **Supervisión Humana Obligatoria (Human-in-the-loop)**: El sistema nunca toma decisiones automáticas de rechazo, cobro o sanción. Funciona exclusivamente como un visor de apoyo para el analista humano.
* **Explicabilidad Mandatoria**: Cada informe de alerta debe ir acompañado de sus atribuciones SHAP correspondientes para justificar matemáticamente la clasificación.
* **Trazabilidad Documental**: Toda alerta generada y reporte redactado se registra con un código único (UUID) y un hash SHA-256 de integridad para evitar la alteración de los registros de auditoría.
