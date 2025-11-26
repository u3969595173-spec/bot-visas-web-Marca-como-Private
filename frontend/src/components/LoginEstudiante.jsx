import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LoginEstudiante.css';

const LoginEstudiante = () => {
  const [estudianteId, setEstudianteId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Verificar que el estudiante existe
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}`);
      
      if (response.data && response.data.id) {
        // Estudiante existe, redirigir al dashboard
        navigate(`/dashboard-usuario/${estudianteId}`);
      }
    } catch (err) {
      if (err.response?.status === 404) {
        setError('No se encontró ningún estudiante con ese ID');
      } else {
        setError('Error al verificar el ID. Por favor intenta de nuevo.');
      }
      setLoading(false);
    }
  };

  return (
    <div className="login-estudiante-container">
      <div className="login-estudiante-card">
        <div className="login-header">
          <h1>🎓 Acceso Estudiantes</h1>
          <p>Ingresa tu ID de estudiante para acceder a tu panel</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="estudianteId">
              <strong>ID de Estudiante</strong>
            </label>
            <input
              type="number"
              id="estudianteId"
              className="form-control"
              placeholder="Ej: 1, 2, 3..."
              value={estudianteId}
              onChange={(e) => setEstudianteId(e.target.value)}
              required
              min="1"
              disabled={loading}
            />
            <small className="form-text">
              💡 Tu ID fue enviado a tu email al registrarte
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
            disabled={loading || !estudianteId}
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
              ¿Olvidaste tu ID? Revisa el email que recibiste al registrarte
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginEstudiante;
