import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LoginEstudiante.css';

const LoginEstudiante = () => {
  const [codigoAcceso, setCodigoAcceso] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Verificar que el código existe y obtener ID del estudiante
      const response = await axios.get(`${apiUrl}/api/estudiantes/codigo/${codigoAcceso}`);
      
      if (response.data && response.data.id) {
        // Código válido, redirigir al dashboard
        navigate(`/dashboard-usuario/${response.data.id}`);
      }
    } catch (err) {
      if (err.response?.status === 404) {
        setError('Código de acceso inválido. Por favor verifica tu código.');
      } else {
        setError('Error al verificar el código. Por favor intenta de nuevo.');
      }
      setLoading(false);
    }
  };

  return (
    <div className="login-estudiante-container">
      <div className="login-estudiante-card">
        <div className="login-header">
          <h1>🎓 Acceso Estudiantes</h1>
          <p>Ingresa tu código de acceso para ver tu panel</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="codigoAcceso">
              <strong>Código de Acceso</strong>
            </label>
            <input
              type="text"
              id="codigoAcceso"
              className="form-control"
              placeholder="Ej: X7K9M2P4"
              value={codigoAcceso}
              onChange={(e) => setCodigoAcceso(e.target.value.toUpperCase())}
              required
              maxLength="10"
              disabled={loading}
              style={{ 
                textTransform: 'uppercase', 
                letterSpacing: '2px',
                fontSize: '18px',
                textAlign: 'center',
                fontWeight: 'bold'
              }}
            />
            <small className="form-text">
              💡 Tu código fue enviado a tu email al registrarte
            </small>
          </div>

          {error && (
            <div className="alert alert-error">
              ⚠️ {error}
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary btn-block"
            disabled={loading || !codigoAcceso || codigoAcceso.length < 6}
          >
            {loading ? '🔄 Verificando...' : '🚀 Acceder a Mi Panel'}
          </button>
        </form>

        <div className="login-footer">
          <p>¿No tienes una cuenta?</p>
          <button 
            className="btn btn-secondary"
            onClick={() => navigate('/registro')}
          >
            📝 Registrarse como Estudiante
          </button>
          
          <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #e2e8f0' }}>
            <p style={{ fontSize: '14px', color: '#64748b' }}>
              ¿Olvidaste tu código? Revisa el email que recibiste al registrarte
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginEstudiante;
