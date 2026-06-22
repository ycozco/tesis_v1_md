import React, { useState, useEffect } from 'react'

export default function Users() {
  const [users, setUsers] = useState([])
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchUsersAndLogs = () => {
    setLoading(true)
    Promise.all([
      fetch('/api/users/list').then(res => res.json()),
      fetch('/api/users/logs').then(res => res.json())
    ])
      .then(([usersData, logsData]) => {
        setUsers(usersData)
        setLogs(logsData)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching users/logs:', err)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchUsersAndLogs()
  }, [])

  const handleToggleCondition = async (username, currentCond) => {
    const nextCond = currentCond === 'INTEGRADO' ? 'AISLADO' : 'INTEGRADO'
    
    try {
      const response = await fetch('/api/users/update-condition', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, condicion: nextCond })
      })

      if (response.ok) {
        fetchUsersAndLogs()
      } else {
        alert('Error al actualizar la condición del usuario.')
      }
    } catch (err) {
      console.error(err)
      alert('Error de red al actualizar la condición.')
    }
  }

  // Get Initials for avatar icon
  const getInitials = (name) => {
    if (!name) return 'OP'
    const parts = name.split(' ')
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase()
    }
    return name.slice(0, 2).toUpperCase()
  }

  return (
    <div className="flex-1 overflow-y-auto p-container-padding">
      <div className="max-w-7xl mx-auto space-y-card-gap">
        
        {/* Header */}
        <div className="flex justify-between items-end border-b border-white/10 pb-4 mb-6">
          <div>
            <h2 className="font-headline-lg text-headline-lg text-on-surface mb-1">Gestión de Usuarios</h2>
            <p className="font-body-md text-body-md text-on-surface-variant">Supervisión de telemetría y control de acceso al sistema.</p>
          </div>
          <button 
            className="glass-panel hover:bg-white/5 px-4 py-2 rounded-lg font-label-md text-label-md text-on-surface border border-outline/30 hover:border-primary transition-colors flex items-center gap-2"
            onClick={() => alert('Función de agregar usuario simulada para prototipo.')}
          >
            <span className="material-symbols-outlined text-[18px]">add</span>
            NUEVO OPERATIVO
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-[50vh]">
            <span className="material-symbols-outlined text-primary text-4xl animate-spin">sync</span>
            <span className="ml-3 text-lg font-medium text-primary">Cargando credenciales y logs...</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-card-gap">
            
            {/* Left Column: User Table (Spans 8 cols) */}
            <div className="lg:col-span-8 space-y-card-gap">
              <div className="glass-panel rounded-xl overflow-hidden flex flex-col h-[600px]">
                <div className="p-4 border-b border-white/10 bg-surface-container/20 flex justify-between items-center">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Registro de Operativos</h3>
                  <div className="relative">
                    <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">search</span>
                    <input className="bg-transparent border border-white/10 rounded-lg pl-9 pr-4 py-1.5 font-body-sm text-body-sm text-on-surface focus:border-primary focus:ring-0 focus:outline-none transition-colors w-64 glass-panel" placeholder="Buscar operativos..." type="text"/>
                  </div>
                </div>
                
                <div className="flex-1 overflow-auto">
                  <table className="w-full text-left border-collapse">
                    <thead className="sticky top-0 bg-surface-container-high/80 backdrop-blur-md border-b-2 border-primary z-10 font-label-md text-label-md text-on-surface-variant uppercase">
                      <tr>
                        <th className="py-3 px-4">OPERATIVO</th>
                        <th className="py-3 px-4">NIVEL DE ACCESO</th>
                        <th className="py-3 px-4">PROTOCOLO</th>
                        <th className="py-3 px-4">ESTADO</th>
                        <th className="py-3 px-4">ACCIONES</th>
                      </tr>
                    </thead>
                    <tbody className="font-mono-data text-mono-data text-on-surface divide-y divide-white/5">
                      {users.map(u => (
                        <tr key={u.username} className="hover:bg-white/[0.02] transition-colors group">
                          <td className="py-3 px-4">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-bold text-primary text-xs">
                                {getInitials(u.nombre)}
                              </div>
                              <div>
                                <div className="font-body-sm text-body-sm text-on-surface font-semibold">{u.nombre}</div>
                                <div className="text-[10px] text-on-surface-variant opacity-70">Activo {u.last_active}</div>
                              </div>
                            </div>
                          </td>
                          <td className="py-3 px-4">
                            <span className={u.rol === 'ADMIN' ? 'text-primary font-bold' : 'text-on-surface-variant'}>
                              {u.rol}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            {u.rol === 'AUDITOR' ? (
                              <span className={`px-2 py-0.5 rounded text-[10px] ${u.condicion === 'INTEGRADO' ? 'bg-primary/10 text-primary border border-primary/20' : 'bg-secondary/10 text-secondary border border-secondary/20'}`}>
                                {u.condicion === 'INTEGRADO' ? 'Condición A (Explicable)' : 'Condición B (Aislada)'}
                              </span>
                            ) : '-'}
                          </td>
                          <td className="py-3 px-4">
                            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-primary/10 text-primary border border-primary/20 text-[11px]">
                              <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span> {u.estado}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            {u.rol === 'AUDITOR' ? (
                              <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                <button 
                                  className="p-1 text-on-surface-variant hover:text-primary transition-colors" 
                                  title="Alternar Condición A/B"
                                  onClick={() => handleToggleCondition(u.username, u.condicion)}
                                >
                                  <span className="material-symbols-outlined text-[18px]">swap_horiz</span>
                                </button>
                                <button className="p-1 text-on-surface-variant hover:text-error transition-colors" title="Reiniciar Sesión" onClick={() => alert('Sesión de telemetría reiniciada.')}>
                                  <span className="material-symbols-outlined text-[18px]">lock_reset</span>
                                </button>
                              </div>
                            ) : '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            
            {/* Right Column: Security Logs (Spans 4 cols) */}
            <div className="lg:col-span-4 space-y-card-gap">
              <div className="glass-panel rounded-xl flex flex-col h-[600px] border-t-2 border-t-error">
                <div className="p-4 border-b border-white/10 bg-surface-container/20 flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-error">gpp_bad</span>
                    <h3 className="font-headline-sm text-headline-sm text-on-surface">Telemetría de Seguridad</h3>
                  </div>
                  <button className="text-on-surface-variant hover:text-primary transition-colors" onClick={fetchUsersAndLogs}><span className="material-symbols-outlined text-[20px]">refresh</span></button>
                </div>
                
                <div className="flex-1 overflow-auto p-4 space-y-3 font-mono-data text-[12px] leading-tight">
                  {logs.map((log, idx) => {
                    const isCritical = log.evento.includes('UNAUTHORIZED') || log.evento.includes('FAILURE');
                    const isWarning = log.evento.includes('CHANGE_CONDITION') || log.evento.includes('RESET');
                    
                    return (
                      <div 
                        key={log.id_log || idx} 
                        className={`p-3 rounded border relative overflow-hidden ${
                          isCritical ? 'border-error/30 bg-error/5 pulse-critical' : isWarning ? 'border-secondary/30 bg-secondary/5' : 'border-white/10 bg-white/5'
                        }`}
                      >
                        {isCritical && <div className="absolute left-0 top-0 bottom-0 w-1 bg-error"></div>}
                        {isWarning && <div className="absolute left-0 top-0 bottom-0 w-1 bg-secondary"></div>}
                        {!isCritical && !isWarning && <div className="absolute left-0 top-0 bottom-0 w-1 bg-outline-variant"></div>}
                        
                        <div className="flex justify-between items-start mb-1 text-on-surface-variant opacity-70">
                          <span>{log.fecha.split('T')[0]} {log.fecha.split('T')[1]?.split('.')[0]}</span>
                          <span className={`font-bold tracking-wider text-[9px] ${isCritical ? 'text-error' : isWarning ? 'text-secondary' : 'text-outline-variant'}`}>
                            {isCritical ? 'CRÍTICO' : isWarning ? 'ALERTA' : 'INFO'}
                          </span>
                        </div>
                        <div className="text-on-surface">{log.evento}</div>
                        <div className="mt-2 text-on-surface-variant flex items-center gap-1 text-[10px]">
                          <span className="material-symbols-outlined text-[12px]">dns</span> IP: {log.ip_address} · Operador: {log.usuario}
                        </div>
                      </div>
                    )
                  })}
                  {logs.length === 0 && (
                    <div className="text-center py-8 text-on-surface-variant">No hay logs de seguridad recientes.</div>
                  )}
                </div>
              </div>
            </div>

          </div>
        )}
      </div>
    </div>
  )
}
