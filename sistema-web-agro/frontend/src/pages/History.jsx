import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function History() {
  const [decisions, setDecisions] = useState([])
  const [loading, setLoading] = useState(true)
  const [condicion, setCondicion] = useState('All')
  const navigate = useNavigate()

  const fetchHistory = () => {
    setLoading(true)
    const param = condicion !== 'All' ? `?condicion=${condicion}` : ''
    
    fetch(`/api/history${param}`)
      .then(res => res.json())
      .then(data => {
        setDecisions(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching history:', err)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchHistory()
  }, [condicion])

  const getDecisionBadge = (code) => {
    if (code === 1) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-error-container/20 text-error border border-error/30">
          <span className="material-symbols-outlined text-[14px]">warning</span> Confirmado
        </span>
      )
    } else if (code === 0) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-variant text-on-surface-variant border border-white/10">
          <span className="material-symbols-outlined text-[14px]">check_circle</span> Falsa Alarma
        </span>
      )
    } else {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-secondary-container/20 text-secondary border border-secondary/30">
          <span className="material-symbols-outlined text-[14px]">info</span> Inspección
        </span>
      )
    }
  }

  return (
    <div className="flex-grow overflow-y-auto overflow-x-hidden">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-card-gap">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface">Historial de Auditoría</h1>
          <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Revisión de clasificaciones operativas previas y tiempos registrados.</p>
        </div>
        <div className="flex flex-wrap items-center gap-4 glass-panel p-2 rounded-lg border border-white/5">
          <div className="flex items-center gap-2 px-2">
            <span className="material-symbols-outlined text-primary text-sm">filter_list</span>
            <span className="font-label-md text-label-md text-on-surface-variant">Filtro Condición:</span>
          </div>
          <div className="flex gap-1 bg-surface-container-highest p-1 rounded-md">
            <button 
              className={`px-4 py-1.5 rounded font-label-md text-label-md transition-colors ${condicion === 'All' ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:bg-surface-variant/50'}`}
              onClick={() => setCondicion('All')}
            >
              Todos
            </button>
            <button 
              className={`px-4 py-1.5 rounded font-label-md text-label-md transition-colors ${condicion === 'INTEGRADO' ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:bg-surface-variant/50'}`}
              onClick={() => setCondicion('INTEGRADO')}
            >
              Condición A (Explicable)
            </button>
            <button 
              className={`px-4 py-1.5 rounded font-label-md text-label-md transition-colors ${condicion === 'AISLADO' ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:bg-surface-variant/50'}`}
              onClick={() => setCondicion('AISLADO')}
            >
              Condición B (Aislada)
            </button>
          </div>
        </div>
      </div>

      {/* Main Data Table Container */}
      <div className="glass-panel rounded-xl overflow-hidden flex flex-col relative min-h-[450px]">
        {loading ? (
          <div className="flex-grow flex items-center justify-center">
            <span className="material-symbols-outlined text-primary text-4xl animate-spin">sync</span>
            <span className="ml-3 text-on-surface font-medium">Cargando histórico de telemetría...</span>
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse audit-table whitespace-nowrap">
                <thead className="bg-surface-container-high/90 border-b border-primary/30 font-label-md text-label-md text-primary uppercase tracking-wider">
                  <tr>
                    <th className="py-4 px-4">ID Decisión</th>
                    <th className="py-4 px-4">ID Alerta</th>
                    <th className="py-4 px-4">DAM</th>
                    <th className="py-4 px-4">Producto</th>
                    <th className="py-4 px-4">Clasificación Final</th>
                    <th className="py-4 px-4 text-center">Comprensión IA</th>
                    <th className="py-4 px-4 text-right">Tiempo (ms)</th>
                    <th className="py-4 px-4">Auditor</th>
                    <th className="py-4 px-4">Condición</th>
                    <th className="py-4 px-4 text-right">Acción</th>
                  </tr>
                </thead>
                <tbody className="font-mono-data text-mono-data text-on-surface divide-y divide-white/5">
                  {decisions.map(decision => (
                    <tr key={decision.id_decision} className="hover:bg-white/5 transition-colors group">
                      <td className="py-3 px-4 text-on-surface-variant">DEC-{1000 + decision.id_decision}</td>
                      <td className="py-3 px-4 text-primary font-semibold">{decision.id_alerta}</td>
                      <td className="py-3 px-4">{decision.numero_dam}</td>
                      <td className="py-3 px-4">{decision.producto}</td>
                      <td className="py-3 px-4">
                        {getDecisionBadge(decision.user_decision)}
                      </td>
                      <td className="py-3 px-4 text-center">
                        <div className="flex justify-center items-center gap-1 text-primary">
                          {[1, 2, 3, 4, 5].map(i => (
                            <span 
                              key={i} 
                              className="material-symbols-outlined text-[16px]"
                              style={{ fontVariationSettings: i <= decision.likert_comprehension ? "'FILL' 1" : "'FILL' 0" }}
                            >
                              star
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-right text-secondary font-bold">
                        {decision.time_to_decision_ms.toLocaleString()}
                      </td>
                      <td className="py-3 px-4 text-on-surface-variant">{decision.usuario_nombre}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[10px] ${decision.condicion_experimento === 'INTEGRADO' ? 'bg-primary/10 text-primary border border-primary/20' : 'bg-secondary/10 text-secondary border border-secondary/20'}`}>
                          {decision.condicion_experimento}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <button 
                          className="opacity-0 group-hover:opacity-100 transition-opacity bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 px-3 py-1.5 rounded font-label-md text-label-md"
                          onClick={() => navigate(`/decision/${decision.id_decision}`)}
                        >
                          Ver Detalle
                        </button>
                      </td>
                    </tr>
                  ))}
                  {decisions.length === 0 && (
                    <tr>
                      <td colSpan="10" className="py-8 text-center text-on-surface-variant font-body-md">No se han registrado auditorías bajo este criterio aún.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            {/* Pagination Footer */}
            <div className="mt-auto border-t border-white/5 p-4 flex justify-between items-center bg-surface-container/20">
              <span className="font-body-sm text-body-sm text-on-surface-variant">Mostrando {decisions.length} decisiones auditadas</span>
              <div className="flex gap-2">
                <button className="p-1 rounded hover:bg-white/10 text-on-surface-variant disabled:opacity-50" disabled>
                  <span className="material-symbols-outlined">chevron_left</span>
                </button>
                <button className="p-1 rounded hover:bg-white/10 text-on-surface-variant disabled:opacity-50" disabled>
                  <span className="material-symbols-outlined">chevron_right</span>
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
