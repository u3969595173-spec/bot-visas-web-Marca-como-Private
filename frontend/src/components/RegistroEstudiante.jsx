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
    fecha_nacimiento: '',
    edad: '',
    nacionalidad: '',
    pais_origen: '',
    ciudad_origen: '',
    carrera_deseada: '',
    especialidad: '',
    nivel_espanol: 'basico',
    tipo_visa: 'estudiante',
    fondos_disponibles: '',
    fecha_inicio_estimada: '',
    consentimiento_gdpr: false
  });
  const [archivos, setArchivos] = useState({
    titulo: null,
    pasaporte_archivo: null,
    extractos: null
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

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    if (files && files[0]) {
      setArchivos(prev => ({
        ...prev,
        [name]: files[0]
      }));
    }
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
      
      // Crear FormData para enviar archivos
      const formDataToSend = new FormData();
      
      // Agregar todos los campos del formulario
      Object.keys(formData).forEach(key => {
        if (key !== 'consentimiento_gdpr') {
          formDataToSend.append(key, formData[key]);
        }
      });
      formDataToSend.append('consentimiento_gdpr', formData.consentimiento_gdpr ? 'true' : 'false');
      
      // Agregar archivos si existen
      if (archivos.titulo) {
        formDataToSend.append('archivo_titulo', archivos.titulo);
      }
      if (archivos.pasaporte_archivo) {
        formDataToSend.append('archivo_pasaporte', archivos.pasaporte_archivo);
      }
      if (archivos.extractos) {
        formDataToSend.append('archivo_extractos', archivos.extractos);
      }

      const response = await axios.post(`${apiUrl}/api/estudiantes`, formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
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
                <label htmlFor="fecha_nacimiento">Fecha de Nacimiento *</label>
                <input
                  type="date"
                  id="fecha_nacimiento"
                  name="fecha_nacimiento"
                  value={formData.fecha_nacimiento}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="form-row">
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

              <div className="form-group">
                <label htmlFor="pais_origen">País de Origen *</label>
                <input
                  type="text"
                  id="pais_origen"
                  name="pais_origen"
                  value={formData.pais_origen}
                  onChange={handleChange}
                  required
                  placeholder="Ej: México"
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
              <label htmlFor="carrera_deseada">Carrera Deseada *</label>
                <input
                type="text"
                id="carrera_deseada"
                name="carrera_deseada"
                value={formData.carrera_deseada}
                onChange={handleChange}
                required
                placeholder="Ej: Licenciatura en Ingeniería, Máster en Derecho..."
              />
            </div>

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

          <div className="form-section">
            <h3>Información Financiera</h3>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="fondos_disponibles">Fondos Disponibles (€) *</label>
                <input
                  type="number"
                  id="fondos_disponibles"
                  name="fondos_disponibles"
                  value={formData.fondos_disponibles}
                  onChange={handleChange}
                  required
                  min="0"
                  step="0.01"
                  placeholder="10000"
                />
                <small style={{color: '#718096', fontSize: '12px'}}>
                  Mínimo recomendado: €10,000 para visa de estudiante
                </small>
              </div>

              <div className="form-group">
                <label htmlFor="fecha_inicio_estimada">Fecha Estimada de Inicio *</label>
                <input
                  type="date"
                  id="fecha_inicio_estimada"
                  name="fecha_inicio_estimada"
                  value={formData.fecha_inicio_estimada}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Documentos</h3>
            <p style={{color: '#718096', fontSize: '14px', marginBottom: '15px'}}>
              Sube los siguientes documentos en formato PDF o JPG (máx. 5MB cada uno)
            </p>

            <div className="form-group">
              <label htmlFor="titulo">Título Académico *</label>
              <input
                type="file"
                id="titulo"
                name="titulo"
                onChange={handleFileChange}
                accept=".pdf,.jpg,.jpeg,.png"
                required
              />
              {archivos.titulo && (
                <small style={{color: '#38b2ac'}}>✓ {archivos.titulo.name}</small>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="pasaporte_archivo">Copia del Pasaporte *</label>
              <input
                type="file"
                id="pasaporte_archivo"
                name="pasaporte_archivo"
                onChange={handleFileChange}
                accept=".pdf,.jpg,.jpeg,.png"
                required
              />
              {archivos.pasaporte_archivo && (
                <small style={{color: '#38b2ac'}}>✓ {archivos.pasaporte_archivo.name}</small>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="extractos">Extractos Bancarios *</label>
              <input
                type="file"
                id="extractos"
                name="extractos"
                onChange={handleFileChange}
                accept=".pdf,.jpg,.jpeg,.png"
                required
              />
              {archivos.extractos && (
                <small style={{color: '#38b2ac'}}>✓ {archivos.extractos.name}</small>
              )}
              <small style={{color: '#718096', fontSize: '12px', display: 'block', marginTop: '5px'}}>
                Últimos 3 meses mostrando saldo suficiente
              </small>
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
