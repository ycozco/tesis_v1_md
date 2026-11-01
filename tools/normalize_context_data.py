"""Parse preserved SISAP HTML by header/row, retaining missing cells and source units."""
import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parents[1] / 'datasets/tratamiento/2026-11-01/contexto'


class Table(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.row = []
        if tag in ('td', 'th'): self.cell = []

    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            if self.row is not None: self.row.append(' '.join(' '.join(self.cell).split()))
            self.cell = None
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def main():
    records, summaries = [], []
    for file in sorted(OUT.glob('sisap-*.html')):
        raw = file.read_bytes()
        # Endpoint declares latin1 but payload is UTF-8 in this collection.
        try: text = raw.decode('utf-8')
        except UnicodeDecodeError: text = raw.decode('latin1')
        table = Table()
        table.feed(text)
        header = next(row for row in table.rows if row and row[0] == 'Fecha')
        names = header[1:]
        period_rows = [row for row in table.rows if row and re.fullmatch(r'[A-Z]{3}-\d{4}', row[0])]
        for row in period_rows:
            if len(row) != len(names) + 1:
                raise ValueError(f'Unexpected column count {file}: {row}')
            for variety, cell in zip(names, row[1:]):
                if cell not in ('...', '', '-', '--') and not re.fullmatch(r'\d+(\.\d+)?', cell):
                    raise ValueError(f'Unrecognized numeric SISAP cell {cell}')
                records.append({'producto': file.name.split('-')[1], 'variedad':variety,
                    'periodo_fuente':row[0], 'precio_promedio':float(cell) if re.fullmatch(r'\d+(\.\d+)?', cell) else None,
                    'unidad_encabezado':'S/. x Kg., S/. x Lt. o S/. x Unid.',
                    'unidad_especifica_validada':False, 'mercado':'15011502',
                    'archivo_fuente':file.name, 'publicado_en':None, 'eligible_asof':False})
        summaries.append({'source':file.name, 'periods':len(period_rows), 'varieties':len(names),
                          'months': [row[0] for row in period_rows]})
    if records:
        with (OUT / 'sisap-mensual-normalizado.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0]))
            writer.writeheader(); writer.writerows(records)
    summary = {'sources':summaries, 'cells':len(records),
        'numeric_prices':sum(r['precio_promedio'] is not None for r in records),
        'missing_cells':sum(r['precio_promedio'] is None for r in records),
        'warning':'Wholesale internal context, not FOB. Unit header is generic; do not assume kilograms. No blueberry series identified.'}
    (OUT / 'normalizacion-resumen.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k != 'sources'}, ensure_ascii=True))


if __name__ == '__main__': main()
