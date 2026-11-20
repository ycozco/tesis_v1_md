import { MarketContextProvider, MarketTicker } from './MarketContext.jsx'
import React, { useEffect, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Leaf, LayoutDashboard, ArrowLeftRight, ChartNoAxesCombined, Radar, FileText, Database, Workflow, MessagesSquare, ChevronLeft, ChevronRight, LogOut, Menu, X, ArrowUpRight } from 'lucide-react'
import { useAuth } from '../App.jsx'
const sections = [
 ['resumen', LayoutDashboard, 'Panorama'], ['series', ArrowLeftRight, 'Explorar y comparar'],
 ['pronosticos', ChartNoAxesCombined, 'Pronósticos'], ['senales', Radar, 'Variaciones para revisar'],
 ['reportes', FileText, 'Evidencia y reportes'], ['fuentes', Database, 'Datos y fuentes'],
 ['proceso', Workflow, 'Trazabilidad'], ['ia', MessagesSquare, 'Asistente y archivo'],
]
export default function ResearchLayout({children}) {
 const [collapsed,setCollapsed]=useState(false),[mobile,setMobile]=useState(false)
 const {user,logout}=useAuth(); const location=useLocation(), navigate=useNavigate()
 const active=new URLSearchParams(location.search).get('view')||'resumen'
 const legacy=location.pathname!=='/dashboard'
 const current=sections.find(s=>s[0]===active)||sections[0]
 const sectionUrl=id=>{const q=new URLSearchParams(location.search);q.set('view',id);return `/dashboard?${q}`}
 useEffect(()=>{window.scrollTo({top:0,behavior:'instant'});document.getElementById('research-main')?.focus({preventScroll:true});setMobile(false)},[active])
 useEffect(()=>{if(!mobile)return;const close=e=>{if(e.key==='Escape')setMobile(false)};window.addEventListener('keydown',close);return()=>window.removeEventListener('keydown',close)},[mobile])
 function leave(){logout();navigate('/login')}
 return <MarketContextProvider><div className={`research-shell observatory ${collapsed?'observatory-collapsed':''} ${mobile?'observatory-menu-open':''}`}>
  <a href="#research-main" className="research-skip">Saltar al contenido</a>
  {mobile&&<button className="observatory-scrim" aria-label="Cerrar navegación" onClick={()=>setMobile(false)} />}
  <aside id="research-navigation" className="observatory-rail">
   <Link to={sectionUrl('resumen')} className="observatory-brand"><Leaf size={30} strokeWidth={1.5} /><span>AgroScope<small>Perú · Observatorio agroexportador</small></span></Link>
   <button className="observatory-fold" aria-label={collapsed?'Ampliar navegación':'Plegar navegación'} aria-expanded={!collapsed} onClick={()=>setCollapsed(!collapsed)}>{collapsed?<ChevronRight size={16}/>:<ChevronLeft size={16}/>}</button>
   <p className="observatory-nav-label">Análisis de mercado</p>
   <nav aria-label="Navegación principal">{sections.map(([id,Icon,label],i)=><React.Fragment key={id}>{i===4&&<p className="observatory-nav-label">Investigación y evidencia</p>}<Link to={sectionUrl(id)} title={label} aria-current={!legacy&&active===id?'page':undefined}><Icon size={18} strokeWidth={1.6}/><span>{label}</span>{!legacy&&active===id&&<span className="observatory-active-dot"/>}</Link></React.Fragment>)}</nav>
   <div className="observatory-rail-bottom"><div className="observatory-pilot"><span className="observatory-pilot-label">Corte documentado <ArrowUpRight size={14}/></span><p>Piloto retrospectivo de desarrollo. Cobertura parcial y evaluación final pendiente.</p><Link to={sectionUrl('fuentes')}>Consultar los datos <span>→</span></Link></div>
   <div className="observatory-account"><span className="observatory-avatar">{(user?.nombre||'R').slice(0,1)}</span><div><strong>{user?.nombre||'Investigación'}</strong><small>Entorno local</small></div><button aria-label="Cerrar sesión" title="Cerrar sesión" onClick={leave}><LogOut size={18}/></button></div></div>
  </aside>
  <div className="observatory-body">
   <MarketTicker/>
   <header className="observatory-topbar"><div><button className="observatory-mobile-toggle" aria-controls="research-navigation" aria-expanded={mobile} onClick={()=>setMobile(!mobile)} aria-label={mobile?'Cerrar menú':'Menú'}>{mobile?<X size={20}/>:<Menu size={20}/>}</button><span className="observatory-breadcrumb">Espacio de investigación <span>/</span> <strong>{current[2]}</strong></span></div><span className="observatory-environment"><i/>Datos del corte local</span></header>
   <main id="research-main" tabIndex={-1}>{legacy&&<div role="status" className="research-notice">Pantalla del prototipo anterior. Sus métricas no pertenecen a la evaluación actual.<Link to={sectionUrl('resumen')}>Volver al análisis</Link></div>}{children}<footer className="observatory-footer"><span>AgroScope Perú · Información con procedencia</span><Link to={sectionUrl('proceso')}>Ver trazabilidad <ArrowUpRight size={13}/></Link></footer></main>
  </div>
 </div></MarketContextProvider>
}
