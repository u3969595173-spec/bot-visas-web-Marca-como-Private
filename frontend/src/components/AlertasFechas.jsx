import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AlertasFechas.css'

const AlertasFechas = ({ estudianteId }) => {
  const [fechas, setFechas] = useState([])
  const [loading, setLoading] = useState(true)
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [formulario, setFormulario] = useState({
    tipo_fecha: 'entrevista_consular',
    fecha: '',
    hora: '09:00',
    descripcion: ''
  })

  const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

  const tiposFecha = {
    entrevista_consular: { nombre: 'Entrevista Consular', emoji: '🎤', color: '#dc3545' },
    vencimiento_pasaporte: { nombre: 'Vencimiento de Pasaporte', emoji: '📘', color: '#ffc107' },
    vencimiento_documento: { nombre: 'Vencimiento de Documento', emoji: '📄', color: '#ffc107' },
    deadline_aplicacion: { nombre: 'Fecha Límite de Aplicación', emoji: '⏰', color: '#fd7e14' },
    cita_visa: { nombre: 'Cita para Visa', emoji: '📅', color: '#dc3545' },
    inicio_clases: { nombre: 'Inicio de Clases', emoji: '🎓', color: '#28a745' },
    pago_matricula: { nombre: 'Pago de Matrícula', emoji: '💵', color: '#17a2b8' },
    renovacion_visa: { nombre: 'Renovación de Visa', emoji: '🔄', color: '#6c757d' },
    entrega_documentos: { nombre: 'Entrega de Documentos', emoji: '📋', color: '#007bff' },
    otro: { nombre: 'Otro', emoji: '📌', color: '#6c757d' }
  }

  useEffect(() => {
    cargarFechas()
  }, [estudianteId])

  const cargarFechas = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/alertas/estudiante/${estudianteId}`)
      if (response.data.success) {
        setFechas(response.data.fechas)
      }
    } catch (error) {
      console.error('Error cargando fechas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormulario(prev => ({ ...prev, [name]: value }))
  }

  const agregarFecha = async (e) => {
    e.preventDefault()
    
    try {
      const fechaCompleta = `${formulario.fecha}T${formulario.hora}:00`
      
      await axios.post(`${API_URL}/api/alertas/fecha`, {
        estudiante_id: parseInt(estudianteId),
        tipo_fecha: formulario.tipo_fecha,
        fecha: fechaCompleta,
        descripcion: formulario.descripcion || null
      })

      // Resetear formulario
      setFormulario({
        tipo_fecha: 'entrevista_consular',
        fecha: '',
        hora: '09:00',
        descripcion: ''
      })
      setMostrarFormulario(false)
      
      // Recargar fechas
      await cargarFechas()
      
    } catch (error) {
      console.error('Error agregando fecha:', error)
      alert('Error al agregar fecha. Por favor intenta de nuevo.')
    }
  }

  const marcarCompletada = async (fechaId) => {
    try {
      await axios.put(`${API_URL}/api/alertas/${fechaId}/completar`)
      await cargarFechas()
    } catch (error) {
      console.error('Error marcando fecha completada:', error)
    }
  }

  const eliminarFecha = async (fechaId) => {
    if (!confirm('¿Estás seguro de que quieres eliminar esta fecha?')) return
    
    try {
      await axios.delete(`${API_URL}/api/alertas/${fechaId}`)
      await cargarFechas()
    } catch (error) {
      console.error('Error eliminando fecha:', error)
    }
  }

  const descargarCalendario = (fechaId) => {
    window.open(`${API_URL}/api/alertas/${fechaId}/descargar-ics`, '_blank')
  }

  const getUrgencia = (diasRestantes) => {
    if (diasRestantes <= 1) return { nivel: 'critico', texto: '¡URGENTE!', color: '#dc3545' }
    if (diasRestantes <= 7) return { nivel: 'alto', texto: 'Próximamente', color: '#ffc107' }
    if (diasRestantes <= 30) return { nivel: 'medio', texto: 'Este mes', color: '#17a2b8' }
    return { nivel: 'bajo', texto: 'Planificado', color: '#28a745' }
  }

  const formatearFecha = (fechaISO) => {
    const fecha = new Date(fechaISO)
    return fecha.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return <div className="alertas-container"><p>Cargando fechas importantes...</p></div>
  }

  return (
    <div className="alertas-container">
      <div className="alertas-header">
        <h1>📅 Fechas Importantes</h1>
        <p className="subtitle">Mantén el control de todas tus fechas críticas</p>
        <button 
          className="btn-agregar-fecha"
          onClick={() => setMostrarFormulario(!mostrarFormulario)}
        >
          {mostrarFormulario ? '✕ Cancelar' : '➕ Agregar Fecha'}
        </button>
      </div>

      {mostrarFormulario && (
        <div className="formulario-fecha">
          <h3>➕ Nueva Fecha Importante</h3>
          <form onSubmit={agregarFecha}>
            <div className="form-row">
              <div className="form-group">
                <label>Tipo de Fecha</label>
                <select 
                  name="tipo_fecha" 
                  value={formulario.tipo_fecha} 
                  onChange={handleChange}
                  required
                >
                  {Object.entries(tiposFecha).map(([key, val]) => (
                    <option key={key} value={key}>
                      {val.emoji} {val.nombre}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label>Fecha</label>
                <input 
                  type="date" 
                  name="fecha" 
                  value={formulario.fecha} 
                  onChange={handleChange}
                  required
                  min={new Date().toISOString().split('T')[0]}
                />
              </div>
              <div className="form-group">
                <label>Hora</label>
                <input 
                  type="time" 
                  name="hora" 
                  value={formulario.hora} 
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Descripción (opcional)</label>
              <textarea 
                name="descripcion" 
                value={formulario.descripcion} 
                onChange={handleChange}
                rows="3"
                placeholder="Ej: Entrevista en Consulado de España - Traer pasaporte original y copias"
              />
            </div>

            <div className="alerta-info">
              ℹ️ Recibirás alertas por email 30, 15, 7 y 1 día antes de la fecha
            </div>

            <button type="submit" className="btn-guardar">
              💾 Guardar Fecha
            </button>
          </form>
        </div>
      )}

      {fechas.length === 0 ? (
        <div className="sin-fechas">
          <div className="sin-fechas-icon">📭</div>
          <h3>No tienes fechas importantes registradas</h3>
          <p>Agrega tus fechas críticas y recibe alertas automáticas por email</p>
          <button 
            className="btn-agregar-primera"
            onClick={() => setMostrarFormulario(true)}
          >
            ➕ Agregar Mi Primera Fecha
          </button>
        </div>
      ) : (
        <div className="timeline-container">
          <div className="timeline-header">
            <h3>📍 Próximas Fechas ({fechas.length})</h3>
          </div>
          
          <div className="timeline">
            {fechas.map((fecha, index) => {
              const tipoInfo = tiposFecha[fecha.tipo_fecha] || tiposFecha.otro
              const urgencia = getUrgencia(fecha.dias_restantes)
              
              return (
                <div 
                  key={fecha.id} 
                  className={`timeline-item urgencia-${urgencia.nivel}`}
                  style={{ borderLeftColor: tipoInfo.color }}
                >
                  <div className="timeline-marker" style={{ backgroundColor: tipoInfo.color }}>
                    {tipoInfo.emoji}
                  </div>
                  
                  <div className="timeline-content">
                    <div className="timeline-fecha-header">
                      <div>
                        <h4>{tipoInfo.nombre}</h4>
                        <p className="fecha-completa">{formatearFecha(fecha.fecha)}</p>
                      </div>
                      <div className="urgencia-badge" style={{ backgroundColor: urgencia.color }}>
                        {urgencia.texto}
                      </div>
                    </div>

                    <div className="dias-restantes-box">
                      <div className="dias-numero">{fecha.dias_restantes}</div>
                      <div className="dias-texto">día{fecha.dias_restantes !== 1 ? 's' : ''}</div>
                    </div>

                    {fecha.descripcion && (
                      <div className="fecha-descripcion">
                        <strong>Detalles:</strong>
                        <p>{fecha.descripcion}</p>
                      </div>
                    )}

                    <div className="alertas-enviadas">
                      <span className={fecha.alertado_30d ? 'enviado' : 'pendiente'}>
                        {fecha.alertado_30d ? '✓' : '○'} 30 días
                      </span>
                      <span className={fecha.alertado_15d ? 'enviado' : 'pendiente'}>
                        {fecha.alertado_15d ? '✓' : '○'} 15 días
                      </span>
                      <span className={fecha.alertado_7d ? 'enviado' : 'pendiente'}>
                        {fecha.alertado_7d ? '✓' : '○'} 7 días
                      </span>
                      <span className={fecha.alertado_1d ? 'enviado' : 'pendiente'}>
                        {fecha.alertado_1d ? '✓' : '○'} 1 día
                      </span>
                    </div>

                    <div className="fecha-acciones">
                      <button 
                        className="btn-accion btn-calendario"
                        onClick={() => descargarCalendario(fecha.id)}
                        title="Descargar para mi calendario"
                      >
                        📥 Calendario
                      </button>
                      <button 
                        className="btn-accion btn-completar"
                        onClick={() => marcarCompletada(fecha.id)}
                        title="Marcar como completada"
                      >
                        ✓ Completar
                      </button>
                      <button 
                        className="btn-accion btn-eliminar"
                        onClick={() => eliminarFecha(fecha.id)}
                        title="Eliminar fecha"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      <div className="info-footer">
        <div className="info-card">
          <h4>📧 Alertas Automáticas</h4>
          <p>Recibirás emails automáticos 30, 15, 7 y 1 día antes de cada fecha importante.</p>
        </div>
        <div className="info-card">
          <h4>📅 Sincroniza tu Calendario</h4>
          <p>Descarga el archivo .ics y agrégalo a Google Calendar, Outlook o Apple Calendar.</p>
        </div>
        <div className="info-card">
          <h4>🔔 No te pierdas nada</h4>
          <p>Mantente al día con todas tus fechas críticas para tu visa de estudiante.</p>
        </div>
      </div>
    </div>
  )
}

export default AlertasFechas
