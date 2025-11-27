import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ContactarUniversidades.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function ContactarUniversidades() {
  const [universidades, setUniversidades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [enviando, setEnviando] = useState(null);
  const [mensaje, setMensaje] = useState({ tipo: '', texto: '' });
  const [editando, setEditando] = useState(null);
  const [formData, setFormData] = useState({
    numeroEstudiantes: '15',
    observaciones: ''
  });

  useEffect(() => {
    cargarUniversidades();
  }, []);

  const cargarUniversidades = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE_URL}/api/admin/universidades`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUniversidades(response.data);
    } catch (error) {
      console.error('Error al cargar universidades:', error);
      setMensaje({ tipo: 'error', texto: 'Error al cargar universidades' });
    } finally {
      setLoading(false);
    }
  };

  const contactarUniversidad = async (universidad) => {
    if (!window.confirm(`¿Enviar email a ${universidad.universidad}?`)) {
      return;
    }

    setEnviando(universidad.id);
    setMensaje({ tipo: '', texto: '' });

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/api/admin/contactar-universidad/${universidad.id}`,
        {
          numero_estudiantes: parseInt(formData.numeroEstudiantes),
          observaciones: formData.observaciones
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setMensaje({ tipo: 'success', texto: `✅ Email enviado exitosamente a ${universidad.universidad}` });
      cargarUniversidades();
    } catch (error) {
      console.error('Error al enviar email:', error);
      setMensaje({ 
        tipo: 'error', 
        texto: error.response?.data?.detail || 'Error al enviar email. Verifica la configuración de Gmail.' 
      });
    } finally {
      setEnviando(null);
    }
  };

  const actualizarEstado = async (id, nuevoEstado, notas) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        `${API_BASE_URL}/api/admin/universidades/${id}`,
        { estado: nuevoEstado, notas },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setMensaje({ tipo: 'success', texto: '✅ Estado actualizado' });
      setEditando(null);
      cargarUniversidades();
    } catch (error) {
      console.error('Error al actualizar:', error);
      setMensaje({ tipo: 'error', texto: 'Error al actualizar estado' });
    }
  };

  const getEstadoBadge = (estado) => {
    const badges = {
      pendiente: { color: '#ffc107', texto: '⏳ Pendiente' },
      contactado: { color: '#2196f3', texto: '📧 Contactado' },
      respondido: { color: '#9c27b0', texto: '💬 Respondió' },
      reunion_agendada: { color: '#ff9800', texto: '📅 Reunión Agendada' },
      acuerdo_firmado: { color: '#4caf50', texto: '✅ Acuerdo Firmado' }
    };
    const badge = badges[estado] || badges.pendiente;
    return (
      <span style={{ 
        backgroundColor: badge.color, 
        color: 'white', 
        padding: '5px 10px', 
        borderRadius: '15px',
        fontSize: '12px',
        fontWeight: 'bold'
      }}>
        {badge.texto}
      </span>
    );
  };

  const formatearFecha = (fecha) => {
    if (!fecha) return '-';
    return new Date(fecha).toLocaleString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return <div className="contactar-universidades"><p>Cargando...</p></div>;
  }

  const stats = {
    total: universidades.length,
    pendientes: universidades.filter(u => u.estado === 'pendiente').length,
    contactados: universidades.filter(u => u.estado === 'contactado').length,
    respondidos: universidades.filter(u => u.estado === 'respondido').length,
    acuerdos: universidades.filter(u => u.estado === 'acuerdo_firmado').length
  };

  return (
    <div className="contactar-universidades">
      <h2>📧 Contactar Universidades</h2>

      {mensaje.texto && (
        <div className={`mensaje ${mensaje.tipo}`}>
          {mensaje.texto}
        </div>
      )}

      <div className="stats-grid">
        <div className="stat-card">
          <h3>{stats.total}</h3>
          <p>Total Universidades</p>
        </div>
        <div className="stat-card pendiente">
          <h3>{stats.pendientes}</h3>
          <p>⏳ Pendientes</p>
        </div>
        <div className="stat-card contactado">
          <h3>{stats.contactados}</h3>
          <p>📧 Contactados</p>
        </div>
        <div className="stat-card respondido">
          <h3>{stats.respondidos}</h3>
          <p>💬 Respondieron</p>
        </div>
        <div className="stat-card acuerdo">
          <h3>{stats.acuerdos}</h3>
          <p>✅ Acuerdos</p>
        </div>
      </div>

      <div className="config-email">
        <h3>📝 Configuración del Email</h3>
        <div className="form-group">
          <label>Número de estudiantes disponibles:</label>
          <input
            type="number"
            value={formData.numeroEstudiantes}
            onChange={(e) => setFormData({ ...formData, numeroEstudiantes: e.target.value })}
            min="1"
          />
        </div>
        <div className="form-group">
          <label>Observaciones adicionales (opcional):</label>
          <textarea
            value={formData.observaciones}
            onChange={(e) => setFormData({ ...formData, observaciones: e.target.value })}
            placeholder="Ej: Estudiantes principalmente interesados en grados de Ingeniería..."
            rows="3"
          />
        </div>
      </div>

      <div className="universidades-lista">
        {universidades.map((uni) => (
          <div key={uni.id} className="universidad-card">
            <div className="uni-header">
              <h3>{uni.universidad}</h3>
              {getEstadoBadge(uni.estado)}
            </div>
            
            <div className="uni-info">
              <p><strong>📧 Email:</strong> {uni.email}</p>
              <p><strong>📞 Teléfono:</strong> {uni.telefono}</p>
              <p><strong>👤 Contacto:</strong> {uni.contacto_nombre}</p>
              <p><strong>📍 Ciudad:</strong> {uni.ciudad}</p>
              <p><strong>📚 Programas:</strong> {uni.programas_interes}</p>
              
              {uni.fecha_contacto && (
                <p><strong>Contactado:</strong> {formatearFecha(uni.fecha_contacto)}</p>
              )}
              {uni.fecha_respuesta && (
                <p><strong>Respondió:</strong> {formatearFecha(uni.fecha_respuesta)}</p>
              )}
              {uni.notas && (
                <p><strong>Notas:</strong> {uni.notas}</p>
              )}
            </div>

            <div className="uni-acciones">
              <button
                onClick={() => contactarUniversidad(uni)}
                disabled={enviando === uni.id}
                className="btn-contactar"
              >
                {enviando === uni.id ? '⏳ Enviando...' : '📧 Enviar Email'}
              </button>

              <button
                onClick={() => setEditando(uni.id)}
                className="btn-editar"
              >
                ✏️ Actualizar Estado
              </button>
            </div>

            {editando === uni.id && (
              <div className="editar-form">
                <h4>Actualizar Estado</h4>
                <select
                  defaultValue={uni.estado}
                  onChange={(e) => {
                    const notas = prompt('Notas/Observaciones:');
                    actualizarEstado(uni.id, e.target.value, notas);
                  }}
                >
                  <option value="pendiente">⏳ Pendiente</option>
                  <option value="contactado">📧 Contactado</option>
                  <option value="respondido">💬 Respondió</option>
                  <option value="reunion_agendada">📅 Reunión Agendada</option>
                  <option value="acuerdo_firmado">✅ Acuerdo Firmado</option>
                </select>
                <button onClick={() => setEditando(null)}>Cancelar</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ContactarUniversidades;
