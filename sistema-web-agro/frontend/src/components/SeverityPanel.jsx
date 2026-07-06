import React from 'react'

export default function SeverityPanel({ alert }) {
  const score = Number(alert.score_anomalia || 0)
  const radius = 55
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (score * circumference)

  let colorClass = 'text-[#a3e635]'
  let label = 'RIESGO BAJO'
  let bgGradient = 'from-[#a3e635]/10 to-transparent'
  let borderIcon = 'check_circle'
  let alertColor = 'text-[#a3e635]'

  if (score >= 0.8) {
    colorClass = 'text-error'
    label = 'RIESGO CRÍTICO'
    bgGradient = 'from-error/15 to-transparent'
    borderIcon = 'warning'
    alertColor = 'text-error animate-pulse'
  } else if (score >= 0.6) {
    colorClass = 'text-[#fbbf24]'
    label = 'RIESGO ALTO'
    bgGradient = 'from-[#fbbf24]/15 to-transparent'
    borderIcon = 'gpp_maybe'
    alertColor = 'text-[#fbbf24]'
  }

  return (
    <div className={`glass-panel rounded-xl p-6 flex flex-col sm:flex-row items-center gap-6 relative overflow-hidden min-h-[220px] bg-gradient-to-br ${bgGradient}`}>
      <div className="absolute inset-0 opacity-5 bg-gradient-to-br from-primary via-transparent to-transparent pointer-events-none"></div>
      
      {/* Visual Ring Gauge */}
      <div className="relative w-32 h-32 flex items-center justify-center flex-shrink-0 z-10">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 150 150">
          {/* Back track */}
          <circle
            cx="75"
            cy="75"
            r={radius}
            fill="transparent"
            stroke="rgba(255, 255, 255, 0.05)"
            strokeWidth="10"
          />
          {/* Active colored path */}
          <circle
            cx="75"
            cy="75"
            r={radius}
            fill="transparent"
            stroke="url(#severityGaugeGradient)"
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
          />
          <defs>
            <linearGradient id="severityGaugeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#4ade80" />
              <stop offset="60%" stopColor="#fbbf24" />
              <stop offset="100%" stopColor="#ef4444" />
            </linearGradient>
          </defs>
        </svg>
        {/* Centered Value */}
        <div className="absolute inset-0 flex flex-col items-center justify-center font-mono-data leading-none">
          <span className="text-2xl font-black text-white tracking-tight">{score.toFixed(4)}</span>
          <span className="text-[9px] text-on-surface-variant uppercase tracking-wider mt-1 font-bold">Score PyOD</span>
        </div>
      </div>

      {/* Text Info */}
      <div className="z-10 flex-1 text-center sm:text-left space-y-2">
        <div className="flex items-center justify-center sm:justify-start gap-2">
          <span className={`material-symbols-outlined text-[18px] ${alertColor}`}>{borderIcon}</span>
          <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px] font-bold">
            Puntaje de Severidad PyOD
          </h3>
        </div>
        
        <div className={`text-3xl font-black tracking-tight uppercase leading-none ${colorClass}`}>
          {label}
        </div>
        
        <p className="font-mono-sm text-mono-sm text-on-surface-variant text-xs">
          Puntaje de Conjunto: <span className="text-white font-bold">{score.toFixed(4)}</span> / 1.0000
        </p>
        
        <div className="text-[10px] font-body-sm text-on-surface-variant/90 mt-2 bg-black/35 p-2 rounded leading-relaxed border border-white/5">
          Indica qué tan atípica es la operación comparada con su clúster logístico e histórico. Las puntuaciones mayores a <strong className="text-white">0.6500</strong> se consideran alertas automáticas.
        </div>
      </div>
    </div>
  )
}

