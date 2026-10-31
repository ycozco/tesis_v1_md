import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const root=path.resolve(process.argv[2]||'.'),out=path.join(root,'datasets/fuentes/2026-10-31');
const m=JSON.parse(await fs.readFile(path.join(out,'manifest-sunat.json'),'utf8'));
for(const s of m.fuentes){const b=await fs.readFile(path.join(root,'data/fuentes_2026-10-31/sunat',s.archivo));assert.equal(b.length,s.bytes);assert.equal(crypto.createHash('sha256').update(b).digest('hex').toUpperCase(),s.sha256.toUpperCase());assert.equal(b.readUInt16LE(0),0x4b50);}
const content=await fs.readFile(path.join(out,'observaciones-sunat.csv'),'utf8');const lines=content.trimEnd().split('\n');assert.equal(lines.length-1,m.filas_seleccionadas);let counts={},keys=new Set();
const parse=line=>[...line.matchAll(/"((?:[^"]|"")*)"(?:,|$)/g)].map(x=>x[1].replaceAll('""','"'));
assert.equal(parse(lines[0]).length,14);for(const line of lines.slice(1)){const r=parse(line);assert.equal(r.length,14);assert.ok(['0804400000','0806100000','0810400000'].includes(r[4]));assert.match(r[2],/^[a-f0-9]{64}$/);const fob=Number(r[10]),weight=Number(r[11]);assert.ok(fob>=0&&weight>0);assert.ok(Math.abs(Number(r[12])-fob/weight)<=1e-9*Math.max(1,fob/weight));keys.add(r[2]);counts[r[0]]=(counts[r[0]]||0)+1;}
for(const s of m.fuentes)assert.equal(counts[s.archivo],s.seleccionados);assert.equal(keys.size,m.claves_declaracion_serie);
console.log(JSON.stringify({estado:'OK',originales_verificados:m.fuentes.length,filas_verificadas:lines.length-1,claves:keys.size}));
