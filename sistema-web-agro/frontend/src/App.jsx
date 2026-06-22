import React, { useState, useEffect, createContext, useContext } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import Layout from './components/Layout.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Alerts from './pages/Alerts.jsx'
import Detail from './pages/Detail.jsx'
import History from './pages/History.jsx'
import AuditDetail from './pages/AuditDetail.jsx'
import Config from './pages/Config.jsx'
import Integrity from './pages/Integrity.jsx'
import Users from './pages/Users.jsx'
import Telemetry from './pages/Telemetry.jsx'
import Data from './pages/Data.jsx'

// Create Auth Context
const AuthContext = createContext(null)

export const useAuth = () => useContext(AuthContext)

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth()
  if (!user) {
    return <Navigate to="/login" replace />
  }
  return children
}

const AppContent = () => {
  const { user, login, logout, condicion } = useAuth()
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/dashboard" replace /> : <Login />} />
      
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Layout><Dashboard /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/alerts" element={
        <ProtectedRoute>
          <Layout><Alerts /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/alert/:id_alerta" element={
        <ProtectedRoute>
          <Layout><Detail /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/history" element={
        <ProtectedRoute>
          <Layout><History /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/decision/:id_decision" element={
        <ProtectedRoute>
          <Layout><AuditDetail /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/config" element={
        <ProtectedRoute>
          <Layout><Config /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/integrity" element={
        <ProtectedRoute>
          <Layout><Integrity /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/users" element={
        <ProtectedRoute>
          <Layout><Users /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/telemetry" element={
        <ProtectedRoute>
          <Layout><Telemetry /></Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/data" element={
        <ProtectedRoute>
          <Layout><Data /></Layout>
        </ProtectedRoute>
      } />

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

export default function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('agro_user')
    return saved ? JSON.parse(saved) : null
  })
  
  const [token, setToken] = useState(() => {
    return localStorage.getItem('agro_token') || null
  })

  const [condicion, setCondicion] = useState(() => {
    return localStorage.getItem('agro_condicion') || null
  })

  const login = (userData, tokenVal, condVal) => {
    setUser(userData)
    setToken(tokenVal)
    setCondicion(condVal)
    localStorage.setItem('agro_user', JSON.stringify(userData))
    localStorage.setItem('agro_token', tokenVal)
    localStorage.setItem('agro_condicion', condVal)
  }

  const logout = () => {
    const username = user?.username || 'anonymous'
    
    // Call logout endpoint
    fetch('/api/auth/logout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username })
    }).catch(err => console.log('Error during logout api call:', err))

    setUser(null)
    setToken(null)
    setCondicion(null)
    localStorage.removeItem('agro_user')
    localStorage.removeItem('agro_token')
    localStorage.removeItem('agro_condicion')
  }

  return (
    <AuthContext.Provider value={{ user, token, condicion, setCondicion, login, logout }}>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AuthContext.Provider>
  )
}
