import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './LoginEstudiante.css'; // Reutilizamos estilos

const LoginAgente = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/api/agentes/login`, formData);
      
      // Guardar token y datos del agente
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('agente_id', response.data.agente.id);
      localStorage.setItem('agente_nombre', response.data.agente.nombre);
      localStorage.setItem('tipo_usuario', 'agente');
      
      // Redirigir al dashboard de agente
      navigate(`/dashboard-agente/${response.data.agente.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>🎯 Portal de Agentes</h1>
          <p>Accede a tu panel de afiliados</p>
        </div>

        {error && (
          <div className="alert alert-error">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="tu@email.com"
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
            />
          </div>

          <button 
            type="submit" 
            className="btn-login"
            disabled={loading}
          >
            {loading ? 'Verificando...' : '🔐 Iniciar Sesión'}
          </button>
        </form>

        <div className="login-footer">
          <p>¿No tienes cuenta? Contacta al administrador</p>
          <button 
            onClick={() => navigate('/')}
            className="btn-secondary"
          >
            ← Volver al inicio
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginAgente;
