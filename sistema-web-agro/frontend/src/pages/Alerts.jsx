import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [producto, setProducto] = useState('')
  const [estado, setEstado] = useState('')
  const [severity, setSeverity] = useState('')
  
  const navigate = useNavigate()

  const fetchAlerts = () => {
    setLoading(true)
    const params = new URLSearchParams()
    if (search) params.append('search', search)
    if (producto) params.append('producto', producto)
    if (estado) params.append('estado', estado)

    fetch(`/api/alerts?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        // Filter by severity locally since database stores raw score_anomalia
        let filtered = data
        if (severity) {
          filtered = data.filter(alert => {
            const score = alert.score_anomalia
            if (severity === 'critical') return score > 0.8
            if (severity === 'high') return score > 0.6 && score <= 0.8
            if (severity === 'medium') return score > 0.4 && score <= 0.6
            if (severity === 'low') return score <= 0.4
            return true
          })
        }
        setAlerts(filtered)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching alerts:', err)
        setLoading(false)
      })
  }

  useEffect(() => {
    // Debounce search slightly or just trigger on change
    fetchAlerts()
  }, [search, producto, estado, severity])

  const handleClearFilters = () => {
    setSearch('')
    setProducto('')
    setEstado('')
    setSeverity('')
  }

  // Helpers to render labels and badges
  const getSeverityBadge = (score) => {
    if (score > 0.8) {
      return (
        <span className="bg-error/10 text-error border border-error/20 px-2.5 py-1 rounded font-label-md text-[10px] uppercase inline-flex items-center gap-1">
          <span className="material-symbols-outlined text-[14px]">warning</span> Crítico
        </span>
      )
    } else if (score > 0.6) {
      return (
        <span className="bg-secondary/10 text-secondary border border-secondary/20 px-2.5 py-1 rounded font-label-md text-[10px] uppercase inline-flex items-center gap-1">
          <span className="material-symbols-outlined text-[14px]">priority_high</span> Alto
        </span>
      )
    } else if (score > 0.4) {
      return (
        <span className="bg-tertiary/10 text-tertiary border border-tertiary/20 px-2.5 py-1 rounded font-label-md text-[10px] uppercase inline-flex items-center gap-1">
          <span className="material-symbols-outlined text-[14px]">info</span> Medio
        </span>
      )
    } else {
      return (
        <span className="bg-primary/10 text-primary border border-primary/20 px-2.5 py-1 rounded font-label-md text-[10px] uppercase inline-flex items-center gap-1">
          <span className="material-symbols-outlined text-[14px]">check_circle</span> Bajo
        </span>
      )
    }
  }

  const getEstadoBadge = (status) => {
    const statusMap = {
      'PENDIENTE': { text: 'Pendiente', style: 'text-error border border-error/35 bg-error/5' },
      'EN_REVISION': { text: 'En Revisión', style: 'text-tertiary border border-tertiary/35 bg-tertiary/5' },
      'CONFIRMADA': { text: 'Confirmado', style: 'text-primary border border-primary/35 bg-primary/5' },
      'FALSA_ALARMA': { text: 'Descartado', style: 'text-outline border border-outline/35 bg-outline/5' },
      'REFIERE_INSPECCION': { text: 'Inspección', style: 'text-secondary border border-secondary/35 bg-secondary/5' }
    }
    const item = statusMap[status] || { text: status, style: 'text-on-surface' }
    return (
      <span className={`${item.style} px-2.5 py-1 rounded font-label-md text-[10px] uppercase`}>
        {item.text}
      </span>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-end justify-between mb-card-gap shrink-0 gap-4">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface mb-1">Bandeja de Alertas de Telemetría</h1>
          <p className="font-body-md text-body-md text-on-surface-variant">Monitoreo de desviaciones en tiempo real en flujos de datos agroexportadores.</p>
        </div>
        <div className="flex gap-3">
          <button className="glass-panel hover:bg-white/5 border border-white/10 px-4 py-2 rounded font-label-md text-label-md flex items-center gap-2 text-on-surface">
            <span className="material-symbols-outlined text-[18px]">rule</span> Asignación Masiva
          </button>
          <button 
            className="bg-primary hover:bg-primary-fixed text-on-primary px-4 py-2 rounded font-label-md text-label-md font-semibold flex items-center gap-2"
            onClick={fetchAlerts}
          >
            <span className="material-symbols-outlined text-[18px]">refresh</span> Sincronizar Datos
          </button>
        </div>
      </header>

      {/* Advanced Filter Bar (Glass Panel) */}
      <section className="glass-panel rounded-xl p-4 mb-card-gap shrink-0 flex flex-col lg:flex-row gap-4 items-center">
        {/* Search Input */}
        <div className="relative w-full lg:w-1/3">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline">search</span>
          <input 
            className="glass-input w-full pl-10 pr-4 py-2 rounded font-body-sm text-body-sm text-on-surface placeholder:text-outline-variant focus:ring-0" 
            placeholder="Buscar ID / DAM / RUC..." 
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex flex-wrap md:flex-nowrap gap-4 w-full lg:w-2/3">
          {/* Product Filter */}
          <div className="flex-1 min-w-[120px]">
            <select 
              className="glass-input w-full px-3 py-2 rounded font-body-sm text-body-sm text-on-surface appearance-none focus:ring-0 cursor-pointer"
              value={producto}
              onChange={(e) => setProducto(e.target.value)}
            >
              <option className="bg-surface-container text-on-surface" value="">Producto: Todos</option>
              <option className="bg-surface-container text-on-surface" value="Palta">Palta</option>
              <option className="bg-surface-container text-on-surface" value="Uva">Uva</option>
              <option className="bg-surface-container text-on-surface" value="Arándano">Arándano</option>
              <option className="bg-surface-container text-on-surface" value="Mango">Mango</option>
            </select>
          </div>
          {/* Severity Filter */}
          <div className="flex-1 min-w-[120px]">
            <select 
              className="glass-input w-full px-3 py-2 rounded font-body-sm text-body-sm text-on-surface appearance-none focus:ring-0 cursor-pointer"
              value={severity}
              onChange={(e) => setSeverity(e.target.value)}
            >
              <option className="bg-surface-container text-on-surface" value="">Severidad: Todas</option>
              <option className="bg-surface-container text-on-surface" value="critical">Crítico</option>
              <option className="bg-surface-container text-on-surface" value="high">Alto</option>
              <option className="bg-surface-container text-on-surface" value="medium">Medio</option>
              <option className="bg-surface-container text-on-surface" value="low">Bajo</option>
            </select>
          </div>
          {/* Status Filter */}
          <div className="flex-1 min-w-[120px]">
            <select 
              className="glass-input w-full px-3 py-2 rounded font-body-sm text-body-sm text-on-surface appearance-none focus:ring-0 cursor-pointer"
              value={estado}
              onChange={(e) => setEstado(e.target.value)}
            >
              <option className="bg-surface-container text-on-surface" value="">Estado: Todos</option>
              <option className="bg-surface-container text-on-surface" value="PENDIENTE">Pendiente</option>
              <option className="bg-surface-container text-on-surface" value="EN_REVISION">En Revisión</option>
              <option className="bg-surface-container text-on-surface" value="CONFIRMADA">Confirmado</option>
              <option className="bg-surface-container text-on-surface" value="FALSA_ALARMA">Descartado</option>
              <option className="bg-surface-container text-on-surface" value="REFIERE_INSPECCION">Requiere Inspección</option>
            </select>
          </div>
        </div>
        <button 
          className="shrink-0 p-2 text-on-surface-variant hover:text-primary transition-colors" 
          title="Limpiar Filtros"
          onClick={handleClearFilters}
        >
          <span className="material-symbols-outlined">filter_alt_off</span>
        </button>
      </section>

      {/* Data Table Container */}
      <section className="glass-panel rounded-xl flex-1 flex flex-col overflow-hidden relative min-h-[400px]">
        {loading ? (
          <div className="flex-grow flex items-center justify-center">
            <span className="material-symbols-outlined text-primary text-4xl animate-spin">sync</span>
            <span className="ml-3 text-on-surface font-medium">Buscando operaciones aduaneras...</span>
          </div>
        ) : (
          <>
            <div className="table-container overflow-auto flex-1">
              <table className="w-full text-left border-collapse audit-table whitespace-nowrap">
                <thead className="sticky top-0 z-10 font-label-md text-label-md text-on-surface uppercase tracking-wider bg-surface-container-high/90 backdrop-blur-md">
                  <tr className="border-b border-white/10">
                    <th className="px-4 py-3 w-12 text-center"><input className="rounded-sm bg-transparent border-outline" type="checkbox"/></th>
                    <th className="px-4 py-3">ID ALERTA</th>
                    <th className="px-4 py-3">DAM</th>
                    <th className="px-4 py-3">FECHA</th>
                    <th className="px-4 py-3">PRODUCTO</th>
                    <th className="px-4 py-3">EXPORTADORA</th>
                    <th className="px-4 py-3">DESTINO</th>
                    <th className="px-4 py-3 text-right">VALOR FOB</th>
                    <th className="px-4 py-3 text-right">Desv %</th>
                    <th className="px-4 py-3 text-center">Score</th>
                    <th className="px-4 py-3 text-center">Severidad</th>
                    <th className="px-4 py-3 text-center">Estado</th>
                    <th className="px-4 py-3 w-12"></th>
                  </tr>
                </thead>
                <tbody className="font-mono-data text-mono-data text-on-surface-variant divide-y divide-white/5">
                  {alerts.map(alert => {
                    const dev = (((alert.valor_fob_esperado - alert.valor_fob_declarado) / alert.valor_fob_esperado) * 100).toFixed(1)
                    return (
                      <tr 
                        key={alert.id_alerta} 
                        className="hover:bg-white/5 transition-colors group cursor-pointer"
                        onClick={() => navigate(`/alert/${alert.id_alerta}`)}
                      >
                        <td className="px-4 py-3 text-center" onClick={(e) => e.stopPropagation()}>
                          <input className="rounded-sm bg-transparent border-outline" type="checkbox"/>
                        </td>
                        <td className="px-4 py-3 text-primary font-bold">{alert.id_alerta}</td>
                        <td className="px-4 py-3">{alert.numero_dam}</td>
                        <td className="px-4 py-3 text-body-sm font-body-sm">{alert.fecha_operacion}</td>
                        <td className="px-4 py-3">
                          <span className="flex items-center gap-2">
                            <span className={`w-2 h-2 rounded-full ${alert.producto === 'Palta' ? 'bg-[#4A7C59]' : alert.producto === 'Uva' ? 'bg-[#8B5A8C]' : alert.producto === 'Arándano' ? 'bg-[#3B5998]' : 'bg-[#C28C38]'}`}></span>
                            {alert.producto}
                          </span>
                        </td>
                        <td className="px-4 py-3 font-body-sm truncate max-w-[180px]">{alert.razon_social}</td>
                        <td className="px-4 py-3">Rotterdam (NLRTM)</td>
                        <td className="px-4 py-3 text-right">${alert.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                        <td className={`px-4 py-3 text-right ${parseFloat(dev) > 0 ? 'text-error' : 'text-[#ffb4ab]'}`}>
                          {parseFloat(dev) > 0 ? `+${dev}%` : `${dev}%`}
                        </td>
                        <td className="px-4 py-3 text-center">{(alert.score_anomalia * 100).toFixed(1)}</td>
                        <td className="px-4 py-3 text-center">
                          {getSeverityBadge(alert.score_anomalia)}
                        </td>
                        <td className="px-4 py-3 text-center">
                          {getEstadoBadge(alert.estado)}
                        </td>
                        <td className="px-4 py-3 text-center">
                          <button className="text-outline hover:text-primary transition-colors opacity-0 group-hover:opacity-100">
                            <span className="material-symbols-outlined">chevron_right</span>
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                  {alerts.length === 0 && (
                    <tr>
                      <td colSpan="13" className="py-8 text-center text-on-surface-variant font-body-md">No se encontraron alertas registradas en el sistema.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            {/* Table Footer / Pagination */}
            <div className="border-t border-white/5 p-4 flex justify-between items-center bg-surface-container-low shrink-0">
              <div className="font-body-sm text-body-sm text-on-surface-variant">
                Mostrando <span className="text-on-surface font-semibold">{alerts.length}</span> registros cargados.
              </div>
              <div className="flex gap-2">
                <button className="px-3 py-1 glass-panel rounded text-outline hover:text-primary disabled:opacity-50" disabled>
                  <span className="material-symbols-outlined text-[20px]">chevron_left</span>
                </button>
                <button className="px-3 py-1 glass-panel rounded text-primary border-primary bg-primary/10 font-mono-data text-mono-data">1</button>
                <button className="px-3 py-1 glass-panel rounded text-on-surface-variant hover:text-primary disabled:opacity-50" disabled>
                  <span className="material-symbols-outlined text-[20px]">chevron_right</span>
                </button>
              </div>
            </div>
          </>
        )}
      </section>
    </div>
  )
}
