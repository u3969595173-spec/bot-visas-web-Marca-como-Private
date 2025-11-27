import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function LoginAdmin({ onLogin }) {
  const [formData, setFormData] = useState({
    usuario: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.post(`${apiUrl}/api/login`, formData)
      
      // Guardar token
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('usuario', response.data.usuario)
      
      // Configurar axios para usar el token en futuras peticiones
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
      
      onLogin()
      navigate('/admin/dashboard')
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Error al iniciar sesión. Verifica tus credenciales.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '450px', margin: '80px auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <div style={{ fontSize: '64px', marginBottom: '15px' }}>🔐</div>
          <h2>Acceso Administrador</h2>
          <p style={{ color: '#718096', marginTop: '10px' }}>
            Ingresa tus credenciales para acceder al panel
          </p>
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Usuario</label>
            <input
              type="text"
              name="usuario"
              value={formData.usuario}
              onChange={handleChange}
              required
              placeholder="admin"
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

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ width: '100%', marginTop: '10px' }}
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default LoginAdmin
