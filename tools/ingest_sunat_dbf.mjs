import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
const root = path.resolve(process.argv[2] || '.');
const raw = path.join(root, 'data/fuentes_2026-10-31');
const out = path.join(root, 'datasets/fuentes/2026-10-31');
await fs.mkdir(out, {recursive:true});
const downloads = JSON.parse((await fs.readFile(path.join(raw,'descargas-sunat.json'),'utf8')).replace(/^\uFEFF/,''));
const targets = {'0804400000':'palta','0806100000':'uva','0810400000':'arandano'};
const cols=['archivo_fuente','fila_fuente','id_declaracion_serie_sha256','producto','subpartida','destino','fecha_numeracion_raw','fecha_embarque_raw','fecha_recepcion_raw','fecha_regularizacion_raw','valor_fob_usd','peso_neto_kg','valor_unitario_fob_usd_kg','estado_calidad'];
const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
let lines=[cols.map(quote).join(',')], files=[], groups={}, keys=new Map(), versions=new Set(), invalid=0, exactDuplicates=0, records=0;
for(const d of downloads.filter(d=>d.estado==='descargado')){
 const dbf=d.archivo.replace(/zip$/i,'DBF'); const b=await fs.readFile(path.join(raw,'sunat',dbf));
 const count=b.readUInt32LE(4),header=b.readUInt16LE(8),length=b.readUInt16LE(10); if(header+count*length>b.length) throw Error('Truncated DBF '+dbf);
 let fields={},offset=1;for(let p=32;p<header-1&&b[p]!==13;p+=32){const name=b.subarray(p,p+11).toString('ascii').replaceAll('\0','');fields[name]={offset,length:b[p+16]};offset+=b[p+16];}
 for(const field of ['CADU','FANO','NDCL','NSER','PART_NANDI','CPAIDES','FNUM','FEMB','VFOBSERDOL','VPESNET'])if(!fields[field])throw Error('Missing '+field+' in '+dbf);
 const get=(i,f)=>{const x=fields[f];return x?b.subarray(header+i*length+x.offset,header+i*length+x.offset+x.length).toString('latin1').trim():'';};
 let selected=0,byProduct={};
 for(let i=0;i<count;i++){
  if(b[header+i*length]===42)continue;
  const code=get(i,'PART_NANDI').split('.')[0].padStart(10,'0');if(!targets[code])continue;
  const product=targets[code],dest=get(i,'CPAIDES'),fobRaw=get(i,'VFOBSERDOL'),weightRaw=get(i,'VPESNET'),fob=Number(fobRaw),weight=Number(weightRaw);
  let status=!fobRaw||!weightRaw||!Number.isFinite(fob)||!Number.isFinite(weight)?'numero_invalido':weight<=0?'peso_no_positivo':fob<0?'fob_negativo':'valido';
  if(status!=='valido')invalid++;
  const id=crypto.createHash('sha256').update(['CADU','FANO','NDCL','NSER'].map(f=>get(i,f)).join('|')).digest('hex');
  const values=[id,product,code,dest,...['FNUM','FEMB','FECH_RECEP','FREG'].map(f=>get(i,f)),fobRaw,weightRaw];
  const fingerprint=crypto.createHash('sha256').update(JSON.stringify(values)).digest('hex');if(versions.has(fingerprint))exactDuplicates++;versions.add(fingerprint);
  if(!keys.has(id))keys.set(id,new Set());keys.get(id).add(fingerprint);
  lines.push([d.archivo,i+1,...values.slice(0,4),...values.slice(4,8),fobRaw,weightRaw,status==='valido'?fob/weight:'',status].map(quote).join(','));
  const g=groups[product+'|'+dest]??={producto:product,destino:dest,filas:0,fechas:new Set(),min:null,max:null};g.filas++;const dt=get(i,'FEMB');if(/^\d{8}$/.test(dt)){g.fechas.add(dt);g.min=!g.min||dt<g.min?dt:g.min;g.max=!g.max||dt>g.max?dt:g.max;}
  selected++;records++;byProduct[product]=(byProduct[product]||0)+1;
 }
 files.push({...d,registros_dbf:count,seleccionados:selected,por_producto:byProduct});
}
await fs.writeFile(path.join(out,'observaciones-sunat.csv'),lines.join('\n')+'\n');
const coverage=Object.values(groups).map(({fechas,...g})=>({...g,fechas_embarque_distintas:fechas.size}));
await fs.writeFile(path.join(out,'cobertura-observada.json'),JSON.stringify(coverage,null,2));
const summary={fecha_recopilacion:'2026-10-31',estado:'recopilacion_parcial_no_dataset_experimental',archivos:files.length,filas_seleccionadas:records,claves_declaracion_serie:keys.size,duplicados_exactos_entre_archivos:exactDuplicates,claves_con_versiones_distintas:[...keys.values()].filter(s=>s.size>1).length,filas_calidad_no_valida:invalid,fuentes:files};
await fs.writeFile(path.join(out,'manifest-sunat.json'),JSON.stringify(summary,null,2));
console.log(JSON.stringify({archivos:files.length,filas:records,claves:keys.size,duplicados:exactDuplicates,conflictos:summary.claves_con_versiones_distintas,invalid}));
