import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useSearchParams } from 'react-router-dom';
import './RegistroEstudiante.css';

const RegistroAgente = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    password: '',
    confirmarPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [tokenValido, setTokenValido] = useState(false);

  const TOKEN_ADMIN = 'AGENTE2024'; // Token para registro de agentes

  useEffect(() => {
    // Verificar token en URL
    const token = searchParams.get('token');
    if (token === TOKEN_ADMIN) {
      setTokenValido(true);
    } else {
      setError('Token de registro inválido. Contacta al administrador.');
    }
  }, [searchParams]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validaciones
    if (formData.password !== formData.confirmarPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (formData.password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    setLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Registrar agente
      const response = await axios.post(`${apiUrl}/api/agentes/registro`, {
        nombre: formData.nombre,
        email: formData.email,
        telefono: formData.telefono,
        password: formData.password
      });

      // Login automático
      const loginResponse = await axios.post(`${apiUrl}/api/agentes/login`, {
        email: formData.email,
        password: formData.password
      });

      // Guardar token y datos
      localStorage.setItem('token', loginResponse.data.access_token);
      localStorage.setItem('agente_id', loginResponse.data.agente.id);
      localStorage.setItem('agente_nombre', loginResponse.data.agente.nombre);
      localStorage.setItem('tipo_usuario', 'agente');

      // Mostrar mensaje de éxito
      alert(`✅ ¡Bienvenido ${formData.nombre}!\n\nTu código de referido es: ${response.data.codigo_referido}\n\nGanarás 10% de comisión por cada estudiante que refieras.`);

      // Redirigir al dashboard de agente
      navigate(`/dashboard-agente/${loginResponse.data.agente.id}`);

    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Error al registrar agente');
    } finally {
      setLoading(false);
    }
  };

  if (!tokenValido && error) {
    return (
      <div className="registro-container">
        <div className="registro-card">
          <div className="alert alert-error">
            <h2>⚠️ Acceso Denegado</h2>
            <p>{error}</p>
            <button onClick={() => navigate('/')} className="btn-primary">
              ← Volver al inicio
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="registro-container">
      <div className="registro-card">
        <div className="registro-header">
          <h1>🎯 Registro de Agente</h1>
          <p>Únete como agente afiliado y gana <strong>10% de comisión</strong></p>
        </div>

        {error && (
          <div className="alert alert-error">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="registro-form">
          <div className="form-group">
            <label>Nombre Completo *</label>
            <input
              type="text"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              required
              placeholder="Tu nombre completo"
            />
          </div>

          <div className="form-group">
            <label>Email *</label>
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
            <label>Teléfono</label>
            <input
              type="tel"
              name="telefono"
              value={formData.telefono}
              onChange={handleChange}
              placeholder="+34 123 456 789"
            />
          </div>

          <div className="form-group">
            <label>Contraseña *</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Mínimo 6 caracteres"
            />
          </div>

          <div className="form-group">
            <label>Confirmar Contraseña *</label>
            <input
              type="password"
              name="confirmarPassword"
              value={formData.confirmarPassword}
              onChange={handleChange}
              required
              placeholder="Repite tu contraseña"
            />
          </div>

          <div className="info-box">
            <h3>💰 Beneficios como Agente:</h3>
            <ul>
              <li>✅ Gana 10% de comisión por cada estudiante referido</li>
              <li>✅ Panel exclusivo para gestionar tus referidos</li>
              <li>✅ Código de referido único personalizado</li>
              <li>✅ Seguimiento en tiempo real de comisiones</li>
            </ul>
          </div>

          <button 
            type="submit" 
            className="btn-registro"
            disabled={loading}
          >
            {loading ? '⏳ Registrando...' : '🚀 Crear Cuenta de Agente'}
          </button>
        </form>

        <div className="registro-footer">
          <p>¿Ya tienes cuenta? <a href="/agente/login">Inicia sesión aquí</a></p>
        </div>
      </div>
    </div>
  );
};

export default RegistroAgente;
