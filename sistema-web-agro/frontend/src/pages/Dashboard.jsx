import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, BarChart, Bar, Cell, Legend } from 'recharts'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [scatterData, setScatterData] = useState([])
  const [distributionData, setDistributionData] = useState([])
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

    fetch('/api/dashboard/fob-scatter')
      .then(res => res.json())
      .then(data => setScatterData(data))
      .catch(err => console.error('Error fetching scatter data:', err))

    fetch('/api/dashboard/fob-distribution')
      .then(res => res.json())
      .then(data => setDistributionData(data))
      .catch(err => console.error('Error fetching distribution data:', err))
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

        {/* KPI 4: Stress Tests */}
        <div className="glass-card rounded-xl p-5 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-secondary/5 to-transparent opacity-50"></div>
          <div className="relative z-10 flex flex-col h-full justify-between gap-4">
            <div className="flex justify-between items-start">
              <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">EVALUACIONES DE STRESS</span>
              <div className="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center border border-secondary/20">
                <span className="material-symbols-outlined text-secondary text-[18px]">psychology</span>
              </div>
            </div>
            <div>
              <div className="flex items-baseline gap-3">
                <span className="font-display-lg text-display-lg text-on-surface">5 Runs</span>
                <span className="flex items-center font-mono-data text-mono-data text-secondary bg-secondary/10 px-1.5 py-0.5 rounded">
                  <span className="material-symbols-outlined text-[14px]">done_all</span>
                  Robustez
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
          {/* Custom Tooltip */}
          {(() => {
            window._CustomTooltip = ({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="bg-surface-container-high border border-white/10 p-3 rounded shadow-xl font-mono-data text-mono-data text-xs">
                    <p className="text-primary font-bold">{data.id_alerta}</p>
                    <p>Cultivo: {data.producto}</p>
                    <p>FOB Declarado: ${data.valor_fob_declarado.toLocaleString()} USD</p>
                    <p>FOB Esperado: ${data.valor_fob_esperado.toLocaleString()} USD</p>
                    <p className="text-error font-bold">Desviación: {data.desviacion_pct}%</p>
                    <p>Score: {data.score_anomalia.toFixed(4)}</p>
                  </div>
                );
              }
              return null;
            };
          })()}

          {/* Charts Container */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Chart 1: FOB Scatter Plot */}
            <div className="glass-card rounded-xl p-6 h-96 flex flex-col">
              <h2 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-4">
                <span className="material-symbols-outlined text-primary">scatter_plot</span>
                FOB Declarado vs Esperado
              </h2>
              <div className="flex-1 min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 10, right: 10, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis 
                      type="number" 
                      dataKey="valor_fob_esperado" 
                      name="FOB Esperado" 
                      unit=" USD"
                      stroke="#8e918f"
                      tickFormatter={(v) => `$${v/1000}k`}
                    />
                    <YAxis 
                      type="number" 
                      dataKey="valor_fob_declarado" 
                      name="FOB Declarado" 
                      unit=" USD"
                      stroke="#8e918f"
                      tickFormatter={(v) => `$${v/1000}k`}
                    />
                    <Tooltip content={<window._CustomTooltip />} />
                    <Scatter name="Alertas" data={scatterData} fill="#ffb4ab">
                      {scatterData.map((entry, index) => {
                        const colors = {
                          'Palta': '#4A7C59',
                          'Uva': '#8B5A8C',
                          'Arándano': '#3B5998',
                          'Mango': '#C28C38'
                        };
                        return <Cell key={`cell-${index}`} fill={colors[entry.producto] || '#ffb4ab'} />;
                      })}
                    </Scatter>
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 2: Deviation Distribution */}
            <div className="glass-card rounded-xl p-6 h-96 flex flex-col">
              <h2 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-4">
                <span className="material-symbols-outlined text-primary">bar_chart</span>
                Distribución de Alertas por Desviación
              </h2>
              <div className="flex-1 min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={distributionData} margin={{ top: 10, right: 10, bottom: 20, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="rango" stroke="#8e918f" />
                    <YAxis stroke="#8e918f" allowDecimals={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'rgba(30,30,30,0.9)', borderColor: 'rgba(255,255,255,0.1)' }}
                      labelStyle={{ color: '#fff' }}
                    />
                    <Bar dataKey="cantidad" radius={[4, 4, 0, 0]}>
                      {distributionData.map((entry, index) => {
                        const colors = ['#a8c7fa', '#7fc7ff', '#ffb4ab', '#ff897a'];
                        return <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />;
                      })}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
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
