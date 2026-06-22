import React, { useState, useEffect } from 'react'

export default function Telemetry() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchStats = () => {
    setLoading(true)
    fetch('/api/telemetry/stats')
      .then(res => res.json())
      .then(data => {
        setStats(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching telemetry stats:', err)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchStats()
  }, [])

  // Function to export telemetry data to JSON/CSV on the client side
  const exportTelemetry = (format) => {
    if (!stats) return
    
    // Simulate fetching full history to export
    fetch('/api/history')
      .then(res => res.json())
      .then(data => {
        let content = ''
        let filename = `telemetria_experimento.${format}`
        let mimeType = 'text/plain'

        if (format === 'json') {
          content = JSON.stringify(data, null, 2)
          mimeType = 'application/json'
        } else {
          // CSV Format
          const headers = ['id_decision', 'id_alerta', 'numero_dam', 'producto', 'usuario_nombre', 'condicion_experimento', 'user_decision', 'likert_comprehension', 'time_to_decision_ms', 'creado_en']
          const rows = data.map(d => headers.map(h => {
            const val = d[h]
            return typeof val === 'string' ? `"${val.replace(/"/g, '""')}"` : val
          }).join(','))
          
          content = [headers.join(','), ...rows].join('\n')
          mimeType = 'text/csv'
        }

        const blob = new Blob([content], { type: mimeType })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        URL.revokeObjectURL(url)
      })
  }

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <span className="material-symbols-outlined text-primary text-5xl animate-spin">sync</span>
        <span className="ml-3 text-lg font-medium text-primary">Cargando métricas del experimento...</span>
      </div>
    )
  }

  const {
    avg_time_integrado_s = 0,
    avg_time_aislado_s = 0,
    avg_comp_integrado = 0,
    avg_comp_aislado = 0,
    boxplot_integrado = {},
    boxplot_aislado = {},
    operativos_progress = []
  } = stats

  // Render Boxplot Calculations using CSS percentages
  // Assume chart Y-axis max is 80 seconds
  const CHART_MAX = 80
  const getPct = (val) => Math.min((val / CHART_MAX) * 100, 100)

  // Map values to percent heights
  const bi = boxplot_integrado
  const ba = boxplot_aislado

  const bi_min = getPct(bi.min)
  const bi_q1 = getPct(bi.q1)
  const bi_med = getPct(bi.median)
  const bi_q3 = getPct(bi.q3)
  const bi_max = getPct(bi.max)

  const ba_min = getPct(ba.min)
  const ba_q1 = getPct(ba.q1)
  const ba_med = getPct(ba.median)
  const ba_q3 = getPct(ba.q3)
  const ba_max = getPct(ba.max)

  return (
    <div className="space-y-card-gap">
      {/* Header Section */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-4">
        <div>
          <h1 className="font-display-lg text-display-lg text-on-surface">Telemetría del Experimento</h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant mt-2 max-w-2xl">Análisis en tiempo real de matrices de decisión, latencia cognitiva e indicadores Likert por condición A/B.</p>
        </div>
        <div className="flex gap-4">
          <button 
            className="glass-panel px-6 py-3 rounded-lg flex items-center gap-2 text-primary hover:bg-primary/10 transition-colors border-primary/30 font-semibold"
            onClick={() => exportTelemetry('json')}
          >
            <span className="material-symbols-outlined">file_download</span>
            <span className="font-label-md text-label-md uppercase tracking-wider">Exportar JSON</span>
          </button>
          <button 
            className="bg-primary text-on-primary px-6 py-3 rounded-lg flex items-center gap-2 hover:bg-primary-fixed transition-colors font-label-md text-label-md uppercase tracking-wider shadow-[0_0_15px_rgba(118,219,143,0.3)] hover:shadow-[0_0_25px_rgba(118,219,143,0.5)] font-semibold"
            onClick={() => exportTelemetry('csv')}
          >
            <span className="material-symbols-outlined">table_view</span>
            Exportar CSV
          </button>
        </div>
      </header>

      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-card-gap">
        
        {/* KPI: Avg Decision Time */}
        <div className="glass-panel rounded-xl p-6 lg:col-span-3 flex flex-col relative overflow-hidden">
          <div className="absolute inset-0 opacity-20 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary-container via-transparent to-transparent pointer-events-none"></div>
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Tiempo Medio de Decisión (vd4-a)</h3>
            <span className="material-symbols-outlined text-primary">timer</span>
          </div>
          <div className="flex items-end gap-4 mt-auto">
            <div>
              <div className="font-label-md text-label-md text-on-surface-variant mb-1">Condición A</div>
              <div className="font-display-lg text-display-lg text-error">
                {avg_time_integrado_s.toFixed(1)}<span className="font-headline-sm text-headline-sm text-on-surface-variant ml-1">s</span>
              </div>
            </div>
            <div className="h-12 w-[1px] bg-white/10 mb-2"></div>
            <div>
              <div className="font-label-md text-label-md text-on-surface-variant mb-1">Condición B</div>
              <div className="font-display-lg text-display-lg text-primary">
                {avg_time_aislado_s.toFixed(1)}<span className="font-headline-sm text-headline-sm text-on-surface-variant ml-1">s</span>
              </div>
            </div>
          </div>
          <div className="mt-4 h-1 w-full bg-white/5 rounded-full overflow-hidden flex">
            {/* Display proportion of time spent */}
            <div 
              className="bg-error h-full" 
              style={{ width: `${(avg_time_integrado_s / (avg_time_integrado_s + avg_time_aislado_s || 1)) * 100}%` }}
            ></div>
            <div 
              className="bg-primary h-full" 
              style={{ width: `${(avg_time_aislado_s / (avg_time_integrado_s + avg_time_aislado_s || 1)) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* KPI: Avg Comprehension */}
        <div className="glass-panel rounded-xl p-6 lg:col-span-3 flex flex-col relative overflow-hidden">
          <div className="absolute inset-0 opacity-20 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-tertiary-container via-transparent to-transparent pointer-events-none"></div>
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Comprensión Percibida (vd4-b)</h3>
            <span className="material-symbols-outlined text-tertiary">psychology</span>
          </div>
          <div className="flex items-end gap-4 mt-auto">
            <div>
              <div className="font-label-md text-label-md text-on-surface-variant mb-1">Condición A</div>
              <div className="font-display-lg text-display-lg text-tertiary">
                {avg_comp_integrado.toFixed(1)}<span className="font-headline-sm text-headline-sm text-on-surface-variant ml-1">/5</span>
              </div>
            </div>
            <div className="h-12 w-[1px] bg-white/10 mb-2"></div>
            <div>
              <div className="font-label-md text-label-md text-on-surface-variant mb-1">Condición B</div>
              <div className="font-display-lg text-display-lg text-error">
                {avg_comp_aislado.toFixed(1)}<span className="font-headline-sm text-headline-sm text-on-surface-variant ml-1">/5</span>
              </div>
            </div>
          </div>
          
          {/* Render 5 bars for rating */}
          <div className="mt-4 flex gap-1">
            {[1, 2, 3, 4, 5].map(i => {
              const active = i <= Math.round(avg_comp_integrado)
              return (
                <div key={i} className={`h-1 flex-1 rounded-full ${active ? 'bg-tertiary shadow-[0_0_5px_rgba(137,206,255,0.5)]' : 'bg-white/10'}`}></div>
              )
            })}
          </div>
        </div>

        {/* Boxplot Visualization */}
        <div className="glass-panel rounded-xl p-6 lg:col-span-6 flex flex-col h-[320px]">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-headline-sm text-headline-sm text-on-surface">Tiempos de Decisión por Condición (Boxplot)</h3>
            <span className="material-symbols-outlined text-on-surface-variant">candlestick_chart</span>
          </div>
          
          <div className="flex-1 relative min-h-[180px] flex items-center justify-center">
            <div className="w-full h-full flex flex-col justify-between py-4 relative">
              {/* Y-axis labels */}
              <div className="absolute left-0 top-0 bottom-0 flex flex-col justify-between font-mono-data text-mono-data text-on-surface-variant text-[10px] py-1 z-10">
                <span>{CHART_MAX}s</span>
                <span>{CHART_MAX * 0.75}s</span>
                <span>{CHART_MAX * 0.5}s</span>
                <span>{CHART_MAX * 0.25}s</span>
                <span>0s</span>
              </div>
              
              {/* Grid lines */}
              <div className="absolute left-8 right-0 top-0 border-t border-white/5 h-1/4"></div>
              <div className="absolute left-8 right-0 top-1/4 border-t border-white/5 h-1/4"></div>
              <div className="absolute left-8 right-0 top-2/4 border-t border-white/5 h-1/4"></div>
              <div className="absolute left-8 right-0 top-3/4 border-t border-white/5 h-1/4"></div>
              <div className="absolute left-8 right-0 bottom-0 border-t border-white/20"></div>
              
              {/* Boxplots container */}
              <div className="absolute left-8 right-0 top-0 bottom-0 flex justify-around items-end pb-8">
                
                {/* Boxplot A (INTEGRADO - Red/Orange Theme) */}
                <div className="relative w-20 h-full flex flex-col justify-end items-center group">
                  {/* Whisker vertical line */}
                  <div className="absolute bg-error/50 w-[1px]" style={{ bottom: `${bi_min}%`, height: `${bi_max - bi_min}%` }}></div>
                  {/* Whisker caps */}
                  <div className="absolute w-4 h-[1px] bg-error/50" style={{ bottom: `${bi_min}%` }}></div>
                  <div className="absolute w-4 h-[1px] bg-error/50" style={{ bottom: `${bi_max}%` }}></div>
                  
                  {/* Box body */}
                  <div 
                    className="absolute w-full bg-error/15 border border-error/50 rounded-sm backdrop-blur-sm transition-all group-hover:bg-error/25 flex flex-col justify-center relative" 
                    style={{ bottom: `${bi_q1}%`, height: `${bi_q3 - bi_q1}%` }}
                  >
                    {/* Median Line */}
                    <div 
                      className="absolute w-full h-[2px] bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)]"
                      style={{ bottom: `${((bi_med - bi_q1) / (bi_q3 - bi_q1 || 1)) * 100}%` }}
                    ></div>
                  </div>
                  <span className="absolute -bottom-6 font-label-md text-label-md text-on-surface-variant font-mono-data">Cond. A (Exp)</span>
                  
                  {/* Tooltip detail */}
                  <div className="absolute bg-surface-container border border-error/30 p-2.5 rounded-lg text-[10px] font-mono-data opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none shadow-2xl z-30 bottom-1/2 left-full ml-2 w-36 space-y-1">
                    <div className="font-bold text-error border-b border-white/10 pb-1 mb-1">CONDICIÓN A</div>
                    <div>Max: {bi.max}s</div>
                    <div>Q3: {bi.q3}s</div>
                    <div>Med: {bi.median}s</div>
                    <div>Q1: {bi.q1}s</div>
                    <div>Min: {bi.min}s</div>
                  </div>
                </div>

                {/* Boxplot B (AISLADO - Green Theme) */}
                <div className="relative w-20 h-full flex flex-col justify-end items-center group">
                  {/* Whisker vertical line */}
                  <div className="absolute bg-primary/50 w-[1px]" style={{ bottom: `${ba_min}%`, height: `${ba_max - ba_min}%` }}></div>
                  {/* Whisker caps */}
                  <div className="absolute w-4 h-[1px] bg-primary/50" style={{ bottom: `${ba_min}%` }}></div>
                  <div className="absolute w-4 h-[1px] bg-primary/50" style={{ bottom: `${ba_max}%` }}></div>
                  
                  {/* Box body */}
                  <div 
                    className="absolute w-full bg-primary/15 border border-primary/50 rounded-sm backdrop-blur-sm transition-all group-hover:bg-primary/25 flex flex-col justify-center relative" 
                    style={{ bottom: `${ba_q1}%`, height: `${ba_q3 - ba_q1}%` }}
                  >
                    {/* Median Line */}
                    <div 
                      className="absolute w-full h-[2px] bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)]"
                      style={{ bottom: `${((ba_med - ba_q1) / (ba_q3 - ba_q1 || 1)) * 100}%` }}
                    ></div>
                  </div>
                  <span className="absolute -bottom-6 font-label-md text-label-md text-on-surface-variant font-mono-data">Cond. B (Aisl)</span>
                  
                  {/* Tooltip detail */}
                  <div className="absolute bg-surface-container border border-primary/30 p-2.5 rounded-lg text-[10px] font-mono-data opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none shadow-2xl z-30 bottom-1/2 left-full ml-2 w-36 space-y-1">
                    <div className="font-bold text-primary border-b border-white/10 pb-1 mb-1">CONDICIÓN B</div>
                    <div>Max: {ba.max}s</div>
                    <div>Q3: {ba.q3}s</div>
                    <div>Med: {ba.median}s</div>
                    <div>Q1: {ba.q1}s</div>
                    <div>Min: {ba.min}s</div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Grid: Scatter Plot & Progress Table */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-card-gap mb-8">
        
        {/* Scatter Plot placeholder */}
        <div className="lg:col-span-4 glass-panel rounded-xl p-6 flex flex-col h-[350px]">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-headline-sm text-headline-sm text-on-surface">Comprensión vs Tiempo</h3>
            <span className="material-symbols-outlined text-on-surface-variant">scatter_plot</span>
          </div>
          <div className="flex-1 relative bg-surface-container-low/50 rounded-lg border border-white/5 p-4 overflow-hidden flex items-center justify-center">
            {/* Draw a simplified grid of scatter points representing test data */}
            <div className="absolute bottom-4 left-4 right-4 h-[1px] bg-white/20"></div>
            <div className="absolute bottom-4 left-4 top-4 w-[1px] bg-white/20"></div>
            <span className="absolute bottom-0 right-4 font-mono-data text-[8px] text-on-surface-variant">Tiempo (s)</span>
            <span className="absolute top-4 left-1 -rotate-90 font-mono-data text-[8px] text-on-surface-variant origin-left">Comprensión</span>
            
            {/* Scatter Dots - Condición A (Red) */}
            <div className="absolute top-[20%] left-[65%] w-2.5 h-2.5 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)] animate-pulse"></div>
            <div className="absolute top-[12%] left-[75%] w-2.5 h-2.5 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)]"></div>
            <div className="absolute top-[30%] left-[58%] w-2.5 h-2.5 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)]"></div>
            <div className="absolute top-[25%] left-[80%] w-2.5 h-2.5 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)]"></div>
            
            {/* Scatter Dots - Condición B (Green) */}
            <div className="absolute top-[65%] left-[25%] w-2.5 h-2.5 rounded-full bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)] animate-pulse"></div>
            <div className="absolute top-[75%] left-[18%] w-2.5 h-2.5 rounded-full bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)]"></div>
            <div className="absolute top-[52%] left-[38%] w-2.5 h-2.5 rounded-full bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)]"></div>
            
            <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 0 }}>
              <line stroke="rgba(118,219,143,0.15)" strokeDasharray="4" strokeWidth="1.5" x1="10%" x2="50%" y1="90%" y2="45%"></line>
              <line stroke="rgba(255,180,171,0.15)" strokeDasharray="4" strokeWidth="1.5" x1="50%" x2="90%" y1="35%" y2="15%"></line>
            </svg>
            <span className="text-[10px] text-on-surface-variant font-mono-data absolute bg-black/60 px-2 py-1 border border-white/5 rounded backdrop-blur">
              Tendencia: Alta comprensión con más latencia
            </span>
          </div>
        </div>

        {/* Real-time Participant Progress */}
        <div className="lg:col-span-8 glass-panel rounded-xl p-0 flex flex-col h-[350px] overflow-hidden">
          <div className="p-6 border-b border-white/5 flex justify-between items-center bg-surface-container-low/30">
            <div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface">Progreso del Experimento en Tiempo Real</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Mapeo del total de alertas auditadas por tester asignado.</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary"></span>
              </span>
              <span className="font-mono-data text-mono-data text-primary text-xs font-bold">MONITOR_VIVO</span>
            </div>
          </div>
          
          <div className="flex-1 overflow-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-white/[0.02] border-b border-primary/20 font-label-md text-label-md text-on-surface-variant uppercase">
                  <th className="py-3 px-6">ID Sujeto / Nombre</th>
                  <th className="py-3 px-6">Condición Asignada</th>
                  <th className="py-3 px-6">Alertas Auditadas</th>
                  <th className="py-3 px-6">Precisión Consenso</th>
                  <th className="py-3 px-6 text-right">Estado red</th>
                </tr>
              </thead>
              <tbody className="font-mono-data text-mono-data divide-y divide-white/5 text-on-surface">
                {operativos_progress.map(op => (
                  <tr key={op.username} className="hover:bg-white/5 transition-colors">
                    <td className="py-3.5 px-6 font-semibold">{op.nombre} <span className="text-[10px] text-on-surface-variant">({op.username})</span></td>
                    <td className="py-3.5 px-6">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${op.condicion === 'INTEGRADO' ? 'bg-error/10 text-error border border-error/20' : 'bg-primary/10 text-primary border border-primary/20'}`}>
                        {op.condicion === 'INTEGRADO' ? 'Condición A' : 'Condición B'}
                      </span>
                    </td>
                    <td className="py-3.5 px-6 text-on-surface-variant">{op.sesiones_adjudicadas} / {op.total_sesiones}</td>
                    <td className="py-3.5 px-6">
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-white/10 rounded-full h-1.5 overflow-hidden">
                          <div className={`h-full ${op.success_rate > 80 ? 'bg-primary' : 'bg-error'}`} style={{ width: `${op.success_rate}%` }}></div>
                        </div>
                        <span className={op.success_rate > 80 ? 'text-primary' : 'text-error'}>{op.success_rate}%</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-6 text-right">
                      {op.online ? (
                        <span className="material-symbols-outlined text-primary text-sm" title="Online">wifi</span>
                      ) : (
                        <span className="material-symbols-outlined text-on-surface-variant opacity-50 text-sm" title="Offline">wifi_off</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  )
}
