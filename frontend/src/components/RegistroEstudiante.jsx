import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './RegistroEstudiante.css';

const RegistroEstudiante = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    consentimiento_gdpr: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [estudianteId, setEstudianteId] = useState(null);
  const [codigoAcceso, setCodigoAcceso] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validar consentimiento GDPR
    if (!formData.consentimiento_gdpr) {
      setError('Debes aceptar la política de privacidad y el tratamiento de datos');
      setLoading(false);
      return;
    }

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      const response = await axios.post(`${apiUrl}/api/estudiantes`, formData);
      
      console.log('Respuesta del servidor:', response.data);
      const id = response.data.estudiante_id || response.data.id;
      const codigo = response.data.codigo_acceso;
      console.log('ID extraído:', id);
      console.log('Código de acceso:', codigo);
      
      setEstudianteId(id);
      setCodigoAcceso(codigo);
      setSuccess(true);
    } catch (err) {
      console.error('Error al registrar:', err);
      setError(err.response?.data?.detail || 'Error al registrar estudiante');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    console.log('Mostrando pantalla de éxito, ID:', estudianteId);
    return (
      <div className="registro-success">
        <div className="success-card">
          <div className="success-icon">✓</div>
          <h2>¡Registro Exitoso!</h2>
          <p>Tu solicitud ha sido recibida.</p>
          
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            borderRadius: '15px',
            padding: '30px',
            margin: '20px 0',
            textAlign: 'center',
            color: 'white',
            boxShadow: '0 10px 30px rgba(102, 126, 234, 0.3)'
          }}>
            <p style={{ fontSize: '16px', marginBottom: '10px', opacity: 0.9 }}>
              <strong>🔐 Tu Código de Acceso Seguro</strong>
            </p>
            <div style={{
              background: 'white',
              borderRadius: '10px',
              padding: '20px',
              margin: '15px 0'
            }}>
              <p style={{
                fontSize: '42px',
                fontWeight: 'bold',
                color: '#667eea',
                margin: '0',
                letterSpacing: '4px'
              }}>
                {codigoAcceso || 'Cargando...'}
              </p>
            </div>
            <p style={{ fontSize: '13px', marginTop: '10px', opacity: 0.9 }}>
              ⚠️ Guarda este código para acceder a tu panel
            </p>
            <p style={{ fontSize: '12px', marginTop: '5px', opacity: 0.8 }}>
              ID de referencia: #{estudianteId}
            </p>
            <p style={{ fontSize: '12px', marginTop: '10px', opacity: 0.9 }}>
              📧 También lo recibirás por email
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '20px', flexWrap: 'wrap' }}>
            <button 
              onClick={() => navigate(`/dashboard-usuario/${estudianteId}`)}
              style={{
                padding: '12px 30px',
                background: '#38b2ac',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              🏠 Mi Panel
            </button>
            <button 
              onClick={() => navigate('/portal')}
              style={{
                padding: '12px 30px',
                background: '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              Consultar Estado
            </button>
            <button 
              onClick={() => navigate('/')}
              style={{
                padding: '12px 30px',
                background: '#e2e8f0',
                color: '#2d3748',
                border: 'none',
                borderRadius: '5px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              Volver al Inicio
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
          <h1>Registro Rápido</h1>
          <p>Completa estos 3 campos básicos para comenzar</p>
          <p style={{fontSize: '13px', color: '#718096', marginTop: '10px'}}>
            ℹ️ Podrás completar tu perfil después con más detalles
          </p>
        </div>

        <form onSubmit={handleSubmit} className="registro-form">
          <div className="form-section">
            <h3>Datos Básicos</h3>
            
            <div className="form-group">
              <label htmlFor="nombre">Nombre Completo *</label>
              <input
                type="text"
                id="nombre"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
                placeholder="Ej: Juan Pérez García"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="tu@email.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="telefono">Teléfono *</label>
              <input
                type="tel"
                id="telefono"
                name="telefono"
                value={formData.telefono}
                onChange={handleChange}
                required
                placeholder="+34 600 000 000"
              />
            </div>
          </div>

          <div className="form-section">
            <div className="form-group" style={{marginBottom: '0'}}>
              <label style={{display: 'flex', alignItems: 'flex-start', cursor: 'pointer'}}>
                <input
                  type="checkbox"
                  name="consentimiento_gdpr"
                  checked={formData.consentimiento_gdpr}
                  onChange={handleChange}
                  required
                  style={{marginRight: '10px', marginTop: '3px'}}
                />
                <span style={{fontSize: '14px', lineHeight: '1.5'}}>
                  He leído y acepto la{' '}
                  <a href="/politica-privacidad" target="_blank" style={{color: '#667eea', textDecoration: 'underline'}}>
                    Política de Privacidad
                  </a>{' '}
                  y doy mi consentimiento para el tratamiento de mis datos personales conforme al RGPD *
                </span>
              </label>
            </div>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠</span>
              {error}
            </div>
          )}

          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading ? 'Creando cuenta...' : '🚀 Crear Cuenta'}
          </button>

          <p className="form-footer">
            ¿Ya tienes cuenta? <a href="/portal">Consulta tu estado aquí</a>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegistroEstudiante;
