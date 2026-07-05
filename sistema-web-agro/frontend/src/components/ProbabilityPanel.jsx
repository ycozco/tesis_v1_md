import React from 'react'

export default function ProbabilityPanel({ alert }) {
  return (
    <div className="glass-panel rounded-xl p-4 flex flex-col justify-between">
      <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant mb-2 text-[11px]">
        Distribución de Probabilidad
      </h3>
      <div className="relative h-20 w-full chart-grid flex items-end mb-4 border-b border-l border-white/10 px-2 pb-1 overflow-hidden">
        <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 50">
          <path d="M 0 50 C 20 50, 30 10, 50 5, 70 10, 80 50, 100 50" fill="none" stroke="rgba(156, 240, 255, 0.4)" strokeWidth="1.5"></path>
          <circle cx={Math.max(15, Math.min(alert.score_anomalia * 100, 85))} cy="25" fill="#ef4444" r="3" className="animate-pulse"></circle>
          <line stroke="#ef4444" strokeDasharray="2" strokeWidth="0.75" x1={Math.max(15, Math.min(alert.score_anomalia * 100, 85))} x2={Math.max(15, Math.min(alert.score_anomalia * 100, 85))} y1="25" y2="50"></line>
        </svg>
        <div className="absolute top-1 left-2 text-[8px] font-mono-sm text-error">DAM Actual</div>
        <div className="absolute top-1 right-2 text-[8px] font-mono-sm text-tertiary">Media Clúster</div>
      </div>
      <div className="grid grid-cols-3 gap-2 border-t border-white/5 pt-3">
        <div className="text-center">
          <div className="text-[9px] text-on-surface-variant font-mono-sm uppercase">Precisión</div>
          <div className="font-bold text-primary font-mono-sm text-[12px]">92.4%</div>
        </div>
        <div className="text-center border-l border-r border-white/10">
          <div className="text-[9px] text-on-surface-variant font-mono-sm uppercase">Recall</div>
          <div className="font-bold text-primary font-mono-sm text-[12px]">88.7%</div>
        </div>
        <div className="text-center">
          <div className="text-[9px] text-on-surface-variant font-mono-sm uppercase">F1-Score</div>
          <div className="font-bold text-primary font-mono-sm text-[12px]">0.905</div>
        </div>
      </div>
    </div>
  )
}
