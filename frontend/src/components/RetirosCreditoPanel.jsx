import React, { useState, useEffect } from 'react'
import axios from 'axios'
import '../styles/RetirosCreditoPanel.css'

const RetirosCreditoPanel = () => {
  const [solicitudes, setSolicitudes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [procesando, setProcesando] = useState({})

  const apiUrl = import.meta.env.VITE_API_URL || 'https://bot-visas-web-marca-como-private.onrender.com'

  useEffect(() => {
    cargarSolicitudes()
    // Recargar cada 30 segundos
    const interval = setInterval(cargarSolicitudes, 30000)
    return () => clearInterval(interval)
  }, [])

  const cargarSolicitudes = async () => {
    try {
      setLoading(true)
      const token = localStorage.getItem('token')
      const headers = token ? { Authorization: `Bearer ${token}` } : {}

      const response = await axios.get(
        `${apiUrl}/api/retiros`,
        { headers }
      )

      const retiros = response.data?.retiros || []
      setSolicitudes(retiros.map((retiro) => ({
        ...retiro,
        monto: Number(retiro.importe || 0),
        fecha_solicitud: retiro.fecha || retiro.created_at,
        beneficiario_tipo: 'inversor',
        credito_disponible: null
      })))
      setError(null)
    } catch (err) {
      console.error('Error cargando solicitudes:', err)
      setError(err.response?.data?.detail || 'Error cargando solicitudes')
      setSolicitudes([])
    } finally {
      setLoading(false)
    }
  }

  const procesarSolicitud = async (solicitudId, accion, notas = '') => {
    const solicitud = solicitudes.find(s => s.id === solicitudId)

    // Confirmación
    const mensaje = accion === 'aprobar'
      ? `¿Aprobar retiro de ${solicitud.monto}€ a ${solicitud.nombre}?`
      : `¿Rechazar retiro de ${solicitud.monto}€?`

    if (!window.confirm(mensaje)) return

    try {
      setProcesando(prev => ({ ...prev, [solicitudId]: true }))
      const token = localStorage.getItem('token')
      const headers = token ? { Authorization: `Bearer ${token}` } : {}

      const response = await axios.put(
        `${apiUrl}/api/retiros/${solicitudId}`,
        { estado: accion === 'aprobar' ? 'Aprobado' : 'Rechazado', notas },
        { headers }
      )

      // Actualizar lista
      await cargarSolicitudes()
      alert(`Solicitud ${accion === 'aprobar' ? 'aprobada' : 'rechazada'} correctamente`)
    } catch (err) {
      const mensajeError = err.response?.data?.detail || 'Error procesando solicitud'
      alert(`Error: ${mensajeError}`)
      console.error('Error procesando solicitud:', err)
    } finally {
      setProcesando(prev => ({ ...prev, [solicitudId]: false }))
    }
  }

  const getBadgeTipo = (tipo) => {
    if (tipo === 'agente') {
      return <span className="badge badge-agente">👤 Agente</span>
    }
    return <span className="badge badge-estudiante">🎓 Estudiante</span>
  }

  const getBadgeEstado = (estado) => {
    const estadoLower = estado?.toLowerCase() || 'pendiente'
    if (estadoLower === 'pendiente') {
      return <span className="badge badge-pendiente">⏳ Pendiente</span>
    } else if (estadoLower === 'aprobada') {
      return <span className="badge badge-aprobada">✅ Aprobada</span>
    } else if (estadoLower === 'rechazada') {
      return <span className="badge badge-rechazada">❌ Rechazada</span>
    }
    return <span className="badge">{estado}</span>
  }

  const formatFecha = (fecha) => {
    if (!fecha) return '-'
    const date = new Date(fecha)
    return date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const solicitudesPendientes = solicitudes.filter(s => ['pendiente', 'pendiente de validación', 'en revisión'].includes(s.estado?.toLowerCase()))
  const solicitudesAprobadas = solicitudes.filter(s => ['aprobada', 'aprobado', 'procesado', 'validada', 'validado'].includes(s.estado?.toLowerCase()))
  const solicitudesRechazadas = solicitudes.filter(s => ['rechazada', 'rechazado'].includes(s.estado?.toLowerCase()))

  if (loading && solicitudes.length === 0) {
    return (
      <div className="retiros-panel">
        <div className="loading">Cargando solicitudes...</div>
      </div>
    )
  }

  return (
    <div className="retiros-panel">
      <div className="panel-header">
        <h2>💰 Gestión de Retiros e Inversiones</h2>
        <button
          className="btn-reload"
          onClick={cargarSolicitudes}
          disabled={loading}
        >
          🔄 Actualizar
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-value">{solicitudesPendientes.length}</div>
          <div className="stat-label">⏳ Pendientes</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{solicitudesAprobadas.length}</div>
          <div className="stat-label">✅ Aprobadas</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{solicitudesRechazadas.length}</div>
          <div className="stat-label">❌ Rechazadas</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {(solicitudesPendientes.reduce((sum, s) => sum + (s.monto || 0), 0)).toFixed(2)}€
          </div>
          <div className="stat-label">💸 Total Pendiente</div>
        </div>
      </div>

      {/* SOLICITUDES PENDIENTES */}
      <div className="solicitudes-section">
        <h3>⏳ Solicitudes Pendientes ({solicitudesPendientes.length})</h3>
        {solicitudesPendientes.length > 0 ? (
          <div className="tabla-wrapper">
            <table className="tabla-solicitudes">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Tipo</th>
                  <th>Monto</th>
                  <th>Saldo Disponible</th>
                  <th>Tipo Solicitud</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {solicitudesPendientes.map(solicitud => (
                  <tr key={solicitud.id} className="row-pendiente">
                    <td>
                      <div className="usuario-info">
                        <div className="nombre">{solicitud.nombre || 'N/A'}</div>
                        <div className="email">{solicitud.email || 'N/A'}</div>
                      </div>
                    </td>
                    <td>{getBadgeTipo(solicitud.beneficiario_tipo)}</td>
                    <td className="monto">
                      <strong>{solicitud.monto?.toFixed(2)}€</strong>
                    </td>
                    <td className="saldo">
                      {solicitud.credito_disponible?.toFixed(2)}€
                    </td>
                    <td>
                      <span className="badge badge-tipo">
                        {solicitud.tipo === 'retiro' ? '💰 Retiro' : '💳 Descuento'}
                      </span>
                    </td>
                    <td>{formatFecha(solicitud.fecha_solicitud)}</td>
                    <td className="acciones">
                      <button
                        className="btn-aprobar"
                        onClick={() => procesarSolicitud(solicitud.id, 'aprobar')}
                        disabled={procesando[solicitud.id]}
                      >
                        ✅ Aprobar
                      </button>
                      <button
                        className="btn-rechazar"
                        onClick={() => procesarSolicitud(solicitud.id, 'rechazar')}
                        disabled={procesando[solicitud.id]}
                      >
                        ❌ Rechazar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No hay solicitudes pendientes</div>
        )}
      </div>

      {/* SOLICITUDES APROBADAS */}
      {solicitudesAprobadas.length > 0 && (
        <div className="solicitudes-section">
          <h3>✅ Solicitudes Aprobadas ({solicitudesAprobadas.length})</h3>
          <div className="tabla-wrapper">
            <table className="tabla-solicitudes">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Tipo</th>
                  <th>Monto</th>
                  <th>Tipo Solicitud</th>
                  <th>Fecha Aprobación</th>
                </tr>
              </thead>
              <tbody>
                {solicitudesAprobadas.map(solicitud => (
                  <tr key={solicitud.id} className="row-aprobada">
                    <td>
                      <div className="usuario-info">
                        <div className="nombre">{solicitud.nombre || 'N/A'}</div>
                        <div className="email">{solicitud.email || 'N/A'}</div>
                      </div>
                    </td>
                    <td>{getBadgeTipo(solicitud.beneficiario_tipo)}</td>
                    <td className="monto">
                      <strong>{solicitud.monto?.toFixed(2)}€</strong>
                    </td>
                    <td>
                      <span className="badge badge-tipo">
                        {solicitud.tipo === 'retiro' ? '💰 Retiro' : '💳 Descuento'}
                      </span>
                    </td>
                    <td>{formatFecha(solicitud.fecha_respuesta)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* SOLICITUDES RECHAZADAS */}
      {solicitudesRechazadas.length > 0 && (
        <div className="solicitudes-section">
          <h3>❌ Solicitudes Rechazadas ({solicitudesRechazadas.length})</h3>
          <div className="tabla-wrapper">
            <table className="tabla-solicitudes">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Tipo</th>
                  <th>Monto</th>
                  <th>Tipo Solicitud</th>
                  <th>Fecha Rechazo</th>
                </tr>
              </thead>
              <tbody>
                {solicitudesRechazadas.map(solicitud => (
                  <tr key={solicitud.id} className="row-rechazada">
                    <td>
                      <div className="usuario-info">
                        <div className="nombre">{solicitud.nombre || 'N/A'}</div>
                        <div className="email">{solicitud.email || 'N/A'}</div>
                      </div>
                    </td>
                    <td>{getBadgeTipo(solicitud.beneficiario_tipo)}</td>
                    <td className="monto">
                      <strong>{solicitud.monto?.toFixed(2)}€</strong>
                    </td>
                    <td>
                      <span className="badge badge-tipo">
                        {solicitud.tipo === 'retiro' ? '💰 Retiro' : '💳 Descuento'}
                      </span>
                    </td>
                    <td>{formatFecha(solicitud.fecha_respuesta)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default RetirosCreditoPanel
