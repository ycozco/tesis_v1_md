"""Bounded historical SUNAT search; new candidates NEVER silently enter research panel."""
import concurrent.futures
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import requests
from urllib.parse import urljoin
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'datasets/busqueda/2026-11-01'
RAW = ROOT/'data/busqueda_2026-11-01'
BASE = 'http://www.aduanet.gob.pe/aduanas/informae/'
PRODUCTS = {'0804400000':'palta','0806100000':'uva','0810400000':'arandano'}


def fetch(name):
    url = BASE+name
    report = {'file':name,'url':url,'retrieved_at_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
    records = []
    try:
        r = requests.get(url, timeout=35)
        report['http_status']=r.status_code
        r.raise_for_status()
        if len(r.content)>20_000_000: raise ValueError('Archive exceeds bounded search size')
        archive=zipfile.ZipFile(io.BytesIO(r.content))
        report.update(bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
        (RAW/name).write_bytes(r.content)
        member=next(n for n in archive.namelist() if n.lower().endswith('.dbf'))
        data=archive.read(member)
        file=RAW/(name+'.DBF');file.write_bytes(data)
        count=struct.unpack_from('<I',data,4)[0]
        header,length=struct.unpack_from('<HH',data,8)
        if header+count*length>len(data):raise ValueError('Truncated DBF')
        fields={};offset=1
        for pos in range(32,header-1,32):
            if data[pos]==13:break
            field=data[pos:pos+11].split(b'\0')[0].decode('ascii')
            fields[field]=(offset,data[pos+16]);offset+=data[pos+16]
        def get(i,key):
            offset,size=fields[key];start=header+i*length+offset
            return data[start:start+size].decode('latin1').strip()
        for i in range(count):
            if data[header+i*length]==42:continue
            code=get(i,'PART_NANDI').split('.')[0].zfill(10)
            if code not in PRODUCTS:continue
            values=[get(i,k) for k in ('CADU','FANO','NDCL','NSER')]
            records.append({'archivo_fuente':name,'fila_fuente':i+1,'producto':PRODUCTS[code],
                'subpartida':code,'destino':get(i,'CPAIDES'),'fecha_embarque_raw':get(i,'FEMB'),
                'valor_fob_usd':get(i,'VFOBSERDOL'),'peso_neto_kg':get(i,'VPESNET'),
                'id_declaracion_serie_sha256':hashlib.sha256('|'.join(values).encode()).hexdigest(),
                'status':'unreconciled_historical_candidate_not_training_data'})
        report.update(status='valid_zip_dbf',three_product_rows=len(records))
    except Exception as e:report.update(status='unavailable_or_invalid',error_type=type(e).__name__)
    return report,records


def main():
    OUT.mkdir(parents=True,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
    names=['x01070118.zip','x31060119.zip','x30050120.zip','x28030121.zip','x03090122.zip','x02080123.zip']
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(fetch,names))
    records=[r for _,rows in results for r in rows]
    if records:
        with (OUT/'historicos-candidatos.csv').open('w',newline='',encoding='utf8') as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    manifest={'status':'bounded_availability_search_NOT_full_historical_coverage',
              'archives':[r for r,_ in results],'candidate_rows':len(records),'official_fields_verified':False,
              'note':'Raw archives remain local; no identity fields published. No new rows integrated or weeks filled.'}
    try:
        r=requests.get(BASE+'presentacion_bases_web.htm',timeout=30)
        r.raise_for_status()
        links=[urljoin(BASE,link.replace('\\','/')) for link in re.findall(r'href\s*=\s*[\"\']?([^\s>\"\']+)',r.text,re.I)]
        manifest['index_document_links']=[l for l in links if re.search(r'estruct|proced|\.xls|\.doc',l,re.I)]
        (OUT/'sunat-index.html').write_bytes(r.content)
        docs=[]
        for url in manifest['index_document_links'][:6]:
            d=requests.get(url,timeout=20)
            item={'url':url,'http_status':d.status_code}
            if d.status_code==200:
                name=url.rsplit('/',1)[-1]
                destination = RAW if name.lower().endswith('.xls') else OUT
                (destination/name).write_bytes(d.content)
                item.update(file=name,storage='local_raw_only' if destination==RAW else 'filtered_delivery',
                            bytes=len(d.content),sha256=hashlib.sha256(d.content).hexdigest())
            docs.append(item)
        manifest['documents']=docs
    except Exception as e:manifest['index_status']=type(e).__name__
    (OUT/'manifest-busqueda.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps(manifest,ensure_ascii=True))


if __name__=='__main__':main()
