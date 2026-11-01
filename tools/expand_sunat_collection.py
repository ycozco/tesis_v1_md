"""Rebuild the 24-source filtered collection from exact archives, preserving the old release.

Raw personal source archives stay local. This script exports only approved analytical fields.
"""
import csv
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT/'datasets/fuentes/2026-10-31'
NEW = ROOT/'datasets/fuentes/2026-11-01-expansion'
RAW = ROOT/'data/busqueda_2026-11-01'


def main():
    NEW.mkdir(parents=True,exist_ok=True)
    old_bytes=(OLD/'observaciones-sunat.csv').read_bytes()
    with (OLD/'observaciones-sunat.csv').open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);columns=reader.fieldnames;rows=list(reader)
    previous_rows=len(rows)
    manifest=json.loads((OLD/'manifest-sunat.json').read_text(encoding='utf8'))
    search=json.loads((ROOT/'datasets/busqueda/2026-11-01/manifest-busqueda.json').read_text(encoding='utf8'))
    sources=[]
    products={'0804400000':'palta','0806100000':'uva','0810400000':'arandano'}
    for item in search['archives']:
        if item.get('status')!='valid_zip_dbf':continue
        original=(RAW/item['file']).read_bytes()
        assert hashlib.sha256(original).hexdigest()==item['sha256']
        with zipfile.ZipFile(RAW/item['file']) as archive:
            member=next(n for n in archive.namelist() if n.lower().endswith('.dbf'))
            data=archive.read(member)
        count=struct.unpack_from('<I',data,4)[0]
        header,length=struct.unpack_from('<HH',data,8)
        assert header+count*length<=len(data)
        fields={};offset=1
        for position in range(32,header-1,32):
            if data[position]==13:break
            field=data[position:position+11].split(b'\0')[0].decode('ascii')
            fields[field]=(offset,data[position+16]);offset+=data[position+16]
        def get(i,name):
            start,width=fields[name];start+=header+i*length
            return data[start:start+width].decode('latin1').strip()
        selected=[]
        for i in range(count):
            if data[header+i*length]==42:continue
            hs=get(i,'PART_NANDI').split('.')[0].zfill(10)
            if hs not in products:continue
            key='|'.join(get(i,k) for k in ('CADU','FANO','NDCL','NSER'))
            fob,weight=get(i,'VFOBSERDOL'),get(i,'VPESNET')
            assert float(fob)>=0 and float(weight)>0
            row={'archivo_fuente':item['file'],'fila_fuente':str(i+1),
                 'id_declaracion_serie_sha256':hashlib.sha256(key.encode()).hexdigest(),
                 'producto':products[hs],'subpartida':hs,'destino':get(i,'CPAIDES'),
                 'fecha_numeracion_raw':get(i,'FNUM'),'fecha_embarque_raw':get(i,'FEMB'),
                 'fecha_recepcion_raw':get(i,'FECH_RECEP'),'fecha_regularizacion_raw':get(i,'FREG'),
                 'valor_fob_usd':fob,'peso_neto_kg':weight,'valor_unitario_fob_usd_kg':str(float(fob)/float(weight)),
                 'estado_calidad':'valido'}
            assert set(row)==set(columns)
            selected.append(row)
        assert len(selected)==item['three_product_rows']
        rows.extend(selected)
        sources.append({'archivo':item['file'],'url':item['url'],'bytes':len(original),'sha256':item['sha256'],
                        'estado':'descargado','fecha_descarga':'2026-11-01','registros_dbf':count,
                        'seleccionados':len(selected),'por_producto':dict(Counter(r['producto'] for r in selected))})
    assert len(rows)==previous_rows+8579
    assert len({(r['archivo_fuente'],r['fila_fuente']) for r in rows})==len(rows)
    with (NEW/'observaciones-sunat.csv').open('w',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    new_manifest={'fecha_recopilacion':'2026-11-01','estado':'expansion_para_conciliacion_no_test_final',
                  'archivos':len(manifest['fuentes'])+len(sources),'filas_seleccionadas':len(rows),
                  'claves_declaracion_serie':len({r['id_declaracion_serie_sha256'] for r in rows}),
                  'procedencia':{'coleccion_previa':'datasets/fuentes/2026-10-31',
                      'observaciones_previas_sha256':hashlib.sha256(old_bytes).hexdigest(),
                      'filas_previas':previous_rows,'filas_agregadas_sin_conciliar':8579,
                      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                  'fuentes':manifest['fuentes']+sources}
    (NEW/'manifest-sunat.json').write_text(json.dumps(new_manifest,indent=2,ensure_ascii=False),encoding='utf8')
    assert (OLD/'observaciones-sunat.csv').read_bytes()==old_bytes
    print(json.dumps({k:v for k,v in new_manifest.items() if k!='fuentes'}))


if __name__=='__main__':main()
