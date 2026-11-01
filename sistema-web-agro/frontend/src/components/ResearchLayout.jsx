import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../App.jsx'

const sections = [
  ['series', 'monitoring', 'Series y comparación'],
  ['pronosticos', 'query_stats', 'Pronóstico'],
  ['senales', 'radar', 'Señales exploratorias'],
  ['reportes', 'description', 'Reportes y evidencia'],
  ['fuentes', 'database', 'Fuentes y cobertura'],
]

export default function ResearchLayout({ children }) {
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const active = new URLSearchParams(location.search).get('view') || 'series'
  const legacy = location.pathname !== '/dashboard'
  function leave() { logout(); navigate('/login') }
  return (
    <div className="min-h-screen bg-background text-on-surface font-body-md">
      <header className="glass-panel border-b border-white/10 px-4 md:px-8 py-4 flex flex-wrap items-center justify-between gap-4">
        <Link to="/dashboard" className="flex items-center gap-3 min-w-0">
          <span className="material-symbols-outlined text-primary text-3xl" aria-hidden="true">eco</span>
          <div><p className="font-headline-md font-semibold text-primary text-xl">Exportaciones peruanas</p>
            <p className="text-xs text-on-surface-variant">Palta · Uva fresca · Arándano</p></div>
        </Link>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-on-surface-variant hidden sm:inline">{user?.nombre || 'Investigación'}</span>
          <button onClick={leave} className="glass-input rounded-lg px-3 py-2 hover:text-primary">Cerrar sesión</button>
        </div>
      </header>
      <div className="max-w-[1600px] mx-auto md:flex">
        <aside className="md:w-64 md:shrink-0 border-b md:border-b-0 md:border-r border-white/10 p-3 md:p-5">
          <p className="hidden md:block text-xs tracking-widest uppercase text-on-surface-variant mb-5">Análisis comparativo</p>
          <nav aria-label="Navegación principal" className="flex md:flex-col gap-2 overflow-x-auto pb-1">
            {sections.map(([id, icon, label]) => (
              <Link key={id} to={`/dashboard?view=${id}`} aria-current={!legacy && active === id ? 'page' : undefined}
                className={`flex items-center gap-3 p-3 rounded-lg whitespace-nowrap text-sm transition-colors ${!legacy && active === id ? 'bg-primary/15 text-primary border border-primary/25' : 'text-on-surface-variant hover:bg-white/5 border border-transparent'}`}>
                <span className="material-symbols-outlined text-xl" aria-hidden="true">{icon}</span>{label}
              </Link>
            ))}
          </nav>
          <div className="hidden md:block glass-panel rounded-xl p-4 mt-8 text-xs leading-relaxed text-on-surface-variant">
            <p className="text-primary font-semibold mb-2">Corte documentado</p>
            Piloto retrospectivo de desarrollo. Cobertura parcial y prueba final pendiente.
          </div>
        </aside>
        <main className="min-w-0 flex-1 p-4 md:p-8">
          {legacy && <div role="status" className="glass-panel border border-error/30 rounded-xl p-4 mb-6 text-sm text-error">
            Pantalla del prototipo anterior. Sus métricas y acciones no pertenecen a la evaluación actual de la tesis.
            <Link to="/dashboard" className="underline ml-2">Volver al análisis actual</Link>
          </div>}
          {children}
        </main>
      </div>
    </div>
  )
}
