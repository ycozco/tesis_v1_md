import React from 'react'

export default function RegressionPanel({ alert }) {
  const dev = alert.valor_fob_esperado !== 0 
    ? ((Math.abs(alert.valor_fob_declarado - alert.valor_fob_esperado) / Math.abs(alert.valor_fob_esperado)) * 100).toFixed(1)
    : "0.0";
  return (
    <div className="glass-panel rounded-xl p-4 flex flex-col justify-between min-h-[170px]">
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-primary text-[16px]">analytics</span>
        <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-sm font-bold">
          Análisis Regresor GBDT
        </h3>
      </div>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-on-surface-variant font-label-md text-xs uppercase mb-1 font-bold">FOB Declarado</p>
          <p className="font-headline-md text-2xl font-bold text-error">${alert.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</p>
          <div className="text-[10px] font-body-sm text-on-surface-variant/90 mt-2 bg-black/20 p-2 rounded leading-tight">
            Valor indicado por el exportador en la DAM.
          </div>
        </div>
        <div>
          <p className="text-on-surface-variant font-label-md text-xs uppercase mb-1 font-bold">Rango Esperado</p>
          <p className={`font-headline-md text-2xl font-bold ${alert.valor_fob_esperado < 0 ? 'text-error' : 'text-primary'}`}>
            ${alert.valor_fob_esperado.toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </p>
          <div className="text-[10px] font-body-sm text-on-surface-variant/90 mt-2 bg-black/20 p-2 rounded leading-tight">
            Valor normal estimado por el modelo GBDT. {alert.valor_fob_esperado < 0 && <span className="text-error font-bold block mt-1">Penalización extrema detectada.</span>}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4 bg-white/5 p-3 rounded-lg border border-white/10">
        <div className="relative w-20 h-12 flex items-center justify-center flex-shrink-0">
          <svg className="w-full h-full transform" viewBox="0 0 100 60">
            {/* Ticks */}
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="rgba(255,255,255,0.05)" strokeDasharray="4 8" strokeWidth="12"></path>
            {/* Background Arc */}
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="rgba(255,255,255,0.1)" strokeLinecap="round" strokeWidth="8"></path>
            {/* Colored Metric Arc */}
            <defs>
              <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#4ade80" />
                <stop offset="50%" stopColor="#fbbf24" />
                <stop offset="100%" stopColor="#ef4444" />
              </linearGradient>
            </defs>
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="url(#gaugeGradient)" strokeDasharray="126" strokeDashoffset={126 - (126 * Math.min(Math.abs(parseFloat(dev)), 100) / 100)} strokeLinecap="round" strokeWidth="8"></path>
            
            {/* Needle */}
            <g transform={`rotate(${180 - (Math.max(0, Math.min(parseFloat(dev) || 0, 100)) / 100 * 180)} 50 50)`}>
              <polygon points="48,50 52,50 50,15" fill="white" />
              <circle cx="50" cy="50" r="4" fill="white" />
            </g>
          </svg>
        </div>
        <p className="font-mono-sm text-sm text-secondary-fixed-dim p-2 rounded flex-1 leading-relaxed">
          Desviación: <strong className="text-error font-bold">-{dev}%</strong> del centroide. <br/>Impacto fiscal est.: <strong className="text-white bg-black/20 px-1 py-0.5 rounded">-${Math.abs(alert.valor_fob_esperado - alert.valor_fob_declarado).toLocaleString('en-US', {maximumFractionDigits:0})}</strong>
        </p>
      </div>
    </div>
  )
}
