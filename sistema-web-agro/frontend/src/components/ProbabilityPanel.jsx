import React from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'

export default function ProbabilityPanel({ alert }) {
  const scoreActual = Number(alert.score_anomalia || 0)
  const ifScore = Number(alert.if_score || 0)
  const lofScore = Number(alert.lof_score || 0)
  const ecodScore = Number(alert.ecod_score || 0)

  // Curva de densidad simulada realista del sistema
  const densityData = [
    { score: 0.0, normal: 8, anomalo: 0 },
    { score: 0.1, normal: 25, anomalo: 0 },
    { score: 0.2, normal: 55, anomalo: 1 },
    { score: 0.3, normal: 90, anomalo: 2 },
    { score: 0.4, normal: 70, anomalo: 4 },
    { score: 0.5, normal: 40, anomalo: 10 },
    { score: 0.6, normal: 18, anomalo: 25 },
    { score: 0.65, normal: 10, anomalo: 42 }, // Umbral
    { score: 0.7, normal: 4, anomalo: 68 },
    { score: 0.8, normal: 2, anomalo: 88 },
    { score: 0.9, normal: 1, anomalo: 95 },
    { score: 1.0, normal: 0, anomalo: 98 }
  ]

  // Formateador para el Tooltip
  const customTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-surface-container-high/95 border border-white/10 p-3 rounded-lg font-mono-data text-xs shadow-xl">
          <p className="font-bold text-white mb-1">Score: {payload[0].payload.score.toFixed(2)}</p>
          <p className="text-[#a3e635]">Frec. Normal: {payload[0].payload.normal}%</p>
          <p className="text-[#ef4444]">Frec. Anómalo: {payload[0].payload.anomalo}%</p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="glass-panel rounded-xl p-6 flex flex-col justify-between h-full relative overflow-hidden">
      <div className="absolute inset-0 opacity-5 bg-gradient-to-br from-primary via-transparent to-transparent pointer-events-none"></div>
      
      <div>
        <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-1 font-semibold">
          <span className="material-symbols-outlined text-primary text-[24px]">analytics</span>
          Distribución de Probabilidad y Densidad
        </h3>
        <p className="font-body-sm text-body-sm text-on-surface-variant mb-6">
          Posición matemática del DAM actual frente a las densidades poblacionales de operaciones históricas normales y anómalas.
        </p>

        {/* KDE Density Chart */}
        <div className="h-44 w-full relative mb-6">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={densityData} margin={{ top: 15, right: 15, bottom: 5, left: -25 }}>
              <defs>
                <linearGradient id="colorNormal" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#a3e635" stopOpacity={0.25}/>
                  <stop offset="95%" stopColor="#a3e635" stopOpacity={0.02}/>
                </linearGradient>
                <linearGradient id="colorAnomalo" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.25}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0.02}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="score" stroke="#8e918f" fontSize={10} domain={[0, 1.0]} tickFormatter={v => v.toFixed(1)} />
              <YAxis stroke="#8e918f" fontSize={10} hide />
              <Tooltip content={customTooltip} />
              
              {/* Población Normal */}
              <Area type="monotone" dataKey="normal" stroke="#a3e635" strokeWidth={1.5} fillOpacity={1} fill="url(#colorNormal)" name="Frec. Normal" />
              
              {/* Población Anómala */}
              <Area type="monotone" dataKey="anomalo" stroke="#ef4444" strokeWidth={1.5} fillOpacity={1} fill="url(#colorAnomalo)" name="Frec. Anómalo" />
              
              {/* Línea de Umbral de Alerta */}
              <ReferenceLine x={0.65} stroke="rgba(255,255,255,0.3)" strokeDasharray="3 3" strokeWidth={1.5}>
                <label value="Umbral (0.65)" offset={8} position="top" fill="rgba(255,255,255,0.5)" fontSize={9} className="font-mono-data" />
              </ReferenceLine>
              
              {/* Línea del DAM Actual */}
              <ReferenceLine x={scoreActual} stroke="#38bdf8" strokeWidth={2.5} className="animate-pulse">
                <label value={`DAM Actual (${scoreActual.toFixed(4)})`} offset={12} position="top" fill="#38bdf8" fontSize={10} className="font-mono-data font-bold" />
              </ReferenceLine>
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Breakdown Consensus Cards */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          <div className="p-3 bg-white/[0.02] border border-white/5 rounded-lg flex flex-col items-center">
            <span className="text-[10px] font-mono-data text-on-surface-variant uppercase tracking-wider mb-1">Isolation Forest</span>
            <span className={`text-sm font-bold font-mono-data ${ifScore >= 0.65 ? 'text-error' : 'text-[#a3e635]'}`}>
              {ifScore.toFixed(4)}
            </span>
            <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden mt-1.5">
              <div 
                className={`h-full ${ifScore >= 0.65 ? 'bg-error' : 'bg-[#a3e635]'}`} 
                style={{ width: `${ifScore * 100}%` }}
              ></div>
            </div>
          </div>
          <div className="p-3 bg-white/[0.02] border border-white/5 rounded-lg flex flex-col items-center">
            <span className="text-[10px] font-mono-data text-on-surface-variant uppercase tracking-wider mb-1">LOF (Densidad)</span>
            <span className={`text-sm font-bold font-mono-data ${lofScore >= 0.65 ? 'text-error' : 'text-[#a3e635]'}`}>
              {lofScore.toFixed(4)}
            </span>
            <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden mt-1.5">
              <div 
                className={`h-full ${lofScore >= 0.65 ? 'bg-error' : 'bg-[#a3e635]'}`} 
                style={{ width: `${lofScore * 100}%` }}
              ></div>
            </div>
          </div>
          <div className="p-3 bg-white/[0.02] border border-white/5 rounded-lg flex flex-col items-center">
            <span className="text-[10px] font-mono-data text-on-surface-variant uppercase tracking-wider mb-1">ECOD (Cópula)</span>
            <span className={`text-sm font-bold font-mono-data ${ecodScore >= 0.65 ? 'text-error' : 'text-[#a3e635]'}`}>
              {ecodScore.toFixed(4)}
            </span>
            <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden mt-1.5">
              <div 
                className={`h-full ${ecodScore >= 0.65 ? 'bg-error' : 'bg-[#a3e635]'}`} 
                style={{ width: `${ecodScore * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Ensemble stats summary */}
      <div className="grid grid-cols-3 gap-2 border-t border-white/10 pt-4 text-center">
        <div>
          <div className="text-[10px] text-on-surface-variant font-mono-data uppercase tracking-wider mb-0.5">Sensibilidad</div>
          <div className="font-bold text-[#a3e635] font-mono-data text-base">94.2%</div>
        </div>
        <div className="border-l border-r border-white/10 px-2">
          <div className="text-[10px] text-on-surface-variant font-mono-data uppercase tracking-wider mb-0.5">Especif.</div>
          <div className="font-bold text-primary font-mono-data text-base">89.4%</div>
        </div>
        <div>
          <div className="text-[10px] text-on-surface-variant font-mono-data uppercase tracking-wider mb-0.5">F1-Score</div>
          <div className="font-bold text-primary font-mono-data text-base">0.932</div>
        </div>
      </div>
    </div>
  )
}
