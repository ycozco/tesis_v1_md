# Checklist Maestro Verificable e Iterativo

## Estado base

- Linea base documental: `docs/tesis/tesis_reestructurada.md`
- Linea base de propuesta: `docs/tesis/CAPITULO_III_3_1_3_2.md`
- Pendientes y dudas: `docs/tesis/PENDIENTES_CONFIRMACION.md`
- Registro de cambios: `docs/tesis/CAMBIOS_REALIZADOS.md`
- PDF de contraste: `Tesis de Investigación YOSET 22-06.pdf`
- Texto extraido del PDF: `reports/tesis_pdf_22_06_extracted.txt`
- Compilados de referencia: `output/tesis.pdf`, `output/tesis.docx`, `output/tesis.html`, `output/tesis.log`, `output/tesis.tex`
- Rama base revisada: `main`
- Commit base revisado: `166bdf890125595ee04c0a7e72407c409b7e7383`
- Hash PDF 22-06: `56DE9F28F6F5671E2F679C7C24D1591B8EDCA64FABEAEADD3AC0CDCB3B116C89`
- Hash `output/tesis.pdf`: `3DE4CFD189C9641413B7B6ECE74FB74F00EF39356E50FD4571CC058A2AB6EDB9`

## Regla de validacion

Una actividad solo se considera completa cuando existe:

1. Archivo o evidencia localizada.
2. Comando o proceso reproducible.
3. Resultado verificable.
4. Correspondencia con un objetivo de tesis.
5. Texto, figura o tabla incorporada en el capitulo correspondiente.

Estados usados:

- `[ ]` No revisado.
- `[~]` Evidencia encontrada, pero falta cierre reproducible o incorporacion final.
- `[x]` Evidencia revisada y utilizable.
- `[P]` Pendiente por falta de evidencia o confirmacion externa.
- `[!]` Inconsistencia o contradiccion detectada.

## Control de avance

| ID | Actividad | Estado | Evidencia | Comando/proceso | Salida esperada | Observaciones |
|---|---|---|---|---|---|---|
| R-00 | Congelar estado base | [~] | `git status`, `git rev-parse HEAD`, hashes SHA-256 | Verificacion Git y `Get-FileHash` | Rama, commit y documentos base documentados | Falta version Python por fallo del launcher de Windows |
| R-01 | Revisar tesis reestructurada | [x] | `docs/tesis/tesis_reestructurada.md` | Lectura documental | Capitulos consolidados/parciales identificados | Tiene Cap. III avanzado y Cap. IV preliminar |
| R-02 | Contrastar Capitulo III base | [x] | `docs/tesis/CAPITULO_III_3_1_3_2.md` | Lectura documental | Brechas de implementacion y redaccion | Requiere ampliar 3.3-3.5 y alinear con prototipo |
| R-03 | Contrastar PDF base | [x] | `Tesis de Investigación YOSET 22-06.pdf`, `reports/tesis_pdf_22_06_extracted.txt` | `pdftotext -layout -nopgbrk` | Indice y secciones comparadas | PDF contiene portada generica y 3.3-3.5 incompletos |
| R-04 | Mapear cambios necesarios | [x] | `docs/tesis/CAMBIOS_REALIZADOS.md`, `docs/tesis/11-documento-maestro-correccion.md` | Lectura documental | Lista de ajustes priorizada | Documento maestro generado |
| R-05 | Verificar soporte tecnico | [~] | `src/module1_prediction.py` a `src/module6_traceability.py` | Revision de codigo | Algoritmos alineados con texto | Implementacion existe; falta registrar comandos y salidas reproducibles |
| R-06 | Verificar prototipo web | [~] | `sistema-web-agro/` | Revision de codigo y pantallas | Evidencia funcional del punto 4 | Funcional parcial; falta matriz de endpoints/vistas/pruebas |
| R-07 | Generar correccion maestra | [x] | `docs/tesis/11-documento-maestro-correccion.md` | Documento de correccion | Correcciones priorizadas y verificables | Nuevo documento rector |

## Criterio de terminado

- Capitulo I y II: consolidados y alineados con el PDF y el borrador vivo.
- Capitulo III: implementado en lo real, con partes parciales marcadas.
- Capitulo IV: solo resultados verificables, preliminares o explicitamente pendientes.
- Prototipo `sistema-web-agro`: documentado como evidencia funcional parcial del punto 4.
- Todo lo que no exista debe quedar como pendiente, no como supuesto.
