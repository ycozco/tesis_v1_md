# Corrida técnica artificial — 2 de noviembre de 2026

Nueva ejecución aislada; no reemplaza el piloto del 1 de noviembre. H3: 189 casos artificiales, nueve ajustes y cinco métodos; verificador independiente aprobado para scores, presupuesto K=4 y tres sensibilidades. H4: 180 recorridos deterministas de prueba y paquete técnico de 45 segundas revisiones preparado. No son 180 generaciones LLM ni revisiones realizadas. Cero llamadas pagadas y cero scores históricos finales.

Reproducir con el Python aislado: tools/advance_h3_h4.py --run-date 2026-11-02; después tools/verify_h3_h4.py --run-date 2026-11-02. La correspondencia ciega privada permanece bajo data/ y no se publica. Volver a ejecutar puede cambiar IDs de cegamiento; conservar cada ejecución si se requiere identidad de bytes.
