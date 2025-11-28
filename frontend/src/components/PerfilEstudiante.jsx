import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PerfilEstudiante.css';

const PerfilEstudiante = ({ estudianteId }) => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const [estudiante, setEstudiante] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [documentosGenerados, setDocumentosGenerados] = useState(null);
  const [generandoDocs, setGenerandoDocs] = useState(false);
  const [documentosOficiales, setDocumentosOficiales] = useState([]);
  const [cargandoDocumentosOficiales, setCargandoDocumentosOficiales] = useState(false);
  const [mensajes, setMensajes] = useState([]);
  const [cargandoMensajes, setCargandoMensajes] = useState(false);
  const [mostrarMensajes, setMostrarMensajes] = useState(false);
  const [mensajeRespuesta, setMensajeRespuesta] = useState('');
  const [enviandoRespuesta, setEnviandoRespuesta] = useState(false);

  useEffect(() => {
    cargarDatos();
    cargarDocumentosOficiales();
    cargarMensajes();
  }, [estudianteId]);

  const cargarDatos = async () => {
    try {
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

  const cargarDocumentosOficiales = async () => {
    setCargandoDocumentosOficiales(true);
    try {
      // Obtener código de acceso del localStorage (primero sin ID, luego con ID)
      let codigoAcceso = localStorage.getItem('codigo_acceso') || 
                         localStorage.getItem(`codigo_acceso_${estudianteId}`);
      
      if (!codigoAcceso) {
        codigoAcceso = prompt('Ingresa tu código de acceso:');
        if (!codigoAcceso) {
          setCargandoDocumentosOficiales(false);
          return;
        }
      }

      // Guardar código para futuras consultas
      localStorage.setItem(`codigo_acceso_${estudianteId}`, codigoAcceso);

      const response = await axios.get(
        `${apiUrl}/api/estudiantes/${estudianteId}/documentos-generados?codigo_acceso=${codigoAcceso}`
      );
      
      // Filtrar solo documentos aprobados y enviados
      const docsAprobados = response.data.documentos.filter(
        doc => doc.estado === 'aprobado' && doc.enviado_estudiante
      );
      
      setDocumentosOficiales(docsAprobados);
    } catch (err) {
      if (err.response?.status === 403) {
        localStorage.removeItem(`codigo_acceso_${estudianteId}`);
        setError('Código de acceso inválido');
      } else if (err.response?.status !== 404) {
        console.error('Error al cargar documentos oficiales:', err);
      }
    } finally {
      setCargandoDocumentosOficiales(false);
    }
  };

  const generarDocumentos = async () => {
    setGenerandoDocs(true);
    setError('');
    try {
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/generar-documentos`);
      setDocumentosGenerados(response.data.documentos);
      setSuccess('✅ Documentos generados exitosamente');
    } catch (err) {
      setError('Error al generar documentos');
    } finally {
      setGenerandoDocs(false);
    }
  };

  const descargarDocumento = (contenido, nombreArchivo) => {
    const blob = new Blob([contenido], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = nombreArchivo;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const descargarPDFOficial = (contenidoBase64, nombreArchivo) => {
    try {
      // Decodificar base64 y crear blob PDF
      const byteCharacters = atob(contenidoBase64);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'application/pdf' });
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = nombreArchivo;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      
      setSuccess('✅ Documento descargado correctamente');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Error al descargar el documento');
      console.error('Error:', err);
    }
  };

  const abrirPDFOficial = (contenidoBase64, nombreArchivo) => {
    try {
      // Decodificar base64 y abrir en nueva ventana
      const byteCharacters = atob(contenidoBase64);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'application/pdf' });
      
      const url = window.URL.createObjectURL(blob);
      window.open(url, '_blank');
      
      // Limpiar URL después de un tiempo
      setTimeout(() => window.URL.revokeObjectURL(url), 60000);
    } catch (err) {
      setError('Error al abrir el documento');
      console.error('Error:', err);
    }
  };

  const cargarMensajes = async () => {
    setCargandoMensajes(true);
    try {
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/mensajes`);
      setMensajes(response.data.mensajes || []);
    } catch (err) {
      console.error('Error cargando mensajes:', err);
    } finally {
      setCargandoMensajes(false);
    }
  };

  const enviarRespuesta = async () => {
    if (!mensajeRespuesta.trim()) {
      setError('El mensaje no puede estar vacío');
      return;
    }

    setEnviandoRespuesta(true);
    try {
      await axios.post(`${apiUrl}/api/estudiantes/${estudianteId}/mensajes`, {
        remitente: 'estudiante',
        mensaje: mensajeRespuesta
      });
      
      setSuccess('✅ Respuesta enviada correctamente');
      setMensajeRespuesta('');
      cargarMensajes();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Error al enviar respuesta: ' + (err.response?.data?.detail || err.message));
    } finally {
      setEnviandoRespuesta(false);
    }
  };

  const marcarComoLeido = async (mensajeId) => {
    try {
      await axios.put(`${apiUrl}/api/mensajes/${mensajeId}/marcar-leido`);
      cargarMensajes();
    } catch (err) {
      console.error('Error marcando mensaje como leído:', err);
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
                <label>Fecha de Nacimiento</label>
                <input
                  type="date"
                  name="fecha_nacimiento"
                  value={formData.fecha_nacimiento || ''}
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
                <label>País de Origen</label>
                <input
                  type="text"
                  name="pais_origen"
                  value={formData.pais_origen || ''}
                  onChange={handleChange}
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
                <label>Carrera Deseada</label>
                <input
                  type="text"
                  name="carrera_deseada"
                  value={formData.carrera_deseada || ''}
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
                <label>Fondos Disponibles (€)</label>
                <input
                  type="number"
                  name="fondos_disponibles"
                  value={formData.fondos_disponibles || ''}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                />
              </div>

              <div className="form-group">
                <label>Fecha Estimada de Inicio</label>
                <input
                  type="date"
                  name="fecha_inicio_estimada"
                  value={formData.fecha_inicio_estimada || ''}
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
                <label>Fecha de Nacimiento</label>
                <p>{estudiante.fecha_nacimiento ? new Date(estudiante.fecha_nacimiento).toLocaleDateString() : 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Edad</label>
                <p>{estudiante.edad || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>País de Origen</label>
                <p>{estudiante.pais_origen || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Nacionalidad</label>
                <p>{estudiante.nacionalidad || 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Ciudad de Origen</label>
                <p>{estudiante.ciudad_origen || 'No especificado'}</p>
              </div>
            </div>
          </div>

          <div className="info-card">
            <h2>Información Académica</h2>
            <div className="info-grid">
              <div className="info-item">
                <label>Carrera Deseada</label>
                <p>{estudiante.carrera_deseada || 'No especificado'}</p>
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
            <h2>Información Financiera</h2>
            <div className="info-grid">
              <div className="info-item">
                <label>Fondos Disponibles</label>
                <p>{estudiante.fondos_disponibles ? `€${Number(estudiante.fondos_disponibles).toLocaleString('es-ES', {minimumFractionDigits: 2})}` : 'No especificado'}</p>
              </div>
              <div className="info-item">
                <label>Fecha Estimada de Inicio</label>
                <p>{estudiante.fecha_inicio_estimada ? new Date(estudiante.fecha_inicio_estimada).toLocaleDateString() : 'No especificado'}</p>
              </div>
            </div>
          </div>

          <div className="info-card">
            <h2>Documentos Subidos</h2>
            <div className="info-grid">
              <div className="info-item">
                <label>📄 Título Académico</label>
                <p>{estudiante.archivo_titulo ? '✅ Subido' : '❌ Pendiente'}</p>
              </div>
              <div className="info-item">
                <label>🛂 Pasaporte</label>
                <p>{estudiante.archivo_pasaporte ? '✅ Subido' : '❌ Pendiente'}</p>
              </div>
              <div className="info-item">
                <label>💰 Extractos Bancarios</label>
                <p>{estudiante.archivo_extractos ? '✅ Subido' : '❌ Pendiente'}</p>
              </div>
              <div className="info-item">
                <label>📋 Consentimiento GDPR</label>
                <p>{estudiante.consentimiento_gdpr ? `✅ Aceptado el ${estudiante.fecha_consentimiento ? new Date(estudiante.fecha_consentimiento).toLocaleDateString() : ''}` : '❌ No aceptado'}</p>
              </div>
            </div>
          </div>

          {/* NUEVA CARD: Probabilidad de Éxito */}
          {estudiante.probabilidad_exito && (
            <div className="info-card">
              <h2>📊 Probabilidad de Éxito</h2>
              <div style={{padding: '15px'}}>
                <div style={{marginBottom: '20px'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '10px'}}>
                    <span style={{fontWeight: 'bold', fontSize: '1.2rem'}}>{estudiante.probabilidad_exito.probabilidad}%</span>
                    <span style={{fontWeight: 'bold', color: estudiante.probabilidad_exito.color === 'success' ? '#28a745' : estudiante.probabilidad_exito.color === 'info' ? '#17a2b8' : estudiante.probabilidad_exito.color === 'warning' ? '#ffc107' : '#dc3545'}}>
                      {estudiante.probabilidad_exito.categoria}
                    </span>
                  </div>
                  <div style={{width: '100%', backgroundColor: '#e9ecef', borderRadius: '10px', height: '25px', overflow: 'hidden'}}>
                    <div style={{
                      width: `${estudiante.probabilidad_exito.probabilidad}%`,
                      backgroundColor: estudiante.probabilidad_exito.color === 'success' ? '#28a745' : estudiante.probabilidad_exito.color === 'info' ? '#17a2b8' : estudiante.probabilidad_exito.color === 'warning' ? '#ffc107' : '#dc3545',
                      height: '100%',
                      transition: 'width 0.5s ease',
                      borderRadius: '10px'
                    }}></div>
                  </div>
                  <p style={{marginTop: '10px', fontSize: '0.95rem', color: '#6c757d'}}>{estudiante.probabilidad_exito.mensaje}</p>
                </div>
                <div>
                  <h4 style={{marginBottom: '10px', fontSize: '1rem'}}>Factores Evaluados:</h4>
                  {estudiante.probabilidad_exito.factores.map((factor, index) => (
                    <div key={index} style={{display: 'flex', justifyContent: 'space-between', padding: '8px', borderBottom: '1px solid #e9ecef'}}>
                      <span style={{fontSize: '0.9rem'}}>
                        {factor.cumple ? '✅' : '❌'} {factor.factor}
                      </span>
                      <span style={{fontWeight: 'bold', fontSize: '0.9rem'}}>{factor.puntos} pts</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* NUEVA CARD: Cursos Sugeridos */}
          {estudiante.cursos_sugeridos && estudiante.cursos_sugeridos.length > 0 && (
            <div className="info-card">
              <h2>🎓 Cursos Sugeridos para Ti</h2>
              <div style={{padding: '10px'}}>
                {estudiante.cursos_sugeridos.map((curso, index) => (
                  <div key={index} style={{
                    border: '1px solid #e9ecef',
                    borderRadius: '8px',
                    padding: '15px',
                    marginBottom: '15px',
                    backgroundColor: curso.asequible ? '#f8f9fa' : '#fff3cd'
                  }}>
                    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '10px'}}>
                      <h3 style={{margin: 0, fontSize: '1.1rem', color: '#212529'}}>{curso.nombre}</h3>
                      <span style={{
                        backgroundColor: '#007bff',
                        color: 'white',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '0.85rem',
                        fontWeight: 'bold'
                      }}>
                        {curso.match}% match
                      </span>
                    </div>
                    <p style={{margin: '5px 0', fontSize: '0.95rem', color: '#6c757d'}}>
                      <strong>Universidad:</strong> {curso.universidad}
                    </p>
                    <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '0.9rem'}}>
                      <p style={{margin: '5px 0'}}>⏱️ <strong>Duración:</strong> {curso.duracion}</p>
                      <p style={{margin: '5px 0'}}>💶 <strong>Costo:</strong> €{curso.costo_anual.toLocaleString()}/año</p>
                      <p style={{margin: '5px 0'}}>🗣️ <strong>Español:</strong> {curso.nivel_espanol_requerido}</p>
                      <p style={{margin: '5px 0'}}>
                        {curso.asequible ? '✅ Asequible' : '⚠️ Revisar fondos'}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* NUEVA CARD: Simulador de Entrevistas */}
          <div className="info-card">
            <h2>🎭 Simulador de Entrevista Consular</h2>
            <div style={{padding: '15px'}}>
              <p style={{marginBottom: '15px', color: '#6c757d'}}>
                Practica con preguntas reales adaptadas a tu perfil. Recibe feedback instantáneo.
              </p>
              <a 
                href="/estudiante/simulador"
                style={{
                  display: 'inline-block',
                  backgroundColor: '#667eea',
                  color: 'white',
                  padding: '12px 24px',
                  border: 'none',
                  borderRadius: '5px',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  textDecoration: 'none',
                  cursor: 'pointer'
                }}
              >
                🚀 Iniciar Simulador
              </a>
            </div>
          </div>

          {/* NUEVA CARD: Calculadora de Fondos */}
          <div className="info-card">
            <h2>💰 Calculadora de Fondos</h2>
            <div style={{padding: '15px'}}>
              <p style={{marginBottom: '15px', color: '#6c757d'}}>
                Calcula cuánto dinero necesitas según tu ciudad, programa y situación familiar.
              </p>
              <a 
                href="/estudiante/calculadora-fondos"
                style={{
                  display: 'inline-block',
                  backgroundColor: '#764ba2',
                  color: 'white',
                  padding: '12px 24px',
                  border: 'none',
                  borderRadius: '5px',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  textDecoration: 'none',
                  cursor: 'pointer'
                }}
              >
                🧮 Calcular Fondos
              </a>
            </div>
          </div>

          {/* NUEVA CARD: Alertas de Fechas */}
          <div className="info-card">
            <h2>📅 Fechas Importantes</h2>
            <div style={{padding: '15px'}}>
              <p style={{marginBottom: '15px', color: '#6c757d'}}>
                Gestiona tus fechas críticas y recibe alertas automáticas por email.
              </p>
              <a 
                href="/estudiante/alertas"
                style={{
                  display: 'inline-block',
                  backgroundColor: '#17a2b8',
                  color: 'white',
                  padding: '12px 24px',
                  border: 'none',
                  borderRadius: '5px',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  textDecoration: 'none',
                  cursor: 'pointer'
                }}
              >
                🔔 Ver Mis Alertas
              </a>
            </div>
          </div>

          {/* NUEVA CARD: Mensajes del Administrador */}
          <div className="info-card" style={{position: 'relative'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
              <h2>💬 Mensajes del Administrador</h2>
              {mensajes.filter(m => m.remitente === 'admin' && !m.leido).length > 0 && (
                <span style={{
                  backgroundColor: '#ef4444',
                  color: 'white',
                  padding: '4px 12px',
                  borderRadius: '12px',
                  fontSize: '0.85rem',
                  fontWeight: 'bold'
                }}>
                  {mensajes.filter(m => m.remitente === 'admin' && !m.leido).length} nuevo(s)
                </span>
              )}
            </div>
            
            {cargandoMensajes ? (
              <div style={{padding: '20px', textAlign: 'center'}}>
                <div className="spinner" style={{margin: '0 auto 10px'}}></div>
                <p style={{color: '#6b7280'}}>Cargando mensajes...</p>
              </div>
            ) : mensajes.length === 0 ? (
              <div style={{padding: '20px', textAlign: 'center', color: '#9ca3af'}}>
                <p>📭 No tienes mensajes del administrador</p>
              </div>
            ) : (
              <div>
                <button
                  onClick={() => setMostrarMensajes(!mostrarMensajes)}
                  style={{
                    width: '100%',
                    padding: '12px',
                    backgroundColor: '#3b82f6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    fontWeight: 'bold',
                    marginBottom: '15px'
                  }}
                >
                  {mostrarMensajes ? '▼ Ocultar Mensajes' : '▶ Ver Mensajes'} ({mensajes.length})
                </button>

                {mostrarMensajes && (
                  <div style={{maxHeight: '600px', overflowY: 'auto'}}>
                    {mensajes.map((mensaje, index) => {
                      const esAdmin = mensaje.remitente === 'admin';
                      const tipoEmoji = {
                        'solicitud_documento': '📄',
                        'recordatorio': '⏰',
                        'informacion': 'ℹ️',
                        'urgente': '🚨'
                      };

                      return (
                        <div
                          key={index}
                          style={{
                            backgroundColor: esAdmin ? '#f0f9ff' : '#f9fafb',
                            border: esAdmin ? '2px solid #3b82f6' : '1px solid #e5e7eb',
                            borderRadius: '8px',
                            padding: '15px',
                            marginBottom: '15px',
                            position: 'relative'
                          }}
                          onClick={() => esAdmin && !mensaje.leido && marcarComoLeido(mensaje.id)}
                        >
                          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '10px'}}>
                            <div>
                              <span style={{
                                fontSize: '1.2rem',
                                marginRight: '8px'
                              }}>
                                {tipoEmoji[mensaje.tipo] || (esAdmin ? '👤' : '💭')}
                              </span>
                              <strong style={{color: esAdmin ? '#1e40af' : '#374151'}}>
                                {esAdmin ? 'Administrador' : 'Tú'}
                              </strong>
                            </div>
                            <div style={{textAlign: 'right'}}>
                              <span style={{fontSize: '0.85rem', color: '#6b7280'}}>
                                {new Date(mensaje.created_at).toLocaleDateString('es-ES')}
                              </span>
                              {esAdmin && !mensaje.leido && (
                                <span style={{
                                  display: 'block',
                                  fontSize: '0.75rem',
                                  color: '#ef4444',
                                  fontWeight: 'bold',
                                  marginTop: '4px'
                                }}>
                                  • NUEVO
                                </span>
                              )}
                            </div>
                          </div>
                          
                          <p style={{
                            margin: '10px 0',
                            color: '#1f2937',
                            whiteSpace: 'pre-line',
                            lineHeight: '1.6'
                          }}>
                            {mensaje.mensaje}
                          </p>

                          {mensaje.tipo === 'solicitud_documento' && (
                            <div style={{
                              backgroundColor: '#fef3c7',
                              padding: '10px',
                              borderRadius: '5px',
                              marginTop: '10px',
                              borderLeft: '4px solid #f59e0b'
                            }}>
                              <p style={{margin: 0, fontSize: '0.9rem', color: '#92400e'}}>
                                <strong>📋 Acción requerida:</strong> Por favor sube el documento solicitado
                              </p>
                            </div>
                          )}
                        </div>
                      );
                    })}

                    {/* Responder */}
                    <div style={{
                      backgroundColor: '#f9fafb',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      padding: '15px',
                      marginTop: '20px'
                    }}>
                      <h4 style={{margin: '0 0 10px 0', color: '#374151'}}>✍️ Enviar Respuesta</h4>
                      <textarea
                        value={mensajeRespuesta}
                        onChange={(e) => setMensajeRespuesta(e.target.value)}
                        placeholder="Escribe tu respuesta al administrador..."
                        rows="4"
                        style={{
                          width: '100%',
                          padding: '10px',
                          border: '1px solid #d1d5db',
                          borderRadius: '5px',
                          fontSize: '0.95rem',
                          fontFamily: 'inherit',
                          marginBottom: '10px'
                        }}
                      />
                      <button
                        onClick={enviarRespuesta}
                        disabled={enviandoRespuesta || !mensajeRespuesta.trim()}
                        style={{
                          backgroundColor: '#10b981',
                          color: 'white',
                          padding: '10px 20px',
                          border: 'none',
                          borderRadius: '5px',
                          cursor: enviandoRespuesta ? 'not-allowed' : 'pointer',
                          fontSize: '0.95rem',
                          fontWeight: 'bold',
                          opacity: enviandoRespuesta || !mensajeRespuesta.trim() ? 0.5 : 1
                        }}
                      >
                        {enviandoRespuesta ? '⏳ Enviando...' : '📤 Enviar Respuesta'}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* NUEVA CARD: Documentos Oficiales Aprobados */}
          {documentosOficiales.length > 0 && (
            <div className="info-card" style={{backgroundColor: '#f0fdf4', border: '2px solid #86efac'}}>
              <h2 style={{color: '#16a34a'}}>📋 Documentos Oficiales Aprobados</h2>
              <div style={{padding: '15px'}}>
                <p style={{marginBottom: '20px', color: '#15803d', fontWeight: 'bold'}}>
                  ✅ Tus documentos han sido revisados y aprobados por nuestro equipo. Puedes descargarlos aquí:
                </p>
                
                <div style={{display: 'grid', gap: '15px'}}>
                  {documentosOficiales.map((doc, index) => (
                    <div key={index} style={{
                      backgroundColor: 'white',
                      border: '1px solid #86efac',
                      borderRadius: '8px',
                      padding: '15px',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                    }}>
                      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '10px'}}>
                        <div>
                          <h3 style={{margin: '0 0 5px 0', fontSize: '1rem', color: '#111827'}}>
                            📄 {doc.tipo_documento.replace(/_/g, ' ').toUpperCase()}
                          </h3>
                          <p style={{margin: '0', fontSize: '0.85rem', color: '#6b7280'}}>
                            {doc.nombre_archivo}
                          </p>
                        </div>
                        <span style={{
                          backgroundColor: '#10b981',
                          color: 'white',
                          padding: '4px 12px',
                          borderRadius: '12px',
                          fontSize: '0.8rem',
                          fontWeight: 'bold'
                        }}>
                          APROBADO
                        </span>
                      </div>
                      
                      <div style={{fontSize: '0.85rem', color: '#6b7280', marginBottom: '12px'}}>
                        <p style={{margin: '3px 0'}}>
                          🗓️ Generado: {new Date(doc.fecha_generacion).toLocaleDateString('es-ES')}
                        </p>
                        {doc.fecha_aprobacion && (
                          <p style={{margin: '3px 0'}}>
                            ✅ Aprobado: {new Date(doc.fecha_aprobacion).toLocaleDateString('es-ES')}
                          </p>
                        )}
                        {doc.notas && (
                          <p style={{margin: '8px 0 0 0', padding: '8px', backgroundColor: '#fef3c7', borderRadius: '5px', fontSize: '0.85rem'}}>
                            💬 <strong>Nota:</strong> {doc.notas}
                          </p>
                        )}
                      </div>
                      
                      <div style={{display: 'flex', gap: '10px'}}>
                        <button
                          onClick={() => abrirPDFOficial(doc.contenido_pdf, doc.nombre_archivo)}
                          style={{
                            flex: 1,
                            backgroundColor: '#3b82f6',
                            color: 'white',
                            padding: '10px 15px',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer',
                            fontSize: '0.9rem',
                            fontWeight: 'bold'
                          }}
                        >
                          👁️ Ver PDF
                        </button>
                        <button
                          onClick={() => descargarPDFOficial(doc.contenido_pdf, doc.nombre_archivo)}
                          style={{
                            flex: 1,
                            backgroundColor: '#10b981',
                            color: 'white',
                            padding: '10px 15px',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer',
                            fontSize: '0.9rem',
                            fontWeight: 'bold'
                          }}
                        >
                          ⬇️ Descargar PDF
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                
                <div style={{marginTop: '15px', padding: '12px', backgroundColor: '#dbeafe', borderRadius: '5px', fontSize: '0.85rem'}}>
                  <p style={{margin: 0, color: '#1e40af'}}>
                    ℹ️ <strong>Importante:</strong> Estos documentos han sido generados y aprobados oficialmente. 
                    Úsalos para tu proceso de visa. Si necesitas modificaciones, contacta al administrador.
                  </p>
                </div>
              </div>
            </div>
          )}

          {cargandoDocumentosOficiales && (
            <div className="info-card">
              <h2>📋 Documentos Oficiales</h2>
              <div style={{padding: '15px', textAlign: 'center'}}>
                <div className="spinner" style={{margin: '0 auto 10px'}}></div>
                <p style={{color: '#6b7280'}}>Cargando documentos oficiales...</p>
              </div>
            </div>
          )}

          {!cargandoDocumentosOficiales && documentosOficiales.length === 0 && (
            <div className="info-card">
              <h2>📋 Documentos Oficiales</h2>
              <div style={{padding: '15px'}}>
                <p style={{color: '#6b7280', marginBottom: '15px'}}>
                  ℹ️ Aún no tienes documentos oficiales aprobados. El administrador generará y revisará tus documentos pronto.
                </p>
                <p style={{fontSize: '0.85rem', color: '#9ca3af'}}>
                  Recibirás un email cuando tus documentos estén listos para descargar.
                </p>
              </div>
            </div>
          )}

          {/* NUEVA CARD: Generador de Documentos */}
          <div className="info-card">
            <h2>📄 Generar Documentos Borrador</h2>
            <div style={{padding: '15px'}}>
              <p style={{marginBottom: '15px', color: '#6c757d'}}>
                Genera automáticamente documentos borrador para tu solicitud de visa
              </p>
              <button 
                onClick={generarDocumentos}
                disabled={generandoDocs}
                style={{
                  backgroundColor: '#28a745',
                  color: 'white',
                  padding: '12px 24px',
                  border: 'none',
                  borderRadius: '5px',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  cursor: generandoDocs ? 'not-allowed' : 'pointer',
                  opacity: generandoDocs ? 0.6 : 1
                }}
              >
                {generandoDocs ? '⏳ Generando...' : '🚀 Generar Documentos'}
              </button>

              {documentosGenerados && (
                <div style={{marginTop: '20px', borderTop: '2px solid #e9ecef', paddingTop: '20px'}}>
                  <h3 style={{marginBottom: '15px', fontSize: '1.1rem'}}>📥 Documentos Listos para Descargar:</h3>
                  
                  <div style={{display: 'grid', gap: '10px'}}>
                    <button
                      onClick={() => descargarDocumento(documentosGenerados.carta_aceptacion, `Carta_Aceptacion_${estudiante.nombre}.txt`)}
                      style={{
                        backgroundColor: '#007bff',
                        color: 'white',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        fontSize: '0.95rem'
                      }}
                    >
                      📜 Descargar Carta de Aceptación (Borrador)
                    </button>

                    <button
                      onClick={() => descargarDocumento(documentosGenerados.carta_patrocinio, `Carta_Patrocinio_${estudiante.nombre}.txt`)}
                      style={{
                        backgroundColor: '#007bff',
                        color: 'white',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        fontSize: '0.95rem'
                      }}
                    >
                      💰 Descargar Carta de Patrocinio (Borrador)
                    </button>

                    <button
                      onClick={() => descargarDocumento(documentosGenerados.checklist_personalizado, `Checklist_${estudiante.nombre}.txt`)}
                      style={{
                        backgroundColor: '#007bff',
                        color: 'white',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        fontSize: '0.95rem'
                      }}
                    >
                      ✅ Descargar Checklist Personalizado
                    </button>
                  </div>

                  <p style={{marginTop: '15px', fontSize: '0.85rem', color: '#dc3545', fontWeight: 'bold'}}>
                    ⚠️ IMPORTANTE: Estos son BORRADORES. Deben ser completados con datos reales y firmados oficialmente.
                  </p>
                </div>
              )}
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
