import React, { useState, useEffect } from 'react'

export default function Integrity() {
  const [stats, setStats] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch integrity statistics and history logs
    Promise.all([
      fetch('/api/integrity/stats').then(res => res.json()),
      fetch('/api/history').then(res => res.json())
    ])
      .then(([statsData, historyData]) => {
        setStats(statsData)
        setHistory(historyData)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching integrity metrics:', err)
        setLoading(false)
      })
  }, [])

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <span className="material-symbols-outlined text-primary text-5xl animate-spin">sync</span>
        <span className="ml-3 text-lg font-medium text-primary">Cargando métricas de integridad y sesgo...</span>
      </div>
    )
  }

  const {
    fpr_by_product = { 'Palta': 0.128, 'Uva': 0.060, 'Arándano': 0.052, 'Mango': 0.040 },
    recall_by_export_group = { 'Pequeño (< $100K)': 0.82, 'Mediano ($100K - $140K)': 0.91, 'Grande (>= $140K)': 0.94 },
    demographic_parity_ratio = 0.94,
    f1_score_by_port = []
  } = stats

  return (
    <div className="space-y-card-gap">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-2">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="material-symbols-outlined text-primary text-sm">gavel</span>
            <span className="font-label-md text-label-md text-primary uppercase tracking-widest">Matriz de Cumplimiento</span>
          </div>
          <h2 className="font-headline-lg text-headline-lg text-on-surface">Monitor de Integridad y Equidad (Fairness)</h2>
          <p className="font-body-sm text-body-sm text-on-surface-variant mt-1 max-w-2xl">Análisis en tiempo real de sesgo de algoritmos de auditoría, impacto dispar y paridad demográfica a través de segmentos de exportación.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="glass-panel px-4 py-2 rounded-lg flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            <span className="font-mono-data text-mono-data text-primary">SYS_NOMINAL</span>
          </div>
        </div>
      </div>

      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-card-gap">
        
        {/* Alerts Panel (High Priority Alert) */}
        <div className="md:col-span-12 xl:col-span-4 flex flex-col gap-card-gap">
          <div className="glass-card rounded-xl p-6 flex-1 relative overflow-hidden pulse-alert border-error/50">
            <div className="absolute -right-10 -top-10 w-40 h-40 bg-error/10 rounded-full blur-3xl pointer-events-none"></div>
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-headline-sm text-headline-sm text-error flex items-center gap-2 font-bold">
                <span className="material-symbols-outlined">warning</span>
                Sesgo de Algoritmo Detectado
              </h3>
              <span className="font-label-md text-label-md text-error bg-error/10 px-2 py-1 rounded">SEV_1</span>
            </div>
            
            <div className="space-y-4">
              <div className="bg-surface-container-high/50 border border-error/20 p-4 rounded-lg relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-error"></div>
                <div className="flex justify-between items-start mb-2">
                  <span className="font-label-md text-label-md text-on-surface font-semibold">Tasa de Falsos Positivos (FPR) Palta</span>
                  <span className="font-mono-data text-mono-data text-error">+14.2%</span>
                </div>
                <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">
                  El ensemble marca despachos de <strong>Palta</strong> de Pequeños Exportadores a una tasa significativamente mayor en comparación con Grandes Exportadores.
                </p>
                <div className="mt-3 flex gap-2">
                  <button className="text-[10px] uppercase tracking-wider bg-error/10 text-error px-2.5 py-1 rounded hover:bg-error/20 transition-colors">Investigar</button>
                  <button className="text-[10px] uppercase tracking-wider bg-surface-variant text-on-surface-variant px-2.5 py-1 rounded hover:bg-surface-bright transition-colors">Reconocer</button>
                </div>
              </div>
              
              <div className="bg-surface-container-high/50 border border-outline/20 p-4 rounded-lg relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-tertiary"></div>
                <div className="flex justify-between items-start mb-2">
                  <span className="font-label-md text-label-md text-on-surface font-semibold">Varianza de Tasa de Selección</span>
                  <span className="font-mono-data text-mono-data text-tertiary">Observar</span>
                </div>
                <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">
                  Ratio de Impacto Dispar para <strong>Uva</strong> aproximándose al límite crítico de 0.80. Monitorear reentrenamiento.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="md:col-span-12 xl:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-card-gap">
          {/* Global Disparate Impact */}
          <div className="glass-panel rounded-xl p-6 relative overflow-hidden group">
            <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-primary/10 to-transparent opacity-50"></div>
            <div className="flex justify-between items-start relative z-10">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-label-md text-label-md text-on-surface-variant uppercase">Impacto Dispar Global (DIR)</span>
                  <span className="material-symbols-outlined text-[16px] text-outline cursor-pointer hover:text-primary transition-colors">info</span>
                </div>
                <div className="font-display-lg text-display-lg text-primary">{demographic_parity_ratio}</div>
              </div>
              <div className="glass-panel p-2 rounded flex flex-col items-center justify-center">
                <span className="material-symbols-outlined text-primary mb-1">balance</span>
                <span className="font-mono-data text-[10px] text-primary">JUSTO</span>
              </div>
            </div>
            {/* Sparkline */}
            <div className="h-8 mt-4 flex items-end gap-1 opacity-60">
              <div className="w-full bg-primary/20 h-[60%] rounded-t-sm"></div>
              <div className="w-full bg-primary/40 h-[70%] rounded-t-sm"></div>
              <div className="w-full bg-primary/30 h-[65%] rounded-t-sm"></div>
              <div className="w-full bg-primary/60 h-[80%] rounded-t-sm"></div>
              <div className="w-full bg-primary/80 h-[90%] rounded-t-sm"></div>
              <div className="w-full bg-primary h-[94%] rounded-t-sm relative">
                <div className="absolute -top-1 left-1/2 w-1.5 h-1.5 bg-white rounded-full transform -translate-x-1/2 shadow-[0_0_5px_#fff]"></div>
              </div>
            </div>
          </div>

          {/* Equal Opportunity Difference */}
          <div className="glass-panel rounded-xl p-6 relative overflow-hidden group">
            <div className="flex justify-between items-start relative z-10">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-label-md text-label-md text-on-surface-variant uppercase">Δ Igualdad Oportunidades</span>
                  <span className="material-symbols-outlined text-[16px] text-outline cursor-pointer hover:text-primary transition-colors">info</span>
                </div>
                <div className="font-display-lg text-display-lg text-on-surface flex items-baseline gap-1">
                  -0.03 <span className="text-sm font-mono-data text-outline">Δ</span>
                </div>
              </div>
              <div className="glass-panel p-2 rounded flex flex-col items-center justify-center">
                <span className="material-symbols-outlined text-tertiary mb-1">analytics</span>
                <span className="font-mono-data text-[10px] text-tertiary">ESTABLE</span>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-white/5 flex justify-between font-mono-data text-[11px] mt-auto">
              <span className="text-on-surface-variant">Límites: ±0.05</span>
              <span className="text-primary">Dentro de Paridad</span>
            </div>
          </div>

          {/* Bar Chart: FPR Parity by product */}
          <div className="glass-panel rounded-xl p-6 md:col-span-2 flex flex-col">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="font-headline-sm text-headline-sm text-on-surface">Paridad FPR: Categoría de Producto</h3>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Tasa de Falsos Positivos (FPR) por producto (Ideal: FPR estable entre cultivos)</p>
              </div>
              <div className="flex gap-4">
                <span className="flex items-center gap-1 font-label-md text-[10px] text-on-surface-variant"><div className="w-2 h-2 rounded bg-primary"></div> Umbral (0.05)</span>
                <span className="flex items-center gap-1 font-label-md text-[10px] text-on-surface-variant"><div className="w-2 h-2 rounded bg-error"></div> Exceso</span>
              </div>
            </div>
            
            {/* Custom Bar Graph */}
            <div className="flex-grow relative pt-4 pb-6 min-h-[165px] flex items-end justify-around">
              <div className="absolute left-0 top-0 h-full flex flex-col justify-between font-mono-data text-[10px] text-outline pb-6">
                <span>0.15</span>
                <span>0.10</span>
                <span>0.05</span>
                <span>0.00</span>
              </div>
              <div className="w-full flex justify-around pl-8 h-full items-end z-10 relative">
                {/* Horizontal reference line for 0.05 */}
                <div className="absolute w-full h-[1px] bg-primary/40 top-[66%] border-t border-dashed border-primary/50 z-0"></div>
                
                {Object.entries(fpr_by_product).map(([prod, fprVal]) => {
                  // Max height representation mapping (0.15 is 100%)
                  const heightPct = Math.min((fprVal / 0.15) * 100, 100)
                  const isHigh = fprVal > 0.07
                  return (
                    <div key={prod} className="w-16 h-full flex items-end justify-center group relative cursor-pointer">
                      <div 
                        className={`w-10 rounded-t transition-all duration-300 ${isHigh ? 'bg-error/80 border-t border-error shadow-[0_0_15px_rgba(255,180,171,0.2)]' : 'bg-secondary/80 border-t border-secondary'} group-hover:opacity-100`}
                        style={{ height: `${heightPct}%` }}
                      ></div>
                      <span className="absolute -bottom-6 font-mono-data text-[10px] text-on-surface">{prod.toUpperCase()}</span>
                      <div className="absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity glass-modal px-2 py-1 rounded text-[11px] font-mono-data text-primary whitespace-nowrap z-20 pointer-events-none">
                        FPR: {fprVal.toFixed(3)}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Secondary charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-card-gap">
        
        {/* Recall per Export Group */}
        <div className="glass-panel rounded-xl p-6 flex flex-col h-[300px]">
          <h3 className="font-headline-sm text-headline-sm text-on-surface mb-1">Sensibilidad por Tamaño de Agroexportadora</h3>
          <p className="font-body-sm text-body-sm text-on-surface-variant mb-4">Tasa de Verdaderos Positivos (Recall) por nivel de volumen de exportación</p>
          <div className="flex-grow flex flex-col justify-center space-y-4">
            {Object.entries(recall_by_export_group).map(([groupName, recallVal]) => (
              <div key={groupName} className="space-y-1">
                <div className="flex justify-between font-mono-data text-xs">
                  <span className="text-on-surface">{groupName}</span>
                  <span className="text-primary font-bold">{recallVal.toFixed(2)}</span>
                </div>
                <div className="h-2 w-full bg-surface-container-high rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary/80 rounded-full shadow-[0_0_8px_#76db8f]" 
                    style={{ width: `${recallVal * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* F1-Score by destination port */}
        <div className="glass-panel rounded-xl flex flex-col h-[300px] overflow-hidden">
          <div className="p-6 pb-2">
            <h3 className="font-headline-sm text-headline-sm text-on-surface">Puntaje F1 por Puerto de Destino</h3>
            <p className="font-body-sm text-body-sm text-on-surface-variant">Media armónica de precisión y sensibilidad por nodo logístico</p>
          </div>
          <div className="flex-1 overflow-auto">
            <table className="w-full text-left border-collapse">
              <thead className="bg-surface-container-high/50 border-b border-primary/30 sticky top-0 z-10">
                <tr>
                  <th className="p-3 pl-6 font-label-md text-label-md text-on-surface-variant uppercase">Nodo Portuario</th>
                  <th className="p-3 font-label-md text-label-md text-on-surface-variant uppercase">Vol (TEU)</th>
                  <th className="p-3 pr-6 font-label-md text-label-md text-on-surface-variant uppercase text-right">Puntaje F1</th>
                </tr>
              </thead>
              <tbody className="font-mono-data text-[13px] divide-y divide-white/5">
                {f1_score_by_port.map((row, idx) => (
                  <tr key={idx} className="hover:bg-white/5 transition-colors">
                    <td className="p-3 pl-6 text-on-surface flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${row.f1_score >= 0.9 ? 'bg-primary' : row.f1_score >= 0.8 ? 'bg-tertiary' : 'bg-error animate-pulse'}`}></span>
                      {row.puerto}
                    </td>
                    <td className="p-3 text-on-surface-variant">{row.volumen.toLocaleString()}</td>
                    <td className={`p-3 pr-6 text-right font-bold ${row.f1_score >= 0.9 ? 'text-primary' : row.f1_score >= 0.8 ? 'text-tertiary' : 'text-error'}`}>{row.f1_score.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      {/* Logs Section */}
      <div className="glass-panel rounded-xl flex flex-col overflow-hidden mb-8">
        <div className="p-6 pb-2">
          <h3 className="font-headline-sm text-headline-sm text-on-surface">Logs de Decisiones del Experimento</h3>
        </div>
        <div className="flex-grow overflow-auto max-h-[300px]">
          <table className="w-full text-left border-collapse">
            <thead className="bg-surface-container-high/50 border-b border-primary/30 sticky top-0 z-10 font-label-md text-label-md text-on-surface-variant uppercase">
              <tr>
                <th className="p-3 pl-6">ID Decisión</th>
                <th className="p-3">ID Alerta</th>
                <th className="p-3">CONDICIÓN</th>
                <th className="p-3">DECISIÓN</th>
                <th className="p-3">PUNTAJE COMP.</th>
                <th className="p-3 pr-6 text-right">TIEMPO (MS)</th>
              </tr>
            </thead>
            <tbody className="font-mono-data text-[13px] divide-y divide-white/5 text-on-surface">
              {history.map((d, index) => (
                <tr key={index} className="hover:bg-white/5 transition-colors">
                  <td className="p-3 pl-6 text-on-surface-variant">DEC-{1000 + d.id_decision}</td>
                  <td className="p-3 text-primary font-bold">{d.id_alerta}</td>
                  <td className="p-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] ${d.condicion_experimento === 'INTEGRADO' ? 'bg-primary/10 text-primary border border-primary/20' : 'bg-secondary/10 text-secondary border border-secondary/20'}`}>
                      {d.condicion_experimento}
                    </span>
                  </td>
                  <td className="p-3">
                    {d.user_decision === 1 && 'Confirmada'}
                    {d.user_decision === 0 && 'Falsa Alarma'}
                    {d.user_decision === 2 && 'Inspección'}
                  </td>
                  <td className="p-3 text-center">
                    <div className="flex items-center gap-0.5 text-primary">
                      {Array.from({ length: d.likert_comprehension }).map((_, i) => (
                        <span key={i} className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
                      ))}
                    </div>
                  </td>
                  <td className="p-3 pr-6 text-right text-secondary font-bold">{d.time_to_decision_ms.toLocaleString()}</td>
                </tr>
              ))}
              {history.length === 0 && (
                <tr>
                  <td colSpan="6" className="p-6 text-center text-on-surface-variant">Sin logs de telemetría registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
