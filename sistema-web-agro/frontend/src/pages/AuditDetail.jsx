import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

export default function AuditDetail() {
  const { id_decision } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/decisiones/${id_decision}`)
      .then(res => res.json())
      .then(resData => {
        setData(resData)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching decision details:', err)
        setLoading(false)
      })
  }, [id_decision])

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <span className="material-symbols-outlined text-primary text-5xl animate-spin">sync</span>
        <span className="ml-3 text-lg font-medium text-primary">Cargando registro histórico...</span>
      </div>
    )
  }

  const { decision, alert, explanations = [] } = data
  const dev = (((alert.valor_fob_esperado - alert.valor_fob_declarado) / alert.valor_fob_esperado) * 100).toFixed(1)
  const isIntegrated = decision.condicion_experimento === 'INTEGRADO'

  return (
    <div className="flex-grow overflow-y-auto p-container-padding pb-24 md:pb-container-padding">
      
      {/* Header */}
      <div className="mb-gutter border-b border-white/5 pb-4">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className="bg-primary/20 text-primary border border-primary/30 px-2 py-0.5 rounded text-[10px] font-mono-data uppercase">
                Auditoría Congelada
              </span>
              <span className="text-on-surface-variant font-mono-data text-[12px]">Registro ID: DEC-{1000 + decision.id_decision}</span>
            </div>
            <h2 className="font-headline-lg text-headline-lg text-on-surface flex items-center gap-3">
              <span className="material-symbols-outlined text-primary text-[32px]">bookmark</span>
              Auditoría de DAM #{alert.numero_dam}
            </h2>
          </div>
          <button 
            className="glass-panel px-5 py-2 rounded-lg font-label-md text-label-md text-on-surface hover:bg-white/10 transition-colors flex items-center gap-2"
            onClick={() => navigate('/history')}
          >
            <span className="material-symbols-outlined text-[18px]">arrow_back</span>
            Volver al Historial
          </button>
        </div>
        
        {/* Meta info */}
        <div className="flex flex-wrap gap-2 text-on-surface-variant font-body-sm">
          <div className="glass-panel px-3 py-1.5 rounded flex items-center gap-2 border-l border-primary">
            <span>Auditor: <strong>{decision.usuario_nombre}</strong></span>
          </div>
          <div className="glass-panel px-3 py-1.5 rounded flex items-center gap-2 border-l border-secondary">
            <span>Condición: <strong>{decision.condicion_experimento}</strong></span>
          </div>
          <div className="glass-panel px-3 py-1.5 rounded flex items-center gap-2 border-l border-tertiary">
            <span>Fecha de Auditoría: <strong>{decision.creado_en.replace('T', ' ').split('.')[0]}</strong></span>
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-card-gap mb-6">
        
        {/* Operation Stats */}
        <div className="xl:col-span-12 glass-panel rounded-xl p-5 border-l-4 border-l-primary flex flex-wrap gap-x-12 gap-y-4">
          <div>
            <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-1">RUC Exportador</div>
            <div className="font-mono-data text-on-surface">{alert.ruc_exportador}</div>
          </div>
          <div>
            <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-1">Razón Social</div>
            <div className="font-body-md text-on-surface font-semibold">{alert.razon_social}</div>
          </div>
          <div>
            <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-1">Producto</div>
            <div className="font-body-md text-on-surface">{alert.producto}</div>
          </div>
          <div>
            <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-1">Valor FOB Declarado</div>
            <div className="font-mono-data text-on-surface">${alert.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
          </div>
          <div>
            <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-1">Valor FOB Esperado</div>
            <div className="font-mono-data text-on-surface">${alert.valor_fob_esperado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
          </div>
        </div>

        {/* Layer 1: GBDT Prediction */}
        <div className="xl:col-span-6 glass-panel rounded-xl p-6">
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-6">
            <span className="material-symbols-outlined text-secondary">monitoring</span>
            Capa 1: Desviación Residual FOB
          </h3>
          <div className="flex items-center justify-between gap-6">
            <div className="flex-1 space-y-3">
              <div className="flex justify-between text-body-sm">
                <span className="text-on-surface-variant">FOB Declarado:</span>
                <span className="font-mono-data">${alert.valor_fob_declarado.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-body-sm">
                <span className="text-primary font-medium">FOB Esperado:</span>
                <span className="font-mono-data text-primary">${alert.valor_fob_esperado.toLocaleString()}</span>
              </div>
            </div>
            <div className="w-20 h-20 rounded-full border-2 border-error/20 flex flex-col items-center justify-center shrink-0">
              <span className="text-[10px] text-on-surface-variant font-mono-data uppercase">Desv.</span>
              <span className="text-lg text-error font-bold font-mono-data">{parseFloat(dev) > 0 ? `+${dev}%` : `${dev}%`}</span>
            </div>
          </div>
        </div>

        {/* Layer 2: Ensemble Score */}
        <div className="xl:col-span-6 glass-panel rounded-xl p-6">
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-4">
            <span className="material-symbols-outlined text-error">gavel</span>
            Capa 2: Score de Anomalía
          </h3>
          <div className="flex items-center gap-4 bg-error/5 border border-error/20 rounded p-4">
            <span className="material-symbols-outlined text-3xl text-error">warning_amber</span>
            <div>
              <div className="text-xs text-on-surface-variant">Score de Anomalía Ensemble</div>
              <div className="font-mono-data text-xl text-error font-bold">{alert.score_anomalia.toFixed(4)}</div>
            </div>
          </div>
        </div>

        {/* Layer 3: SHAP (Condición A) */}
        {isIntegrated && (
          <div className="xl:col-span-12 glass-panel rounded-xl p-6">
            <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-6">
              <span className="material-symbols-outlined text-tertiary">analytics</span>
              Capa 3: Explicación SHAP en el Momento del Test
            </h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-12 gap-y-4">
              {explanations.map((exp, index) => {
                const isPositive = exp.shap_value >= 0
                const absVal = Math.min(Math.abs(exp.shap_value) * 150, 95)
                return (
                  <div key={exp.id_explicacion || index} className="flex items-center gap-4">
                    <div className="w-1/3 text-right font-label-md text-label-md text-on-surface truncate">{exp.variable_nombre}</div>
                    <div className={`w-2/3 flex items-center gap-2 ${isPositive ? '' : 'flex-row-reverse justify-end'}`}>
                      <div className={`h-4 rounded-sm ${isPositive ? 'bg-error/70' : 'bg-tertiary/70'}`} style={{ width: `${absVal}%` }}></div>
                      <span className={`font-mono-data text-[12px] ${isPositive ? 'text-error' : 'text-tertiary'}`}>{exp.shap_value.toFixed(2)}</span>
                      <span className="text-[10px] text-on-surface-variant font-mono-data ml-1">({exp.variable_valor})</span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Auditor Adjudication Details */}
        <div className="xl:col-span-12 glass-card rounded-xl p-6 border border-primary/20">
          <h3 className="font-headline-sm text-headline-sm text-primary flex items-center gap-2 mb-6">
            <span className="material-symbols-outlined">assignment_turned_in</span>
            Adjudicación del Auditor (Métricas de Telemetría)
          </h3>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div>
              <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-2">Clasificación Adjudicada</div>
              <div className="p-3 bg-white/5 border border-white/5 rounded-lg text-center font-bold font-mono-data text-md">
                {decision.user_decision === 1 && <span className="text-error">Anomalía Confirmada (True Positive)</span>}
                {decision.user_decision === 0 && <span className="text-on-surface-variant">Falsa Alarma (Modelo)</span>}
                {decision.user_decision === 2 && <span className="text-secondary">Dudoso / Requiere Inspección</span>}
              </div>
            </div>
            
            <div>
              <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-2">Tiempo Registrado de Decisión</div>
              <div className="p-3 bg-white/5 border border-white/5 rounded-lg text-center text-secondary font-bold font-mono-data text-md">
                {decision.time_to_decision_ms.toLocaleString()} ms <span className="text-xs text-on-surface-variant">({(decision.time_to_decision_ms / 1000).toFixed(2)}s)</span>
              </div>
            </div>
            
            <div>
              <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-2">Comprensión Percibida (Likert)</div>
              <div className="p-3 bg-white/5 border border-white/5 rounded-lg flex justify-center items-center gap-1 text-primary">
                {[1, 2, 3, 4, 5].map(i => (
                  <span 
                    key={i} 
                    className="material-symbols-outlined text-[20px]"
                    style={{ fontVariationSettings: i <= decision.likert_comprehension ? "'FILL' 1" : "'FILL' 0" }}
                  >
                    star
                  </span>
                ))}
              </div>
            </div>
            
            <div className="lg:col-span-3 border-t border-white/5 pt-4">
              <div className="text-xs text-on-surface-variant uppercase tracking-wider mb-2">Justificación Técnica del Auditor</div>
              <div className="p-4 bg-surface-container-low/50 border border-white/5 rounded-lg italic text-on-surface-variant leading-relaxed">
                "{decision.justification_text}"
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  )
}
