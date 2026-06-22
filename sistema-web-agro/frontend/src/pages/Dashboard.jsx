import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch('/api/dashboard/stats')
      .then(res => res.json())
      .then(data => {
        setStats(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching dashboard stats:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <span className="material-symbols-outlined text-primary text-5xl animate-spin">sync</span>
        <span className="ml-3 text-lg font-medium text-primary">Cargando telemetría del dashboard...</span>
      </div>
    )
  }

  const {
    active_alerts_count = 0,
    total_alerts_count = 0,
    avg_decision_time_s = 0,
    priority_alerts = [],
    recent_logs = []
  } = stats || {}

  return (
    <div>
      {/* Page Header */}
      <header className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight mb-1">Terminal del Auditor</h1>
          <p className="font-body-md text-body-md text-on-surface-variant">Supervisión en tiempo real y detección de anomalías para nodos primarios.</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-2 font-mono-data text-mono-data text-primary-fixed bg-primary-fixed/10 px-3 py-1.5 rounded border border-primary-fixed/20">
            <span className="w-2 h-2 rounded-full bg-primary-fixed animate-pulse"></span>
            SISTEMA EN LÍNEA
          </span>
          <span className="font-mono-data text-mono-data text-on-surface-variant px-3 py-1.5 rounded glass-panel">
            UTC-5 {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })}
          </span>
        </div>
      </header>

      {/* KPI Bento Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {/* KPI 1: Active Alerts */}
        <div className="glass-card rounded-xl p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-error/5 to-transparent opacity-50"></div>
          <div className="relative z-10 flex flex-col h-full justify-between gap-4">
            <div className="flex justify-between items-start">
              <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">ALERTAS ACTIVAS</span>
              <div className="w-8 h-8 rounded-full bg-error/10 flex items-center justify-center border border-error/20 pulse-border">
                <span className="material-symbols-outlined text-error text-[18px]">warning</span>
              </div>
            </div>
            <div>
              <div className="flex items-baseline gap-3">
                <span className="font-display-lg text-display-lg text-error">{active_alerts_count}</span>
                <span className="flex items-center font-mono-data text-mono-data text-error bg-error/10 px-1.5 py-0.5 rounded">
                  <span className="material-symbols-outlined text-[14px]">arrow_upward</span>
                  5%
                </span>
              </div>
            </div>
          </div>
          {/* Abstract sparkline */}
          <div className="absolute bottom-0 left-0 w-full h-12 opacity-30 pointer-events-none">
            <svg className="w-full h-full stroke-error fill-none" preserveAspectRatio="none" strokeWidth="2" viewBox="0 0 100 30">
              <path d="M0,25 L10,22 L20,28 L30,15 L40,18 L50,10 L60,12 L70,5 L80,8 L90,2 L100,0"></path>
            </svg>
            <svg className="w-full h-full fill-error/20 absolute bottom-0 left-0" preserveAspectRatio="none" viewBox="0 0 100 30">
              <path d="M0,30 L0,25 L10,22 L20,28 L30,15 L40,18 L50,10 L60,12 L70,5 L80,8 L90,2 L100,0 L100,30 Z"></path>
            </svg>
          </div>
        </div>

        {/* KPI 2: Operations Analyzed */}
        <div className="glass-card rounded-xl p-5 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-50"></div>
          <div className="relative z-10 flex flex-col h-full justify-between gap-4">
            <div className="flex justify-between items-start">
              <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">OPERACIONES ANALIZADAS</span>
              <div className="w-8 h-8 rounded-full bg-surface-container-high flex items-center justify-center border border-white/10">
                <span className="material-symbols-outlined text-on-surface-variant text-[18px]">dataset</span>
              </div>
            </div>
            <div>
              <div className="flex items-baseline gap-3">
                <span className="font-display-lg text-display-lg text-on-surface">{total_alerts_count}</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant">vol. total</span>
              </div>
            </div>
          </div>
        </div>

        {/* KPI 3: Model F1-Score */}
        <div className="glass-card rounded-xl p-5 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-tertiary/5 to-transparent opacity-50"></div>
          <div className="relative z-10 flex flex-col h-full justify-between gap-4">
            <div className="flex justify-between items-start">
              <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">PUNTAJE F1 DEL MODELO</span>
              <div className="w-8 h-8 rounded-full bg-tertiary/10 flex items-center justify-center border border-tertiary/20">
                <span className="material-symbols-outlined text-tertiary text-[18px]">model_training</span>
              </div>
            </div>
            <div>
              <div className="flex items-baseline gap-3">
                <span className="font-display-lg text-display-lg text-tertiary">0.92</span>
                <span className="font-body-sm text-body-sm text-tertiary/80 bg-tertiary/10 px-2 py-0.5 rounded border border-tertiary/20">alta conf</span>
              </div>
            </div>
          </div>
        </div>

        {/* KPI 4: Avg Decision Time */}
        <div className="glass-card rounded-xl p-5 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-secondary/5 to-transparent opacity-50"></div>
          <div className="relative z-10 flex flex-col h-full justify-between gap-4">
            <div className="flex justify-between items-start">
              <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">TIEMPO MEDIO DE DECISIÓN</span>
              <div className="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center border border-secondary/20">
                <span className="material-symbols-outlined text-secondary text-[18px]">timer</span>
              </div>
            </div>
            <div>
              <div className="flex items-baseline gap-3">
                <span className="font-display-lg text-display-lg text-on-surface">{avg_decision_time_s}s</span>
                <span className="flex items-center font-mono-data text-mono-data text-secondary bg-secondary/10 px-1.5 py-0.5 rounded">
                  <span className="material-symbols-outlined text-[14px]">arrow_downward</span>
                  2s
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Center Column (Chart & Table) */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          {/* Alert Trends Chart Container */}
          <div className="glass-card rounded-xl p-6 h-80 flex flex-col">
            <div className="flex justify-between items-center mb-6">
              <h2 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">show_chart</span>
                Tendencias de Alertas (14 Días)
              </h2>
              <div className="flex gap-2">
                <button className="px-3 py-1 font-label-md text-label-md text-on-surface-variant bg-surface-container-high rounded border border-white/5 hover:text-primary transition-colors">7D</button>
                <button className="px-3 py-1 font-label-md text-label-md text-on-primary-container bg-primary-container rounded border border-primary/30">14D</button>
                <button className="px-3 py-1 font-label-md text-label-md text-on-surface-variant bg-surface-container-high rounded border border-white/5 hover:text-primary transition-colors">30D</button>
              </div>
            </div>
            {/* Simulated Chart Area using Grid & CSS */}
            <div className="flex-1 relative w-full border-b border-l border-white/10 flex items-end pt-4 pb-2 pr-2">
              {/* Y-axis labels */}
              <div className="absolute left-[-24px] top-0 bottom-0 flex flex-col justify-between text-[10px] font-mono-data text-on-surface-variant py-2">
                <span>20</span>
                <span>15</span>
                <span>10</span>
                <span>5</span>
                <span>0</span>
              </div>
              {/* Grid lines */}
              <div className="absolute inset-0 flex flex-col justify-between pointer-events-none z-0 px-2 py-2">
                <div className="w-full border-t border-white/5 h-0"></div>
                <div className="w-full border-t border-white/5 h-0"></div>
                <div className="w-full border-t border-white/5 h-0"></div>
                <div className="w-full border-t border-white/5 h-0"></div>
                <div className="w-full border-t border-white/5 h-0"></div>
              </div>
              {/* Simulated Line Chart */}
              <div className="relative w-full h-full z-10 flex items-end">
                <svg className="absolute inset-0 w-full h-full stroke-primary fill-none overflow-visible" preserveAspectRatio="none" strokeWidth="2" vectorEffect="non-scaling-stroke" viewBox="0 0 100 100">
                  <path d="M0,80 L8,75 L16,60 L24,65 L32,40 L40,45 L48,30 L56,50 L64,20 L72,35 L80,10 L88,25 L96,5 L100,5" strokeLinejoin="round"></path>
                </svg>
                {/* Area fill */}
                <svg className="absolute inset-0 w-full h-full fill-primary/10" overflow="visible" preserveAspectRatio="none" viewBox="0 0 100 100">
                  <path d="M0,100 L0,80 L8,75 L16,60 L24,65 L32,40 L40,45 L48,30 L56,50 L64,20 L72,35 L80,10 L88,25 L96,5 L100,5 L100,100 Z"></path>
                </svg>
                {/* Data points */}
                <div className="absolute w-full h-full flex justify-between items-end px-[0.5%]">
                  <div className="w-2 h-2 rounded-full bg-primary border border-background absolute" style={{ left: '0%', bottom: '20%' }}></div>
                  <div className="w-2 h-2 rounded-full bg-primary border border-background absolute" style={{ left: '32%', bottom: '60%' }}></div>
                  <div className="w-2 h-2 rounded-full bg-error border border-background absolute animate-pulse" style={{ left: '80%', bottom: '90%' }}></div>
                  <div className="w-2 h-2 rounded-full bg-primary border border-background absolute" style={{ left: '100%', bottom: '95%' }}></div>
                </div>
              </div>
              {/* X-axis labels */}
              <div className="absolute bottom-[-20px] left-0 right-0 flex justify-between text-[10px] font-mono-data text-on-surface-variant px-2">
                <span>D-14</span>
                <span>D-10</span>
                <span>D-5</span>
                <span>Hoy</span>
              </div>
            </div>
          </div>

          {/* Priority Alerts Table */}
          <div className="glass-card rounded-xl flex flex-col overflow-hidden">
            <div className="p-6 border-b border-white/5 flex justify-between items-center bg-surface-container/20">
              <h2 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
                <span className="material-symbols-outlined text-error">policy</span>
                Cola de Alertas Prioritarias
              </h2>
              <button 
                onClick={() => navigate('/alerts')} 
                className="text-primary hover:text-primary-fixed text-sm font-label-md flex items-center gap-1 transition-colors"
              >
                Ver Todo
                <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
              </button>
            </div>
            <div className="overflow-x-auto w-full">
              <table className="w-full text-left border-collapse min-w-[600px]">
                <thead>
                  <tr className="bg-surface-container-high/50 border-b-2 border-primary/30">
                    <th className="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">ID ALERTA</th>
                    <th className="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">PRODUCTO</th>
                    <th className="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">EXPORTADORA</th>
                    <th className="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">SEVERIDAD</th>
                    <th className="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider text-right">ACCIÓN</th>
                  </tr>
                </thead>
                <tbody className="font-mono-data text-mono-data">
                  {priority_alerts.map(alert => (
                    <tr key={alert.id_alerta} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
                      <td className="py-3 px-4 text-on-surface">{alert.id_alerta}</td>
                      <td className="py-3 px-4">
                        <span className="inline-flex items-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant border border-white/10 font-body-sm text-body-sm">
                          <span className={`w-2 h-2 rounded-full ${alert.producto === 'Palta' ? 'bg-[#4A7C59]' : alert.producto === 'Uva' ? 'bg-[#8B5A8C]' : alert.producto === 'Arándano' ? 'bg-[#3B5998]' : 'bg-[#C28C38]'} mr-2`}></span>
                          {alert.producto}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-on-surface-variant">{alert.razon_social}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
                            <div className={`h-full ${alert.score_anomalia > 0.8 ? 'bg-error' : alert.score_anomalia > 0.6 ? 'bg-secondary' : 'bg-primary-fixed-dim'}`} style={{ width: `${Math.round(alert.score_anomalia * 100)}%` }}></div>
                          </div>
                          <span className={`${alert.score_anomalia > 0.8 ? 'text-error' : alert.score_anomalia > 0.6 ? 'text-secondary' : 'text-primary-fixed-dim'} font-bold`}>{alert.score_anomalia.toFixed(2)}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <Link 
                          to={`/alert/${alert.id_alerta}`} 
                          className="inline-block px-3 py-1 bg-transparent border border-error text-error rounded hover:bg-error/10 transition-colors font-label-md text-label-md uppercase opacity-80 group-hover:opacity-100"
                        >
                          AUDITAR
                        </Link>
                      </td>
                    </tr>
                  ))}
                  {priority_alerts.length === 0 && (
                    <tr>
                      <td colSpan="5" className="py-6 text-center text-on-surface-variant">No hay alertas de prioridad pendientes.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column (Activity Feed) */}
        <div className="glass-card rounded-xl flex flex-col h-[calc(100vh-16rem)] min-h-[500px]">
          <div className="p-6 border-b border-white/5 bg-surface-container/20 shrink-0">
            <h2 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-tertiary">history</span>
              Flujo de Telemetría del Sistema
            </h2>
          </div>
          <div className="p-6 overflow-y-auto flex-1 relative">
            {/* Timeline track */}
            <div className="absolute left-8 top-6 bottom-6 w-px bg-white/10 z-0"></div>
            <ul className="space-y-6 relative z-10">
              {recent_logs.map(log => {
                const isWarning = log.evento.includes('FAIL') || log.evento.includes('UNAUTHORIZED') || log.evento.includes('ADVERTENCIA') || log.evento.includes('CRÍTICO');
                return (
                  <li key={log.id_log} className="flex gap-4">
                    <div className={`w-4 h-4 rounded-full ${isWarning ? 'bg-error shadow-[0_0_8px_rgba(255,180,171,0.6)] animate-pulse' : 'bg-primary'} border-[3px] border-background shrink-0 mt-1 relative z-10`}></div>
                    <div>
                      <div className="font-mono-data text-mono-data text-on-surface-variant text-[10px] mb-1">
                        {log.fecha.split('T')[0]} {log.fecha.split('T')[1]?.split('.')[0]} · {log.usuario}
                      </div>
                      <div className="font-body-sm text-body-sm text-on-surface font-medium">{log.evento}</div>
                    </div>
                  </li>
                );
              })}
              {recent_logs.length === 0 && (
                <li className="py-4 text-center text-on-surface-variant font-body-sm">Sin telemetría activa en este ciclo.</li>
              )}
            </ul>
          </div>
          <div className="p-4 border-t border-white/5 bg-surface-container/10 mt-auto">
            <button className="w-full text-center text-primary font-label-md text-label-md hover:text-primary-fixed transition-colors" onClick={() => navigate('/users')}>
              Cargar Registros Anteriores
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
