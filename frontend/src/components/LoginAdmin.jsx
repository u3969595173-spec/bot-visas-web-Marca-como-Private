import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './LoginEstudiante.css'

function LoginAdmin({ onLogin }) {
  const [formData, setFormData] = useState({
    usuario: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const getApiUrl = () => {
    if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL
    const hostname = window.location.hostname
    return (hostname === 'localhost' || hostname === '127.0.0.1')
      ? 'http://localhost:8000'
      : `http://${hostname}:8000`
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const username = (formData.usuario || '').trim()
    const password = (formData.password || '').trim()

    if (!username || !password) {
      setError('Usuario y contraseña requeridos.')
      setLoading(false)
      return
    }

    try {
      const apiUrl = getApiUrl()
      const response = await axios.post(`${apiUrl}/api/admin/login`, {
        usuario: username,
        password: password
      }, { timeout: 8000 })

      const { token, usuario, role } = response.data

      localStorage.setItem('token', token)
      localStorage.setItem('usuario', usuario)
      localStorage.setItem('capital_trade_user', JSON.stringify({
        id: 'admin-1',
        name: usuario,
        email: username,
        role: role || 'admin'
      }))

      window.dispatchEvent(new Event('capital-trade-sync'))

      if (typeof onLogin === 'function') {
        onLogin({ id: 'admin-1', name: usuario, email: username, role: role || 'admin' })
      }

      navigate('/admin')
    } catch (err) {
      let errorMsg = 'Error al iniciar sesión. Verifica tus credenciales.'

      if (err.code === 'ECONNABORTED') {
        errorMsg = 'El servidor tardó demasiado. Verifica tu conexión de red.'
      } else if (err.response?.status === 401 || err.response?.status === 403) {
        errorMsg = 'Credenciales incorrectas. Verifica usuario y contraseña.'
      } else if (err.response?.data?.detail) {
        errorMsg = Array.isArray(err.response.data.detail)
          ? err.response.data.detail[0]?.msg || errorMsg
          : err.response.data.detail
      } else if (err.code === 'ERR_NETWORK') {
        errorMsg = 'No se puede conectar al servidor. ¿Está en línea?'
      }

      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-estudiante-container">
      <div className="login-estudiante-card">
        <div className="login-header">
          <p className="section-label">Panel admin</p>
          <h1>Acceso administrativo</h1>
          <p>Control del portafolio, operaciones, documentos y seguimiento comercial.</p>
        </div>

        <div className="portal-cta-group">
          <button className="portal-cta btn-secondary" onClick={() => navigate('/login')}>Inversor</button>
          <button className="portal-cta btn-primary">Administrador</button>
        </div>

        {error && <div className="alert alert-error">⚠️ {error}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Usuario</label>
            <input
              type="text"
              name="usuario"
              value={formData.usuario}
              onChange={handleChange}
              required
              placeholder="Tu usuario"
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label>Contraseña</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Iniciando sesión...' : 'Iniciar sesión'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default LoginAdmin
