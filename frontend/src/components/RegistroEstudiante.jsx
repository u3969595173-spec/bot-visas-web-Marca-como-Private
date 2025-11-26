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
    pasaporte: '',
    edad: '',
    nacionalidad: '',
    ciudad_origen: '',
    especialidad: '',
    nivel_espanol: 'basico',
    tipo_visa: 'estudiante'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [estudianteId, setEstudianteId] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/api/estudiantes`, formData);
      
      console.log('Respuesta del servidor:', response.data);
      const id = response.data.estudiante_id || response.data.id;
      console.log('ID extraído:', id);
      
      setEstudianteId(id);
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
            background: '#e6fffa',
            border: '2px solid #38b2ac',
            borderRadius: '10px',
            padding: '20px',
            margin: '20px 0',
            textAlign: 'center'
          }}>
            <p style={{ fontSize: '14px', color: '#2c7a7b', marginBottom: '10px' }}>
              <strong>Tu ID de Seguimiento:</strong>
            </p>
            <p style={{
              fontSize: '48px',
              fontWeight: 'bold',
              color: '#2c7a7b',
              margin: '10px 0'
            }}>
              {estudianteId || 'Cargando...'}
            </p>
            <p style={{ fontSize: '14px', color: '#2c7a7b', marginTop: '10px' }}>
              ⚠️ Guarda este número para consultar tu estado
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
          <h1>Solicitud de Visa de Estudio</h1>
          <p>Completa el formulario para comenzar tu proceso</p>
        </div>

        <form onSubmit={handleSubmit} className="registro-form">
          <div className="form-section">
            <h3>Datos Personales</h3>
            
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

            <div className="form-row">
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

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="pasaporte">Número de Pasaporte *</label>
                <input
                  type="text"
                  id="pasaporte"
                  name="pasaporte"
                  value={formData.pasaporte}
                  onChange={handleChange}
                  required
                  placeholder="ABC123456"
                />
              </div>

              <div className="form-group">
                <label htmlFor="edad">Edad *</label>
                <input
                  type="number"
                  id="edad"
                  name="edad"
                  value={formData.edad}
                  onChange={handleChange}
                  required
                  min="18"
                  max="99"
                  placeholder="25"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="nacionalidad">Nacionalidad *</label>
                <input
                  type="text"
                  id="nacionalidad"
                  name="nacionalidad"
                  value={formData.nacionalidad}
                  onChange={handleChange}
                  required
                  placeholder="Ej: Mexicana"
                />
              </div>

              <div className="form-group">
                <label htmlFor="ciudad_origen">Ciudad de Origen *</label>
                <input
                  type="text"
                  id="ciudad_origen"
                  name="ciudad_origen"
                  value={formData.ciudad_origen}
                  onChange={handleChange}
                  required
                  placeholder="Ej: Ciudad de México"
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Información Académica</h3>

            <div className="form-group">
              <label htmlFor="especialidad">Especialidad de Interés *</label>
              <input
                type="text"
                id="especialidad"
                name="especialidad"
                value={formData.especialidad}
                onChange={handleChange}
                required
                placeholder="Ej: Ingeniería Informática, Medicina, Derecho..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="nivel_espanol">Nivel de Español *</label>
                <select
                  id="nivel_espanol"
                  name="nivel_espanol"
                  value={formData.nivel_espanol}
                  onChange={handleChange}
                  required
                >
                  <option value="basico">Básico (A1-A2)</option>
                  <option value="intermedio">Intermedio (B1-B2)</option>
                  <option value="avanzado">Avanzado (C1-C2)</option>
                  <option value="nativo">Nativo</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="tipo_visa">Tipo de Visa *</label>
                <select
                  id="tipo_visa"
                  name="tipo_visa"
                  value={formData.tipo_visa}
                  onChange={handleChange}
                  required
                >
                  <option value="estudiante">Estudiante (Grado/Máster)</option>
                  <option value="idiomas">Curso de Idiomas</option>
                  <option value="doctorado">Doctorado/Investigación</option>
                </select>
              </div>
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
            {loading ? 'Enviando...' : 'Enviar Solicitud'}
          </button>

          <p className="form-footer">
            ¿Ya tienes cuenta? <a href="/login-estudiante">Inicia sesión aquí</a>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegistroEstudiante;
