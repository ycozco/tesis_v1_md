import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../App.jsx'

export default function Login() {
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')
  const [shake, setShake] = useState(false)
  const [loading, setLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setErrorMsg('')
    setShake(false)
    
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier, password })
      })

      const data = await response.json()
      
      if (response.ok) {
        login(data.user, data.token, data.condicion)
        navigate('/dashboard')
      } else {
        setErrorMsg(data.message || 'Credenciales inválidas. Acceso denegado.')
        setShake(true)
        setTimeout(() => setShake(false), 500)
      }
    } catch (err) {
      setErrorMsg('Error de red. No se pudo conectar al servidor.')
      setShake(true)
      setTimeout(() => setShake(false), 500)
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-background text-on-background min-h-screen flex items-center justify-center relative overflow-hidden font-body-md">
      {/* Background Texture */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-surface-container-lowest via-background to-surface-container-highest"></div>
        <div className="absolute inset-0 grid-bg"></div>
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-container rounded-full mix-blend-screen filter blur-[120px] opacity-20 animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-tertiary-container rounded-full mix-blend-screen filter blur-[120px] opacity-10"></div>
      </div>
      
      {/* Login Container */}
      <main className="w-full max-w-md px-container-padding relative z-10">
        {/* Logo Area */}
        <div className="text-center mb-8">
          <h1 className="font-display-lg text-display-lg text-primary flex items-center justify-center gap-2 mb-2">
            <span className="material-symbols-outlined" style={{ fontSize: '48px', fontVariationSettings: "'FILL' 1" }}>eco</span>
          </h1>
          <h2 className="font-headline-md text-headline-md text-on-surface tracking-tight">Agro-Intelligence Oversight</h2>
          <p className="font-body-sm text-body-sm text-on-surface-variant mt-2">Nivel de Vigilancia: Alto · Terminal Seguro</p>
        </div>
        
        {/* Glassmorphism Card */}
        <div className={`glass-card rounded-xl p-8 relative overflow-hidden transition-transform ${shake ? 'animate-shake' : ''}`}>
          {/* Subtle top border highlight */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-primary to-transparent opacity-50"></div>
          
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface">Autenticación del Operador</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Ingrese sus credenciales para acceder al sistema de supervisión de telemetría.</p>
              
              {errorMsg && (
                <div className="bg-error/20 border border-error/50 p-4 rounded-lg text-error text-body-sm mt-4 flex items-center gap-2">
                  <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>error</span>
                  <span>{errorMsg}</span>
                </div>
              )}
            </div>
            
            {/* Username/Email Field */}
            <div className="space-y-2 relative group">
              <label className="font-label-md text-label-md text-on-surface-variant block" htmlFor="identifier">ID de Auditor / Correo</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline group-focus-within:text-primary transition-colors">person</span>
                <input 
                  className="input-glass w-full rounded-lg py-3 pl-10 pr-4 font-body-md text-body-md text-on-surface placeholder:text-outline-variant glass-input" 
                  id="identifier" 
                  name="identifier" 
                  placeholder="ej. auditor1 o correo" 
                  required 
                  type="text"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                />
              </div>
            </div>
            
            {/* Password Field */}
            <div className="space-y-2 relative group">
              <label className="font-label-md text-label-md text-on-surface-variant block flex justify-between" htmlFor="password">
                <span>Código de Acceso</span>
                <a className="text-primary hover:text-primary-fixed transition-colors" href="#forgot" onClick={(e) => e.preventDefault()}>¿Olvidó su código?</a>
              </label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline group-focus-within:text-primary transition-colors">lock</span>
                <input 
                  className="input-glass w-full rounded-lg py-3 pl-10 pr-12 font-body-md text-body-md text-on-surface placeholder:text-outline-variant glass-input" 
                  id="password" 
                  name="password" 
                  placeholder="Ingrese clave de acceso" 
                  required 
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button 
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-outline hover:text-on-surface transition-colors focus:outline-none" 
                  id="togglePassword" 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  <span className="material-symbols-outlined" id="visibilityIcon">
                    {showPassword ? 'visibility_off' : 'visibility'}
                  </span>
                </button>
              </div>
            </div>
            
            {/* Action Button */}
            <button 
              className="w-full bg-primary-container text-on-primary-container font-headline-sm text-headline-sm rounded-lg py-3 px-6 mt-8 flex items-center justify-center gap-2 btn-glow transition-all duration-200 transform active:scale-95 disabled:opacity-50" 
              type="submit"
              disabled={loading}
            >
              <span>{loading ? 'Autorizando...' : 'Autorizar Acceso'}</span>
              <span className="material-symbols-outlined">login</span>
            </button>
            
            {/* System Status */}
            <div className="flex items-center justify-center gap-2 mt-6 pt-6 border-t border-white/10">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse shadow-[0_0_8px_#76db8f]"></span>
              <span className="font-mono-data text-mono-data text-on-surface-variant tracking-wider uppercase">Cifrado de grado militar activo</span>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}
