import { Button } from '../components/ui/button.jsx'
import { Leaf, UserRound, LockKeyhole, Eye, EyeOff, LogIn, CircleAlert } from 'lucide-react'
import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { sessionReturnPath } from '../lib/sessionNavigation.js'
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
  const location = useLocation()

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
        navigate(sessionReturnPath(location.state?.from), { replace: true })
      } else {
        setErrorMsg(data.message || (typeof data.detail === 'string' ? data.detail : 'Credenciales inválidas. Acceso denegado.'))
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
    <div className="research-shell research-login text-on-surface min-h-screen flex items-center justify-center relative overflow-hidden font-body-md">
      <div className="research-login-decoration absolute inset-0 z-0" aria-hidden="true" />
      <main className="w-full max-w-md px-container-padding relative z-10">
        {/* Logo Area */}
        <div className="text-center mb-8">
          <h1 className="font-display-lg text-display-lg text-primary flex items-center justify-center gap-2 mb-2">
            <Leaf size={40} strokeWidth={1.5} aria-hidden="true" />
          </h1>
          <h2 className="font-headline-md text-headline-md text-on-surface tracking-tight">AgroScope Perú</h2>
          <p className="font-body-sm text-body-sm text-on-surface-variant mt-2">Palta, uva fresca y arándano · Análisis comparativo y pronóstico</p>
        </div>

        {/* Glassmorphism Card */}
        <div className={`ui-card rounded-xl p-8 relative overflow-hidden transition-transform ${shake ? 'animate-shake' : ''}`}>
          {/* Subtle top border highlight */}


          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface">Acceso al sistema</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Consulte series semanales, resultados de desarrollo y evidencia documental.</p>

              {errorMsg && (
                <div role="alert" className="bg-error/20 border border-error/50 p-4 rounded-lg text-error text-body-sm mt-4 flex items-center gap-2">
                  <CircleAlert size={18} aria-hidden="true" />
                  <span>{errorMsg}</span>
                </div>
              )}
            </div>

            {/* Username/Email Field */}
            <div className="space-y-2 relative group">
              <label className="font-label-md text-label-md text-on-surface-variant block" htmlFor="identifier">Usuario o correo</label>
              <div className="relative">
                <UserRound size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-outline" aria-hidden="true" />
                <input
                  className="input-glass w-full rounded-lg py-3 pl-10 pr-4 font-body-md text-body-md text-on-surface placeholder:text-outline-variant ui-input"
                  id="identifier"
                  name="identifier"
                  placeholder="Usuario o correo registrado"
                  required
                  type="text"
                  autoComplete="username"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="space-y-2 relative group">
              <label className="font-label-md text-label-md text-on-surface-variant block flex justify-between" htmlFor="password">
                <span>Contraseña</span>
              </label>
              <div className="relative">
                <LockKeyhole size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-outline" aria-hidden="true" />
                <input
                  className="input-glass w-full rounded-lg py-3 pl-10 pr-12 font-body-md text-body-md text-on-surface placeholder:text-outline-variant ui-input"
                  id="password"
                  name="password"
                  placeholder="Ingrese clave de acceso"
                  required
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-outline hover:text-on-surface transition-colors focus:outline-none"
                  id="togglePassword"
                  aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  <span aria-hidden="true">{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</span>
                </button>
              </div>
            </div>

            {/* Action Button */}
            <Button
              className="w-full mt-8"
              type="submit"
              disabled={loading}
            >
              <span>{loading ? 'Ingresando...' : 'Ingresar'}</span>
              <LogIn size={18} aria-hidden="true" />
            </Button>

            {/* System Status */}
            <div className="flex items-center justify-center gap-2 mt-6 pt-6 border-t border-white/10">
              <span className="w-2 h-2 rounded-full bg-primary"></span>
              <span className="font-body-sm text-body-sm text-on-surface-variant">Entorno de investigación · evaluación técnica</span>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}
