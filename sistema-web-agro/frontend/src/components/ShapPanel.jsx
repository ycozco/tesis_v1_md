import React from 'react'

export default function ShapPanel({ explanations, handleOpenRag }) {
  return (
    <div className="glass-panel rounded-xl p-4 flex flex-col justify-between">
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-tertiary text-[16px]">bar_chart</span>
        <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
          Atribución de Variables (SHAP)
        </h3>
      </div>
      <div className="space-y-2">
        {explanations.slice(0, 4).map((exp, index) => {
          const isPositive = exp.shap_value >= 0
          const absVal = Math.min(Math.abs(exp.shap_value) * 150, 95)
          return (
            <div key={exp.id_explicacion || index} className="space-y-0.5">
              <div className="flex justify-between text-[9px] font-mono-sm uppercase">
                <span className="text-on-surface-variant">{exp.variable_nombre}</span>
                <span className={`font-bold ${isPositive ? 'text-error' : 'text-tertiary'}`}>
                  {isPositive ? `+${exp.shap_value.toFixed(2)}` : exp.shap_value.toFixed(2)}
                </span>
              </div>
              <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden relative">
                <div 
                  className={`h-full rounded-full ${isPositive ? 'bg-error' : 'bg-tertiary'}`}
                  style={{ width: `${absVal}%` }}
                ></div>
              </div>
            </div>
          )
        })}
      </div>
      <button 
        type="button"
        className="mt-2 w-full py-1.5 border border-white/10 rounded-lg text-[10px] font-label-md text-on-surface-variant hover:bg-white/5 hover:text-white transition-colors flex items-center justify-center gap-2"
        onClick={() => handleOpenRag('LMY-IA-D115')}
      >
        <span className="material-symbols-outlined text-[12px]">info</span>
        Ver detalles RAG
      </button>
    </div>
  )
}
