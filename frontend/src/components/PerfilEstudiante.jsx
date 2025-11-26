import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PerfilEstudiante.css';

const PerfilEstudiante = ({ estudianteId }) => {
  const [estudiante, setEstudiante] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    cargarDatos();
  }, [estudianteId]);

  const cargarDatos = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const token = localStorage.getItem('token');
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      setEstudiante(response.data);
      setFormData(response.data);
      setLoading(false);
    } catch (err) {
      setError('Error al cargar datos del estudiante');
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const token = localStorage.getItem('token');
      await axios.put(`${apiUrl}/api/estudiantes/${estudianteId}`, formData, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      
      setSuccess('Datos actualizados correctamente');
      setEstudiante(formData);
      setEditing(false);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al actualizar datos');
    }
  };

  const getEstadoBadgeClass = (estado) => {
    const classes = {
      'pendiente': 'badge-pendiente',
      'aprobado': 'badge-aprobado',
      'rechazado': 'badge-rechazado',
      'en_revision': 'badge-revision'
    };
    return classes[estado] || 'badge-pendiente';
  };

  if (loading) {
    return (
      <div className="perfil-loading">
        <div className="spinner"></div>
        <p>Cargando datos...</p>
      </div>
    );
  }

  if (!estudiante) {
    return (
      <div className="perfil-error">
        <p>No se encontró el estudiante</p>
      </div>
    );
  }

  return (
    <div className="perfil-container">
      <div className="perfil-header">
        <div className="perfil-header-content">
          <div className="perfil-avatar">
            {estudiante.nombre?.charAt(0) || 'E'}
          </div>
          <div className="perfil-header-info">
            <h1>{estudiante.nombre || 'Estudiante'}</h1>
            <p className="perfil-email">{estudiante.email}</p>
            <span className={`perfil-badge ${getEstadoBadgeClass(estudiante.estado)}`}>
              {estudiante.estado?.toUpperCase() || 'PENDIENTE'}
            </span>
          </div>
        </div>
        {!editing && (
          <div className="perfil-header-actions">
            <button className="btn-edit" onClick={() => setEditing(true)}>
              ✏️ Editar Perfil
            </button>
            <a 
              href={`${apiUrl}/api/estudiantes/${estudianteId}/reporte-pdf?tipo=completo`}
              download
              className="btn-download-profile"
            >
              📄 Descargar PDF
            </a>
          </div>
        )}
      </div>

      {success && (
        <div className="alert alert-success">
          ✓ {success}
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          ⚠ {error}
        </div>
      )}

      {editing ? (
        <form onSubmit={handleSubmit} className="perfil-form">
          <div className="form-card">
            <h2>Datos Personales</h2>
            
            <div className="form-grid">
              <div className="form-group">
                <label>Nombre Completo</label>
                <input
                  type="text"
                  name="nombre"
                  value={formData.nombre || ''}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email || ''}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Teléfono</label>
                <input
                  type="tel"
                  name="telefono"
                  value={formData.telefono || ''}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Pasaporte</label>
                <input
                  type="text"
                  name="pasaporte"
                  value={formData.pasaporte || ''}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Edad</label>
                <input
                  type="number"
                  name="edad"
                  value={formData.edad || ''}
                  onChange={handleChange}
                  min="18"
                  max="99"
                />
              </div>

              <div className="form-group">
                <label>Nacionalidad</label>
                <input
                  type="text"
                  name="nacionalidad"
                  value={formData.nacionalidad || ''}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Ciudad de Origen</label>
                <input
                  type="text"
                  name="ciudad_origen"
                  value={formData.ciudad_origen || ''}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Especialidad</label>
                <input
                  type="text"
                  name="especialidad"
                  value={formData.especialidad || ''}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Nivel de Español</label>
                <select
                  name="nivel_espanol"
                  value={formData.nivel_espanol || 'basico'}
                  onChange={handleChange}
                >
                  <option value="basico">Básico (A1-A2)</option>
                  <option value="intermedio">Intermedio (B1-B2)</option>
                  <option value="avanzado">Avanzado (C1-C2)</option>
                  <option value="nativo">Nativo</option>
                </select>
              </div>

              <div className="form-group">
                <label>Tipo de Visa</label>
                <select
                  name="tipo_visa"
                  value={formData.tipo_visa || 'estudiante'}
                  onChange={handleChange}
                >
                  <option value="estudiante">Estudiante (Grado/Máster)</option>
                  <option value="idiomas">Curso de Idiomas</option>
                  <option value="doctorado">Doctorado/Investigación</option>
                </select>
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-save">
                💾 Guardar Cambios
              </button>
              <button 
                type="button" 
                className="btn-cancel"
                onClick={() => {
                  setEditing(false);
                  setFormData(estudiante);
                  setError('');
                }}
              >
                ✕ Cancelar
              </button>
            </div>
          </div>
        </form>
      ) : (
        <div className="perfil-view">
          <div className="info-card">
            <h2>Datos Personales</h2>
            <div className="info-grid">
              <div className="info-item">
                <label>Nombre Completo</label>
                <p>{estudiante.nombre || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Email</label>
                <p>{estudiante.email || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Teléfono</label>
                <p>{estudiante.telefono || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Pasaporte</label>
                <p>{estudiante.pasaporte || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Edad</label>
                <p>{estudiante.edad || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Nacionalidad</label>
                <p>{estudiante.nacionalidad || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Ciudad de Origen</label>
                <p>{estudiante.ciudad_origen || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Especialidad</label>
                <p>{estudiante.especialidad || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Nivel de Español</label>
                <p>{estudiante.nivel_espanol || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Tipo de Visa</label>
                <p>{estudiante.tipo_visa || 'No especificado'}</p>
              </div>
            </div>
          </div>

          <div className="info-card">
            <h2>Estado del Proceso</h2>
            <div className="info-grid">
              <div className="info-item">
                <label>Estado</label>
                <p>
                  <span className={`perfil-badge ${getEstadoBadgeClass(estudiante.estado)}`}>
                    {estudiante.estado?.toUpperCase() || 'PENDIENTE'}
                  </span>
                </p>
              </div>
              <div className="info-item">
                <label>Documentos</label>
                <p>{estudiante.documentos_estado || 'Pendiente'}</p>
              </div>
              <div className="info-item">
                <label>Fecha de Registro</label>
                <p>{estudiante.created_at ? new Date(estudiante.created_at).toLocaleDateString() : 'No disponible'}</p>
              </div>
              {estudiante.notas && (
                <div className="info-item full-width">
                  <label>Notas</label>
                  <p className="notas">{estudiante.notas}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PerfilEstudiante;
