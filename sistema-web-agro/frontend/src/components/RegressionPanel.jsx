import React from 'react'

export default function RegressionPanel({ alert }) {
  const devVal = alert.valor_fob_esperado !== 0 
    ? ((alert.valor_fob_declarado - alert.valor_fob_esperado) / alert.valor_fob_esperado) * 100
    : 0;
  const devStr = devVal >= 0 ? `+${devVal.toFixed(1)}` : `${devVal.toFixed(1)}`;
  const devAbs = Math.abs(devVal).toFixed(1);

  return (
    <div className="glass-panel rounded-xl p-5 flex flex-col justify-between min-h-[170px]">
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-primary text-[18px]">analytics</span>
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
          <p className="text-on-surface-variant font-label-md text-xs uppercase mb-1 font-bold">FOB Esperado</p>
          <p className={`font-headline-md text-2xl font-bold ${alert.valor_fob_esperado < 0 ? 'text-error' : 'text-primary'}`}>
            ${alert.valor_fob_esperado.toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </p>
          <div className="text-[10px] font-body-sm text-on-surface-variant/90 mt-2 bg-black/20 p-2 rounded leading-tight">
            Valor normal estimado por el modelo GBDT. {alert.valor_fob_esperado < 0 && <span className="text-error font-bold block mt-1">Penalización extrema detectada.</span>}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4 bg-white/5 p-3 rounded-lg border border-white/10">
        <div className="relative w-28 h-16 flex items-center justify-center flex-shrink-0">
          <svg className="w-full h-full" viewBox="0 0 100 60">
            <defs>
              <linearGradient id="regressionGaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#4ade80" />
                <stop offset="50%" stopColor="#fbbf24" />
                <stop offset="100%" stopColor="#ef4444" />
              </linearGradient>
              <filter id="gaugeGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="1.2" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>
            {/* Back track */}
            <path 
              d="M 10 50 A 40 40 0 0 1 90 50" 
              fill="none" 
              stroke="rgba(255,255,255,0.06)" 
              strokeWidth="7"
              strokeLinecap="round"
            />
            {/* Colored Metric Arc */}
            <path 
              d="M 10 50 A 40 40 0 0 1 90 50" 
              fill="none" 
              stroke="url(#regressionGaugeGradient)" 
              strokeWidth="7" 
              strokeLinecap="round"
              strokeDasharray="126" 
              strokeDashoffset={126 - (126 * Math.min(Math.abs(parseFloat(devAbs)), 100) / 100)}
              filter="url(#gaugeGlow)"
            />
            {/* Ticks */}
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="rgba(0,0,0,0.35)" strokeDasharray="2 5" strokeWidth="7.5"></path>
            
            {/* Legend Ticks */}
            <text x="50" y="48" textAnchor="middle" fill="#8e918f" fontSize="7" fontFamily="monospace">50%</text>
            <text x="12" y="56" textAnchor="middle" fill="#8e918f" fontSize="6" fontFamily="monospace">0%</text>
            <text x="88" y="56" textAnchor="middle" fill="#8e918f" fontSize="6" fontFamily="monospace">&gt;100%</text>
            
            {/* Needle */}
            <g transform={`rotate(${180 - (Math.max(0, Math.min(parseFloat(devAbs) || 0, 100)) / 100 * 180)} 50 50)`}>
              <path d="M 49 50 L 50 16 L 51 50 Z" fill="#38bdf8" />
              <circle cx="50" cy="50" r="3.5" fill="#38bdf8" />
              <circle cx="50" cy="50" r="1.5" fill="white" />
            </g>
          </svg>
        </div>
        <p className="font-mono-sm text-xs text-secondary-fixed-dim p-2 rounded flex-1 leading-relaxed">
          Desviación: <strong className={`${devVal < 0 ? 'text-error animate-pulse' : 'text-[#a3e635]'} font-bold`}>{devStr}%</strong> del precio FOB esperado. <br/>Brecha de valor: <strong className="text-white bg-black/20 px-1 py-0.5 rounded">${Math.abs(alert.valor_fob_esperado - alert.valor_fob_declarado).toLocaleString('en-US', {maximumFractionDigits:2})}</strong>
        </p>
      </div>
    </div>
  )
}
