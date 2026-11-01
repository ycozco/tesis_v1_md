export function comparisonCsv(series, product, destination, comparison, unit, sourceHash) {
  const header = ['semana_iso', 'producto', 'destino', 'valor', 'unidad', 'destino_comparado', 'valor_comparado', 'estado_principal', 'fuente_sha256']
  const rows = series.map(row => [row.week, product, destination, row.main ?? '', unit, comparison,
    row.comparison ?? '', row.main == null ? 'unknown' : 'observed_partial', sourceHash])
  return '\uFEFF' + [header, ...rows].map(row => row.map(value => `"${String(value).replaceAll('"', '""')}"`).join(';')).join('\r\n')
}
