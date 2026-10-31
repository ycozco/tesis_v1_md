# Resolución operativa documentada de conflictos

Versión: seleccion-heuristica-observada-1.0. Ejecución: 31 de octubre de 2026.

**Las elecciones son supuestos analíticos explícitos, no rectificaciones ni confirmaciones de SUNAT.** Se eligieron filas completas ya publicadas en los DBF; no se inventó un FOB, no se mezcló el peso de una variante con el FOB de otra y no se modificaron los originales. La vista conservadora y la cuarentena permanecen disponibles para contraste.

## Resultado

- Base conservadora: 93225 series.
- Conflictos resueltos operativamente: 28 series de 25 declaraciones.
- Series vecinas sin conflicto propio reincorporadas: 45.
- Vista analítica resultante: 93298 series (palta 38579; uva 27287; arándano 27432).
- Todos los casos utilizaron el mismo producto y destino con referencias de los últimos 90 días. No se aplicaron desempates por hash ni falta de referencias.
- El verificador independiente confirmó selección, referencias, valores de origen y sensibilidad.

## Sustento documental y alcance de cada documento

| Documento | Qué respalda | Qué NO respalda |
|---|---|---|
| SUNAT, DESPA-PG.02, versión 7, apartado de rectificaciones | El FOB y otros datos declarados pueden rectificarse; un importe mayor no tiene prioridad automática. | No identifica la variante correcta de estos 28 casos ni autoriza elegirla mediante una mediana. |
| NIST/SEMATECH, EDA 1.3.5.1, Measures of Location | La mediana es una referencia central menos sensible que la media a valores extremos. | No certifica registros aduaneros ni impone ventanas de 90 días o un mínimo de 20 referencias. |
| W3C, PROV-DM, 2.1.2 y 5.3 | Vincular el dato derivado con entradas y actividad que lo produjo permite documentar su procedencia. | La trazabilidad no demuestra que la elección sea verdadera; tampoco se declara una implementación completa de PROV. |

Fuentes primarias y copias descargadas con SHA-256:

- [SUNAT DESPA-PG.02](https://www.sunat.gob.pe/legislacion/procedim/despacho/exportacion/exportac/procGeneral/despa-pg.02.htm) — copia [sunat.html](documentos/sunat.html).
- [NIST, Measures of Location](https://itl.nist.gov/div898/handbook/eda/section3/eda351.htm) — copia [nist.html](documentos/nist.html).
- [W3C, PROV-DM](https://www.w3.org/TR/prov-dm/) — copia [w3c.html](documentos/w3c.html).
- Manifiesto de consulta y hashes: [fuentes.json](documentos/fuentes.json).

Las referencias documentan fundamentos generales; la regla concreta siguiente es una decisión de diseño propia. No se atribuye a esas instituciones la aprobación de los valores elegidos.

## Regla fijada y ejecutada

1. Se conserva la conciliación anterior por último paquete disponible de cada declaración. Solo se actúa sobre las 28 series contradictorias de ese último paquete; no se vuelve a una versión antigua por resultar más conveniente.
2. Cada candidato es una fila analítica original completa. Las repeticiones exactas de una variante no le otorgan votos: copias repetidas no son evidencia independiente.
3. Se usa como referencia la base conservadora sin declaraciones bloqueadas. Se toman registros de igual producto y destino con FOB y peso positivos, desde 90 días antes hasta la fecha de embarque del caso, incluidos ambos extremos. No se incorporan fechas de embarque posteriores ni otros destinos.
4. Se exige un mínimo operativo de 20 referencias. Si no se cumple, se amplía a 365 días conservando producto/destino. Esos parámetros son elecciones de diseño, no umbrales de significación estadística. Ningún caso necesitó esa ampliación.
5. Para cada referencia se calcula log(FOB/peso). El centro es su mediana. La distancia de una variante es el valor absoluto de la diferencia entre su log(FOB/peso) y ese centro. Se elige la variante con menor distancia; así se compara cercanía relativa a una referencia robusta y se conserva un valor observado.
6. La selección no usa resultados de modelos ni métricas del test. Si hay empate a tolerancia 1e-12 se prevé elegir por huella SHA-256, expresamente como desempate arbitrario reproducible, sin evidencia adicional. Si no hay referencias suficientes se prevé también un desempate técnico marcado. Ninguna de estas excepciones se utilizó.
7. Las 45 series sin contradicción propia de las declaraciones afectadas conservan su única variante observada.
8. Se guardan todas las alternativas, distancias, medianas, referencias utilizadas, fuente/fila y decisión. Los importes y pesos agregados de sensibilidad se suman con Decimal para evitar errores de redondeo binario.

El atributo decision conserva la decisión histórica de cuarentena; resolucion_analitica describe el tratamiento nuevo. No se debe borrar esa historia ni interpretar confirmacion_oficial=no como confirmación por terceros.

## Justificación y límites de la elección

La regla permite disponer de una única variante por serie sin crear valores intermedios. Se prefiere a elegir sistemáticamente el FOB mayor o menor, o asumir que la última fila representa una rectificación, porque esas opciones no tienen respaldo temporal dentro del paquete. La mediana proporciona un criterio uniforme de plausibilidad contextual, no un documento probatorio de la operación.

Elegir la variante más típica puede reducir artificialmente la dispersión y ocultar una operación extraordinaria verdadera. También existen diferencias de calidad/variedad que el agregado no controla. La base de referencia es retrospectiva y puede contener revisiones conocidas después del embarque: usar solo fechas de embarque anteriores NO acredita disponibilidad en tiempo real ni ausencia de fuga. Estas limitaciones se deben conservar en la tesis y al evaluar H1-H3.

Para resultados científicos deben compararse al menos la vista conservadora y esta selección analítica bajo reglas fijadas antes del test. Una mejora predictiva no convierte la elección en verdad oficial. La confirmación de una variante exigiría la rectificación o documentos de la operación correspondientes.

## Fichas de las 28 decisiones

Cada fila resume una decisión; los hashes completos y todas las referencias están en los CSV. Los puntajes son distancias al centro, NO probabilidades de corrección.

| Caso (hash abreviado) | Producto / destino | FOB elegido USD | Peso elegido kg | Referencias | Mediana FOB/kg aproximada | Alternativas FOB/peso y distancia | Justificación |
|---|---|---:|---:|---:|---:|---|---|
| 06db9414d1d4 | palta / NL | 6696.000 | 3600.000 | 2369 | 2.024726 | 6696.000/3600.000: 0.084858 (elegida); 30000.000/2400.000: 1.820294 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 1111f99a3fce | palta / ES | 4176.000 | 2400.000 | 1581 | 2.250000 | 4176.000/2400.000: 0.257045 (elegida); 20000.000/2400.000: 1.309333 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 14b16f902f2f | palta / NL | 30000.000 | 12000.000 | 4637 | 1.945596 | 33000.000/12000.000: 0.346033; 30000.000/12000.000: 0.250722 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 1f96e79b1920 | palta / US | 4875.600 | 2891.700 | 3740 | 1.819783 | 10547.200/7257.600: 0.224906; 4875.600/2891.700: 0.076319 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 2466d9d028a8 | arandano / US | 8689.070 | 1423.920 | 924 | 8.729161 | 5000.000/3488.400: 1.806674; 8689.070/1423.920: 0.358017 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 2530b891ab2d | arandano / NL | 31872.620 | 3920.000 | 2875 | 8.621908 | 31872.620/3920.000: 0.058651 (elegida); 10000.000/3920.000: 1.217813 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 2badb9d18dca | arandano / GB | 44216.420 | 6255.000 | 24 | 7.058073 | 40657.500/6255.000: 0.082370; 44216.420/6255.000: 0.001543 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 344a544a150d | arandano / US | 70000.000 | 11444.400 | 1327 | 5.089189 | 70000.000/11444.400: 0.183876 (elegida); 38040.450/10208.160: 0.311656 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 53fc10a38db4 | palta / CN | 9634.000 | 4940.000 | 1086 | 1.919356 | 9634.000/4940.000: 0.015943 (elegida); 7106.779/4940.000: 0.288306 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 7a8e0a4ca7d0 | arandano / US | 60679.090 | 6816.720 | 2623 | 7.740719 | 10000.000/5006.640: 1.354674; 60679.090/6816.720: 0.139726 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 822299080820 | arandano / CN | 15000.000 | 1755.000 | 117 | 9.000000 | 15000.000/1755.000: 0.051643 (elegida); 25740.000/4680.000: 0.492476 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 8473bb12229a | palta / NL | 12120.000 | 4840.000 | 462 | 2.350000 | 10000.000/11500.000: 0.994177; 12120.000/4840.000: 0.063527 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 90e3039a4f3f | uva / NL | 15000.000 | 7000.000 | 1253 | 2.449856 | 15000.000/7000.000: 0.133889 (elegida); 830.370/600.000: 0.571087 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| 9bc259aa90f4 | arandano / US | 50937.650 | 5696.640 | 2623 | 7.740719 | 10000.000/7506.720: 1.759708; 50937.650/5696.640: 0.144231 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| a4b3380d6a38 | arandano / US | 21750.070 | 2448.000 | 561 | 10.010695 | 32166.000/3672.000: 0.133481; 21750.070/2448.000: 0.119308 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| a53f3c0eec53 | uva / MX | 20000.000 | 8364.000 | 79 | 2.195122 | 20000.000/8364.000: 0.085558 (elegida); 25080.000/8322.000: 0.316931 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| aa3041d26f3e | palta / ES | 6762.000 | 3600.000 | 1051 | 2.313823 | 30000.000/3600.000: 1.281363; 6762.000/3600.000: 0.208516 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| aa9589dfc188 | palta / US | 10547.200 | 7344.000 | 3740 | 1.819783 | 5297.400/3717.900: 0.244660; 10547.200/7344.000: 0.236741 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| b0f016641c99 | palta / US | 21195.760 | 13460.580 | 3740 | 1.819783 | 21195.760/13460.580: 0.144682 (elegida); 10547.200/7257.600: 0.224906 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| b23cb448c2f1 | palta / NL | 10942.000 | 6000.000 | 1142 | 2.202304 | 10942.000/6000.000: 0.188655 (elegida); 30000.000/6000.000: 0.819934 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| c0928cc3b262 | arandano / US | 20808.000 | 4161.600 | 1302 | 5.117431 | 20808.000/4161.600: 0.023215 (elegida); 15000.000/832.320: 1.258936 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| d0fb41a56c69 | arandano / US | 14320.800 | 1909.440 | 4479 | 7.884882 | 20000.000/1909.440: 0.283975; 14320.800/1909.440: 0.050044 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| d10055762f2e | palta / US | 10547.200 | 7344.000 | 3740 | 1.819783 | 25222.600/17702.100: 0.244660; 10547.200/7344.000: 0.236741 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| dc3eab855eed | uva / NL | 12943.521 | 5400.000 | 1517 | 2.482537 | 15000.000/5333.000: 0.124855; 12943.521/5400.000: 0.035085 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| dedb44e8fb39 | palta / US | 10547.200 | 7344.000 | 3740 | 1.819783 | 10547.200/7344.000: 0.236741 (elegida); 18813.400/13203.900: 0.244660 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| e0f09d44de81 | arandano / GB | 31550.770 | 4803.000 | 24 | 7.058073 | 28818.000/4803.000: 0.162413; 31550.770/4803.000: 0.071815 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| e702d12ba722 | palta / US | 32120.660 | 15796.620 | 3740 | 1.819783 | 32120.660/15796.620: 0.110986 (elegida); 10547.200/7257.600: 0.224906 | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |
| f7e4bd2682d6 | arandano / US | 23500.800 | 3133.440 | 4479 | 7.884882 | 20000.000/3133.440: 0.211346; 23500.800/3133.440: 0.050044 (elegida) | Menor distancia con el mismo criterio NIST + diseño propio; no confirmada oficialmente. |

## Sensibilidad a las alternativas

Se calcula una envolvente por producto para FOB y peso, manteniendo fijas las 93225 series conservadoras y las series restauradas sin conflicto propio. Para cada variable se suman por separado sus mínimos y máximos observados en las variantes. No son intervalos de confianza, totales oficiales ni un único escenario conjunto: el mínimo FOB y el mínimo peso pueden proceder de filas distintas. Los totales pertenecen solo a esta colección incompleta.

| Producto | Variable | Selección analítica | Mínimo observado | Máximo observado | Amplitud relativa % |
|---|---|---:|---:|---:|---:|
| arandano | valor_fob_usd | 2059628625.604 | 2059463887.134 | 2059655460.734 | 0.009301 |
| arandano | peso_neto_kg | 270402774.276 | 270396398.676 | 270410797.836 | 0.005325 |
| palta | valor_fob_usd | 1166759801.164 | 1166717682.123 | 1166872838.364 | 0.013298 |
| palta | peso_neto_kg | 599545261.194 | 599525693.094 | 599572505.094 | 0.007808 |
| uva | valor_fob_usd | 1078124356.416 | 1078110186.786 | 1078131492.895 | 0.001976 |
| uva | peso_neto_kg | 376314118.845 | 376307609.845 | 376314118.845 | 0.001730 |

La amplitud agregada FOB es inferior a 0.014 % por producto en esta colección. Esto no demuestra que cada operación sea correcta: algunas alternativas individuales son muy distintas y sus efectos locales pueden ser relevantes.

## Reproducción y auditoría

Desde la raíz del repositorio:

    python -B tools/resolve_sunat_conflicts.py .
    python -B tools/verify_sunat_resolution.py .

Se usó Python con biblioteca estándar. El script y sus entradas tienen hashes en resumen.json. El verificador relee la selección, reconstruye medianas con las referencias guardadas, comprueba la opción ganadora y los totales de sensibilidad con aritmética decimal. Comprueba también que las entradas conservadoras y la cuarentena no se hayan modificado.

Archivos: vista-resuelta-analitica.csv; decisiones-resolucion.csv; alternativas.csv; referencias-por-caso.csv; sensibilidad.csv; resumen.json. No se entrenaron modelos ni se modificó la vista conservadora.
