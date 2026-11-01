# Continuación — reglas H3 y catálogo controlado H4

## Publicación de la primera entrega

Tras autorización explícita del titular, el commit `ed103bc` fue enviado a `origin/main` y el [ZIP de 31.069.486 bytes](https://drive.google.com/file/d/1IiJFMPBHuq4svBmh0KB5wv3DCETA6FHp/view) fue publicado en la carpeta de Drive seleccionada. SHA-256 del ZIP: `5085841418aedfe04b69245ceee73e2d987be2ab8a15fe5faa055ccfc2595894`. Los metadatos de Drive confirman ID, tamaño y carpeta padre; no se afirma verificación remota del SHA-256. El estado pendiente que figura en `avance.md` describe el momento anterior a esta autorización y queda actualizado por esta nota. La carpeta tiene acceso del dominio UNSA y colaboradores; sus permisos no se modificaron.

## P08: reglas H3 implementadas, todavía sin integración final

Fundamento: sección 3.6.3–3.6.4 de la tesis, ancla T12. `pipeline/research/h3_rules.py` aplica la CDF empírica del entrenamiento por detector y su media simple; no utiliza rangos del lote evaluado. Convención explícita: proporción de puntuaciones de entrenamiento menores o iguales al nuevo score, con scores orientados de menor a mayor rareza. La función no acredita por sí sola que el llamador haya entrenado antes del caso; el runner deberá conservar y verificar fechas y ventanas.

El presupuesto es `max(1, ceil(0.05*N))` por producto, sobre el universo común entregado; empates por fecha y destino. La rúbrica retrospectiva usa w, w+1 y w+2 frente a w−52 y posteriores, cobertura comprobada, referencia positiva y cambios del mismo signo con magnitud mínima de 20 %. Sensibilidades prefijadas 10/20/30 %. Las dos últimas semanas del test son inelegibles. Se conservan q/r/u y límites por indeterminación; no se denominan intervalos de confianza ni exactitud comercial.

La colección ampliada tiene observaciones parciales sin certificados: no se transforma en etiquetas válidas por implementar esta función. Los scores y selecciones del piloto anterior permanecen intactos y no se presentan como ejecución de estas reglas corregidas.

## P11: 30 esquemas controlados preparados

Fundamento: sección 3.9.5.1, ancla T07. Nueva versión en `datasets/experimentos/h4-controlado-v1`, separada del histórico. Contiene 30 casos artificiales, sus claves, documentos artificiales y 180 turnos sin ejecutar. Cubre los diez esquemas por cada uno de los tres productos. La clave común se prepara antes de cualquier recuperación/generación y queda fuera de los payloads. Los dos brazos comparten la huella del mismo payload. Se explicitan casos donde la respuesta correcta es abstenerse y donde una razón parcial puede calcularse sin afirmar cobertura completa.

Pendientes: revisión humana de claves y regla de cobertura de abstenciones, configuración congelada del generador y RAG, runner pareado, evaluación ciega, agregación de tres repeticiones dentro de caso, y evaluación de los 30 casos con igual peso. No hay salidas generadas, costos de IA ni resultados de H4. No se atribuye aún cumplimiento total a P08 ni P11.

## Verificación

Las pruebas incluyen: CDF respecto al entrenamiento, presupuesto por producto y desempates, rúbrica con datos parciales y referencia cero, límites de indeterminación, 30 combinaciones producto–esquema, 180 turnos con payload pareado, claves de abstención, aritmética sin redondeo intermedio y rechazo del guard ante diseño alterado. La auditoría y el constructor H4 se pueden ejecutar en el entorno nuevo sin pip. El experimento final de pronóstico sigue sin ejecutarse por los requisitos de cobertura, disponibilidad y protocolo previamente documentados.
