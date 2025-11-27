import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AdminServicios.css'

function AdminServicios() {
  const [servicios, setServicios] = useState([])
  const [loading, setLoading] = useState(true)
  const [editando, setEditando] = useState(null)
  const [precio, setPrecio] = useState('')
  const [notas, setNotas] = useState('')
  const [estado, setEstado] = useState('pendiente')

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const token = localStorage.getItem('token')

  useEffect(() => {
    cargarServicios()
  }, [])

  const cargarServicios = async () => {
    try {
      const res = await axios.get(`${apiUrl}/api/admin/servicios-solicitados`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setServicios(res.data.servicios || [])
    } catch (err) {
      console.error('Error cargando servicios:', err)
      alert('Error cargando servicios solicitados')
    } finally {
      setLoading(false)
    }
  }

  const abrirEdicion = (servicio) => {
    setEditando(servicio.id)
    setPrecio(servicio.precio || '')
    setNotas(servicio.notas || '')
    setEstado(servicio.estado)
  }

  const guardarCambios = async (servicioId) => {
    try {
      await axios.put(
        `${apiUrl}/api/admin/servicios-solicitados/${servicioId}`,
        { estado, precio: parseFloat(precio) || null, notas },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      alert('✅ Servicio actualizado')
      setEditando(null)
      cargarServicios()
    } catch (err) {
      console.error('Error actualizando:', err)
      alert('Error al actualizar servicio')
    }
  }

  const serviciosPorEstado = {
    pendiente: servicios.filter(s => s.estado === 'pendiente'),
    en_proceso: servicios.filter(s => s.estado === 'en_proceso'),
    completado: servicios.filter(s => s.estado === 'completado')
  }

  if (loading) {
    return <div className="admin-servicios-loading">Cargando solicitudes...</div>
  }

  return (
    <div className="admin-servicios">
      <div className="admin-servicios-header">
        <h2>💼 Servicios Solicitados por Estudiantes</h2>
        <div className="servicios-stats">
          <div className="stat-card pendiente">
            <div className="stat-numero">{serviciosPorEstado.pendiente.length}</div>
            <div className="stat-label">Pendientes</div>
          </div>
          <div className="stat-card proceso">
            <div className="stat-numero">{serviciosPorEstado.en_proceso.length}</div>
            <div className="stat-label">En Proceso</div>
          </div>
          <div className="stat-card completado">
            <div className="stat-numero">{serviciosPorEstado.completado.length}</div>
            <div className="stat-label">Completados</div>
          </div>
        </div>
      </div>

      {servicios.length === 0 ? (
        <div className="no-servicios">
          <p>📭 No hay solicitudes de servicios todavía</p>
        </div>
      ) : (
        <div className="servicios-lista">
          {servicios.map(servicio => (
            <div key={servicio.id} className={`servicio-card estado-${servicio.estado}`}>
              <div className="servicio-header">
                <div className="servicio-icon">
                  {servicio.servicio_id === 'antecedentes' ? '📋' : '🏛️'}
                </div>
                <div className="servicio-info">
                  <h3>{servicio.servicio_nombre}</h3>
                  <p className="estudiante-nombre">
                    👤 {servicio.estudiante_nombre}
                    <span className="estudiante-email"> ({servicio.estudiante_email})</span>
                  </p>
                  <p className="fecha-solicitud">
                    📅 Solicitado: {new Date(servicio.fecha_solicitud).toLocaleString('es-ES')}
                  </p>
                </div>
                <div className={`estado-badge badge-${servicio.estado}`}>
                  {servicio.estado === 'pendiente' && '⏳ Pendiente'}
                  {servicio.estado === 'en_proceso' && '🔄 En Proceso'}
                  {servicio.estado === 'completado' && '✅ Completado'}
                </div>
              </div>

              {editando === servicio.id ? (
                <div className="servicio-edicion">
                  <div className="form-group">
                    <label>Estado</label>
                    <select value={estado} onChange={(e) => setEstado(e.target.value)}>
                      <option value="pendiente">⏳ Pendiente</option>
                      <option value="en_proceso">🔄 En Proceso</option>
                      <option value="completado">✅ Completado</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Precio (€)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={precio}
                      onChange={(e) => setPrecio(e.target.value)}
                      placeholder="Ej: 150.00"
                    />
                  </div>
                  <div className="form-group">
                    <label>Notas para el estudiante</label>
                    <textarea
                      value={notas}
                      onChange={(e) => setNotas(e.target.value)}
                      placeholder="Información adicional, instrucciones, etc."
                      rows="3"
                    />
                  </div>
                  <div className="form-actions">
                    <button className="btn-guardar" onClick={() => guardarCambios(servicio.id)}>
                      💾 Guardar
                    </button>
                    <button className="btn-cancelar" onClick={() => setEditando(null)}>
                      ✖️ Cancelar
                    </button>
                  </div>
                </div>
              ) : (
                <div className="servicio-detalles">
                  {servicio.precio && (
                    <p className="servicio-precio">💰 Precio: <strong>{servicio.precio}€</strong></p>
                  )}
                  {servicio.notas && (
                    <p className="servicio-notas">📝 Notas: {servicio.notas}</p>
                  )}
                  <button className="btn-editar" onClick={() => abrirEdicion(servicio)}>
                    ✏️ Editar
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default AdminServicios
