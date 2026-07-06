import React from 'react'

export default function SeverityPanel({ alert }) {
  return (
    <div className="glass-panel rounded-xl p-6 flex flex-col justify-center items-center relative overflow-hidden min-h-[220px]">
      <div className="z-10 text-center space-y-2">
        <span className="material-symbols-outlined text-4xl text-error">warning</span>
        <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
          Puntaje de Severidad PyOD
        </h3>
        <div className="text-[34px] font-bold tracking-tight uppercase anomaly-gradient leading-none my-1">
          {alert.score_anomalia > 0.8 ? 'RIESGO CRÍTICO' : alert.score_anomalia > 0.6 ? 'RIESGO ALTO' : 'RIESGO BAJO'}
        </div>
        <p className="font-mono-sm text-mono-sm text-on-surface-variant">
          Puntaje de Conjunto: <span className="text-white font-bold">{alert.score_anomalia.toFixed(4)}</span> / 1.000
        </p>
        <div className="text-[9px] font-body-sm text-on-surface-variant/80 mt-2 bg-black/20 p-1.5 rounded mx-2 md:mx-6 leading-tight">
          Indica qué tan atípica es la operación comparada con su clúster logístico e histórico. Mayor a 0.65 se considera alerta.
        </div>
      </div>
    </div>
  )
}
