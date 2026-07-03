import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../App.jsx'

export default function Layout({ children }) {
  const { user, logout, condicion } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  
  const [searchTerm, setSearchTerm] = React.useState('')
  const [showNotifications, setShowNotifications] = React.useState(false)

  const handleSearchKeyPress = (e) => {
    if (e.key === 'Enter' && searchTerm.trim()) {
      navigate(`/alerts?search=${encodeURIComponent(searchTerm.trim())}`)
    }
  }
  
  const activePage = location.pathname.split('/')[1] || 'dashboard'

  const handleLogoutClick = (e) => {
    e.preventDefault()
    logout()
    navigate('/login')
  }

  // Helper to determine if a sidebar tab is active
  const isActive = (path) => activePage === path

  return (
    <div className="bg-background text-on-background font-body-md antialiased min-h-screen overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
      
      {/* TopNavBar (Web) */}
      <nav className="hidden md:flex justify-between items-center px-container-padding w-full h-16 bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl docked full-width top-0 border-b border-white/10 shadow-sm z-40 fixed">
        <div className="flex items-center gap-6">
          <span className="font-headline-md text-headline-md font-bold text-primary tracking-tight">Agro-Intelligence Oversight</span>
          <div className="hidden lg:flex items-center gap-1 bg-surface-container-high rounded-full px-4 py-1.5 ml-4 border border-white/5">
            <span className="material-symbols-outlined text-primary text-sm mr-2">search</span>
            <input 
              className="bg-transparent border-none text-body-sm text-on-surface focus:ring-0 w-48 placeholder:text-on-surface-variant/50 p-0" 
              placeholder="Buscar parámetros, dejas..." 
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyPress={handleSearchKeyPress}
            />
          </div>
        </div>
        <div className="flex items-center gap-8">
          <ul className="flex items-center gap-6">
            <li className="cursor-pointer active:scale-95 group flex flex-col items-center">
              <Link to="/telemetry" className={`font-body-md text-body-md transition-colors py-1 ${isActive('telemetry') ? 'text-primary' : 'text-on-surface-variant hover:text-primary'}`}>Telemetría</Link>
            </li>
            <li className="cursor-pointer active:scale-95 group flex flex-col items-center">
              <Link to="/alerts" className={`font-body-md text-body-md transition-colors py-1 ${isActive('alerts') ? 'text-primary' : 'text-on-surface-variant hover:text-primary'}`}>Auditorías</Link>
            </li>
            <li className="cursor-pointer active:scale-95 group flex flex-col items-center">
              <Link to="/data" className={`font-body-md text-body-md transition-colors py-1 ${isActive('data') ? 'text-primary' : 'text-on-surface-variant hover:text-primary'}`}>Inventario</Link>
            </li>
          </ul>
          <div className="flex items-center gap-4 border-l border-white/10 pl-6">
            <div className="relative">
              <button 
                onClick={() => setShowNotifications(!showNotifications)}
                aria-label="Notifications" 
                className="text-on-surface-variant hover:text-primary transition-colors active:scale-95 relative"
              >
                <span className="material-symbols-outlined">notifications</span>
                <span className="absolute top-0 right-0 w-2 h-2 bg-error rounded-full animate-pulse"></span>
              </button>
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 glass-panel bg-surface-container-high rounded-lg shadow-2xl p-4 border border-white/10 z-50 font-body-sm text-body-sm text-on-surface">
                  <div className="flex justify-between items-center border-b border-white/5 pb-2 mb-2 font-bold text-on-surface">
                    <span>Notificaciones Aduaneras</span>
                    <button className="text-xs text-primary hover:underline" onClick={() => setShowNotifications(false)}>Cerrar</button>
                  </div>
                  <ul className="space-y-2 max-h-48 overflow-y-auto">
                    <li className="p-2 hover:bg-white/5 rounded transition-colors text-error border-l-2 border-l-error text-left">
                      <strong>AL-2026-0012:</strong> Desviación del 11.1% detectada en Palta.
                    </li>
                    <li className="p-2 hover:bg-white/5 rounded transition-colors text-secondary border-l-2 border-l-secondary text-left">
                      <strong>AL-2026-0014:</strong> Retraso logístico (+5 días) en Mango.
                    </li>
                    <li className="p-2 hover:bg-white/5 rounded transition-colors text-on-surface-variant text-left">
                      Sistema de IA en línea. Modelos analíticos sincronizados.
                    </li>
                  </ul>
                </div>
              )}
            </div>
            <button aria-label="Settings" className="text-on-surface-variant hover:text-primary transition-colors active:scale-95" onClick={() => navigate('/config')}>
              <span className="material-symbols-outlined">settings</span>
            </button>
            <div className="flex items-center gap-2 ml-2">
              <span className="text-body-sm text-on-surface font-medium">{user?.nombre || 'Auditor'}</span>
              <div 
                className="w-8 h-8 rounded-full bg-surface-container-high border border-primary/30 overflow-hidden cursor-pointer"
                onClick={() => navigate('/users')}
              >
                <img 
                  alt="Perfil" 
                  className="w-full h-full object-cover" 
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCxwvAsWimcF03V3njsUr4hg_f38wYuUsLCKv-xiu1PqPz3NR0-RIDqBBNh9BwgAvS4ns7FUNBXzxJ7wtir0npR8M3RPlm_whruKlOLHu7mBAhj9UF9FC6Ux9yZFTa-bKIkz5L2xU5CG3U1ETCNh4zAtHRLCE0utlfji8bJ1Tbf87aVkzvF-PF-2Slr3QZHlE-nDxHkXAMrMMDeWRV6ituElBxadSzZzBDRq378bk6lfFuG5I7oDw0ZHMmUPmTDlExpdWyT9v48Xv4"
                />
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Contenedor Lateral y Contenido Principal */}
      <div className="flex h-screen pt-16 md:pt-0">
        
        {/* SideNavBar (Hidden on Mobile) */}
        <aside className="hidden md:flex flex-col py-6 bg-surface-container-lowest dark:bg-surface-container-lowest h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 border-r border-white/5 shadow-2xl group overflow-hidden">
          {/* Header */}
          <div className="flex items-center px-4 mb-8 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center border border-white/10 shrink-0">
              <span className="material-symbols-outlined text-primary">terminal</span>
            </div>
            <div className="ml-3">
              <div className="font-headline-sm text-headline-sm text-primary-fixed leading-tight">AUDIT_OS_V1</div>
              <div className="font-label-md text-label-md text-primary/70 uppercase tracking-wider text-[10px]">Terminal Activa</div>
            </div>
          </div>
          {/* Main Tabs */}
          <nav className="flex-1 overflow-y-auto">
            <ul className="space-y-2">
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('dashboard') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/dashboard"
                >
                  <span className="material-symbols-outlined shrink-0">dashboard</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Dashboard</span>
                </Link>
              </li>
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('alerts') || isActive('alert') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/alerts"
                >
                  <span className="material-symbols-outlined shrink-0">security_update_warning</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Bandeja Alertas</span>
                </Link>
              </li>
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('data') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/data"
                >
                  <span className="material-symbols-outlined shrink-0">monitoring</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Explorar Datos</span>
                </Link>
              </li>
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('history') || isActive('decision') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/history"
                >
                  <span className="material-symbols-outlined shrink-0">fact_check</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Historial Auditorías</span>
                </Link>
              </li>
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('config') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/config"
                >
                  <span className="material-symbols-outlined shrink-0">settings</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Configuración</span>
                </Link>
              </li>
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('integrity') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/integrity"
                >
                  <span className="material-symbols-outlined shrink-0">shield</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Integridad y Sesgo</span>
                </Link>
              </li>
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('users') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/users"
                >
                  <span className="material-symbols-outlined shrink-0">supervisor_account</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Control Usuarios</span>
                </Link>
              </li>
              <li>
                <Link 
                  className={`flex items-center px-4 py-3 ${isActive('telemetry') ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/20'} rounded-lg mx-2 transition-all duration-300`} 
                  to="/telemetry"
                >
                  <span className="material-symbols-outlined shrink-0">science</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Telemetría Experimento</span>
                </Link>
              </li>
            </ul>
          </nav>
          {/* CTA */}
          <div className="px-4 my-6 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
            <button className="w-full bg-primary/10 hover:bg-primary/20 border border-primary text-primary font-label-md text-label-md uppercase tracking-wider py-2 rounded-lg transition-colors flex items-center justify-center gap-2">
              <span className="material-symbols-outlined text-[18px]">download</span>
              Exportar Reporte
            </button>
          </div>
          {/* Footer Tabs */}
          <div className="mt-auto border-t border-white/5 pt-4">
            <ul className="space-y-2">
              <li>
                <a className="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="/support" onClick={(e) => e.preventDefault()}>
                  <span className="material-symbols-outlined shrink-0">help</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Soporte</span>
                </a>
              </li>
              <li>
                <a className="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="/logout" onClick={handleLogoutClick}>
                  <span className="material-symbols-outlined shrink-0">logout</span>
                  <span className="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Cerrar Sesión</span>
                </a>
              </li>
            </ul>
          </div>
        </aside>

        {/* Lienzo de Contenido Principal */}
        <main className="flex-1 md:ml-20 w-full overflow-y-auto bg-background px-4 md:px-container-padding py-8 md:pt-24 pb-24 relative z-10">
          {/* Global Environment Banner */}
          <div className="mb-6 flex items-center justify-center w-full py-1.5 glass-panel rounded-md border-tertiary/30 bg-tertiary/5 text-tertiary font-mono-data text-mono-data uppercase">
            <span className="material-symbols-outlined text-[16px] mr-2">science</span>
            {condicion && (condicion === 'INTEGRADO' || condicion === 'AISLADO') ? (
              <span>ENTORNO DE PRUEBA · EVALUACIÓN EN CURSO ({condicion})</span>
            ) : (
              <span>ENTORNO DE DEMOSTRACIÓN · DATOS SINTÉTICOS</span>
            )}
          </div>

          {children}
        </main>
      </div>

      {/* Navegación Móvil Inferior */}
      <nav className="md:hidden fixed bottom-0 w-full h-16 bg-surface-container/80 backdrop-blur-xl border-t border-white/5 z-50 flex justify-around items-center px-2 pb-safe">
        <Link className={`flex flex-col items-center justify-center w-16 h-full ${isActive('dashboard') ? 'text-primary' : 'text-on-surface-variant'}`} to="/dashboard">
          <div className={`w-12 h-8 ${isActive('dashboard') ? 'bg-primary-container' : ''} rounded-full flex items-center justify-center mb-1`}>
            <span className="material-symbols-outlined">dashboard</span>
          </div>
          <span className="font-label-md text-[10px] tracking-tight">Inicio</span>
        </Link>
        <Link className={`flex flex-col items-center justify-center w-16 h-full ${isActive('alerts') ? 'text-primary' : 'text-on-surface-variant'}`} to="/alerts">
          <div className={`w-12 h-8 ${isActive('alerts') ? 'bg-primary-container' : ''} rounded-full flex items-center justify-center mb-1`}>
            <span className="material-symbols-outlined">fact_check</span>
          </div>
          <span className="font-label-md text-[10px] tracking-tight">Alertas</span>
        </Link>
        <Link className={`flex flex-col items-center justify-center w-16 h-full ${isActive('history') ? 'text-primary' : 'text-on-surface-variant'}`} to="/history">
          <div className={`w-12 h-8 ${isActive('history') ? 'bg-primary-container' : ''} rounded-full flex items-center justify-center mb-1`}>
            <span className="material-symbols-outlined">history</span>
          </div>
          <span className="font-label-md text-[10px] tracking-tight">Historial</span>
        </Link>
        <Link className={`flex flex-col items-center justify-center w-16 h-full ${isActive('telemetry') ? 'text-primary' : 'text-on-surface-variant'}`} to="/telemetry">
          <div className={`w-12 h-8 ${isActive('telemetry') ? 'bg-primary-container' : ''} rounded-full flex items-center justify-center mb-1`}>
            <span className="material-symbols-outlined">science</span>
          </div>
          <span className="font-label-md text-[10px] tracking-tight">Test</span>
        </Link>
      </nav>

    </div>
  )
}
