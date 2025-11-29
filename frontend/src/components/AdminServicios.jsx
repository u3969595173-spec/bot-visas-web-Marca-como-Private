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

  const limpiarTodosLosPresupuestos = async () => {
    if (!confirm('⚠️ ¿ELIMINAR TODOS los presupuestos aceptados del panel?\n\nEsto borrará TODO el seguimiento actual.\nÚsalo solo para empezar de cero con pruebas.\n\n¿Continuar?')) {
      return
    }

    try {
      const res = await axios.delete(`${apiUrl}/api/admin/presupuestos/limpiar-aceptados`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      alert(`✅ ${res.data.message}`)
      cargarServicios()
    } catch (err) {
      console.error('Error limpiando presupuestos:', err)
      alert('❌ Error al limpiar presupuestos: ' + (err.response?.data?.detail || err.message))
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
        <button
          onClick={limpiarTodosLosPresupuestos}
          style={{
            padding: '10px 20px',
            backgroundColor: '#ef4444',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#dc2626'}
          onMouseLeave={(e) => e.target.style.backgroundColor = '#ef4444'}
        >
          🗑️ Limpiar Panel (Pruebas)
        </button>
      </div>
      
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

      {servicios.length === 0 ? (
        <div className="no-servicios">
          <p>📭 No hay presupuestos aceptados todavía</p>
        </div>
      ) : (
        <div className="servicios-lista">
          {servicios.map(servicio => (
            <div key={servicio.id} className={`servicio-card estado-${servicio.estado}`}>
              <div className="servicio-header">
                <div className="servicio-icon">
                  💼
                </div>
                <div className="servicio-info">
                  <h3>Presupuesto #{servicio.id}</h3>
                  <p className="estudiante-nombre">
                    👤 {servicio.estudiante_nombre}
                    <span className="estudiante-email"> ({servicio.estudiante_email})</span>
                  </p>
                  <p className="fecha-solicitud">
                    📅 Aceptado: {new Date(servicio.fecha_solicitud).toLocaleString('es-ES')}
                  </p>
                  <div style={{ marginTop: '10px' }}>
                    <strong>Servicios solicitados:</strong>
                    <ul style={{ marginLeft: '20px', marginTop: '5px' }}>
                      {servicio.servicios_solicitados && Array.isArray(servicio.servicios_solicitados) && servicio.servicios_solicitados.map((s, idx) => (
                        <li key={idx} style={{ fontSize: '12px', color: '#6b7280' }}>{s}</li>
                      ))}
                    </ul>
                  </div>
                  <div style={{ marginTop: '10px', fontSize: '12px', color: '#4b5563' }}>
                    <strong>Estado de pagos:</strong>
                    <div style={{ marginLeft: '10px', marginTop: '5px' }}>
                      {servicio.pagado_al_empezar ? '✅' : '⏳'} Pago Inicial
                      <br />
                      {servicio.pagado_con_visa ? '✅' : '⏳'} Pago con Visa
                      <br />
                      {servicio.pagado_financiado ? '✅' : '⏳'} Pago Financiado
                    </div>
                  </div>
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
                    <label>Estado del Servicio</label>
                    <select value={estado} onChange={(e) => setEstado(e.target.value)}>
                      <option value="pendiente">⏳ Pendiente (No ha pagado inicial)</option>
                      <option value="en_proceso">🔄 En Proceso (Pagó inicial, trabajando)</option>
                      <option value="completado">✅ Completado (Proceso de visa terminado)</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Monto Total</label>
                    <input
                      type="text"
                      value={`€${servicio.monto_total}`}
                      disabled
                      style={{ background: '#f3f4f6', cursor: 'not-allowed' }}
                    />
                    <small style={{ color: '#6b7280' }}>El monto no se puede editar aquí</small>
                  </div>
                  <div className="form-actions">
                    <button className="btn-guardar" onClick={() => guardarCambios(servicio.id)}>
                      💾 Actualizar Estado
                    </button>
                    <button className="btn-cancelar" onClick={() => setEditando(null)}>
                      ✖️ Cancelar
                    </button>
                  </div>
                </div>
              ) : (
                <div className="servicio-detalles">
                  <p className="servicio-precio">💰 Monto Total: <strong>€{servicio.monto_total.toFixed(2)}</strong></p>
                  <button className="btn-editar" onClick={() => abrirEdicion(servicio)}>
                    ✏️ Cambiar Estado
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
