import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import './RegistroEstudiante.css';

const CompletarPerfil = () => {
  const navigate = useNavigate();
  const { estudianteId } = useParams();
  const [formData, setFormData] = useState({
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
    fondos_suficientes: false,
    monto_fondos: '',
    tiene_patrocinador: false,
    tipo_patrocinador: '',
    nombre_patrocinador: '',
    relacion_patrocinador: ''
  });
  const [archivos, setArchivos] = useState({
    titulo: null,
    pasaporte_archivo: null,
    extractos: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [estudiante, setEstudiante] = useState(null);

  useEffect(() => {
    cargarEstudiante();
  }, [estudianteId]);

  const cargarEstudiante = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const codigo = localStorage.getItem('codigo_acceso');
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}?codigo_acceso=${codigo}`);
      setEstudiante(response.data);
      
      // Pre-llenar campos si ya existen
      if (response.data.pasaporte) setFormData(prev => ({...prev, pasaporte: response.data.pasaporte}));
      if (response.data.fecha_nacimiento) setFormData(prev => ({...prev, fecha_nacimiento: response.data.fecha_nacimiento}));
      if (response.data.edad) setFormData(prev => ({...prev, edad: response.data.edad}));
      if (response.data.nacionalidad) setFormData(prev => ({...prev, nacionalidad: response.data.nacionalidad}));
      if (response.data.pais_origen) setFormData(prev => ({...prev, pais_origen: response.data.pais_origen}));
      if (response.data.ciudad_origen) setFormData(prev => ({...prev, ciudad_origen: response.data.ciudad_origen}));
      if (response.data.carrera_deseada) setFormData(prev => ({...prev, carrera_deseada: response.data.carrera_deseada}));
      if (response.data.especialidad) setFormData(prev => ({...prev, especialidad: response.data.especialidad}));
      if (response.data.nivel_espanol) setFormData(prev => ({...prev, nivel_espanol: response.data.nivel_espanol}));
      if (response.data.tipo_visa) setFormData(prev => ({...prev, tipo_visa: response.data.tipo_visa}));
      if (response.data.fondos_disponibles) setFormData(prev => ({...prev, fondos_disponibles: response.data.fondos_disponibles}));
      if (response.data.fecha_inicio_estimada) setFormData(prev => ({...prev, fecha_inicio_estimada: response.data.fecha_inicio_estimada}));
      if (response.data.fondos_suficientes !== undefined) setFormData(prev => ({...prev, fondos_suficientes: response.data.fondos_suficientes}));
      if (response.data.monto_fondos) setFormData(prev => ({...prev, monto_fondos: response.data.monto_fondos}));
      if (response.data.tiene_patrocinador !== undefined) setFormData(prev => ({...prev, tiene_patrocinador: response.data.tiene_patrocinador}));
      if (response.data.tipo_patrocinador) setFormData(prev => ({...prev, tipo_patrocinador: response.data.tipo_patrocinador}));
      if (response.data.nombre_patrocinador) setFormData(prev => ({...prev, nombre_patrocinador: response.data.nombre_patrocinador}));
      if (response.data.relacion_patrocinador) setFormData(prev => ({...prev, relacion_patrocinador: response.data.relacion_patrocinador}));
    } catch (err) {
      console.error('Error cargando estudiante:', err);
      setError('Error al cargar tus datos');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    if (files && files[0]) {
      const file = files[0];
      const maxSize = 10 * 1024 * 1024; // 10MB
      
      if (file.size > maxSize) {
        setError(`El archivo "${file.name}" excede el tamaño máximo de 10MB`);
        e.target.value = '';
        return;
      }
      
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
      if (!allowedTypes.includes(file.type)) {
        setError(`Tipo de archivo no permitido. Solo PDF, JPG y PNG`);
        e.target.value = '';
        return;
      }
      
      setError('');
      setArchivos(prev => ({
        ...prev,
        [name]: file
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const codigo = localStorage.getItem('codigo_acceso');
      
      // Crear FormData para enviar archivos
      const formDataToSend = new FormData();
      
      // Agregar todos los campos
      Object.keys(formData).forEach(key => {
        if (formData[key]) {
          formDataToSend.append(key, formData[key]);
        }
      });
      
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

      await axios.put(
        `${apiUrl}/api/estudiantes/${estudianteId}/completar-perfil?codigo_acceso=${codigo}`,
        formDataToSend,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      alert('✅ Perfil completado exitosamente');
      navigate(`/dashboard-usuario/${estudianteId}`);
    } catch (err) {
      console.error('Error al completar perfil:', err);
      setError(err.response?.data?.detail || 'Error al completar perfil');
    } finally {
      setLoading(false);
    }
  };

  if (!estudiante) {
    return <div style={{padding: '40px', textAlign: 'center'}}>Cargando...</div>;
  }

  return (
    <div className="registro-container">
      <div className="registro-card">
        <div className="registro-header">
          <h1>Completar tu Perfil</h1>
          <p>Proporciona la información adicional para procesar tu visa</p>
          <div style={{
            background: '#f7fafc',
            padding: '15px',
            borderRadius: '10px',
            marginTop: '15px',
            border: '1px solid #e2e8f0'
          }}>
            <p style={{margin: 0, fontSize: '14px', color: '#4a5568'}}>
              👤 <strong>{estudiante.nombre}</strong>
            </p>
            <p style={{margin: '5px 0 0 0', fontSize: '13px', color: '#718096'}}>
              📧 {estudiante.email}
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="registro-form">
          <div className="form-section">
            <h3>📋 Datos Personales</h3>
            
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
            </div>

            <div className="form-row">
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
            <h3>🎓 Información Académica</h3>

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

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠</span>
              {error}
            </div>
          )}

          <div style={{display: 'flex', gap: '10px', justifyContent: 'center'}}>
            <button
              type="button"
              onClick={() => navigate(`/dashboard-usuario/${estudianteId}`)}
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
              Cancelar
            </button>
            <button 
              type="submit" 
              className="submit-button"
              disabled={loading}
            >
              {loading ? 'Guardando...' : '✅ Completar Perfil'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CompletarPerfil;
