import React from 'react'

export default function RegressionPanel({ alert }) {
  const dev = alert.valor_fob_esperado > 0 
    ? ((Math.abs(alert.valor_fob_declarado - alert.valor_fob_esperado) / alert.valor_fob_esperado) * 100).toFixed(1)
    : "0.0";
  return (
    <div className="glass-panel rounded-xl p-4 flex flex-col justify-between min-h-[170px]">
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-primary text-[16px]">analytics</span>
        <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
          Análisis Regresor GBDT
        </h3>
      </div>
      
      <div className="grid grid-cols-2 gap-2 mb-3">
        <div>
          <p className="text-on-surface-variant font-label-md text-[10px] uppercase">FOB Declarado</p>
          <p className="font-headline-md text-lg font-bold text-error">${alert.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</p>
        </div>
        <div>
          <p className="text-on-surface-variant font-label-md text-[10px] uppercase">Rango Esperado</p>
          <p className="font-headline-md text-lg font-bold text-primary">${alert.valor_fob_esperado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative w-16 h-10 flex items-center justify-center flex-shrink-0">
          <svg className="w-full h-full transform" viewBox="0 0 100 60">
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="rgba(255,255,255,0.1)" strokeLinecap="round" strokeWidth="8"></path>
            <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#ec6a06" strokeDasharray="126" strokeDashoffset="30" strokeLinecap="round" strokeWidth="8"></path>
            <line stroke="white" strokeLinecap="round" strokeWidth="2.5" transform={`rotate(${180 - (Math.max(0, Math.min(parseFloat(dev) || 0, 30)) / 30 * 180)} 50 50)`} x1="50" x2="50" y1="50" y2="15"></line>
          </svg>
        </div>
        <p className="font-mono-sm text-[10px] text-secondary-fixed-dim bg-[#2c1a11]/45 p-2 rounded border border-secondary/15 flex-1">
          Desviación: <strong className="text-error">-{dev}%</strong> del centroide. Impacto fiscal est.: <strong className="text-white">-${Math.abs(alert.valor_fob_esperado - alert.valor_fob_declarado).toLocaleString('en-US', {maximumFractionDigits:0})}</strong>
        </p>
      </div>
    </div>
  )
}
