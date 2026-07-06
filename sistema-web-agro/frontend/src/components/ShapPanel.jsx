import React from 'react'

export default function ShapPanel({ explanations, handleOpenRag }) {
  return (
    <div className="glass-panel rounded-xl p-4 flex flex-col justify-between">
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-tertiary text-[16px]">bar_chart</span>
        <h3 className="font-label-md uppercase tracking-widest text-on-surface-variant text-sm font-bold">
          Atribución de Variables (SHAP)
        </h3>
      </div>
      <p className="text-on-surface-variant text-xs mb-3 font-mono-sm leading-tight">
        Análisis de interpretabilidad local: peso de cada variable en la puntuación final de anomalía.
      </p>
      <div className="space-y-3">
        {(() => {
          const topExplanations = explanations.slice(0, 4);
          const maxShap = Math.max(...topExplanations.map(e => Math.abs(e.shap_value)), 1);
          
          return topExplanations.map((exp, index) => {
            const isPositive = exp.shap_value >= 0
            const absVal = (Math.abs(exp.shap_value) / maxShap) * 95;
            
            return (
              <div key={exp.id_explicacion || index} className="space-y-1">
                <div className="flex justify-between text-xs font-mono-sm uppercase font-bold">
                  <span className="text-on-surface-variant">{exp.variable_nombre}</span>
                  <span className={`${isPositive ? 'text-primary' : 'text-error'}`}>
                    {isPositive ? `+$${exp.shap_value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : `-$${Math.abs(exp.shap_value).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`}
                  </span>
                </div>
                <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden relative">
                  <div 
                    className={`h-full rounded-full ${isPositive ? 'bg-primary' : 'bg-error'}`}
                    style={{ width: `${Math.max(absVal, 5)}%` }}
                  ></div>
                </div>
                <div className="text-xs font-body-sm text-on-surface-variant/90 mt-1.5 leading-tight bg-white/5 p-1.5 rounded">
                  {isPositive ? '↑ Aumenta la valoración FOB (A favor)' : '↓ Reduce la valoración FOB (Penalización)'}
                </div>
              </div>
            )
          })
        })()}
      </div>
      <button 
        type="button"
        className="mt-4 w-full py-2 border border-white/10 rounded-lg text-xs font-label-md text-on-surface-variant hover:bg-white/5 hover:text-white transition-colors flex items-center justify-center gap-2 font-bold"
        onClick={() => handleOpenRag('LMY-IA-D115')}
      >
        <span className="material-symbols-outlined text-[14px]">info</span>
        Ver detalles RAG
      </button>
    </div>
  )
}
