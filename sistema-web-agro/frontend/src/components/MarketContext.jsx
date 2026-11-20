import { Dialog } from './ui/dialog.jsx'
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs.jsx'
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { createContext, useContext, useEffect, useState } from 'react'
import { ArrowUpRight, CloudSun, Coins, Leaf, Grape } from 'lucide-react'
import { useAuth } from '../App.jsx'
import { researchApi } from '../lib/researchApi.js'

const Context = createContext({items:[],loading:true,error:'',openDetail:()=>{}})
const fmt=(v,d=2)=>v==null?'No disponible':new Intl.NumberFormat('es-PE',{maximumFractionDigits:d,minimumFractionDigits:d}).format(v)
const dated=value=>{if(!value)return 'Sin fecha de dato';const date=new Date(value.length===10?value+'T12:00:00-05:00':value);return new Intl.DateTimeFormat('es-PE',{timeZone:'America/Lima',day:'2-digit',month:'short',...(value.length>10?{hour:'2-digit',minute:'2-digit'}:{year:'numeric'})}).format(date)}
const statusName=item=>item?.status==='stale'?'Último dato guardado':item?.status==='delayed'?'Dato con retraso':item?.status==='available'?'Publicado':'No disponible'
export function MarketContextProvider({children}) {
 const {token}=useAuth();const [state,setState]=useState({items:[],loading:true,error:''});const [selectedId,setSelectedId]=useState(null)
 useEffect(()=>{let active=true,timer
  async function read(){try{const payload=await researchApi('market-context',token);if(active)setState({...payload,loading:false,error:''})}catch(e){if(active)setState(s=>({...s,loading:false,error:e.message,items:s.items.map(i=>({...i,status:'stale'}))}))}finally{if(active)timer=setTimeout(read,30000)}}
  if(token)read()
  return()=>{active=false;clearTimeout(timer)}
 },[token])
 return <Context.Provider value={{...state,openDetail:id=>setSelectedId(id)}}>{children}<MarketDetail item={state.items.find(i=>i.id===selectedId)} items={state.items} onClose={()=>setSelectedId(null)}/></Context.Provider>
}
export function MarketTicker(){
 const {items,loading,error,openDetail}=useContext(Context)
 const usable=items.filter(i=>i.value!=null)
 const messages=usable.map(i=>({id:i.id,text:`${i.kind==='weather'?'Clima · ':''}${i.label}  ${fmt(i.value,i.kind==='exchange'?3:i.kind==='weather'?1:2)} ${i.unit}  ·  ${dated(i.observed_at)}  ·  ${i.source}${i.status!=='available'?' · '+statusName(i):''}`}))
 const fallback=loading?'Consultando precios, dólar y clima regional…':error?'No se pudo consultar la actualidad del mercado':'Recopilando las primeras observaciones de las fuentes públicas…'
 return <section className="market-ticker" aria-label="Actualidad del mercado"><button className="market-ticker-title" aria-label="Ver detalle del mercado" onClick={()=>openDetail(usable[0]?.id)}><span/>Mercado al día</button><div className="market-ticker-window"><div className={`market-ticker-track ${messages.length?'':'market-ticker-pending'}`}>{[0,1].map(copy=><div className="market-ticker-group" key={copy} aria-hidden={copy===1?true:undefined}>{messages.length?messages.map(m=><button tabIndex={copy===1?-1:0} aria-haspopup="dialog" aria-label={`Ver detalle: ${m.text}`} onClick={()=>openDetail(m.id)} key={m.id}><i/>{m.text}</button>):<span>{fallback}</span>}</div>)}</div></div></section>

}
export function MarketContextCards(){
 const {items,checked_at,loading,error,openDetail}=useContext(Context)
 const [region,setRegion]=useState('ica')
 const exchange=items.find(i=>i.kind==='exchange')
 const palta=items.find(i=>i.label==='Palta Fuerte')||items.find(i=>i.kind==='price'&&i.product==='Palta')
 const uva=items.find(i=>i.label==='Uva Red Globe')||items.find(i=>i.kind==='price'&&i.product==='Uva')
 const weather=items.find(i=>i.id==='weather-'+region)
 const cards=[{key:'usd',item:exchange,label:'Dólar interbancario',Icon:Coins,kind:'exchange'},
 {key:'palta',item:palta,label:palta?.label||'Palta · mayorista',Icon:Leaf,kind:'price'},
 {key:'uva',item:uva,label:uva?.label||'Uva · mayorista',Icon:Grape,kind:'price'},
 {key:'weather',item:weather,label:'Clima regional',Icon:CloudSun,kind:'weather'}]
 return <section className="market-context" aria-label="Mercado al día">
  <header className="market-context-heading"><div><span className="market-context-kicker">Contexto actualizado</span><h2>Mercado al día</h2></div><p>Fuentes públicas · consulta {checked_at?dated(checked_at):loading?'en curso':'pendiente'}</p></header>
  {error&&<p role="status" className="market-context-error">No se pudo actualizar. Los datos conservados indican su antigüedad.</p>}
  <div className="market-context-grid">{cards.map(({key,item,label,Icon,kind})=><article key={key} className={`market-context-card ${item?.value==null?'is-empty':''}`} onClick={e=>{if(!e.target.closest('button,a,select,option')&&item)openDetail(item.id)}}>
   <div className="market-card-top"><span><Icon size={16} strokeWidth={1.5}/>{label}</span>{kind==='weather'?<select aria-label="Región del clima" value={region} onChange={e=>setRegion(e.target.value)}><option value="ica">Ica</option><option value="trujillo">Trujillo</option><option value="arequipa">Arequipa</option></select>:<span className={`market-card-state ${item?.status==='available'?'is-available':''}`}>{statusName(item)}</span>}</div>
   <div className="market-card-value">{item?.value!=null?fmt(item.value,kind==='exchange'?3:kind==='weather'?1:2):loading?'Consultando…':'No disponible'}{item?.value!=null&&<small>{item.unit}</small>}</div>
   <p className="market-card-description">{kind==='weather'&&item?.value!=null?`Hoy: mín. ${fmt(item.low,1)}° · máx. ${fmt(item.high,1)}° · Humedad ${fmt(item.humidity,0)}% · Lluvia ${fmt(item.precipitation,1)} mm`:item?.detail||'Esperando una observación verificable de la fuente'}</p>
   {kind==='exchange'&&item?.change!=null&&<p className="market-card-change">{item.change>0?'↑':item.change<0?'↓':'→'} {fmt(Math.abs(item.change),3)} S/ frente a la observación previa</p>}
   {kind==='price'&&<p className="market-card-unit">Unidad publicada: kg, litro o unidad; sin conversión.</p>}
   {kind==='weather'&&<p className="market-card-unit">Dato de modelo · punto regional, sin atribución a parcelas{item?.status&&item.status!=='available'?' · '+statusName(item):''}</p>}
   <button className="market-card-detail-button" aria-haspopup="dialog" disabled={!item} onClick={()=>openDetail(item.id)} aria-label={`Ver detalle de ${label}`}>Ver detalle <ArrowUpRight size={13}/></button>
   <footer><span>{dated(item?.observed_at)}</span>{item?.url?<a href={item.url} target="_blank" rel="noreferrer">{item.source}<ArrowUpRight size={12}/></a>:<span>{kind==='price'?'SISAP':kind==='weather'?'Open-Meteo':'BCRP'}</span>}</footer>
  </article>)}</div>
  <details className="market-context-details"><summary>Consultar variedades, unidades y procedencia</summary><div className="market-context-detail-body"><p>Precios del Mercado Mayorista N.º 2 de Frutas, Lima. El encabezado de SISAP mezcla S/ por kg, litro o unidad; no se infiere una unidad específica. No hay cotización de arándano verificada en esta consulta. Estas referencias no equivalen al valor unitario FOB ni actualizan el corte de investigación.</p><div className="overflow-x-auto"><table><thead><tr><th>Variedad</th><th>Precio publicado · S/</th><th>Fecha</th></tr></thead><tbody>{items.filter(i=>i.kind==='price'&&i.value!=null).map(i=><tr key={i.id}><td>{i.label}</td><td>{fmt(i.value)}</td><td>{dated(i.observed_at)} · {statusName(i)}</td></tr>)}</tbody></table></div><p>El recolector consulta cada hora y conserva la última respuesta válida. Open-Meteo aporta condiciones de modelo por coordenadas de referencia. Si la consulta falla, los valores anteriores se marcan como guardados.</p></div></details>
 </section>
}

function MarketDetail({item,items,onClose}) {
 const [tab,setTab]=useState('detail')
 useEffect(()=>setTab('detail'),[item?.id])
 const peers=item?.kind==='price'?items.filter(i=>i.kind==='price'&&i.product===item.product):item?.kind==='weather'?items.filter(i=>i.kind==='weather'):[]
 const graph=item?.kind==='weather'?peers.filter(i=>i.value!=null).map(i=>({name:i.label,value:i.value})):item?.kind==='exchange'&&item.value!=null?[...(item.change!=null?[{name:'Anterior publicada',value:item.value-item.change}]:[]),{name:'Última publicada',value:item.value}]:[]
 function download(){const data={observation:item,related:peers,scope:'public_context',research_dataset_updated:false};const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`mercado-${item.id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
 return <Dialog open={!!item} onClose={onClose} title={item?.label||'Detalle del mercado'} description={item?`${item.source} · dato de ${dated(item.observed_at)} · ${statusName(item)}`:''}>{item&&<>
  <div className="market-dialog-reading"><strong>{fmt(item.value,item.kind==='exchange'?3:item.kind==='weather'?1:2)} <small>{item.unit}</small></strong><span>{item.detail}</span></div>
  <Tabs value={tab} onValueChange={setTab}><TabsList aria-label="Detalle de mercado"><TabsTrigger value="detail">Información</TabsTrigger><TabsTrigger value="comparison">{item.kind==='price'?'Variedades':'Comparación'}</TabsTrigger><TabsTrigger value="source">Fuente y fechas</TabsTrigger></TabsList>
  <TabsContent value="detail" className="market-modal-tab"><dl className="market-detail-facts"><div><dt>Estado</dt><dd>{statusName(item)}</dd></div><div><dt>Fecha del dato</dt><dd>{dated(item.observed_at)}</dd></div><div><dt>Última consulta</dt><dd>{dated(item.checked_at)}</dd></div><div><dt>Última recuperación válida</dt><dd>{dated(item.last_success_at)}</dd></div>{item.series&&<div><dt>Serie BCRP</dt><dd>{item.series} · venta</dd></div>}{item.product&&<div><dt>Producto / mercado</dt><dd>{item.product} · Mercado Mayorista N.º 2, Lima</dd></div>}{item.kind==='weather'&&<><div><dt>Humedad / precipitación</dt><dd>{fmt(item.humidity,0)} % · {fmt(item.precipitation,1)} mm</dd></div><div><dt>Extremos estimados de hoy</dt><dd>{fmt(item.low,1)} a {fmt(item.high,1)} °C</dd></div><div><dt>Punto regional</dt><dd>{item.latitude}, {item.longitude}</dd></div></>}</dl><p className="market-modal-note">{item.kind==='price'?item.unit_note:item.kind==='weather'?'Condiciones de modelo para un punto regional. No son mediciones de una parcela ni explican por sí solas el precio.':'Última observación diaria publicada, no una cotización intradía. La diferencia se calcula frente a la observación anterior disponible.'}</p>{item.reason&&<p role="status" className="market-modal-note">{item.reason}</p>}</TabsContent>
  <TabsContent value="comparison" className="market-modal-tab">{graph.length>0&&<><h3>{item.kind==='weather'?'Temperatura por punto regional':'Observaciones publicadas del dólar'}</h3><div className="market-modal-chart"><ResponsiveContainer width="100%" height="100%"><BarChart accessibilityLayer data={graph} margin={{left:12,right:20,top:20,bottom:8}}><CartesianGrid vertical={false} stroke="#e3e8e2"/><XAxis dataKey="name" tick={{fontSize:11}}/><YAxis tick={{fontSize:11}}/><Tooltip formatter={v=>[fmt(v,item.kind==='exchange'?3:1),item.unit]}/><Bar dataKey="value" name={item.unit} fill="#6c8952" maxBarSize={72} radius={[4,4,0,0]}/></BarChart></ResponsiveContainer></div></>}{peers.length>0&&<div className="interpretation-table-wrap"><table><thead><tr><th>{item.kind==='price'?'Variedad':'Punto'}</th><th>Valor publicado</th><th>Fecha</th></tr></thead><tbody>{peers.map(i=><tr key={i.id}><td>{i.label}</td><td>{fmt(i.value)} {i.unit}</td><td>{dated(i.observed_at)}</td></tr>)}</tbody></table></div>}{item.kind==='price'&&<p className="market-modal-note">Se conservan las variedades separadas. El encabezado no valida su unidad específica; no se grafica una comparación de precios con unidades supuestas.</p>}{!graph.length&&!peers.length&&<p>No hay observaciones suficientes para comparar.</p>}</TabsContent>
  <TabsContent value="source" className="market-modal-tab"><dl className="market-detail-facts"><div><dt>Proveedor</dt><dd>{item.source}</dd></div><div><dt>Actualización del recolector</dt><dd>Cada hora</dd></div><div><dt>Uso</dt><dd>Contexto público; separado del corte de investigación</dd></div></dl><a className="market-source-address" href={item.url} target="_blank" rel="noreferrer">{item.url}</a><p className="market-modal-note">Si la fuente falla, se conserva la última recuperación válida y se muestra su estado. Abrir la fuente permite comprobar su publicación original.</p></TabsContent>
  </Tabs><footer className="market-dialog-actions"><button className="ui-button ui-button-outline" onClick={download}>Descargar detalle JSON</button><a className="ui-button ui-button-primary" href={item.url} target="_blank" rel="noreferrer">Abrir fuente oficial <ArrowUpRight size={16}/></a></footer>
 </>}</Dialog>
}
