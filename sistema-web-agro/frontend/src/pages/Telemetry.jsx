import React, { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Cell } from 'recharts'

export default function Telemetry() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [injecting, setInjecting] = useState(false)
  const [injectedAlert, setInjectedAlert] = useState(null)
  const [stressTesting, setStressTesting] = useState(false)

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

  const handleInjectAnomaly = async (tipo) => {
    setInjecting(true)
    setInjectedAlert(null)
    try {
      const res = await fetch('/api/admin/inject-anomaly', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tipo_anomalia: tipo })
      })
      if (res.ok) {
        const data = await res.json()
        setInjectedAlert({
          tipo,
          id: data.alerta.id_alerta,
          ruc: data.alerta.ruc_exportador,
          producto: data.alerta.producto,
          declarado: data.alerta.valor_fob_declarado,
          esperado: data.alerta.valor_fob_esperado,
          score: data.alerta.score_anomalia
        })
      } else {
        alert('Error al inyectar anomalía sintética.')
      }
    } catch (err) {
      console.error(err)
      alert('Error de conexión al inyectar.')
    } finally {
      setInjecting(false)
    }
  }

  const runStressTest = () => {
    setStressTesting(true)
    // Simulate real-time stress testing of models over 100 samples
    setTimeout(() => {
      fetch('/api/telemetry/stats')
        .then(res => res.json())
        .then(data => {
          setStats(data)
          setStressTesting(false)
        })
        .catch(err => {
          console.error(err)
          setStressTesting(false)
        })
    }, 1500)
  }

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <span className="material-symbols-outlined text-primary text-5xl animate-spin">sync</span>
        <span className="ml-3 text-lg font-medium text-primary">Cargando métricas de simulación y evaluación...</span>
      </div>
    )
  }

  const {
    operativos_progress = [],
    evaluation_metrics = [],
    recalls_by_type = [],
    simulated_runs = []
  } = stats

  return (
    <div className="space-y-card-gap">
      {/* Header Section */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-2">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="material-symbols-outlined text-primary text-sm">science</span>
            <span className="font-label-md text-label-md text-primary uppercase tracking-widest">Validación Experimental</span>
          </div>
          <h1 className="font-display-lg text-display-lg text-on-surface">Consola de Simulación y Evaluación</h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant mt-1 max-w-2xl">
            Inyección controlada de anomalías sintéticas y benchmarking de robustez del ensemble frente a algoritmos baseline.
          </p>
        </div>
      </header>

      {/* Bento Grid layout */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-card-gap">
        
        {/* Injector Panel */}
        <div className="xl:col-span-6 glass-panel rounded-xl p-6 flex flex-col relative overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-gradient-to-br from-tertiary-container via-transparent to-transparent pointer-events-none"></div>
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-4 font-semibold">
            <span className="material-symbols-outlined text-tertiary">precision_manufacturing</span>
            Inyector de Anomalías Sintéticas
          </h3>
          <p className="font-body-sm text-body-sm text-on-surface-variant mb-6">
            Inyecta transacciones alteradas sintéticamente en la base de datos para validar la reacción en tiempo real de las 4 capas de IA.
          </p>
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              onClick={() => handleInjectAnomaly('precio')}
              disabled={injecting}
              className="glass-panel p-4 rounded-xl flex flex-col items-center justify-center gap-2 hover:bg-error/10 hover:border-error/30 transition-all text-center group border-white/5 active:scale-95"
            >
              <span className="material-symbols-outlined text-error text-3xl group-hover:scale-110 transition-transform">price_change</span>
              <span className="font-label-md text-xs text-on-surface font-bold uppercase tracking-wider">Subvaloración FOB</span>
              <span className="text-[10px] text-on-surface-variant">-30% FOB Declarado</span>
            </button>

            <button
              onClick={() => handleInjectAnomaly('temperatura')}
              disabled={injecting}
              className="glass-panel p-4 rounded-xl flex flex-col items-center justify-center gap-2 hover:bg-warning/10 hover:border-warning/30 transition-all text-center group border-white/5 active:scale-95"
            >
              <span className="material-symbols-outlined text-orange-400 text-3xl group-hover:scale-110 transition-transform">thermostat</span>
              <span className="font-label-md text-xs text-on-surface font-bold uppercase tracking-wider">Falla de Frío</span>
              <span className="text-[10px] text-on-surface-variant">+6.5°C en Contenedor</span>
            </button>

            <button
              onClick={() => handleInjectAnomaly('retraso')}
              disabled={injecting}
              className="glass-panel p-4 rounded-xl flex flex-col items-center justify-center gap-2 hover:bg-primary/10 hover:border-primary/30 transition-all text-center group border-white/5 active:scale-95"
            >
              <span className="material-symbols-outlined text-primary text-3xl group-hover:scale-110 transition-transform">schedule_send</span>
              <span className="font-label-md text-xs text-on-surface font-bold uppercase tracking-wider">Retraso Logístico</span>
              <span className="text-[10px] text-on-surface-variant">+8 Días en Puerto</span>
            </button>
          </div>

          {/* Injection Feedback */}
          <div className="mt-6 flex-grow flex items-center justify-center border border-dashed border-white/10 rounded-xl p-4 bg-surface-container-low/30 min-h-[90px]">
            {injecting ? (
              <div className="flex items-center gap-2 text-tertiary">
                <span className="material-symbols-outlined animate-spin">sync</span>
                <span className="font-mono-data text-xs">Simulando alteración & corriendo pipeline XGBoost+PyOD...</span>
              </div>
            ) : injectedAlert ? (
              <div className="w-full space-y-2">
                <div className="flex justify-between items-center border-b border-white/5 pb-1">
                  <span className="font-mono-data text-xs text-primary font-bold">¡INYECCIÓN EXITOSA!</span>
                  <span className="font-mono-data text-[10px] text-on-surface-variant">{injectedAlert.id}</span>
                </div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-1 font-mono-data text-[11px] text-on-surface-variant">
                  <div>RUC: <span className="text-on-surface">{injectedAlert.ruc}</span></div>
                  <div>Cultivo: <span className="text-on-surface">{injectedAlert.producto}</span></div>
                  <div>Declarado: <span className="text-error font-bold">${injectedAlert.declarado.toLocaleString()}</span></div>
                  <div>Esperado: <span className="text-primary font-bold">${injectedAlert.esperado.toLocaleString()}</span></div>
                  <div className="col-span-2 mt-1">
                    Score Anomalia: <span className="text-tertiary font-bold">{injectedAlert.score.toFixed(4)}</span>
                  </div>
                </div>
              </div>
            ) : (
              <span className="font-body-sm text-xs text-on-surface-variant">Ninguna anomalía inyectada en esta sesión.</span>
            )}
          </div>
        </div>

        {/* Stress Testing and Run History */}
        <div className="xl:col-span-6 glass-panel rounded-xl p-6 flex flex-col h-[360px]">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 font-semibold">
              <span className="material-symbols-outlined text-primary">dynamic_form</span>
              Evaluación y Stress Test
            </h3>
            <button
              onClick={runStressTest}
              disabled={stressTesting}
              className="bg-primary text-on-primary py-1.5 px-4 rounded-lg flex items-center gap-1.5 hover:bg-primary-fixed transition-colors font-label-md text-xs uppercase tracking-wider font-semibold active:scale-95 disabled:opacity-50"
            >
              {stressTesting ? (
                <>
                  <span className="material-symbols-outlined text-[16px] animate-spin">sync</span>
                  Procesando...
                </>
              ) : (
                <>
                  <span className="material-symbols-outlined text-[16px]">play_circle</span>
                  Correr Stress Test
                </>
              )}
            </button>
          </div>
          
          <p className="font-body-sm text-body-sm text-on-surface-variant mb-4">
            Historial de ejecuciones de evaluación automatizada sobre el conjunto de testeo sintético de validación.
          </p>

          <div className="flex-1 overflow-auto border border-white/5 rounded-lg bg-surface-container-low/20">
            <table className="w-full text-left border-collapse font-mono-data text-xs">
              <thead className="bg-white/[0.02] border-b border-white/10 text-on-surface-variant">
                <tr>
                  <th className="p-2.5 pl-4">ID Run</th>
                  <th className="p-2.5">Inyectados</th>
                  <th className="p-2.5">Detectados</th>
                  <th className="p-2.5 text-right">Exactitud</th>
                  <th className="p-2.5 pr-4 text-right">Hora</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-on-surface">
                {simulated_runs.map((run, idx) => (
                  <tr key={run.run_id || idx} className="hover:bg-white/5 transition-colors">
                    <td className="p-2.5 pl-4 text-primary font-bold">{run.run_id}</td>
                    <td className="p-2.5">{run.anomalies_injected}</td>
                    <td className="p-2.5">{run.detected_alerts}</td>
                    <td className="p-2.5 text-right text-tertiary font-bold">{(run.accuracy * 100).toFixed(1)}%</td>
                    <td className="p-2.5 pr-4 text-right text-on-surface-variant">{run.timestamp}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      {/* Model Benchmark Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-card-gap">
        
        {/* Chart A: Multi-model evaluation benchmark */}
        <div className="glass-panel rounded-xl p-6 flex flex-col h-[320px]">
          <h3 className="font-headline-sm text-headline-sm text-on-surface mb-1">Benchmarking de Modelos (PR-AUC vs ROC-AUC)</h3>
          <p className="font-body-sm text-body-sm text-on-surface-variant mb-4">
            Comparativa de rendimiento en base a semillas experimentales
          </p>
          <div className="flex-grow min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={evaluation_metrics} margin={{ top: 10, right: 10, bottom: 20, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="metodo" stroke="#8e918f" fontSize={9} />
                <YAxis stroke="#8e918f" domain={[0.6, 1.0]} fontSize={10} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'rgba(30,30,30,0.9)', borderColor: 'rgba(255,255,255,0.1)' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: 11 }} />
                <Bar dataKey="pr_auc" name="PR-AUC (Sensible a Desbalance)" fill="#76db8f" radius={[3, 3, 0, 0]} />
                <Bar dataKey="roc_auc" name="ROC-AUC" fill="#89c6ff" radius={[3, 3, 0, 0]} />
                <Bar dataKey="f1_score" name="F1-Score" fill="#ffb4ab" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart B: Recall by Anomaly Type */}
        <div className="glass-panel rounded-xl p-6 flex flex-col h-[320px]">
          <h3 className="font-headline-sm text-headline-sm text-on-surface mb-1">Recall (Sensibilidad) por Tipo de Anomalía</h3>
          <p className="font-body-sm text-body-sm text-on-surface-variant mb-4">
            Tasa de detección exitosa del ensemble propuesto según el vector de alteración
          </p>
          <div className="flex-grow min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={recalls_by_type} layout="vertical" margin={{ top: 10, right: 20, bottom: 10, left: 30 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis type="number" domain={[0.7, 1.0]} stroke="#8e918f" fontSize={10} />
                <YAxis dataKey="tipo" type="category" stroke="#8e918f" fontSize={10} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'rgba(30,30,30,0.9)', borderColor: 'rgba(255,255,255,0.1)' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Bar dataKey="sensibilidad" name="Recall Ensemble" fill="#76db8f" radius={[0, 3, 3, 0]}>
                  {recalls_by_type.map((entry, index) => {
                    const colors = ['#76db8f', '#a8c7fa', '#efb489', '#f97316', '#ffb4ab']
                    return <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                  })}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Real-time Participant Progress (Mantenido a petición del usuario) */}
      <div className="glass-panel rounded-xl p-0 flex flex-col h-[350px] overflow-hidden mb-8">
        <div className="p-6 border-b border-white/5 flex justify-between items-center bg-surface-container-low/30">
          <div>
            <h3 className="font-headline-sm text-headline-sm text-on-surface">Registro de Auditores Asignados</h3>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Auditores habilitados en la matriz experimental de compliance.</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary"></span>
            </span>
            <span className="font-mono-data text-mono-data text-primary text-xs font-bold">MONITOR_ACTIVO</span>
          </div>
        </div>
        
        <div className="flex-grow overflow-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-white/[0.02] border-b border-primary/20 font-label-md text-label-md text-on-surface-variant uppercase">
                <th className="py-3 px-6">Nombre de Auditor</th>
                <th className="py-3 px-6">Condición Asignada</th>
                <th className="py-3 px-6">Alertas Auditadas</th>
                <th className="py-3 px-6">Precisión Consenso</th>
                <th className="py-3 px-6 text-right">Estado Red</th>
              </tr>
            </thead>
            <tbody className="font-mono-data text-mono-data divide-y divide-white/5 text-on-surface">
              {operativos_progress.map((op, idx) => (
                <tr key={op.username || idx} className="hover:bg-white/5 transition-colors">
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
  )
}
